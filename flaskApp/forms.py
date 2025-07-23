from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskApp.models import User

class RegistrationForm(FlaskForm):
    Username = StringField('Username: ',
                           validators=[DataRequired(), Length(min=6, max=20)])

    email = StringField('Email: ',
                        validators=[DataRequired(), Email()])

    password = PasswordField('Password: ',
                             validators=[DataRequired(), Length(min=10)])

    confirm_password = PasswordField('Confirm Password: ', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')


    def validate_username(self, Username):
        user = User.query.filter_by(username = Username.data).first()

        if user:
            raise ValidationError('Username Already exists')

    def validate_email(self, email):
        email = User.query.filter_by(email = email.data)

        if email:
            raise ValidationError('Email Already exists')


class LoginForm(FlaskForm):
    email = StringField('Email: ',
                        validators=[DataRequired(), Email()])

    password = PasswordField('Password: ',
                             validators=[DataRequired(), Length(min=10)])

    remeber = BooleanField('Remember Me')

    submit = SubmitField('Sign In')
