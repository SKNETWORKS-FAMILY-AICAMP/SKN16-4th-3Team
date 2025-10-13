from pydantic import BaseModel, Field, model_validator
import re

class UserCreate(BaseModel):
    nickname: str = Field(min_length=2, max_length=14)
    username: str
    password: str = Field(min_length=8, max_length=16)
    password_confirm: str
    email: str = Field(pattern=r'^[^@]+@[^@]+\.[^@]+$')
    gender: str | None = None

    @model_validator(mode='after')
    def validate_all_fields(self):
        # 닉네임 검증
        if not re.match(r'^[a-zA-Z0-9가-힣]+$', self.nickname):
            raise ValueError('닉네임에는 한글, 영문, 숫자만 사용 가능합니다.')
        
        forbidden_words = ["운영자", "관리자", "admin"]
        if any(word in self.nickname.lower() for word in forbidden_words):
            raise ValueError('닉네임에 금지된 단어를 포함할 수 없습니다.')
        
        # 비밀번호 검증
        conditions = [
            re.search(r'[a-zA-Z]', self.password),
            re.search(r'\d', self.password),
            re.search(r'[!#$%()*+,-./:;<=>?@\[\]^_`{|}~]', self.password)
        ]
        if sum(1 for c in conditions if c) < 2:
            raise ValueError('비밀번호는 영문, 숫자, 특수문자 중 2가지 이상을 조합해야 합니다.')
        
        # 비밀번호 확인
        if self.password != self.password_confirm:
            raise ValueError('비밀번호가 일치하지 않습니다.')
        
        return self