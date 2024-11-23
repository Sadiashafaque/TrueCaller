Spam Caller || DJANGO Backend Project A trulecaller like API written in Django REST framework.

Steps to run the API

Install dependencies pip3 install -r requirements.txt

Migrations

python manage.py makemigrations python manage.py migrate

Populate dummy data for all tables python manage.py populate_db

Runserver python manage.py runserver 8000

Test the API

Route: http://localhost:8000/signup/ Request Type: POST Data: { "user": { "username": "sadiass", "password": "testpassword" }, "phone": 9908464343, "email": "ssss@example.com", "spam": false } Route: http://localhost:8000/login/ Request Type: POST Data:

{
    "username":"sadiass",
    "password":"testpassword"
}
JWT AUTH You will receive a JWT Auth Token after signUp and signIn. Include the JWT token in headers as a Token for all private requests

Authorization: Token 98002dd40f5039263fdf024ffce7aa421008a107

To add contact to current user Public Route: http://127.0.0.1:8000/contacts/ Request Type: POST Data: { "name": "joseph osk", "phone": 87276985326781, "spam": false, "email": "j.d@example.com" }

To view all contacts of current user Public Route: http://127.0.0.1:8000/contacts/ Request Type: GET

To mark a contact as SPAM Private Route: http://127.0.0.1:8000/spam/ Request Type: POST Data: { "phone_number" : 5709372156 }

To view all spam numbers Private Route: http://127.0.0.1:8000/spam/ Request Type: GET

To search a contact by name Private Route: http://127.0.0.1:8000/searchname/ Request Type: GET Data: { "name" : "Richard Manning" }

To search a contact by phone Private Route: http://127.0.0.1:8000/searchnumber/ Data: { "phone_number" : 127143192192005 } Request Type: GET

FIND THE SCREENSHOTS OF ALL THE API CALLS IN THE POSTMAN SCREENSHOTS FOLDER.
