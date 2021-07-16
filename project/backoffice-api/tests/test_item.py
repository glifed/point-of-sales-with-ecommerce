import pytest


@pytest.fixture(scope="function")
def category_create(fake_name):
    return {"name": fake_name}

@pytest.fixture(scope="function")
def item_create(fake_name, fake_sku):
    return {
        "name": fake_name,
        "sku": fake_sku,
        "serial_number": fake_name,
        "description": fake_name,
        "images": [{"image": 1}],
        "qty": 0,
        "min_qty": 0,
        "cost": 0,
        "margin": 0,
        "price": 0,
        "rating": 0,
        "excento_itbis": False,
    }


def test_create_item(test_app_with_db, headers, api_domain, item_create, category_create):
    """Test that an item can be created"""
    
    response = test_app_with_db.post(
        f"{api_domain}/category/", headers=headers, json=category_create,
    )
    category_id = response.json()["id"]

    response = test_app_with_db.post(
        f"{api_domain}/item/{category_id}", headers=headers, json=item_create,
    )

    assert response.status_code == 201
    assert response.json()["name"] == item_create['name']
