class CustomException(Exception):
    def __init__(self, message, status_code):
        super().__init__()
        self.message = message
        self.status_code = status_code


class NoDataException(CustomException):
    def __init__(self, message, status_code=400):
        super().__init__(message, status_code)


class DataException(CustomException):
    def __init__(self, message, status_code=400):
        super().__init__(message, status_code)


class BadRequestException(CustomException):
    def __init__(self, message, status_code=400):
        super().__init__(message, status_code)
