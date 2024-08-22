from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import ConfigurableFieldSpec
from langchain_core.runnables.history import RunnableWithMessageHistory

from agent import llm
from model import PersonalDetails
from store import get_session_history


def update_from(text_input, current_obj):
    new_obj = parse_details(text_input)
    merged_obj = add_non_empty_details(current_obj, new_obj)
    return merged_obj

def add_non_empty_details(current_details: PersonalDetails, new_details: PersonalDetails):
    non_empty_details = {k: v for k, v in new_details.dict().items() if v not in [None, ""]}
    updated_details = current_details.copy(update=non_empty_details)
    return updated_details

def parse_details(text_input):
    if not text_input: return PersonalDetails()
    parser = PydanticOutputParser(pydantic_object=PersonalDetails)
    format_instructions = parser.get_format_instructions()
    prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Parse the user information.  If you feel you do not have the information, do not guess, just leave it blank.",
        ),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}\n{format_instructions}"),
    ])
    runnable = prompt | llm

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
    res = chain.invoke(
        {"input": text_input, "format_instructions": format_instructions},
        config={"configurable": {"user_id": "123", "conversation_id": "1"}}
    )
    return res
