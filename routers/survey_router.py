from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
import models, schemas
import json
from datetime import datetime, timezone
from routers.user_router import get_current_user   # 인증 함수 import
import os
from openai import OpenAI
import re
from typing import List, Dict, Any
from math import sqrt
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("환경변수 OPENAI_API_KEY가 설정되지 않았습니다.")

client = OpenAI(api_key=OPENAI_API_KEY)

router = APIRouter(prefix="/api/survey")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ============ RAG 관련 유틸 함수 ============
def chunk_text(text: str, chunk_size: int = 800, overlap: int = 100) -> List[str]:
    """텍스트를 청크로 분할"""
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
    """코사인 유사도 계산"""
    dot = sum(x * y for x, y in zip(a, b))
    na = sqrt(sum(x * x for x in a)) or 1e-8
    nb = sqrt(sum(x * x for x in b)) or 1e-8
    return dot / (na * nb)

def embed_texts(texts: List[str], model: str = "text-embedding-3-small") -> List[List[float]]:
    """텍스트를 임베딩으로 변환"""
    res = client.embeddings.create(model=model, input=texts)
    return [item.embedding for item in res.data]

def top_k_chunks(query: str, index: Dict[str, Any], k: int = 3) -> List[str]:
    """쿼리와 유사한 상위 k개 청크 검색"""
    q_emb = embed_texts([query])[0]
    sims = [(cosine_similarity(q_emb, emb), i) for i, emb in enumerate(index["embeddings"])]
    sims.sort(reverse=True, key=lambda x: x[0])
    return [index["chunks"][i] for _, i in sims[:k]]

def build_rag_index(filepath: str) -> Dict[str, Any]:
    """RAG 인덱스 구축"""
    try:
        with open(filepath, encoding="utf-8") as f:
            text = f.read()
        chunks = chunk_text(text, chunk_size=800, overlap=100)
        embeddings = embed_texts(chunks)
        return {"chunks": chunks, "embeddings": embeddings}
    except FileNotFoundError:
        print(f"⚠️ RAG 파일을 찾을 수 없습니다: {filepath}")
        return {"chunks": [], "embeddings": []}

# RAG 인덱스 빌드 (앱 시작 시 한 번만 실행)
try:
    personal_color_index = build_rag_index("data/RAG/personal_color_RAG.txt")
    beauty_trend_index = build_rag_index("data/RAG/beauty_trend_2025_autumn_RAG.txt")
except Exception as e:
    print(f"⚠️ RAG 인덱스 빌드 오류: {e}")
    personal_color_index = {"chunks": [], "embeddings": []}
    beauty_trend_index = {"chunks": [], "embeddings": []}

def analyze_personal_color_with_openai(answers: list[schemas.SurveyAnswerCreate]) -> dict:
    """
    사용자의 답변을 OpenAI API로 분석하여 퍼스널 컬러 타입 결정
    RAG를 활용하여 컨텍스트 기반 분석 수행
    
    Returns:
        {
            'result_tone': 'spring'|'summer'|'autumn'|'winter',
            'confidence': 0-100 (신뢰도 퍼센트),
            'total_score': 0-100 (종합 점수)
        }
    """
    
    # 프롬프트 구성 - 사용자의 답변을 명확하게 전달
    answers_text = "\n".join([
        f"Q{ans.question_id}: {ans.option_label}"
        for ans in answers
    ])
    
    # RAG 검색으로 관련 정보 가져오기
    rag_context = ""
    if personal_color_index["chunks"]:
        related_chunks = top_k_chunks(answers_text, personal_color_index, k=3)
        rag_context = "\n\n[퍼스널 컬러 참고 정보]\n" + "\n".join(related_chunks)
    
    # 트렌드 정보도 추가
    trend_context = ""
    if beauty_trend_index["chunks"]:
        trend_chunks = top_k_chunks(answers_text, beauty_trend_index, k=2)
        trend_context = "\n\n[최신 뷰티 트렌드]\n" + "\n".join(trend_chunks)
    
    system_prompt = (
        "당신은 전문적인 퍼스널 컬러 진단 컨설턴트입니다. "
        "사용자의 답변을 기반으로 가장 적합한 퍼스널 컬러 타입을 정확하게 진단해주세요. "
        "봄, 여름, 가을, 겨울 중 정확히 하나의 타입만 선택해야 하며, "
        "진단 신뢰도와 종합 점수를 객관적으로 평가해주세요."
    )
    
    user_prompt = f"""사용자의 퍼스널 컬러 테스트 답변:

{answers_text}
{rag_context}
{trend_context}

이 답변들을 기반으로 사용자의 퍼스널 컬러 타입을 분석하세요.

분석 결과는 다음 형식으로 JSON으로 반드시 응답해주세요:
{{
    "result_tone": "spring|summer|autumn|winter 중 정확히 하나",
    "confidence": 0-100 사이의 숫자 (신뢰도 퍼센트, 진단의 확실성 정도),
    "total_score": 0-100 사이의 숫자 (종합 점수, 타입 특성의 부합도)
}}

응답은 반드시 JSON 형식만 포함해야 합니다. 다른 설명은 포함하지 마세요."""

    try:
        # OpenAI API 호출
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        # 응답 파싱
        response_text = response.choices[0].message.content.strip()
        
        # JSON 추출 (혹시 다른 텍스트가 포함될 경우 대비)
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            response_text = json_match.group()
        
        result = json.loads(response_text)
        
        # 결과 검증 및 정규화
        if result.get("result_tone") not in ["spring", "summer", "autumn", "winter"]:
            result["result_tone"] = "spring"
        
        result["confidence"] = max(0, min(100, int(result.get("confidence", 50))))
        result["total_score"] = max(0, min(100, int(result.get("total_score", 50))))
        
        print(f"✅ OpenAI 분석 완료: {result}")
        return result
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON 파싱 오류: {e}")
        # JSON 파싱 실패 시 기본값 반환
        return {
            "result_tone": "spring",
            "confidence": 50,
            "total_score": 50
        }
    except Exception as e:
        print(f"❌ OpenAI API 호출 오류: {e}")
        # API 오류 시 기본값 반환
        return {
            "result_tone": "spring",
            "confidence": 50,
            "total_score": 50
        }

# TODO: survey API 구현 필요. 현재 정상 동작 X
@router.post("/submit", status_code=201)
async def submit_survey(
    result: schemas.SurveyResultCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    퍼스널 컬러 테스트 결과 제출
    
    프로세스:
    1. 프론트엔드에서 사용자 답변 데이터만 받음
    2. OpenAI API에 답변 데이터를 prompt로 전송 (RAG 컨텍스트 포함)
    3. OpenAI에서 result_tone, confidence, total_score 받음
    4. DB에 설문 결과 및 답변 저장
    
    Request Body (PersonalColorTest 컴포넌트에서 전송):
        {
            "answers": [
                {
                    "question_id": 1,
                    "option_id": "q1_opt_a",
                    "option_label": "밝고 생기 있는 피부"
                },
                ...
            ]
        }
    
    Response:
        {
            "message": "설문 결과 저장 완료",
            "survey_result_id": 123,
            "result_tone": "spring",
            "confidence": 85,
            "total_score": 88
        }
    """
    
    # 사용자 인증 확인
    if not current_user or not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="로그인 후 설문 응답만 가능합니다."
        )
    
    # 답변 데이터 검증
    if not result.answers or len(result.answers) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="답변 데이터가 필요합니다."
        )
    
    print(f"▶ 사용자 {current_user.username}({current_user.id})의 설문 제출")
    print(f"▶ 받은 답변 수: {len(result.answers)}")
    print(f"▶ 받은 데이터: {result}")

    # 1. OpenAI API 호출로 result_tone, confidence, total_score 받기
    print("▶ OpenAI API로 퍼스널 컬러 분석 중...")
    openai_result = analyze_personal_color_with_openai(result.answers)
    result_tone = openai_result['result_tone']
    confidence = openai_result['confidence']
    total_score = openai_result['total_score']
    
    print(f"✅ 분석 완료 - tone: {result_tone}, confidence: {confidence}, score: {total_score}")

    # 2. Survey Result 생성
    survey_result = models.SurveyResult(
        user_id=current_user.id,
        result_tone=result_tone,
        confidence=confidence,
        total_score=total_score,
        created_at=datetime.now(timezone.utc)
    )
    db.add(survey_result)
    db.flush()  # ID 생성을 위해 flush
    
    print(f"▶ SurveyResult 생성: ID {survey_result.id}")
    
    # 3. 모든 답변 저장
    for ans in result.answers:
        answer = models.SurveyAnswer(
            survey_result_id=survey_result.id,
            question_id=ans.question_id,
            option_id=ans.option_id,
            option_label=ans.option_label
        )
        db.add(answer)
    
    db.commit()
    db.refresh(survey_result)
    
    print(f"✅ 설문 결과 저장 완료 - Survey ID: {survey_result.id}")
    
    return {
        "message": "설문 결과 저장 완료", 
        "survey_result_id": survey_result.id,
        "result_tone": result_tone,
        "confidence": confidence,
        "total_score": total_score
    }

@router.get("/list", response_model=list[schemas.SurveyResult])
async def get_my_survey_results(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    현재 사용자의 모든 설문 결과 조회 (최신순)
    """
    if not current_user or not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="로그인이 필요합니다."
        )

    results = db.query(models.SurveyResult).filter(
        models.SurveyResult.user_id == current_user.id
    ).order_by(models.SurveyResult.created_at.desc()).all()
    
    return results

@router.get("/{survey_id}", response_model=schemas.SurveyResult)
async def get_survey_detail(
    survey_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    특정 설문 결과 상세 조회
    """
    if not current_user or not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="로그인이 필요합니다."
        )

    result = db.query(models.SurveyResult).filter(
        models.SurveyResult.id == survey_id,
        models.SurveyResult.user_id == current_user.id
    ).first()
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="설문 결과를 찾을 수 없습니다."
        )
    
    return result

@router.delete("/{survey_id}", status_code=200)
async def delete_survey(
    survey_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    설문 결과 삭제 (본인이 작성한 것만)
    """
    if not current_user or not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="로그인이 필요합니다."
        )

    result = db.query(models.SurveyResult).filter(
        models.SurveyResult.id == survey_id,
        models.SurveyResult.user_id == current_user.id
    ).first()
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="설문 결과를 찾을 수 없습니다."
        )
    
    db.delete(result)
    db.commit()
    
    return {"message": "설문 결과가 삭제되었습니다."}
