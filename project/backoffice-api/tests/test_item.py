from app.core.config import get_settings

settings = get_settings()

def test_create_item(test_app_with_db, test_jwt_token, fake_name):
    access_token = test_jwt_token["access_token"]  # jwt access token
    
    response = test_app_with_db.post(
        f"{settings.API_V1_STR}/item/",
        headers={
            "Authorization": f"{access_token['token_type']} {access_token['token']}"
        },
        json={
            "name": fake_name,
            "sku": fake_name,
            "serial_number": fake_name,
            "description": fake_name,
            "images": [{"image": 1}],
            "qty": 0,
            "min_qty": 0,
            "cost": 0,
            "margin": 0,
            "price": 0,
            "rating": 0,
            "excento_itbis": False
        },
    )

    assert response.status_code == 201
    assert response.json()["name"] == fake_name
