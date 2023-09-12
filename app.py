from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import MySQLdb.cursors
import re
import hashlib

app = Flask(__name__)


app.secret_key = ''

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '610520Jjkk++'
app.config['MYSQL_DB'] = 'pythonlogin'

# Intialize MySQL
mysql = MySQL(app)


@app.route('/')
def home():
    return redirect(url_for('login'))


@app.route("/python_web", methods=['GET'])
def login():
    return render_template('index.html')
