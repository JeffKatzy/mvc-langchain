import json

from langchain.output_parsers import PydanticOutputParser
from langchain.output_parsers.openai_tools import JsonOutputToolsParser
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import ConfigurableFieldSpec
from langchain_core.runnables.history import RunnableWithMessageHistory

from agent import llm
from model import GeneralResponse, IFSPart
from store import get_session_history


def merge(current_details, new_details):
    non_empty_details = {k: v for k, v in new_details.items() if v not in [None, ""]}
    updated_details = current_details.copy(update=non_empty_details)
    return updated_details

def parse_details(text_input):
    parser = JsonOutputToolsParser()
    # parser = PydanticOutputParser()
    prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are here to parse part information someone providing IFS therapy information.  
            If they are providing part information use the IFSPart. 
            If you feel you do not have the information, do not guess, just leave it blank.
            If the user asks a question about IFS, or does not answer the question, use the
            GeneralResponse object to parse.
            Do not use the IFSPart parser if you are unsure.  We can always ask the user for more clarification.
            """,
        ),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ])
    # catch user responses that dont need parsing with GeneralResponse
    
    runnable = prompt | llm.bind_tools([IFSPart, GeneralResponse], tool_choice="any")
    # potentially use create react agent
    # https://python.langchain.com/v0.1/docs/modules/agents/how_to/handle_parsing_errors/
    runnable_with_history = RunnableWithMessageHistory(
        runnable,
        get_session_history,
        input_messages_key="input",
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
    chain = runnable_with_history | parser
    runnable_res = runnable_with_history.invoke(
        {"input": text_input},
        config={"configurable": {"user_id": "123", "conversation_id": "1"}}
    )
    add_tool_message(runnable_res)
    return parser.invoke(runnable_res)

def add_tool_message(runnable_res):
    tool_call = runnable_res.tool_calls[0]
    content = json.dumps(runnable_res.tool_calls[0]['args'])
    tool_message = ToolMessage(content = content,
                    tool_call_id = tool_call['id'])
    history = get_session_history(**{"user_id": "123", "conversation_id": "1"})
    
    history.messages.append(tool_message)
