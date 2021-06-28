from fastapi import HTTPException, status

from app.resources.strings import APIResponseMessage


class InvalidUsernamePasswordException(HTTPException):
    def __init__(self) -> None:
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.detail = APIResponseMessage.INVALID_USERNAME_PASSWORD


class InactiveUserException(HTTPException):
    def __init__(self) -> None:
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.detail = APIResponseMessage.INACTIVE_USER


class InsufficientPermissionsException(HTTPException):
    def __init__(self) -> None:
        self.status_code = status.HTTP_403_FORBIDDEN
        self.detail = APIResponseMessage.InsufficientPermissions


class NameTakenException(HTTPException):
    def __init__(self) -> None:
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = APIResponseMessage.NAME_TAKEN


class ItemNotFoundException(HTTPException):
    def __init__(self) -> None:
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = APIResponseMessage.ITEM_NOT_FOUND_IN_DB


class InvalidIdException(HTTPException):
    def __init__(self) -> None:
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = APIResponseMessage.INVALID_UUID


class ErrorSavingItemException(HTTPException):
    def __init__(self) -> None:
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = APIResponseMessage.ERROR_IN_SAVING_ITEM
