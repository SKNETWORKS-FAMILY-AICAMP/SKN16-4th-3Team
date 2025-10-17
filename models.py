from sqlalchemy import Column, Integer, String, DateTime, Enum, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
import datetime
from database import Base

class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False)
    nickname = Column(String(50), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    gender = Column(Enum("여성", "남성", name="gender_enum"), nullable=True)
    create_date = Column(DateTime, default=datetime.datetime.now)
    is_active = Column(Boolean, default=True)

class SurveyResult(Base):
    __tablename__ = "survey_result"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
    result_tone = Column(String(20))
    confidence = Column(String(20))
    total_score = Column(Integer)

    user = relationship("User", backref="survey_results")
    answers = relationship("SurveyAnswer", back_populates="survey", cascade="all, delete-orphan")

class SurveyAnswer(Base):
    __tablename__ = "survey_answer"
    id = Column(Integer, primary_key=True, index=True)
    survey_result_id = Column(Integer, ForeignKey("survey_result.id"), nullable=False)
    question_id = Column(String(100), nullable=False)
    option_id = Column(String(100), nullable=False)
    option_label = Column(Text, nullable=False)
    score_map = Column(Text, nullable=True)

    survey = relationship("SurveyResult", back_populates="answers")
