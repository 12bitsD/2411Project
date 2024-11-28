import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import sqlite3
import pandas as pd

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.style = ttk.Style("litera")
        self.title('Banquet Management System')
        self.geometry('800x600')

        # Create menu bar
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)

        # Create banquet management menu
        banquet_menu = tk.Menu(menu_bar, tearoff=0)
        banquet_menu.add_command(label='Manage Banquets', command=self.open_banquet_manager)
        menu_bar.add_cascade(label='Banquet Management', menu=banquet_menu)

        # Create meal management menu
        meal_menu = tk.Menu(menu_bar, tearoff=0)
        meal_menu.add_command(label='Manage Meals', command=self.open_meal_manager)
        menu_bar.add_cascade(label='Meal Management', menu=meal_menu)

        # Create attendee management menu
        attendee_menu = tk.Menu(menu_bar, tearoff=0)
        attendee_menu.add_command(label='Manage Attendees', command=self.open_attendee_manager)
        menu_bar.add_cascade(label='Attendee Management', menu=attendee_menu)

        # Create registration management menu
        register_menu = tk.Menu(menu_bar, tearoff=0)
        register_menu.add_command(label='Manage Registrations', command=self.open_register_manager)
        menu_bar.add_cascade(label='Registration Management', menu=register_menu)

        report_menu = tk.Menu(menu_bar, tearoff=0)
        report_menu.add_command(label='Registration Status Report', command=self.generate_registration_report)
        report_menu.add_command(label='Popular Meals Report', command=self.generate_popular_meals_report)
        report_menu.add_command(label='Attendance Behavior Report', command=self.generate_attendance_behavior_report)
        menu_bar.add_cascade(label='Reports', menu=report_menu)

    def open_banquet_manager(self):
        BanquetManager(self)

    def open_meal_manager(self):
        MealManager(self)

    def open_attendee_manager(self):
        AttendeeManager(self)

    def open_register_manager(self):
        RegisterManager(self)

    def generate_registration_report(self):
        conn = sqlite3.connect('banquet.db')
        cursor = conn.cursor()
    
    # 查询数据
        cursor.execute("""
            SELECT Banquet.Name, COUNT(Registrations.RegistrationID) AS RegistrationCount
            FROM Banquet
            LEFT JOIN Registrations ON Banquet.BIN = Registrations.BIN
            GROUP BY Banquet.BIN;
            """)
        data = cursor.fetchall()
    
        columns = [desc[0] for desc in cursor.description]
        report_data = [dict(zip(columns, row)) for row in data]
        
        ReportWindow(self, report_data, 'Registration Status Report')
        
        conn.close()

    def generate_popular_meals_report(self):
        conn = sqlite3.connect('banquet.db')
        cursor = conn.cursor()
    
    # 查询数据
        cursor.execute("""
            SELECT Banquet.Name, Meal.DishName, Count
            FROM (
                SELECT Banquet.Name, Meal.DishName, COUNT(Registrations.RegistrationID) AS Count,
                       ROW_NUMBER() OVER (PARTITION BY Banquet.BIN ORDER BY COUNT(Registrations.RegistrationID) DESC) AS rn
                FROM Banquet
                JOIN Registrations ON Banquet.BIN = Registrations.BIN
                JOIN Meal ON Registrations.MealChoice = Meal.MealID
                GROUP BY Banquet.BIN, Meal.DishName
            ) sub
            WHERE sub.rn = 1;
        """)
        data = cursor.fetchall()
    
        columns = [desc[0] for desc in cursor.description]
        report_data = [dict(zip(columns, row)) for row in data]
    
        ReportWindow(self, report_data, 'Popular Meals Report')
    
        conn.close()

    def generate_attendance_behavior_report(self):
        conn = sqlite3.connect('banquet.db')
        cursor = conn.cursor()
    
    # 查询数据
        cursor.execute("""
            SELECT attendees_account.FirstName, attendees_account.LastName, COUNT(CASE WHEN Registrations.AttendanceStatus = 'Y' THEN 1 END) AS AttendanceCount
            FROM attendees_account
            LEFT JOIN Registrations ON attendees_account.AccountID = Registrations.AccountID
            GROUP BY attendees_account.AccountID;
        """)
        data = cursor.fetchall()
    
        columns = [desc[0] for desc in cursor.description]
        report_data = [dict(zip(columns, row)) for row in data]
    
        ReportWindow(self, report_data, 'Attendance Behavior Report')
       
        conn.close()

class BanquetManager(ttk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Banquet Manager')
        self.geometry('600x400')

        #  grid 
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        
        main_frame = ttk.Frame(self)
        main_frame.grid(row=0, column=0, sticky='nsew')

        # 在MainFrame中设置行和列的权重
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # 创建 Treeview 和垂直滚动条
        self.tree = ttk.Treeview(main_frame, columns=('BIN', 'Name', 'DateTime', 'Address', 'Location', 'ContactFirstName', 'ContactLastName', 'Available', 'Quota'), show='headings')
        self.tree.heading('BIN', text='BIN')
        self.tree.heading('Name', text='Name')
        self.tree.heading('DateTime', text='Date Time')
        self.tree.heading('Address', text='Address')
        self.tree.heading('Location', text='Location')
        self.tree.heading('ContactFirstName', text='Contact First Name')
        self.tree.heading('ContactLastName', text='Contact Last Name')
        self.tree.heading('Available', text='Available')
        self.tree.heading('Quota', text='Quota')
        self.tree.grid(row=0, column=0, sticky='nsew')

        vsb = ttk.Scrollbar(main_frame, orient="vertical", command=self.tree.yview)
        vsb.grid(row=0, column=1, sticky='ns')
        self.tree.configure(yscrollcommand=vsb.set)

        # 添加水平滚动条
        hsb = ttk.Scrollbar(main_frame, orient="horizontal", command=self.tree.xview)
        hsb.grid(row=1, column=0, sticky='ew')
        self.tree.configure(xscrollcommand=hsb.set)

        # 创建按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky='e')

        ttk.Button(button_frame, text='Add', command=self.add_banquet).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text='Edit', command=self.edit_banquet).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text='Delete', command=self.delete_banquet).pack(side=tk.LEFT, padx=5)

        # 加载数据
        self.load_data()

    def load_data(self):
        conn = sqlite3.connect('banquet.db')
        c = conn.cursor()
        c.execute('SELECT * FROM Banquet')
        rows = c.fetchall()
        conn.close()
        for row in rows:
            self.tree.insert('', tk.END, values=row)

    def add_banquet(self):
        AddBanquetWindow(self)

    def edit_banquet(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror('Error', 'Please select a banquet')
            return
        bin = self.tree.item(selected_item)['values'][0]
        EditBanquetWindow(self, bin)

    def delete_banquet(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror('Error', 'Please select a banquet')
            return
        bin = self.tree.item(selected_item)['values'][0]
        conn = sqlite3.connect('banquet.db')
        c = conn.cursor()
        c.execute('DELETE FROM Banquet WHERE BIN = ?', (bin,))
        conn.commit()
        conn.close()
        self.tree.delete(selected_item)

class AddBanquetWindow(ttk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Add Banquet')
        self.geometry('400x300')

        # Create labels and entry fields with grid
        ttk.Label(self, text='Name:').grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.name_entry = ttk.Entry(self)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self, text='Date Time:').grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.datetime_entry = ttk.Entry(self)
        self.datetime_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self, text='Address:').grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        self.address_entry = ttk.Entry(self)
        self.address_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self, text='Location:').grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
        self.location_entry = ttk.Entry(self)
        self.location_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(self, text='Contact First Name:').grid(row=4, column=0, padx=5, pady=5, sticky=tk.E)
        self.contact_firstname_entry = ttk.Entry(self)
        self.contact_firstname_entry.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(self, text='Contact Last Name:').grid(row=5, column=0, padx=5, pady=5, sticky=tk.E)
        self.contact_lastname_entry = ttk.Entry(self)
        self.contact_lastname_entry.grid(row=5, column=1, padx=5, pady=5)

        ttk.Label(self, text='Available:').grid(row=6, column=0, padx=5, pady=5, sticky=tk.E)
        self.available_entry = ttk.Entry(self)
        self.available_entry.grid(row=6, column=1, padx=5, pady=5)

        ttk.Label(self, text='Quota:').grid(row=7, column=0, padx=5, pady=5, sticky=tk.E)
        self.quota_entry = ttk.Entry(self)
        self.quota_entry.grid(row=7, column=1, padx=5, pady=5)

        # Create button
        ttk.Button(self, text='Add', command=self.add).grid(row=8, column=1, padx=5, pady=10)

    def add(self):
        name = self.name_entry.get()
        datetime = self.datetime_entry.get()
        address = self.address_entry.get()
        location = self.location_entry.get()
        contact_firstname = self.contact_firstname_entry.get()
        contact_lastname = self.contact_lastname_entry.get()
        available = self.available_entry.get()
        quota = self.quota_entry.get()

        if not name or not datetime or not address or not location or not contact_firstname or not contact_lastname or not available or not quota:
            messagebox.showerror('Error', 'Invalid input')
            return

        conn = sqlite3.connect('banquet.db')
        c = conn.cursor()
        c.execute('INSERT INTO Banquet (Name, DateTime, Address, Location, ContactFirstName, ContactLastName, Available, Quota) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                  (name, datetime, address, location, contact_firstname, contact_lastname, available, quota))
        conn.commit()
        conn.close()

        self.destroy()
        self.master.load_data()

class EditBanquetWindow(ttk.Toplevel):
    def __init__(self, parent, bin):
        super().__init__(parent)
        self.title('Edit Banquet')
        self.geometry('400x300')
        self.bin = bin

        # Query banquet information
        conn = sqlite3.connect('banquet.db')
        c = conn.cursor()
        c.execute('SELECT * FROM Banquet WHERE BIN = ?', (bin,))
        row = c.fetchone()
        conn.close()

        # Create labels and entry fields with grid
        ttk.Label(self, text='Name:').grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.name_entry = ttk.Entry(self)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        self.name_entry.insert(0, row[1])

        ttk.Label(self, text='Date Time:').grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.datetime_entry = ttk.Entry(self)
        self.datetime_entry.grid(row=1, column=1, padx=5, pady=5)
        self.datetime_entry.insert(0, row[2])

        ttk.Label(self, text='Address:').grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        self.address_entry = ttk.Entry(self)
        self.address_entry.grid(row=2, column=1, padx=5, pady=5)
        self.address_entry.insert(0, row[3])

        ttk.Label(self, text='Location:').grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
        self.location_entry = ttk.Entry(self)
        self.location_entry.grid(row=3, column=1, padx=5, pady=5)
        self.location_entry.insert(0, row[4])

        ttk.Label(self, text='Contact First Name:').grid(row=4, column=0, padx=5, pady=5, sticky=tk.E)
        self.contact_firstname_entry = ttk.Entry(self)
        self.contact_firstname_entry.grid(row=4, column=1, padx=5, pady=5)
        self.contact_firstname_entry.insert(0, row[5])

        ttk.Label(self, text='Contact Last Name:').grid(row=5, column=0, padx=5, pady=5, sticky=tk.E)
        self.contact_lastname_entry = ttk.Entry(self)
        self.contact_lastname_entry.grid(row=5, column=1, padx=5, pady=5)
        self.contact_lastname_entry.insert(0, row[6])

        ttk.Label(self, text='Available:').grid(row=6, column=0, padx=5, pady=5, sticky=tk.E)
        self.available_entry = ttk.Entry(self)
        self.available_entry.grid(row=6, column=1, padx=5, pady=5)
        self.available_entry.insert(0, row[7])

        ttk.Label(self, text='Quota:').grid(row=7, column=0, padx=5, pady=5, sticky=tk.E)
        self.quota_entry = ttk.Entry(self)
        self.quota_entry.grid(row=7, column=1, padx=5, pady=5)
        self.quota_entry.insert(0, row[8])

        # Create button
        ttk.Button(self, text='Save', command=self.save).grid(row=8, column=1, padx=5, pady=10)

    def save(self):
        name = self.name_entry.get()
        datetime = self.datetime_entry.get()
        address = self.address_entry.get()
        location = self.location_entry.get()
        contact_firstname = self.contact_firstname_entry.get()
        contact_lastname = self.contact_lastname_entry.get()
        available = self.available_entry.get()
        quota = self.quota_entry.get()

        if not name or not datetime or not address or not location or not contact_firstname or not contact_lastname or not available or not quota:
            messagebox.showerror('Error', 'Invalid input')
            return

        conn = sqlite3.connect('banquet.db')
        c = conn.cursor()
        c.execute('UPDATE Banquet SET Name = ?, DateTime = ?, Address = ?, Location = ?, ContactFirstName = ?, ContactLastName = ?, Available = ?, Quota = ? WHERE BIN = ?',
                  (name, datetime, address, location, contact_firstname, contact_lastname, available, quota, self.bin))
        conn.commit()
        conn.close()

        self.destroy()
        self.master.load_data()

class MealManager(ttk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Meal Manager')
        self.geometry('600x400')

        # 使用 grid 布局
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # 创建主框架
        main_frame = ttk.Frame(self)
        main_frame.grid(row=0, column=0, sticky='nsew')

        # 在主框架中设置行和列的权重
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # 创建 Treeview 和垂直滚动条
        self.tree = ttk.Treeview(main_frame, columns=('MealID', 'BIN', 'Type', 'DishName', 'Price', 'SpecialCuisine'), show='headings')
        self.tree.heading('MealID', text='MealID')
        self.tree.heading('BIN', text='BIN')
        self.tree.heading('Type', text='Type')
        self.tree.heading('DishName', text='Dish Name')
        self.tree.heading('Price', text='Price')
        self.tree.heading('SpecialCuisine', text='Special Cuisine')
        self.tree.grid(row=0, column=0, sticky='nsew')

        vsb = ttk.Scrollbar(main_frame, orient="vertical", command=self.tree.yview)
        vsb.grid(row=0, column=1, sticky='ns')
        self.tree.configure(yscrollcommand=vsb.set)

        # 添加水平滚动条
        hsb = ttk.Scrollbar(main_frame, orient="horizontal", command=self.tree.xview)
        hsb.grid(row=1, column=0, sticky='ew')
        self.tree.configure(xscrollcommand=hsb.set)

        # 创建按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky='e')
        ttk.Button(button_frame, text='Add', command=self.add_meal).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text='Edit', command=self.edit_meal).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text='Delete', command=self.delete_meal).pack(side=tk.LEFT, padx=5)

        # 加载数据
        self.load_data()

    def load_data(self):
        conn = sqlite3.connect('banquet.db')
        c = conn.cursor()
        c.execute('SELECT * FROM Meal')
        rows = c.fetchall()
        conn.close()
        for row in rows:
            self.tree.insert('', tk.END, values=row)

    def add_meal(self):
        AddMealWindow(self)

    def edit_meal(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror('Error', 'Please select a meal')
            return
        mealid = self.tree.item(selected_item)['values'][0]
        EditMealWindow(self, mealid)

    def delete_meal(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror('Error', 'Please select a meal')
            return
        mealid = self.tree.item(selected_item)['values'][0]
        conn = sqlite3.connect('banquet.db')
        c = conn.cursor()
        c.execute('DELETE FROM Meal WHERE MealID = ?', (mealid,))
        conn.commit()
        conn.close()
        self.tree.delete(selected_item)

class AddMealWindow(ttk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Add Meal')
        self.geometry('400x300')

        # Query banquet data for BIN combobox
        conn = sqlite3.connect('banquet.db')
        c = conn.cursor()
        c.execute('SELECT BIN FROM Banquet')
        banquets = c.fetchall()
        conn.close()

        # Create labels and entry fields with grid
        ttk.Label(self, text='BIN:').grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.bin_combobox = ttk.Combobox(self, values=[banquet[0] for banquet in banquets])
        self.bin_combobox.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self, text='Type:').grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.type_entry = ttk.Entry(self)
        self.type_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self, text='Dish Name:').grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        self.dishname_entry = ttk.Entry(self)
        self.dishname_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self, text='Price:').grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
        self.price_entry = ttk.Entry(self)
        self.price_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(self, text='Special Cuisine:').grid(row=4, column=0, padx=5, pady=5, sticky=tk.E)
        self.specialcuisine_entry = ttk.Entry(self)
        self.specialcuisine_entry.grid(row=4, column=1, padx=5, pady=5)

        # Create button
        ttk.Button(self, text='Add', command=self.add).grid(row=5, column=1, padx=5, pady=10)

    def add(self):
        bin = self.bin_combobox.get()
        type = self.type_entry.get()
        dishname = self.dishname_entry.get()
        price = self.price_entry.get()
        specialcuisine = self.specialcuisine_entry.get()

        if not bin or not type or not dishname or not price:
            messagebox.showerror('Error', 'Invalid input')
            return

        conn = sqlite3.connect('banquet.db')
        c = conn.cursor()
        c.execute('INSERT INTO Meal (BIN, Type, DishName, Price, SpecialCuisine) VALUES (?, ?, ?, ?, ?)',
                  (bin, type, dishname, price, specialcuisine))
        conn.commit()
        conn.close()

        self.destroy()
        self.master.load_data()

class EditMealWindow(ttk.Toplevel):
    def __init__(self, parent, mealid):
        super().__init__(parent)
        self.title('Edit Meal')
        self.geometry('400x300')
        self.mealid = mealid

        # Query meal information
        conn = sqlite3.connect('banquet.db')
        c = conn.cursor()
        c.execute('SELECT * FROM Meal WHERE MealID = ?', (mealid,))
        row = c.fetchone()
        conn.close()

        # Create labels and entry fields with grid
        ttk.Label(self, text='BIN:').grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.bin_combobox = ttk.Combobox(self)
        self.bin_combobox.grid(row=0, column=1, padx=5, pady=5)
        self.bin_combobox.insert(0, row[1])

        ttk.Label(self, text='Type:').grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.type_entry = ttk.Entry(self)
        self.type_entry.grid(row=1, column=1, padx=5, pady=5)
        self.type_entry.insert(0, row[2])

        ttk.Label(self, text='Dish Name:').grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        self.dishname_entry = ttk.Entry(self)
        self.dishname_entry.grid(row=2, column=1, padx=5, pady=5)
        self.dishname_entry.insert(0, row[3])

        ttk.Label(self, text='Price:').grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
        self.price_entry = ttk.Entry(self)
        self.price_entry.grid(row=3, column=1, padx=5, pady=5)
        self.price_entry.insert(0, row[4])

        ttk.Label(self, text='Special Cuisine:').grid(row=4, column=0, padx=5, pady=5, sticky=tk.E)
        self.specialcuisine_entry = ttk.Entry(self)
        self.specialcuisine_entry.grid(row=4, column=1, padx=5, pady=5)
        self.specialcuisine_entry.insert(0, row[5])

        # Create button
        ttk.Button(self, text='Save', command=self.save).grid(row=5, column=1, padx=5, pady=10)

    def save(self):
        bin = self.bin_combobox.get()
        type = self.type_entry.get()
        dishname = self.dishname_entry.get()
        price = self.price_entry.get()
        specialcuisine = self.specialcuisine_entry.get()

        if not bin or not type or not dishname or not price:
            messagebox.showerror('Error', 'Invalid input')
            return

        conn = sqlite3.connect('banquet.db')
        c = conn.cursor()
        c.execute('UPDATE Meal SET BIN = ?, Type = ?, DishName = ?, Price = ?, SpecialCuisine = ? WHERE MealID = ?',
                  (bin, type, dishname, price, specialcuisine, self.mealid))
        conn.commit()
        conn.close()

        self.destroy()
        self.master.load_data()

class AttendeeManager(ttk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Attendee Manager')
        self.geometry('800x400')

        # Use grid layout for the main window
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create a main frame
        main_frame = ttk.Frame(self)
        main_frame.grid(row=0, column=0, sticky='nsew')

        # Configure rows and columns in the main frame
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # Create Treeview with scrollbars
        self.tree = ttk.Treeview(main_frame, columns=('AccountID', 'FirstName', 'LastName', 'Address', 'AttendeeType', 'Password', 'MobileNumber', 'AffiliatedOrganization'), show='headings')
        self.tree.heading('AccountID', text='Account ID')
        self.tree.heading('FirstName', text='First Name')
        self.tree.heading('LastName', text='Last Name')
        self.tree.heading('Address', text='Address')
        self.tree.heading('AttendeeType', text='Attendee Type')
        self.tree.heading('Password', text='Password')
        self.tree.heading('MobileNumber', text='Mobile Number')
        self.tree.heading('AffiliatedOrganization', text='Affiliated Organization')
        self.tree.grid(row=0, column=0, sticky='nsew')

        vsb = ttk.Scrollbar(main_frame, orient="vertical", command=self.tree.yview)
        vsb.grid(row=0, column=1, sticky='ns')
        self.tree.configure(yscrollcommand=vsb.set)

        hsb = ttk.Scrollbar(main_frame, orient="horizontal", command=self.tree.xview)
        hsb.grid(row=1, column=0, sticky='ew')
        self.tree.configure(xscrollcommand=hsb.set)

        # Create buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky='e')
        ttk.Button(button_frame, text='Add', command=self.add_attendee).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text='Edit', command=self.edit_attendee).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text='Delete', command=self.delete_attendee).pack(side=tk.LEFT, padx=5)

        # Load data
        self.load_data()

    def load_data(self):
        conn = sqlite3.connect('banquet.db')
        c = conn.cursor()
        c.execute('SELECT * FROM attendees_account')
        rows = c.fetchall()
        conn.close()
        for row in rows:
            self.tree.insert('', tk.END, values=row)

    def add_attendee(self):
        AddAttendeeWindow(self)

    def edit_attendee(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror('Error', 'Please select an attendee')
            return
        accountid = self.tree.item(selected_item)['values'][0]
        EditAttendeeWindow(self, accountid)

    def delete_attendee(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror('Error', 'Please select an attendee')
            return
        accountid = self.tree.item(selected_item)['values'][0]
        conn = sqlite3.connect('banquet.db')
        c = conn.cursor()
        c.execute('DELETE FROM attendees_account WHERE AccountID = ?', (accountid,))
        conn.commit()
        conn.close()
        self.tree.delete(selected_item)

class AddAttendeeWindow(ttk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Add Attendee')
        self.geometry('400x300')

        # Create labels and entry fields with grid
        ttk.Label(self, text='Account ID:').grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.accountid_entry = ttk.Entry(self)
        self.accountid_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self, text='First Name:').grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.firstname_entry = ttk.Entry(self)
        self.firstname_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self, text='Last Name:').grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        self.lastname_entry = ttk.Entry(self)
        self.lastname_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self, text='Address:').grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
        self.address_entry = ttk.Entry(self)
        self.address_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(self, text='Attendee Type:').grid(row=4, column=0, padx=5, pady=5, sticky=tk.E)
        self.attendee_type_entry = ttk.Entry(self)
        self.attendee_type_entry.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(self, text='Password:').grid(row=5, column=0, padx=5, pady=5, sticky=tk.E)
        self.password_entry = ttk.Entry(self, show='*')
        self.password_entry.grid(row=5, column=1, padx=5, pady=5)

        ttk.Label(self, text='Mobile Number:').grid(row=6, column=0, padx=5, pady=5, sticky=tk.E)
        self.mobile_entry = ttk.Entry(self)
        self.mobile_entry.grid(row=6, column=1, padx=5, pady=5)

        ttk.Label(self, text='Affiliated Organization:').grid(row=7, column=0, padx=5, pady=5, sticky=tk.E)
        self.organization_entry = ttk.Entry(self)
        self.organization_entry.grid(row=7, column=1, padx=5, pady=5)

        # Create button
        ttk.Button(self, text='Add', command=self.add).grid(row=8, column=1, padx=5, pady=10)

    def add(self):
        accountid = self.accountid_entry.get()
        firstname = self.firstname_entry.get()
        lastname = self.lastname_entry.get()
        address = self.address_entry.get()
        attendee_type = self.attendee_type_entry.get()
        password = self.password_entry.get()
        mobile = self.mobile_entry.get()
        organization = self.organization_entry.get()

        if not accountid or not firstname or not lastname or not address or not attendee_type or not password or not mobile or not organization:
            messagebox.showerror('Error', 'Invalid input')
            return

        conn = sqlite3.connect('banquet.db')
        c = conn.cursor()
        c.execute('INSERT INTO attendees_account (AccountID, FirstName, LastName, Address, AttendeeType, Password, MobileNumber, AffiliatedOrganization) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                  (accountid, firstname, lastname, address, attendee_type, password, mobile, organization))
        conn.commit()
        conn.close()

        self.destroy()
        self.master.load_data()

class EditAttendeeWindow(ttk.Toplevel):
    def __init__(self, parent, accountid):
        super().__init__(parent)
        self.title('Edit Attendee')
        self.geometry('400x300')
        self.accountid = accountid

        # Query attendee information
        conn = sqlite3.connect('banquet.db')
        c = conn.cursor()
        c.execute('SELECT * FROM attendees_account WHERE AccountID = ?', (accountid,))
        row = c.fetchone()
        conn.close()

        # Create labels and entry fields with grid
        ttk.Label(self, text='Account ID:').grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.accountid_entry = ttk.Entry(self)
        self.accountid_entry.grid(row=0, column=1, padx=5, pady=5)
        self.accountid_entry.insert(0, row[0])
        self.accountid_entry.config(state='readonly')

        ttk.Label(self, text='First Name:').grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.firstname_entry = ttk.Entry(self)
        self.firstname_entry.grid(row=1, column=1, padx=5, pady=5)
        self.firstname_entry.insert(0, row[1])

        ttk.Label(self, text='Last Name:').grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        self.lastname_entry = ttk.Entry(self)
        self.lastname_entry.grid(row=2, column=1, padx=5, pady=5)
        self.lastname_entry.insert(0, row[2])

        ttk.Label(self, text='Address:').grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
        self.address_entry = ttk.Entry(self)
        self.address_entry.grid(row=3, column=1, padx=5, pady=5)
        self.address_entry.insert(0, row[3])

        ttk.Label(self, text='Attendee Type:').grid(row=4, column=0, padx=5, pady=5, sticky=tk.E)
        self.attendee_type_entry = ttk.Entry(self)
        self.attendee_type_entry.grid(row=4, column=1, padx=5, pady=5)
        self.attendee_type_entry.insert(0, row[4])

        ttk.Label(self, text='Password:').grid(row=5, column=0, padx=5, pady=5, sticky=tk.E)
        self.password_entry = ttk.Entry(self, show='*')
        self.password_entry.grid(row=5, column=1, padx=5, pady=5)
        self.password_entry.insert(0, row[5])

        ttk.Label(self, text='Mobile Number:').grid(row=6, column=0, padx=5, pady=5, sticky=tk.E)
        self.mobile_entry = ttk.Entry(self)
        self.mobile_entry.grid(row=6, column=1, padx=5, pady=5)
        self.mobile_entry.insert(0, row[6])

        ttk.Label(self, text='Affiliated Organization:').grid(row=7, column=0, padx=5, pady=5, sticky=tk.E)
        self.organization_entry = ttk.Entry(self)
        self.organization_entry.grid(row=7, column=1, padx=5, pady=5)
        self.organization_entry.insert(0, row[7])

        # Create button
        ttk.Button(self, text='Save', command=self.save).grid(row=8, column=1, padx=5, pady=10)

    def save(self):
        firstname = self.firstname_entry.get()
        lastname = self.lastname_entry.get()
        address = self.address_entry.get()
        attendee_type = self.attendee_type_entry.get()
        password = self.password_entry.get()
        mobile = self.mobile_entry.get()
        organization = self.organization_entry.get()

        if not firstname or not lastname or not address or not attendee_type or not password or not mobile or not organization:
            messagebox.showerror('Error', 'Invalid input')
            return

        conn = sqlite3.connect('banquet.db')
        c = conn.cursor()
        c.execute('UPDATE attendees_account SET FirstName = ?, LastName = ?, Address = ?, AttendeeType = ?, Password = ?, MobileNumber = ?, AffiliatedOrganization = ? WHERE AccountID = ?',
                  (firstname, lastname, address, attendee_type, password, mobile, organization, self.accountid))
        conn.commit()
        conn.close()

        self.destroy()
        self.master.load_data()

class RegisterManager(ttk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Registration Manager')
        self.geometry('600x400')

        # 使用 grid 布局
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # 创建主框架
        main_frame = ttk.Frame(self)
        main_frame.grid(row=0, column=0, sticky='nsew')

        # 在主框架中设置行和列的权重
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # 创建 Treeview 和垂直滚动条
        self.tree = ttk.Treeview(main_frame, columns=('RegistrationID', 'AccountID', 'BIN', 'RegistrationDate', 'DrinkChoice', 'MealChoice', 'Remarks', 'SeatNumber'), show='headings')
        self.tree.heading('RegistrationID', text='Registration ID')
        self.tree.heading('AccountID', text='Account ID')
        self.tree.heading('BIN', text='BIN')
        self.tree.heading('RegistrationDate', text='Registration Date')
        self.tree.heading('DrinkChoice', text='Drink Choice')
        self.tree.heading('MealChoice', text='Meal Choice')
        self.tree.heading('Remarks', text='Remarks')
        self.tree.heading('SeatNumber', text='Seat Number')
        self.tree.grid(row=0, column=0, sticky='nsew')

        vsb = ttk.Scrollbar(main_frame, orient="vertical", command=self.tree.yview)
        vsb.grid(row=0, column=1, sticky='ns')
        self.tree.configure(yscrollcommand=vsb.set)

        # 添加水平滚动条
        hsb = ttk.Scrollbar(main_frame, orient="horizontal", command=self.tree.xview)
        hsb.grid(row=1, column=0, sticky='ew')
        self.tree.configure(xscrollcommand=hsb.set)

        # 创建按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky='e')
        ttk.Button(button_frame, text='Add', command=self.add_register).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text='Delete', command=self.delete_register).pack(side=tk.LEFT, padx=5)

        # 加载数据
        self.load_data()

    def load_data(self):
        conn = sqlite3.connect('banquet.db')
        c = conn.cursor()
        c.execute('SELECT * FROM Registrations')
        rows = c.fetchall()
        conn.close()
        for row in rows:
            self.tree.insert('', tk.END, values=row)

    def add_register(self):
        AddRegisterWindow(self)

    def delete_register(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror('Error', 'Please select a registration')
            return
        regid = self.tree.item(selected_item)['values'][0]
        conn = sqlite3.connect('banquet.db')
        c = conn.cursor()
        c.execute('DELETE FROM Registrations WHERE RegistrationID = ?', (regid,))
        conn.commit()
        conn.close()
        self.tree.delete(selected_item)

class AddRegisterWindow(ttk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Add Registration')
        self.geometry('400x300')

        # Query attendee and banquet data
        conn = sqlite3.connect('banquet.db')
        c = conn.cursor()
        c.execute('SELECT AccountID FROM attendees_account')
        attendees = c.fetchall()
        c.execute('SELECT BIN FROM Banquet')
        banquets = c.fetchall()
        conn.close()

        # Create labels and entry fields with grid
        ttk.Label(self, text='Registration Date:').grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.date_entry = ttk.Entry(self)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self, text='Account ID:').grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.accountid_combobox = ttk.Combobox(self, values=[attendee[0] for attendee in attendees])
        self.accountid_combobox.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self, text='BIN:').grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        self.bin_combobox = ttk.Combobox(self, values=[banquet[0] for banquet in banquets])
        self.bin_combobox.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self, text='Drink Choice:').grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
        self.drink_entry = ttk.Entry(self)
        self.drink_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(self, text='Meal Choice:').grid(row=4, column=0, padx=5, pady=5, sticky=tk.E)
        self.meal_entry = ttk.Entry(self)
        self.meal_entry.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(self, text='Remarks:').grid(row=5, column=0, padx=5, pady=5, sticky=tk.E)
        self.remarks_entry = ttk.Entry(self)
        self.remarks_entry.grid(row=5, column=1, padx=5, pady=5)

        ttk.Label(self, text='Seat Number:').grid(row=6, column=0, padx=5, pady=5, sticky=tk.E)
        self.seat_entry = ttk.Entry(self)
        self.seat_entry.grid(row=6, column=1, padx=5, pady=5)

        # Create button
        ttk.Button(self, text='Add', command=self.add).grid(row=7, column=1, padx=5, pady=10)

    def add(self):
        date = self.date_entry.get()
        accountid = self.accountid_combobox.get()
        bin = self.bin_combobox.get()
        drink = self.drink_entry.get()
        meal = self.meal_entry.get()
        remarks = self.remarks_entry.get()
        seat = self.seat_entry.get()

        if not date or not accountid or not bin or not seat:
            messagebox.showerror('Error', 'Invalid input')
            return

        conn = sqlite3.connect('banquet.db')
        c = conn.cursor()
        c.execute('INSERT INTO Registrations (RegistrationDate, AccountID, BIN, DrinkChoice, MealChoice, Remarks, SeatNumber) VALUES (?, ?, ?, ?, ?, ?, ?)',
                  (date, accountid, bin, drink, meal, remarks, seat))
        conn.commit()
        conn.close()

        self.destroy()
        self.master.load_data()
class ReportWindow(tk.Toplevel):
    def __init__(self, parent, report_data, report_title):
        super().__init__(parent)
        self.title(report_title)
        
        # 创建菜单栏
        menu = tk.Menu(self)
        self.config(menu=menu)
        file_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label='File', menu=file_menu)
        file_menu.add_command(label='Export to Excel', command=self.export_to_excel)
        file_menu.add_command(label='Export to PDF', command=self.export_to_pdf)
        
        # 创建Treeview来显示数据
        self.tree = ttk.Treeview(self, columns=tuple(report_data[0].keys()), show='headings')
        for col in report_data[0].keys():
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        for row in report_data:
            self.tree.insert('', 'end', values=tuple(row.values()))
        self.tree.pack(expand=True, fill='both')
        
        # 保存数据以便导出
        self.data = report_data

    def export_to_excel(self):
        df = pd.DataFrame(self.data)
        file_path = filedialog.asksaveasfilename(defaultextension='.xlsx', filetypes=[('Excel files', '*.xlsx')])
        if file_path:
            df.to_excel(file_path, index=False)

    def export_to_pdf(self):
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
        from reportlab.lib import colors

        file_path = filedialog.asksaveasfilename(defaultextension='.pdf', filetypes=[('PDF files', '*.pdf')])
        if not file_path:
            return

        data = [tuple(self.data[0].keys())] + [tuple(row.values()) for row in self.data]
        pdf = SimpleDocTemplate(file_path, pagesize=letter)
        table = Table(data)

        # 设置表格样式
        style = TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.grey),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('BACKGROUND', (0,1), (-1,-1), colors.beige),
        ])
        table.setStyle(style)

        # 添加表格到PDF
        pdf.build([table])

if __name__ == '__main__':
    conn = sqlite3.connect('banquet.db')
    print ("数据库打开成功")
    app = MainWindow()
    app.mainloop()