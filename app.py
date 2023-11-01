from utils import file_controller
from dao import user_dao
from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import os
from fileinput import filename
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = os.path.join('staticFiles', 'uploads')
 
# Define allowed files
ALLOWED_EXTENSIONS = {'csv'}


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'jackpot6666'

if __name__ == "__main__":
    app.run()

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


@app.route("/welcome_user", methods=['GET', 'POST'])
def welcome():
    if request.method == 'POST':
        username = request.form['username']
        user_dao.user_info['id'] = username
        if file_controller.check_file_exist(username):
            user_dao.user_info['first_login'] = False
        else:
            file_controller.creste_user_file(user_dao.user_info)
    print(user_dao.user_info)
    return render_template('welcome_user.html', user=user_dao.user_info)

@app.route("/db_import",methods=['GET', 'POST'])
def import_csv():
    if request.method == 'POST':
        f = request.files.get('file')
        data_filename = secure_filename(f.filename)

        f.save(os.path.join(app.config['UPLOAD_FOLDER'],data_filename))

        session['uploaded_data_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'],data_filename)
        user_dao.user_info['uploads'] = True
        
    return redirect(url_for('welcome'))


@app.route("/show_csv")
def showData():
    # Uploaded File Path
    data_file_path = session.get('uploaded_data_file_path', None)
    # read csv
    uploaded_df = pd.read_csv(data_file_path,encoding='utf-8')
    # Converting to html Table
    uploaded_df_html = uploaded_df.to_html()
    return redirect(url_for('welcome'))           #data_var=uploaded_df_html