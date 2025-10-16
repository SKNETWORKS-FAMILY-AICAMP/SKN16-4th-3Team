from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import SessionLocal
import models, schemas
import json
import datetime

router = APIRouter(prefix="/api/survey")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/submit", status_code=201)
def submit_survey(result: schemas.SurveyResultCreate, db: Session = Depends(get_db)):
    survey_result = models.SurveyResult(
        user_id=result.user_id,
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
