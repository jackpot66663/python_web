import csv


old_problems = []


def excel_search(data):
    category = data['Category']
    keyword = data['Keyword']
    with open('staticFiles/uploads/old_problem_db_1.csv','r',encoding='utf-8') as e:
    # with open('staticFiles/uploads/old_problem_db.csv','r',encoding='utf-8') as e:
        reader = csv.reader(e)
        for row in reader:
            if category and keyword in row:
                old_problems.append(row)
        e.close()
    return old_problems

def excel_write(data):
    with open('staticFiles/uploads/old_problem_db_1.csv','a',encoding='utf-8') as e:
        writer = csv.writer(e)
        # print(data)
        pro = data['Problem_Description'].replace("<br>","\n")
        list = [data['Category'],data['Keywords'],pro,data['Solution'],data['Hint']]
        writer.writerow(list)
        e.close()

    
    
