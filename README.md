# FoodieGoodie
 A Django project to practice usecase implementation (a culinary website).

## Screenshots

![obraz](https://github.com/user-attachments/assets/58c2f3de-01e0-4629-86cd-ee527d79f87d)

![obraz](https://github.com/user-attachments/assets/0f581c80-b7cc-4ea7-a7b4-098d4e29d778)

![obraz](https://github.com/user-attachments/assets/70955034-531d-4f8b-9ce2-2e27cafd2c13)

![obraz](https://github.com/user-attachments/assets/c9857ed2-5f97-449c-82ca-f7a34139ed07)



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
