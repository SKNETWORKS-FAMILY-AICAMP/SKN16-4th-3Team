from pydantic import BaseModel, field_validator, Field
import re

class UserCreate(BaseModel):
    # --- 필드 정의 ---
    nickname: str
    username: str
    password: str = Field(min_length=8, max_length=16)
    password_confirm: str
    email: str
    gender: str | None = None  # 선택적 필드

    # --- 닉네임 유효성 검사 ---
    @field_validator('nickname')
    def validate_nickname(cls, value):
        if not (2 <= len(value) <= 14):
            raise ValueError('닉네임은 2자 이상 14자 이하로 입력해주세요.')
        if not re.match(r'^[a-zA-Z0-9가-힣]+$', value):
            raise ValueError('닉네임에는 한글, 영문, 숫자만 사용 가능하며 공백과 특수문자는 사용할 수 없습니다.')
        forbidden_words = ["운영자", "관리자", "admin"]
        if any(word in value.lower() for word in forbidden_words):
            raise ValueError('닉네임에 금지된 단어를 포함할 수 없습니다.')
        return value

    # --- 비밀번호 유효성 검사 ---
    @field_validator('password')
    def validate_password(cls, value):
        conditions = [
            re.search(r'[a-zA-Z]', value),
            re.search(r'\d', value),
            re.search(r'[!#$%()*+,-./:;<=>?@\[\]^_`{|}~]', value)
        ]
        if sum(1 for c in conditions if c) < 2:
            raise ValueError('비밀번호는 영문, 숫자, 특수문자 중 2가지 이상을 조합해야 합니다.')
        if re.search(r'(.)\1\1\1', value):
            raise ValueError('비밀번호에 4자리 이상 동일한 문자를 연속으로 사용할 수 없습니다.')
        return value

    # --- 비밀번호 확인 검사 ---
    @field_validator('password_confirm')
    def passwords_match(cls, value, values):
        if 'password' in values and value != values['password']:
            raise ValueError('비밀번호가 일치하지 않습니다.')
        return value

    # --- 이메일 형식 검사 ---
    @field_validator('email')
    def validate_email(cls, value):
        if not re.match(r'[^@]+@[^@]+\.[^@]+', value):
            raise ValueError('유효하지 않은 이메일 형식입니다.')
        return value