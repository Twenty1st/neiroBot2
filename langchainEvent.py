from langchain.agents import Tool
from langchain.agents import AgentType
from langchain.prompts import PromptTemplate
from langchain.agents import initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
import vars

openai_api_key=vars.openai_api

with open("product.txt", "r", encoding="utf-8") as file:
    products = file.read()

llm = ChatOpenAI(openai_api_key=openai_api_key, temperature=0.2, model="gpt-3.5-turbo-0613")

kp_prompt=PromptTemplate(
    input_variables=["product", "user"],
    template="write a simple text of 70 words in a formal tone in Russian"
             " for the user {user}, making him interested in buying our product {product}"
)

kp_chain = LLMChain(llm=llm, prompt=kp_prompt, output_key="text")

tools = [
    Tool(
        name = "create kp",
        func= kp_chain,
        description="useful for drawing up a commercial offer"
    )
]

agent = initialize_agent(tools=tools, llm=llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True, max_iterations=4)


def KP_create(product, user_name):
    resp = kp_chain({"product":product, "user":user_name})
    return resp
