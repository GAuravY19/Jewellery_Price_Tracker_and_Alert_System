from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return '<h1>About Page</h1>'

@app.route('/data')
def data():
    return "<h1>Data Page</h1>"

@app.route('/analytics')
def analytics():
    return "<h1>Analytics Page</h1>"

