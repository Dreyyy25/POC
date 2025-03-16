"""
Tools for the financial statement tagging agent.
"""
# Enhanced Tagging tag_statement_section tool with batch processing
import logging

# Add a logger at the top of the file 
logger = logging.getLogger(__name__)

from typing import Dict, Any, List, Union, Optional
from datetime import date
import time
import re
from pydantic import BaseModel, Field
from pydantic_ai import RunContext

from .dependencies import XBRLTaxonomyDependencies

# Tags cache to avoid redundant lookups
_tags_cache = {}

# Tagging apply_tags_to_element tool with enhanced performance
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
    # Check cache first using a compound key
    cache_key = f"{element_name}:{statement_type}"
    if cache_key in _tags_cache:
        cached_result = _tags_cache[cache_key].copy()
        cached_result["value"] = value  # Update with current value
        return cached_result
    
    tags = []
    messages = []
    start_time = time.time()
    
    # Find tags for the element name
    if element_name in context.deps.field_tags:
        tags = context.deps.field_tags[element_name]
        messages.append(f"Found exact tag match for {element_name}")
    else:
        messages.append(f"No exact tag match found for {element_name}")
        # Try finding similar tags for fuzzy matching - optimized version
        element_lower = element_name.lower()
        
        # First try direct substring matches (faster)
        for field_name, field_tags in context.deps.field_tags.items():
            field_lower = field_name.lower()
            if element_lower in field_lower or field_lower in element_lower:
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
        "processing_time_ms": (time.time() - start_time) * 1000
    }
    
    # Store in cache (without the value to save memory)
    cache_entry = result.copy()
    cache_entry.pop("value", None)  # Remove value for caching
    _tags_cache[cache_key] = cache_entry
    
    return result

# Enhanced Tagging tag_statement_section tool with error handling
def tag_statement_section(
    context: RunContext[XBRLTaxonomyDependencies],
    section_name: str,
    section_data: Dict[str, Any],
    use_batch_processing: bool = True
) -> Dict[str, Any]:
    """
    Apply tags to an entire statement section with improved performance
    
    Args:
        context: Runtime context containing taxonomy dependencies
        section_name: Name of the section (e.g., "filingInformation", "statementOfFinancialPosition")
        section_data: Dictionary of data for the section
        use_batch_processing: Whether to use batch processing for better performance
        
    Returns:
        Dictionary with tagged section data
    """
    try:
        start_time = time.time()
        tagged_section = {"meta_tags": []}
        
        # Find section-level abstract tags
        try:
            for tag in context.deps.statement_tags:
                try:
                    if section_name.lower() in tag.element_name.lower():
                        # Use safe dictionary conversion
                        if hasattr(tag, 'dict') and callable(tag.dict):
                            tagged_section["meta_tags"].append(tag.dict())
                        else:
                            # Fallback for objects without dict() method
                            tag_dict = {k: v for k, v in tag.__dict__.items() if not k.startswith('_')}
                            tagged_section["meta_tags"].append(tag_dict)
                except Exception as tag_e:
                    logger.warning(f"Error processing tag in section {section_name}: {str(tag_e)}")
                    continue  # Skip problematic tags
        except Exception as tags_e:
            logger.warning(f"Error accessing statement_tags: {str(tags_e)}")
            # Continue with empty meta_tags
            
        # Determine statement type from section name
        statement_type = "filing"
        section_lower = section_name.lower() if section_name else ""
        if "financial" in section_lower or "position" in section_lower or "balance" in section_lower:
            statement_type = "balance_sheet"
        elif "income" in section_lower or "profit" in section_lower or "loss" in section_lower:
            statement_type = "income_statement"
        elif "cash" in section_lower:
            statement_type = "cash_flow"
        elif "equity" in section_lower or "changes" in section_lower:
            statement_type = "equity"
        elif "director" in section_lower:
            statement_type = "directors"
        elif "audit" in section_lower:
            statement_type = "audit"
        
        # Check if section_data is valid
        if not section_data or not isinstance(section_data, dict):
            logger.warning(f"Invalid section data for {section_name}: {type(section_data)}")
            return {
                "section_name": section_name,
                "error": "Invalid section data",
                "meta_tags": tagged_section["meta_tags"],
                "_performance": {
                    "section_name": section_name,
                    "statement_type": statement_type,
                    "elements_processed": 0,
                    "processing_time_ms": (time.time() - start_time) * 1000,
                    "batch_processing_used": use_batch_processing,
                    "status": "error"
                }
            }
        
        try:
            if use_batch_processing:
                # Batch process simple elements
                simple_elements = {}
                complex_elements = {}
                
                for element_name, element_value in section_data.items():
                    try:
                        if isinstance(element_value, (list, dict)):
                            complex_elements[element_name] = element_value
                        else:
                            simple_elements[element_name] = element_value
                    except Exception as e:
                        logger.warning(f"Error categorizing element {element_name}: {str(e)}")
                        continue
                
                # Process simple elements in a single pass
                if simple_elements:
                    # For each simple element, find tags efficiently
                    for element_name, element_value in simple_elements.items():
                        try:
                            # Skip processing of None values
                            if element_value is None:
                                continue
                                
                            # Get tags (using cache if possible)
                            cache_key = f"{element_name}:{statement_type}"
                            if cache_key in _tags_cache:
                                # Use cached tags
                                cached_entry = _tags_cache[cache_key]
                                tagged_section[element_name] = {
                                    "value": element_value,
                                    "tags": cached_entry.get("tags", []),
                                    "is_mandatory": cached_entry.get("is_mandatory", False)
                                }
                            else:
                                # Find tags for this element
                                tags = []
                                try:
                                    if element_name in context.deps.field_tags:
                                        tags = context.deps.field_tags[element_name]
                                    else:
                                        # Try finding similar tags
                                        element_lower = element_name.lower()
                                        for field_name, field_tags in context.deps.field_tags.items():
                                            try:
                                                field_lower = field_name.lower()
                                                if element_lower in field_lower or field_lower in element_lower:
                                                    tags = field_tags
                                                    break
                                            except Exception:
                                                continue
                                except Exception as tags_e:
                                    logger.warning(f"Error finding tags for {element_name}: {str(tags_e)}")
                                
                                # Convert tags to dict safely
                                tag_dicts = []
                                for tag in tags:
                                    try:
                                        if hasattr(tag, 'dict') and callable(tag.dict):
                                            tag_dicts.append(tag.dict())
                                        else:
                                            # Fallback for objects without dict() method
                                            tag_dict = {k: v for k, v in tag.__dict__.items() 
                                                      if not k.startswith('_')}
                                            tag_dicts.append(tag_dict)
                                    except Exception:
                                        continue
                                
                                # Store in result and cache
                                is_mandatory = False
                                try:
                                    is_mandatory = element_name in context.deps.mandatory_fields and context.deps.mandatory_fields[element_name]
                                except Exception:
                                    pass
                                
                                tagged_section[element_name] = {
                                    "value": element_value,
                                    "tags": tag_dicts,
                                    "is_mandatory": is_mandatory
                                }
                                
                                # Add to cache
                                try:
                                    _tags_cache[cache_key] = {
                                        "tags": tag_dicts,
                                        "is_mandatory": is_mandatory
                                    }
                                except Exception as cache_e:
                                    logger.warning(f"Error caching tags for {element_name}: {str(cache_e)}")
                        except Exception as elem_e:
                            logger.warning(f"Error processing element {element_name}: {str(elem_e)}")
                            # Add minimal entry for this element to avoid breaking the output
                            tagged_section[element_name] = {
                                "value": element_value,
                                "tags": [],
                                "processing_error": str(elem_e)
                            }
            else:
                # Original non-batch processing for comparison
                for element_name, element_value in section_data.items():
                    try:
                        # Skip processing of lists/dicts - they would be handled separately
                        if isinstance(element_value, (list, dict)):
                            continue
                            
                        # Find matching tags
                        tags = []
                        try:
                            if element_name in context.deps.field_tags:
                                tags = context.deps.field_tags[element_name]
                        except Exception:
                            pass
                        
                        # Convert tags to dict safely
                        tag_dicts = []
                        for tag in tags:
                            try:
                                if hasattr(tag, 'dict') and callable(tag.dict):
                                    tag_dicts.append(tag.dict())
                                else:
                                    tag_dict = {k: v for k, v in tag.__dict__.items() 
                                               if not k.startswith('_')}
                                    tag_dicts.append(tag_dict)
                            except Exception:
                                continue
                        
                        tagged_section[element_name] = {
                            "value": element_value,
                            "tags": tag_dicts
                        }
                    except Exception as elem_e:
                        logger.warning(f"Error in non-batch processing for element {element_name}: {str(elem_e)}")
        except Exception as batch_e:
            logger.error(f"Error in batch processing for section {section_name}: {str(batch_e)}")
            # Return partial results with error information
            tagged_section["_error"] = str(batch_e)
        
        # Add performance metrics
        try:
            tagged_section["_performance"] = {
                "section_name": section_name,
                "statement_type": statement_type,
                "elements_processed": len(section_data),
                "processing_time_ms": (time.time() - start_time) * 1000,
                "batch_processing_used": use_batch_processing,
                "status": "success" if "_error" not in tagged_section else "partial_failure"
            }
        except Exception as perf_e:
            logger.warning(f"Error adding performance metrics: {str(perf_e)}")
        
        return tagged_section
        
    except Exception as e:
        # Catch-all error handler
        logger.error(f"Critical error in tag_statement_section: {str(e)}")
        # Return a minimal valid response
        return {
            "section_name": section_name,
            "critical_error": str(e),
            "_performance": {
                "section_name": section_name,
                "processing_time_ms": (time.time() - time.time()) * 1000,
                "status": "critical_failure"
            }
        }

# Update the create_context_info tool - this is still useful for creating proper XBRL contexts
def create_context_info(
    context: RunContext[XBRLTaxonomyDependencies],
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

# # Enhanced validation tool
# def validate_tagged_data(
#     context: RunContext[XBRLTaxonomyDependencies],
#     tagged_data: Dict[str, Any]
# ) -> List[Dict[str, str]]:
#     """
#     Validate the tagged data for completeness and correctness
    
#     Args:
#         context: Runtime context containing taxonomy dependencies
#         tagged_data: Complete set of tagged financial data
        
#     Returns:
#         List of validation issues found
#     """
#     start_time = time.time()
#     issues = []
    
#     # Check for missing mandatory fields
#     for field_name, is_mandatory in context.deps.mandatory_fields.items():
#         if is_mandatory:
#             field_found = False
            
#             # Search through all sections for the field
#             for section_name, section_data in tagged_data.items():
#                 if isinstance(section_data, dict) and field_name in section_data:
#                     field_found = True
#                     break
            
#             if not field_found:
#                 issues.append({
#                     "severity": "error",
#                     "type": "missing_mandatory_field",
#                     "field": field_name,
#                     "message": f"Mandatory field '{field_name}' is missing from the tagged data"
#                 })
    
#     # Check for fields without tags
#     for section_name, section_data in tagged_data.items():
#         if isinstance(section_data, dict):
#             for field_name, field_data in section_data.items():
#                 if isinstance(field_data, dict) and "tags" in field_data and not field_data["tags"]:
#                     issues.append({
#                         "severity": "warning",
#                         "type": "missing_tags",
#                         "section": section_name,
#                         "field": field_name,
#                         "message": f"No tags applied to field '{field_name}' in section '{section_name}'"
#                     })
    
#     # Return issues with performance data
#     return {
#         "issues": issues,
#         "issue_count": len(issues),
#         "validation_time_ms": (time.time() - start_time) * 1000
#     }

# New batch processing helper for the existing apply_tags_to_element function
def batch_tag_elements(
    context: RunContext[XBRLTaxonomyDependencies],
    elements: Dict[str, Any],
    statement_type: str
) -> Dict[str, Any]:
    """
    Process multiple elements at once for better performance
    
    Args:
        context: Runtime context containing taxonomy dependencies
        elements: Dictionary of elements to tag {name: value}
        statement_type: Type of statement these elements belong to
        
    Returns:
        Dictionary of tagged elements
    """
    start_time = time.time()
    result = {}
    
    # Process all elements at once
    for element_name, element_value in elements.items():
        if not isinstance(element_value, dict) and element_value is not None:
            # Get individual element tags
            element_result = apply_tags_to_element(
                context, 
                element_name, 
                element_value, 
                statement_type
            )
            result[element_name] = element_result
    
    # Add performance metrics
    processing_time = (time.time() - start_time) * 1000
    result["_performance"] = {
        "elements_processed": len(elements),
        "processing_time_ms": processing_time,
        "elements_per_second": len(elements) / (processing_time / 1000) if processing_time > 0 else 0
    }
    
    return result