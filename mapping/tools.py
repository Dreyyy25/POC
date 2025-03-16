"""
Tools for the financial statement mapping agent.
"""
from typing import Dict, Any, List, Union
from pydantic import BaseModel, Field
from pydantic_ai import RunContext

from .dependencies import FinancialTermDeps

class MatchTermContext(BaseModel):
    """Context for the term matching tool"""
    pass

class FinancialData(BaseModel):
    """Schema for financial data structure"""
    data: Dict[str, Any] = Field(..., description="Financial data items")
    
    # Alternative constructor for direct dictionary input
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(data=data)

class ExtractContext(BaseModel):
    """Context for the extraction tool"""
    pass

def match_financial_term(context: RunContext[FinancialTermDeps], term: str, statement_type: str = "all") -> Dict[str, Any]:
    """
    Match a financial term to the standardized field name in financial statements.
    Uses injected financial term mappings from dependencies.
    
    Args:
        context: The tool context with injected dependencies
        term: The financial term to match (e.g., "Revenue", "Staff Costs", "Cash and bank", etc.)
        statement_type: Type of statement to match against ("income", "position", "all")
        
    Returns:
        Dictionary with matching field name, statement type, and confidence level
    """
    term_lower = term.lower().strip()
    
    # Get mappings from dependencies
    income_mappings = context.deps.income_statement_terms
    position_mappings = context.deps.financial_position_terms
    
    # Filter mappings based on statement_type - with null safety
    filtered_mappings = {}
    
    # Ensure statement_type is not None before calling lower()
    statement_type = statement_type or "all"
    
    if statement_type.lower() in ["all", "income", "profit", "loss"]:
        for field, keywords in income_mappings.items():
            filtered_mappings[f"income.{field}"] = keywords
    
    if statement_type.lower() in ["all", "position", "balance", "financial_position"]:
        for field, keywords in position_mappings.items():
            filtered_mappings[f"position.{field}"] = keywords
    
    # If no valid statement type provided, use all mappings
    if not filtered_mappings:
        for field, keywords in income_mappings.items():
            filtered_mappings[f"income.{field}"] = keywords
        for field, keywords in position_mappings.items():
            filtered_mappings[f"position.{field}"] = keywords
    
    # Find matches
    matches = {}
    for full_field, keywords in filtered_mappings.items():
        score = 0
        for keyword in keywords:
            if keyword in term_lower:
                score += 1
            # Extra points for exact matches or close matches
            if keyword == term_lower:
                score += 5
            elif keyword in term_lower and len(keyword) > 5:
                score += 2
                
        if score > 0:
            matches[full_field] = score
    
    # If we have matches, return the best one
    if matches:
        best_match = max(matches.items(), key=lambda x: x[1])
        statement_type, field_name = best_match[0].split('.', 1)
        
        return {
            "statement_type": "income_statement" if statement_type == "income" else "financial_position",
            "field": field_name,
            "match_score": best_match[1],
            "matched_term": term
        }
    
    # No matches found - make a best guess based on the term
    if any(word in term_lower for word in ["revenue", "income", "sale", "expense", "cost", "profit", "loss", "tax"]):
        return {
            "statement_type": "income_statement",
            "field": term,
            "match_score": 0,
            "matched_term": term
        }
    elif any(word in term_lower for word in ["asset", "liability", "equity", "cash", "receivable", "payable", "property", "equipment"]):
        return {
            "statement_type": "financial_position", 
            "field": term,
            "match_score": 0,
            "matched_term": term
        }
    
    # Truly unknown
    return {
        "statement_type": "unknown",
        "field": "unknown",
        "match_score": 0,
        "matched_term": term
    }

def extract_and_categorize_financial_data(context: RunContext[ExtractContext], data: Union[Dict[str, Any], FinancialData], field_path: str = "") -> Dict[str, Dict[str, float]]:
    """
    Extract and categorize financial values from nested structures, organizing them into appropriate statement models.
    Handles direct values without CFY/PFY structure, assuming each field has only one value.
    
    Args:
        context: The tool context
        data: Financial data structure (raw dictionary or FinancialData object)
        field_path: Current path in the nested structure (used in recursion)
        
    Returns:
        Dictionary with categorized financial data organized by statement type and field
    """
    # Initialize results with statement types
    results = {
        "income_statement": {},
        "financial_position": {},
        "unknown": {}
    }
    
    # Handle different input types
    if isinstance(data, dict):
        items_dict = data
    elif hasattr(data, 'data'):
        items_dict = data.data
    else:
        items_dict = {}
        
    # Special case: Check if data is already in statement form
    if "incomeStatement" in items_dict and isinstance(items_dict["incomeStatement"], dict):
        results["income_statement"] = {k: float(v) for k, v in items_dict["incomeStatement"].items() if isinstance(v, (int, float))}
    
    if "statementOfFinancialPosition" in items_dict and isinstance(items_dict["statementOfFinancialPosition"], dict):
        # Extract values from the financial position structure
        financial_position = items_dict["statementOfFinancialPosition"]
        
        # First handle top-level items
        for key, value in financial_position.items():
            if isinstance(value, (int, float)):
                results["financial_position"][key] = float(value)
        
        # Handle nested structures (current assets, non-current assets, etc.)
        for section in ["currentAssets", "nonCurrentAssets", "currentLiabilities", "nonCurrentLiabilities", "equity"]:
            if section in financial_position and isinstance(financial_position[section], dict):
                for key, value in financial_position[section].items():
                    if isinstance(value, (int, float)):
                        results["financial_position"][f"{section}.{key}"] = float(value)
    
    # Process regular dictionary structure
    for key, value in items_dict.items():
        # Skip already processed statement sections
        if key in ["incomeStatement", "statementOfFinancialPosition"]:
            continue
            
        current_path = f"{field_path}_{key}" if field_path else key
        
        # Process direct numeric values
        if isinstance(value, (int, float)):
            float_value = float(value)
            term_info = match_financial_term(context, current_path)
            
            if term_info["statement_type"] != "unknown":
                results[term_info["statement_type"]][term_info["field"]] = float_value
            else:
                term_info_key_only = match_financial_term(context, key)
                if term_info_key_only["statement_type"] != "unknown":
                    results[term_info_key_only["statement_type"]][term_info_key_only["field"]] = float_value
                else:
                    results["unknown"][current_path] = float_value
        
        # Process nested dictionaries
        elif isinstance(value, dict):
            if len(value) == 1 and isinstance(list(value.values())[0], (int, float)):
                term_info = match_financial_term(context, current_path)
                if term_info["statement_type"] != "unknown":
                    results[term_info["statement_type"]][term_info["field"]] = float(list(value.values())[0])
                else:
                    results["unknown"][current_path] = float(list(value.values())[0])
                continue
            
            nested_results = extract_and_categorize_financial_data(context, value, current_path)
            for statement_type, fields in nested_results.items():
                for field, value in fields.items():
                    if statement_type in results:
                        results[statement_type][field] = value
        
        # Handle arrays/lists
        elif isinstance(value, list):
            for i, item in enumerate(value):
                if isinstance(item, dict):
                    list_path = f"{current_path}[{i}]"
                    nested_results = extract_and_categorize_financial_data(context, item, list_path)
                    
                    for statement_type, fields in nested_results.items():
                        for field, value in fields.items():
                            if statement_type in results:
                                results[statement_type][field] = value
                elif isinstance(item, (int, float)) and i == 0:
                    term_info = match_financial_term(context, current_path)
                    if term_info["statement_type"] != "unknown":
                        results[term_info["statement_type"]][term_info["field"]] = float(item)
                    else:
                        results["unknown"][current_path] = float(item)
    
    # Remove empty statement types
    for statement_type in list(results.keys()):
        if not results[statement_type]:
            del results[statement_type]
    
    return results
