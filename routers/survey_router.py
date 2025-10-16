from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
import models, schemas
import json
import datetime
from routers.user_router import get_current_user   # 인증 함수 import

router = APIRouter(prefix="/api/survey")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/submit", status_code=201)
async def submit_survey(
    result: schemas.SurveyResultCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)  # 로그인 필수!
):
    if not current_user or not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="로그인 후 설문 응답만 가능합니다.")

    survey_result = models.SurveyResult(
        user_id=current_user.id,    # 반드시 로그인 사용자의 id 사용
        result_tone=result.result_tone,
        confidence=result.confidence,
        total_score=result.total_score,
        created_at=datetime.datetime.now()
    )
    db.add(survey_result)
    db.commit()
    db.refresh(survey_result)
    for ans in result.answers:
        answer = models.SurveyAnswer(
            survey_result_id=survey_result.id,
            question_id=ans.question_id,
            option_id=ans.option_id,
            option_label=ans.option_label,
            score_map=json.dumps(ans.score_map)
        )
        db.add(answer)
    db.commit()
    return {"message": "설문 결과 저장 완료", "survey_result_id": survey_result.id}

