from exceptions import APIException, ErrorCode


class UsernameAlreadyExists(APIException):
    def __init__(self, username: str):
        super().__init__(409, ErrorCode.USERNAME_ALREADY_EXISTS, f"帳號 {username} 已被註冊")


class InvalidCredentials(APIException):
    def __init__(self):
        super().__init__(401, ErrorCode.INVALID_CREDENTIALS, "帳號或密碼錯誤")


class Unauthorized(APIException):
    def __init__(self):
        super().__init__(401, ErrorCode.UNAUTHORIZED, "Access Token 無效或未提供")
