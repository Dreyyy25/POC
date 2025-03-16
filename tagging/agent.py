"""
Agent for XBRL tagging operations.
"""
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
import os

from .models import PartialXBRLWithTags
from .system_prompts import XBRL_DATA_TAGGING_PROMPT
from .dependencies import XBRLTaxonomyDependencies

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

tagging_model = OpenAIModel(model_name="gpt-4o", api_key=OPENAI_API_KEY)

# Define the agent with dependencies
xbrl_tagging_agent = Agent(
    model=tagging_model,
    result_type=PartialXBRLWithTags,
    system_prompt=XBRL_DATA_TAGGING_PROMPT,
    deps_type=XBRLTaxonomyDependencies,
    retries=5,
)