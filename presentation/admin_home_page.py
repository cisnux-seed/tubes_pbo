from functools import partial
from data.models.food_model import FoodModel
from data.db.database_helper import DatabaseHelper
from tkinter import *
from tkinter import ttk
from utils.generate_uuid import generate_uuid


class AdminHomePage:
    def __init__(self):
        self.__current_id = ''
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

    def draw_home_page(self):
        self.__tk.title('Home Page')
        self.__tk.geometry('1270x720')

        self.__draw_table(self.__foods)
        Button(self.__tk, text="Add Food", fg="white", bg="blue",
               command=self.__nav_to_add_food).place(relx=0.4, rely=0.35, anchor=CENTER)
        Button(self.__tk, text="Update Food",  fg="white", bg="blue",
               command=self.__nav_to_update_food).place(relx=0.5, rely=0.35, anchor=CENTER)
        Button(self.__tk, text="Delete",  fg="white", bg="blue",
               command=self.__delete_food).place(relx=0.6, rely=0.35, anchor=CENTER)
        self.__tk.mainloop()

    def __draw_table(self, foods):
        self.__table['columns'] = ('no', 'food_id', 'food_name',
                                   'food_quantity', 'food_price')

        self.__table.column("#0", width=0,  stretch=NO)
        self.__table.column("no", anchor=CENTER, width=120)
        self.__table.column("food_id", anchor=CENTER, width=120)
        self.__table.column("food_name", anchor=CENTER, width=120)
        self.__table.column("food_quantity", anchor=CENTER, width=120)
        self.__table.column("food_price", anchor=CENTER, width=120)

        self.__table.heading("#0", text="", anchor=CENTER)
        self.__table.heading("no", text="No", anchor=CENTER)
        self.__table.heading("food_id", text="Id", anchor=CENTER)
        self.__table.heading("food_name", text="Name", anchor=CENTER)
        self.__table.heading("food_quantity", text="Quantity", anchor=CENTER)
        self.__table.heading("food_price", text="Price", anchor=CENTER)

        index = 0
        for food in foods:
            self.__table.insert(parent='', index='end', iid=index, text='',
                                values=(
                                    index+1,
                                    food.id,
                                    food.name,
                                    food.food_quantity,
                                    food.price
                                )
                                )

            index += 1
        self.__table.pack()

    def __on_tree_select(self, event):
        for item in self.__table.selection():
            item_value = self.__table.item(item, "values")
        self.__current_id = item_value[1]

    def __nav_to_add_food(self):
        self.__tk.destroy()
        AddFoodPage().draw_add_food()

    def __nav_to_update_food(self):
        self.__tk.destroy()
        UpdateFoodPage(self.__current_id).draw_update_food()

    def __delete_food(self):
        self.__db_helper.remove_food(self.__current_id)
        self.__tk.destroy()
        AdminHomePage().draw_home_page()


class AddFoodPage:
    def __init__(self):
        self.__tk = Tk()
        self.__db_helper = DatabaseHelper().get_instance()

    def __add_food(self, name, quantity, price):
        self.__db_helper.add_food(
            FoodModel(generate_uuid(), name.get(), quantity.get(), price.get()))
        self.__tk.destroy()
        AdminHomePage().draw_home_page()

    def draw_add_food(self):
        self.__tk.geometry('400x150')
        self.__tk.title('Foods')

        Label(
            self.__tk, text="Name", justify=LEFT).grid(row=0, column=0)
        name = StringVar()
        Entry(self.__tk, textvariable=name).grid(row=0, column=1)

        Label(self.__tk, text="Quantity").grid(row=1, column=0)
        quantity = IntVar()
        Entry(self.__tk, textvariable=quantity).grid(row=1, column=1)

        Label(self.__tk, text="Price").grid(row=2, column=0)
        price = IntVar()
        Entry(self.__tk, textvariable=price).grid(row=2, column=1)

        add_food = partial(self.__add_food, name, quantity, price)

        Button(self.__tk, text="Add Food",
               command=add_food).grid(row=4, column=1)

        self.__tk.mainloop()


class UpdateFoodPage:
    def __init__(self, id: str):
        self.__tk = Tk()
        self.id = id
        self.__db_helper = DatabaseHelper().get_instance()
        self.__food = self.__db_helper.fetch_food_by_id(self.id)

    def __update_food(self, name, quantity, price):
        self.__db_helper.update_food(
            FoodModel(self.__food.id, name.get(), quantity.get(), price.get()))
        self.__tk.destroy()
        AdminHomePage().draw_home_page()

    def draw_update_food(self):
        self.__tk.geometry('400x150')
        self.__tk.title('Foods')

        if self.__food is not None:
            Label(
                self.__tk, text="Name", justify=LEFT).grid(row=0, column=0)
            name = StringVar(self.__tk, value=self.__food.name)
            Entry(self.__tk, textvariable=name).grid(row=0, column=1)

            Label(self.__tk, text="Quantity").grid(row=1, column=0)
            quantity = IntVar(self.__tk, value=self.__food.food_quantity)
            Entry(self.__tk, textvariable=quantity).grid(row=1, column=1)

            Label(self.__tk, text="Price").grid(row=2, column=0)
            price = IntVar(self.__tk, value=self.__food.price)
            Entry(self.__tk, textvariable=price).grid(row=2, column=1)

            update_food = partial(self.__update_food, name, quantity, price)

            Button(self.__tk, text="Update Food",
                   command=update_food).grid(row=4, column=1)
        else:
            Label(
                self.__tk, text="No data", justify=CENTER, bg='red', fg='white').place(relx=0.5, rely=0.5, anchor=CENTER)

        self.__tk.mainloop()
