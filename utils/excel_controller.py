import csv
from openpyxl import load_workbook




def excel_search(data):
    old_problems = {}
    category = data['Category']
    keywords = data['Keyword']
    keywords.sort()
    keyword_s = ""
    
    for i in range(0,len(keywords)):
        keyword_s += keywords[i]
        if i != len(keywords)-1:
            keyword_s+=","
            
    print(category)
    print(keyword_s)
    wb = load_workbook('staticFiles/uploads/old_problem_db_1.xlsx')
    ws = wb.active
    for row in ws.rows:
        if row[0].value==category:
            if row[1].value ==keyword_s:
                old_problems['description'] = row[2].value
                old_problems['solution'] = row[3].value
        
    
    # with open('staticFiles/uploads/old_problem_db_1.csv','r',encoding='utf-8') as e:
    #     reader = csv.reader(e)
        
    #     for row in reader:
    #         if category in row:
    #             if keyword_s in row:
    #                 old_problems.append(row)
    #         print(row)
    #     e.close()
    keyword_s = ""
    return old_problems

def excel_write(data):
    with open('staticFiles/uploads/old_problem_db_1.csv','a',encoding='utf-8') as e:
        writer = csv.writer(e)
        # print(data)
        pro = data['Problem_Description'].replace("<br>","\n")
        list = [data['Category'],data['Keywords'],pro,data['Solution'],data['Hint']]
        writer.writerow(list)
        e.close()

    
    
