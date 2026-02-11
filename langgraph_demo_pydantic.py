from datetime import date
import re

from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field, field_validator, model_validator

try:
    # New API (recommended): moved from LangGraph to LangChain.
    from langchain.agents import create_agent
except ImportError:
    create_agent = None
    from langgraph.prebuilt import create_react_agent


load_dotenv()


class PayrollQueryInput(BaseModel):
    department: str = Field(..., description="Department name, e.g. Sales")
    month: str = Field(..., description="Explicit month name, e.g. January")

    @field_validator("department", mode="before")
    @classmethod
    def normalize_department(cls, value: str) -> str:
        clean = str(value).strip()
        clean = re.sub(r"(?i)\s+department$", "", clean)
        return clean.title()

    @field_validator("month", mode="before")
    @classmethod
    def normalize_month(cls, value: str) -> str:
        clean = str(value).strip().replace(",", " ")
        parts = clean.split()
        if parts:
            first = parts[0].title()
            if first in {
                "January", "February", "March", "April", "May", "June",
                "July", "August", "September", "October", "November", "December",
            }:
                return first
        return clean.title()

    @model_validator(mode="after")
    def reject_relative_months(self):
        if self.month.lower() in {"last month", "previous month", "this month", "current month"}:
            raise ValueError(
                "Relative month not accepted. Use CurrentDate first and convert to an explicit month name."
            )
        return self


@tool("CurrentDate")
def get_current_date() -> str:
    """Return today's date in ISO format (YYYY-MM-DD)."""
    return date.today().isoformat()


def get_payroll_expense(department: str, month: str):
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
    return payroll_db.get(department, {}).get(month)


@tool("PayrollQuery", args_schema=PayrollQueryInput)
def payroll_query(department: str, month: str) -> str:
    """Return payroll expense value for a department and explicit month name."""
    amount = get_payroll_expense(department, month)
    if not amount:
        return f"No payroll data found for department={department}, month={month}."
    return amount


system_prompt = (
    "You are a careful payroll assistant.\n"
    "If the user asks with relative dates like 'last month', call CurrentDate first.\n"
    "Then convert relative date to an explicit month name and call PayrollQuery.\n"
    "Do not call PayrollQuery with relative dates."
)

llm = ChatOpenAI(model="gpt-4", temperature=0)
if create_agent is not None:
    try:
        agent = create_agent(
            model=llm,
            tools=[get_current_date, payroll_query],
            system_prompt=system_prompt,
        )
    except TypeError:
        agent = create_agent(
            model=llm,
            tools=[get_current_date, payroll_query],
            prompt=system_prompt,
        )
else:
    agent = create_react_agent(
        model=llm,
        tools=[get_current_date, payroll_query],
        prompt=system_prompt,
    )


if __name__ == "__main__":
    query = "What was the total payroll expense for the Sales department last month?"
    result = agent.invoke({"messages": [("user", query)]})
    if isinstance(result, dict) and "messages" in result:
        final_message = result["messages"][-1]
        print(getattr(final_message, "content", final_message))
    else:
        print(result)
