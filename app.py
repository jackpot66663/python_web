from utils import file_controller
from utils import openai_controller
from utils import excel_controller
from dao import user_dao
from flask import Flask, render_template, request, redirect, url_for, session,jsonify
import pandas as pd
import os
from fileinput import filename
from werkzeug.utils import secure_filename
import numpy as np
import json


UPLOAD_FOLDER = os.path.join('staticFiles', 'uploads')
 
# Define allowed files
ALLOWED_EXTENSIONS = {'csv'}


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'jackpot6666'




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
        # print(user_dao.user_info['id'])
        f = request.files.get('file')
        data_filename = secure_filename(f.filename)

        f.save(os.path.join(app.config['UPLOAD_FOLDER'],data_filename))

        session['uploaded_data_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'],data_filename)
        
        user_dao.user_info['uploads'] = True
        # Uploaded File Path
        data_file_path = session.get('uploaded_data_file_path', None)
        # read csv
        uploaded_df = pd.read_csv(data_file_path,encoding='utf-8')
        # Converting to html Table
        uploaded_df_html = uploaded_df.to_html()
        return render_template('db_import.html',user=user_dao.user_info,data_var=uploaded_df_html)
    return render_template('db_import.html',user=user_dao.user_info)

@app.route("/prompt_build",methods=['GET', 'POST'])
def prompt_build():
    cols = ['Category','Keywords','Problem_Description','Solution']
    df = pd.read_csv(session['uploaded_data_file_path'],encoding='utf-8',usecols=cols,dtype={'Category':str,'Keywords':str,'Problem_Description':str,'Solution':str})
    # for index,row in df.iterrows():
    #     problem_dao.problems_set.append(row)
    # print(problem_dao.problems_set)
    df_n = df.to_json(orient='index')
    problem_dict = json.loads(df_n)
    categorys = set()
    keywords = set()
    for problem in problem_dict:
        categorys.add(problem_dict[problem]['Category'])
        t = problem_dict[problem]['Keywords']
        tarray = t.split(',')
        for i,keyword in enumerate(tarray):
            keywords.add(keyword)

    return render_template('prompt_build.html',problems=df_n,categorys = categorys,keywords = keywords)
ans = ""
@app.route("/result",methods=['GET', 'POST'])
def result():
    if request.method=="POST":
        data = request.get_json()
        result = openai_controller.prompt_message(data)
        global ans 
        ans = result
        print(result)
        return jsonify(result)
    elif request.method == "GET":
        ans = json.loads(ans)
        # print(ans)
        # print(ans['new_solution'])
        return render_template('result.html',ans = ans)
    

@app.route("/search",methods=['GET', 'POST'])
def search():
    if request.method=="POST":
        data = request.get_json()
        search = excel_controller.excel_search(data)
        return jsonify(search)

@app.route("/next",methods=['GET', 'POST'])
def next():
    if request.method=="GET":
        return render_template('next.html',)

if __name__ == "__main__":
    app.run()
             