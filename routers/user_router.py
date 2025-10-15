from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import jwt
from datetime import datetime, timedelta
import datetime as dt
import os
from dotenv import load_dotenv

import models, schemas, hashing
from database import SessionLocal

# 환경변수 로드 및 시크릿키 세팅
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24시간

router = APIRouter(prefix="/api/users")

# DB 세션 의존성 주입
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/signup", status_code=201)
def user_signup(user_create: schemas.UserCreate, db: Session = Depends(get_db)):
    # 닉네임 중복 확인
    existing_nickname = db.query(models.User).filter(models.User.nickname == user_create.nickname).first()
    if existing_nickname:
        raise HTTPException(status_code=409, detail="이미 사용 중인 닉네임입니다.")

    # 이메일 중복 확인
    existing_email = db.query(models.User).filter(models.User.email == user_create.email).first()
    if existing_email:
        raise HTTPException(status_code=409, detail="이미 등록된 이메일입니다.")
    
    # 비밀번호 길이 체크 (72바이트 제한)
    if len(user_create.password.encode('utf-8')) > 72:
        raise HTTPException(status_code=400, detail="비밀번호가 너무 깁니다. 72바이트 이하로 입력해주세요.")
    
    # 비밀번호 해싱
    hashed_password = hashing.hash_password(user_create.password)

    # 데이터베이스에 사용자 생성
    new_user = models.User(
        nickname=user_create.nickname,
        username=user_create.username,
        password=hashed_password,
        email=user_create.email,
        gender=user_create.gender,
        create_date=dt.datetime.now()
    )
    db.add(new_user)
    db.commit()

    return {"message": "회원가입이 완료되었습니다."}

@router.post("/login", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # nickname으로 사용자 검색 (form_data.username 값을 nickname으로 해석)
    user = db.query(models.User).filter(models.User.nickname == form_data.username).first()
    
    if not user or not hashing.verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="닉네임 또는 비밀번호가 올바르지 않습니다.",  # 메시지도 변경
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # JWT 토큰 발급 (nickname 기반)
    data = {
        "sub": user.nickname,  # username 대신 nickname 사용
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    
    # 유저 정보 반환 (Pydantic 변환)
    user_obj = schemas.User.from_orm(user)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user_obj
    }

