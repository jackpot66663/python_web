from utils import file_controller
from flask import Flask, render_template, request, redirect, url_for, session


app = Flask(__name__)


# app.secret_key = ''

# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = '610520Jjkk++'
# app.config['MYSQL_DB'] = 'pythonlogin'

# Intialize MySQL
# mysql = MySQL(app)


@app.route('/')
def home():
    return redirect(url_for('login'))


@app.route("/python_web")
def login():
    return render_template('index.html')


@app.route("/problem_library", methods=['GET', 'POST'])
def problem_library():
    if request.method == 'POST':
        username = request.form['username']
        file_controller.creste_user_file(username)
        return render_template('problem_library.html', username=username)
