
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import ConfigurableFieldSpec
from langchain_core.runnables.history import RunnableWithMessageHistory

from agent import llm
from model import GeneralResponse, IFSPart
from prompt import general_message_prompt, next_message_prompt
from store import get_session_history


def get_next_step_for(obj):
    if next_field := obj.get_next_field():
        return obj.render(next_field)

def build_next_message_for(next_step = ""):
    next_message_chain = build_message_chain(next_message_prompt, "input")
    res = next_message_chain.invoke(
            {"input": next_step},
            config={"configurable": {"user_id": "123", "conversation_id": "1"}}
    )
    return res

def build_general_message(text_input):
    message_chain = build_message_chain(general_message_prompt, "input")
    res = message_chain.invoke(input = {'input': text_input},
            config={"configurable": {"user_id": "123", "conversation_id": "1"}}
    )
    return res

def build_message_chain(prompt, messages_key):
    info_gathering_chain = prompt | llm
    return RunnableWithMessageHistory(
        info_gathering_chain,
        get_session_history,
        input_messages_key=messages_key,
        history_messages_key="history",
        history_factory_config=[
        ConfigurableFieldSpec(
            id='user_id',
            annotation=str,
            name='User ID',
            description='Unique identifier for the user.',
            default='',
            is_shared=True,
        ),
        ConfigurableFieldSpec(
            id="conversation_id",
            annotation=str,
            name="Conversation ID",
            description="Unique identifier for the conversation.",
            default="",
            is_shared=True,
        ),
        ]
    )

