from faker import Faker

from app.core.config import get_settings

settings = get_settings()


def test_create_user(test_app_with_db, fake_name):
    response = test_app_with_db.post(
        f"{settings.API_V1_STR}/user/",
        json={
            "username": fake_name,
            "hashed_password": fake_name,
            "full_name": fake_name,
            "cedula": Faker().isbn10(separator=""),
            "sueldo": 0,
            "comision": 0,
        },
    )

    assert response.status_code == 201
    assert response.json()["username"] == fake_name
