import os
import uvicorn
import logging
from dotenv import load_dotenv
from db_init import initialize_database

# 환경 변수 로드
load_dotenv()

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "8000"))

if __name__ == "__main__":
    logger.info("🚀 퍼스널컬러 진단 서버를 시작합니다...")
    
    # 서버 실행 전 데이터베이스 초기화
    logger.info("📊 데이터베이스를 초기화합니다...")
    try:
        if initialize_database():
            logger.info("✅ 데이터베이스 초기화 완료!")
        else:
            logger.warning("⚠️ 데이터베이스 초기화에 문제가 있습니다.")
    except Exception as e:
        logger.error(f"❌ 데이터베이스 초기화 실패: {e}")
        logger.info("🔄 서버는 계속 실행됩니다. 수동으로 데이터베이스를 확인해주세요.")
    
    # 서버 실행
    logger.info(f"🌐 서버 실행: http://{HOST}:{PORT}")
    uvicorn.run("main:app", host=HOST, port=PORT, reload=True)