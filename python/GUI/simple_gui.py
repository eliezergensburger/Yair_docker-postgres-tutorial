import tkinter as tk
from tkinter import ttk
from sqlalchemy import create_engine, text

from datetime import date

# הגדרת חיבור עם SQLAlchemy
DATABASE_URL = "postgresql://eliezer:admin@localhost:5432/db5785"

# יצירת מנוע SQLAlchemy
engine = create_engine(DATABASE_URL)


def format_date(value):
    if isinstance(value, date):
        return value.strftime("%Y-%m-%d")
    return value


def fetch_data():
    with engine.connect() as connection:
        result = connection.execute(text('SELECT * FROM public.person;'))
        columns = result.keys()  # Get column names
        data = result.fetchall()
        return columns, data


def display_data():
    columns, data = fetch_data()

    window = tk.Tk()
    window.title("Persons Data")

    tree = ttk.Treeview(window, columns=list(columns), show="headings") 
    for col in columns:
        tree.heading(col, text=col)

    for row in data:
        formatted_row = [format_date(value) for value in row]
        try: 
            tree.insert("", "end", values=formatted_row)
        except Exception as e:
            print(f"Error inserting row: {row}")
            print(f"Error: {e}")

    tree.pack()
    window.mainloop()


if __name__ == "__main__":
    display_data()
