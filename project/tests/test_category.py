

def test_create_category(test_app_with_db):
    response = test_app_with_db.post("/category/", json={"name": "Pantallas"})

    assert response.status_code == 201

    response_dict = response.json()["category"]
    assert response_dict["name"] == "Pantallas"
