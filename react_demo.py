from dotenv import load_dotenv
from datetime import date
from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool

try:
    # LangChain versions where legacy agents are still exposed here
    from langchain.agents import initialize_agent, AgentType
except ImportError:
    # LangChain v1+: legacy agent API moved to langchain_classic
    from langchain_classic.agents import initialize_agent, AgentType

# Load environment variables from .env (e.g. OPENAI_API_KEY)
load_dotenv()

# 1. Define the tools the agent can use
def get_current_date():
    today = date.today()
    return today.isoformat()


def get_payroll_expense(dept: str, month: str):
    # In a real scenario, this would query a SQL DB or API
    return "$142,500"

payroll_tool = Tool(
    name="PayrollQuery",
    func=lambda q: get_payroll_expense("Sales", "January"),
    description="Useful for finding payroll and expense data by department and month."
)

current_date_tool = Tool(
    name="CurrentDate",
    func=lambda _: get_current_date(),
    description="Returns today's date in ISO format (YYYY-MM-DD). Use this to resolve relative dates like 'last month'."
)

# 2. Initialize the LLM and Agent
llm = ChatOpenAI(model="gpt-4", temperature=0)
tools = [current_date_tool, payroll_tool]

agent = initialize_agent(
    tools, 
    llm, 
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, 
    verbose=True # This shows the "Thought/Action/Observation" logs
)

# 3. Run the query
agent.invoke("What was the total payroll expense for the Sales department last month?")
