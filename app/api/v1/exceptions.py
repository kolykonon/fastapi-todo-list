from fastapi import HTTPException, status


class TaskNotFoundException(HTTPException):
    def __init__(
        self,
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Задача с указанным ID не найдена",
    ):
        super().__init__(status_code, detail)


class TaskAlreadyExistsException(HTTPException):
    def __init__(
        self,
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Задача с таким названием уже существует",
        headers=None,
    ):
        super().__init__(status_code, detail, headers)
