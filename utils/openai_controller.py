from openai import OpenAI

client = OpenAI()

input_ac = {
    "int_s":"整數，單行輸入",
    "int_m":"整數，多行輸入",
    "s_s":"字串，單行輸入",
    "s_m":"字串，多行輸入",
    "l_s_s":"列表，單行輸入，元素為字串",
    "l_s_int":"列表，單行輸入，元素為整數",
}

output_ac = {
    "int":"印出指定整數結果",
    "str":"印出指定整數結果",
}

def get_completion_from_messages(messages, 
                                 model="gpt-4-0613", 
                                 temperature=0, 
                                 max_tokens=500):
    
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature, 
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content

def prompt_message(data):
    
    global user_message 
    input = input_ac[data['Input']]
    output = output_ac[data['Output']]
    print(input+output)
    user_message['new_question_input'] = input
    user_message['new_question_output'] = output
    user_message['new_question'] = data['Problem_n']
    user_message['old_question'] = data['Problem_o']
    user_message['old_question_solution'] = data['Solution']
    # print(user_message)
    messages =  [  
        {'role':'system', 
        'content': system_message},    
        {'role':'user', 
        'content': f"{delimiter}{user_message}{delimiter}"},  
    ]
    
    return get_completion_from_messages(messages)


delimiter = "####"

system_message = f"""
    You are a teaching assistant.\
    You will be provided with user question json. \
    The user question json will be delimited with \
    {delimiter} characters.
    Output a python json, where json has the following format:
    "code_solution":<the code answer of the new question>,
    "relation":<the comparison between new question and old question>,
    "instruction": <generate steps explanation array of the code_solution>
    

    New question description and old question solution can be found in user_message["new_question"] and user_message["old_question"]
    Analyze new question with the given old question solution
    Whatever question you solve,try use the function or library that has been used in old question solution 
    Beware of the input and output format of the new_question,format that can be found in user_message["new_question_input"] and user_message["new_question_output"]


    Only output the json, with nothing else
    Output language must be traditional chinese.
"""
user_message = {
    "new_question_input":"",
    "new_question_output":"",
    "new_question":"",
    "old_question":"",
    "old_question_solution":""
}

#################################################################

# user_message_m ={
#     "Category":"",
#     "Keywords":"",
#     "Questions":[],
# }

# def prompt_message_test(data):
    
#     global user_message_m
#     user_message_m['Category'] = data[0][0]
#     user_message_m['Keywords'] = data[0][1]
#     question = {
#         "old_question":"",
#         "old_question_solution":""
#     }
#     for d in data:
#         question['old_question'] = d[2]
#         question['old_question_solution']=d[3]
#         user_message_m['Questions'].append(question)

#     # print(user_message_m)

#     messages =  [  
#         {'role':'system', 
#         'content': system_message_m},    
#         {'role':'user', 
#         'content': f"{delimiter}{user_message_m}{delimiter}"},  
#     ]
    
#     return get_completion_from_messages(messages)

# system_message_m = f"""
#     You are a teaching assistant.\
#     You will be provided with user question json. \
#     The user question json will be delimited with \
#     {delimiter} characters.
#     Output a python json, where json has the following format:
#     "question": <generate a new question according to the given old_question,if there are two or more samples,combine both and generate it>
#     "solution": <generate solution that corresponds to the new question>,

#     Old question description and solution can be found in user_message_m json
#     Don't output code directly


#     Only output the json, with nothing else
#     Output language must be traditional chinese.
# """
