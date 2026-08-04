from exceptions import APIException, ErrorCode


class UserNotFound(APIException):
    def __init__(self, user_id: int):
        super().__init__(404, ErrorCode.USER_NOT_FOUND, f"找不到 id 為 {user_id} 的使用者")


class UserAlreadyExists(APIException):
    def __init__(self, name: str):
        super().__init__(409, ErrorCode.USER_ALREADY_EXISTS, f"使用者 {name} 已存在")


class InvalidAge(APIException):
    def __init__(self):
        super().__init__(400, ErrorCode.INVALID_AGE, "年齡不能是負數")
