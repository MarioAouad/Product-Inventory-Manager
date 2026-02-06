# Product Inventory Manager

A robust desktop GUI application developed in Python for efficient product and inventory tracking. This tool leverages **SQLite** for reliable local storage and **Tkinter** for an intuitive interface, allowing users to manage product details including names, symbols, quantities, and expiration dates.

## 🚀 Key Features

* **CRUD Operations:** Add, Edit, Delete, and View products with ease.
* **Smart Search:** Real-time filtering to find products by name instantly.
* **Data Validation:**
    * Ensures "Symbol" contains only letters.
    * Ensures "Quantity" contains only integers.
    * Validates "Expiration Date" format (DD-MM-YYYY).
    * Prevents duplicate entries.
* **Automated Export:** Automatically exports the entire database to a `.sql` file (`exported_products.sql`) upon exit, ensuring you always have a backup.
* **Safety Controls:** Includes warning prompts before resetting the database or quitting the application.

## 🛠️ Technology Stack

* **Language:** Python 3.x
* **GUI Framework:** Tkinter (Standard Python Library)
* **Database:** SQLite3 (Built-in)

## 📂 Project Structure

* `Product Inventory Manager.py`: The main application script containing the GUI and database logic.
* `products.db`: The local SQLite database file (automatically created on first run).
* `exported_products.sql`: The backup file generated when closing the program.

## 📦 Installation & Usage

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/MarioAouad/Product-Inventory-Manager.git
    cd Product-Inventory-Manager
    ```

2.  **Run the Application:**
    Since this uses standard libraries, no `pip install` is usually required.
    ```bash
    python Product Inventory Manager.py
    ```

## 🎮 How to Use

1.  **Add Product:** Fill in the Name, Symbol, Quantity, and Expiration Date (DD-MM-YYYY) at the top form and click **Add Product**.
2.  **Edit/Delete:** Select a row from the list and use the buttons at the bottom to modify or remove it.
3.  **Search:** Type a product name in the search bar to filter the list.
4.  **Export & Quit:** Click **Quit** to automatically save your current data into a SQL script file for external use.

## ⚠️ Notes
* The `exported_products.sql` file is generated using T-SQL syntax (`IF OBJECT_ID...`), making it compatible for import into **Microsoft SQL Server**.
