from tkinter import *
from functools import partial
from tkinter import messagebox
from data.db.database_helper import DatabaseHelper
from data.models.user_model import UserModel
from domain.auth import Auth
from presentation.customer_home_page import CustomerHomePage
from utils.generate_uuid import *


class CustomerLoginPage:
    def __init__(self):
        self.__tk = Tk()
        self.__db_helper = DatabaseHelper().get_instance()
        self.__auth = Auth(self.__db_helper)

    def __validate(self, email, password):
        result = self.__auth.customer_sign_in(
            UserModel(None, email.get(), password.get(), False))

        if type(result) is str:
            messagebox.showerror('Login Error', result)
        else:
            self.__tk.destroy()
            CustomerHomePage(result.id).draw_home_page()

    def __nav_to_sign_in(self):
        self.__tk.destroy()
        CustomerRegisterPage().draw_register()

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
        Entry(self.__tk, textvariable=password,
              width=23, show='*').grid(row=1, column=1)

        validate_login = partial(self.__validate, email, password)

        Button(self.__tk, text="Sign in",
               command=validate_login).grid(row=4, column=0)

        Label(
            self.__tk, text="Don't have an account? ").grid(row=4, column=1)

        Button(self.__tk,
               text="Sign Up",
               command=self.__nav_to_sign_in,
               border=False,
               fg='blue'
               ).grid(row=4, column=2)

        self.__tk.mainloop()


class CustomerRegisterPage:
    def __init__(self):
        self.__tk = Tk()
        self.__db_helper = DatabaseHelper().get_instance()
        self.__auth = Auth(self.__db_helper)

    def __validate(self, email, password):
        result = self.__auth.customer_sign_up(
            UserModel(generate_uuid(), email.get(), password.get(), False))
        self.__tk.destroy()
        CustomerHomePage(result.id).draw_home_page()

    def __nav_to_sign_in(self):
        self.__tk.destroy()
        CustomerLoginPage().draw_login()

    def draw_register(self):
        self.__tk.geometry('400x150')
        self.__tk.title('Register Form')

        Label(
            self.__tk, text="Email", justify=LEFT).grid(row=0, column=0)
        email = StringVar()
        Entry(
            self.__tk, textvariable=email, width=23).grid(row=0, column=1)

        Label(
            self.__tk, text="Password").grid(row=1, column=0)
        password = StringVar()
        Entry(self.__tk, textvariable=password,
              show='*', width=23).grid(row=1, column=1)

        validate_register = partial(self.__validate, email, password)

        Button(self.__tk, text="Sign Up",
               command=validate_register).grid(row=4, column=0)

        Label(self.__tk, text="Have an account? ").grid(row=4, column=1)

        Button(self.__tk,
               text="Sign in",
               command=self.__nav_to_sign_in,
               border=False,
               fg='blue'
               ).grid(row=4, column=2)

        self.__tk.mainloop()
