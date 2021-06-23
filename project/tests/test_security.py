from faker import Faker

from app.core.config import get_settings
from app.core.security import (create_access_token,
                               create_refresh_token,
                               get_password_hash,
                               verify_password)

settings = get_settings()


def test_password_hash_functionality():
    """
    Test password has generator.
    """
    
    password = "Test_" + Faker().color_name() + Faker().first_name()
    another_password = "Test_" + Faker().color_name() + Faker().first_name()
    
    password_hash = get_password_hash(password)

    assert verify_password(password, password_hash) == True
    assert verify_password(another_password, password_hash) == False


def test_token_generation_route(test_app_with_db):
    """
    Test login/jwt token generation.
    """
    fake_name = "Test_" + Faker().color_name() + Faker().first_name()
    response = test_app_with_db.post(
        f"{settings.API_V1_STR}/user/",
        json={
            "username": fake_name,
            "hashed_password": fake_name,
            "full_name": fake_name,
            "cedula": Faker().isbn10(separator=''),
            "sueldo": 0,
            "comision": 0
        }
    )

    response = test_app_with_db.post(
        url=f"{settings.API_V1_STR}/login",
        data={"username": fake_name, "password":fake_name},
    )
    tokens = response.json()
    
    assert response.status_code == 200
    assert "access_token" in tokens
    assert "refresh_token" in tokens
    assert tokens["access_token"]
    assert tokens["refresh_token"]
