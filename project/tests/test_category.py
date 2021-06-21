from faker import Faker

from app.resources import strings


def test_create_category(test_app_with_db):
    fake_name = "Test_" + Faker().color_name() + Faker().first_name()
    response = test_app_with_db.post("/category/", json={"name": fake_name})

    assert response.status_code == 201
    assert response.json()["name"] == fake_name


def test_create_category_name_taken(test_app_with_db):
    fake_name = "Test_" + Faker().color_name() + Faker().first_name()
    response = test_app_with_db.post("/category/", json={"name": fake_name})
    category_name = response.json()["name"]

    response = test_app_with_db.post("/category/", json={"name": category_name})

    assert response.status_code == 400
    assert response.json() == {"detail": strings.NAME_TAKEN}


def test_get_categories(test_app_with_db):
    fake_name = "Test_" + Faker().color_name() + Faker().first_name()

    response = test_app_with_db.post("/category/", json={"name": fake_name})
    category_id = response.json()["id"]

    response = test_app_with_db.get("/category/")
    assert response.status_code == 200
    assert response.json()["total"]

    response_list = response.json()["categories"]
    assert len(list(filter(lambda d: d["id"] == category_id, response_list))) == 1


def test_get_category_single(test_app_with_db):
    fake_name = "Test_" + Faker().color_name() + Faker().first_name()

    response = test_app_with_db.post("/category/", json={"name": fake_name})
    category_id = response.json()["id"]

    response = test_app_with_db.get(f"/category/{category_id}")

    assert response.status_code == 200
    assert response.json() == {"id": category_id, "name": fake_name}


def test_get_category_incorrect_id(test_app_with_db):
    response = test_app_with_db.get("/category/83d53aa8-47b0-4e23-8015-3b26d2c841de")

    assert response.status_code == 404
    assert response.json() == {"detail": strings.ITEM_NOT_FOUND_IN_DB}


def test_update_category(test_app_with_db):
    fake_name = "Test_" + Faker().color_name() + Faker().first_name()
    fake_name2 = "Test_" + Faker().color_name() + Faker().first_name()

    response = test_app_with_db.post("/category/", json={"name": fake_name})
    category_id = response.json()["id"]

    response = test_app_with_db.put(
        f"category/{category_id}", json={"name": fake_name2}
    )

    assert response.status_code == 200
    assert response.json() == {"id": category_id, "name": fake_name2}


def test_update_category_incorrect_id(test_app_with_db):
    fake_name = "Test_" + Faker().color_name() + Faker().first_name()
    response = test_app_with_db.put(
        "/category/83d53aa8-47b0-4e23-8015-3b26d2c841de", json={"name": fake_name}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": strings.ITEM_NOT_FOUND_IN_DB}


def test_update_category_name_taken(test_app_with_db):
    fake_name = "Test_" + Faker().color_name() + Faker().first_name()
    response = test_app_with_db.post("/category/", json={"name": fake_name})
    category_name = response.json()["name"]

    fake_name2 = "Test_" + Faker().color_name() + Faker().first_name()
    response = test_app_with_db.post("/category/", json={"name": fake_name2})
    category_id = response.json()["id"]

    response = test_app_with_db.put(
        f"category/{category_id}", json={"name": category_name}
    )

    assert response.status_code == 400
    assert response.json() == {"detail": strings.NAME_TAKEN}


def test_delete_category(test_app_with_db):
    fake_name = "Test_" + Faker().color_name() + Faker().first_name()
    response = test_app_with_db.post("/category/", json={"name": fake_name})
    category_id = response.json()["id"]

    response = test_app_with_db.delete(f"/category/{category_id}")
    assert response.status_code == 200
    assert response.json() == {"detail": strings.ITEM_DELETED_SUCCESSFULLY}

    response = test_app_with_db.get(f"/category/{category_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": strings.ITEM_NOT_FOUND_IN_DB}
