from sqlalchemy import text
from database import engine

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT DATABASE();"))
        db_name = result.scalar()
        print(f"연결 성공! 현재 데이터베이스: {db_name}")
except Exception as e:
    print(f"연결 실패: {e}")