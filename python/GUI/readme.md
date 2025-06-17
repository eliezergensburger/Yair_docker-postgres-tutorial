# תצוגת נתונים עם  SQLAlchemy ו Tkinter (או Streamlit).  

## תיאור

הקובץ מכיל קוד ב-Python המציג נתונים מטבלת `students` בבסיס נתונים PostgreSQL באמצעות Tkinter ו-SQLAlchemy.

## דרישות מקדימות

1. התקנת Python (גרסה 3.7 ומעלה מומלצת).
2. התקנת חבילות נדרשות באמצעות pip:
   ```sh
   pip install tkinter sqlalchemy psycopg2
   ```
3. התקנת והפעלת שרת PostgreSQL עם מסד נתונים ושם משתמש תואם למוגדר בקובץ (`DATABASE_URL`).
4. לוודא שקיימת טבלה בשם `students` המכילה נתונים לתצוגה.

## מבנה הקוד

1. **חיבור לבסיס הנתונים:**

   - מוגדר באמצעות SQLAlchemy על ידי יצירת מנוע (`engine`).

2. **פונקציות עזר:**

   - `format_date(value)`: פורמט לתאריכים כך שיוצגו בתצורה `YYYY-MM-DD`.
   - `fetch_data()`: פונקציה זו מתחברת לבסיס הנתונים, מריצה שאילתת SQL לשליפת כל הנתונים מהטבלה `students`, ומחזירה את שמות העמודות ואת הנתונים כמאגר רשומות.
   - `display_data()`: פונקציה זו יוצרת חלון Tkinter, מציגה בו טבלת `ttk.Treeview`, ומטעינה אליו את הנתונים שהוחזרו מהפונקציה `fetch_data`. כמו כן, היא מטפלת בפורמט תאריכים ובשגיאות בזמן הכנסת נתונים לתצוגה.

3. **תצוגת הנתונים:**

   - `display_data()`: מציגה את הנתונים בחלון Tkinter באמצעות `ttk.Treeview`.

## הפעלת הקוד

להרצת הקובץ:

```sh
python simple_gui.py
```

## הערות

- יש לוודא שהחיבור לבסיס הנתונים פעיל ושיש הרשאות מתאימות למשתמש.
- אם מתרחשת שגיאה בעת הכנסת נתונים לרכיב התצוגה, השגיאה תודפס במסוף.

### for streamlit install the following

```sh
pip install streamlit pandas sqlalchemy psycopg2-binary plotly
```

and then type from the GUI folder

```sh
streamlit run .\streamlit_app.py
```

