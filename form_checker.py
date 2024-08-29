
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import ConfigurableFieldSpec
from langchain_core.runnables.history import RunnableWithMessageHistory

from agent import llm
from model import GeneralResponse, IFSPart
from prompt import general_message_prompt
from store import get_session_history


async def invoke_message_from(prompt, input_message):
        chain = build_message_chain(prompt, "input")
        str_chain = chain | StrOutputParser()
        async for chunk in str_chain.astream(
            {"input": input_message},
            config={"configurable": {"user_id": "123", "conversation_id": "1"}}):
            yield chunk

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

