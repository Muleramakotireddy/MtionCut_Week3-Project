import os
import tkinter as tk
from tkinter import ttk
import csv

def validate_amount(new_value):
    if new_value == "" or new_value.isdigit() or (new_value.count('.') == 1 and new_value.replace('.', '').isdigit()):
        return True
    return False

def add_expense():
    date = date_entry.get()
    category = category_entry.get()
    description = description_entry.get("1.0", tk.END).strip()  
    amount = amount_entry.get()
    if not amount.isdigit() and not is_valid_float(amount):
        status_label.config(text="Amount must be a valid number!", fg="red")
        return
    if date and category and description and amount:
        with open("expenses.txt", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([date, category, description.replace('\n', '\\n'), amount])
        status_label.config(text="Expense added successfully!", fg="green")
        date_entry.delete(0, tk.END)
        category_entry.delete(0, tk.END)
        description_entry.delete("1.0", tk.END)  
        amount_entry.delete(0, tk.END)
        view_expenses()
    else:
        status_label.config(text="Please fill all the fields!", fg="red")

def is_valid_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def delete_expense():
    selected_item = expenses_tree.selection()
    if selected_item:
        item_text = expenses_tree.item(selected_item, "values")
        date, category, description, amount = item_text
        description = description.replace('\n', '\\n')  # Match stored format
        with open("expenses.txt", "r") as file:
            lines = list(csv.reader(file))
        with open("expenses.txt", "w", newline="") as file:
            writer = csv.writer(file)
            for line in lines:
                if line != [date, category, description, amount]:
                    writer.writerow(line)
        status_label.config(text="Expense deleted successfully!", fg="green")
        view_expenses()
    else:
        status_label.config(text="Please select an expense to delete!", fg="red")

def view_expenses():
    global expenses_tree
    if os.path.exists("expenses.txt"):
        total_expense = 0
        expenses_tree.delete(*expenses_tree.get_children())  
        with open("expenses.txt", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                date, category, description, amount = row
                description = description.replace('\\n', '\n')  
                if len(description) > 50:  
                    description = description[:50] + "..."
                expenses_tree.insert("", tk.END, values=(date, category, description, amount))
                total_expense += float(amount)
        total_label.config(text=f"Total Expense: {total_expense:.2f}")
    else:
        total_label.config(text="No expenses recorded.")
        expenses_tree.delete(*expenses_tree.get_children())

def show_full_description(event):
    selected_item = expenses_tree.selection()
    if selected_item:
        item = expenses_tree.item(selected_item)
        description = item['values'][2]  
        
        
        popup = tk.Toplevel(root)
        popup.title("Full Description")
        description_label = tk.Label(popup, text=description, wraplength=400) 
        description_label.pack(padx=10, pady=10)


root = tk.Tk()
root.title("Expense Tracker")


date_label = tk.Label(root, text="Date (DD-MM-YYYY):")
date_label.grid(row=0, column=0, padx=5, pady=5)
date_entry = tk.Entry(root)
date_entry.grid(row=0, column=1, padx=5, pady=5)

category_label = tk.Label(root, text="Category:")
category_label.grid(row=1, column=0, padx=5, pady=5)
category_entry = tk.Entry(root)
category_entry.grid(row=1, column=1, padx=5, pady=5)

description_label = tk.Label(root, text="Description:")
description_label.grid(row=2, column=0, padx=5, pady=5)
description_entry = tk.Text(root, height=4, width=20)  
description_entry.grid(row=2, column=1, padx=5, pady=5)

amount_label = tk.Label(root, text="Amount:")
amount_label.grid(row=3, column=0, padx=5, pady=5)


vcmd = (root.register(validate_amount), '%P')
amount_entry = tk.Entry(root, validate="key", validatecommand=vcmd)
amount_entry.grid(row=3, column=1, padx=5, pady=5)

add_button = tk.Button(root, text="Add Expense", command=add_expense)
add_button.grid(row=4, column=0, columnspan=2, padx=5, pady=10)


columns = ("Date", "Category", "Description", "Amount")
expenses_tree = ttk.Treeview(root, columns=columns, show="headings")
expenses_tree.heading("Date", text="Date")
expenses_tree.heading("Category", text="Category")
expenses_tree.heading("Description", text="Description")
expenses_tree.heading("Amount", text="Amount")
expenses_tree.column("Description", width=500)  # Widen the description column
expenses_tree.grid(row=5, column=0, columnspan=3, padx=5, pady=5)


h_scrollbar = ttk.Scrollbar(root, orient="horizontal", command=expenses_tree.xview)
expenses_tree.configure(xscrollcommand=h_scrollbar.set)


h_scrollbar.grid(row=6, column=0, columnspan=3, sticky='ew')
expenses_tree.bind("<Double-1>", show_full_description)


total_label = tk.Label(root, text="")
total_label.grid(row=7, column=0, columnspan=2, padx=5, pady=5)


status_label = tk.Label(root, text="", fg="green")
status_label.grid(row=8, column=0, columnspan=2, padx=5, pady=5)


view_button = tk.Button(root, text="View Expenses", command=view_expenses)
view_button.grid(row=9, column=0, padx=5, pady=10)


delete_button = tk.Button(root, text="Delete Expense", command=delete_expense)
delete_button.grid(row=9, column=2, padx=5, pady=10)

if not os.path.exists("expenses.txt"):
    with open("expenses.txt", "w"):
        pass
view_expenses()
root.mainloop()
