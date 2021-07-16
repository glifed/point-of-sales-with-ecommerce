import pytest


@pytest.fixture(scope="function")
def item_create(fake_name, fake_sku):
    return {
        "name": fake_name,
        "sku": fake_sku,
        "serial_number": fake_sku,
        "description": fake_name,
        "images": [{"id": 1, "name": "image1"}],
        "qty": 0,
        "min_qty": 0,
        "cost": 0,
        "margin": 0,
        "price": 0,
        "rating": 0,
        "excento_itbis": False,
    }


def test_create_item(test_app_with_db, headers, api_domain, item_create, fake_name):
    """Test that an item can be created"""
    category_json = {"name": fake_name}
    response = test_app_with_db.post(
        f"{api_domain}/category/",
        headers=headers,
        json=category_json,
    )
    category_id = response.json()["id"]

    response = test_app_with_db.post(
        f"{api_domain}/item/{category_id}",
        headers=headers,
        json=item_create,
    )

    item = response.json()["item"]
    category = response.json()["category"]

    assert response.status_code == 201
    assert item["name"] == item_create["name"]
    assert category["name"] == category_json["name"]
