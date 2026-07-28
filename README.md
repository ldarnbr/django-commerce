# E-Commerce RESTful Web API & CLI Client

## Project Description
This is an interactive command line interface built with Python and the requests library. The back-end RESTful API is built with Django to handle typical online retailer functions such as managing stock, customer registration, product browsing, placing orders and checking order history.

## Setup Instructions
1. Clone the repository to your local machine.
```bash
git clone [https://github.com/ldarnbr/django-commerce.git](https://github.com/ldarnbr/django-commerce.git)
cd <path/to/repo/directory>
```
2. Create a virtual environment to store project dependencies.
```bash
python -m venv venv
```
3. Activate the environment.
```bash
# Windows
venv/Scripts/Activate

# Mac/Linux
source venv/bin/activate
```
4. Install all dependencies.
```bash
pip install -r requirements.txt
```
5. Database setup.
```bash
python manage.py migrate
```
6. Create the Admin account.
```bash
python manage.py createsuperuser
```
7. Run the back-end server.
```bash
python manage.py runserver
```
8. Run the client script.
```bash
# Open a new terminal and type the following command:
python client.py
```
## Admin Site
The admin site can be reached at: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/). This requires
the user to login with the admin credentials that were created during the project setup. To populate the database, navigate 
to the appropriate model table and add entries e.g. adding products to the Items table.
