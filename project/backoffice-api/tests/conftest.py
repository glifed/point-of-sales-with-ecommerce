import os
from typing import Any

import pytest
from faker import Faker
from starlette.testclient import TestClient
from tortoise.contrib.fastapi import register_tortoise

from app.core.config import Settings, get_settings
from app.main import create_application
from app.models.schema.security import Action, Model
from app.resources.db import MODELS

settings = get_settings()


def get_settings_override():
    return Settings(
        TESTING=1, ENVIRONMENT="test", DATABASE_URL=settings.DATABASE_TEST_URL
    )


@pytest.fixture(scope="module")
def test_app_with_db() -> Any:
    # set up
    app = create_application()
    app.dependency_overrides[get_settings] = get_settings_override
    register_tortoise(
        app,
        db_url=os.environ.get("DATABASE_TEST_URL"),
        modules={"models": MODELS},
        generate_schemas=True,
        add_exception_handlers=True,
    )
    with TestClient(app) as test_client:

        # testing
        yield test_client

    # tear down


@pytest.fixture(scope="module")
def test_jwt_token(test_app_with_db) -> Any:
    # Create fake user
    fake_name = "Test_" + Faker().color_name() + Faker().first_name()

    # Add all permissions
    scopes = {}
    for model in Model:
        for action in Action:
            scopes[f"{model.value}:{action.value}"] = f"{model.value} {action.value}"

    response = test_app_with_db.post(
        f"{settings.API_V1_STR}/user/",
        json={
            "username": fake_name,
            "hashed_password": fake_name,
            "full_name": fake_name,
            "cedula": Faker().isbn10(separator=""),
            "sueldo": 0,
            "comision": 0,
            "scopes": scopes,
        },
    )

    # Log in with fake user
    response = test_app_with_db.post(
        url=f"{settings.API_V1_STR}/login",
        data={"username": fake_name, "password": fake_name},
    )
    tokens = response.json()  # Access and Refresh tokens

    return tokens


@pytest.fixture(scope="module")
def test_jwt_token_no_scopes(test_app_with_db) -> Any:
    # Create fake user
    fake_name = "Test_" + Faker().color_name() + Faker().first_name()

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

    # Log in with fake user
    response = test_app_with_db.post(
        url=f"{settings.API_V1_STR}/login",
        data={"username": fake_name, "password": fake_name},
    )
    tokens = response.json()  # Access and Refresh tokens

    return tokens


@pytest.fixture(scope="function")
def fake_name():
    return "Test_" + Faker().color_name() + Faker().first_name()
