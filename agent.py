from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from model import PersonalDetails

load_dotenv()

llm = ChatOpenAI(temperature=0, model="gpt-4o-2024-08-06")
# chain = llm.with_structured_output(PersonalDetails)

