import asyncio

from form_checker import invoke_message_from
from model import IFSPart, IFSWorkflow
from obj_updater import merge, parse_details
from prompt import general_message_prompt
from store import get_session_history


class Server:
    def __init__(self, workflows):
        self.workflows = workflows

    def current_workflow(self):
        return self.workflows[-1]
    
    async def stream_content(self, system_prompt, message_text):
        chunks = []
        async for chunk in invoke_message_from(system_prompt, message_text):
            chunks.append(chunk)
            print(chunk, end="", flush=True)

    def route_from(self, text_input):
        output_json = parse_details(text_input)[0]
        if output_json['type'] == 'GeneralResponse':
            asyncio.run(self.stream_content(general_message_prompt, text_input))
        else:
            workflow = self.current_workflow()
            current_model = workflow.model
            workflow._model = merge(current_model, output_json['args'])
            message_text = workflow.get_next_prompt()
            asyncio.run(self.stream_content(workflow.prompt(), message_text))

            

    def listen(self):
        ai_text = "Hey there."
        print(ai_text)
        while True:
            text_input = input("\n\nMe: ")
            print("\nBot:")
            ai_text = self.route_from(text_input)

    # def log(self):
    #     history = get_session_history(**{"user_id": "123", "conversation_id": "1"})
    #     print(history.messages[-2:])

workflows = [ IFSWorkflow(IFSPart()) ]
server = Server(workflows)
server.listen()

    

# next_step = get_next_step()
# while next_step:
    # get_ai_prompt (render)
    # get_ai_response
        # user_input
        # route_to
    # update_state()
    # get_next_step()