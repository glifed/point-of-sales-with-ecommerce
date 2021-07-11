from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from app.models.domain.base import AbstractBaseModel

ModelType = TypeVar("ModelType", bound=AbstractBaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: ModelType):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        This object abstracts away the implementation of these methods to higher
        level clients.

        **parameters**

        * `model`: An ORM model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def filter_by_query(self, **kwargs) -> Optional[ModelType]:
        return self.model.get(**kwargs)

    def filter_or_none(self, **kwargs) -> Optional[ModelType]:
        return self.model.get_or_none(**kwargs)

    def get_all(
        self,
        skip: int,
        limit: int,
    ) -> List[ModelType]:
        return self.model.all().offset(skip).limit(limit)

    async def get_count(self) -> int:
        return await self.model.all().count()

    def create(self, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        return self.model.create(**obj_in_data)

    def update(
        self, id: str, obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        return self.model.filter(id=id).update(**obj_in_data)

    def delete(self, id: str) -> ModelType:
        return self.model.filter(id=id).delete()


class CRUDRelationsBase(CRUDBase):
    def __init__(self, model, related_model):
        """
        CRUD extended object that adds relationship operations to models.
        **parameters**

        * `model`: An ORM model class
        * `related_model`: An ORM model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model
        self.related_model = related_model

    def get_related(self):
        pass

    def add_related(self):
        pass
