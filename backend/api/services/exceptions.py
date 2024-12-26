from fastapi import HTTPException, status


class NotFoundError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class MultipleFoundError(NotFoundError):
    pass


class AlreadyExistError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class UnauthorizedError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)
