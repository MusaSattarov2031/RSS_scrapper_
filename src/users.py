import bcrypt

class UserAuth:
    def __init__(self, db_connection):
        self.conn = db_connection

    def create_user(self, username, password, email):
        pass
    

    def authenticate(self, username, password):
        pass

    def does_user_exist(self, username, email):
        pass

    def is_valid_password(self, password):
        pass

    def get_user_by_id(self, user_id):
        pass

    def delete_user(self, user_id):
        pass

    def get_id_by_username(self, username):
        pass

    def update_email(self, user_id, new_email):
        pass

    def update_username(self, user_id, new_username):
        pass

    def update_password(self, user_id, old_password, new_password):
        pass