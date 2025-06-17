#Prerequesites
#pip install streamlit pandas sqlalchemy psycopg2-binary plotly

# streamlit_app.py
import streamlit as st
import pandas as pd
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from your_models import Customer, Product, Invoice, engine
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Streamlit app title
st.title("PostgreSQL CRUD App")

# Create session
Session = sessionmaker(bind=engine)

# Sidebar for table selection
table = st.sidebar.selectbox("Select Table", ["Customer", "Product", "Invoice", "Customer Invoices"])

# Fetch data function (unchanged, assuming it works)
def fetch_data(table_name):
    session = Session()
    try:
        model = {'Customer': Customer, 'Product': Product, 'Invoice': Invoice}[table_name]
        data = session.query(model).all()
        if not data:
            return pd.DataFrame()
        if table_name == "Customer":
            return pd.DataFrame([
                {'id': d.id, 'first_name': d.first_name, 'last_name': d.last_name}
                for d in data
            ])
        elif table_name == "Product":
            return pd.DataFrame([
                {'id': d.id, 'name': d.name, 'price': d.price}
                for d in data
            ])
        elif table_name == "Invoice":
            return pd.DataFrame([
                {'id': d.id, 'customer_id': d.customer_id, 'product_id': d.product_id, 'quantity': d.quantity}
                for d in data
            ])
    finally:
        session.close()

# Customer CRUD Functions
def add_customer(first_name, last_name):
    session = Session()
    try:
        # Validate input lengths
        if len(first_name) > 50 or len(last_name) > 50:
            logger.warning(f"Input too long: first_name={len(first_name)}, last_name={len(last_name)}")
            st.error("First Name and Last Name must be 50 characters or less")
            return
        if not first_name or not last_name:
            logger.warning("Empty input detected")
            st.error("First Name and Last Name cannot be empty")
            return

        logger.debug(f"Attempting to add customer: first_name='{first_name}', last_name='{last_name}'")
        new_customer = Customer(first_name=first_name, last_name=last_name)
        session.add(new_customer)
        session.flush()  # Ensure ID is assigned
        logger.debug(f"Assigned customer ID: {new_customer.id}")
        session.commit()
        logger.info(f"Customer '{first_name} {last_name}' added successfully with ID {new_customer.id}")
        st.success(f"Customer '{first_name} {last_name}' added successfully")
    except IntegrityError as e:
        session.rollback()
        logger.error(f"IntegrityError: {str(e)}")
        st.error(f"Database error: {str(e)} (Possible sequence issue or duplicate data)")
        st.info("Check if the 'customer_id_seq' sequence is synchronized with the table's max ID")
    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f"SQLAlchemyError: {str(e)}")
        st.error(f"Database error: {str(e)}")
    except Exception as e:
        session.rollback()
        logger.error(f"Unexpected error: {str(e)}")
        st.error(f"Unexpected error: {str(e)}")
    finally:
        session.close()
        
def update_customer(customer_id, first_name, last_name):
    session = Session()
    try:
        logger.debug(f"Attempting to update customer ID: {customer_id}")
        customer = session.query(Customer).get(customer_id)
        if customer:
            customer.first_name = first_name
            customer.last_name = last_name
            session.commit()
            logger.info("Customer updated successfully")
            st.success("Customer updated successfully")
        else:
            logger.warning(f"Customer ID {customer_id} not found")
            st.error(f"Customer with ID {customer_id} not found")
    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f"SQLAlchemyError: {str(e)}")
        st.error(f"Database error: {str(e)}")
    except Exception as e:
        session.rollback()
        logger.error(f"Unexpected error: {str(e)}")
        st.error(f"Unexpected error: {str(e)}")
    finally:
        session.close()

def delete_customer(customer_id):
    session = Session()
    try:
        logger.debug(f"Attempting to delete customer ID: {customer_id}")
        customer = session.query(Customer).get(customer_id)
        if customer:
            session.delete(customer)
            session.commit()
            logger.info("Customer deleted successfully")
            st.success("Customer deleted successfully")
        else:
            logger.warning(f"Customer ID {customer_id} not found")
            st.error(f"Customer with ID {customer_id} not found")
    except IntegrityError as e:
        session.rollback()
        logger.error(f"IntegrityError: {str(e)}")
        st.error(f"Cannot delete customer: {str(e)} (Likely due to associated invoices)")
    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f"SQLAlchemyError: {str(e)}")
        st.error(f"Database error: {str(e)}")
    except Exception as e:
        session.rollback()
        logger.error(f"Unexpected error: {str(e)}")
        st.error(f"Unexpected error: {str(e)}")
    finally:
        session.close()

# Other CRUD Functions (unchanged, included for completeness)
def add_product(name, price):
    session = Session()
    try:
        price_float = float(price)
        session.add(Product(name=name, price=price_float))
        session.commit()
        st.success("Product added")
    except ValueError:
        st.error("Price must be a number")
    except Exception as e:
        session.rollback()
        st.error(f"Error adding product: {str(e)}")
    finally:
        session.close()

def update_product(product_id, name, price):
    session = Session()
    try:
        price_float = float(price)
        product = session.query(Product).get(product_id)
        if product:
            product.name = name
            product.price = price_float
            session.commit()
            st.success("Product updated")
        else:
            st.error("Product not found")
    except ValueError:
        st.error("Price must be a number")
    except Exception as e:
        session.rollback()
        st.error(f"Error updating product: {str(e)}")
    finally:
        session.close()

def delete_product(product_id):
    session = Session()
    try:
        product = session.query(Product).get(product_id)
        if product:
            session.delete(product)
            session.commit()
            st.success("Product deleted")
        else:
            st.error("Product not found")
    except Exception as e:
        session.rollback()
        st.error(f"Error deleting product: {str(e)}")
    finally:
        session.close()

def add_invoice(customer_id, product_id, quantity):
    session = Session()
    try:
        customer = session.query(Customer).get(int(customer_id))
        product = session.query(Product).get(int(product_id))
        quantity_int = int(quantity)
        if not customer:
            st.error(f"Customer with ID {customer_id} not found")
            return
        if not product:
            st.error(f"Product with ID {product_id} not found")
            return
        session.add(Invoice(customer_id=customer_id, product_id=product_id, quantity=quantity_int))
        session.commit()
        st.success("Invoice added")
    except ValueError:
        st.error("Customer ID, Product ID, and Quantity must be integers")
    except Exception as e:
        session.rollback()
        st.error(f"Error adding invoice: {str(e)}")
    finally:
        session.close()

def update_invoice(invoice_id, customer_id, product_id, quantity):
    session = Session()
    try:
        customer = session.query(Customer).get(int(customer_id))
        product = session.query(Product).get(int(product_id))
        quantity_int = int(quantity)
        if not customer:
            st.error(f"Customer with ID {customer_id} not found")
            return
        if not product:
            st.error(f"Product with ID {product_id} not found")
            return
        invoice = session.query(Invoice).get(invoice_id)
        if invoice:
            invoice.customer_id = customer_id
            invoice.product_id = product_id
            invoice.quantity = quantity_int
            session.commit()
            st.success("Invoice updated")
        else:
            st.error("Invoice not found")
    except ValueError:
        st.error("Customer ID, Product ID, and Quantity must be integers")
    except Exception as e:
        session.rollback()
        st.error(f"Error updating invoice: {str(e)}")
    finally:
        session.close()

def delete_invoice(invoice_id):
    session = Session()
    try:
        invoice = session.query(Invoice).get(invoice_id)
        if invoice:
            session.delete(invoice)
            session.commit()
            st.success("Invoice deleted")
        else:
            st.error("Invoice not found")
    except Exception as e:
        session.rollback()
        st.error(f"Error deleting invoice: {str(e)}")
    finally:
        session.close()

# Customer Section
if table == "Customer":
    st.header("Customers")
    df = fetch_data("Customer")
    if not df.empty:
        st.dataframe(df)
    else:
        st.write("No customers found")

    with st.form("add_customer"):
        first_name = st.text_input("First Name", max_chars=50)
        last_name = st.text_input("Last Name", max_chars=50)
        submitted = st.form_submit_button("Add Customer")
        if submitted:
            if first_name.strip() and last_name.strip():
                add_customer(first_name.strip(), last_name.strip())
                st.rerun()
            else:
                st.warning("First Name and Last Name cannot be empty or contain only whitespace")

    with st.form("update_customer"):
        customer_id = st.number_input("Customer ID to Update", min_value=1, step=1)
        update_first_name = st.text_input("New First Name", max_chars=50)
        update_last_name = st.text_input("New Last Name", max_chars=50)
        submitted = st.form_submit_button("Update Customer")
        if submitted:
            if update_first_name.strip() and update_last_name.strip():
                update_customer(customer_id, update_first_name.strip(), update_last_name.strip())
                st.rerun()
            else:
                st.warning("New First Name and Last Name cannot be empty or contain only whitespace")

    with st.form("delete_customer"):
        delete_id = st.number_input("Customer ID to Delete", min_value=1, step=1)
        submitted = st.form_submit_button("Delete Customer")
        if submitted:
            delete_customer(delete_id)
            st.rerun()

# Product Section
if table == "Product":
    st.header("Products")
    df = fetch_data("Product")
    if not df.empty:
        st.dataframe(df)
    else:
        st.write("No products found")

    with st.form("add_product"):
        name = st.text_input("Product Name")
        price = st.text_input("Price")
        if st.form_submit_button("Add Product"):
            if name and price:
                add_product(name, price)
                st.rerun()
            else:
                st.warning("Please fill all fields")

    with st.form("update_product"):
        product_id = st.number_input("Product ID to Update", min_value=1, step=1)
        update_name = st.text_input("New Product Name")
        update_price = st.text_input("New Price")
        if st.form_submit_button("Update Product"):
            if update_name and update_price:
                update_product(product_id, update_name, update_price)
                st.rerun()
            else:
                st.warning("Please fill all fields")

    with st.form("delete_product"):
        delete_id = st.number_input("Product ID to Delete", min_value=1, step=1)
        if st.form_submit_button("Delete Product"):
            delete_product(delete_id)
            st.rerun()

# Invoice Section
if table == "Invoice":
    st.header("Invoices")
    df = fetch_data("Invoice")
    if not df.empty:
        st.dataframe(df)
    else:
        st.write("No invoices found")

    with st.form("add_invoice"):
        customer_id = st.number_input("Customer ID", min_value=1, step=1)
        product_id = st.number_input("Product ID", min_value=1, step=1)
        quantity = st.number_input("Quantity", min_value=1, step=1)
        if st.form_submit_button("Add Invoice"):
            if customer_id and product_id and quantity:
                add_invoice(customer_id, product_id, quantity)
                st.rerun()
            else:
                st Siegfried

# Customer Invoice Details
if table == "Customer Invoices":
    st.header("Customer Invoice Details")
    session = Session()
    try:
        invoices = session.query(Invoice).join(Customer).join(Product).all()
        details = [
            {
                'Customer ID': inv.customer.id,
                'Customer Name': f"{inv.customer.first_name} {inv.customer.last_name}",
                'Product': inv.product.name,
                'Price': inv.product.price,
                'Quantity': inv.quantity,
                'Total': inv.product.price * inv.quantity
            } for inv in invoices
        ]
        if details:
            st.dataframe(pd.DataFrame(details))
            import plotly.express as px
            fig = px.bar(details, x='Customer Name', y='Total', title="Invoice Totals by Customer",
                         color_discrete_sequence=['#4e73df'])
            st.plotly_chart(fig)
        else:
            st.write("No invoice details found")
    finally:
        session.close()