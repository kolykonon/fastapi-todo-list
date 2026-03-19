from fastapi import HTTPException, status
from typing import Callable


class TaskNotFoundException(HTTPException):
    def __init__(
        self,
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Задача с указанным ID не найдена",
    ):
        super().__init__(status_code, detail)


class AlreadyExistsException(HTTPException):
    def __init__(
        self, substance: Callable, status_code=status.HTTP_400_BAD_REQUEST, headers=None
    ):
        super().__init__(
            status_code=status_code,
            headers=headers,
            detail=f"{substance.__name__} уже существует!",
        )


class UnauthorizedException(HTTPException):
    def __init__(
        self,
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Неправильный логин или пароль",
        headers=None,
    ):
        super().__init__(status_code, detail, headers)
