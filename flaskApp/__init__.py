from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '2116ecc90bebada37c62ff7655a46b52dc58f364ae36948f6849d61307dd8cbb781656ff6322c4f918ad09d63dfcec21366cef777bf287be4a1772368d16b33f'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)


from flaskApp import routes
