import json
import os


def check_file_exist(username):
    exist = False
    dir_path = r'C:\Users\Jackpot\graduate_paper\python_web\user_log'
    filename = str(username)+'.txt'
    for path in os.listdir(dir_path):
        # print(os.path.basename(path))
        if os.path.basename(path) == filename:
            exist = True
    return exist

def get_user_file(username):
    user_str =""
    with open('user_log/'f'{username}.txt', 'r') as f:
        user_str = f.read()
        f.close()
    return json.loads(user_str)

def create_user_file(user):
    user = json.loads(user)
    username = user["name"]
    with open('user_log/'f'{username}.txt', 'w') as f:
        query = json.dumps(user)
        print(query)
        f.write(query)
        f.close()

def update_user_file(user):
    user = json.loads(user)
    username = user["name"]
    with open('user_log/'f'{username}.txt', 'w') as f:
        query = json.dumps(user)
        f.write(query)
        f.close()

