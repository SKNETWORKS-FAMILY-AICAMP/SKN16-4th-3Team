from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# routers 폴더의 user_router를 import
from routers import user_router

app = FastAPI()

origins = [
    "http://localhost:5173", # React 개발 서버 주소
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "퍼스널컬러 진단 AI 백엔드 서버"}

# user_router.py에 있는 API들을 앱에 포함
app.include_router(user_router.router)