from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import json

# routers 폴더의 user_router를 import
from routers import user_router
from routers import chatbot_router
from routers import survey_router

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

# RequestValidationError 핸들러 추가 (422 에러 상세 정보)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print(f"❌ 422 Validation Error from {request.url}")
    print(f"❌ Errors: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={
            "detail": exc.errors(),
        },
    )

# user_router.py에 있는 API들을 앱에 포함
app.include_router(user_router.router)
app.include_router(chatbot_router.router)
app.include_router(survey_router.router)
