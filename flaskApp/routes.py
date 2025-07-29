from flask import redirect, url_for, render_template, flash, request
from flaskApp.forms import RegistrationForm, LoginForm, EditForm
from flaskApp import app, bcrypt, db, login_manager
from flask_login import login_required, login_user, current_user, logout_user
from flaskApp.models import User
import random
import os

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/data')
def data():
    return "<h1>Data Page</h1>"


@app.route('/analytics')
def analytics():
    return "<h1>Analytics Page</h1>"


@app.route('/register', methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        image = os.path.join('D:\Final_Projects\Scraping_Project\Jewellery_Price_Tracker_and_Alert_System\flaskApp\static\images\profilepics', f'default_{int(random.randrange(0,5))}.png')
        user = User(username = form.username.data,
                    email = form.email.data,
                    image_file = image,
                    password = hashed_pw)

        db.session.add(user)
        db.session.commit()

        flash('You Signed up successfully', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', title = 'Sign Up', form = form)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('home'))

        else:
            flash('Login Unsuccessful. Check email and password!', 'danger')

    return render_template('login.html', title = 'Sign In', form = form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/profile', methods = ['GET', 'POST'])
@login_required
def profile():
    return render_template('profile.html', title='Profile Page')

@app.route('/edit', methods = ['GET', 'POST'])
def edit():
    form = EditForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('profile'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    return render_template('edit.html', title='Edit Details', form = form)

