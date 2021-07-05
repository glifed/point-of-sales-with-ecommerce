from app.crud.base import CRUDBase, CRUDRelationsBase
from app.models.domain.base import AbstractBaseModel

model = AbstractBaseModel()
related_model = AbstractBaseModel()

def test_crudbase_has_get_getall_create_update_delete():
    crud = CRUDBase(model)
    assert hasattr(crud, 'get') and callable(getattr(crud, 'get'))
    assert hasattr(crud, 'get_all') and callable(getattr(crud, 'get_all'))
    assert hasattr(crud, 'create') and callable(getattr(crud, 'create'))
    assert hasattr(crud, 'update') and callable(getattr(crud, 'update'))
    assert hasattr(crud, 'delete') and callable(getattr(crud, 'delete'))

def test_crudbaserelations_has_getrelations_addrelations():
    crud = CRUDRelationsBase(model, related_model)
    assert hasattr(crud, 'get_related') and callable(getattr(crud, 'get_related'))
    assert hasattr(crud, 'add_related') and callable(getattr(crud, 'add_related'))

