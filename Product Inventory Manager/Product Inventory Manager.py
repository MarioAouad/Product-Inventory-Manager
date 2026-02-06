import tkinter as tk
from tkinter import messagebox
from tkinter.simpledialog import askstring
from datetime import datetime
import sqlite3

# Initialize main window
root = tk.Tk()
root.title("Product Management")
root.geometry("1000x750")  # Adjusted window size

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('products.db')
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        name TEXT NOT NULL PRIMARY KEY,
        symbol TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        expiration TEXT NOT NULL
    )
''')

# Function to validate symbol (only letters allowed)
def validate_symbol(symbol):
    return symbol.isalpha()

# Function to validate quantity (only numbers allowed)
def validate_quantity(quantity):
    return quantity.isdigit()

# Function to add product to the database
def add_product():
    product_name = entry_product.get().strip().title().replace(" ", "_")  # Capitalize first letter of each word and replace spaces with underscores
    product_quantity = entry_quantity.get().strip()
    product_symbol = entry_symbol.get().strip()
    expiration_date = entry_expiration.get().strip()

    # Validate symbol and quantity
    if not validate_symbol(product_symbol):
        messagebox.showwarning("Input Error", "Symbol can only contain letters!")
        return

    if not validate_quantity(product_quantity):
        messagebox.showwarning("Input Error", "Quantity can only contain numbers!")
        return

    if product_name and product_quantity and product_symbol and expiration_date:
        # Check if expiration date is valid
        try:
            expiration_date_obj = datetime.strptime(expiration_date, "%d-%m-%Y")  # Validate date format
            expiration_date = expiration_date_obj.strftime("%d-%m-%Y")  # Reformat to day-month-year
        except ValueError:
            messagebox.showwarning("Input Error", "Expiration date must be in the format DD-MM-YYYY!")
            return

        # Check for duplicate name or symbol in the database
        cursor.execute('SELECT * FROM products WHERE name = ? OR symbol = ?', (product_name, product_symbol))
        if cursor.fetchone():
            messagebox.showwarning("Duplicate Entry", "Product with this name or symbol already exists!")
            return

        # Insert the new product into the database
        cursor.execute('''
            INSERT INTO products (name, quantity, symbol, expiration)
            VALUES (?, ?, ?, ?)
        ''', (product_name, product_quantity, product_symbol, expiration_date))
        conn.commit()

        # Add product to the listbox
        listbox_products.insert(tk.END, f"Name: {product_name} - Symbol: {product_symbol} - Quantity: {product_quantity} - Expires: {expiration_date}")
        reset_entries()
    else:
        messagebox.showwarning("Input Error", "Please fill all fields!")

# Function to reset entry fields
def reset_entries():
    entry_product.delete(0, tk.END)
    entry_quantity.delete(0, tk.END)
    entry_symbol.delete(0, tk.END)
    entry_expiration.delete(0, tk.END)
    entry_search.delete(0, tk.END)  # Clear the search entry as well

# Function to reset the database
def reset_database():
    cursor.execute('DELETE FROM products')
    conn.commit()
    listbox_products.delete(0, tk.END)

# Function to delete selected product
def delete_product():
    selected_item = listbox_products.curselection()
    if selected_item:
        product_text = listbox_products.get(selected_item)
        product_name = product_text.split(" - ")[0].split(": ")[1]
        
        # Delete the product from the database
        cursor.execute('DELETE FROM products WHERE name = ?', (product_name,))
        conn.commit()

        # Remove from listbox
        listbox_products.delete(selected_item)
    else:
        messagebox.showwarning("Selection Error", "Please select a product to delete!")

# Function to edit selected product
def edit_product():
    selected_item = listbox_products.curselection()
    if selected_item:
        product_text = listbox_products.get(selected_item)
        product_name = product_text.split(" - ")[0].split(": ")[1]
        
        # Find the product in the database
        cursor.execute('SELECT * FROM products WHERE name = ?', (product_name,))
        product = cursor.fetchone()

        # Ask user what part of the product to edit
        edit_option = askstring("Edit Option", "What would you like to edit? (name, symbol, quantity, expiration)")

        if edit_option:
            edit_option = edit_option.lower()
            if edit_option == "name":
                new_name = askstring("New Name", "Enter the new name:")
                if new_name:
                    new_name = new_name.strip().title().replace(" ", "_")  # Capitalize and replace spaces with underscores
                    ((new_name.strip()).title()).replace(" ", "_")
                    cursor.execute('UPDATE products SET name = ? WHERE name = ?', (new_name, product_name))
                    conn.commit()
                    listbox_products.delete(selected_item)
                    listbox_products.insert(selected_item, f"Name: {new_name} - Symbol: {product[1]} - Quantity: {product[2]} - Expires: {product[3]}")
            elif edit_option == "quantity":
                new_quantity = askstring("New Quantity", "Enter the new quantity:")
                if new_quantity and new_quantity.isdigit():
                    cursor.execute('UPDATE products SET quantity = ? WHERE name = ?', (new_quantity, product_name))
                    conn.commit()
                    listbox_products.delete(selected_item)
                    listbox_products.insert(selected_item, f"Name: {product[0]} - Symbol: {product[1]} - Quantity: {new_quantity} - Expires: {product[3]}")
                else:
                    messagebox.showwarning("Input Error", "Quantity must be a number!")
            elif edit_option == "symbol":
                new_symbol = askstring("New Symbol", "Enter the new symbol:")
                if new_symbol and new_symbol.isalpha():
                    cursor.execute('UPDATE products SET symbol = ? WHERE name = ?', (new_symbol, product_name))
                    conn.commit()
                    listbox_products.delete(selected_item)
                    listbox_products.insert(selected_item, f"Name: {product[0]} - Symbol: {new_symbol} - Quantity: {product[2]} - Expires: {product[3]}")
                else:
                    messagebox.showwarning("Input Error", "Symbol must contain only letters!")
            elif edit_option == "expiration":
                new_expiration = askstring("New Expiration", "Enter the new expiration date (DD-MM-YYYY):")
                try:
                    expiration_date_obj = datetime.strptime(new_expiration, "%d-%m-%Y")  # Validate date format
                    cursor.execute('UPDATE products SET expiration = ? WHERE name = ?', (expiration_date_obj.strftime("%d-%m-%Y"), product_name))
                    conn.commit()
                    listbox_products.delete(selected_item)
                    listbox_products.insert(selected_item, f"Name: {product[0]} - Symbol: {product[1]} - Quantity: {product[2]} - Expires: {expiration_date_obj.strftime('%d-%m-%Y')}")
                except ValueError:
                    messagebox.showwarning("Input Error", "Expiration date must be in the format DD-MM-YYYY!")
            else:
                messagebox.showwarning("Input Error", "Invalid option entered. Please choose name, quantity, symbol, or expiration.")
    else:
        messagebox.showwarning("Selection Error", "Please select a product to edit!")

# Function to search for a product
def search_product():
    search_name = entry_search.get().strip().lower()
    # Clear the listbox and show only the matching product(s)
    listbox_products.delete(0, tk.END)
    
    cursor.execute('SELECT * FROM products WHERE name LIKE ?', ('%' + search_name + '%',))
    found_products = cursor.fetchall()
    
    if found_products:
        for product in found_products:
            listbox_products.insert(tk.END, f"Name: {product[0]} - Symbol: {product[1]} - Quantity: {product[2]} - Expires: {product[3]}")
    else:
        listbox_products.insert(tk.END, "No products found.")

# Function to show all products in the table again
def show_table():
    listbox_products.delete(0, tk.END)
    cursor.execute('SELECT * FROM products')
    all_products = cursor.fetchall()
    if not all_products:
        listbox_products.insert(tk.END, "No products in the database.")
    else:
        for product in all_products:
            listbox_products.insert(tk.END, f"Name: {product[0]} - Symbol: {product[1]} - Quantity: {product[2]} - Expires: {product[3]}")

# Function to export database to SQL file
def export_to_sql():
    # Open a file to write the SQL queries
    with open('exported_products.sql', 'w') as sql_file:
        # Write the table creation statement to the file
        sql_file.write('''-- Create products table if it doesn't exist
    IF OBJECT_ID('products', 'U') IS NULL
    BEGIN
        CREATE TABLE products (
            name VARCHAR(100) NOT NULL PRIMARY KEY,
            symbol VARCHAR(100) NOT NULL,
            quantity INT NOT NULL,
            expiration VARCHAR(20) NOT NULL
        );
    END
    \n\n''')

        # Fetch all data from the products table
        cursor.execute('SELECT * FROM products')
        rows = cursor.fetchall()

        # Check the length of each row and write the corresponding INSERT statement
        for row in rows:
            if len(row) == 4:  # Ensure row contains 4 elements
                product_name, symbol, quantity, expiration = row
                sql_file.write(f"INSERT INTO products (name, symbol, quantity, expiration) VALUES ('{product_name}', '{symbol}', {quantity}, '{expiration}');\n")
            else:
                print(f"Skipping row with unexpected format: {row}")

        sql_file.write("\nselect * from products")

    print("SQL file exported successfully!")


# Quit function
def quit_program():
    if messagebox.askokcancel("Quit", "Are you sure you want to quit?"):
        export_to_sql()  # Export database before quitting
        conn.commit()
        conn.close()  # Close the database connection when quitting
        root.quit()

# Frame for adding and searching product (above the table)
frame_top = tk.Frame(root)
frame_top.pack(side=tk.TOP, pady=10)

# Frame for table and buttons (center of the window)
frame_center = tk.Frame(root)
frame_center.pack(side=tk.TOP, padx=10, pady=10)

# Frame for bottom buttons (directly below the table)
frame_bottom = tk.Frame(root)
frame_bottom.pack(side=tk.TOP, pady=10)

# Add product section
label_product = tk.Label(frame_top, text="Enter Product Name:")
label_product.grid(row=0, column=0, padx=5, pady=5)

entry_product = tk.Entry(frame_top)
entry_product.grid(row=0, column=1, padx=5, pady=5)

label_quantity = tk.Label(frame_top, text="Enter Quantity:")
label_quantity.grid(row=2, column=0, padx=5, pady=5)

entry_symbol = tk.Entry(frame_top)
entry_symbol.grid(row=1, column=1, padx=5, pady=5)

label_symbol = tk.Label(frame_top, text="Enter Symbol:")
label_symbol.grid(row=1, column=0, padx=5, pady=5)

entry_quantity = tk.Entry(frame_top)
entry_quantity.grid(row=2, column=1, padx=5, pady=5)

label_expiration = tk.Label(frame_top, text="Enter Expiration Date (DD-MM-YYYY):")
label_expiration.grid(row=3, column=0, padx=5, pady=5)

entry_expiration = tk.Entry(frame_top)
entry_expiration.grid(row=3, column=1, padx=5, pady=5)

btn_add = tk.Button(frame_top, text="Add Product", command=add_product)
btn_add.grid(row=3, column=2, padx=5, pady=5)

# Search section
label_search = tk.Label(frame_top, text="Search for Product:")
label_search.grid(row=4, column=0, padx=5, pady=5)

entry_search = tk.Entry(frame_top)
entry_search.grid(row=4, column=1, padx=5, pady=5)

search_button = tk.Button(frame_top, text="Search", command=search_product)
search_button.grid(row=4, column=2, padx=5, pady=5)

# Product listbox (table) and scrollbar
listbox_products = tk.Listbox(frame_center, width=100, height=20)
listbox_products.grid(row=0, column=0, padx=5, pady=5)

# Buttons
btn_show_table = tk.Button(frame_bottom, text="Show Table", command=show_table)
btn_show_table.grid(row=0, column=0, padx=5, pady=5)

btn_edit = tk.Button(frame_bottom, text="Edit Product", command=edit_product)
btn_edit.grid(row=0, column=1, padx=5, pady=5)

btn_delete = tk.Button(frame_bottom, text="Delete Product", command=delete_product)
btn_delete.grid(row=0, column=2, padx=5, pady=5)

btn_reset_entries = tk.Button(frame_bottom, text="Reset Entries", command=reset_entries)
btn_reset_entries.grid(row=0, column=3, padx=5, pady=5)

btn_reset_database = tk.Button(frame_bottom, text="Reset Database", command=reset_database)
btn_reset_database.grid(row=0, column=4, padx=5, pady=5)

btn_quit = tk.Button(frame_bottom, text="Quit", command=quit_program)
btn_quit.grid(row=0, column=5, padx=5, pady=5)

# Center the buttons by expanding columns equally
frame_bottom.grid_columnconfigure(0, weight=1)
frame_bottom.grid_columnconfigure(1, weight=1)
frame_bottom.grid_columnconfigure(2, weight=1)
frame_bottom.grid_columnconfigure(3, weight=1)
frame_bottom.grid_columnconfigure(4, weight=1)
frame_bottom.grid_columnconfigure(5, weight=1)

# Run the application
root.mainloop()
