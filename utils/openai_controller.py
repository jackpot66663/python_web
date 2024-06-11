from openai import OpenAI

client = OpenAI()

user_message = {}

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
    # print(type(response))
    # print(type(response.choices[0]))
    # print(type(response.choices[0].message))
    # print(type(response.choices[0].message.content))
    return response.choices[0].message.content

def prompt_message(data):
    
    global user_message 
    if data['Mode'] == 1:
        user_message['new_question_input'] = data['Input']
        user_message['new_question_output'] = data['Output']
        user_message['new_question'] = data['Problem_n']
        user_message['sample_input'] = data['S_input']
        user_message['sample_input'] = data['S_output']
        user_message['parameter_declaration'] = data['Parameters']
        user_message['process'] = data['Category']
        user_message['Hint'] = data['Hint']
    else:
        user_message['new_question_input'] = data['Input']
        user_message['new_question_output'] = data['Output']
        user_message['new_question'] = data['Problem_n']
        user_message['sample_input'] = data['S_input']
        user_message['sample_input'] = data['S_output']
        user_message['parameter_declaration'] = data['Parameters']
        user_message['process'] = data['Category']
        user_message['old_question'] = data['Problem_o']
        user_message['old_question_solution'] = data['Solution']
        user_message['Hint'] = data['Hint']
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
    "code_solution":<the code answer of the new question>
    "relation":<relation between old problem and new problem>
    
    The following rules you must to follow:
    1.New question description can be found in user_message["new_question"].
    2.The new problem must be solved according to the given user_message["process"] way,also the parameter declaration must use the given user_message['parameter_declaration'] if given.
    3.Whatever question you solve,try use function or library that has been used in old question solution to solve new question. 
    4.The solution must adhere to the input-output examples that can be found in user_message["sample_input"] and user_message["sample_output"].
    5.If there is given user_message['Hint'],you must reference to solve question.
    6.Test input must use user_message["sample_input"]

    Only output the json, with nothing else.
    Output language must be traditional chinese.
    Make sure follow the above rules.
"""

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
