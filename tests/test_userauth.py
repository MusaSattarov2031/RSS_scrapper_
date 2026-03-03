from src.users import UserAuth
import pytest
from sqlalchemy import text
import bcrypt

def test_create_user(userauth, connection):
    userauth.create_user("Alex2", "password1", "exampleemail2@test.com")
    row = connection.execute(
        text(
            "SELECT * FROM users WHERE username = 'Alex2'"
            )
        ).fetchone()

    assert row is not None, f"User not found"
    assert row.username == "Alex2"
    assert row.password_hash != "password1" #should be hashed, not exact value
    assert row.email == "exampleemail2@test.com"

def test_authenticate(userauth):
    assert userauth.authenticate("Alex", "password1") is True

def test_authenticate_invalid_password(userauth):
    assert userauth.authenticate("Alex", "wrong_password") is False

def test_authenticate_non_existent_user(userauth):
    assert userauth.authenticate("Jon", "password1") is False

def test_create_user_duplicate_username(userauth):
    with pytest.raises(ValueError, match="Username Alex2 already exists"):
        userauth.create_user("Alex2", "password2", "example@email.com")

def test_create_user_duplicate_email(userauth):
    with pytest.raises(ValueError, match="Email exampleemail2@test.com already registered. Do you want to log in?"):
        userauth.create_user("Alex11", "password2", "exampleemail2@test.com")

def test_password_is_hashed(connection):
    row = connection.execute(
        text(
            "SELECT password_hash FROM users WHERE username = 'Alex2'"
            )
        ).fetchone()
    
    stored_hash = row.password_hash
    if isinstance(stored_hash, bytes):
        stored_hash = stored_hash.decode('utf_8')
    
    assert stored_hash != "password1"
    assert stored_hash.startswith('$2b$') 
    assert bcrypt.checkpw(
        "password1".encode('utf-8'), 
        stored_hash.encode('utf-8'))

def test_create_user_empty_fields(userauth):
    with pytest.raises(ValueError, match="Username cannot be empty"):  # ✅ Add specific match
        userauth.create_user("", "password1", "email@test.com")
    
    with pytest.raises(ValueError, match="Password cannot be empty"):
        userauth.create_user("testuser", "", "email@test.com")
    
    with pytest.raises(ValueError, match="Email cannot be empty"):
        userauth.create_user("testuser", "password1", "")

@pytest.mark.parametrize("password, expected_valid, expected_message", [
    # Valid passwords
    ("Password123", True, "Password valid"),
    ("Test12345", True, "Password valid"),
    ("Abc123!@#", True, "Password valid"),
    
    # Invalid - missing numbers
    ("PasswordOnly", False, "Password must contain at least one number"),
    ("NoNumbersHere", False, "Password must contain at least one number"),
    ("abcdefgh", False, "Password must contain at least one number"),
    
    # Invalid - missing letters
    ("12345678", False, "Password must contain at least one letter"),
    ("!@#$%^&1", False, "Password must contain at least one letter"),
    ("98765432", False, "Password must contain at least one letter"),
    
    # Invalid - too short
    ("Pass1", False, "Password too short"),
    ("Ab1", False, "Password too short"),
])
def test_is_valid_password_complexity(password, expected_valid, expected_message):
    is_valid, message = UserAuth.is_valid_password(password)
    assert is_valid == expected_valid
    assert message == expected_message

@pytest.mark.parametrize("email, expected_valid", [
    ("valid@email.com", True),
    ("valid.email@test.co.uk", True),
    ("user+tag@example.com", True),
    ("invalid-email", False),
    ("missing@domain", False),
    ("@missingusername.com", False),
    ("spaces in@email.com", False)
])
def test_invalid_email_format(userauth, email, expected_valid):
    result = userauth.is_valid_email(email)
    assert result == expected_valid

@pytest.mark.parametrize("username, email, does_exist", [
    ("Alex", "exampleemail@test.com", True),
    ("Jon", "someemail@test.com", False)
])
def test_does_user_exist(userauth, username, email, does_exist):
    assert userauth.does_user_exist(username, email) == does_exist

def test_get_user_by_id(userauth):
    user_id = userauth.create_user("Sally", "password2", "sally@test.com")
    
    user = userauth.get_user_by_id(user_id)
    
    assert user is not None
    assert user["username"] == "Sally"
    assert user["email"] == "sally@test.com"

def test_get_id_by_username(userauth):
    user_id = userauth.create_user("Alex3", "password3", "alex2@test.com")

    assert user_id == userauth.get_id_by_username("Alex3")

def test_update_email(userauth):
    id = userauth.get_id_by_username("Alex")

    new_email = "alex@test.com"
    userauth.update_email(id, new_email)
    updated_user = userauth.get_user_by_id(id)

    assert new_email == updated_user["email"]

def test_update_username(userauth):
    id = userauth.get_id_by_username("Alex")

    new_username = "Jon"
    userauth.update_username(id, new_username)
    updated_user = userauth.get_user_by_id(id)

    assert new_username == updated_user["username"]

def test_update_password(userauth, connection):
    id = userauth.get_id_by_username("Alex")

    new_password = "new_password1"
    userauth.update_password(id, "password1", new_password)

    row = connection.execute(
        text(
            "SELECT password_hash FROM users WHERE username = 'Alex'"
        )
    ).fetchone()

    stored_hash = row[0]

    assert not (
        bcrypt.checkpw(
            "password1".encode('utf-8'),
            stored_hash
        )
    )

    assert bcrypt.checkpw(
        new_password.encode('utf-8'),
        stored_hash
    )

def test_delete_user(userauth, connection):
    id = userauth.get_id_by_username("Alex")

    userauth.delete_user(id)
    assert id is not None

    row = connection.execute(
        text(
            "SELECT * FROM users WHERE username = 'Alex'"
        )
    ).fetchone()

    assert row is None