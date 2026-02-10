from dotenv import load_dotenv
from datetime import date
import json
import re
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
    return date.today().isoformat()


def get_payroll_expense(dept: str, month: str):
    # Simulated payroll table (in production this would come from DB/API)
    payroll_db = {
        "Sales": {
            "January": "$142,500",
            "February": "$149,200",
            "March": "$151,000",
        },
        "Engineering": {
            "January": "$310,000",
            "February": "$319,400",
            "March": "$321,100",
        },
        "Finance": {
            "January": "$98,300",
            "February": "$101,000",
            "March": "$102,700",
        },
    }
    return payroll_db.get(dept, {}).get(month)


def resolve_month(month_raw: str) -> str:
    value = month_raw.strip().lower()
    return month_raw.strip().title()


def parse_payroll_input(action_input: str):
    department = None
    month = None

    # Expected format (preferred): {"department":"Sales","month":"January"}
    try:
        payload = json.loads(action_input)
        if isinstance(payload, dict):
            department = payload.get("department") or payload.get("dept")
            month = payload.get("month")
    except json.JSONDecodeError:
        pass

    # Fallback for free-text inputs
    if not department:
        dept_match = re.search(r'(?i)(?:department|dept)\s*[:=]\s*"?([a-zA-Z ]+)"?', action_input)
        if dept_match:
            department = dept_match.group(1).strip().title()
    if not month:
        month_match = re.search(r'(?i)month\s*[:=]\s*"?([a-zA-Z ]+)"?', action_input)
        if month_match:
            month = month_match.group(1).strip()

    return department, month


def payroll_query(action_input: str):
    department, month = parse_payroll_input(action_input)
    if not department or not month:
        return "Invalid input. Use JSON with keys 'department' and 'month'."

    raw_month = month.strip().lower()
    if raw_month in {"last month", "previous month", "this month", "current month"}:
        return (
            "Relative month not accepted. "
            "Use CurrentDate first and convert to an explicit month name."
        )

    canonical_month = resolve_month(month)
    amount = get_payroll_expense(department, canonical_month)
    if not amount:
        return f"No payroll data found for department={department}, month={canonical_month}."

    # Return only the value to keep the tool output realistic and minimal.
    return amount

payroll_tool = Tool(
    name="PayrollQuery",
    func=payroll_query,
    description=(
        "Returns payroll expense value for a department and month. "
        "Accepts only explicit month names (e.g., January, February, March). "
        "If the question has relative dates like 'last month', call CurrentDate first, "
        "convert to an explicit month, then call PayrollQuery."
    ),
)

current_date_tool = Tool(
    name="CurrentDate",
    func=lambda _: get_current_date(),
    description="Returns today's date in ISO format (YYYY-MM-DD). Use this to resolve relative dates like 'last month'."
)

# 2. Initialize the LLM and Agent
llm = ChatOpenAI(model="gpt-4", temperature=0)
tools = [current_date_tool, payroll_tool]
agent_prefix = (
    "You are a careful payroll assistant.\n"
    "Important rule: if the user asks using relative dates like "
    "'last month', 'previous month', 'this month', or 'current month', "
    "you must call CurrentDate first.\n"
    "After getting today's date, convert the relative date to an explicit "
    "month name, then call PayrollQuery.\n"
    "Do not call PayrollQuery with relative dates."
)

agent = initialize_agent(
    tools, 
    llm, 
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, 
    agent_kwargs={"prefix": agent_prefix},
    verbose=True # This shows the "Thought/Action/Observation" logs
)

# 3. Run the query
query = "What was the total payroll expense for the Sales department last month?"

def extract_output(value):
    if isinstance(value, dict):
        return value.get("output", str(value))
    return str(value)


try:
    response = agent.invoke({"input": query})
except Exception:
    try:
        response = agent.invoke(query)
    except Exception:
        response = agent.run(query)

print(extract_output(response))
