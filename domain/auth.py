from data.db.database_helper import DatabaseHelper
from data.models.user_model import UserModel


class Auth:
    def __init__(self, db_helper: DatabaseHelper):
        self.db_helper = db_helper

    def customer_sign_in(self, user: UserModel):
        result = self.db_helper.customer_sign_in(user)
        if result is None:
            return "Sorry, your account not found :("
        else:
            return result

    def customer_sign_up(self, user: UserModel):
        result = self.db_helper.customer_sign_up(user)
        return result

    def admin_sign_in(self, user: UserModel):
        result = self.db_helper.admin_sign_in(user)
        if result is None:
            return "Sorry, your account not found :("
        else:
            return result
