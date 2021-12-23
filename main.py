from flask import Flask, jsonify
from flask_jwt_extended import JWTManager

import config
from db import engine
from models import Base
import views

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = config.SECRET_KEY
jwt = JWTManager(app)


@app.errorhandler(404)
def not_found(error):
    return jsonify(msg='Not found.'), 404


@app.errorhandler(405)
def not_found(error):
    return jsonify(msg='The method is not allowed for the requested URL.'), 405


@app.errorhandler(500)
def not_found(error):
    return jsonify(msg='Something went wrong'), 500


app.add_url_rule('/api/v1/login/', view_func=views.login, methods=('POST',))
app.add_url_rule('/api/v1/registration/', view_func=views.registration, methods=('POST',))
app.add_url_rule('/api/v1/my-user/', view_func=views.MyUserView.as_view('my user'))
app.add_url_rule('/api/v1/my-products/', view_func=views.MyProductsView.as_view('my products'))

app.add_url_rule('/media/<model_name>/images/<name>', endpoint="images", build_only=True)

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    app.run()
