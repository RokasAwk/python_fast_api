from exceptions import APIException, ErrorCode


class ItemVolumeInValidExists(APIException):
    def __init__(self):
        super().__init__(400, ErrorCode.INVALID_ITEM_VOLUME, "數量輸入錯誤")
