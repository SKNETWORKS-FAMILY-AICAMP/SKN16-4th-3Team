from sqlalchemy import Column, Integer, String, DateTime, Enum, Boolean, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
import datetime
from database import Base

class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False)  # unique, index 제거
    nickname = Column(String(50), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    gender = Column(Enum("여성", "남성", name="gender_enum"), nullable=True)
    create_date = Column(DateTime, default=datetime.datetime.now)
    is_active = Column(Boolean, default=True)  # > is_deleted -> is_active 변경  

# 퍼스널컬러 진단 설문 저장용 모델 추가

class SurveyResult(Base):
    __tablename__ = "survey_result"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.now)
    result_tone = Column(String(20))  # spring/summer/autumn/winter
    confidence = Column(Float)
    total_score = Column(Integer)
    answers = relationship("SurveyAnswer", back_populates="result")

class SurveyAnswer(Base):
    __tablename__ = "survey_answer"
    id = Column(Integer, primary_key=True, index=True)
    survey_result_id = Column(Integer, ForeignKey("survey_result.id"))
    question_id = Column(String(50))
    option_id = Column(String(50))
    option_label = Column(String(255))
    score_map = Column(Text)  # JSON 문자열
    result = relationship("SurveyResult", back_populates="answers")