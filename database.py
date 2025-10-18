import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import logging

load_dotenv()

# 데이터베이스 연결 URL 가져오기
SQLALCHEMY_DATABASE_URL = os.getenv("DB_URL")

if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("DB_URL 환경 변수가 설정되지 않았습니다. .env 파일을 확인해주세요.")

# MySQL 엔진 생성
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,    # 연결 상태 확인
    pool_recycle=3600,     # 1시간마다 연결 재생성
    pool_size=10,          # 연결 풀 크기
    max_overflow=20,       # 최대 추가 연결 수
    echo=False             # SQL 로깅 (개발 시 True로 변경 가능)
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 로깅 설정
logger = logging.getLogger(__name__)

# 데이터베이스 세션 의존성 함수
def get_db():
    """데이터베이스 세션 생성 및 관리"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()