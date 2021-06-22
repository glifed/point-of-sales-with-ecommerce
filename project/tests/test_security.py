from faker import Faker

from app.core.security import (create_access_token,
                               create_refresh_token,
                               get_password_hash,
                               verify_password)

def test_password_hash_functionality():
    """
    Test password has generator.
    """
    
    password = "Test_" + Faker().color_name() + Faker().first_name()
    another_password = "Test_" + Faker().color_name() + Faker().first_name()
    
    password_hash = get_password_hash(password)

    assert verify_password(password, password_hash) == True
    assert verify_password(another_password, password_hash) == False
