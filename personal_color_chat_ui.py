# 통합 Streamlit + LLM 퍼스널컬러 챗봇 예제 (RAG 적용 버전)
# 실행: streamlit run personal_color_chat_ui.py
# 준비: os.getenv["OPENAI_API_KEY"]에 OpenAI API 키 설정
# 데이터 파일은 data/RAG 폴더에 위치:
#   - data/RAG/personal_color_RAG.txt (불변 지식: 퍼스널컬러 이론)
#   - data/RAG/beauty_trend_2025_autumn_RAG.txt (가변 지식: 2025 가을 최신 트렌드)

import os
from dotenv import load_dotenv
# .env 파일 로드
load_dotenv()
# 환경변수에서 API 키 가져오기
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# OpenAI 클라이언트 초기화 시 사용
from openai import OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)
import json
import time
import streamlit as st
from typing import Dict, Any, Tuple, List
from math import sqrt

# ======================================================================
# 파트 A) 공용 유틸리티 (RAG용 텍스트 분할/임베딩/검색)
# ======================================================================

def chunk_text(text: str, chunk_size: int = 800, overlap: int = 100) -> List[str]:
    """텍스트를 일정 길이로 안전하게 분할"""
    if overlap >= chunk_size:
        raise ValueError("overlap은 chunk_size보다 작아야 합니다.")
    chunks = []
    start = 0
    text_length = len(text)
    while start < text_length:
        end = min(start + chunk_size, text_length)
        chunks.append(text[start:end])
        if end == text_length:
            break
        start += (chunk_size - overlap)  # 안전한 전진
    return [c.strip() for c in chunks if c.strip()]

def cosine_similarity(a: List[float], b: List[float]) -> float:
    """코사인 유사도 계산"""
    dot = sum(x * y for x, y in zip(a, b))
    na = sqrt(sum(x * x for x in a)) or 1e-8
    nb = sqrt(sum(x * x for x in b)) or 1e-8
    return dot / (na * nb)

def embed_texts(client: OpenAI, texts: List[str], model: str = "text-embedding-3-small") -> List[List[float]]:
    """텍스트 리스트를 임베딩 벡터로 변환"""
    res = client.embeddings.create(model=model, input=texts)
    return [item.embedding for item in res.data]

def build_rag_index(client: OpenAI, filepath: str, chunk_size: int = 800, overlap: int = 100) -> Dict[str, Any]:
    """RAG 인덱스 생성"""
    with open(filepath, encoding="utf-8") as f:
        text = f.read()
    chunks = chunk_text(text, chunk_size=chunk_size, overlap=overlap)
    embeddings = embed_texts(client, chunks)
    return {"chunks": chunks, "embeddings": embeddings}

def top_k_chunks(query: str, index: Dict[str, Any], client: OpenAI, k: int = 3) -> List[str]:
    """쿼리와 가장 유사한 청크 Top-K 반환"""
    if not index or "embeddings" not in index or "chunks" not in index:
        return []
    q_emb = embed_texts(client, [query])[0]
    sims = [(cosine_similarity(q_emb, emb), i) for i, emb in enumerate(index["embeddings"])]
    sims.sort(reverse=True, key=lambda x: x[0])
    return [index["chunks"][i] for _, i in sims[:k]]

# ======================================================================
# 파트 B) 데이터/상태 클래스 및 LLM 챗봇 로직
# ======================================================================

class ChatState:
    INITIAL = "initial"
    COLLECTING = "collecting"
    ANALYZING = "analyzing"
    COMPLETE = "complete"

class PersonalColorResult:
    """퍼스널컬러 분석 결과 데이터 객체"""
    def __init__(self, primary_tone: str, sub_tone: str, description: str, recommendations: List[str]):
        self.primary_tone = primary_tone
        self.sub_tone = sub_tone
        self.description = description
        self.recommendations = recommendations

    def to_dict(self) -> Dict[str, Any]:
        return {
            "primary_tone": self.primary_tone,
            "sub_tone": self.sub_tone,
            "description": self.description,
            "recommendations": self.recommendations
        }

class LLMPersonalColorChatbot:
    """LLM 기반 퍼스널컬러 챗봇"""
    def __init__(self, client: OpenAI, model: str = "gpt-4o-mini"):
        self.client = client
        self.model = model
        self.state: str = ChatState.INITIAL
        self.collected_data: Dict[str, Any] = {"answers": []}
        self.last_question: str = ""

    def start_new_session(self) -> str:
        self.state = ChatState.COLLECTING
        self.collected_data = {"answers": []}
        self.last_question = ""
        return "안녕하세요! 🎨 퍼스널컬러 진단을 시작합니다. 간단한 질문을 드릴게요. 준비되셨나요?"

    def _call_llm(self, messages: List[Dict[str, str]], temperature: float = 0.7, max_tokens: int = 400):
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception:
            return None

    def process_message(self, user_message: str, temperature: float = 0.7, max_tokens: int = 400) -> str:
        timestamp = int(time.time())
        self.collected_data.setdefault("answers", []).append({"text": user_message, "timestamp": timestamp})

        prompt_system = "당신은 퍼스널컬러 전문 상담사입니다. ..."
        prompt_user = (
            f"지금까지 수집된 정보: {self.collected_data}\n"
            f"사용자의 최신 답변: {user_message}\n\n"
            "다음 단계로 자연스럽게 이어갈 질문을 해주세요."
        )

        messages = [{"role": "system", "content": prompt_system}, {"role": "user", "content": prompt_user}]
        answer = self._call_llm(messages, temperature=temperature, max_tokens=max_tokens)
        if answer is None:
            return "⚠️ 모델 호출 중 오류가 발생했습니다."
        return answer

    def get_final_report(self, temperature: float = 0.3, max_tokens: int = 800) -> Tuple[str, PersonalColorResult]:
        answers = [a.get("text", "") for a in self.collected_data.get("answers", [])]
        query = " / ".join(answers).strip() or "퍼스널컬러 진단 기준"

        fixed_index = st.session_state.get("fixed_index")
        trend_index = st.session_state.get("trend_index")

        fixed_chunks = top_k_chunks(
            query, fixed_index, self.client, k=st.session_state.get("top_k", 3)
        ) if fixed_index else []

        trend_chunks = top_k_chunks(
            query, trend_index, self.client, k=st.session_state.get("top_k", 3)
        ) if trend_index else []

        # ✅ 프롬프트 강화: 불변/가변 지식 구분해서 리포트에 반영하도록 지시
        prompt_system = (
            "당신은 퍼스널컬러 전문가이자 최신 패션 트렌드 컨설턴트입니다. "
            "사용자의 답변을 분석하고, 퍼스널컬러 이론(기본 원칙)과 최신 트렌드(보완 설명)를 "
            "자연스럽게 연결해 하나의 완성된 문장으로 설명하세요. "
            "딱딱한 나열이 아니라, 전문가가 조언하듯 부드럽게 작성하세요. "
            "JSON 형식으로만 답변하세요."
        )

        prompt_user = (
            "[관련 지식 컨텍스트]\n"
            + "\n".join(fixed_chunks + trend_chunks) + "\n\n"
            f"[사용자 답변 요약]\n{query}\n\n"
            "반드시 다음 JSON 필드만 포함해 반환하세요:\n"
            "- primary_tone: '웜' 또는 '쿨'\n"
            "- sub_tone: '봄'/'여름'/'가을'/'겨울'\n"
            "- description: 퍼스널컬러 기본 원칙과 최신 트렌드를 자연스럽게 연결한 설명 (완성된 문장)\n"
            "- recommendations: 3~6개의 짧은 문장형 추천 (예: '브라운 니트는 따뜻한 인상을 줍니다.', "
            "'블랙 코트는 세련된 분위기를 더해줍니다.')\n\n"
            "출력 예시:\n"
            "{\n"
            "  \"primary_tone\": \"웜\",\n"
            "  \"sub_tone\": \"가을\",\n"
            "  \"description\": \"가을 웜톤에는 따뜻한 브라운 계열이 잘 어울립니다. 마침 2025년 가을 트렌드도 브라운과 블랙이 중심이니, 기본 원칙과 트렌드를 함께 살려 스타일링해 보세요.\",\n"
            "  \"recommendations\": [\n"
            "    \"브라운 니트는 따뜻한 인상을 줍니다.\",\n"
            "    \"블랙 코트는 세련된 분위기를 더해줍니다.\",\n"
            "    \"카멜색 가방은 포인트 아이템으로 적합합니다.\"\n"
            "  ]\n"
            "}\n"
        )

        messages = [
            {"role": "system", "content": prompt_system},
            {"role": "user", "content": prompt_user}
        ]

        content = self._call_llm(messages, temperature=temperature, max_tokens=max_tokens)


        if content is None:
            return "⚠️ 최종 리포트 생성 오류", None

        start, end = content.find("{"), content.rfind("}")
        if start == -1 or end == -1 or end <= start:
            return "⚠️ JSON을 찾을 수 없습니다.", None

        try:
            data = json.loads(content[start:end+1])
        except json.JSONDecodeError:
            return "⚠️ JSON 파싱 오류", None

        primary = data.get("primary_tone", "")
        sub = data.get("sub_tone", "")
        description = data.get("description", "")
        recommendations = data.get("recommendations", [])
        # 타입 보정
        if not isinstance(recommendations, list):
            if isinstance(recommendations, str):
                recommendations = [r.strip() for r in recommendations.split(",") if r.strip()]
            else:
                recommendations = []

        result = PersonalColorResult(primary, sub, description, recommendations)
        final_message = f"✨ 퍼스널컬러 진단 결과: {result.primary_tone} - {result.sub_tone} ✨\n\n{result.description}"
        return final_message, result

# ======================================================================
# 파트 C) Streamlit 앱 초기화 및 세션 상태
# ======================================================================

st.set_page_config(page_title="퍼스널컬러 챗봇 (LLM+RAG)", page_icon="🎨", layout="centered")
st.title("🎨 퍼스널컬러 챗봇 (LLM + RAG 연동)")
st.markdown("퍼스널컬러 이론(불변 지식)과 최신 트렌드(가변 지식)를 결합해 맞춤 리포트를 제공합니다.")

# OpenAI 클라이언트 초기화
if os.getenv("OPENAI_API_KEY") is None:
    st.error("OpenAI API 키가 설정되어 있지 않습니다. os.getenv['OPENAI_API_KEY']에 키를 설정해 주세요.")
    st.stop()

try:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
except Exception as e:
    st.error(f"OpenAI 클라이언트 초기화 중 오류가 발생했습니다: {e}")
    st.stop()

# 데이터 경로
DATA_DIR = os.path.join("data", "RAG")
FIXED_PATH = os.path.join(DATA_DIR, "personal_color_RAG.txt")
TREND_PATH = os.path.join(DATA_DIR, "beauty_trend_2025_autumn_RAG.txt")

# 세션 상태 초기화
if "pc_chatbot" not in st.session_state:
    st.session_state.pc_chatbot = LLMPersonalColorChatbot(client=client)
    st.session_state.messages = []
    st.session_state.last_report = None
    st.session_state.show_report_expander = False
    st.session_state.is_dialog_complete = False
    st.session_state.temperature = 0.7
    st.session_state.max_tokens = 400
    first_question = st.session_state.pc_chatbot.start_new_session()
    st.session_state.messages.append({"role": "assistant", "content": first_question})

# ======================================================================
# 파트 D) 사이드바: 설정 + RAG 인덱스 빌드/리셋
# ======================================================================

with st.sidebar:
    st.header("설정")
    st.session_state.temperature = st.slider(
        "Temperature", min_value=0.0, max_value=1.0,
        value=st.session_state.get("temperature", 0.7), step=0.05
    )
    st.session_state.max_tokens = st.number_input(
        "Max tokens", min_value=50, max_value=2000,
        value=st.session_state.get("max_tokens", 400), step=50
    )

    st.markdown("---")
    st.subheader("RAG 옵션")
    st.session_state.chunk_size = st.number_input(
        "Chunk size", min_value=200, max_value=2000,
        value=st.session_state.get("chunk_size", 800), step=100
    )
    st.session_state.overlap = st.number_input(
        "Chunk overlap", min_value=0, max_value=500,
        value=st.session_state.get("overlap", 100), step=50
    )
    st.session_state.top_k = st.slider(
        "Top-K 검색 개수", min_value=1, max_value=10,
        value=st.session_state.get("top_k", 3), step=1
    )

    st.markdown("---")
    st.subheader("RAG 인덱스")
    if st.button("RAG 인덱스 생성/갱신"):
        try:
            st.session_state.fixed_index = build_rag_index(
                client, FIXED_PATH,
                chunk_size=st.session_state.chunk_size,
                overlap=st.session_state.overlap
            )
            st.session_state.trend_index = build_rag_index(
                client, TREND_PATH,
                chunk_size=st.session_state.chunk_size,
                overlap=st.session_state.overlap
            )
            st.success("RAG 인덱스가 생성/갱신되었습니다.")
            st.rerun()
        except Exception as e:
            st.error(f"인덱스 생성 중 오류: {e}")

    fixed_ready = "fixed_index" in st.session_state
    trend_ready = "trend_index" in st.session_state
    st.caption(f"불변 지식 인덱스: {'✅ 준비됨' if fixed_ready else '❌ 없음'}")
    st.caption(f"가변 지식 인덱스: {'✅ 준비됨' if trend_ready else '❌ 없음'}")

    st.markdown("---")
    st.subheader("테스트/디버그")
    if st.button("강제로 최종 리포트 생성"):
        st.session_state.pc_chatbot.state = ChatState.ANALYZING
        # ✅ 토큰 여유를 넉넉히 확보 (최소 800)
        max_tokens_val = max(800, st.session_state.max_tokens)
        final_message, result = st.session_state.pc_chatbot.get_final_report(
            temperature=st.session_state.temperature,
            max_tokens=max_tokens_val
        )
        if result:
            st.session_state.last_report = result.to_dict()
            st.session_state.is_dialog_complete = True
            st.session_state.messages.append({"role": "assistant", "content": final_message})
            st.success("최종 리포트가 생성되었습니다.")
        else:
            st.error(final_message)

    if st.button("새 대화 시작"):
        st.session_state.pc_chatbot.start_new_session()
        st.session_state.messages = []
        msg = st.session_state.pc_chatbot.start_new_session()
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.session_state.last_report = None
        st.session_state.show_report_expander = False
        st.session_state.is_dialog_complete = False
        st.rerun()

# ======================================================================
# 파트 E) 채팅 UI 및 대화 흐름
# ======================================================================

# ✅ 상단 안내문 추가
st.info("💡 언제든지 채팅창에 **'리포트 생성'** 이라고 입력하면 즉시 최종 진단 리포트를 확인할 수 있습니다.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

input_disabled = st.session_state.is_dialog_complete
placeholder = "진단이 완료되었습니다. '새 대화 시작'을 눌러주세요." if input_disabled else "메시지를 입력하세요..."

if user_input := st.chat_input(placeholder, disabled=input_disabled):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    chatbot: LLMPersonalColorChatbot = st.session_state.pc_chatbot

    # ✅ 시동어 '리포트 생성' 감지
    if user_input.strip() == "리포트 생성":
        chatbot.state = ChatState.ANALYZING
        max_tokens_val = max(800, st.session_state.max_tokens)
        final_message, result_obj = chatbot.get_final_report(
            temperature=st.session_state.temperature,
            max_tokens=max_tokens_val
        )
        if result_obj:
            st.session_state.last_report = result_obj.to_dict()
            st.session_state.is_dialog_complete = True
            st.session_state.show_report_expander = True
            st.session_state.messages.append({"role": "assistant", "content": final_message})
            with st.chat_message("assistant"):
                st.markdown(final_message)
        else:
            st.session_state.messages.append({"role": "assistant", "content": final_message})
            with st.chat_message("assistant"):
                st.markdown(final_message)
        st.rerun()

    else:
        # ✅ 일반 대화 처리 (COMPLETE 감지 제거됨)
        bot_response = chatbot.process_message(
            user_input,
            temperature=st.session_state.temperature,
            max_tokens=st.session_state.max_tokens
        )
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        with st.chat_message("assistant"):
            st.markdown(bot_response)

    st.rerun()

# ======================================================================
# 파트 F) 완료 UI: 리포트 상세 보기 및 재시작
# ======================================================================

if st.session_state.is_dialog_complete and st.session_state.last_report:
    with st.expander("🔍 퍼스널컬러 리포트", expanded=st.session_state.show_report_expander):
        report = st.session_state.last_report

        # 톤 정보는 강조 카드 스타일로
        st.markdown(
            f"""
            <div style="padding:12px; border-radius:8px; background-color:#f0f2f6; margin-bottom:12px;">
                <b>기본 톤:</b> {report.get('primary_tone','-')}<br>
                <b>세부 톤:</b> {report.get('sub_tone','-')}
            </div>
            """,
            unsafe_allow_html=True
        )

        # 전문가 진단은 본문 스타일
        st.markdown("### AI 전문가 진단")
        st.markdown(f"> {report.get('description','-')}")

        # 추천 스타일은 카드 리스트 느낌으로
        st.markdown("### 추천 스타일")
        recs = report.get("recommendations", [])
        if recs:
            for rec in recs:
                st.markdown(
                    f"""
                    <div style="padding:10px; margin:6px 0; border-left:4px solid #4CAF50; background-color:#fafafa; border-radius:4px;">
                        {rec}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.markdown("- (추천 없음)")

    if st.button("새 대화 시작"):
        st.session_state.pc_chatbot.start_new_session()
        st.session_state.messages = []
        msg = st.session_state.pc_chatbot.start_new_session()
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.session_state.last_report = None
        st.session_state.show_report_expander = False
        st.session_state.is_dialog_complete = False
        st.rerun()

if not st.session_state.messages:
    msg = st.session_state.pc_chatbot.start_new_session()
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.rerun()