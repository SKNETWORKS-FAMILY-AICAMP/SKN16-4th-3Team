from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import datetime

from database import SessionLocal
import models, schemas, hashing

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
    
    # 비밀번호 해싱
    hashed_password = hashing.hash_password(user_create.password)

    # 데이터베이스에 사용자 생성
    new_user = models.User(
        nickname=user_create.nickname,
        username=user_create.username,
        password=hashed_password,
        email=user_create.email,
        gender=user_create.gender,
        create_date=datetime.datetime.now()
    )
    db.add(new_user)
    db.commit()

    return {"message": "회원가입이 완료되었습니다."}