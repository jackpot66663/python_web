import json


class User():
    name = ""
    first_login =True
    create_t = ""
    cur_login = ""
    topic_1_start = ""
    topic_1_finish = "" 

    def __init__(self,dict_object=None):
        if dict_object != None:
            for key in dict_object:
                setattr(self,key,dict_object[key])
        else:
            pass

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)


        
