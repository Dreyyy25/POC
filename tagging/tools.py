"""
Tools for the financial statement tagging agent.
"""
from typing import Dict, Any, List, Union, Optional
from datetime import date
from pydantic import BaseModel, Field
from pydantic_ai import RunContext

from .dependencies import XBRLTaxonomyDependencies

# Tagging apply_tags_to_element tool
def apply_tags_to_element(
    context: RunContext[XBRLTaxonomyDependencies],
    element_name: str,
    value: Any,
    statement_type: str,
    is_instant: bool = True
) -> Dict[str, Any]:
    """
    Apply appropriate XBRL tags to a financial element
    
    Args:
        context: Runtime context containing taxonomy dependencies
        element_name: The name of the financial element to tag
        value: The value of the element
        statement_type: Type of statement (filing, balance_sheet, income_statement, etc.)
        is_instant: Whether the element is an instant (point-in-time) value
        
    Returns:
        Dictionary containing the tagged value and metadata
    """
    tags = []
    messages = []
    
    # Find tags for the element name
    if element_name in context.deps.field_tags:
        tags = context.deps.field_tags[element_name]
        messages.append(f"Found exact tag match for {element_name}")
    else:
        messages.append(f"No exact tag match found for {element_name}")
        # Try finding similar tags for fuzzy matching
        for field_name, field_tags in context.deps.field_tags.items():
            # Simple substring matching - could be improved with better algorithms
            if element_name.lower() in field_name.lower() or field_name.lower() in element_name.lower():
                tags = field_tags
                messages.append(f"Using similar tag: {field_name}")
                break
    
    # Check if it's a mandatory field
    is_mandatory = False
    if element_name in context.deps.mandatory_fields:
        is_mandatory = context.deps.mandatory_fields[element_name]
        if is_mandatory:
            messages.append(f"Note: {element_name} is a mandatory field")
    
    # Create response
    result = {
        "element_name": element_name,
        "value": value,
        "tags": [tag.dict() for tag in tags],  # Convert tags to dict for JSON serialization
        "is_mandatory": is_mandatory,
        "messages": messages,
    }
    
    return result

# Tagging create_context_info tool
def create_context_info(
    context: RunContext[XBRLTaxonomyDependencies],  # Add this as first parameter
    entity_name: str,
    entity_identifier: str,
    period_end: date,
    period_start: Optional[date] = None,
    is_consolidated: bool = False,
    dimensions: Dict[str, str] = None
) -> Dict[str, Any]:
    """
    Create XBRL context information for a set of related elements
    
    Args:
        context: Runtime context containing taxonomy dependencies
        entity_name: Name of the reporting entity
        entity_identifier: Unique identifier of the entity (UEN)
        period_end: End date of the reporting period
        period_start: Start date of the reporting period (for duration contexts)
        is_consolidated: Whether the context is for consolidated statements
        dimensions: Additional dimensions for the context
        
    Returns:
        Dictionary containing context information
    """
    # Create a unique context ID based on parameters
    period_part = f"i{period_end.strftime('%Y%m%d')}" if period_start is None else \
                  f"d{period_start.strftime('%Y%m%d')}to{period_end.strftime('%Y%m%d')}"
    
    context_id = f"ctx_{period_part}_{'c' if is_consolidated else 's'}"
    
    # Add dimension information if provided
    if dimensions:
        dim_parts = []
        for dim_name, dim_value in sorted(dimensions.items()):
            dim_parts.append(f"{dim_name}-{dim_value}")
        if dim_parts:
            context_id = f"{context_id}_{'_'.join(dim_parts)}"
    
    # Create context object
    context_info = {
        "id": context_id,
        "entity": {
            "name": entity_name,
            "identifier": entity_identifier
        },
        "period": {
            "end_date": period_end.isoformat()
        },
        "is_consolidated": is_consolidated
    }
    
    if period_start is not None:
        context_info["period"]["start_date"] = period_start.isoformat()
    
    if dimensions:
        context_info["dimensions"] = dimensions
    
    return context_info

# Tagging tag_statement_section tool
def tag_statement_section(
    context: RunContext[XBRLTaxonomyDependencies],
    section_name: str,
    section_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Apply tags to an entire statement section
    
    Args:
        context: Runtime context containing taxonomy dependencies
        section_name: Name of the section (e.g., "filingInformation", "statementOfFinancialPosition")
        section_data: Dictionary of data for the section
        
    Returns:
        Dictionary with tagged section data
    """
    tagged_section = {"meta_tags": []}
    
    # Find section-level abstract tags
    for tag in context.deps.statement_tags:
        if section_name.lower() in tag.element_name.lower():
            tagged_section["meta_tags"].append(tag.dict())
    
    # Tag individual elements
    for element_name, element_value in section_data.items():
        # Skip processing of lists/dicts - they would be handled separately
        if isinstance(element_value, (list, dict)):
            continue
            
        # Find matching tags
        tags = []
        if element_name in context.deps.field_tags:
            tags = context.deps.field_tags[element_name]
        
        tagged_section[element_name] = {
            "value": element_value,
            "tags": [tag.dict() for tag in tags]
        }
    
    return tagged_section

# Tagging validate_tagged_data tool
def validate_tagged_data(
    context: RunContext[XBRLTaxonomyDependencies],
    tagged_data: Dict[str, Any]
) -> List[Dict[str, str]]:
    """
    Validate the tagged data for completeness and correctness
    
    Args:
        context: Runtime context containing taxonomy dependencies
        tagged_data: Complete set of tagged financial data
        
    Returns:
        List of validation issues found
    """
    issues = []
    
    # Check for missing mandatory fields
    for field_name, is_mandatory in context.deps.mandatory_fields.items():
        if is_mandatory:
            field_found = False
            
            # Search through all sections for the field
            for section_name, section_data in tagged_data.items():
                if isinstance(section_data, dict) and field_name in section_data:
                    field_found = True
                    break
            
            if not field_found:
                issues.append({
                    "type": "missing_mandatory_field",
                    "field": field_name,
                    "message": f"Mandatory field '{field_name}' is missing from the tagged data"
                })
    
    # Check for fields without tags
    for section_name, section_data in tagged_data.items():
        if isinstance(section_data, dict):
            for field_name, field_data in section_data.items():
                if isinstance(field_data, dict) and "tags" in field_data and not field_data["tags"]:
                    issues.append({
                        "type": "missing_tags",
                        "section": section_name,
                        "field": field_name,
                        "message": f"No tags applied to field '{field_name}' in section '{section_name}'"
                    })
    
    return issues