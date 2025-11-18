from dotenv import load_dotenv

load_dotenv()

from langchain_classic import hub
from langchain_classic.agents import AgentExecutor
from langchain_classic.agents.react.agent import create_react_agent
from langchain_core.output_parsers.pydantic import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch

from prompt import REACT_PROMPT_WITH_FORMAT_INSTRUCTIONS
from schemas import AgentResponse

tools = [TavilySearch()]
llm = ChatOpenAI(model="gpt-4")
react_prompt = hub.pull("hwchase17/react")

# Output parser object
output_parser = PydanticOutputParser(pydantic_object=AgentResponse)

# Langchain PromptTemplate object
react_prompt_with_format_instructions = PromptTemplate(
    template=REACT_PROMPT_WITH_FORMAT_INSTRUCTIONS,
    input_variables=["input", "agent_scratchpad", "tool_names"],
).partial(format_instructions=output_parser.get_format_instructions())

# Create agent
agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=react_prompt_with_format_instructions,
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
extract_output = RunnableLambda(lambda x: x["output"])
parse_output = RunnableLambda(lambda x: output_parser.parse(x))

# Pipe everything together
# The agent_executor will run the agent, use the given tools, and output a response of the agent of type dictionary
# The extract_output will extract the output field from the agent's response
# The extracted string then be passed to the parse_output, which will parse it into a Pydantic object
chain = agent_executor | extract_output | parse_output

# When run chain.invoke, it's going to run the compose chain on the input query, and return the parsed structured response.


# This script uses LangChain to create an agent that searches for job postings
def main():
    result = chain.invoke(
        input={
            "input": "Search for 3 job posings for an AI Engineer using langchain in Vietnam on LinkedIn and list their details."
        }
    )
    print(result)


if __name__ == "__main__":
    main()
