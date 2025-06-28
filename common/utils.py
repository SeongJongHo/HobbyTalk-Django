import json

from common.exceptions import JsonDecodeException

class DataSerializer:
    @staticmethod
    def serialize(data: dict):
        return json.dumps(
                data,
                ensure_ascii=False,
                indent=4
            )
    @staticmethod
    def deserialize(data: str) -> str:
        try:
            return json.loads(
                data,
                strict=False,
            )
        except json.JSONDecodeError as e:
            raise JsonDecodeException(
                f"유효하지 않은 JSON 데이터입니다: {data}",
                status=400
            )
    