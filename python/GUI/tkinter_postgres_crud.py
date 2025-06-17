import tkinter as tk
from tkinter import ttk, messagebox
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# PostgreSQL connection
engine = create_engine("postgresql://eliezer:admin@localhost:5432/db5785")

# Utility: fetch all rows
def fetch_all(table):
    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT * FROM {table}"))
        return result.keys(), result.fetchall()

# Insert new customer
def add_customer():
    fname = entry_fname.get()
    lname = entry_lname.get()
    if fname and lname:
        try:
            with engine.begin() as conn:
                conn.execute(text("INSERT INTO customer (first_name, last_name) VALUES (:fname, :lname)"),
                             {"fname": fname, "lname": lname})
            messagebox.showinfo("Success", "customer added")
            entry_fname.delete(0, tk.END)
            entry_lname.delete(0, tk.END)
            refresh_table("customer")
        except SQLAlchemyError as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showwarning("Input Error", "Please fill all fields")

# Update customer
def update_customer():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Selection Error", "Please select a customer to update")
        return
    
    fname = entry_fname.get()
    lname = entry_lname.get()
    if fname and lname:
        try:
            # Get the selected item's values
            item_values = tree.item(selected[0])['values']
            customer_id = item_values[0]  # Assuming first column is ID
            
            with engine.begin() as conn:
                conn.execute(text("UPDATE customer SET first_name = :fname, last_name = :lname WHERE id = :id"),
                             {"fname": fname, "lname": lname, "id": customer_id})
            messagebox.showinfo("Success", "Customer updated")
            entry_fname.delete(0, tk.END)
            entry_lname.delete(0, tk.END)
            refresh_table("customer")
        except SQLAlchemyError as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showwarning("Input Error", "Please fill all fields")

# Insert new product
def add_product():
    name = entry_product_name.get()
    price = entry_product_price.get()
    if name and price:
        try:
            price = float(price)
            with engine.begin() as conn:
                conn.execute(text("INSERT INTO Product (name, price) VALUES (:name, :price)"),
                             {"name": name, "price": price})
            messagebox.showinfo("Success", "Product added")
            entry_product_name.delete(0, tk.END)
            entry_product_price.delete(0, tk.END)
            refresh_table("Product")
        except ValueError:
            messagebox.showwarning("Input Error", "Price must be a number")
        except SQLAlchemyError as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showwarning("Input Error", "Please fill all fields")

# Update product
def update_product():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Selection Error", "Please select a product to update")
        return
    
    name = entry_product_name.get()
    price = entry_product_price.get()
    if name and price:
        try:
            price = float(price)
            # Get the selected item's values
            item_values = tree.item(selected[0])['values']
            product_id = item_values[0]  # Assuming first column is ID
            
            with engine.begin() as conn:
                conn.execute(text("UPDATE Product SET name = :name, price = :price WHERE id = :id"),
                             {"name": name, "price": price, "id": product_id})
            messagebox.showinfo("Success", "Product updated")
            entry_product_name.delete(0, tk.END)
            entry_product_price.delete(0, tk.END)
            refresh_table("Product")
        except ValueError:
            messagebox.showwarning("Input Error", "Price must be a number")
        except SQLAlchemyError as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showwarning("Input Error", "Please fill all fields")

# Insert new invoice
def add_invoice():
    cid = entry_invoice_customer.get()
    pid = entry_invoice_product.get()
    qty = entry_invoice_qty.get()
    
    if cid and pid and qty:
        try:
            cid = int(cid)
            pid = int(pid)
            qty = int(qty)
            with engine.begin() as conn:
                conn.execute(text("INSERT INTO Invoice (customer_id, product_id, quantity) VALUES (:cid, :pid, :qty)"),
                             {"cid": cid, "pid": pid, "qty": qty})
            messagebox.showinfo("Success", "Invoice added")
            entry_invoice_customer.delete(0, tk.END)
            entry_invoice_product.delete(0, tk.END)
            entry_invoice_qty.delete(0, tk.END)
            refresh_table("Invoice")
        except ValueError:
            messagebox.showwarning("Input Error", "All values must be integers")
        except SQLAlchemyError as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showwarning("Input Error", "Please fill all fields")

# Update invoice
def update_invoice():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Selection Error", "Please select an invoice to update")
        return
    
    cid = entry_invoice_customer.get()
    pid = entry_invoice_product.get()
    qty = entry_invoice_qty.get()
    
    if cid and pid and qty:
        try:
            cid = int(cid)
            pid = int(pid)
            qty = int(qty)
            # Get the selected item's values
            item_values = tree.item(selected[0])['values']
            invoice_id = item_values[0]  # Assuming first column is ID
            
            with engine.begin() as conn:
                conn.execute(text("UPDATE Invoice SET customer_id = :cid, product_id = :pid, quantity = :qty WHERE id = :id"),
                             {"cid": cid, "pid": pid, "qty": qty, "id": invoice_id})
            messagebox.showinfo("Success", "Invoice updated")
            entry_invoice_customer.delete(0, tk.END)
            entry_invoice_product.delete(0, tk.END)
            entry_invoice_qty.delete(0, tk.END)
            refresh_table("Invoice")
        except ValueError:
            messagebox.showwarning("Input Error", "All values must be integers")
        except SQLAlchemyError as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showwarning("Input Error", "Please fill all fields")

# Display table
def refresh_table(table_name):
    try:
        columns, rows = fetch_all(table_name)
        
        # Clear existing items
        for item in tree.get_children():
            tree.delete(item)
        
        # Configure columns
        tree["columns"] = list(columns)
        tree["show"] = "headings"  # Hide the default first column
        
        # Set up column headings and widths
        for col in columns:
            tree.heading(col, text=str(col))
            tree.column(col, anchor="center", width=100)
        
        # Insert data - convert all values to strings to avoid formatting issues
        for row in rows:
            # Convert each value in the row to string and handle None values
            clean_values = []
            for value in row:
                if value is None:
                    clean_values.append("")
                else:
                    clean_values.append(str(value))
            tree.insert("", "end", values=clean_values)
            
    except SQLAlchemyError as e:
        messagebox.showerror("Database Error", f"Failed to fetch data from {table_name}: {str(e)}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while refreshing the table: {str(e)}")

# Load selected record into form fields
def load_selected_record():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Selection Error", "Please select a record to edit")
        return
    
    # Get the selected item's values
    item_values = tree.item(selected[0])['values']
    current_table = label_table.cget("text").split()[0].lower()  # Get current table name
    
    if current_table == "customer":
        if len(item_values) >= 3:  # Assuming id, first_name, last_name
            entry_fname.delete(0, tk.END)
            entry_lname.delete(0, tk.END)
            entry_fname.insert(0, item_values[1])  # first_name
            entry_lname.insert(0, item_values[2])  # last_name
    elif current_table == "product":
        if len(item_values) >= 3:  # Assuming id, name, price
            entry_product_name.delete(0, tk.END)
            entry_product_price.delete(0, tk.END)
            entry_product_name.insert(0, item_values[1])  # name
            entry_product_price.insert(0, item_values[2])  # price
    elif current_table == "invoice":
        if len(item_values) >= 4:  # Assuming id, customer_id, product_id, quantity
            entry_invoice_customer.delete(0, tk.END)
            entry_invoice_product.delete(0, tk.END)
            entry_invoice_qty.delete(0, tk.END)
            entry_invoice_customer.insert(0, item_values[1])  # customer_id
            entry_invoice_product.insert(0, item_values[2])  # product_id
            entry_invoice_qty.insert(0, item_values[3])  # quantity

# Switch view
def switch_table(table):
    label_table.config(text=f"{table} Table")
    refresh_table(table)

# GUI Setup
window = tk.Tk()
window.title("PostgreSQL CRUD GUI")
window.geometry("900x600")

# --- Customer Section ---
frm_customer = tk.LabelFrame(window, text="Add Customer")
frm_customer.pack(padx=10, pady=5, fill="x")

tk.Label(frm_customer, text="First Name:").pack(side="left", padx=5)
entry_fname = tk.Entry(frm_customer)
entry_fname.pack(side="left", padx=5)

tk.Label(frm_customer, text="Last Name:").pack(side="left", padx=5)
entry_lname = tk.Entry(frm_customer)
entry_lname.pack(side="left", padx=5)

btn_add_cust = tk.Button(frm_customer, text="Add Customer", command=add_customer)
btn_add_cust.pack(side="left", padx=5)

btn_update_cust = tk.Button(frm_customer, text="Update Customer", command=update_customer)
btn_update_cust.pack(side="left", padx=5)

# --- Product Section ---
frm_product = tk.LabelFrame(window, text="Add Product")
frm_product.pack(padx=10, pady=5, fill="x")

tk.Label(frm_product, text="Name:").pack(side="left", padx=5)
entry_product_name = tk.Entry(frm_product)
entry_product_name.pack(side="left", padx=5)

tk.Label(frm_product, text="Price:").pack(side="left", padx=5)
entry_product_price = tk.Entry(frm_product)
entry_product_price.pack(side="left", padx=5)

btn_add_prod = tk.Button(frm_product, text="Add Product", command=add_product)
btn_add_prod.pack(side="left", padx=5)

btn_update_prod = tk.Button(frm_product, text="Update Product", command=update_product)
btn_update_prod.pack(side="left", padx=5)

# --- Invoice Section ---
frm_invoice = tk.LabelFrame(window, text="Add Invoice")
frm_invoice.pack(padx=10, pady=5, fill="x")

tk.Label(frm_invoice, text="Customer ID:").pack(side="left", padx=5)
entry_invoice_customer = tk.Entry(frm_invoice)
entry_invoice_customer.pack(side="left", padx=5)

tk.Label(frm_invoice, text="Product ID:").pack(side="left", padx=5)
entry_invoice_product = tk.Entry(frm_invoice)
entry_invoice_product.pack(side="left", padx=5)

tk.Label(frm_invoice, text="Quantity:").pack(side="left", padx=5)
entry_invoice_qty = tk.Entry(frm_invoice)
entry_invoice_qty.pack(side="left", padx=5)

btn_add_invoice = tk.Button(frm_invoice, text="Add Invoice", command=add_invoice)
btn_add_invoice.pack(side="left", padx=5)

btn_update_invoice = tk.Button(frm_invoice, text="Update Invoice", command=update_invoice)
btn_update_invoice.pack(side="left", padx=5)

# --- Table Display ---
label_table = tk.Label(window, text="Customer Table", font=("Arial", 14))
label_table.pack(pady=5)

# Create frame for treeview with scrollbars
tree_frame = tk.Frame(window)
tree_frame.pack(expand=True, fill="both", padx=10, pady=10)

tree = ttk.Treeview(tree_frame, show="headings")
tree.pack(side="left", expand=True, fill="both")

# Add scrollbars
v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
v_scrollbar.pack(side="right", fill="y")
tree.configure(yscrollcommand=v_scrollbar.set)

h_scrollbar = ttk.Scrollbar(window, orient="horizontal", command=tree.xview)
h_scrollbar.pack(fill="x", padx=10)
tree.configure(xscrollcommand=h_scrollbar.set)

# --- Table Switch Buttons ---
frm_buttons = tk.Frame(window)
frm_buttons.pack(pady=5)

tk.Button(frm_buttons, text="Show Customers", command=lambda: switch_table("customer")).pack(side="left", padx=5)
tk.Button(frm_buttons, text="Show Products", command=lambda: switch_table("Product")).pack(side="left", padx=5)
tk.Button(frm_buttons, text="Show Invoices", command=lambda: switch_table("Invoice")).pack(side="left", padx=5)
tk.Button(frm_buttons, text="Load Selected", command=load_selected_record).pack(side="left", padx=5)

# Initial load
refresh_table("customer")

window.mainloop()
