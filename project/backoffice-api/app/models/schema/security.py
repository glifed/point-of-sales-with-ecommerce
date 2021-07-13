from enum import Enum
from typing import List

from pydantic import BaseModel


# Permissions
class Action(str, Enum):
    CREATE = "Create"
    READ = "Read"
    UPDATE = "Update"
    DELETE = "Delete"
    ACTIVATE = "Activate"


class Model(str, Enum):
    USER = "User"
    CATEGORY = "Category"
    ITEM = "Item"


class Permission(BaseModel):
    permission: str
    detail: str


class PermissionList(BaseModel):
    permissions: List[Permission]
