import tkinter as tk
from tkinter import ttk, messagebox
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.exc import SQLAlchemyError

# PostgreSQL connection
engine = create_engine("postgresql://eliezer:admin@localhost:5432/db5785")
Base = declarative_base()

# ORM Models
class Customer(Base):
    __tablename__ = 'customer'
    
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    
    # Relationship
    invoices = relationship("Invoice", back_populates="customer")
    
    def __repr__(self):
        return f"<Customer(id={self.id}, name='{self.first_name} {self.last_name}')>"

class Product(Base):
    __tablename__ = 'product'  # Note: keeping your original table name
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    
    # Relationship
    invoices = relationship("Invoice", back_populates="product")
    
    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', price={self.price})>"

class Invoice(Base):
    __tablename__ = 'invoice'  # Note: keeping your original table name
    
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    
    # Relationships
    customer = relationship("Customer", back_populates="invoices")
    product = relationship("Product", back_populates="invoices")
    
    def __repr__(self):
        return f"<Invoice(id={self.id}, customer_id={self.customer_id}, product_id={self.product_id}, qty={self.quantity})>"

# Create session
Session = sessionmaker(bind=engine)

# Utility: fetch all rows using ORM
def fetch_all_orm(model_class):
    session = Session()
    try:
        records = session.query(model_class).all()
        # Convert to list of tuples for compatibility with existing UI code
        if not records:
            return [], []
        
        # Get column names from the model
        columns = [column.name for column in model_class.__table__.columns]
        
        # Convert records to tuples
        rows = []
        for record in records:
            row = tuple(getattr(record, col) for col in columns)
            rows.append(row)
        
        return columns, rows
    except SQLAlchemyError as e:
        messagebox.showerror("Database Error", str(e))
        return [], []
    finally:
        session.close()

# Get model class by table name
def get_model_by_name(table_name):
    models = {
        'customer': Customer,
        'product': Product,
        'invoice': Invoice
    }
    return models.get(table_name)

# Insert new customer using ORM
def add_customer():
    fname = entry_fname.get()
    lname = entry_lname.get()
    if fname and lname:
        session = Session()
        try:
            new_customer = Customer(first_name=fname, last_name=lname)
            session.add(new_customer)
            session.commit()
            messagebox.showinfo("Success", "Customer added")
            entry_fname.delete(0, tk.END)
            entry_lname.delete(0, tk.END)
            refresh_table("customer")
        except SQLAlchemyError as e:
            session.rollback()
            messagebox.showerror("Error", str(e))
        finally:
            session.close()
    else:
        messagebox.showwarning("Input Error", "Please fill all fields")

# Update customer using ORM
def update_customer():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Selection Error", "Please select a customer to update")
        return
    
    fname = entry_fname.get()
    lname = entry_lname.get()
    if fname and lname:
        session = Session()
        try:
            # Get the selected item's values
            item_values = tree.item(selected[0])['values']
            customer_id = int(item_values[0])
            
            # Find and update the customer
            customer = session.query(Customer).get(customer_id)
            if customer:
                customer.first_name = fname
                customer.last_name = lname
                session.commit()
                messagebox.showinfo("Success", "Customer updated")
                entry_fname.delete(0, tk.END)
                entry_lname.delete(0, tk.END)
                refresh_table("customer")
            else:
                messagebox.showerror("Error", "Customer not found")
        except SQLAlchemyError as e:
            session.rollback()
            messagebox.showerror("Error", str(e))
        finally:
            session.close()
    else:
        messagebox.showwarning("Input Error", "Please fill all fields")

# Insert new product using ORM
def add_product():
    name = entry_product_name.get()
    price = entry_product_price.get()
    if name and price:
        session = Session()
        try:
            price_float = float(price)
            new_product = Product(name=name, price=price_float)
            session.add(new_product)
            session.commit()
            messagebox.showinfo("Success", "Product added")
            entry_product_name.delete(0, tk.END)
            entry_product_price.delete(0, tk.END)
            refresh_table("Product")
        except ValueError:
            messagebox.showwarning("Input Error", "Price must be a number")
        except SQLAlchemyError as e:
            session.rollback()
            messagebox.showerror("Error", str(e))
        finally:
            session.close()
    else:
        messagebox.showwarning("Input Error", "Please fill all fields")

# Update product using ORM
def update_product():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Selection Error", "Please select a product to update")
        return
    
    name = entry_product_name.get()
    price = entry_product_price.get()
    if name and price:
        session = Session()
        try:
            price_float = float(price)
            # Get the selected item's values
            item_values = tree.item(selected[0])['values']
            product_id = int(item_values[0])
            
            # Find and update the product
            product = session.query(Product).get(product_id)
            if product:
                product.name = name
                product.price = price_float
                session.commit()
                messagebox.showinfo("Success", "Product updated")
                entry_product_name.delete(0, tk.END)
                entry_product_price.delete(0, tk.END)
                refresh_table("Product")
            else:
                messagebox.showerror("Error", "Product not found")
        except ValueError:
            messagebox.showwarning("Input Error", "Price must be a number")
        except SQLAlchemyError as e:
            session.rollback()
            messagebox.showerror("Error", str(e))
        finally:
            session.close()
    else:
        messagebox.showwarning("Input Error", "Please fill all fields")

# Insert new invoice using ORM
def add_invoice():
    cid = entry_invoice_customer.get()
    pid = entry_invoice_product.get()
    qty = entry_invoice_qty.get()
    
    if cid and pid and qty:
        session = Session()
        try:
            cid_int = int(cid)
            pid_int = int(pid)
            qty_int = int(qty)
            
            # Validate that customer and product exist
            customer = session.query(Customer).get(cid_int)
            product = session.query(Product).get(pid_int)
            
            if not customer:
                messagebox.showerror("Error", f"Customer with ID {cid_int} not found")
                return
            if not product:
                messagebox.showerror("Error", f"Product with ID {pid_int} not found")
                return
            
            new_invoice = Invoice(customer_id=cid_int, product_id=pid_int, quantity=qty_int)
            session.add(new_invoice)
            session.commit()
            messagebox.showinfo("Success", "Invoice added")
            entry_invoice_customer.delete(0, tk.END)
            entry_invoice_product.delete(0, tk.END)
            entry_invoice_qty.delete(0, tk.END)
            refresh_table("Invoice")
        except ValueError:
            messagebox.showwarning("Input Error", "All values must be integers")
        except SQLAlchemyError as e:
            session.rollback()
            messagebox.showerror("Error", str(e))
        finally:
            session.close()
    else:
        messagebox.showwarning("Input Error", "Please fill all fields")

# Update invoice using ORM
def update_invoice():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Selection Error", "Please select an invoice to update")
        return
    
    cid = entry_invoice_customer.get()
    pid = entry_invoice_product.get()
    qty = entry_invoice_qty.get()
    
    if cid and pid and qty:
        session = Session()
        try:
            cid_int = int(cid)
            pid_int = int(pid)
            qty_int = int(qty)
            
            # Get the selected item's values
            item_values = tree.item(selected[0])['values']
            invoice_id = int(item_values[0])
            
            # Validate that customer and product exist
            customer = session.query(Customer).get(cid_int)
            product = session.query(Product).get(pid_int)
            
            if not customer:
                messagebox.showerror("Error", f"Customer with ID {cid_int} not found")
                return
            if not product:
                messagebox.showerror("Error", f"Product with ID {pid_int} not found")
                return
            
            # Find and update the invoice
            invoice = session.query(Invoice).get(invoice_id)
            if invoice:
                invoice.customer_id = cid_int
                invoice.product_id = pid_int
                invoice.quantity = qty_int
                session.commit()
                messagebox.showinfo("Success", "Invoice updated")
                entry_invoice_customer.delete(0, tk.END)
                entry_invoice_product.delete(0, tk.END)
                entry_invoice_qty.delete(0, tk.END)
                refresh_table("Invoice")
            else:
                messagebox.showerror("Error", "Invoice not found")
        except ValueError:
            messagebox.showwarning("Input Error", "All values must be integers")
        except SQLAlchemyError as e:
            session.rollback()
            messagebox.showerror("Error", str(e))
        finally:
            session.close()
    else:
        messagebox.showwarning("Input Error", "Please fill all fields")

# Delete record using ORM
def delete_record():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Selection Error", "Please select a record to delete")
        return
    
    current_table = label_table.cget("text").split()[0].lower()
    model_class = get_model_by_name(current_table)
    
    if not model_class:
        messagebox.showerror("Error", "Unknown table")
        return
    
    # Confirm deletion
    if not messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this record?"):
        return
    
    session = Session()
    try:
        # Get the selected item's values
        item_values = tree.item(selected[0])['values']
        record_id = int(item_values[0])
        
        # Find and delete the record
        record = session.query(model_class).get(record_id)
        if record:
            session.delete(record)
            session.commit()
            messagebox.showinfo("Success", "Record deleted")
            refresh_table(current_table)
        else:
            messagebox.showerror("Error", "Record not found")
    except SQLAlchemyError as e:
        session.rollback()
        messagebox.showerror("Error", str(e))
    finally:
        session.close()

# Display table using ORM
def refresh_table(table_name):
    try:
        model_class = get_model_by_name(table_name)
        if not model_class:
            messagebox.showerror("Error", f"Unknown table: {table_name}")
            return
            
        columns, rows = fetch_all_orm(model_class)
        
        # Clear existing items
        for item in tree.get_children():
            tree.delete(item)
        
        # Configure columns
        tree["columns"] = list(columns)
        tree["show"] = "headings"
        
        # Set up column headings and widths
        for col in columns:
            tree.heading(col, text=str(col))
            tree.column(col, anchor="center", width=100)
        
        # Insert data
        for row in rows:
            clean_values = []
            for value in row:
                if value is None:
                    clean_values.append("")
                else:
                    clean_values.append(str(value))
            tree.insert("", "end", values=clean_values)
            
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while refreshing the table: {str(e)}")

# Load selected record into form fields
def load_selected_record():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Selection Error", "Please select a record to edit")
        return
    
    item_values = tree.item(selected[0])['values']
    current_table = label_table.cget("text").split()[0].lower()
    
    if current_table == "customer":
        if len(item_values) >= 3:
            entry_fname.delete(0, tk.END)
            entry_lname.delete(0, tk.END)
            entry_fname.insert(0, item_values[1])
            entry_lname.insert(0, item_values[2])
    elif current_table == "product":
        if len(item_values) >= 3:
            entry_product_name.delete(0, tk.END)
            entry_product_price.delete(0, tk.END)
            entry_product_name.insert(0, item_values[1])
            entry_product_price.insert(0, item_values[2])
    elif current_table == "invoice":
        if len(item_values) >= 4:
            entry_invoice_customer.delete(0, tk.END)
            entry_invoice_product.delete(0, tk.END)
            entry_invoice_qty.delete(0, tk.END)
            entry_invoice_customer.insert(0, item_values[1])
            entry_invoice_product.insert(0, item_values[2])
            entry_invoice_qty.insert(0, item_values[3])

# Switch view
def switch_table(table):
    label_table.config(text=f"{table} Table")
    refresh_table(table)

# Show customers with their invoice details (using relationships)
def show_customer_invoices():
    session = Session()
    try:
        # Using ORM relationships to join data
        customers_with_invoices = session.query(Customer).join(Invoice).join(Product).all()
        
        # Create a new window to display the results
        detail_window = tk.Toplevel(window)
        detail_window.title("Customer Invoice Details")
        detail_window.geometry("800x400")
        
        # Create treeview for detailed view
        detail_tree = ttk.Treeview(detail_window, show="headings")
        detail_tree["columns"] = ("Customer ID", "Customer Name", "Product", "Price", "Quantity", "Total")
        
        for col in detail_tree["columns"]:
            detail_tree.heading(col, text=col)
            detail_tree.column(col, anchor="center", width=120)
        
        # Populate with relationship data
        for customer in customers_with_invoices:
            for invoice in customer.invoices:
                total = invoice.product.price * invoice.quantity
                detail_tree.insert("", "end", values=(
                    customer.id,
                    f"{customer.first_name} {customer.last_name}",
                    invoice.product.name,
                    f"${invoice.product.price:.2f}",
                    invoice.quantity,
                    f"${total:.2f}"
                ))
        
        detail_tree.pack(expand=True, fill="both", padx=10, pady=10)
        
    except SQLAlchemyError as e:
        messagebox.showerror("Error", str(e))
    finally:
        session.close()

# GUI Setup
window = tk.Tk()
window.title("PostgreSQL CRUD GUI with ORM")
window.geometry("900x700")

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

# --- Action Buttons ---
frm_buttons = tk.Frame(window)
frm_buttons.pack(pady=5)

tk.Button(frm_buttons, text="Show Customers", command=lambda: switch_table("customer")).pack(side="left", padx=5)
tk.Button(frm_buttons, text="Show Products", command=lambda: switch_table("product")).pack(side="left", padx=5)
tk.Button(frm_buttons, text="Show Invoices", command=lambda: switch_table("invoice")).pack(side="left", padx=5)
tk.Button(frm_buttons, text="Load Selected", command=load_selected_record).pack(side="left", padx=5)
tk.Button(frm_buttons, text="Delete Selected", command=delete_record, bg="red", fg="white").pack(side="left", padx=5)

# --- Advanced ORM Features ---
frm_advanced = tk.Frame(window)
frm_advanced.pack(pady=5)

tk.Button(frm_advanced, text="Customer Invoice Details", command=show_customer_invoices, bg="lightblue").pack(side="left", padx=5)

# Initial load
refresh_table("customer")

window.mainloop()
