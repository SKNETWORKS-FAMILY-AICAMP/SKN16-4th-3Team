import os
from dotenv import load_dotenv
# .env 파일 로드
load_dotenv()
# 환경변수에서 API 키 가져오기
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# OpenAI 클라이언트 초기화 시 사용
from openai import OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)
import io
import json
import time
import re
import streamlit as st
from typing import List, Dict, Any, Tuple
from math import sqrt

# ---------------- 유틸 함수 ----------------
def chunk_text(text: str, chunk_size: int = 800, overlap: int = 100) -> List[str]:
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
        # ✅ 무한루프 방지: start를 앞으로 전진
        start += (chunk_size - overlap)
    return [c.strip() for c in chunks if c.strip()]

def cosine_similarity(a: List[float], b: List[float]) -> float:
    dot = sum(x*y for x,y in zip(a,b))
    na = sqrt(sum(x*x for x in a)) or 1e-8
    nb = sqrt(sum(x*x for x in b)) or 1e-8
    return dot / (na * nb)

def embed_texts(client: OpenAI, texts: List[str], model: str = "text-embedding-3-small") -> List[List[float]]:
    """텍스트 리스트를 임베딩 벡터로 변환"""
    res = client.embeddings.create(model=model, input=texts)
    return [item.embedding for item in res.data]

def top_k_chunks(query: str, index: Dict[str, Any], client: OpenAI, k: int = 5) -> List[str]:
    """쿼리와 가장 유사한 청크 Top-K 반환"""
    q_emb = embed_texts(client, [query])[0]
    sims = [(cosine_similarity(q_emb, emb), i) for i, emb in enumerate(index["embeddings"])]
    sims.sort(reverse=True, key=lambda x: x[0])
    return [index["chunks"][i] for _, i in sims[:k]]

# ---------------- RAG 초기화 ----------------
def build_rag_index(client: OpenAI, filepath: str) -> Dict[str, Any]:
    """txt 파일을 읽어 청크 분할 후 임베딩 인덱스 생성"""
    with open(filepath, encoding="utf-8") as f:
        text = f.read()
    chunks = chunk_text(text, chunk_size=800, overlap=100)
    embeddings = embed_texts(client, chunks)
    return {"chunks": chunks, "embeddings": embeddings}

# ---------------- LLM + RAG 리포트 생성 ----------------
def generate_report_with_rag(client: OpenAI, user_answers: List[str],
                             fixed_index: Dict[str, Any], trend_index: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
    """사용자 답변 + RAG 검색 결과를 기반으로 최종 리포트 생성"""
    query = " / ".join(user_answers)

    # 불변 지식에서 관련 청크 검색
    fixed_chunks = top_k_chunks(query, fixed_index, client, k=3) if fixed_index else []
    # 가변 지식에서 관련 청크 검색
    trend_chunks = top_k_chunks(query, trend_index, client, k=3) if trend_index else []

    prompt_system = (
        "당신은 퍼스널컬러 전문가이자 최신 패션 트렌드 컨설턴트입니다. "
        "사용자의 답변을 분석하고, 퍼스널컬러 이론(불변 지식)과 최신 트렌드(가변 지식)를 모두 반영하여 "
        "최종 진단 리포트를 JSON 형식으로 작성하세요."
    )

    prompt_user = f"""
사용자 답변 요약:
{query}

[불변 지식 관련 컨텍스트]
{chr(10).join(fixed_chunks)}

[가변 지식 관련 컨텍스트]
{chr(10).join(trend_chunks)}

위 정보를 종합하여 JSON 형식으로 결과를 반환하세요:
- primary_tone: '웜' 또는 '쿨'
- sub_tone: '봄'/'여름'/'가을'/'겨울'
- description: 퍼스널컬러 특징 설명 (불변 지식 기반)
- recommendations: 추천 색상/스타일 (최신 트렌드 반영)
"""

    messages = [
        {"role": "system", "content": prompt_system},
        {"role": "user", "content": prompt_user}
    ]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.3,
        max_tokens=600
    )
    content = response.choices[0].message.content

    # JSON 추출
    start = content.find("{")
    end = content.rfind("}")
    if start == -1 or end == -1:
        return "⚠️ JSON 결과를 찾을 수 없습니다.", None

    try:
        data = json.loads(content[start:end+1])
    except json.JSONDecodeError:
        return "⚠️ JSON 파싱 오류", None

    final_message = f"✨ 퍼스널컬러 진단 결과: {data.get('primary_tone')} - {data.get('sub_tone')} ✨\n\n{data.get('description')}"
    return final_message, data

# ---------------- Streamlit 데모 ----------------
st.title("🎨 퍼스널컬러 챗봇 (RAG 적용 데모)")

if os.getenv("OPENAI_API_KEY") is None:
    raise ValueError("OPENAI_API_KEY 환경변수가 설정되지 않았습니다.")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# RAG 인덱스 생성 (앱 시작 시 1회)
if "fixed_index" not in st.session_state:
    st.session_state.fixed_index = build_rag_index(client, "data/RAG/personal_color_RAG.txt")
if "trend_index" not in st.session_state:
    st.session_state.trend_index = build_rag_index(client, "data/RAG/beauty_trend_2025_autumn_RAG.txt")

# 사용자 입력
user_input = st.text_input("퍼스널컬러 진단을 위해 답변을 입력하세요 (예: 피부가 노르스름하고 갈색 머리를 자주 염색해요)")

if st.button("리포트 생성") and user_input:
    answers = [user_input]
    final_message, report = generate_report_with_rag(
        client,
        answers,
        st.session_state.fixed_index,
        st.session_state.trend_index
    )
    st.write(final_message)
    if report:
        st.json(report)