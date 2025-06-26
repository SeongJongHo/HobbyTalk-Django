class BusinessException(Exception):
    def __init__(self, message: str, status: int = 400):
        super().__init__(message)
        self.message = message
        self.status = status

class NotFoundException(BusinessException):
    def __init__(self, message: str = "Resource not found", status: int = 404):
        super().__init__(message, status)

class UnauthorizedException(BusinessException):
    def __init__(self, message: str = "Unauthorized access", status: int = 401):
        super().__init__(message, status)

class ForbiddenException(BusinessException):
    def __init__(self, message: str = "Forbidden access", status: int = 403):
        super().__init__(message, status)

class ValidationException(BusinessException):
    def __init__(self, message: str = "Validation error", status: int = 422):
        super().__init__(message, status)

class ConflictException(BusinessException):
    def __init__(self, message: str = "Conflict error", status: int = 409):
        super().__init__(message, status)

class InvalidTokenException(BusinessException):
    def __init__(self, message: str = "Invalid token", status: int = 401):
        super().__init__(message, status)