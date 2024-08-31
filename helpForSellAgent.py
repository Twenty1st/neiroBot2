from langchain.agents import Tool
from langchain.agents import AgentType
from langchain.prompts import PromptTemplate
from langchain.agents import initialize_agent
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
import chatModelAgent as chatAgent
import vars

with open("product.txt", "r", encoding="utf-8") as file:
    products = file.read()

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
llm = ChatOpenAI(openai_api_key=vars.openai_api, temperature=0, model="gpt-3.5-turbo-0613")

product_prompt = PromptTemplate(
    input_variables=["client_message"],
    template="write a text-description in russian language of what the customer wants from the message {client_message}"
)
product_chain = LLMChain(llm=llm, prompt=product_prompt, output_key="text")

product_check = PromptTemplate(
    input_variables=["client_message"],
    template="you check whether the necessary data: {client_message} is in the database: "+products
)
check_chain = LLMChain(llm=llm, prompt=product_check, output_key="text")


tools = [
    Tool(
        name = "diagnostic",
        func= product_chain,
        description="used for message analysis"
    )
]

agent = initialize_agent(tools=tools, llm=llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

# Функция для обработки сообщения клиента
def check_client_message(message):
    otvet = agent.run(message)
    ret= chatAgent.handle_client_message(otvet)
    return ret





