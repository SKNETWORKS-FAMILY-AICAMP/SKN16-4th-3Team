from sqlalchemy import Column, Integer, String, DateTime, Enum, Boolean
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
    is_deleted = Column(Boolean, default=False)  # 소프트 딜리트용 필드 추가