"""
Agent for XBRL tagging operations.
"""

from pydantic_ai import Agent, Tool
from pydantic_ai.models.openai import OpenAIModel
import os

from .models import PartialXBRLWithTags
from .system_prompts import XBRL_DATA_TAGGING_PROMPT
from .dependencies import XBRLTaxonomyDependencies

# Import the enhanced tools
from .tools import (
    apply_tags_to_element,
    tag_statement_section,
    create_context_info, 
    # validate_tagged_data,
    batch_tag_elements
)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

tagging_model = OpenAIModel(model_name="gpt-4o", api_key=OPENAI_API_KEY)

# Define the agent with dependencies and register tools
xbrl_tagging_agent = Agent(
    model=tagging_model,
    result_type=PartialXBRLWithTags,
    system_prompt=XBRL_DATA_TAGGING_PROMPT,
    deps_type=XBRLTaxonomyDependencies,
    retries=10,
    tools=[
        Tool(apply_tags_to_element, takes_ctx=True),
        Tool(tag_statement_section, takes_ctx=True),
        Tool(create_context_info, takes_ctx=True),
        # Tool(validate_tagged_data, takes_ctx=True),
        Tool(batch_tag_elements, takes_ctx=True)
    ]
)