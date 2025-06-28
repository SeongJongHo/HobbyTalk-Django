from pydantic import BaseModel, Field

from open_chats.models import OpenChatRoom


class CreateOpenChatRoomDto(BaseModel):
    title: str = Field(..., description="채팅방 제목 (NotEmpty)")
    notice: str | None = Field(None, description="공지사항 (선택사항)")
    category_id: int = Field(..., description="카테고리 ID (NotEmpty)")
    maximum_capacity: int = Field(2, ge=1, description="최대 수용 인원 (기본값: 2, 최소 1명 이상)")
    password: str | None = Field(
        None,
        min_length=1,
        max_length=255,
        description="채팅방 비밀번호 (선택사항, 1자 이상)"
    )

    def to_model(self, manager_id: int, hashed_password: str=None) -> OpenChatRoom:
        DEFAULT_CURRENT_ATTENDANCE = 1

        return OpenChatRoom(
            title=self.title,
            notice=self.notice,
            category_id=self.category_id,
            maximum_capacity=self.maximum_capacity,
            current_attendance=DEFAULT_CURRENT_ATTENDANCE,
            password=hashed_password,
            manager_id=manager_id
        )