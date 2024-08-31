from langchain.agents import Tool
from langchain.agents import AgentType
from langchain.prompts import PromptTemplate
from langchain.agents import initialize_agent
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
import vars
from langchain.schema import (
    SystemMessage
)

openai_api_key=vars.openai_api

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
llm = ChatOpenAI(openai_api_key=openai_api_key, temperature=0.1, model="gpt-3.5-turbo-0613")

with open("product.txt", "r", encoding="utf-8") as file:
    products = file.read()

product_prompt = PromptTemplate(
    input_variables=["message"],
    template="write a text in Russian, tell about the product that interested the client according to the description {message}, "
             "but we have these products "+products
)
product_chain = LLMChain(llm=llm, prompt=product_prompt, output_key="text")


selling_prompt = PromptTemplate(
    input_variables=["message"],
    template= "Write a text in Russian, you want to offer products that interested the customer according to "
              "the description {message}, we have these products "+products
)
selling_chain = LLMChain(llm=llm, prompt=selling_prompt, output_key="text")

chat_prompt = PromptTemplate(
    input_variables=["message"],
    template="Write a text to reply to the client in an official tone in Russian from the description of {message},"
             " you did not understand what he wants"
)
chat_chains = LLMChain(llm=llm, prompt=selling_prompt, output_key="text")

ok_prompt = PromptTemplate(
    input_variables=["client_message"],
    template= "Write the text in an official tone in Russian to thank the customer for the purchase"
)
ok_chain = LLMChain(llm=llm, prompt=selling_prompt, output_key="text")

tools = [
    Tool(
        name = "about product",
        func= product_chain,
        description="useful for when you need tell about product"
    ),
    Tool(
        name="sell product",
        func=selling_chain,
        description="useful when a customer wants to buy a product"
    ),
    Tool(
        name="just chating",
        func=chat_chains,
        description="useful for those cases when you did not understand the client's question "
    ),
    Tool(
        name="deal is done",
        func=chat_chains,
        description="useful for those cases when the customer has agreed to buy the product "
    )
]

messages = [
    SystemMessage(content="You're a smart sales consultant"),
]

agent = initialize_agent(tools=tools, llm=llm, agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION, verbose=True, memory=memory, messages=messages)

# Функция для обработки сообщения клиента
def handle_client_message(message):
   return agent.run(message)





