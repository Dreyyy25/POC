"""
API endpoint for the XBRL mapping and tagging service.
"""
import os
import json
from fastapi import FastAPI, HTTPException, Body, Request
from pydantic import BaseModel
from typing import Dict, Any, Optional
from dotenv import load_dotenv
import logfire  # Add logfire import

# Import your existing functionality
from mapping.agent import financial_statement_agent, financial_deps
from tagging.agent import xbrl_tagging_agent
from tagging.dependencies import sg_xbrl_deps

# Set environment variables directly
# Load environment variables from .env file
load_dotenv()

# Configure logging
logfire.configure(console=False)
logfire.instrument_openai()  # Track OpenAI API calls

# Validate that required environment variables are set
if not os.environ.get("OPENAI_API_KEY"):
    logfire.error("Missing API key", key="OPENAI_API_KEY")
    raise ValueError("OPENAI_API_KEY environment variable is not set in .env file")

# Create FastAPI app
app = FastAPI(
    title="XBRL Mapping and Tagging API",
    description="API for converting financial statements to XBRL tagged format",
    version="1.0.0"
)

# Add logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    # Log incoming request
    path = request.url.path
    method = request.method
    client_host = request.client.host if request.client else "unknown"
    
    logfire.info(
        "API Request received", 
        path=path,
        method=method,
        client=client_host
    )
    
    # Process request
    try:
        response = await call_next(request)
        logfire.info(
            "API Request completed", 
            path=path, 
            status_code=response.status_code
        )
        return response
    except Exception as e:
        logfire.exception(
            "API Request failed", 
            path=path, 
            error=str(e)
        )
        raise

# Define input models
class FinancialStatementData(BaseModel):
    """Raw financial statement data for processing"""
    data: Dict[str, Any]
    
# Define response models
class MappingResponse(BaseModel):
    """Response from the mapping operation"""
    mapped_data: Dict[str, Any]
    
class TaggingResponse(BaseModel):
    """Response from the tagging operation"""
    tagged_data: Dict[str, Any]
    tags: Dict[str, Any]
    
class CombinedResponse(BaseModel):
    """Combined mapping and tagging response"""
    mapped_data: Dict[str, Any]
    tagged_data: Dict[str, Any]
    tags: Dict[str, Any]

# API endpoints
@app.post("/api/map", response_model=MappingResponse)
async def map_financial_data(data: FinancialStatementData):
    """Map financial statement data to standard format"""
    try:
        logfire.info("Starting financial data mapping process")
        
        # Convert to JSON string and process
        data_json = json.dumps(data.data, indent=4)
        logfire.debug("Input data prepared", data_size=len(data_json))
        
        result_mapping = await financial_statement_agent.run(
            f'Please map this financial statement data: {data_json}',
            deps=financial_deps
        )
        
        logfire.info("Financial data mapping completed successfully")
        
        # Convert Pydantic model to dictionary - fix for the error
        if hasattr(result_mapping.data, 'model_dump'):  # Pydantic v2
            mapped_data_dict = result_mapping.data.model_dump()
        elif hasattr(result_mapping.data, 'dict'):      # Pydantic v1
            mapped_data_dict = result_mapping.data.dict()
        else:
            # Fallback to manual conversion
            mapped_data_dict = {k: v for k, v in result_mapping.data.__dict__.items() 
                               if not k.startswith('_')}
        
        return {
            "mapped_data": mapped_data_dict
        }
    except Exception as e:
        logfire.exception("Error during financial data mapping", error=str(e))
        raise HTTPException(status_code=500, detail=f"Mapping error: {str(e)}")

@app.post("/api/tag", response_model=TaggingResponse)
async def tag_financial_data(data: FinancialStatementData):
    """Apply XBRL tags to already mapped financial data"""
    try:
        logfire.info("Starting XBRL tagging process")
        
        # Process data through tagging agent
        tagged_result = await xbrl_tagging_agent.run(
            f'Please apply appropriate XBRL tags to this financial data',
            deps=sg_xbrl_deps,
            data=data.data  # Pass data directly
        )
        
        logfire.info("XBRL tagging completed successfully", 
                    tags_count=len(tagged_result.get_all_tags()))
        
        return {
            "tagged_data": tagged_result.data,
            "tags": tagged_result.get_all_tags()
        }
    except Exception as e:
        logfire.exception("Error during XBRL tagging", error=str(e))
        raise HTTPException(status_code=500, detail=f"Tagging error: {str(e)}")

@app.post("/api/process", response_model=CombinedResponse)
async def process_financial_data(data: FinancialStatementData):
    """Map and tag financial data in one request"""
    try:
        logfire.info("Starting combined mapping and tagging process")
        
        # Step 1: Map data
        data_json = json.dumps(data.data, indent=4)
        result_mapping = await financial_statement_agent.run(
            f'Please map this financial statement data: {data_json}',
            deps=financial_deps
        )
        
        logfire.info("Financial data mapping completed")
        
        # Step 2: Tag mapped data
        tagged_result = await xbrl_tagging_agent.run(
            f'Please apply appropriate XBRL tags to this financial data: {result_mapping}',
            deps=sg_xbrl_deps
        )
        
        logfire.info("XBRL tagging completed", 
                    tags_count=len(tagged_result.get_all_tags()))
        
        # Convert Pydantic models to dictionaries for response
        if hasattr(result_mapping.data, 'model_dump'):
            mapped_data_dict = result_mapping.data.model_dump()
        elif hasattr(result_mapping.data, 'dict'):
            mapped_data_dict = result_mapping.data.dict()
        else:
            mapped_data_dict = {k: v for k, v in result_mapping.data.__dict__.items() 
                              if not k.startswith('_')}
        
        return {
            "mapped_data": mapped_data_dict,
            "tagged_data": tagged_result.data,
            "tags": tagged_result.get_all_tags()
        }
    except Exception as e:
        logfire.exception("Error during combined process", error=str(e))
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")

# Run with: uvicorn api:app --reload
if __name__ == "__main__":
    import uvicorn
    
    logfire.info("Starting XBRL API server")
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)