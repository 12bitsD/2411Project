import tkinter as tk
from tkinter import ttk, messagebox, filedialog
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
        attendee_menu.add_command(label='Search Registrations', command=self.open_search_registrations)
        menu_bar.add_cascade(label='Attendee Management', menu=attendee_menu)

        # Create reports menu
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

    def open_search_registrations(self):
        SearchRegistrationsWindow(self)

    def generate_registration_report(self):
        conn = sqlite3.connect('banquet.db')
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT Banquet.Name, COUNT(AttendeesAccount.AccountID) AS RegistrationCount
            FROM Banquet
            LEFT JOIN AttendeesAccount ON Banquet.BIN = AttendeesAccount.BIN
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
        
        cursor.execute("""
            SELECT Banquet.Name, Meal.DishName, COUNT(AttendeesAccount.AccountID) AS Count
            FROM Banquet
            JOIN AttendeesAccount ON Banquet.BIN = AttendeesAccount.BIN
            JOIN Meal ON AttendeesAccount.MealChoice = Meal.MealID
            GROUP BY Banquet.BIN, Meal.DishName
            ORDER BY Count DESC;
        """)
        data = cursor.fetchall()
        
        columns = [desc[0] for desc in cursor.description]
        report_data = [dict(zip(columns, row)) for row in data]
        
        ReportWindow(self, report_data, 'Popular Meals Report')
        
        conn.close()

    def generate_attendance_behavior_report(self):
        conn = sqlite3.connect('banquet.db')
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT AttendeesAccount.FirstName, AttendeesAccount.LastName, 
                   COUNT(CASE WHEN AttendeesAccount.Available = 'Y' THEN 1 END) AS AttendanceCount
            FROM AttendeesAccount
            GROUP BY AttendeesAccount.AccountID;
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

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        main_frame = ttk.Frame(self)
        main_frame.grid(row=0, column=0, sticky='nsew')

        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

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

        hsb = ttk.Scrollbar(main_frame, orient="horizontal", command=self.tree.xview)
        hsb.grid(row=1, column=0, sticky='ew')
        self.tree.configure(xscrollcommand=hsb.set)

        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky='e')
        ttk.Button(button_frame, text='Add', command=self.add_banquet).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text='Edit', command=self.edit_banquet).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text='Delete', command=self.delete_banquet).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text='Manage Meals', command=self.manage_meals).pack(side=tk.LEFT, padx=5)

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

    def manage_meals(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror('Error', 'Please select a banquet')
            return
        bin = self.tree.item(selected_item)['values'][0]
        ManageBanquetMealsWindow(self, bin)

class AddBanquetWindow(ttk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Add Banquet')
        self.geometry('400x300')

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
        self.available_entry = ttk.Combobox(self, values=['Y', 'N'])
        self.available_entry.grid(row=6, column=1, padx=5, pady=5)

        ttk.Label(self, text='Quota:').grid(row=7, column=0, padx=5, pady=5, sticky=tk.E)
        self.quota_entry = ttk.Entry(self)
        self.quota_entry.grid(row=7, column=1, padx=5, pady=5)

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

        conn = sqlite3.connect('banquet.db')
        c = conn.cursor()
        c.execute('SELECT * FROM Banquet WHERE BIN = ?', (bin,))
        row = c.fetchone()
        conn.close()

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
        self.available_entry = ttk.Combobox(self, values=['Y', 'N'])
        self.available_entry.grid(row=6, column=1, padx=5, pady=5)
        self.available_entry.set(row[7])

        ttk.Label(self, text='Quota:').grid(row=7, column=0, padx=5, pady=5, sticky=tk.E)
        self.quota_entry = ttk.Entry(self)
        self.quota_entry.grid(row=7, column=1, padx=5, pady=5)
        self.quota_entry.insert(0, row[8])

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

class ManageBanquetMealsWindow(ttk.Toplevel):
    def __init__(self, parent, bin):
        super().__init__(parent)
        self.title('Manage Banquet Meals')
        self.bin = bin

        conn = sqlite3.connect('banquet.db')
        c = conn.cursor()
        c.execute('SELECT MealID, DishName FROM Meal')
        meals = c.fetchall()
        conn.close()

        self.meals_list = ttk.Listbox(self, exportselection=False)
        self.meals_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        for meal in meals:
            self.meals_list.insert(tk.END, f"{meal[0]} - {meal[1]}")

        ttk.Button(self, text='Add Meal', command=self.add_meal).pack(side=tk.TOP, padx=5, pady=5)
        ttk.Button(self, text='Remove Meal', command=self.remove_meal).pack(side=tk.TOP, padx=5, pady=5)

        self.load_current_meals()

    def load_current_meals(self):
        conn = sqlite3.connect('banquet.db')
        c = conn.cursor()
        c.execute('SELECT MealID FROM BanquetMeal WHERE BIN = ?', (self.bin,))
        current_meals = c.fetchall()
        conn.close()

        for meal in self.meals_list.get(0, tk.END):
            meal_id = int(meal.split(' - ')[0])
            if meal_id in [cm[0] for cm in current_meals]:
                self.meals_list.select_set(self.meals_list.index(meal))

    def add_meal(self):
        selected_indices = self.meals_list.curselection()
        if not selected_indices:
            return
        for idx in selected_indices:
            meal_id = int(self.meals_list.get(idx).split(' - ')[0])
            conn = sqlite3.connect('banquet.db')
            c = conn.cursor()
            c.execute('INSERT INTO BanquetMeal (BIN, MealID) VALUES (?, ?)', (self.bin, meal_id))
            conn.commit()
            conn.close()

    def remove_meal(self):
        selected_indices = self.meals_list.curselection()
        if not selected_indices:
            return
        for idx in selected_indices:
            meal_id = int(self.meals_list.get(idx).split(' - ')[0])
            conn = sqlite3.connect('banquet.db')
            c = conn.cursor()
            c.execute('DELETE FROM BanquetMeal WHERE BIN = ? AND MealID = ?', (self.bin, meal_id))
            conn.commit()
            conn.close()

class MealManager(ttk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Meal Manager')
        self.geometry('600x400')

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        main_frame = ttk.Frame(self)
        main_frame.grid(row=0, column=0, sticky='nsew')

        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

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

        hsb = ttk.Scrollbar(main_frame, orient="horizontal", command=self.tree.xview)
        hsb.grid(row=1, column=0, sticky='ew')
        self.tree.configure(xscrollcommand=hsb.set)

        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky='e')
        ttk.Button(button_frame, text='Add', command=self.add_meal).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text='Edit', command=self.edit_meal).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text='Delete', command=self.delete_meal).pack(side=tk.LEFT, padx=5)

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

        ttk.Label(self, text='BIN:').grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.bin_entry = ttk.Entry(self)
        self.bin_entry.grid(row=0, column=1, padx=5, pady=5)

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

        ttk.Button(self, text='Add', command=self.add).grid(row=5, column=1, padx=5, pady=10)

    def add(self):
        bin = self.bin_entry.get()
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

        conn = sqlite3.connect('banquet.db')
        c = conn.cursor()
        c.execute('SELECT * FROM Meal WHERE MealID = ?', (mealid,))
        row = c.fetchone()
        conn.close()

        ttk.Label(self, text='BIN:').grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.bin_entry = ttk.Entry(self)
        self.bin_entry.grid(row=0, column=1, padx=5, pady=5)
        self.bin_entry.insert(0, row[1])

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

        ttk.Button(self, text='Save', command=self.save).grid(row=5, column=1, padx=5, pady=10)

    def save(self):
        bin = self.bin_entry.get()
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

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        main_frame = ttk.Frame(self)
        main_frame.grid(row=0, column=0, sticky='nsew')

        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        self.tree = ttk.Treeview(main_frame, columns=('AccountID', 'BIN', 'FirstName', 'LastName', 'Address', 'AttendeeType', 'Password', 'MobileNumber', 'AffiliatedOrganization', 'DrinkChoice', 'MealChoice', 'Remarks', 'SeatNumber'), show='headings')
        self.tree.heading('AccountID', text='Account ID')
        self.tree.heading('BIN', text='BIN')
        self.tree.heading('FirstName', text='First Name')
        self.tree.heading('LastName', text='Last Name')
        self.tree.heading('Address', text='Address')
        self.tree.heading('AttendeeType', text='Attendee Type')
        self.tree.heading('Password', text='Password')
        self.tree.heading('MobileNumber', text='Mobile Number')
        self.tree.heading('AffiliatedOrganization', text='Affiliated Organization')
        self.tree.heading('DrinkChoice', text='Drink Choice')
        self.tree.heading('MealChoice', text='Meal Choice')
        self.tree.heading('Remarks', text='Remarks')
        self.tree.heading('SeatNumber', text='Seat Number')
        self.tree.grid(row=0, column=0, sticky='nsew')

        vsb = ttk.Scrollbar(main_frame, orient="vertical", command=self.tree.yview)
        vsb.grid(row=0, column=1, sticky='ns')
        self.tree.configure(yscrollcommand=vsb.set)

        hsb = ttk.Scrollbar(main_frame, orient="horizontal", command=self.tree.xview)
        hsb.grid(row=1, column=0, sticky='ew')
        self.tree.configure(xscrollcommand=hsb.set)

        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky='e')
        ttk.Button(button_frame, text='Add', command=self.add_attendee).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text='Edit', command=self.edit_attendee).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text='Delete', command=self.delete_attendee).pack(side=tk.LEFT, padx=5)

        self.load_data()

    def load_data(self):
        conn = sqlite3.connect('banquet.db')
        c = conn.cursor()
        c.execute('SELECT * FROM AttendeesAccount')
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
        c.execute('DELETE FROM AttendeesAccount WHERE AccountID = ?', (accountid,))
        conn.commit()
        conn.close()
        self.tree.delete(selected_item)

class AddAttendeeWindow(ttk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Add Attendee')
        self.geometry('600x400')

        conn = sqlite3.connect('banquet.db')
        c = conn.cursor()
        c.execute('SELECT BIN, Name FROM Banquet')
        banquets = c.fetchall()
        c.execute('SELECT MealID, DishName FROM Meal')
        meals = c.fetchall()
        conn.close()

        ttk.Label(self, text='Account ID:').grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.accountid_entry = ttk.Entry(self)
        self.accountid_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self, text='BIN:').grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.bin_combobox = ttk.Combobox(self, values=[str(banquet[0]) for banquet in banquets])
        self.bin_combobox.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self, text='First Name:').grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        self.firstname_entry = ttk.Entry(self)
        self.firstname_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self, text='Last Name:').grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
        self.lastname_entry = ttk.Entry(self)
        self.lastname_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(self, text='Address:').grid(row=4, column=0, padx=5, pady=5, sticky=tk.E)
        self.address_entry = ttk.Entry(self)
        self.address_entry.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(self, text='Attendee Type:').grid(row=5, column=0, padx=5, pady=5, sticky=tk.E)
        self.attendee_type_entry = ttk.Entry(self)
        self.attendee_type_entry.grid(row=5, column=1, padx=5, pady=5)

        ttk.Label(self, text='Password:').grid(row=6, column=0, padx=5, pady=5, sticky=tk.E)
        self.password_entry = ttk.Entry(self, show='*')
        self.password_entry.grid(row=6, column=1, padx=5, pady=5)

        ttk.Label(self, text='Mobile Number:').grid(row=7, column=0, padx=5, pady=5, sticky=tk.E)
        self.mobile_entry = ttk.Entry(self)
        self.mobile_entry.grid(row=7, column=1, padx=5, pady=5)

        ttk.Label(self, text='Affiliated Organization:').grid(row=8, column=0, padx=5, pady=5, sticky=tk.E)
        self.organization_entry = ttk.Entry(self)
        self.organization_entry.grid(row=8, column=1, padx=5, pady=5)

        ttk.Label(self, text='Drink Choice:').grid(row=9, column=0, padx=5, pady=5, sticky=tk.E)
        self.drink_entry = ttk.Entry(self)
        self.drink_entry.grid(row=9, column=1, padx=5, pady=5)

        ttk.Label(self, text='Meal Choice:').grid(row=10, column=0, padx=5, pady=5, sticky=tk.E)
        self.meal_combobox = ttk.Combobox(self, values=[f"{meal[0]} - {meal[1]}" for meal in meals])
        self.meal_combobox.grid(row=10, column=1, padx=5, pady=5)

        ttk.Label(self, text='Remarks:').grid(row=11, column=0, padx=5, pady=5, sticky=tk.E)
        self.remarks_entry = ttk.Entry(self)
        self.remarks_entry.grid(row=11, column=1, padx=5, pady=5)

        ttk.Label(self, text='Seat Number:').grid(row=12, column=0, padx=5, pady=5, sticky=tk.E)
        self.seat_entry = ttk.Entry(self)
        self.seat_entry.grid(row=12, column=1, padx=5, pady=5)

        ttk.Button(self, text='Add', command=self.add).grid(row=13, column=1, padx=5, pady=10)

    def add(self):
        accountid = self.accountid_entry.get()
        bin = self.bin_combobox.get()
        firstname = self.firstname_entry.get()
        lastname = self.lastname_entry.get()
        address = self.address_entry.get()
        attendee_type = self.attendee_type_entry.get()
        password = self.password_entry.get()
        mobile = self.mobile_entry.get()
        organization = self.organization_entry.get()
        drink = self.drink_entry.get()
        meal_choice = self.meal_combobox.get().split(' - ')[0] if self.meal_combobox.get() else None
        remarks = self.remarks_entry.get()
        seat = self.seat_entry.get()

        if not accountid or not bin or not firstname or not lastname or not address or not attendee_type or not password or not mobile or not organization or not seat:
            messagebox.showerror('Error', 'Invalid input')
            return

        conn = sqlite3.connect('banquet.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO AttendeesAccount (
                AccountID, BIN, FirstName, LastName, Address, AttendeeType, 
                Password, MobileNumber, AffiliatedOrganization, DrinkChoice, 
                MealChoice, Remarks, SeatNumber
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            accountid, bin, firstname, lastname, address, attendee_type,
            password, mobile, organization, drink,
            meal_choice, remarks, seat
        ))
        conn.commit()
        conn.close()

        self.destroy()
        self.master.load_data()

class EditAttendeeWindow(ttk.Toplevel):
    def __init__(self, parent, accountid):
        super().__init__(parent)
        self.title('Edit Attendee')
        self.geometry('600x400')
        self.accountid = accountid

        conn = sqlite3.connect('banquet.db')
        c = conn.cursor()
        c.execute('SELECT * FROM AttendeesAccount WHERE AccountID = ?', (accountid,))
        row = c.fetchone()
        c.execute('SELECT BIN, Name FROM Banquet')
        banquets = c.fetchall()
        c.execute('SELECT MealID, DishName FROM Meal')
        meals = c.fetchall()
        conn.close()

        ttk.Label(self, text='Account ID:').grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.accountid_entry = ttk.Entry(self)
        self.accountid_entry.grid(row=0, column=1, padx=5, pady=5)
        self.accountid_entry.insert(0, row[0])
        self.accountid_entry.config(state='readonly')

        ttk.Label(self, text='BIN:').grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.bin_combobox = ttk.Combobox(self, values=[str(banquet[0]) for banquet in banquets])
        self.bin_combobox.grid(row=1, column=1, padx=5, pady=5)
        self.bin_combobox.set(row[1])

        ttk.Label(self, text='First Name:').grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        self.firstname_entry = ttk.Entry(self)
        self.firstname_entry.grid(row=2, column=1, padx=5, pady=5)
        self.firstname_entry.insert(0, row[2])

        ttk.Label(self, text='Last Name:').grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
        self.lastname_entry = ttk.Entry(self)
        self.lastname_entry.grid(row=3, column=1, padx=5, pady=5)
        self.lastname_entry.insert(0, row[3])

        ttk.Label(self, text='Address:').grid(row=4, column=0, padx=5, pady=5, sticky=tk.E)
        self.address_entry = ttk.Entry(self)
        self.address_entry.grid(row=4, column=1, padx=5, pady=5)
        self.address_entry.insert(0, row[4])

        ttk.Label(self, text='Attendee Type:').grid(row=5, column=0, padx=5, pady=5, sticky=tk.E)
        self.attendee_type_entry = ttk.Entry(self)
        self.attendee_type_entry.grid(row=5, column=1, padx=5, pady=5)
        self.attendee_type_entry.insert(0, row[5])

        ttk.Label(self, text='Password:').grid(row=6, column=0, padx=5, pady=5, sticky=tk.E)
        self.password_entry = ttk.Entry(self, show='*')
        self.password_entry.grid(row=6, column=1, padx=5, pady=5)
        self.password_entry.insert(0, row[6])

        ttk.Label(self, text='Mobile Number:').grid(row=7, column=0, padx=5, pady=5, sticky=tk.E)
        self.mobile_entry = ttk.Entry(self)
        self.mobile_entry.grid(row=7, column=1, padx=5, pady=5)
        self.mobile_entry.insert(0, row[7])

        ttk.Label(self, text='Affiliated Organization:').grid(row=8, column=0, padx=5, pady=5, sticky=tk.E)
        self.organization_entry = ttk.Entry(self)
        self.organization_entry.grid(row=8, column=1, padx=5, pady=5)
        self.organization_entry.insert(0, row[8])

        ttk.Label(self, text='Drink Choice:').grid(row=9, column=0, padx=5, pady=5, sticky=tk.E)
        self.drink_entry = ttk.Entry(self)
        self.drink_entry.grid(row=9, column=1, padx=5, pady=5)
        self.drink_entry.insert(0, row[9] if row[9] else '')

        ttk.Label(self, text='Meal Choice:').grid(row=10, column=0, padx=5, pady=5, sticky=tk.E)
        self.meal_combobox = ttk.Combobox(self, values=[f"{meal[0]} - {meal[1]}" for meal in meals])
        self.meal_combobox.grid(row=10, column=1, padx=5, pady=5)
        if row[10]:
            self.meal_combobox.set(f"{row[10]} - ")

        ttk.Label(self, text='Remarks:').grid(row=11, column=0, padx=5, pady=5, sticky=tk.E)
        self.remarks_entry = ttk.Entry(self)
        self.remarks_entry.grid(row=11, column=1, padx=5, pady=5)
        self.remarks_entry.insert(0, row[11] if row[11] else '')

        ttk.Label(self, text='Seat Number:').grid(row=12, column=0, padx=5, pady=5, sticky=tk.E)
        self.seat_entry = ttk.Entry(self)
        self.seat_entry.grid(row=12, column=1, padx=5, pady=5)
        self.seat_entry.insert(0, row[12])

        ttk.Button(self, text='Save', command=self.save).grid(row=13, column=1, padx=5, pady=10)

    def save(self):
        bin = self.bin_combobox.get()
        firstname = self.firstname_entry.get()
        lastname = self.lastname_entry.get()
        address = self.address_entry.get()
        attendee_type = self.attendee_type_entry.get()
        password = self.password_entry.get()
        mobile = self.mobile_entry.get()
        organization = self.organization_entry.get()
        drink = self.drink_entry.get()
        meal_choice = self.meal_combobox.get().split(' - ')[0] if self.meal_combobox.get() else None
        remarks = self.remarks_entry.get()
        seat = self.seat_entry.get()

        if not bin or not firstname or not lastname or not address or not attendee_type or not password or not mobile or not organization or not seat:
            messagebox.showerror('Error', 'Invalid input')
            return

        conn = sqlite3.connect('banquet.db')
        c = conn.cursor()
        c.execute('''
            UPDATE AttendeesAccount SET
                BIN = ?, FirstName = ?, LastName = ?, Address = ?, AttendeeType = ?,
                Password = ?, MobileNumber = ?, AffiliatedOrganization = ?,
                DrinkChoice = ?, MealChoice = ?, Remarks = ?, SeatNumber = ?
            WHERE AccountID = ?
        ''', (
            bin, firstname, lastname, address, attendee_type,
            password, mobile, organization,
            drink, meal_choice, remarks, seat,
            self.accountid
        ))
        conn.commit()
        conn.close()

        self.destroy()
        self.master.load_data()

class SearchRegistrationsWindow(ttk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Search Registrations')
        self.geometry('800x600')

        ttk.Label(self, text='Search Criteria:').grid(row=0, column=0, padx=10, pady=10, sticky='w')

        ttk.Label(self, text='Date:').grid(row=1, column=0, padx=10, pady=5, sticky='e')
        self.date_entry = ttk.Entry(self)
        self.date_entry.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(self, text='Banquet Name:').grid(row=2, column=0, padx=10, pady=5, sticky='e')
        self.banquet_name_entry = ttk.Entry(self)
        self.banquet_name_entry.grid(row=2, column=1, padx=10, pady=5)

        ttk.Label(self, text='Attendee Type:').grid(row=3, column=0, padx=10, pady=5, sticky='e')
        self.attendee_type_entry = ttk.Entry(self)
        self.attendee_type_entry.grid(row=3, column=1, padx=10, pady=5)

        ttk.Button(self, text='Search', command=self.search).grid(row=4, column=1, padx=10, pady=10)

        self.tree = ttk.Treeview(self, columns=('AccountID', 'BIN', 'Name', 'FirstName', 'LastName', 'AttendeeType', 'MealChoice'), show='headings')
        self.tree.heading('AccountID', text='Account ID')
        self.tree.heading('BIN', text='BIN')
        self.tree.heading('Name', text='Banquet Name')
        self.tree.heading('FirstName', text='First Name')
        self.tree.heading('LastName', text='Last Name')
        self.tree.heading('AttendeeType', text='Attendee Type')
        self.tree.heading('MealChoice', text='Meal Choice')
        self.tree.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

        ttk.Button(self, text='Update', command=self.update_registration).grid(row=6, column=1, padx=10, pady=10)

    def search(self):
        self.tree.delete(*self.tree.get_children())
        date = self.date_entry.get()
        banquet_name = self.banquet_name_entry.get()
        attendee_type = self.attendee_type_entry.get()

        query = '''
            SELECT AttendeesAccount.AccountID, AttendeesAccount.BIN, Banquet.Name, AttendeesAccount.FirstName, AttendeesAccount.LastName, AttendeesAccount.AttendeeType, AttendeesAccount.MealChoice
            FROM AttendeesAccount
            JOIN Banquet ON AttendeesAccount.BIN = Banquet.BIN
            WHERE 1=1
        '''
        params = []
        if date:
            query += ' AND AttendeesAccount.DateTime = ? '
            params.append(date)
        if banquet_name:
            query += ' AND Banquet.Name LIKE ? '
            params.append(f'%{banquet_name}%')
        if attendee_type:
            query += ' AND AttendeesAccount.AttendeeType = ? '
            params.append(attendee_type)

        conn = sqlite3.connect('banquet.db')
        c = conn.cursor()
        c.execute(query, tuple(params))
        rows = c.fetchall()
        conn.close()

        for row in rows:
            self.tree.insert('', 'end', values=row)

    def update_registration(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror('Error', 'Please select a registration to update.')
            return
        accountid = self.tree.item(selected_item)['values'][0]
        UpdateRegistrationWindow(self, accountid)

class UpdateRegistrationWindow(ttk.Toplevel):
    def __init__(self, parent, accountid):
        super().__init__(parent)
        self.title('Update Registration')
        self.geometry('400x300')
        self.accountid = accountid

        conn = sqlite3.connect('banquet.db')
        c = conn.cursor()
        c.execute('SELECT * FROM AttendeesAccount WHERE AccountID = ?', (accountid,))
        row = c.fetchone()
        conn.close()

        ttk.Label(self, text='First Name:').grid(row=0, column=0, padx=10, pady=5, sticky='e')
        self.firstname_entry = ttk.Entry(self)
        self.firstname_entry.grid(row=0, column=1, padx=10, pady=5)
        self.firstname_entry.insert(0, row[2])

        ttk.Label(self, text='Last Name:').grid(row=1, column=0, padx=10, pady=5, sticky='e')
        self.lastname_entry = ttk.Entry(self)
        self.lastname_entry.grid(row=1, column=1, padx=10, pady=5)
        self.lastname_entry.insert(0, row[3])

        ttk.Label(self, text='Attendee Type:').grid(row=2, column=0, padx=10, pady=5, sticky='e')
        self.attendee_type_entry = ttk.Entry(self)
        self.attendee_type_entry.grid(row=2, column=1, padx=10, pady=5)
        self.attendee_type_entry.insert(0, row[5])

        ttk.Label(self, text='Meal Choice:').grid(row=3, column=0, padx=10, pady=5, sticky='e')
        self.meal_choice_entry = ttk.Entry(self)
        self.meal_choice_entry.grid(row=3, column=1, padx=10, pady=5)
        self.meal_choice_entry.insert(0, row[10] if row[10] else '')

        ttk.Button(self, text='Save Changes', command=self.save).grid(row=4, column=1, padx=10, pady=10)

    def save(self):
        firstname = self.firstname_entry.get()
        lastname = self.lastname_entry.get()
        attendee_type = self.attendee_type_entry.get()
        meal_choice = self.meal_choice_entry.get()

        conn = sqlite3.connect('banquet.db')
        c = conn.cursor()
        c.execute('''
            UPDATE AttendeesAccount SET
                FirstName = ?, LastName = ?, AttendeeType = ?, MealChoice = ?
            WHERE AccountID = ?
        ''', (firstname, lastname, attendee_type, meal_choice, self.accountid))
        conn.commit()
        conn.close()

        messagebox.showinfo('Success', 'Registration updated successfully.')
        self.destroy()
        self.master.search()

class ReportWindow(tk.Toplevel):
    def __init__(self, parent, report_data, report_title):
        super().__init__(parent)
        self.title(report_title)
        self.report_data = report_data

        menu = tk.Menu(self)
        self.config(menu=menu)
        file_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label='File', menu=file_menu)
        file_menu.add_command(label='Export to Excel', command=self.export_to_excel)
        file_menu.add_command(label='Export to PDF', command=self.export_to_pdf)

        self.tree = ttk.Treeview(self, columns=tuple(report_data[0].keys()), show='headings')
        for col in report_data[0].keys():
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        for row in report_data:
            self.tree.insert('', 'end', values=tuple(row.values()))
        self.tree.pack(expand=True, fill='both')

    def export_to_excel(self):
        df = pd.DataFrame(self.report_data)
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

        data = [tuple(self.report_data[0].keys())] + [tuple(row.values()) for row in self.report_data]
        pdf = SimpleDocTemplate(file_path, pagesize=letter)
        table = Table(data)

        style = TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.grey),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('BACKGROUND', (0,1), (-1,-1), colors.beige),
        ])
        table.setStyle(style)

        pdf.build([table])

if __name__ == '__main__':
    conn = sqlite3.connect('banquet.db')
    print("Database opened successfully")
    app = MainWindow()
    app.mainloop()