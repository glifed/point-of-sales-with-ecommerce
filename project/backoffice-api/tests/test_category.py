from app.resources.strings import APIResponseMessage


def test_create_category(test_app_with_db, headers, api_domain, fake_name):
    """Test create category endpoint"""

    response = test_app_with_db.post(
        f"{api_domain}/category/",
        headers=headers,
        json={"name": fake_name},
    )

    assert response.status_code == 201
    assert response.json()["name"] == fake_name


def test_create_category_no_permission(
    test_app_with_db, headers_noscope, api_domain, fake_name
):
    response = test_app_with_db.post(
        f"{api_domain}/category/",
        headers=headers_noscope,
        json={"name": fake_name},
    )

    assert response.status_code == 403
    assert response.json() == {"detail": APIResponseMessage.InsufficientPermissions}


def test_create_category_name_taken(test_app_with_db, headers, api_domain, fake_name):

    response = test_app_with_db.post(
        f"{api_domain}/category/",
        headers=headers,
        json={"name": fake_name},
    )
    category_name = response.json()["name"]

    response = test_app_with_db.post(
        f"{api_domain}/category/",
        headers=headers,
        json={"name": category_name},
    )

    assert response.status_code == 400
    assert response.json() == {"detail": APIResponseMessage.NAME_TAKEN}


def test_get_categories(test_app_with_db, headers, api_domain, fake_name):

    response = test_app_with_db.post(
        f"{api_domain}/category/",
        headers=headers,
        json={"name": fake_name},
    )
    category_id = response.json()["id"]

    response = test_app_with_db.get(f"{api_domain}/category/")
    assert response.status_code == 200
    assert response.json()["total"]

    response_list = response.json()["categories"]
    assert len(list(filter(lambda d: d["id"] == category_id, response_list))) == 1


def test_get_category_single(test_app_with_db, headers, api_domain, fake_name):

    response = test_app_with_db.post(
        f"{api_domain}/category/",
        headers=headers,
        json={"name": fake_name},
    )
    category_id = response.json()["id"]

    response = test_app_with_db.get(f"{api_domain}/category/{category_id}")

    assert response.status_code == 200
    assert response.json() == {"id": category_id, "name": fake_name}


def test_get_category_incorrect_id(test_app_with_db, api_domain):
    response = test_app_with_db.get(
        f"{api_domain}/category/83d53aa8-47b0-4e23-8015-3b26d2c841de"
    )

    assert response.status_code == 404
    assert response.json() == {"detail": APIResponseMessage.ITEM_NOT_FOUND_IN_DB}

    response = test_app_with_db.get(f"{api_domain}/category/aa2")

    assert response.status_code == 400
    assert response.json() == {"detail": APIResponseMessage.INVALID_UUID}


def test_update_category(test_app_with_db, headers, api_domain, fake_name, fake_name2):

    response = test_app_with_db.post(
        f"{api_domain}/category/",
        headers=headers,
        json={"name": fake_name},
    )
    category_id = response.json()["id"]

    response = test_app_with_db.put(
        f"{api_domain}/category/{category_id}",
        headers=headers,
        json={"name": fake_name2},
    )

    assert response.status_code == 200
    assert response.json() == {"id": category_id, "name": fake_name2}


def test_update_category_incorrect_id(test_app_with_db, headers, api_domain, fake_name):

    response = test_app_with_db.put(
        f"{api_domain}/category/83d53aa8-47b0-4e23-8015-3b26d2c841de",
        headers=headers,
        json={"name": fake_name},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": APIResponseMessage.ITEM_NOT_FOUND_IN_DB}

    response = test_app_with_db.put(
        f"{api_domain}/category/a22",
        headers=headers,
        json={"name": fake_name},
    )

    assert response.status_code == 400
    assert response.json() == {"detail": APIResponseMessage.INVALID_UUID}


def test_update_category_name_taken(
    test_app_with_db, headers, api_domain, fake_name, fake_name2
):

    # create a category
    response = test_app_with_db.post(
        f"{api_domain}/category/",
        headers=headers,
        json={"name": fake_name},
    )
    category_name = response.json()["name"]

    # create another category
    response = test_app_with_db.post(
        f"{api_domain}/category/",
        headers=headers,
        json={"name": fake_name2},
    )
    category_id = response.json()["id"]

    # try to duplicate
    response = test_app_with_db.put(
        f"{api_domain}/category/{category_id}",
        headers=headers,
        json={"name": category_name},
    )

    assert response.status_code == 400
    assert response.json() == {"detail": APIResponseMessage.NAME_TAKEN}


def test_delete_category(test_app_with_db, headers, api_domain, fake_name):

    # create category
    response = test_app_with_db.post(
        f"{api_domain}/category/",
        headers=headers,
        json={"name": fake_name},
    )
    category_id = response.json()["id"]

    # delete category
    response = test_app_with_db.delete(
        f"{api_domain}/category/{category_id}",
        headers=headers,
    )
    assert response.status_code == 200
    assert response.json() == {"detail": APIResponseMessage.ITEM_DELETED_SUCCESSFULLY}

    response = test_app_with_db.get(f"{api_domain}/category/{category_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": APIResponseMessage.ITEM_NOT_FOUND_IN_DB}


def test_delete_category_incorrect_id(test_app_with_db, api_domain, headers):

    response = test_app_with_db.delete(
        f"{api_domain}/category/83d53aa8-47b0-4e23-8026-3c26b2c841de",
        headers=headers,
    )

    assert response.status_code == 404
    assert response.json() == {"detail": APIResponseMessage.ITEM_NOT_FOUND_IN_DB}

    response = test_app_with_db.delete(
        f"{api_domain}/category/a22",
        headers=headers,
    )

    assert response.status_code == 400
    assert response.json() == {"detail": APIResponseMessage.INVALID_UUID}
