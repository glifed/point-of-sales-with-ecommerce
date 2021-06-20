from uuid import UUID

from tortoise import Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator
from pydantic import BaseModel, validator

from app.models.domain.base import Status
from app.models.domain.category import Category


Tortoise.init_models(
    ["models.domain.category"],
    "models"
)

Category_Pydantic = pydantic_model_creator(Category, name='Category')
Category_List_Pydantic = pydantic_queryset_creator(Category)
CategoryIn_Pydantic = pydantic_model_creator(Category, name="CategoryIn", exclude_readonly=True)


class Pagination(BaseModel):
    skip: int
    limit: int

    @validator('*', pre=True)
    def check_non_negative(cls, v):
        if (v) < 0:
            raise ValueError()
        return v


class CategoryInfo(BaseModel):
    id: UUID
    name: str
