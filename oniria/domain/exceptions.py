from fastapi import HTTPException


class NoContentException(Exception):
    pass


class ConflictException(HTTPException):
    def __init__(self, detail: str = "Conflict occurred"):
        super().__init__(status_code=409, detail=detail)


class UnauthorizedException(Exception):
    pass
