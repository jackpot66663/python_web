from utils import file_controller
from utils import openai_controller
from utils import excel_controller
from dao.user_dao import User
from flask import Flask, render_template, request, redirect, url_for, session,jsonify
import pandas as pd
import os
from fileinput import filename
from werkzeug.utils import secure_filename
import numpy as np
import json
import datetime



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
        if file_controller.check_file_exist(username):
            user_dict = file_controller.get_user_file(username)
            user_info = User(user_dict)
            user_info.first_login = False
            user_info.cur_login = str(datetime.datetime.today())
            user_json = user_info.toJSON()
            file_controller.update_user_file(user_json)
            session['user'] = user_json
            return render_template('welcome_user.html', user=json.loads(user_json))
        else:
            user_info = User()
            user_info.name = username
            user_info.first_login = True
            user_info.create_time = str(datetime.datetime.today())
            user_info.cur_login = str(datetime.datetime.today())
            user_json = user_info.toJSON()
            file_controller.create_user_file(user_json)
            session['user'] = user_json
            return render_template('welcome_user.html', user=json.loads(user_json))
   

@app.route("/select",methods=['GET', 'POST'])
def import_csv():
    user_json = session['user']
    if request.method == 'POST':
        #
        # f = request.files.get('file')
        # data_filename = secure_filename(f.filename)

        # f.save(os.path.join(app.config['UPLOAD_FOLDER'],data_filename))

        # session['uploaded_data_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'],data_filename)
        # print(session)
        # # user_dao.user_info['uploads'] = True
        # # Uploaded File Path
        # data_file_path = session.get('uploaded_data_file_path', None)
        # # read csv
        # uploaded_df = pd.read_csv(data_file_path,encoding='utf-8')
        # # Converting to html Table
        # uploaded_df_html = uploaded_df.to_html()
        return render_template('select.html',user=json.loads(user_json),data_var=uploaded_df_html)
    elif request.method == "GET":
        
        return render_template('select.html',user=json.loads(user_json))


@app.route("/topic_1",methods=['GET', 'POST'])
def prompt_build():
    
    cols = ['Category','Keywords','Problem_Description','Solution','Hint','Prompt','IAO']
    df = pd.read_csv('staticFiles/uploads/old_problem_db_1.csv',encoding='utf-8',usecols=cols,dtype={'Category':str,'Keywords':str,'Problem_Description':str,'Solution':str,'Hint':str,'Prompt':str,'IAO':str})
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

    return render_template('topic_1.html',problems=df_n,categorys = categorys,keywords = keywords)

@app.route("/topic_1_extend",methods=['GET', 'POST'])
def prompt_build_extend():
    cols = ['Category','Keywords','Problem_Description','Solution','Hint','Prompt','IAO']
    df = pd.read_csv('staticFiles/uploads/old_problem_db_1.csv',encoding='utf-8',usecols=cols,dtype={'Category':str,'Keywords':str,'Problem_Description':str,'Solution':str,'Hint':str,'Prompt':str,'IAO':str})
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

    return render_template('topic_1_e.html',problems=df_n,categorys = categorys,keywords = keywords)


ans = ""
problem = ""
mode = 0
@app.route("/result",methods=['GET', 'POST'])
def result():
    if request.method=="POST":
        data = request.get_json()
        global mode
        mode= data['Mode']
        global problem
        problem = data['Problem_n']
        result = openai_controller.prompt_message(data)
        global ans 
        ans = result
        session['prompt'] = data
        # print(result)
        return jsonify(result)
    elif request.method == "GET":
        ans = json.loads(ans)
        problem = problem.replace("<br>","\n")
        return render_template('result_pre.html',ans = ans,problem = problem,mode = mode)
    

@app.route("/search",methods=['GET', 'POST'])
def search():
    if request.method=="POST":
        data = request.get_json()
        global k
        global c
        c=data['Category']
        k=data['Keyword']
        search = excel_controller.excel_search(data)
        return jsonify(search)

@app.route("/try",methods=['GET','POST'])
def modify():
    if request.method == "GET":
        prompt = session['prompt']
        print(prompt)
        prompt['Problem_n'] = prompt['Problem_n'].replace("<br>","\n")
        prompt['Solution'] = prompt['Solution'].replace("<br>","\n")
        return render_template('try.html',prompt = prompt)


# gpt = ""
# @app.route("/next",methods=['GET', 'POST'])
# def next():
#     generate_set=""
#     if request.method=="POST":
        
#         data = request.get_json()
#         data['Category'] = c
#         data['Keywords'] = k
        
#         excel_controller.excel_write(data)
#         #要gpt生成新題目
#         indexing = {
#             "Category":c,
#             "Keyword":k,
#         }
#         search = excel_controller.excel_search(indexing)
#         # print(search)
#         # print(123)
#         generate_set = openai_controller.prompt_message_test(search)
#         global gpt
#         gpt = generate_set
#         # print(generate_set)
#         return jsonify(generate_set)
#     elif request.method == "GET":
#         gpt = json.loads(gpt)
#         # gpt['question'].replace("\n","<br>")
#         print(gpt['question'])
#         print(gpt['solution'])
#         return render_template('next.html',gpt = gpt)

if __name__ == "__main__":

    app.run()
    
             