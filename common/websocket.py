from common.exceptions import InvalidValueException
from common.utils import DataSerializer


class MessageType:
    JOIN = 'join'
    LEAVE = 'leave'
    MESSAGE = 'message'
    READ = 'read'
    ERROR = 'error'

    @staticmethod
    def is_valid(message_type: str) -> bool:
        return message_type in {
            MessageType.JOIN,
            MessageType.LEAVE,
            MessageType.MESSAGE,
            MessageType.READ,
            MessageType.ERROR
        }

class WebSocketMessage:
    def __init__(self, message_type: str, content):
        self.message_type = message_type
        if not MessageType.is_valid(message_type):
            raise InvalidValueException(f"Invalid message type: {message_type}")
        self.content = content
    
    def to_dict(self):
        return {
            'type': self.message_type,
            'content': self.content
        }
    
    def to_json(self):
        return DataSerializer.serialize(self.to_dict())
    
    @staticmethod
    def of(json: str) -> 'WebSocketMessage':
        data = DataSerializer.deserialize(json)
        message_type = data.get('type')
        content = data.get('content', {})

        if not MessageType.is_valid(message_type):
            raise InvalidValueException(f"Invalid message type: {message_type}")
        
        return WebSocketMessage(message_type, content)