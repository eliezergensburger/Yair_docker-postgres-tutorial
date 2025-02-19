# מדריך עבודה עם בסיס נתונים PostgreSQL באמצעות Docker.


## התקנה

1. הורד והתקן את Docker Desktop:
   - [Docker Desktop](https://www.docker.com/)

## שימוש ב־Volumes
השימוש ב Volumes מספק דרך אמינה לאחסן נתונים, אפילו אם הקונטיינר נמחק.


צור Volume לדאטה:

```bash
docker volume create mydbdata
```

## הפעלת PostgreSQL עם ה־volume

הפעל את הקונטיינר עם ה־volume החדש:

```bash
docker run -d --name my_postgres \
  -e POSTGRES_USER=myuser \
  -e POSTGRES_PASSWORD=mypassword \
  -e POSTGRES_DB=mydatabase \
  -v mydbdata:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres
```

### הסבר על הפקודות:

הרצת הקונטיינר והפעלתו כשרת בסיס נתונים דורשת מספר משתני סביבה, שם משתמש וסיסמא, ושם עבור בסיס הנתונים, ניתן לקבוע כרצונכם

- `-e POSTGRES_USER=myuser` – יוצר משתמש חדש עבור PostgreSQL.
- `-e POSTGRES_PASSWORD=mypassword` – מגדיר את הסיסמה למשתמש.
- `-e POSTGRES_DB=mydatabase` – יוצר מסד נתונים עם השם שצוין.
- `-v mydbdata:/var/lib/postgresql/data` – שומר את הנתונים של PostgreSQL בווליום `mydbdata`, כך שהם לא ימחקו כאשר הקונטיינר נמחק.
- `-p 5432:5432` – ממפה את הפורט 5432 של הקונטיינר לפורט 5432 של המחשב המארח.



## הרצת pgAdmin עם Docker

1. **משוך את הImage של pgAdmin**

```bash
docker pull dpage/pgadmin4
```

2. **הרץ את הקונטיינר עם pgAdmin**

```bash
docker run -d --name pgadmin \
  -p 5050:80 \
  -e PGADMIN_DEFAULT_EMAIL=admin@example.com \
  -e PGADMIN_DEFAULT_PASSWORD=admin123 \
  -v pgadmin_data:/var/lib/pgadmin \
  dpage/pgadmin4
```

### הסבר על הפקודות:

- `-e PGADMIN_DEFAULT_EMAIL=admin@example.com` – מגדיר את כתובת האימייל להתחברות ל־pgAdmin.
- `-e PGADMIN_DEFAULT_PASSWORD=admin123` – מגדיר את סיסמת ההתחברות.
- `-v pgadmin_data:/var/lib/pgadmin` – שומר את הנתונים של pgAdmin בווליום `pgadmin_data`.
- `-p 5050:80` – ממפה את הפורט 80 של הקונטיינר לפורט 5050 של המחשב המארח כדי שניתן יהיה לגשת ל־pgAdmin דרך הדפדפן בכתובת `http://localhost:5050`.

ניתן לקבוע את שמות משתני הסביבה

## מציאת כתובת הip של הקונטיינר שמריץ את השרת

כדי שנוכל להתחבר לשרת אנחנו צריכים את כתובת הip שלו בתוך הרשת הפנימית שdocker מנהל
לכל קונטיינר יש מזהה ייחודי, נריץ את פקודת inspect אם המזהה הייחודי או אם שם הקונטיינר

```bash
docker inspect my_postgres
```
נוכל לראות את הערך של IPADDRESS

## הוספת שרת ה־PostgreSQL ב־pgAdmin

1. פתח את pgAdmin בדפדפן:

   - [http://localhost:5050](http://localhost:5050)

2. התחבר עם הפרטים הבאים (או הפרטים שהגדרת):

   - **Email**: `admin@example.com`
   - **Password**: `admin123`

3. לחץ על **Add New Server**.

4. עבור ללשונית **General**:

   - **Name**: PostgreSQL Server (או שם אחר לבחירתך).

5. עבור ללשונית **Connection**:

   - **Host**: כתובת הip של הקונטיינר שמריץ את השרת.
   - **Port**: `5432`.
   - **Username**: `myuser` (או מה שהגדרת).
   - **Password**: `mypassword`.
   - **Save Password?** ✔️

6. לחץ על **Save**.
   -[https://www.docker.com/blog/how-to-use-the-postgres-docker-official-image/]

   ![database connection](https://github.com/yair-go/docker-postgres-tutorial/blob/main/database%20connection.png)




