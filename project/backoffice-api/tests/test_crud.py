from app.crud.base import CRUDBase

def test_crudbase_has_get_getall_create_update_delete():
    crud = CRUDBase()
    assert hasattr(crud, 'get') and callable(getattr(crud, 'get'))
    assert hasattr(crud, 'get_all') and callable(getattr(crud, 'get_all'))
    assert hasattr(crud, 'create') and callable(getattr(crud, 'create'))
    assert hasattr(crud, 'update') and callable(getattr(crud, 'get_all'))
    assert hasattr(crud, 'delete') and callable(getattr(crud, 'delete'))