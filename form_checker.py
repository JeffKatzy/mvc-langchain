


from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from agent import llm
from model import PersonalDetails


def get_missing_attrs(obj):
    if next_field := obj.get_next_field():
        return obj.render(next_field)

def ask_for_info(ask_for = ['name','age', 'location']):
    first_prompt = ChatPromptTemplate.from_template(
        """Below is are some things to ask the user for in a coversation way.
        You should only ask one question at a time even 
        if you don't get all the info don't ask as a list!
        Don't greet the user! Don't say Hi.
        Explain you need to get some info.
        If the ask_for list is empty then 
        thank them and ask how you can help them \n\n
        ### ask_for list: {ask_for}"""
    )
    info_gathering_chain = first_prompt | llm
    ai_chat = info_gathering_chain.invoke({'ask_for': ask_for})
    return ai_chat


