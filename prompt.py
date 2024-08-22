from langchain.prompts import ChatPromptTemplate, PromptTemplate

first_prompt = ChatPromptTemplate.from_template(
        "Below is are some things to ask the user for in a coversation way. you should only ask one question at a time even if you don't get all the info \
        don't ask as a list! Don't greet the user! Don't say Hi.Explain you need to get some info. If the ask_for list is empty then thank them and ask how you can help them \n\n \
        ### ask_for list: {ask_for}"
    )
