from uuid import UUID

from tortoise import Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator
from pydantic import BaseModel

from app.models.domain.category import Category


Tortoise.init_models(
    ["models.domain.category"],
    "models"
)

Category_Pydantic = pydantic_model_creator(Category, name='Category')
Category_List_Pydantic = pydantic_queryset_creator(Category)
CategoryIn_Pydantic = pydantic_model_creator(Category, name="CategoryIn", exclude_readonly=True)


class CategoryInfo(BaseModel):
    id: UUID
    name: str
    status: int
