import re
from typing import Optional

from common.exceptions import ValidationException
from users.commands import CreateUserCommand
from pydantic import Field, BaseModel

class SignUpDto(BaseModel):
    nickname: str = Field(..., min_length=1, description="별명 (NotEmpty)")
    password: str = Field(
        ...,
        min_length=8,
        description="비밀번호는 8자 이상의 영문, 숫자, 특수문자 조합이어야 합니다."
    )
    password_confirm: str = Field(
        ...,
        min_length=8,
        description="비밀번호 확인은 8자 이상의 영문, 숫자, 특수문자 조합이어야 합니다."
    )
    username: str = Field(..., min_length=1, description="사용자 이름 (NotEmpty)")
    phone_number: str = Field(
        ...,
        min_length=10,
        max_length=11,
        pattern=r'^\d{10,11}$',
        description="전화번호는 10~11자리 숫자여야 합니다."
    )
    profile_image: Optional[str] = Field(None, description="프로필 이미지 URL (Nullable)")
    role: str = Field(
        "USER",
        description="사용자 역할 (기본값: USER, 선택사항: ADMIN)"
    )

    @classmethod
    def _validate_password(cls, value: str) -> str:
        if not re.search(r'[A-Za-z]', value):
            raise ValidationException("비밀번호에는 영문자가 포함되어야 합니다.")
        if not re.search(r'\d', value):
            raise ValidationException("비밀번호에는 숫자가 포함되어야 합니다.")
        if not re.search(r'[@#$%^&+=!]', value):
            raise ValidationException("비밀번호에는 특수문자가 포함되어야 합니다.")
        return value

    def __init__(self, **data):
        data['password'] = self._validate_password(data.get('password', ''))
        data['password_confirm'] = self._validate_password(data.get('password_confirm', ''))
        super().__init__(**data)

    def to_command(self, hashed_password: str) -> CreateUserCommand:
        return CreateUserCommand(
            nickname=self.nickname,
            password=hashed_password,
            username=self.username,
            phone_number=self.phone_number,
            profile_image=self.profile_image
        )