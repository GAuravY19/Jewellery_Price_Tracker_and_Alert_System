from flaskApp import db, login_manager, app
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer as Serial

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    image_file = db.Column(db.String(60), nullable=False, default = 'default.jpg')
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User : {self.username}, {self.email}, {self.image_file}"

