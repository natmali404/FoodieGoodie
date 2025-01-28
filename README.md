# FoodieGoodie
 A project to practice usecase implementation.

## Database setup
In pgAdmin, create a database (eg. FoodieGoodie) and remember the credentials to use in .env file

## Installation
1. Download repository
2. Open the project in VS Code
3. Create a virtual environment
```
python -m venv venv
```
4. Activate the environment
```
venv\Scripts\activate
```
5. Install requirements while in venv
```
pip install -r requirements.txt
```
6. If no database, create it in pgAdmin and run migrations
```
py manage.py makemigrations
py manage.py migrate
py manage.py seed_database
```
7. If first launch, create the .env file in the project directory and update it with your database credentials:
```
DB_NAME=FoodieGoodie
DB_USER=postgres
DB_PASSWORD=postgres
```
8. Start the project
```cd foodie_goodie```
```py manage.py runserver```
