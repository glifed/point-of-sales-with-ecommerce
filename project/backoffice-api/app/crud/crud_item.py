from app.crud.base import CRUDBaseRelated
from app.models.domain.item import Item


class CRUDItem(CRUDBaseRelated):
    pass


item_crud = CRUDItem(Item)
