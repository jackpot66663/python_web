import datetime
import json
import os


def check_file_exist(username):
    exist = False
    dir_path = r'C:\Users\Jackpot\graduate_paper\python_web\user_log'
    filename = str(username)+'.txt'
    for path in os.listdir(dir_path):
        print(os.path.basename(path))
        if os.path.basename(path) == filename:
            exist = True
    return exist


def creste_user_file(user):
    username = user['id']
    user['create_time'] = str(datetime.datetime.today())
    with open('user_log/'f'{username}.txt', 'w') as f:
        query = json.dumps(user)
        f.write(query)
