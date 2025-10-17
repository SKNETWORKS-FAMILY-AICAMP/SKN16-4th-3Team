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

# OpenAI API 클라이언트 초기화
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

router = APIRouter(prefix="/api/survey")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def analyze_personal_color_with_openai(answers: list[schemas.SurveyAnswerCreate]) -> dict:
    """
    사용자의 답변을 OpenAI API로 분석하여 퍼스널 컬러 타입 결정
    
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
    
    prompt = f"""당신은 퍼스널 컬러 진단 전문가입니다.

아래는 사용자가 퍼스널 컬러 테스트에 응답한 내용입니다:

{answers_text}

이 답변들을 기반으로 사용자의 퍼스널 컬러 타입을 분석하세요.

분석 결과는 다음 형식으로 JSON으로 반드시 응답해주세요:
{{
    "result_tone": "spring|summer|autumn|winter 중 하나",
    "confidence": 0-100 사이의 숫자 (신뢰도 퍼센트),
    "total_score": 0-100 사이의 숫자 (종합 점수)
}}

응답은 반드시 JSON 형식만 포함해야 합니다. 다른 설명은 포함하지 마세요."""

    try:
        # OpenAI API 호출
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "당신은 퍼스널 컬러 진단 전문가입니다."},
                {"role": "user", "content": prompt}
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
        
        # 결과 검증
        if result.get("result_tone") not in ["spring", "summer", "autumn", "winter"]:
            result["result_tone"] = "spring"
        
        result["confidence"] = max(0, min(100, int(result.get("confidence", 50))))
        result["total_score"] = max(0, min(100, int(result.get("total_score", 50))))
        
        return result
        
    except json.JSONDecodeError as e:
        print(f"JSON 파싱 오류: {e}")
        # JSON 파싱 실패 시 기본값 반환
        return {
            "result_tone": "spring",
            "confidence": 50,
            "total_score": 50
        }
    except Exception as e:
        print(f"OpenAI API 호출 오류: {e}")
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
    2. OpenAI API에 답변 데이터를 prompt로 전송
    3. OpenAI에서 result_tone, confidence, total_score 받음
    4. DB에 저장
    """
    if not current_user or not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="로그인 후 설문 응답만 가능합니다."
        )

    # OpenAI API 호출로 result_tone, confidence, total_score 받기
    openai_result = analyze_personal_color_with_openai(result.answers)
    result_tone = openai_result['result_tone']
    confidence = openai_result['confidence']
    total_score = openai_result['total_score']

    # Survey Result 생성
    survey_result = models.SurveyResult(
        user_id=current_user.id,
        result_tone=result_tone,
        confidence=confidence,
        total_score=total_score,
        created_at=datetime.now(timezone.utc)
    )
    db.add(survey_result)
    db.flush()  # ID 생성을 위해 flush
    
    # 모든 답변 저장
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
