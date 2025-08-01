from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskApp.models import User
from flask_login import current_user

class RegistrationForm(FlaskForm):
    username = StringField('Username: ',
                           validators=[DataRequired(), Length(min=6, max=20)])
    email = StringField('Email: ',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password: ',
                             validators=[DataRequired(), Length(min=10)])
    confirm_password = PasswordField('Confirm Password: ', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()

        if user:
            print("Validation Error")
            raise ValidationError('Username already exists!')


    def validate_email(self, email):
        check_email = User.query.filter_by(email = email.data).first()

        if check_email:
            raise ValidationError('Email already exists!')


class LoginForm(FlaskForm):
    email = StringField('Email: ',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password: ',
                             validators=[DataRequired(), Length(min=10)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class EditForm(FlaskForm):
    username = StringField('Username: ',
                           validators=[DataRequired(), Length(min=6, max=20)])
    email = StringField('Email: ',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Update Profile')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username = username.data).first()

            if user:
                raise ValidationError('Username already exists')


    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email = email.data).first()

            if email:
                raise ValidationError('Email Already exists')
