import datetime as dt
import psycopg2 as ps
import io
import sqlite3 as sl
import tkinter
import tkinter.messagebox as mb
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Button, PhotoImage, Label, Text, ttk

ASSETS_PATH = Path(__file__).parent / "Images"


class DataBase:
    def __init__(self):
        self.db_params = {
            'user': 'postgres',
            'password': '123',
            'host': 'localhost',
            'port': '5432',
        }

        self.db_name = 'calories_app'

        try:
            self.db_connection = ps.connect(**self.db_params, dbname=self.db_name)
        except ps.OperationalError:
            self.db_connection = ps.connect(**self.db_params)

        self.db_cursor = self.db_connection.cursor()

    def create_tables(self):
        file = open('DataBase actions.sql')
        create_drop_func = file.read()
        file.close()

        self.db_cursor.execute(create_drop_func)

        self.db_cursor.execute('SELECT create_db(%s)', (self.db_name,))

    def initialize_functions(self):
        file = open('Delete_info_db.sql')
        delete_func = file.read()
        file.close()

        file = open('find_in_db.sql')
        find_func = file.read()
        file.close()

        file = open('Insert_into_db.sql')
        insert_func = file.read()
        file.close()

        file = open('update_db_table.sql')
        update_func = file.read()
        file.close()

        file = open('trigger_functions.sql')
        trigger_functions = file.read()
        file.close()

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
        self.db_cursor.execute('SELECT * FROM public.find_account_id_and_password(\'{}\')'.format(login))
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
        self.db_cursor.execute("SELECT * FROM get_user_statistic(%s, %s)", (user_id, date,))
        user_statistic = self.db_cursor.fetchone()

        return user_statistic if user_statistic else None

    def find_fav_product(self, user_id, product_id):
        self.db_cursor.execute("SELECT * FROM get_fav_product(%s, %s)", (user_id, product_id,))
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
        self.db_cursor.execute("SELECT * FROM get_meal_macro(%s, %s)", (user_id, date,))
        meal_macro = self.db_cursor.fetchall()

        return meal_macro if meal_macro else None

    def get_meal_info(self, meal_type, date, user_id):
        self.db_cursor.execute("SELECT * FROM get_meal_info(%s, %s, %s)", (meal_type, date, user_id,))
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
        self.db_cursor.execute("SELECT add_product_to_favourites(%s, %s)",
                               (user_id, product_id,))
        self.db_connection.commit()

    def insert_user_statistic(self, kilocalories_intake, fats_intake, carbohydrates_intake,
                              proteins_intake, date, weight_loss, user_id):
        self.db_cursor.execute("SELECT add_statistic_info(%s, %s, %s, %s, %s, %s, %s)",
                               (kilocalories_intake, fats_intake, carbohydrates_intake,
                                proteins_intake, date, weight_loss, user_id,))
        self.db_connection.commit()

    def insert_product_info(self, prod_id, name, proteins, fats, carbohydrates, kilocalories):
        self.db_cursor.execute("SELECT insert_product_info(%s, %s, %s, %s, %s, %s)",
                               (prod_id, name, proteins, fats, carbohydrates, kilocalories,))
        self.db_connection.commit()

    def insert_acc_info(self, login, password):
        self.db_cursor.execute("SELECT insert_account(%s, %s)", (login, password,))
        self.db_connection.commit()

    def insert_user_info(self, gender, account_id, activity, age=18, weight=70.0, height=180.0, goal='-'):
        self.db_cursor.execute("SELECT insert_user_info(%s, %s, %s, %s, %s, %s, %s)",
                               (gender, int(age), float(weight), float(height), activity, account_id, goal,)
                               )
        self.db_connection.commit()

    def insert_meal_info(self, meal_type, date, proteins, fats, carbohydrates, kilocalories, user_id):
        self.db_cursor.execute("SELECT insert_meal_info(%s, %s, %s, %s, %s, %s, %s)",
                               (meal_type, date, proteins, fats, carbohydrates, kilocalories, user_id,)
                               )
        self.db_connection.commit()

    def update_meal_info(self, meal_type, date, proteins, fats, carbohydrates, kilocalories, user_id):
        self.db_cursor.execute("SELECT update_meal_info(%s, %s, %s, %s, %s, %s, %s)",
                               (meal_type, date, proteins, fats, carbohydrates, kilocalories, user_id,)
                               )
        self.db_connection.commit()

    def update_password(self, new_password, login):
        self.db_cursor.execute("SELECT change_password(%s, %s)", (new_password, login,))
        self.db_connection.commit()

    def update_user_statistic(self, kilocalories_intake, fats_intake, carbohydrates_intake,
                              proteins_intake, date, weight_loss, user_id):
        self.db_cursor.execute("SELECT update_statistic_info(%s, %s, %s, %s, %s, %s, %s)",
                               (kilocalories_intake, fats_intake, carbohydrates_intake,
                                proteins_intake, date, weight_loss, user_id,))
        self.db_connection.commit()

    def update_username(self, new_username, account_id):
        self.db_cursor.execute("SELECT update_username(%s, %s)",
                               (new_username, account_id,))
        self.db_connection.commit()

    def update_user_info(self, age, gender, weight, height, goal, account_id):
        self.db_cursor.execute("SELECT update_user_info(%s, %s, %s, %s, %s, %s)",
                               (age, gender, weight, height, goal, account_id,))
        self.db_connection.commit()

    def delete_fav_product(self, user_id, product_id):
        self.db_cursor.execute("SELECT delete_fav_product(%s, %s)", (user_id, product_id,))
        self.db_connection.commit()

    def delete_account(self, account_id):
        self.db_cursor.execute("SELECT clear_account_table(%s)", (account_id,))
        self.db_connection.commit()

    def delete_database(self):
        self.db_cursor.execute("SELECT drop_db(%s)", ('calories_app',))
        self.db_connection.commit()

    def close_connection(self):
        self.db_cursor.close()
        self.db_connection.close()


class AuthorizationWindow:
    def __init__(self):
        self.window = Tk()
        self.window.geometry("700x500")
        self.window.configure(bg="#F3ACFF")

        self.db = DataBase()
        self.db.create_tables()

        self.create_widgets()

        self.db.initialize_functions()

    def create_widgets(self):
        self.canvas = Canvas(
            self.window,
            bg="#F3ACFF",
            height=500,
            width=700,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        self.draw_background()

        self.canvas.create_rectangle(350.0, 200.0, 700.0, 203.0, fill="#000000", outline="")

        self.draw_logo()

        self.draw_login_form()
        self.draw_buttons()

    def draw_background(self):
        self.canvas.create_rectangle(0, 0, 350, 500, fill="#F1FFA1", outline="")

    def draw_logo(self):
        self.canvas.create_text(
            34.99999999999997,
            123.0,
            anchor="nw",
            text="MEOW",
            fill="#000000",
            font=("Inter", 40 * -1)
        )

        self.image_1 = PhotoImage(file=ASSETS_PATH / "image_1.png")
        self.canvas.create_image(161, 342, image=self.image_1)

    def draw_login_form(self):
        self.canvas.create_text(
            525.0, 30,
            text="Login:",
            font=("Inter", 18),
            fill="#000"
        )

        self.canvas.create_text(
            525.0, 131,
            text="Password:",
            font=("Inter", 18),
            fill="#000"
        )

        self.login_entry = Entry(bd=0, bg="#D9D9D9", fg="#000716")
        self.login_entry.place(x=445, y=46, width=165, height=30)

        self.password_entry = Entry(bd=0, bg="#D9D9D9", fg="#000716", show="*")
        self.password_entry.place(x=445, y=146, width=165, height=30)

    def draw_buttons(self):
        self.auth_button_image = PhotoImage(file=ASSETS_PATH / "button_1.png")
        self.auth_button = Button(
            image=self.auth_button_image, command=lambda: self.verify_user())
        self.auth_button.place(x=445, y=220, width=154, height=52)

        self.reg_button_image = PhotoImage(file=ASSETS_PATH / "button_2.png")
        self.reg_button = Button(
            image=self.reg_button_image, command=lambda: [self.window.destroy(), RegistrationWindow()])
        self.reg_button.place(x=445, y=297, width=154, height=52)

        self.resset_button_image = PhotoImage(file=ASSETS_PATH / "button_3.png")
        self.resset_button = Button(
            image=self.resset_button_image, command=lambda: [self.window.destroy(), RessetWindow()])
        self.resset_button.place(x=445, y=374, width=154, height=52)

    def verify_user(self):
        user_pass = self.db.find_id_and_password(self.login_entry.get())

        if not user_pass:
            mb.showerror("Error", "User does not exists!")
        elif not (user_pass[1] == self.password_entry.get()):
            mb.showerror("Error", "Incorrect password!")
        else:
            self.window.destroy()
            DiaryWindow(user_pass[0])

    def run(self):
        self.window.mainloop()


class RegistrationWindow:
    def __init__(self):
        self.window = Tk()

        self.window.geometry("400x500")
        self.window.configure(bg="#D8D5D5")

        self.db = DataBase()

        self.window.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):
        self.canvas = Canvas(
            self.window,
            bg="#D8D5D5",
            height=500,
            width=400,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        self.draw_buttons()
        self.draw_input()

    def draw_buttons(self):
        self.reg_button_image = PhotoImage(file=ASSETS_PATH / "reg_button_1.png")
        self.reg_button = Button(
            image=self.reg_button_image, command=lambda: self.user_registration())
        self.reg_button.place(x=132, y=412, width=127, height=35)

    def draw_input(self):
        # Поле логин
        self.canvas.create_text(
            98.0,
            25.0,
            anchor="nw",
            text="Username:",
            fill="#2C302C",
            font=("Inter", 16 * -1)
        )
        self.username_entry = Entry(bd=0, bg="#2C302C", fg="#FFFFFF", highlightthickness=0)
        self.username_entry.place(x=98.0, y=45.0, width=196.0, height=26.0)

        # Поле пароль
        self.canvas.create_text(
            98.0,
            75.0,
            anchor="nw",
            text="Password:",
            fill="#2C302C",
            font=("Inter", 16 * -1)
        )
        self.password_entry = Entry(bd=0, bg="#2C302C", fg="#FFFFFF", highlightthickness=0)
        self.password_entry.place(x=98.0, y=95, width=196.0, height=26.0)

        # Поле возраст
        self.canvas.create_text(
            98.0,
            124.0,
            anchor="nw",
            text="Age:",
            fill="#2C302C",
            font=("Inter", 16 * -1)
        )
        self.age_entry = Entry(bd=0, bg="#2C302C", fg="#FFFFFF", highlightthickness=0)
        self.age_entry.place(x=98.0, y=143, width=196.0, height=26.0)

        # Выбор гендера
        self.gender_var = tkinter.StringVar(self.canvas)
        self.gender_var.set('Male')
        self.gender_menu = tkinter.OptionMenu(self.canvas, self.gender_var, *["Male", "Female"])
        self.gender_menu.config(bg="#2C302C", fg="#FFFFFF")
        self.gender_menu.place(x=98.0, y=177, width=85.0, height=26.0)

        # Выбор активности
        self.activity_var = tkinter.StringVar(self.canvas)
        self.activity_var.set('Medium')
        self.activity_menu = tkinter.OptionMenu(self.canvas, self.activity_var,
                                                *["Very low", "Low", "Medium", "High", "Very high"])
        self.activity_menu.config(bg="#2C302C", fg="#FFFFFF")
        self.activity_menu.place(x=198.0, y=177, width=85.0, height=26.0)

        # Поле вес
        self.canvas.create_text(
            98.0,
            211.0,
            anchor="nw",
            text="Weight (kg):",
            fill="#2C302C",
            font=("Inter", 16 * -1)
        )
        self.weight_entry = Entry(bd=0, bg="#2C302C", fg="#FFFFFF", highlightthickness=0)
        self.weight_entry.place(x=98.0, y=230, width=196.0, height=26.0)

        # Поле рост
        self.canvas.create_text(
            98.0,
            264.0,
            anchor="nw",
            text="Height (cm):",
            fill="#2C302C",
            font=("Inter", 16 * -1)
        )
        self.height_entry = Entry(bd=0, bg="#2C302C", fg="#FFFFFF", highlightthickness=0)
        self.height_entry.place(x=98.0, y=283, width=196.0, height=26.0)

        # Поле цели
        self.canvas.create_text(
            98.0,
            317.0,
            anchor="nw",
            text="Goal:",
            fill="#2C302C",
            font=("Inter", 16 * -1)
        )
        self.goal_entry = Text(self.canvas, bg="#2C302C", fg="#FFFFFF")
        self.goal_entry.place(x=98.0, y=336, width=196.0, height=50.0)
        self.goal_entry.configure(state="normal")

    def user_registration(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        sex, age = self.gender_var.get(), self.age_entry.get()
        activity = self.activity_var.get()
        weight, height = self.weight_entry.get(), self.height_entry.get()

        goal = self.goal_entry.get("1.0", "end-1c")
        goal = 'Empty' if len(goal) == 0 else goal

        # Поиск id аккаунта
        account_id = self.db.find_id_and_password(username)

        if account_id is not None:
            mb.showerror("Error", "This user is already exists")

        else:
            # Вставка данных аккаунта в БД
            self.db.insert_acc_info(username, password)

            account_id = self.db.find_id_and_password(username)

            # Вставка данных пользователя в БД
            self.db.insert_user_info(gender=sex.lower(), age=age, weight=weight, height=height,
                                     goal=goal, activity=activity, account_id=account_id[0])

            self.window.destroy()
            AuthorizationWindow()


class RessetWindow:
    def __init__(self):
        self.window = Tk()

        self.window.geometry("200x200")
        self.window.configure(bg="#D8D5D5")

        self.db = DataBase()

        self.window.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):
        self.canvas = Canvas(
            self.window,
            bg="#D8D5D5",
            height=200,
            width=200,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        self.draw_verify_button()
        self.draw_input()

    def draw_input(self):
        self.canvas.create_text(
            62.0,
            25.0,
            anchor="nw",
            text="Username:",
            fill="#2C302C",
            font=("Inter", 16 * -1)
        )
        self.username_entry = Entry(bd=0, bg="#2C302C", fg="#FFFFFF", highlightthickness=0)
        self.username_entry.place(x=35.0, y=45.0, width=130.0, height=26.0)

    def draw_verify_button(self):
        self.verify_button_image = PhotoImage(file=ASSETS_PATH / "verify_button.png")
        self.verify_button = Button(
            image=self.verify_button_image, command=lambda: self.verify_user())
        self.verify_button.place(x=59, y=139, width=82, height=33)

    def verify_user(self):
        user_pass = self.db.find_id_and_password(self.username_entry.get())[1]

        if user_pass is None:
            mb.showerror("Error", "User does not exists!")
        else:
            username = self.username_entry.get()
            self.window.destroy()
            self.draw_reset(user_pass[0], username)

    def draw_reset(self, password, username):
        self.window = Tk()

        self.window.geometry("200x200")
        self.window.configure(bg="#D8D5D5")

        self.window.resizable(False, False)

        self.canvas = Canvas(
            self.window,
            bg="#D8D5D5",
            height=200,
            width=200,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        self.canvas.create_text(
            62.0,
            25.0,
            anchor="nw",
            text="Password:",
            fill="#2C302C",
            font=("Inter", 16 * -1)
        )
        self.password_entry = Entry(bd=0, bg="#2C302C", fg="#FFFFFF", highlightthickness=0)
        self.password_entry.place(x=35.0, y=45.0, width=130.0, height=26.0)

        self.reset_button_image = PhotoImage(file=ASSETS_PATH / "reset_button.png")
        self.reset_button = Button(
            image=self.reset_button_image,
            command=lambda: self.update_password(password, self.password_entry.get(), username))
        self.reset_button.place(x=59, y=139, width=82, height=33)

    def update_password(self, prev_password, new_password, username):
        if prev_password == new_password:
            mb.showerror("Error", "You have already used this password")

        elif len(new_password.split()) != 1:
            mb.showerror("Error", "Password field cannot contain spaces")

        else:
            self.db.update_password(new_password, username)
            mb.showinfo("Successfully", "Password was successfully changed")

            self.window.destroy()
            AuthorizationWindow()


class DiaryWindow:
    def __init__(self, account_id):
        self.window = Tk()
        self.window.geometry("700x600")
        self.window.configure(bg="#D8D5D5")

        self.window.resizable(False, False)

        self.db = DataBase()
        self.account_id = account_id

        self.create_widgets()
        self.fill_product_table()

    def fill_product_table(self):

        product = self.db.get_product()
        if product is None:
            with io.open('DataBase.txt', encoding='utf-8') as file:
                for line in file:
                    values = line.split("?")
                    self.db.insert_product_info(*values)

    def create_widgets(self):
        self.canvas = Canvas(
            self.window,
            bg="#D8D5D5",
            height=600,
            width=700,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        self.draw_buttons()
        self.draw_background()

    def draw_background(self):
        self.canvas.create_rectangle(0.0, 87.0, 700.0, 90.0, fill="#000000", outline="")

    def draw_buttons(self):
        # Кнопка аккаунт
        self.acc_button_image = PhotoImage(file=ASSETS_PATH / "Me_button.png")
        self.acc_button = Button(
            image=self.acc_button_image, command=lambda: [self.window.destroy(), AccountWindow(self.account_id)])
        self.acc_button.place(x=564, y=5, width=70, height=70)

        # Кнопка статистика
        self.stat_button_image = PhotoImage(file=ASSETS_PATH / "Reports_button.png")
        self.stat_button = Button(
            image=self.stat_button_image, command=lambda: [self.window.destroy(), ReportWindow(self.account_id)])
        self.stat_button.place(x=394, y=5, width=70, height=70)

        # Кнопка избранное
        self.favour_button_image = PhotoImage(file=ASSETS_PATH / "Favourites_button.png")
        self.favour_button = Button(
            image=self.favour_button_image, command=lambda: [self.window.destroy(), FavouritesWindow(self.account_id)])
        self.favour_button.place(x=224, y=5, width=70, height=70)

        # Кнопка дневник
        self.diary_button_image = PhotoImage(file=ASSETS_PATH / "Diary_button.png")
        self.diary_button = Button(
            image=self.diary_button_image, command=lambda: [self.window.destroy(), DiaryWindow(self.account_id)])
        self.diary_button.place(x=54, y=5, width=70, height=70)

        # Кнопка завтрак
        self.breakfast_button_image = PhotoImage(file=ASSETS_PATH / "Breakfast_button.png")
        self.breakfast_button = Button(
            image=self.breakfast_button_image, command=lambda: self.breakfast_wind())
        self.breakfast_button.place(x=38, y=153, width=624, height=80)

        # Кнопка обед
        self.lunch_button_image = PhotoImage(file=ASSETS_PATH / "Lunch_button.png")
        self.lunch_button = Button(
            image=self.lunch_button_image, command=lambda: self.lunch_wind())
        self.lunch_button.place(x=38, y=284, width=624, height=80)

        # Кнопка ужин
        self.dinner_button_image = PhotoImage(file=ASSETS_PATH / "Dinner_button.png")
        self.dinner_button = Button(
            image=self.dinner_button_image, command=lambda: self.dinner_wind())
        self.dinner_button.place(x=38, y=415, width=624, height=80)

    def breakfast_wind(self):
        DietList(self.account_id, "Breakfast")

    def lunch_wind(self):
        DietList(self.account_id, "Lunch")

    def dinner_wind(self):
        DietList(self.account_id, "Dinner")


class DietList:
    def __init__(self, account_id, meal_type=""):
        self.new_window = tkinter.Toplevel()
        self.new_window.geometry("700x500")
        self.new_window.configure(bg="#D8D5D5")

        self.new_window.resizable(False, False)

        self.new_window.grab_set()

        self.db = DataBase()

        self.meal_type = meal_type
        self.account_id = account_id
        self.user_id = self.db.find_user_id(account_id)

        self.get_components()

        self.create_widgets()

    def create_widgets(self):
        self.new_canvas = Canvas(
            self.new_window,
            bg="#D8D5D5",
            height=500,
            width=700,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.new_canvas.place(x=0, y=0)

        self.draw_entry()
        self.draw_buttons()

        self.get_table()

    def draw_entry(self):
        self.new_canvas.create_text(
            235.0,
            11.0,
            anchor="nw",
            text="Enter the name of the dish:",
            fill="#000000",
            font=("Inter", 18 * -1)
        )

        self.entry_field = Entry(self.new_canvas, bd=0, bg="#2C302C", fg="#FFFFFF", highlightthickness=0)
        self.entry_field.place(x=71.0, y=33.0, width=559.0, height=57.0)

    def draw_buttons(self):
        # Кнопка поиска
        self.search_button_image = PhotoImage(file=ASSETS_PATH / "search_button.png")
        self.search_button = Button(
            self.new_canvas, image=self.search_button_image, command=lambda: self.get_table())
        self.search_button.place(x=285, y=101, width=117, height=43)

        # Кнопка посмотреть избранное
        self.fav_list_button_image = PhotoImage(file=ASSETS_PATH / "fav_list_button.png")
        self.fav_list_button = Button(self.new_canvas, image=self.fav_list_button_image,
                                      command=lambda: self.favourite_window())
        self.fav_list_button.place(x=71, y=414, width=117, height=50)

        # Кнопка добавить в рацион
        self.add_diet_button_image = PhotoImage(file=ASSETS_PATH / "add_diet_button.png")
        self.add_diet_button = Button(self.new_canvas, image=self.add_diet_button_image,
                                      command=lambda: self.add_to_diet())
        self.add_diet_button.place(x=285, y=414, width=140, height=49)

    def get_table(self):
        search_prod = self.entry_field.get()
        products = self.db.find_product(search_prod)

        self.favourite_tree = ttk.Treeview(self.new_canvas, selectmode="browse")
        self.favourite_tree.delete(*self.favourite_tree.get_children())

        self.favourite_tree.configure(yscrollcommand=tkinter.Scrollbar(self.new_window).set)
        self.favourite_tree.configure(yscroll=tkinter.YES, xscroll=tkinter.YES)
        self.favourite_tree["columns"] = ("id", "name", "proteins", "fats", "carbohydrates", "kilocalories")

        self.favourite_tree.column("#0", width=0, stretch=tkinter.NO)
        self.favourite_tree.heading("#0", text="", anchor=tkinter.W)

        self.favourite_tree.column("id", anchor=tkinter.CENTER, width=50)
        self.favourite_tree.heading("id", text="ID", anchor=tkinter.CENTER)

        self.favourite_tree.column("name", anchor=tkinter.W, width=150)
        self.favourite_tree.heading("name", text="Name", anchor=tkinter.CENTER)

        self.favourite_tree.column("proteins", anchor=tkinter.CENTER, width=100)
        self.favourite_tree.heading("proteins", text="Proteins", anchor=tkinter.CENTER)

        self.favourite_tree.column("fats", anchor=tkinter.CENTER, width=100)
        self.favourite_tree.heading("fats", text="Fats", anchor=tkinter.CENTER)

        self.favourite_tree.column("carbohydrates", anchor=tkinter.CENTER, width=100)
        self.favourite_tree.heading("carbohydrates", text="Carbohydrates", anchor=tkinter.CENTER)

        self.favourite_tree.column("kilocalories", anchor=tkinter.CENTER, width=100)
        self.favourite_tree.heading("kilocalories", text="Kilocalories", anchor=tkinter.CENTER)

        for product in products:
            self.favourite_tree.insert("", "end", values=(product[0], product[1], product[2], product[3],
                                                          product[4], product[5]))
        self.favourite_tree.place(x=44, y=175)

    def add_to_diet(self):
        selected_item = self.favourite_tree.selection()[0]
        product_id = self.favourite_tree.item(selected_item, option="values")[0]

        product_info = self.db.get_prod_info(product_id)

        self.proteins += product_info[0]
        self.fats += product_info[1]
        self.carbohydrates += product_info[2]
        self.kilocalories += product_info[3]

        self.add_to_db()

    def get_components(self):
        date = dt.datetime.now().date()

        meal = self.db.get_meal_info(self.meal_type, date, self.user_id)

        self.proteins = meal[0] if meal else 0
        self.fats = meal[1] if meal else 0
        self.carbohydrates = meal[2] if meal else 0
        self.kilocalories = meal[3] if meal else 0

    def add_to_db(self):
        date = dt.datetime.now().date()

        exists = self.db.get_meal_info(self.meal_type, date, self.user_id)

        if not exists:
            self.db.insert_meal_info(self.meal_type, date, self.proteins, self.fats,
                                     self.carbohydrates, self.kilocalories, self.user_id)

        else:
            self.db.update_meal_info(self.meal_type, date, self.proteins, self.fats,
                                     self.carbohydrates, self.kilocalories, self.user_id)

    def favourite_window(self):
        self.third_window = tkinter.Toplevel()

        self.third_window.geometry("700x400")
        self.third_window.configure(bg="#D8D5D5")

        self.third_window.resizable(False, False)

        self.third_window.grab_set()

        self.third_canvas = Canvas(
            self.third_window,
            bg="#D8D5D5",
            height=400,
            width=700,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.third_canvas.place(x=0, y=0)

        # Кнопка добавить в рацион
        self.add_diet_button2_image = PhotoImage(file=ASSETS_PATH / "add_diet_button.png")
        self.add_diet_button2 = Button(self.third_canvas, image=self.add_diet_button2_image,
                                       command=lambda: self.add_to_diet())
        self.add_diet_button2.place(x=275, y=300, width=147, height=49)

        products = self.db.get_favourite_products(self.user_id)

        self.favourite_tree = ttk.Treeview(self.third_canvas, selectmode="browse")
        self.favourite_tree.delete(*self.favourite_tree.get_children())

        self.favourite_tree.configure(yscrollcommand=tkinter.Scrollbar(self.new_window).set)
        self.favourite_tree.configure(yscroll=tkinter.YES, xscroll=tkinter.YES)
        self.favourite_tree["columns"] = ("id", "name", "proteins", "fats", "carbohydrates", "kilocalories")

        self.favourite_tree.column("#0", width=0, stretch=tkinter.NO)
        self.favourite_tree.heading("#0", text="", anchor=tkinter.W)

        self.favourite_tree.column("id", anchor=tkinter.CENTER, width=50)
        self.favourite_tree.heading("id", text="ID", anchor=tkinter.CENTER)

        self.favourite_tree.column("name", anchor=tkinter.W, width=150)
        self.favourite_tree.heading("name", text="Name", anchor=tkinter.CENTER)

        self.favourite_tree.column("proteins", anchor=tkinter.CENTER, width=100)
        self.favourite_tree.heading("proteins", text="Proteins", anchor=tkinter.CENTER)

        self.favourite_tree.column("fats", anchor=tkinter.CENTER, width=100)
        self.favourite_tree.heading("fats", text="Fats", anchor=tkinter.CENTER)

        self.favourite_tree.column("carbohydrates", anchor=tkinter.CENTER, width=100)
        self.favourite_tree.heading("carbohydrates", text="Carbohydrates", anchor=tkinter.CENTER)

        self.favourite_tree.column("kilocalories", anchor=tkinter.CENTER, width=100)
        self.favourite_tree.heading("kilocalories", text="Kilocalories", anchor=tkinter.CENTER)

        for product in products if products else '':
            self.favourite_tree.insert("", "end", values=(product[0], product[1], product[2], product[3],
                                                          product[4], product[5]))
        self.favourite_tree.place(x=50, y=30)


class FavouritesWindow:
    def __init__(self, account_id):
        self.window = Tk()
        self.window.geometry("700x600")
        self.window.configure(bg="#D8D5D5")

        self.window.resizable(False, False)

        self.db = DataBase()
        self.account_id = account_id
        self.user_id = self.db.find_user_id(account_id)

        self.create_widgets()

    def create_widgets(self):
        self.canvas = Canvas(
            self.window,
            bg="#D8D5D5",
            height=600,
            width=700,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        self.draw_buttons()
        self.draw_background()
        self.draw_input()

        self.output_table()

    def draw_buttons(self):
        # Кнопка аккаунт
        self.acc_button_image = PhotoImage(file=ASSETS_PATH / "Me_button.png")
        self.acc_button = Button(
            image=self.acc_button_image, command=lambda: [self.window.destroy(), AccountWindow(self.account_id)])
        self.acc_button.place(x=564, y=5, width=70, height=70)

        # Кнопка статистика
        self.stat_button_image = PhotoImage(file=ASSETS_PATH / "Reports_button.png")
        self.stat_button = Button(
            image=self.stat_button_image, command=lambda: [self.window.destroy(), ReportWindow(self.account_id)])
        self.stat_button.place(x=394, y=5, width=70, height=70)

        # Кнопка избранное
        self.favour_button_image = PhotoImage(file=ASSETS_PATH / "Favourites_button.png")
        self.favour_button = Button(
            image=self.favour_button_image, command=lambda: [self.window.destroy(), FavouritesWindow(self.account_id)])
        self.favour_button.place(x=224, y=5, width=70, height=70)

        # Кнопка дневник
        self.diary_button_image = PhotoImage(file=ASSETS_PATH / "Diary_button.png")
        self.diary_button = Button(
            image=self.diary_button_image, command=lambda: [self.window.destroy(), DiaryWindow(self.account_id)])
        self.diary_button.place(x=54, y=5, width=70, height=70)

        # Кнопка поиска
        self.search_button_image = PhotoImage(file=ASSETS_PATH / "search_button.png")
        self.search_button = Button(
            image=self.search_button_image,
            command=lambda: self.output_table())
        self.search_button.place(x=286, y=170, width=127, height=49)

        # Кнопка добавить в избранное
        self.add_fav_button_image = PhotoImage(file=ASSETS_PATH / "add_fav_button.png")
        self.add_fav_button = Button(
            image=self.add_fav_button_image,
            command=lambda: self.add_to_favourites())
        self.add_fav_button.place(x=280, y=480, width=140, height=49)

        # Кнопка посмотреть избранное
        self.fav_list_button_image = PhotoImage(file=ASSETS_PATH / "fav_list_button.png")
        self.fav_list_button = Button(
            image=self.fav_list_button_image,
            command=lambda: FavouriteList(self.account_id))
        self.fav_list_button.place(x=65, y=480, width=127, height=49)

    def draw_background(self):
        self.canvas.create_rectangle(0.0, 87.0, 700.0, 90.0, fill="#000000", outline="")

    def draw_input(self):
        self.canvas.create_text(
            269.0,
            100.0,
            anchor="nw",
            text="Enter a product name:",
            fill="#2C302C",
            font=("Inter", 16 * -1)
        )

        self.entry_field = Entry(bd=0, bg="#2C302C", fg="#FFFFFF", highlightthickness=0)
        self.entry_field.place(x=254.0, y=120.0, width=192.0, height=39.0)

    def output_table(self):
        search_prod = self.entry_field.get()
        products = self.db.find_product(search_prod)

        self.product_tree = ttk.Treeview(self.canvas, selectmode="browse")
        self.product_tree.delete(*self.product_tree.get_children())

        self.product_tree.configure(yscrollcommand=tkinter.Scrollbar(self.window).set)
        self.product_tree.configure(yscroll=tkinter.YES, xscroll=tkinter.YES)
        self.product_tree["columns"] = ("id", "name", "proteins", "fats", "carbohydrates", "kilocalories")

        self.product_tree.column("#0", width=0, stretch=tkinter.NO)
        self.product_tree.heading("#0", text="", anchor=tkinter.W)

        self.product_tree.column("id", anchor=tkinter.CENTER, width=50)
        self.product_tree.heading("id", text="ID", anchor=tkinter.CENTER)

        self.product_tree.column("name", anchor=tkinter.W, width=150)
        self.product_tree.heading("name", text="Name", anchor=tkinter.CENTER)

        self.product_tree.column("proteins", anchor=tkinter.CENTER, width=100)
        self.product_tree.heading("proteins", text="Proteins", anchor=tkinter.CENTER)

        self.product_tree.column("fats", anchor=tkinter.CENTER, width=100)
        self.product_tree.heading("fats", text="Fats", anchor=tkinter.CENTER)

        self.product_tree.column("carbohydrates", anchor=tkinter.CENTER, width=100)
        self.product_tree.heading("carbohydrates", text="Carbohydrates", anchor=tkinter.CENTER)

        self.product_tree.column("kilocalories", anchor=tkinter.CENTER, width=100)
        self.product_tree.heading("kilocalories", text="Kilocalories", anchor=tkinter.CENTER)

        for product in products:
            self.product_tree.insert("", "end", values=(product[0], product[1], product[2], product[3],
                                                        product[4], product[5]))
        self.product_tree.place(x=48, y=230)

    def add_to_favourites(self):
        selected_item = self.product_tree.selection()[0]
        product_id = self.product_tree.item(selected_item, option="values")[0]

        prod_is_in = self.db.find_fav_product(self.user_id, product_id)

        if not prod_is_in[0]:
            self.db.add_to_favourites(self.user_id, product_id)


class FavouriteList:
    def __init__(self, account_id):
        self.new_window = tkinter.Toplevel()

        self.new_window.geometry("700x400")
        self.new_window.configure(bg="#D8D5D5")

        self.new_window.resizable(False, False)
        self.new_window.grab_set()

        self.db = DataBase()
        self.account_id = account_id
        self.user_id = self.db.find_user_id(account_id)

        self.create_widgets()

    def create_widgets(self):
        self.new_canvas = Canvas(
            self.new_window,
            bg="#D8D5D5",
            height=400,
            width=700,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.new_canvas.place(x=0, y=0)

        self.draw_button()
        self.get_table()

    def draw_button(self):
        # Кнопка удалить избранное
        self.del_fav_button_image = PhotoImage(file=ASSETS_PATH / "del_fav_button.png")
        self.del_fav_button = Button(self.new_canvas, image=self.del_fav_button_image,
                                     command=lambda: self.delete_fav())
        self.del_fav_button.place(x=275, y=300, width=147, height=49)

    def get_table(self):
        products = self.db.get_favourite_products(self.user_id)

        self.favourite_tree = ttk.Treeview(self.new_canvas, selectmode="browse")
        self.favourite_tree.delete(*self.favourite_tree.get_children())

        self.favourite_tree.configure(yscrollcommand=tkinter.Scrollbar(self.new_window).set)
        self.favourite_tree.configure(yscroll=tkinter.YES, xscroll=tkinter.YES)
        self.favourite_tree["columns"] = ("id", "name", "proteins", "fats", "carbohydrates", "kilocalories")

        self.favourite_tree.column("#0", width=0, stretch=tkinter.NO)
        self.favourite_tree.heading("#0", text="", anchor=tkinter.W)

        self.favourite_tree.column("id", anchor=tkinter.CENTER, width=50)
        self.favourite_tree.heading("id", text="ID", anchor=tkinter.CENTER)

        self.favourite_tree.column("name", anchor=tkinter.W, width=150)
        self.favourite_tree.heading("name", text="Name", anchor=tkinter.CENTER)

        self.favourite_tree.column("proteins", anchor=tkinter.CENTER, width=100)
        self.favourite_tree.heading("proteins", text="Proteins", anchor=tkinter.CENTER)

        self.favourite_tree.column("fats", anchor=tkinter.CENTER, width=100)
        self.favourite_tree.heading("fats", text="Fats", anchor=tkinter.CENTER)

        self.favourite_tree.column("carbohydrates", anchor=tkinter.CENTER, width=100)
        self.favourite_tree.heading("carbohydrates", text="Carbohydrates", anchor=tkinter.CENTER)

        self.favourite_tree.column("kilocalories", anchor=tkinter.CENTER, width=100)
        self.favourite_tree.heading("kilocalories", text="Kilocalories", anchor=tkinter.CENTER)

        for product in products if products else '':
            self.favourite_tree.insert("", "end", values=(product[0], product[1], product[2], product[3],
                                                          product[4], product[5]))
        self.favourite_tree.place(x=50, y=30)

    def delete_fav(self):
        selected_item = self.favourite_tree.selection()[0]
        product_id = self.favourite_tree.item(selected_item, option="values")[0]

        self.db.delete_fav_product(self.user_id, product_id)
        self.get_table()


class ReportWindow:
    def __init__(self, account_id):
        self.window = Tk()
        self.window.geometry("700x600")
        self.window.configure(bg="#D8D5D5")

        self.window.resizable(False, False)

        self.db = DataBase()
        self.account_id = account_id
        self.user_id = self.db.find_user_id(account_id)

        self.total_num_proteins, self.total_num_fats = 0, 0
        self.total_num_carbohydrates, self.total_num_calories = 0, 0
        self.difference = 0

        self.get_diet_info()

        self.create_widgets()
        self.draw_logo()

    def create_widgets(self):
        self.canvas = Canvas(
            self.window,
            bg="#D8D5D5",
            height=600,
            width=700,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        self.draw_buttons()
        self.draw_background()

    def draw_logo(self):
        self.cat_image = PhotoImage(file=ASSETS_PATH / "sad_cat.png")
        self.canvas.create_image(350, 350, image=self.cat_image)

    def draw_buttons(self):
        # Кнопка аккаунт
        self.acc_button_image = PhotoImage(file=ASSETS_PATH / "Me_button.png")
        self.acc_button = Button(
            image=self.acc_button_image, command=lambda: [self.window.destroy(), AccountWindow(self.account_id)])
        self.acc_button.place(x=564, y=5, width=70, height=70)

        # Кнопка статистика
        self.stat_button_image = PhotoImage(file=ASSETS_PATH / "Reports_button.png")
        self.stat_button = Button(
            image=self.stat_button_image, command=lambda: [self.window.destroy(), ReportWindow(self.account_id)])
        self.stat_button.place(x=394, y=5, width=70, height=70)

        # Кнопка избранное
        self.favour_button_image = PhotoImage(file=ASSETS_PATH / "Favourites_button.png")
        self.favour_button = Button(
            image=self.favour_button_image, command=lambda: [self.window.destroy(), FavouritesWindow(self.account_id)])
        self.favour_button.place(x=224, y=5, width=70, height=70)

        # Кнопка дневник
        self.diary_button_image = PhotoImage(file=ASSETS_PATH / "Diary_button.png")
        self.diary_button = Button(
            image=self.diary_button_image, command=lambda: [self.window.destroy(), DiaryWindow(self.account_id)])
        self.diary_button.place(x=54, y=5, width=70, height=70)

        # Кнопка калорий
        self.calories_button_image = PhotoImage(file=ASSETS_PATH / "calories_button.png")
        self.calories_button = Button(
            image=self.calories_button_image, command=lambda: self.calories_page())
        self.calories_button.place(x=95, y=95, width=164, height=43)

        # Кнопка состав
        self.macros_button_image = PhotoImage(file=ASSETS_PATH / "macros_button.png")
        self.macros_button = Button(
            image=self.macros_button_image, command=lambda: self.macros_page())
        self.macros_button.place(x=429, y=95, width=164, height=43)

    def draw_background(self):
        self.canvas.create_rectangle(0.0, 87.0, 700.0, 90.0, fill="#000000", outline="")

        self.canvas.create_rectangle(0.0, 146.0, 700.0, 149.0, fill="#000000", outline="")

    def get_diet_info(self):
        curr_date = dt.datetime.now().date()

        meal = self.db.get_meal_macro(self.user_id, curr_date)
        if meal is not None:
            self.meal_info = [tuple(map(float, meal[i])) if i < len(meal)
                              else (tuple(0 for _ in range(4))) for i in range(3)]
        else:
            self.meal_info = [tuple(0 for _ in range(4)) for _ in range(3)]

        self.user_info = self.db.get_user_info(self.user_id)
        self.get_meal_macros()

    def get_meal_macros(self):
        self.kilocalories = [self.meal_info[0][3], self.meal_info[2][3], self.meal_info[1][3]]
        self.total_num_calories = sum(self.kilocalories)

        self.proteins = [self.meal_info[0][0], self.meal_info[2][0], self.meal_info[1][0]]
        self.fats = [self.meal_info[0][1], self.meal_info[2][1], self.meal_info[1][1]]
        self.carbohydrates = [self.meal_info[0][2], self.meal_info[2][2], self.meal_info[1][2]]

        self.total_num_proteins = sum(self.proteins)
        self.total_num_fats = sum(self.fats)
        self.total_num_carbohydrates = sum(self.carbohydrates)

    def calories_page(self):
        self.canvas.destroy()
        self.create_widgets()

        # Поле со средним кол-вом калорий за сутки
        self.canvas.create_text(
            35.0,
            166.0,
            anchor="nw",
            text="AVG calories for the meal:",
            fill="#000000",
            font=("Inter", 20 * -1)
        )
        self.avg_calories = Label(self.canvas, text=f'{(self.total_num_calories / 3):.3f} kcal', bg="#2C302C",
                                  fg="#FFFFFF")
        self.avg_calories.place(x=321, y=159, width=338, height=42)

        self.total_num_calories = float(sum(self.kilocalories)) if sum(self.kilocalories) != 0 else 1

        # Поле с кол-вом калорий за завтрак
        self.canvas.create_text(
            35.0,
            259.0,
            anchor="nw",
            text="Breakfast:",
            fill="#000000",
            font=("Inter", 20 * -1)
        )
        self.break_calories = Label(self.canvas, text=f'{(self.kilocalories[0]):.3f} kcal', bg="#2C302C", fg="#FFFFFF")
        self.break_calories.place(x=165, y=252, width=94, height=42)

        self.break_calories_perc = Label(self.canvas,
                                         text=f'{(self.kilocalories[0]) / self.total_num_calories * 100:.2f} %',
                                         bg="#2C302C",
                                         fg="#FFFFFF")
        self.break_calories_perc.place(x=303, y=252, width=182, height=42)

        # Поле с кол-вом калорий за обэд
        self.canvas.create_text(
            35.0,
            359.0,
            anchor="nw",
            text="Lunch:",
            fill="#000000",
            font=("Inter", 20 * -1)
        )
        self.lunch_calories = Label(self.canvas, text=f'{(self.kilocalories[1]):.3f} kcal', bg="#2C302C", fg="#FFFFFF")
        self.lunch_calories.place(x=124, y=353, width=94, height=42)

        self.lunch_calories_perc = Label(self.canvas,
                                         text=f'{(self.kilocalories[1]) / self.total_num_calories * 100:.2f} %',
                                         bg="#2C302C",
                                         fg="#FFFFFF")
        self.lunch_calories_perc.place(x=259, y=353, width=182, height=42)

        # Поле с кол-вом калорий за ужин
        self.canvas.create_text(
            35.0,
            459.0,
            anchor="nw",
            text="Dinner:",
            fill="#000000",
            font=("Inter", 20 * -1)
        )
        self.dinner_calories = Label(self.canvas, text=f'{(self.kilocalories[2]):.3f} kcal', bg="#2C302C", fg="#FFFFFF")
        self.dinner_calories.place(x=131, y=453, width=94, height=42)

        self.dinner_calories_perc = Label(self.canvas,
                                          text=f'{(self.kilocalories[2]) / self.total_num_calories * 100:.2f} %',
                                          bg="#2C302C", fg="#FFFFFF")
        self.dinner_calories_perc.place(x=262, y=453, width=182, height=42)

        # Поле с потерянным весом
        activity_coef = {"Very low": 1.2, "Low": 1.375, "Medium": 1.55, "High": 1.725, "Very high": 1.9}

        sex = self.user_info[0]
        activity = activity_coef[self.user_info[1]]
        weight = float(self.user_info[2])
        height = float(self.user_info[3])
        age = self.user_info[4]

        BMR = 655.1 + (9.563 * weight) + (1.850 * height) - (4.676 * age) if sex == 'female' \
            else 66.47 + (13.75 * weight) + (5.003 * height) - (6.755 * age)

        AMR = BMR * activity
        self.difference = self.total_num_calories - AMR

        text = "Weight loss:" if self.difference < 0 else "Weight increase:"

        self.canvas.create_text(
            416.0,
            535.0,
            anchor="nw",
            text=text,
            fill="#000000",
            font=("Inter", 20 * -1)
        )
        self.weight = Label(self.canvas, text=f'{abs(self.difference / 7700):.3f} kg', bg="#2C302C", fg="#FFFFFF")
        self.weight.place(x=564, y=529, width=94, height=42)

    def macros_page(self):
        self.canvas.destroy()
        self.create_widgets()

        # Поле со средним кол-вом БЖУ за сутки
        self.canvas.create_text(
            35.0,
            166.0,
            anchor="nw",
            text="AVG PFC for the meal:",
            fill="#000000",
            font=("Inter", 20 * -1)
        )
        self.avg_pfc_1 = Label(self.canvas, text=f'{(self.total_num_proteins / 3):.3f} proteins', bg="#2C302C",
                               fg="#FFFFFF")
        self.avg_pfc_1.place(x=260, y=159, width=118, height=42)

        self.avg_pfc_2 = Label(self.canvas, text=f'{(self.total_num_fats / 3):.3f} fats', bg="#2C302C", fg="#FFFFFF")
        self.avg_pfc_2.place(x=390, y=159, width=118, height=42)

        self.avg_pfc_3 = Label(self.canvas, text=f'{(self.total_num_carbohydrates / 3):.3f} carbohydrates',
                               bg="#2C302C",
                               fg="#FFFFFF")
        self.avg_pfc_3.place(x=518, y=159, width=123, height=42)

        # Поле с кол-вом БЖУ за завтрак
        self.canvas.create_text(
            35.0,
            259.0,
            anchor="nw",
            text="Breakfast:",
            fill="#000000",
            font=("Inter", 20 * -1)
        )
        self.break_proteins = Label(self.canvas, text=f'{(self.proteins[0]):.3f} proteins', bg="#2C302C", fg="#FFFFFF")
        self.break_proteins.place(x=165, y=252, width=94, height=42)

        self.break_fats = Label(self.canvas, text=f'{(self.fats[0]):.3f} fats', bg="#2C302C",
                                fg="#FFFFFF")
        self.break_fats.place(x=270, y=252, width=94, height=42)

        self.break_carbo = Label(self.canvas, text=f'{(self.carbohydrates[0]):.3f} carbohydrates', bg="#2C302C",
                                 fg="#FFFFFF")
        self.break_carbo.place(x=375, y=252, width=182, height=42)

        # Поле с кол-вом БЖУ за обэд
        self.canvas.create_text(
            35.0,
            359.0,
            anchor="nw",
            text="Lunch:",
            fill="#000000",
            font=("Inter", 20 * -1)
        )
        self.break_proteins = Label(self.canvas, text=f'{(self.proteins[1]):.3f} proteins', bg="#2C302C", fg="#FFFFFF")
        self.break_proteins.place(x=165, y=352, width=94, height=42)

        self.break_fats = Label(self.canvas, text=f'{(self.fats[1]):.3f} fats', bg="#2C302C",
                                fg="#FFFFFF")
        self.break_fats.place(x=270, y=352, width=94, height=42)

        self.break_carbo = Label(self.canvas, text=f'{(self.carbohydrates[1]):.3f} carbohydrates', bg="#2C302C",
                                 fg="#FFFFFF")
        self.break_carbo.place(x=375, y=352, width=182, height=42)

        # Поле с кол-вом БЖУ за ужин
        self.canvas.create_text(
            35.0,
            459.0,
            anchor="nw",
            text="Dinner:",
            fill="#000000",
            font=("Inter", 20 * -1)
        )
        self.break_proteins = Label(self.canvas, text=f'{(self.proteins[2]):.3f} proteins', bg="#2C302C", fg="#FFFFFF")
        self.break_proteins.place(x=165, y=452, width=94, height=42)

        self.break_fats = Label(self.canvas, text=f'{(self.fats[2]):.3f} fats', bg="#2C302C",
                                fg="#FFFFFF")
        self.break_fats.place(x=270, y=452, width=94, height=42)

        self.break_carbo = Label(self.canvas, text=f'{(self.carbohydrates[2]):.3f} carbohydrates', bg="#2C302C",
                                 fg="#FFFFFF")
        self.break_carbo.place(x=375, y=452, width=182, height=42)


class AccountWindow:
    def __init__(self, account_id):
        self.window = Tk()
        self.window.geometry("700x600")
        self.window.configure(bg="#D8D5D5")

        self.window.resizable(False, False)

        self.db = DataBase()
        self.account_id = account_id
        self.user_id = self.db.find_user_id(account_id)

        self.create_widgets()

    def create_widgets(self):
        self.canvas = Canvas(
            self.window,
            bg="#D8D5D5",
            height=600,
            width=700,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        self.draw_logo()
        self.draw_background()
        self.draw_buttons()
        self.draw_info()

    def draw_background(self):
        self.canvas.create_rectangle(0.0, 87.0, 700.0, 90.0, fill="#000000", outline="")

    def draw_info(self):
        self.account_info = self.db.get_account_info(self.account_id)

        # Поле логин
        self.canvas.create_text(
            251.0,
            118.0,
            anchor="nw",
            text="Username:",
            fill="#000000",
            font=("Inter", 20 * -1)
        )
        name_info = Label(self.canvas, text=f'{self.account_info[0]}', bg="#2C302C", fg="#FFFFFF")
        name_info.place(x=354, y=116, width=260, height=30)

        # Поле возраст
        self.canvas.create_text(
            251.0,
            166.0,
            anchor="nw",
            text="Age:",
            fill="#000000",
            font=("Inter", 20 * -1)
        )
        age_info = Label(self.canvas, text=f'{self.account_info[5]}', bg="#2C302C", fg="#FFFFFF")
        age_info.place(x=302, y=166, width=51, height=25)

        # Поле пол
        self.canvas.create_text(
            379.0,
            166.0,
            anchor="nw",
            text="Sex:",
            fill="#000000",
            font=("Inter", 20 * -1)
        )
        sex_info = Label(self.canvas, text=f'{self.account_info[1]}', bg="#2C302C", fg="#FFFFFF")
        sex_info.place(x=428, y=166, width=51, height=25)

        # Поле активность
        self.canvas.create_text(
            490.0,
            166.0,
            anchor="nw",
            text="Activity:",
            fill="#000000",
            font=("Inter", 20 * -1)
        )
        activity_info = Label(self.canvas, text=f'{self.account_info[2]}', bg="#2C302C", fg="#FFFFFF")
        activity_info.place(x=565, y=166, width=51, height=25)

        # Поле вес
        self.canvas.create_text(
            251.0,
            199.0,
            anchor="nw",
            text="Weight (kg):",
            fill="#000000",
            font=("Inter", 20 * -1)
        )
        weight_info = Label(self.canvas, text=f'{self.account_info[3]}', bg="#2C302C", fg="#FFFFFF")
        weight_info.place(x=373, y=199, width=51, height=25)

        # Поле рост
        self.canvas.create_text(
            251.0,
            232.0,
            anchor="nw",
            text="Height (cm):",
            fill="#000000",
            font=("Inter", 20 * -1)
        )
        height_info = Label(self.canvas, text=f'{self.account_info[4]}', bg="#2C302C", fg="#FFFFFF")
        height_info.place(x=373, y=233, width=51, height=25)

        # Поле goal
        self.canvas.create_text(
            251.0,
            269.0,
            anchor="nw",
            text="Goal:",
            fill="#000000",
            font=("Inter", 20 * -1)
        )
        goal_info = Text(self.canvas, bg="#2C302C", fg="#FFFFFF")
        goal_info.place(x=305, y=270, width=350, height=50)
        goal_info.insert(tkinter.END, f'{self.account_info[6]}')
        goal_info.configure(state=tkinter.DISABLED)

    def draw_buttons(self):
        # Кнопка аккаунт
        self.acc_button_image = PhotoImage(file=ASSETS_PATH / "Me_button.png")
        self.acc_button = Button(
            image=self.acc_button_image, command=lambda: [self.window.destroy(), AccountWindow(self.account_id)])
        self.acc_button.place(x=564, y=5, width=70, height=70)

        # Кнопка статистика
        self.stat_button_image = PhotoImage(file=ASSETS_PATH / "Reports_button.png")
        self.stat_button = Button(
            image=self.stat_button_image, command=lambda: [self.window.destroy(), ReportWindow(self.account_id)])
        self.stat_button.place(x=394, y=5, width=70, height=70)

        # Кнопка избранное
        self.favour_button_image = PhotoImage(file=ASSETS_PATH / "Favourites_button.png")
        self.favour_button = Button(
            image=self.favour_button_image, command=lambda: [self.window.destroy(), FavouritesWindow(self.account_id)])
        self.favour_button.place(x=224, y=5, width=70, height=70)

        # Кнопка дневник
        self.diary_button_image = PhotoImage(file=ASSETS_PATH / "Diary_button.png")
        self.diary_button = Button(
            image=self.diary_button_image, command=lambda: [self.window.destroy(), DiaryWindow(self.account_id)])
        self.diary_button.place(x=54, y=5, width=70, height=70)

        # Кнопка замены данных аккаунта
        self.change_acc_button_image = PhotoImage(file=ASSETS_PATH / "change_acc_button.png")
        self.change_acc_button = Button(
            image=self.change_acc_button_image,
            command=lambda: [self.window.destroy(), ChangeInfo(self.account_info, self.account_id)])
        self.change_acc_button.place(x=370, y=340, width=187, height=49)

        # Кнопка выйти с аккаунта
        self.logout_button_image = PhotoImage(file=ASSETS_PATH / "logout_button.png")
        self.logout_button = Button(
            image=self.logout_button_image,
            command=lambda: [self.db.close_connection(), self.window.destroy(), AuthorizationWindow()])
        self.logout_button.place(x=452, y=523, width=187, height=49)

        # Кнопка удалить аккаунт
        self.del_acc_button_image = PhotoImage(file=ASSETS_PATH / "del_acc_button.png")
        self.del_acc_button = Button(image=self.del_acc_button_image,
                                     command=lambda: self.delete_account_wind())
        self.del_acc_button.place(x=16, y=523, width=173, height=49)

        # Кнопка удалить базу данных
        self.del_DB_button_image = PhotoImage(file=ASSETS_PATH / "del_DB_button.png")
        self.del_DB_button = Button(image=self.del_DB_button_image,
                                    command=lambda: [self.drop_db(), self.window.destroy()])
        self.del_DB_button.place(x=227, y=523, width=187, height=49)

    def draw_logo(self):
        self.acc_photo = PhotoImage(file=ASSETS_PATH / "acc_image.png")
        self.canvas.create_image(115, 210, image=self.acc_photo)

    def delete_account_wind(self):
        self.new_window = tkinter.Toplevel()
        self.new_window.geometry("300x300")
        self.new_window.configure(bg="#D8D5D5")

        self.new_window.resizable(False, False)

        self.new_window.grab_set()

        self.new_canvas = Canvas(
            self.new_window,
            bg="#D8D5D5",
            height=300,
            width=300,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.new_canvas.place(x=0, y=0)

        self.del_image = PhotoImage(file=ASSETS_PATH / "del_acc_image.png")
        self.new_canvas.create_image(150, 110, image=self.del_image)

        self.conf_button_image = PhotoImage(file=ASSETS_PATH / "del_acc_conf.png")
        self.conf_button = Button(self.new_window,
                                  image=self.conf_button_image,
                                  command=lambda: self.delete_user())
        self.conf_button.place(x=56, y=229, width=187, height=49)

    def delete_user(self):
        self.db.delete_account(self.account_id)

        self.new_window.destroy()
        self.window.destroy()

    def drop_db(self):
        self.db.delete_database()


class ChangeInfo:
    def __init__(self, user_info, account_id):
        self.window = Tk()
        self.window.geometry("300x500")
        self.window.configure(bg="#D8D5D5")

        self.window.resizable(False, False)

        self.db = DataBase()
        self.account_id = account_id
        self.user_id = self.db.find_user_id(account_id)
        self.user_info = user_info

        self.create_widgets()

    def create_widgets(self):
        self.canvas = Canvas(
            self.window,
            bg="#D8D5D5",
            height=600,
            width=700,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        self.draw_buttons()
        self.draw_input()

    def draw_buttons(self):
        self.confirm_button_image = PhotoImage(file=ASSETS_PATH / "confirm_button.png")
        self.confirm_button = Button(
            image=self.confirm_button_image, command=lambda: self.update_info())
        self.confirm_button.place(x=56, y=423, width=187, height=49)

    def draw_input(self):
        self.canvas.create_text(
            30.0,
            17.0,
            anchor="nw",
            text="Username:",
            fill="#000000",
            font=("Inter", 20 * -1)
        )
        self.name_info = Entry(self.canvas, bg="#2C302C", fg="#FFFFFF")
        self.name_info.insert(0, f'{self.user_info[0]}')
        self.name_info.place(x=138, y=15, width=145, height=31)

        # Поле возраст
        self.canvas.create_text(
            30.0,
            74.0,
            anchor="nw",
            text="Age:",
            fill="#000000",
            font=("Inter", 20 * -1)
        )
        self.age_info = Entry(self.canvas, bg="#2C302C", fg="#FFFFFF")
        self.age_info.insert(0, f'{self.user_info[5]}')
        self.age_info.place(x=78, y=74, width=47, height=28)

        # Поле пол
        self.canvas.create_text(
            145.0,
            74.0,
            anchor="nw",
            text="Sex:",
            fill="#000000",
            font=("Inter", 20 * -1)
        )

        self.gender_var = tkinter.StringVar(self.canvas)
        self.gender_var.set(f'{self.user_info[1]}')
        self.gender_menu = tkinter.OptionMenu(self.canvas, self.gender_var, *["Male", "Female"])

        self.gender_menu.config(bg="#2C302C", fg="#FFFFFF")
        self.gender_menu.place(x=200, y=74, width=70, height=28)

        # Поле активность
        self.canvas.create_text(
            30.0,
            114.0,
            anchor="nw",
            text="Activity:",
            fill="#000000",
            font=("Inter", 20 * -1)
        )

        self.activity_var = tkinter.StringVar(self.canvas)
        self.activity_var.set(f'{self.user_info[2]}')
        self.activity_menu = tkinter.OptionMenu(self.canvas, self.activity_var,
                                                *["Very low", "Low", "Medium", "High", "Very high"])

        self.activity_menu.config(bg="#2C302C", fg="#FFFFFF")
        self.activity_menu.place(x=150, y=114, width=125, height=28)

        # Поле вес
        self.canvas.create_text(
            30.0,
            154.0,
            anchor="nw",
            text="Weight (kg):",
            fill="#000000",
            font=("Inter", 20 * -1)
        )
        self.weight_info = Entry(self.canvas, bg="#2C302C", fg="#FFFFFF")
        self.weight_info.insert(0, f'{self.user_info[3]}')
        self.weight_info.place(x=150, y=154, width=125, height=28)

        # Поле рост
        self.canvas.create_text(
            30.0,
            194.0,
            anchor="nw",
            text="Height (cm):",
            fill="#000000",
            font=("Inter", 20 * -1)
        )
        self.height_info = Entry(self.canvas, bg="#2C302C", fg="#FFFFFF")
        self.height_info.insert(0, f'{self.user_info[4]}')
        self.height_info.place(x=150, y=194, width=125, height=28)

        # Поле goal
        self.canvas.create_text(
            125.0,
            234.0,
            anchor="nw",
            text="Goal:",
            fill="#000000",
            font=("Inter", 20 * -1)
        )
        self.goal_info = Text(self.canvas, bg="#2C302C", fg="#FFFFFF")
        self.goal_info.place(x=35, y=274, width=230, height=118)
        self.goal_info.insert(tkinter.END, f'{self.user_info[6]}')
        self.goal_info.configure(state="normal")

    def update_info(self):
        if len(self.name_info.get().split()) != 1 and len(self.age_info.get().split()) != 1 and len(
                self.weight_info.get().split()) != 1 and len(self.height_info.get().split()) != 1:
            mb.showerror("Error", "Fields cannot contain spaces")

        else:
            self.db.update_username(self.name_info.get(), self.account_id)

            self.db.update_user_info(self.age_info.get(), self.gender_var.get(),
                                     self.weight_info.get(), self.height_info.get(),
                                     self.goal_info.get("1.0", "end-1c"), self.account_id)
            self.window.destroy()
            AccountWindow(self.account_id)


window = AuthorizationWindow()
window.run()
