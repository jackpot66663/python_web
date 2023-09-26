import datetime


def creste_user_file(username):
    with open('user_log/'f'{username}.txt', 'w') as f:
        f.write('std_id: '+username+'\n' +
                'create_time: '+str(datetime.datetime.today()))
