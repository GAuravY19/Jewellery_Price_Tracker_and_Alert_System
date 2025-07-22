from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = '2116ecc90bebada37c62ff7655a46b52dc58f364ae36948f6849d61307dd8cbb781656ff6322c4f918ad09d63dfcec21366cef777bf287be4a1772368d16b33f'

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

@app.route('/login')
def login():
    return render_template('login.html', title = 'Sign In')

@app.route('/register')
def register():
    return render_template('register.html')

# @app.route('/logout')
# def logout():
#     return render_template('logout.html', title = 'Logout')

