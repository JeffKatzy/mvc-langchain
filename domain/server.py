import asyncio

from domain.models.part import GeneralResponse, Part
from domain.prompt import general_message_prompt
from domain.store import get_session_history
from lib.agent import invoke_message_from
from lib.model_updater import merge, parse_details


class Server:
    def __init__(self, workflows):
        self.workflows = workflows

    def current_workflow(self):
        return self.workflows[-1]
    
    async def stream_content(self, system_prompt, message_text):
        async for chunk in invoke_message_from(system_prompt, message_text):
            print(chunk, end="", flush=True)

    def route_from(self, text_input):
        output_json = parse_details(text_input, [Part, GeneralResponse])[0]
        if output_json['type'] == 'GeneralResponse':
            asyncio.run(self.stream_content(general_message_prompt, text_input))
        else:
            workflow = self.current_workflow()
            workflow._model = merge(workflow.model, output_json['args'])
            message_text = workflow.get_next_message() or "Thank the user for the session."
            asyncio.run(self.stream_content(workflow.prompt(), message_text))

    def listen(self):
        ai_text = "Hey there."
        print(ai_text)
        while True:
            text_input = input("\n\nMe: ")
            print("\nBot:")
            ai_text = self.route_from(text_input)

    def log(self):
        history = get_session_history(**{"user_id": "123", "conversation_id": "1"})
        print(history.messages[-2:])