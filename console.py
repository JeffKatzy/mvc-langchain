from form_checker import (build_general_message, build_next_message_for,
                          get_next_step_for)
from model import IFSPart
from obj_updater import merge, parse_details
from router import build_route_layer
from store import get_session_history


class WorkflowRunner():
    def __init__(self, obj):
        self.obj = obj
        
    def get_next_message(self):
        next_step = get_next_step_for(self.obj)
        ai_response = build_next_message_for(next_step)
        return ai_response

    def get_general_message(self):
        return build_general_message()
        


class Server:
    def __init__(self):
        # self.categorize = build_route_layer()
        self.workflow_runners = [WorkflowRunner(IFSPart())]

    def current_workflow(self):
        return self.workflow_runners[-1]

    def listen(self):
        ai_text = "Hey there."
        while True:
            self.log()
            text_input = input(ai_text)
            ai_text = self.route_from(text_input)
            
    def route_from(self, text_input):
        output_json = parse_details(text_input)[0]

        if output_json['type'] == 'GeneralResponse':
            ai_message = build_general_message(text_input)
            return ai_message.content
        else:
            self.workflow_runner = self.current_workflow()
            current_obj = self.workflow_runner.obj
            self.workflow_runner.obj = merge(current_obj, output_json['args'])
            ai_message = self.workflow_runner.get_next_message()
            return ai_message.content

    def log(self):
        history = get_session_history(**{"user_id": "123", "conversation_id": "1"})
        print(history.messages[-2:])

server = Server()
server.listen()

    

# next_step = get_next_step()
# while next_step:
    # get_ai_prompt (render)
    # get_ai_response
        # user_input
        # route_to
    # update_state()
    # get_next_step()