from form_checker import ask_for_info, get_missing_attrs
from model import PersonalDetails
from obj_updater import update_from

# user_details, ask_for = filter_response(text_input, user_details)

# user_details = PersonalDetails()


class Server():
    def __init__(self, obj):
        self.obj = obj
        
    def listen(self):
        missing_attrs = get_missing_attrs(self.obj)
        while missing_attrs:
            ai_response = ask_for_info(missing_attrs)
            text_input = input(ai_response.content)
            self.obj = update_from(text_input, self.obj)
            missing_attrs = get_missing_attrs(self.obj)
        else:
            print('Everything gathered move to next phase')

user_details = PersonalDetails()
server = Server(user_details)
server.listen()