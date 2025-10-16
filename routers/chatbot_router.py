# routers/chatbot_router.py

import os
import json
from typing import List, Dict, Any
from math import sqrt

from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv

import models
from routers.user_router import get_current_user

# 환경변수 로드(OpenAI API 키)
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("환경변수 OPENAI_API_KEY가 설정되지 않았습니다.")

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=OPENAI_API_KEY)

router = APIRouter(prefix="/api/chatbot", tags=["Chatbot"])


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
        start += (chunk_size - overlap)
    return [c.strip() for c in chunks if c.strip()]


def cosine_similarity(a: List[float], b: List[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = sqrt(sum(x * x for x in a)) or 1e-8
    nb = sqrt(sum(x * x for x in b)) or 1e-8
    return dot / (na * nb)


def embed_texts(client: OpenAI, texts: List[str], model: str = "text-embedding-3-small") -> List[List[float]]:
    res = client.embeddings.create(model=model, input=texts)
    return [item.embedding for item in res.data]


def top_k_chunks(query: str, index: Dict[str, Any], client: OpenAI, k: int = 3) -> List[str]:
    q_emb = embed_texts(client, [query])[0]
    sims = [(cosine_similarity(q_emb, emb), i) for i, emb in enumerate(index["embeddings"])]
    sims.sort(reverse=True, key=lambda x: x[0])
    return [index["chunks"][i] for _, i in sims[:k]]


def build_rag_index(client: OpenAI, filepath: str) -> Dict[str, Any]:
    with open(filepath, encoding="utf-8") as f:
        text = f.read()
    chunks = chunk_text(text, chunk_size=800, overlap=100)
    embeddings = embed_texts(client, chunks)
    return {"chunks": chunks, "embeddings": embeddings}


# 서버 시작 시 RAG 인덱스 1회 생성
fixed_index = build_rag_index(client, "data/RAG/personal_color_RAG.txt")
trend_index = build_rag_index(client, "data/RAG/beauty_trend_2025_autumn_RAG.txt")


# ---------------- 요청/응답 스키마 ----------------
class ChatbotRequest(BaseModel):
    answers: List[str]


class ChatbotResponse(BaseModel):
    primary_tone: str
    sub_tone: str
    description: str
    recommendations: List[str]


# ---------------- 헬스체크 엔드포인트 ----------------
@router.get("/health")
def health_check(current_user: models.User = Depends(get_current_user)):
    return {"status": "ok", "message": "Chatbot API is running"}


# ---------------- 챗봇 분석 엔드포인트 ----------------
@router.post("/analyze", response_model=ChatbotResponse)
def analyze_personal_color(
    request: ChatbotRequest,
    current_user: models.User = Depends(get_current_user)
):
    query = " / ".join(request.answers).strip()
    if not query:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="answers 배열에 하나 이상의 답변이 필요합니다."
        )

    # RAG 검색
    fixed_chunks = top_k_chunks(query, fixed_index, client, k=3)
    trend_chunks = top_k_chunks(query, trend_index, client, k=3)

    # 시스템 프롬프트
    prompt_system = (
        "당신은 퍼스널컬러 전문가이자 최신 패션 트렌드 컨설턴트입니다. "
        "사용자의 답변을 분석하고, 퍼스널컬러 이론(불변 지식)과 최신 트렌드(가변 지식)를 모두 반영하여 "
        "최종 진단 리포트를 JSON 형식으로 작성하세요."
    )

    # 사용자 프롬프트
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

    # LLM 호출
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.3,
            max_tokens=600
        )
        content = response.choices[0].message.content
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"LLM 호출 오류: {str(e)}"
        )

    # JSON 결과 추출
    start = content.find("{")
    end = content.rfind("}")
    if start == -1 or end == -1:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="JSON 결과를 찾을 수 없습니다."
        )

    try:
        data = json.loads(content[start:end+1])
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="JSON 파싱 오류"
        )
    
    recs = data.get("recommendations")
    if isinstance(recs, dict):
        # 'colors' 키가 있으면 그 값을, 없으면 첫 값 리스트로
        data["recommendations"] = recs.get("colors") or list(recs.values())[0]
    if not isinstance(data["recommendations"], list):
        data["recommendations"] = []

    return ChatbotResponse(**data)
