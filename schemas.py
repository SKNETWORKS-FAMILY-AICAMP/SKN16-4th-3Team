from datetime import datetime
from pydantic import BaseModel, Field, model_validator
from typing import List, Dict, Optional, Literal
import re

class UserCreate(BaseModel):
    nickname: str = Field(min_length=2, max_length=14)
    username: str
    password: str = Field(min_length=8, max_length=16)
    password_confirm: str
    email: str = Field(pattern=r'^[^@]+@[^@]+\.[^@]+$')
    gender: Literal['남성', '여성'] | None = None

    @model_validator(mode='after')
    def validate_all_fields(self):
        if not (2 <= len(self.nickname) <= 14):
            raise ValueError('닉네임은 2자 이상 14자 이하로 입력해주세요.')
        if ' ' in self.nickname:
            raise ValueError('닉네임에 공백이 있어 안됩니다.')
        if not re.match(r'^[a-zA-Z0-9가-힣]+$', self.nickname):
            raise ValueError('닉네임에는 한글, 영문, 숫자만 사용 가능합니다.')
        forbidden_words = ["운영자", "관리자", "admin"]
        if any(word in self.nickname.lower() for word in forbidden_words):
            raise ValueError('닉네임에 금지된 단어를 포함할 수 없습니다.')
        allowed_special = r'!"#$%()*+,-./:;<=>?@\[\]^_`{|}~'
        conditions = [
            re.search(r'[a-zA-Z]', self.password),
            re.search(r'\d', self.password),
            re.search(f'[{allowed_special}]', self.password)
        ]
        if sum(1 for c in conditions if c) < 2:
            raise ValueError('비밀번호는 영문, 숫자, 특수문자 중 2가지 이상을 조합해야 합니다.')
        if re.search(rf'[^a-zA-Z0-9{allowed_special}]', self.password):
            raise ValueError('비밀번호에 허용되지 않은 특수문자가 포함되어 있습니다.')
        if re.search(r'(\w)\1{3,}', self.password):
            raise ValueError('비밀번호에 4자리 이상 동일한 문자를 연속으로 사용할 수 없습니다.')
        if self.password != self.password_confirm:
            raise ValueError('비밀번호가 일치하지 않습니다.')
        return self

class User(BaseModel):
    id: int
    username: str
    nickname: str
    email: str
    gender: Literal['남성', '여성'] | None = None
    create_date: datetime
    is_active: bool

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: User

class SurveyAnswerCreate(BaseModel):
    """
    사용자의 답변 데이터 (프론트엔드에서 전송)
    - score_map, confidence, total_score는 OpenAI에서 받을 예정
    """
    question_id: int
    option_id: str
    option_label: str

class SurveyResultCreate(BaseModel):
    """
    퍼스널 컬러 테스트 결과 생성 스키마
    - answers: 모든 질문에 대한 답변 데이터만 포함
    - OpenAI API에서 받을 데이터:
      - result_tone: spring, summer, autumn, winter
      - confidence: 0-1 사이의 신뢰도
      - total_score: 종합 점수
    """
    answers: List[SurveyAnswerCreate]  # 사용자의 모든 답변

class SurveyAnswer(BaseModel):
    """
    저장된 사용자 답변 (DB에서 조회)
    """
    id: int
    survey_result_id: int
    question_id: int
    option_id: str
    option_label: str
    score_map: Dict[str, int]

    class Config:
        from_attributes = True

class SurveyResult(BaseModel):
    """
    설문 결과 응답 스키마
    - 사용자의 과거 모든 설문 결과를 포함
    """
    id: int
    user_id: Optional[int]
    created_at: datetime
    result_tone: str
    confidence: float
    total_score: int
    answers: List[SurveyAnswer] = []

    class Config:
        from_attributes = True
