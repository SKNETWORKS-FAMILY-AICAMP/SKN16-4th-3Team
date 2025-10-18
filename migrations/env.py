from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import os
from dotenv import load_dotenv

# 추가된 import
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

# .env 파일 로드
load_dotenv()

# versions 폴더가 없으면 자동 생성
versions_dir = os.path.join(os.path.dirname(__file__), 'versions')
if not os.path.exists(versions_dir):
    os.makedirs(versions_dir)
    print(f"📁 Created missing versions directory: {versions_dir}")

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# models import 및 metadata 설정
from models import Base
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    # 환경변수에서 DB URL 가져오기
    url = os.getenv("DB_URL")
    if not url:
        url = config.get_main_option("sqlalchemy.url")
    
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    # 환경변수에서 DB URL 가져오기
    db_url = os.getenv("DB_URL")
    
    if db_url:
        # 환경변수가 있으면 직접 엔진 생성
        from sqlalchemy import create_engine
        connectable = create_engine(db_url)
    else:
        # 환경변수가 없으면 기본 설정 사용
        connectable = engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()