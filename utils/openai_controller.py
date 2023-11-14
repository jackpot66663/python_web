from openai import OpenAI

client = OpenAI(
    api_key = "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"
)


def get_completion_from_messages(messages, 
                                 model="gpt-3.5-turbo", 
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
    
    messages =  [  
        {'role':'system', 
        'content': system_message},    
        {'role':'user', 
        'content': f"{delimiter}{user_message}{delimiter}"},  
    ]
    # print(messages)
    
    return get_completion_from_messages(messages)


delimiter = "####"
system_message = f"""
    You will be provided with user question json. \
    The user question json will be delimited with \
    {delimiter} characters.
    Output a python json, where json has the following format:
    "new_solution": <the solution of the new question>
    "relation":<the comparison between new question and old question>,

    the new question description and old question solution can be found in user_message json
    Solve new question with the given old question solution


    Only output the json, with nothing else
"""
user_message = {
    "new_question":"",
    "old_question":"",
    "old_question_solution":""
}

