from tkinter import *
from functools import partial
from tkinter import messagebox
from data.db.database_helper import DatabaseHelper
from data.models.user_model import UserModel
from domain.auth import Auth
from presentation.admin_home_page import AdminHomePage


class AdminLoginPage:
    def __init__(self):
        self.__tk = Tk()

    def __validate(self, email, password):
        db_helper = DatabaseHelper().get_instance()
        auth = Auth(db_helper)
        result = auth.admin_sign_in(
            UserModel(None, email.get(), password.get(), True))

        if type(result) is str:
            messagebox.showerror('Login Error', result)
        else:
            self.__tk.destroy()
            AdminHomePage().draw_home_page()

    def draw_login(self):
        self.__tk.geometry('400x150')
        self.__tk.title('Login Form')

        Label(
            self.__tk, text="Email", justify=LEFT).grid(row=0, column=0)
        email = StringVar()
        Entry(
            self.__tk, textvariable=email, width=23).grid(row=0, column=1)

        Label(
            self.__tk, text="Password").grid(row=1, column=0)
        password = StringVar()
        Entry(self.__tk, textvariable=password, width=23,
              show='*').grid(row=1, column=1)

        validateLogin = partial(self.__validate, email, password)

        Button(self.__tk, text="Sign in",
               command=validateLogin).grid(row=4, column=0)

        self.__tk.mainloop()
