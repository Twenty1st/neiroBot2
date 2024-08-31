from langchain.agents import Tool
from langchain.agents import AgentType
from langchain.prompts import PromptTemplate
from langchain.agents import initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
import vars

llm = ChatOpenAI(openai_api_key=vars.openai_api, temperature=0, model="gpt-3.5-turbo-0613")

with open("product.txt", "r", encoding="utf-8") as file:
    products = file.read()

analise_msg = PromptTemplate(
    input_variables=["client_message"],
    template="""You are an observer, you check the message: {client_message}, if it looks like
the customer is interested in buying the product, then you return the product name""",
)
analise_chain = LLMChain(llm=llm, prompt=analise_msg, output_key="text")

check_product = PromptTemplate(
    input_variables=["product"],
    template="you check the availability of this product: {product} or similar products in the base: "+ products+", "
                      "return full descriptions for this product"
)
check_chain = LLMChain(llm=llm, prompt=check_product, output_key="text")

tools1 = [
    Tool(
        name = "diagnostic",
        func= analise_chain,
        description="used for message analysis"
    )
]
tools2 = [
    Tool(
        name = "check",
        func= check_chain,
        description="used for check product in base"
    )
]
agent1 = initialize_agent(tools=tools1, llm=llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True, max_iterations=6)
agent2 = initialize_agent(tools=tools2, llm=llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

# Функция для обработки сообщения клиента
def check_client_message(message):
    analise = agent1.run(message)
    otvet = agent2.run(analise)
    return otvet




