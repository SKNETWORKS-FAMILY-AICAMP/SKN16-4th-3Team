"""
MySQL 데이터베이스 초기화 및 관리 유틸리티
"""
import os
import logging
import pymysql
from sqlalchemy import text, inspect, create_engine
from database import engine, Base, SQLALCHEMY_DATABASE_URL
import models

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_database_if_not_exists():
    """MySQL 데이터베이스가 존재하지 않으면 생성"""
    try:
        # .env 파일의 DB_URL에서 연결 정보 추출
        db_url = os.getenv("DB_URL")
        if not db_url:
            logger.error("❌ DB_URL 환경 변수가 설정되지 않았습니다.")
            return False
        
        # DB_URL 파싱
        if not db_url.startswith("mysql+pymysql://"):
            logger.error("❌ MySQL URL 형식이 올바르지 않습니다.")
            return False
            
        # URL에서 정보 추출
        import re
        pattern = r'mysql\+pymysql://([^:]+):([^@]+)@([^:/]+)(?::(\d+))?/(.+)'
        match = re.match(pattern, db_url)
        
        if not match:
            logger.error("❌ DB_URL 파싱 실패")
            return False
            
        DB_USER = match.group(1)
        DB_PASSWORD = match.group(2)
        DB_HOST = match.group(3)
        DB_PORT = int(match.group(4) or "3306")
        DB_NAME = match.group(5)

        # 데이터베이스 없이 MySQL 서버에 연결
        connection = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            charset='utf8mb4'
        )
        
        with connection:
            with connection.cursor() as cursor:
                # 데이터베이스 존재 확인
                cursor.execute(f"SHOW DATABASES LIKE '{DB_NAME}'")
                result = cursor.fetchone()
                
                if not result:
                    # 데이터베이스 생성
                    cursor.execute(f"CREATE DATABASE {DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
                    logger.info(f"✅ MySQL 데이터베이스 '{DB_NAME}'가 생성되었습니다.")
                else:
                    logger.info(f"📊 MySQL 데이터베이스 '{DB_NAME}'가 이미 존재합니다.")
                    
            connection.commit()
        
        return True
        
    except Exception as e:
        logger.error(f"❌ MySQL 데이터베이스 생성 실패: {e}")
        return False

def check_database_connection():
    """MySQL 데이터베이스 연결 확인"""
    try:
        # 먼저 데이터베이스가 존재하는지 확인하고 없으면 생성
        if not create_database_if_not_exists():
            return False
            
        # SQLAlchemy 엔진으로 연결 테스트
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        logger.info("✅ MySQL 데이터베이스 연결이 성공적으로 확인되었습니다.")
        return True
    except Exception as e:
        logger.error(f"❌ MySQL 데이터베이스 연결 실패: {e}")
        logger.error("💡 MySQL 서버가 실행 중인지, 연결 정보가 올바른지 확인해주세요.")
        return False

def check_tables_exist():
    """테이블 존재 여부 확인"""
    try:
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()
        
        # 필요한 테이블 목록
        required_tables = ['user', 'survey_result', 'survey_answer']
        
        missing_tables = [table for table in required_tables if table not in existing_tables]
        
        if missing_tables:
            logger.info(f"📋 누락된 테이블: {missing_tables}")
            return False
        else:
            logger.info("✅ 모든 필요한 테이블이 존재합니다.")
            return True
            
    except Exception as e:
        logger.error(f"❌ 테이블 확인 실패: {e}")
        return False

def create_tables():
    """데이터베이스 테이블 생성"""
    try:
        # 1. 데이터베이스 연결 확인
        if not check_database_connection():
            raise Exception("데이터베이스 연결을 확인할 수 없습니다.")
        
        # 2. 테이블 존재 여부 확인
        if check_tables_exist():
            logger.info("🎯 데이터베이스 테이블이 이미 존재합니다. 스킵합니다.")
            return True
        
        # 3. 테이블 생성
        logger.info("🔨 데이터베이스 테이블을 생성합니다...")
        Base.metadata.create_all(bind=engine)
        
        # 4. 생성 확인
        if check_tables_exist():
            logger.info("✅ 데이터베이스 테이블이 성공적으로 생성되었습니다.")
            return True
        else:
            raise Exception("테이블 생성 후 확인에 실패했습니다.")
            
    except Exception as e:
        logger.error(f"❌ 데이터베이스 테이블 생성 실패: {e}")
        raise e

def initialize_database():
    """MySQL 데이터베이스 전체 초기화"""
    try:
        # DB_URL 환경 변수 확인
        db_url = os.getenv("DB_URL")
        if not db_url:
            logger.error("❌ DB_URL 환경 변수가 설정되지 않았습니다.")
            return False
        
        logger.info(f"📊 MySQL 데이터베이스 연결 중...")
        
        # 테이블 생성
        return create_tables()
        
    except Exception as e:
        logger.error(f"❌ MySQL 데이터베이스 초기화 실패: {e}")
        return False

if __name__ == "__main__":
    # 직접 실행 시 데이터베이스 초기화
    initialize_database()
