from typing import List

from pydantic import BaseModel

from app.models.schema.schemas import UserBase


class ResponseUser(UserBase):
    pass


class ResponseUserList(BaseModel):
    users: List[ResponseUser]


class ResponseUserListPaginated(ResponseUserList):
    total: int
