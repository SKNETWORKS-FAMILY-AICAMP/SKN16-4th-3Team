# 🎨 퍼스널컬러 진단 서비스

SKN 16기 4차 단위프로젝트 - AI 기반 퍼스널컬러 진단 웹 애플리케이션

## 🚀 빠른 시작

### 필수 요구사항

- **Python**: 3.11+

### 1. 환경 설정

```bash
# 프로젝트 클론
git clone <repository-url>
cd SKN16-4th-3Team

# 백엔드 의존성 설치
pip install -r requirements.txt
```

📝 환경 변수 설정 (.env 파일):
DB_URL=your_db_url_here
OPENAI_API_KEY=your_openai_api_key_here
SECRET_KEY=your_secret_key_here

### 3. MySQL 데이터베이스 설정

#### 📋 사전 준비사항

- **MySQL 서버 설치 및 실행**
- **MySQL 사용자 계정 생성** (필요시)

#### 🔧 데이터베이스 초기화

```bash
# 방법 1: 서버 실행 시 자동 초기화 (권장)
python run.py

# 방법 2: 수동 데이터베이스 관리
python db_manager.py create  # MySQL 데이터베이스만 생성
python db_manager.py init    # 데이터베이스 + 테이블 전체 초기화
python db_manager.py check   # MySQL 연결 및 테이블 상태 확인
python db_manager.py reset   # 완전 리셋 (주의: 모든 데이터 삭제!)
```

#### ⚠️ MySQL 연결 문제 해결

```bash
# 1. MySQL 서버 상태 확인
brew services list | grep mysql  # macOS
sudo service mysql status        # Ubuntu

# 2. MySQL 서버 시작
brew services start mysql        # macOS
sudo service mysql start         # Ubuntu

# 3. MySQL 접속 테스트
mysql -h localhost -u root -p
```

### 4. 서버 실행

```bash
# 개발 서버 실행
python run.py

# 또는 직접 uvicorn 실행
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

서버가 실행되면 http://127.0.0.1:8000 에서 API에 접근할 수 있습니다.

### 5. 프론트엔드 실행

```bash
# 프론트엔드 폴더로 이동
cd frontend

# 의존성 설치
npm install

# 개발 서버 실행
npm run dev
```

프론트엔드는 http://localhost:5173 에서 실행됩니다.

## 📁 프로젝트 구조

```
SKN16-4th-3Team/
├── 📂 backend/
│   ├── main.py              # FastAPI 메인 애플리케이션
│   ├── run.py               # 서버 실행 스크립트
│   ├── database.py          # 데이터베이스 설정
│   ├── models.py            # SQLAlchemy 모델
│   ├── schemas.py           # Pydantic 스키마
│   ├── db_init.py           # 데이터베이스 초기화
│   ├── db_manager.py        # 데이터베이스 관리 도구
│   ├── requirements.txt     # Python 의존성
│   └── 📂 routers/          # API 라우터
│       ├── user_router.py   # 사용자 인증 API
│       ├── survey_router.py # 설문조사 API
│       └── chatbot_router.py # 챗봇 API
├── 📂 frontend/             # React 프론트엔드
│   ├── src/                 # 소스 코드
│   ├── package.json         # Node.js 의존성
│   └── README.md            # 프론트엔드 가이드
├── 📂 data/                 # RAG 데이터
└── .env                     # 환경 변수
```
