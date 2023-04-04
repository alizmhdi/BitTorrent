class BaseException(Exception):
    def __init__(self, message: str, *args: object) -> None:
        self.message = message
        super().__init__(*args)


class FileDoseNotExist(BaseException):
    def __init__(self, *args: object, message=None) -> None:
        message = message if message else "FileDoseNotExist"
        super().__init__(message, *args)
