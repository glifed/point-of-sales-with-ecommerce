from app.resources.strings import NAME_TAKEN

def test_create_category(test_app_with_db):
    response = test_app_with_db.post("/category/", json={"name": "Pantallas"})

    assert response.status_code in (201,400)

    response_dict = response.json()
    if response.status_code == 201:
        assert response_dict["name"] == "Pantallas"
    else:
        assert response_dict == {
            'detail': NAME_TAKEN
        }
