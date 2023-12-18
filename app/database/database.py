from pathlib import Path
import psycopg2 as ps

from app.database.config import DBConfig


SQL_PATH = Path(__file__).parent / "sql"


class DataBase:
    DB_NAME = "calories_app"
    DB_USER = "calories_app_user"
    DB_PASSWORD = "very_hard_password_to_guess"

    def __init__(self, config: DBConfig):
        self.config = config
        self.db_params = config.to_dict()

        self.init_database()
        self.create_database_user_connection_and_cursor()

    def create_database_user_connection_and_cursor(self):
        self.db_connection = ps.connect(
            f"dbname={self.DB_NAME} user={self.DB_USER} password={self.DB_PASSWORD}"
        )
        self.db_cursor = self.db_connection.cursor()

    def init_database(self):
        self.create_tables()
        self.initialize_functions()

    def create_tables(self):
        self.db_connection = ps.connect(self.config.to_connection_string())
        self.db_cursor = self.db_connection.cursor()

        with open(SQL_PATH / "DataBase actions.sql") as file:
            create_drop_func = file.read()

        self.db_cursor.execute(create_drop_func)
        self.db_cursor.execute(
            "SELECT create_db(%s, %s, %s)",
            (self.DB_USER, self.DB_PASSWORD, self.DB_NAME),
        )
        self.close_connection()

    def initialize_functions(self):
        self.db_connection = ps.connect(
            f"dbname={self.DB_NAME} user={self.DB_USER} password={self.DB_PASSWORD}"
        )
        self.db_cursor = self.db_connection.cursor()

        with open(SQL_PATH / "Delete_info_db.sql") as file:
            delete_func = file.read()

        with open(SQL_PATH / "find_in_db.sql") as file:
            find_func = file.read()

        with open(SQL_PATH / "Insert_into_db.sql") as file:
            insert_func = file.read()

        with open(SQL_PATH / "update_db_table.sql") as file:
            update_func = file.read()

        with open(SQL_PATH / "trigger_functions.sql") as file:
            trigger_functions = file.read()

        self.db_cursor.execute(delete_func)
        self.db_connection.commit()

        self.db_cursor.execute(find_func)
        self.db_connection.commit()

        self.db_cursor.execute(insert_func)
        self.db_connection.commit()

        self.db_cursor.execute(update_func)
        self.db_connection.commit()

        self.db_cursor.execute(trigger_functions)
        self.db_connection.commit()

    def find_id_and_password(self, login):
        self.db_cursor.execute(
            "SELECT * FROM public.find_account_id_and_password('{}')".format(login)
        )
        user_info = self.db_cursor.fetchone()

        return user_info if user_info else None

    def find_product(self, product_name):
        self.db_cursor.execute("SELECT * FROM find_product(%s)", (product_name,))
        request = self.db_cursor.fetchall()

        return request if request else None

    def find_user_id(self, account_id):
        self.db_cursor.execute("SELECT * FROM find_user_id(%s)", (account_id,))
        user_id = self.db_cursor.fetchone()

        return user_id if user_id else None

    def get_user_statistic(self, user_id, date):
        self.db_cursor.execute(
            "SELECT * FROM get_user_statistic(%s, %s)",
            (
                user_id,
                date,
            ),
        )
        user_statistic = self.db_cursor.fetchone()

        return user_statistic if user_statistic else None

    def find_fav_product(self, user_id, product_id):
        self.db_cursor.execute(
            "SELECT * FROM get_fav_product(%s, %s)",
            (
                user_id,
                product_id,
            ),
        )
        prod_id = self.db_cursor.fetchone()

        return prod_id

    def get_user_info(self, user_id):
        self.db_cursor.execute("SELECT * FROM get_user_info(%s)", (user_id,))
        user_info = self.db_cursor.fetchone()

        return user_info if user_info else None

    def get_product(self):
        self.db_cursor.execute("SELECT * FROM get_product()")
        product = self.db_cursor.fetchone()

        return product if product else None

    def get_prod_info(self, product_id):
        self.db_cursor.execute("SELECT * FROM get_product_info(%s)", (product_id,))
        product_info = self.db_cursor.fetchone()

        return product_info if product_info else None

    def get_meal_macro(self, user_id, date):
        self.db_cursor.execute(
            "SELECT * FROM get_meal_macro(%s, %s)",
            (
                user_id,
                date,
            ),
        )
        meal_macro = self.db_cursor.fetchall()

        return meal_macro if meal_macro else None

    def get_meal_info(self, meal_type, date, user_id):
        self.db_cursor.execute(
            "SELECT * FROM get_meal_info(%s, %s, %s)",
            (
                meal_type,
                date,
                user_id,
            ),
        )
        meal_info = self.db_cursor.fetchone()

        return meal_info if meal_info else None

    def get_favourite_products(self, user_id):
        self.db_cursor.execute("SELECT * FROM get_favourite_products(%s)", (user_id,))
        favourite_product = self.db_cursor.fetchall()

        return favourite_product if favourite_product else None

    def get_account_info(self, account_id):
        self.db_cursor.execute("SELECT * FROM find_user_data(%s)", (account_id,))
        acc_information = self.db_cursor.fetchone()

        return acc_information if acc_information else None

    def add_to_favourites(self, user_id, product_id):
        self.db_cursor.execute(
            "SELECT add_product_to_favourites(%s, %s)",
            (
                user_id,
                product_id,
            ),
        )
        self.db_connection.commit()

    def insert_user_statistic(
        self,
        kilocalories_intake,
        fats_intake,
        carbohydrates_intake,
        proteins_intake,
        date,
        weight_loss,
        user_id,
    ):
        self.db_cursor.execute(
            "SELECT add_statistic_info(%s, %s, %s, %s, %s, %s, %s)",
            (
                kilocalories_intake,
                fats_intake,
                carbohydrates_intake,
                proteins_intake,
                date,
                weight_loss,
                user_id,
            ),
        )
        self.db_connection.commit()

    def insert_product_info(
        self, prod_id, name, proteins, fats, carbohydrates, kilocalories
    ):
        self.db_cursor.execute(
            "SELECT insert_product_info(%s, %s, %s, %s, %s, %s)",
            (
                prod_id,
                name,
                proteins,
                fats,
                carbohydrates,
                kilocalories,
            ),
        )
        self.db_connection.commit()

    def insert_acc_info(self, login, password):
        self.db_cursor.execute(
            "SELECT insert_account(%s, %s)",
            (
                login,
                password,
            ),
        )
        self.db_connection.commit()

    def insert_user_info(
        self, gender, account_id, activity, age=18, weight=70.0, height=180.0, goal="-"
    ):
        self.db_cursor.execute(
            "SELECT insert_user_info(%s, %s, %s, %s, %s, %s, %s)",
            (
                gender,
                int(age),
                float(weight),
                float(height),
                activity,
                account_id,
                goal,
            ),
        )
        self.db_connection.commit()

    def insert_meal_info(
        self, meal_type, date, proteins, fats, carbohydrates, kilocalories, user_id
    ):
        self.db_cursor.execute(
            "SELECT insert_meal_info(%s, %s, %s, %s, %s, %s, %s)",
            (
                meal_type,
                date,
                proteins,
                fats,
                carbohydrates,
                kilocalories,
                user_id,
            ),
        )
        self.db_connection.commit()

    def update_meal_info(
        self, meal_type, date, proteins, fats, carbohydrates, kilocalories, user_id
    ):
        self.db_cursor.execute(
            "SELECT update_meal_info(%s, %s, %s, %s, %s, %s, %s)",
            (
                meal_type,
                date,
                proteins,
                fats,
                carbohydrates,
                kilocalories,
                user_id,
            ),
        )
        self.db_connection.commit()

    def update_password(self, new_password, login):
        self.db_cursor.execute(
            "SELECT change_password(%s, %s)",
            (
                new_password,
                login,
            ),
        )
        self.db_connection.commit()

    def update_user_statistic(
        self,
        kilocalories_intake,
        fats_intake,
        carbohydrates_intake,
        proteins_intake,
        date,
        weight_loss,
        user_id,
    ):
        self.db_cursor.execute(
            "SELECT update_statistic_info(%s, %s, %s, %s, %s, %s, %s)",
            (
                kilocalories_intake,
                fats_intake,
                carbohydrates_intake,
                proteins_intake,
                date,
                weight_loss,
                user_id,
            ),
        )
        self.db_connection.commit()

    def update_username(self, new_username, account_id):
        self.db_cursor.execute(
            "SELECT update_username(%s, %s)",
            (
                new_username,
                account_id,
            ),
        )
        self.db_connection.commit()

    def update_user_info(self, age, gender, weight, height, goal, account_id):
        self.db_cursor.execute(
            "SELECT update_user_info(%s, %s, %s, %s, %s, %s)",
            (
                age,
                gender,
                weight,
                height,
                goal,
                account_id,
            ),
        )
        self.db_connection.commit()

    def delete_fav_product(self, user_id, product_id):
        self.db_cursor.execute(
            "SELECT delete_fav_product(%s, %s)",
            (
                user_id,
                product_id,
            ),
        )
        self.db_connection.commit()

    def delete_account(self, account_id):
        self.db_cursor.execute("SELECT clear_account_table(%s)", (account_id,))
        self.db_connection.commit()

    def delete_database(self):
        self.close_connection()
        connection = ps.connect(self.config.to_connection_string())
        cursor = connection.cursor()
        cursor.execute("DROP DATABASE %s", (self.DB_NAME,))
        connection.commit()

    def close_connection(self):
        self.db_cursor.close()
        self.db_connection.close()
