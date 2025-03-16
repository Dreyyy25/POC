"""
Financial statement mapping agent implementation.
"""
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
import os

from .models import PartialXBRL
from .dependencies import FinancialTermDeps, financial_deps
from .system_prompts import FINANCIAL_STATEMENT_PROMPT
from .tools import match_financial_term, extract_and_categorize_financial_data, MatchTermContext, ExtractContext

# Get OpenAI API key from environment
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

# Initialize the OpenAI model
mapping_model = OpenAIModel(model_name="gpt-4o", api_key=OPENAI_API_KEY)

# Define the agent with dependencies
financial_statement_agent = Agent(
    model=mapping_model,
    result_type=PartialXBRL,
    system_prompt=FINANCIAL_STATEMENT_PROMPT,
    deps_type=FinancialTermDeps,
    retries=3
)

# Register tools with the agent
@financial_statement_agent.tool
def match_financial_term(context, term, statement_type="all"):
    from .tools import match_financial_term as mft
    return mft(context, term, statement_type)

@financial_statement_agent.tool
def extract_and_categorize_financial_data(context, data, field_path=""):
    from .tools import extract_and_categorize_financial_data as ecfd
    return ecfd(context, data, field_path)
