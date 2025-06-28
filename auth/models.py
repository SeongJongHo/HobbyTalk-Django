from common.utils import DataSerializer


class CurrentUser:
    def __init__(self, user_id: int, role: str, refresh_token: str):
        self.user_id = user_id
        self.role = role
        self.refresh_token = refresh_token

    def to_dict(self) -> dict:
        return {
            'user_id': self.user_id,
            'role': self.role,
            'refresh_token': self.refresh_token
        }
    
    def to_json(self) -> str:
        return DataSerializer.serialize(self.to_dict())
    
    @staticmethod
    def of(data: dict) -> 'CurrentUser':
        return CurrentUser(
            user_id=data.get('user_id'),
            role=data.get('role'),
            refresh_token=data.get('refresh_token')
        )