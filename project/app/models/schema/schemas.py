from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, validator
from tortoise import Tortoise
from tortoise.contrib.pydantic import (pydantic_model_creator,
                                       pydantic_queryset_creator)

from app.models.domain.base import Status
from app.models.domain.category import Category
from app.models.domain.user import User


Tortoise.init_models([
    "models.domain.category",
    "models.domain.user",
], "models")


# pydantic schemas
User_Pydantic = pydantic_model_creator(User, name="User")
User_List_Pydantic = pydantic_queryset_creator(User)
UserIn_Pydantic = pydantic_model_creator(
    User, name="UserIn", exclude_readonly=True
)

Category_Pydantic = pydantic_model_creator(Category, name="Category")
Category_List_Pydantic = pydantic_queryset_creator(Category)
CategoryIn_Pydantic = pydantic_model_creator(
    Category, name="CategoryIn", exclude_readonly=True
)


# custom schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: Optional[int] = None


class TokenResponse(BaseModel):
    access_token: Token
    refresh_token: Token


class CustomResponse(BaseModel):
    detail: str


class Pagination(BaseModel):
    skip: int
    limit: int

    @validator("*", pre=True)
    def check_non_negative(cls, v):
        if (v) < 0:
            raise ValueError()
        return v


class StatusMixin(BaseModel):
    status: Status


class CategoryBase(BaseModel):
    id: UUID
    name: str


class UserBase(StatusMixin):
    id: UUID
    username: str
    full_name: str
    cedula: str
    sueldo: Decimal
    comision: Decimal