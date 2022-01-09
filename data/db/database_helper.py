import sqlite3
from data.models.food_model import FoodModel
from data.models.order_model import OrderModel
from data.models.user_model import UserModel


class DatabaseHelper:
    __instance = None
    __database = None
    __AUTH = "user_auth"
    __FOOD = "food"
    __ORDER = "customer_order"

    @staticmethod
    def get_instance():
        if DatabaseHelper.__instance is None:
            DatabaseHelper()
        return DatabaseHelper.__instance

    def __init__(self):
        if DatabaseHelper.__instance is None:
            DatabaseHelper.__instance = self

    @property
    def database(self):
        if self.__database is None:
            self.__database = self.__initDb()
            return self.__database
        return self.__database

    def __initDb(self):
        db = sqlite3.connect('resto.db')
        db.row_factory = sqlite3.Row
        self.__on_create_table(db)
        return db

    def __on_create_table(self, db):
        db.execute(f'''CREATE TABLE IF NOT EXISTS {self.__AUTH}
         (id VARCHAR(32) NOT NULL PRIMARY KEY,
         email           TEXT    NOT NULL UNIQUE,
         password        TEXT    NOT NULL,
         is_admin        INT NOT NULL
         );''')

        db.execute(f'''CREATE TABLE IF NOT EXISTS {self.__FOOD}
         (id VARCHAR(32) NOT NULL PRIMARY KEY,
         name           TEXT    NOT NULL,
         food_quantity        INT    NOT NULL,
         price        INT    NOT NULL
         );''')

        db.execute(f'''CREATE TABLE IF NOT EXISTS {self.__ORDER}
         (id VARCHAR(32) NOT NULL PRIMARY KEY,
         user_id      VARCHAR(32) NOT NULL,
         food_id      VARCHAR(32) NOT NULL,
         order_quantity     INT    NOT NULL,
         already_paid INT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES {self.__AUTH} (id),
        FOREIGN KEY (food_id) REFERENCES {self.__FOOD} (id)
         );''')

        # create account for admin
        admin = UserModel('22fe7456aba4405c84d17de2b7c931d1',
                          'resto.admin@gmail.com', 'admin123', True)
        params = (admin.id, admin.email, admin.password, int(admin.is_admin))
        db.execute(
            f"INSERT OR REPLACE INTO {self.__AUTH} VALUES(?,?,?,?)", params)
        db.commit()

    def customer_sign_up(self, user):
        db = self.database
        params = (user.id, user.email, user.password, int(user.is_admin))
        db.execute(
            f"INSERT OR REPLACE INTO {self.__AUTH} VALUES(?,?,?,?)", params)
        db.commit()
        return user

    def customer_sign_in(self, user):
        db = self.database
        params = (user.email, user.password, int(user.is_admin))
        result = db.execute(
            f"SELECT * FROM {self.__AUTH} WHERE email = ? AND password = ? AND is_admin = ?", params)

        result = result.fetchone()
        if result is None:
            return None
        return UserModel.from_dict(result)

    def admin_sign_in(self, user):
        db = self.database
        params = (user.email, user.password, int(user.is_admin))
        result = db.execute(
            f"SELECT * FROM {self.__AUTH} WHERE email = ? AND password = ? AND is_admin = ?", params)

        result = result.fetchone()
        if result is None:
            return None

        return UserModel.from_dict(result)

    def add_food(self, food):
        db = self.database
        params = (food.id, food.name, food.food_quantity, food.price)
        db.execute(
            f"INSERT OR REPLACE INTO {self.__FOOD} VALUES(?,?,?,?)", params)
        db.commit()

    def update_food(self, food):
        db = self.database
        params = (food.id, food.name, food.food_quantity, food.price, food.id)
        db.execute(
            f"UPDATE {self.__FOOD} SET id = ?, name = ?, food_quantity = ?, price = ? WHERE id = ?", params)
        db.commit()

    def remove_food(self, id):
        db = self.database
        params = (id,)
        db.execute(f"DELETE FROM {self.__FOOD} WHERE id = ?", params)
        db.commit()

    def fetch_foods(self):
        db = self.database
        result = db.execute(f"SELECT * FROM {self.__FOOD}")

        result = result.fetchall()
        if result is None:
            return None

        # convert sqlite3.row to map
        result = [dict(row) for row in result]
        # decode result from sqlite
        return list(map(lambda data: FoodModel.from_dict(data), result))

    def fetch_food_by_id(self, id):
        db = self.database
        params = (id,)
        result = db.execute(
            f"SELECT * FROM {self.__FOOD} WHERE id = ?", params)

        result = result.fetchone()
        if result is None:
            return None

        return FoodModel.from_dict(result)

    def order_food(self, order, food):
        db = self.database
        params = (order.id, order.user_id, order.food_id,
                  order.order_quantity, int(order.already_paid))
        db.execute(
            f"INSERT OR REPLACE INTO {self.__ORDER} VALUES(?,?,?,?,?)", params)
        db.commit()
        params = (food.food_quantity, food.id)
        db.execute(
            f"UPDATE {self.__FOOD} SET food_quantity = ? WHERE id = ?", params)
        db.commit()

    def fetch_order_datail(self, user_id):
        db = self.database
        params = (user_id, 0)
        result = db.execute(
            f"""SELECT * FROM {self.__ORDER} INNER JOIN {self.__FOOD} 
            ON food_id = {self.__FOOD}.id 
            WHERE user_id = ? AND already_paid = ?""", params)

        result = result.fetchall()
        if result is None:
            return None

        # convert sqlite3.row to map
        result = [dict(row) for row in result]
        # decode result from sqlite
        return list(map(lambda data: OrderModel.from_dict(data), result))

    def fetch_total_bill(self, user_id):
        db = self.database
        params = (user_id, 0)
        result = db.execute(
            f"""SELECT SUM(o.order_quantity * {self.__FOOD}.price) AS total_bill FROM {self.__ORDER} AS o INNER JOIN {self.__FOOD} 
            ON o.food_id = {self.__FOOD}.id 
            WHERE o.user_id = ? AND already_paid = ?""", params)

        result = result.fetchone()
        if result is None:
            return None

        return result['total_bill']

    def pay_bills(self, total_bill, user_money):
        if user_money >= total_bill:
            return int(user_money - total_bill)
        else:
            return "Your money is not enough to pay the bills"

    def update_order(self, user_id):
        db = self.database
        params = (int(True), user_id)
        db.execute(
            f"UPDATE {self.__ORDER} SET already_paid = ? WHERE user_id = ?", params)
        db.commit()

    def remove_order(self, order):
        db = self.database
        params = (order.id,)
        db.execute(f"DELETE FROM {self.__ORDER} WHERE id = ?", params)
        params = (order.food.food_quantity, order.food.id)
        db.commit()
        db.execute(
            f"UPDATE {self.__FOOD} SET food_quantity = ? WHERE id = ?", params)
        db.commit()
