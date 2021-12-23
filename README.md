# Products API Server

Task here -> ___

Frameworks:

* [Flask](https://flask.palletsprojects.com/)
* [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/)
* [SQLAlchemy](https://www.sqlalchemy.org/)

Clone a project and move to it:

    $ git clone https://github.com/Kouff/products-api.git
    $ cd products-api

Create a [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html#via-pip)
and [activate](https://virtualenv.pypa.io/en/latest/user_guide.html#activators) it and install the requirements:

    $ pip install -r requirements.txt

Create .env file from .env.example and add virtual environments in it. 

Migrate:

    $ python create_db_tables.py

Run the server (gunicorn does not work on Windows OS):

    $ gunicorn --bind 0.0.0.0:5000 main:app

Run the server on Windows OS (for testing):

    $ python main.py

### Registration:
POST /api/v1/registration/ - Registration / Create a new user.

### Token:
POST /api/v1/login/ - Get JWT.

### Users:
GET /api/v1/my-user/ - Show the current user;

PATCH /api/v1/my-user/ - Edit the current user.

### Products:
GET /api/v1/my-products/ - Show products of the current user;

POST /api/v1/my-products/ - Create a new product;

GET /api/v1/my-products/{id}/ - Show a product with prices;

PATCH /api/v1/my-products/{id}/ - Edit a product.

### Prices:
POST /api/v1/my-products/{id}/prices/ - Create a new price to the product.
