#!/usr/bin/env python3
"""
MySQL 데이터베이스 관리 스크립트
사용법:
  python db_manager.py init     # 데이터베이스 초기화
  python db_manager.py check    # 데이터베이스 상태 확인
  python db_manager.py reset    # 데이터베이스 리셋 (주의!)
  python db_manager.py create   # 데이터베이스만 생성
"""
import sys
import logging
from sqlalchemy import text
from database import engine, Base
from db_init import initialize_database, check_database_connection, check_tables_exist, create_database_if_not_exists

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def init_database():
    """데이터베이스 초기화"""
    logger.info("📊 데이터베이스를 초기화합니다...")
    success = initialize_database()
    if success:
        logger.info("✅ 데이터베이스 초기화가 완료되었습니다!")
    else:
        logger.error("❌ 데이터베이스 초기화에 실패했습니다.")
    return success

def create_database():
    """MySQL 데이터베이스만 생성"""
    logger.info("🗄️ MySQL 데이터베이스를 생성합니다...")
    success = create_database_if_not_exists()
    if success:
        print("✅ MySQL 데이터베이스가 성공적으로 생성되었습니다!")
    else:
        print("❌ MySQL 데이터베이스 생성에 실패했습니다.")
        print("💡 MySQL 서버 실행 상태와 연결 정보를 확인해주세요.")
    return success

def check_database():
    """MySQL 데이터베이스 상태 확인"""
    logger.info("🔍 MySQL 데이터베이스 상태를 확인합니다...")
    
    # 연결 확인
    connection_ok = check_database_connection()
    
    # 테이블 확인
    tables_ok = check_tables_exist() if connection_ok else False
    
    # 결과 출력
    print("\n" + "="*60)
    print("📊 MySQL 데이터베이스 상태 보고서")
    print("="*60)
    print(f"🔗 MySQL 서버 연결: {'✅ 정상' if connection_ok else '❌ 실패'}")
    print(f"📋 테이블 상태: {'✅ 모든 테이블 존재' if tables_ok else '❌ 누락된 테이블 있음'}")
    
    if connection_ok and tables_ok:
        print("🎉 MySQL 데이터베이스가 정상적으로 구성되어 있습니다!")
    elif connection_ok and not tables_ok:
        print("⚠️ MySQL 연결은 정상이지만 테이블이 누락되었습니다.")
        print("💡 'python db_manager.py init' 명령어로 테이블을 생성하세요.")
    else:
        print("🚨 MySQL 데이터베이스 연결에 문제가 있습니다.")
        print("💡 다음 사항들을 확인해주세요:")
        print("   1. MySQL 서버가 실행 중인가?")
        print("   2. .env 파일의 DB_URL이 올바른가?")
        print("   3. MySQL 사용자 권한이 적절한가?")
    
    print("="*60)
    return connection_ok and tables_ok

def reset_database():
    """데이터베이스 리셋 (주의: 모든 데이터 삭제!)"""
    print("🚨 경고: 이 작업은 모든 테이블과 데이터를 삭제합니다!")
    
    # 사용자 확인
    confirm = input("정말로 데이터베이스를 리셋하시겠습니까? (yes/no): ").lower().strip()
    if confirm != 'yes':
        print("❌ 데이터베이스 리셋이 취소되었습니다.")
        return False
    
    try:
        logger.info("🗑️ 모든 테이블을 삭제합니다...")
        Base.metadata.drop_all(bind=engine)
        logger.info("✅ 테이블 삭제 완료!")
        
        logger.info("🔨 새로운 테이블을 생성합니다...")
        Base.metadata.create_all(bind=engine)
        logger.info("✅ 테이블 생성 완료!")
        
        print("🎉 데이터베이스 리셋이 완료되었습니다!")
        return True
        
    except Exception as e:
        logger.error(f"❌ 데이터베이스 리셋 실패: {e}")
        return False

def show_help():
    """도움말 출력"""
    print("""
🛠️ MySQL 데이터베이스 관리 도구

사용법:
  python db_manager.py <명령어>

명령어:
  create   MySQL 데이터베이스만 생성
  init     데이터베이스 초기화 (데이터베이스 + 테이블 생성)
  check    데이터베이스 상태 확인
  reset    데이터베이스 리셋 (모든 데이터 삭제 후 재생성)
  help     이 도움말 출력

예시:
  python db_manager.py create   # MySQL 데이터베이스만 생성
  python db_manager.py init     # 전체 초기화
  python db_manager.py check    # 상태 확인
  
📝 환경 변수 설정 (.env 파일):
  DB_HOST=localhost
  DB_PORT=3306
  DB_USER=root
  DB_PASSWORD=your_password
  DB_NAME=personal_color_db
    """)

def main():
    """메인 함수"""
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == 'create':
        create_database()
    elif command == 'init':
        init_database()
    elif command == 'check':
        check_database()
    elif command == 'reset':
        reset_database()
    elif command in ['help', '-h', '--help']:
        show_help()
    else:
        print(f"❌ 알 수 없는 명령어: {command}")
        show_help()

if __name__ == "__main__":
    main()
