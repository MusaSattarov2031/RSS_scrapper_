import bcrypt
from os import getenv
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import re

class UserAuth:
    def __init__(self):
        load_dotenv()
        db_url = getenv("DATABASE_URL")
        if db_url is None:
            raise ValueError("DATABASE_URL not set in environment")
        self.engine = create_engine(db_url)
        self.conn = self.engine.connect()
    
    def close(self):
        if hasattr(self, 'conn'):
            self.conn.close()
        if hasattr(self, 'engine'):
            self.engine.dispose()

        print("Auth connection is closed")

    def create_user(self, username, password, email):
        """
        Add user to database, returns id if succesfull
        Checks validity of username, password and email, raises ValueError if not valid
        """
        #Check fields is empty
        if username is None or username == "":
            raise ValueError("Username cannot be empty")
        elif password is None or password == "":
            raise ValueError("Password cannot be empty")
        elif email is None or email == "":
            raise ValueError("Email cannot be empty")
        
        # Checking password
        is_valid, message = self.is_valid_password(password)
        if not is_valid:
            raise ValueError(message)

        # Cheking email
        if not self.is_valid_email(email):
            raise ValueError("Invalid email")
        
        #Checking for duplicate email
        if self.does_user_exist(username=username):
            raise ValueError(f"Username {username} already exists")
        if self.does_user_exist(email=email):
            raise ValueError(f"Email {email} already registered. Do you want to log in?")
        
        # Hashing password
        salt = bcrypt.gensalt()
        hashed  = bcrypt.hashpw(password.encode('utf-8'), salt)

        # Creating a user
        result = self.conn.execute(
            text("""
                INSERT INTO users (username, password_hash, email)
                VALUES (:username, :hashed, :email)
            """),
            {
                "username": username,
                "hashed": hashed,
                "email": email
            }
        )
        self.conn.commit()
        new_id = result.lastrowid
        if new_id is None:
            raise ValueError("Not created")
        return new_id

    def authenticate(self, username, password):
        if not self.does_user_exist(username):
            return False

        row = self.conn.execute(
            text(
                "SELECT password_hash FROM users WHERE username = :username"
            ),
            {
                "username": username
            }
        ).fetchone()

        stored_hash = row.password_hash
        return bool(
            bcrypt.checkpw(
                password.encode('utf-8'),
                stored_hash
            )
        )

    def does_user_exist(self, username=None, email=None):
        """Returns True if duplicate exists"""
        if not(username or email):
            raise ValueError("args not given")
        if username:
            row = self.conn.execute(
                text(
                    "SELECT * FROM users WHERE username = :username"
                ),
                {"username": username}
            ).fetchone()
        
            if row is not None:
                return True
        if email:
            row = self.conn.execute(
                text(
                    "SELECT * FROM users WHERE email = :email"
                ),
                {"email": email}
            ).fetchone()

            if row is not None:
                return True
        return False

    
    @staticmethod
    def is_valid_password(password: str):
        """Validate password complexity"""
        if len(password) < 8:
            return False, "Password too short"
        if not re.search(r"[a-zA-Z]", password):
            return False, "Password must contain at least one letter"
        if not re.search(r"[0-9]", password):
            return False, "Password must contain at least one number"
        return True, "Password valid"
    
    @staticmethod
    def is_valid_email(email):
        """Validate email adress"""
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, email))

    def get_user_by_id(self, user_id):
        """return dictionary with id, username and email"""
        row = self.conn.execute(
            text(
                "SELECT username, email FROM users WHERE id = :user_id"
            ),
            {
                "user_id": user_id
            }
        ).fetchone()
        user = {}
        user["username"] = row.username
        user["id"] = user_id
        user["email"] = row.email
        return user

    def delete_user(self, user_id):
        pass

    def get_id_by_username(self, username):
        row = self.conn.execute(
            text(
                "SELECT id FROM users WHERE username = :username"
            ),
            {
                "username": username
            }
        ).fetchone()
        if row is None:
            raise ValueError("Username not found")
        return row.id

    def update_email(self, user_id, new_email):
        result = self.conn.execute(
            text("UPDATE users SET email = :new_email WHERE id = :user_id"),
            {"user_id": user_id, "new_email": new_email}
        )
        if result.rowcount == 0:
            raise ValueError("User not found")
        self.conn.commit()

    def update_username(self, user_id, new_username):
        result = self.conn.execute(
            text("UPDATE users SET username = :new_username WHERE id = :user_id"),
            {"user_id": user_id, "new_username": new_username}
        )
        if result.rowcount == 0:
            raise ValueError("User not found")
        self.conn.commit()

    def update_password(self, user_id, old_password, new_password):
        pass