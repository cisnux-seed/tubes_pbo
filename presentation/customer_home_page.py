from functools import partial
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from data.db.database_helper import DatabaseHelper
from data.models.food_model import FoodModel
from data.models.order_model import OrderModel
from utils.generate_uuid import generate_uuid


class CustomerHomePage:
    def __init__(self, user_id):
        self.__tk = Tk()
        self.user_id = user_id

    def __nav_to_bill_menu(self):
        self.__tk.destroy()
        BillMenu(self.user_id).draw_bill_menu()

    def __nav_to_food_menu(self):
        self.__tk.destroy()
        FoodMenu(self.user_id).draw_menu()

    def draw_home_page(self):
        self.__tk.geometry('400x150')
        self.__tk.title('Home Page')

        Button(self.__tk,
               text="Pilih Menu",
               command=self.__nav_to_food_menu,
               bg='blue',
               fg='white'
               ).place(relx=0.5, rely=0.6, anchor=CENTER)

        Button(self.__tk,
               text="Bayar Pesanan",
               command=self.__nav_to_bill_menu,
               ).place(relx=0.5, rely=0.4, anchor=CENTER)

        self.__tk.mainloop()


class FoodMenu:
    def __init__(self, user_id):
        self.__food_index = None
        self.user_id = user_id
        self.__db_helper = DatabaseHelper().get_instance()
        self.__foods = self.__db_helper.fetch_foods()
        self.__tk = Tk()
        self.__table_frame = Frame(self.__tk)
        self.__table_frame.pack()
        self.__table_scrolly = Scrollbar(self.__table_frame)
        self.__table_scrolly.pack(side=RIGHT, fill=Y)
        self.__table = ttk.Treeview(
            self.__table_frame, yscrollcommand=self.__table_scrolly.set)
        self.__table_frame.pack()
        self.__table_scrolly.config(command=self.__table.yview)
        self.__table.bind("<<TreeviewSelect>>", self.__on_tree_select)

    def draw_menu(self):
        self.__tk.title('Foods')
        self.__tk.geometry('1270x720')

        self.__draw_table(self.__foods)
        Label(
            self.__tk, text="Jumlah", justify=LEFT).place(
            relx=0.35, rely=0.35, anchor=CENTER)
        quantity = IntVar()
        Entry(self.__tk, textvariable=quantity).place(
            relx=0.5, rely=0.35, anchor=CENTER)
        add_to_cart = partial(self.__add_to_cart, quantity)
        Button(self.__tk, text="Add to Cart",  fg="white", bg="blue",
               command=add_to_cart).place(relx=0.5, rely=0.4, anchor=CENTER)
        Button(self.__tk, text="Back",  fg="white", bg="black",
               command=self.__back).place(relx=0.5, rely=0.45, anchor=CENTER)
        self.__tk.mainloop()

    def __draw_table(self, foods):
        self.__table['columns'] = ('no', 'food_name',
                                   'food_quantity', 'food_price', 'stock')

        self.__table.column("#0", width=0,  stretch=NO)
        self.__table.column("no", anchor=CENTER, width=120)
        self.__table.column("food_name", anchor=CENTER, width=120)
        self.__table.column("food_quantity", anchor=CENTER, width=120)
        self.__table.column("food_price", anchor=CENTER, width=120)
        self.__table.column("stock", anchor=CENTER, width=120)

        self.__table.heading("#0", text="", anchor=CENTER)
        self.__table.heading("no", text="No", anchor=CENTER)
        self.__table.heading("food_name", text="Name", anchor=CENTER)
        self.__table.heading("food_quantity", text="Quantity", anchor=CENTER)
        self.__table.heading("food_price", text="Price", anchor=CENTER)
        self.__table.heading("stock", text="Stock", anchor=CENTER)

        no = 1
        for food in foods:
            self.__table.insert(parent='', index='end',
                                values=(
                                    no,
                                    food.name,
                                    food.food_quantity,
                                    food.price,
                                    "Available" if food.food_quantity > 0 else "Not Available"
                                )
                                )

            no += 1
        self.__table.pack()

    def __on_tree_select(self, event):
        for item in self.__table.selection():
            item_value = self.__table.item(item, "values")
        # should be convert to int because item_value return a string
        self.__food_index = int(item_value[0])-1

    def __add_to_cart(self, quantity_order):
        if self.__food_index is not None:
            if quantity_order.get() < self.__foods[self.__food_index].food_quantity and quantity_order.get() != 0 and self.__foods[self.__food_index].food_quantity != 0:
                order = OrderModel(generate_uuid(), self.user_id,
                                   self.__foods[self.__food_index].id, quantity_order.get(), int(False), None)
                self.__foods[self.__food_index].food_quantity -= quantity_order.get()
                self.__db_helper.order_food(
                    order, self.__foods[self.__food_index])
                self.__tk.destroy()
                FoodMenu(self.user_id).draw_menu()

    def __back(self):
        self.__tk.destroy()
        CustomerHomePage(self.user_id).draw_home_page()


class BillMenu:
    def __init__(self, user_id):
        self.user_id = user_id
        self.__order_index = None
        self.__db_helper = DatabaseHelper().get_instance()
        self.__orders = self.__db_helper.fetch_order_datail(self.user_id)
        self.__total_bill = self.__db_helper.fetch_total_bill(self.user_id)
        self.__tk = Tk()
        self.__table_frame = Frame(self.__tk)
        self.__table_frame.pack()
        self.__table_scrolly = Scrollbar(self.__table_frame)
        self.__table_scrolly.pack(side=RIGHT, fill=Y)
        self.__table = ttk.Treeview(
            self.__table_frame, yscrollcommand=self.__table_scrolly.set)
        self.__table_frame.pack()
        self.__table_scrolly.config(command=self.__table.yview)
        self.__table.bind("<<TreeviewSelect>>", self.__on_tree_select)

    def draw_bill_menu(self):
        self.__tk.title('Foods')
        self.__tk.geometry('1270x720')

        self.__draw_table(self.__orders)

        Label(
            self.__tk, text="Total Tagihan :", justify=LEFT).place(
            relx=0.35, rely=0.4, anchor=CENTER)
        Label(
            self.__tk, text=f"Rp. {self.__total_bill if self.__total_bill != None else 0},-", justify=LEFT).place(
            relx=0.42, rely=0.4, anchor=CENTER)

        Label(
            self.__tk, text="Masukkan Uang :", justify=LEFT).place(
            relx=0.35, rely=0.43, anchor=CENTER)
        user_money = IntVar()
        Entry(self.__tk, textvariable=user_money).place(
            relx=0.45, rely=0.43, anchor=CENTER)
        pay = partial(self.__pay_bills, user_money)

        Button(self.__tk, text="Delete",  fg="white", bg="blue",
               command=self.__delete).place(relx=0.417, rely=0.48, anchor=CENTER)
        Button(self.__tk, text="Pay",  fg="white", bg="blue",
               command=pay).place(relx=0.45, rely=0.48, anchor=CENTER)
        Button(self.__tk, text="Back",  fg="white", bg="black",
               command=self.__back).place(relx=0.48, rely=0.48, anchor=CENTER)
        self.__tk.mainloop()

    def __draw_table(self, orders):
        self.__table['columns'] = (
            'no',
            'food_name',
            'food_price',
            'order_quantity'
        )

        self.__table.column("#0", width=0,  stretch=NO)
        self.__table.column("no", anchor=CENTER, width=120)
        self.__table.column("food_name", anchor=CENTER, width=120)
        self.__table.column("food_price", anchor=CENTER, width=120)
        self.__table.column("order_quantity", anchor=CENTER, width=120)

        self.__table.heading("#0", text="", anchor=CENTER)
        self.__table.heading("no", text="No", anchor=CENTER)
        self.__table.heading("food_name", text="Food Name", anchor=CENTER)
        self.__table.heading("food_price", text="Price", anchor=CENTER)
        self.__table.heading(
            "order_quantity", text="Order Quantity", anchor=CENTER)

        no = 1
        for order in orders:
            self.__table.insert(parent='', index='end',
                                values=(
                                    no,
                                    order.food.name,
                                    order.food.price,
                                    order.order_quantity
                                )
                                )
            no += 1
        self.__table.pack()

    def __on_tree_select(self, event):
        for item in self.__table.selection():
            item_value = self.__table.item(item, "values")
        # should be convert to int because item_value return a string
        self.__order_index = int(item_value[0])-1

    def __pay_bills(self, user_money):
        if self.__total_bill != None:
            result = self.__db_helper.pay_bills(
                self.__total_bill, user_money.get())

            if type(result) == int:
                self.__db_helper.update_order(self.user_id)
                messagebox.showinfo(title="Pay Bills",
                                    message=f"Your money changes: Rp. {result},-")
                self.__tk.destroy()
                BillMenu(self.user_id).draw_bill_menu()
            else:
                messagebox.showwarning(title="Pay Bills", message=result)

    def __back(self):
        self.__tk.destroy()
        CustomerHomePage(self.user_id).draw_home_page()

    def __delete(self):
        if self.__order_index != None:
            self.__orders[self.__order_index].food.food_quantity += self.__orders[self.__order_index].order_quantity
            self.__db_helper.remove_order(self.__orders[self.__order_index])
            self.__tk.destroy()
            BillMenu(self.user_id).draw_bill_menu()
