from utils import file_controller
from dao import user_dao
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
        user_dao.user_info['id'] = username
        if file_controller.check_file_exist(username):
            user_dao.user_info['first_login'] = 1
        else:
            file_controller.creste_user_file(user_dao.user_info)

        return render_template('problem_library.html', username=username)
