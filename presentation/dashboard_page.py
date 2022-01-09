from tkinter import *
from presentation.admin_login_page import AdminLoginPage
from presentation.customer_login_page import CustomerLoginPage


class DashboardPage:
    def __init__(self):
        self.__tk = Tk()

    def __nav_to_customer_login(self):
        self.__tk.destroy()
        CustomerLoginPage().draw_login()

    def __nav_to_admin_login(self):
        self.__tk.destroy()
        AdminLoginPage().draw_login()

    def draw_dashboard(self):
        self.__tk.geometry('400x150')
        self.__tk.title('Dashboard')

        Button(self.__tk,
               text="Admin",
               command=self.__nav_to_admin_login,
               bg='blue',
               fg='white'
               ).place(relx=0.5, rely=0.6, anchor=CENTER)

        Button(self.__tk,
               text="User",
               command=self.__nav_to_customer_login,
               ).place(relx=0.5, rely=0.4, anchor=CENTER)

        self.__tk.mainloop()
