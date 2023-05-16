from flask import Flask
from flask import render_template
app = Flask(__name__)


@app.route("/")
def home():
    return 'hello flask'


@app.route("/hello")
def hello():
    return render_template('hello.html')
