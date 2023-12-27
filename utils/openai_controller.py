from openai import OpenAI

client = OpenAI()


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
#"modification":<provide a little part of code or function that will be modified according to the old question solution >
system_message = f"""
    You are a teaching assistant.\
    You will be provided with user question json. \
    The user question json will be delimited with \
    {delimiter} characters.
    Output a python json, where json has the following format:
    "instruction": <generate a solving steps description array of the new question>
    "relation":<the comparison between new question and old question>,

    New question description and old question solution can be found in user_message json
    Analyze new question with the given old question solution
    Whatever question you solve,try use the function or library that has been used in old question solution 
    But don't output code directly


    Only output the json, with nothing else
    Output language must be traditional chinese.
"""
user_message = {
    "new_question":"",
    "old_question":"",
    "old_question_solution":""
}

