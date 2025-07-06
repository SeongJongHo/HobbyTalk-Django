from datetime import datetime
from pydantic import BaseModel, Field

from common.utils import DataSerializer
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
class WebSocketMessageDto():
    message_type: str = Field(..., description="메시지 타입 (예: 'text')")
    message: str = Field(..., min_length=1, max_length=1000, description="메시지 내용 (1자 이상, 1000자 이하)")
    created_at: datetime = Field(default_factory=datetime.now, description="메시지 생성 시간")
    updated_at: datetime = Field(default_factory=datetime.now, description="메시지 수정 시간")
    deleted_at: datetime | None = Field(None, description="메시지 삭제 시간 (선택사항)")

class ChatMessageDto(WebSocketMessageDto):
    open_chat_id: int = Field(..., description="채팅 ID (NotEmpty)")
    sender_id: int = Field(..., description="보낸 사람 ID (NotEmpty)")

    def to_dict(self) -> dict:
        return {
            "message_type": self.message_type,
            "open_chat_id": self.open_chat_id,
            "message": self.message,
            "sender_id": self.sender_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "deleted_at": self.deleted_at if self.deleted_at else None
        }
    
    def to_json(self) -> str:
        return DataSerializer.serialize(self.to_dict())
    
class MessageDtoType:
    Text = "text"
    Image = "image"
    Video = "video"
    File = "file"

class JoinMessageDto(WebSocketMessageDto):
    joiner_id: int = Field(..., description="참여자 ID (NotEmpty)")
    last_message_id: int | None = Field(None, description="마지막 메시지 ID (선택사항)")

    def to_dict(self) -> dict:
        return {
            "message_type": MessageDtoType.Text,
            "message": self.message,
            "joiner_id": self.joiner_id,
            "last_message_id": self.last_message_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "deleted_at": self.deleted_at if self.deleted_at else None
        }
    def to_json(self) -> str:
        return DataSerializer.serialize(self.to_dict())
    
    @staticmethod
    def of(joiner_id: int, last_message_id: int = None) -> 'JoinMessageDto':
        message = f"User {joiner_id} has joined the chat room."
        return JoinMessageDto(joiner_id=joiner_id, message=message, last_message_id=last_message_id)

class ReadMessageDto(WebSocketMessageDto):
    open_chat_id: int = Field(..., description="채팅 ID (NotEmpty)")
    reader_id: int = Field(..., description="읽은 사용자 ID (NotEmpty)")

    def to_dict(self) -> dict:
        return {
            "message_type": self.message_type,
            "message": self.message,
            "open_chat_id": self.open_chat_id,
            "reader_id": self.reader_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "deleted_at": self.deleted_at if self.deleted_at else None
        }
    
    def to_json(self) -> str:
        return DataSerializer.serialize(self.to_dict())

class LeaveMessageDto(WebSocketMessageDto):
    leaver_id: int = Field(..., description="떠난 사용자 ID (NotEmpty)")

    def to_dict(self) -> dict:
        return {
            "message_type": self.message_type,
            "message": self.message,
            "leaver_id": self.leaver_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "deleted_at": self.deleted_at if self.deleted_at else None
        }