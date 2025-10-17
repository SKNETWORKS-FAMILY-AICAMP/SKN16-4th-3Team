from pydantic import BaseModel, Field, model_validator
from datetime import datetime
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
        # 닉네임 길이 검증 (커스텀 메시지)
        if not (2 <= len(self.nickname) <= 14):
            raise ValueError('닉네임은 2자 이상 14자 이하로 입력해주세요.')
        # 닉네임에 공백 포함 시 에러
        if ' ' in self.nickname:
            raise ValueError('닉네임에 공백이 있어 안됩니다.')
        # 닉네임 검증
        if not re.match(r'^[a-zA-Z0-9가-힣]+$', self.nickname):
            raise ValueError('닉네임에는 한글, 영문, 숫자만 사용 가능합니다.')
        
        forbidden_words = ["운영자", "관리자", "admin"]
        if any(word in self.nickname.lower() for word in forbidden_words):
            raise ValueError('닉네임에 금지된 단어를 포함할 수 없습니다.')
        
        # 비밀번호 검증
        allowed_special = r'!"#$%()*+,-./:;<=>?@\[\]^_`{|}~'
        conditions = [
            re.search(r'[a-zA-Z]', self.password),
            re.search(r'\d', self.password),
            re.search(f'[{allowed_special}]', self.password)
        ]
        if sum(1 for c in conditions if c) < 2:
            raise ValueError('비밀번호는 영문, 숫자, 특수문자 중 2가지 이상을 조합해야 합니다.')
        # 허용된 특수문자만 사용 가능
        if re.search(rf'[^a-zA-Z0-9{allowed_special}]', self.password):
            raise ValueError('비밀번호에 허용되지 않은 특수문자가 포함되어 있습니다.')
        
        # 4자리 이상 동일한 문자/숫자 연속 사용 금지
        if re.search(r'(\w)\1{3,}', self.password):
            raise ValueError('비밀번호에 4자리 이상 동일한 문자를 연속으로 사용할 수 없습니다.')
        
        # 비밀번호 확인
        if self.password != self.password_confirm:
            raise ValueError('비밀번호가 일치하지 않습니다.')
        
        return self
class User(BaseModel):
    id: int
    username: str
    nickname: str
    email: str
    gender: str | None = None
    create_date: datetime.datetime
    is_active: bool

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: User
