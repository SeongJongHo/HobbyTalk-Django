from users.models import User


class CreateUserCommand:
    nickname: str
    phone_number: str
    username: str
    password: str
    profile_image: str | None = None

    def __init__(self, nickname: str, phone_number: str, username: str, password: str, profile_image: str | None = None):
        self.nickname = nickname
        self.phone_number = phone_number
        self.username = username
        self.password = password
        self.profile_image = profile_image

    def to_model(self):
        return User(
            nickname=self.nickname,
            phone_number=self.phone_number,
            username=self.username,
            password=self.password,
            profile_image=self.profile_image
        )