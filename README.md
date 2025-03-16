# XBRL Mapping and Tagging API Documentation

## Overview
The XBRL Mapping and Tagging API converts financial statements into standardized formats with proper XBRL tags for regulatory reporting. This API supports mapping financial data to standard formats and applying appropriate XBRL tags based on Singapore ACRA taxonomy.

## Getting Started

### Prerequisites
* Python 3.8 or higher
* OpenAI API key (required for the LLM-based mapping and tagging)

### Installation
1. Clone the repository:
   ```
   git clone https://github.com/yourusername/xbrl-mapping.git
   cd xbrl-mapping
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Configure environment variables:
   * Create a .env file in the project root
   * Add your OpenAI API key: OPENAI_API_KEY=your_api_key_here
4. Start the API server:
   ```
   uvicorn api:app --reload
   ```

## API Endpoints
The API provides three main endpoints for different processing needs:

### Base URL
`http://127.0.0.1:8000`

### 1. Map Financial Data (`/api/map`)
Converts raw financial data into a standardized format.

**Request:**
* Method: `POST`
* Content-Type: `application/json`
* Body:
  ```json
  {
    "data": {
      "filingInformation": {
        "CompanyName": "example",
        "UniqueEntityNumber": "123456789A",
        "CurrentPeriodStartDate": "2025-01-01",
        "CurrentPeriodEndDate": "2025-12-31"
      },
      "statementOfFinancialPosition": {
        "currentAssets": {
          "CashAndBankBalances": 150000,
          "TotalCurrentAssets": 500000
        }
      }
    }
  }
  ```

**Response:**
```json
{
  "mapped_data": {
    "filingInformation": {
      "companyName": "example",
      "uniqueEntityNumber": "123456789A",
      "currentPeriodStartDate": "2025-01-01",
      "currentPeriodEndDate": "2025-12-31"
    },
    "statementOfFinancialPosition": {
      "currentAssets": {
        "cashAndBankBalances": 150000,
        "totalCurrentAssets": 500000
      }
    }
  }
}
```

### 2. Apply XBRL Tags (`/api/tag`)
Applies XBRL tags to already-mapped financial data.

**Request:**
* Method: `POST`
* Content-Type: `application/json`
* Body:
  ```json
  {
    "data": {
      "filingInformation": {
        "companyName": "example",
        "uniqueEntityNumber": "123456789A"
      },
      "statementOfFinancialPosition": {
        "currentAssets": {
          "cashAndBankBalances": 150000
        }
      }
    }
  }
  ```

**Response:**
```json
{
  "tagged_data": {
    "filingInformation": {
      "companyName": {
        "value": "example",
        "tags": [
          {
            "namespace": "sg-dei",
            "element_name": "NameOfCompany",
            "element_id": "dei_NameOfCompany"
          }
        ]
      }
    }
  },
  "tags": {
    "sg-dei:NameOfCompany": "example",
    "sg-common:CashAndBankBalances": 150000
  }
}
```

### 3. Process Complete Financial Data (`/api/process`)
Maps and tags financial data in a single request.

**Request:**
* Method: `POST`
* Content-Type: `application/json`
* Body: Same as `/api/map` endpoint

**Response:**
```json
{
  "mapped_data": { /* Mapped data structure */ },
  "tagged_data": { /* Tagged data structure */ },
  "tags": { /* Simplified tag list */ }
}
```

## Error Handling
The API returns standard HTTP status codes:
* `200 OK`: Request processed successfully
* `400 Bad Request`: Invalid request format
* `422 Unprocessable Entity`: Valid request format but processing failed
* `500 Internal Server Error`: Server-side error

Error responses include a detail message:
```json
{
  "detail": "Mapping error: Invalid financial statement structure"
}
```

## Examples

### Example 1: Map a Simple Balance Sheet
**Request:**
```bash
curl -X POST http://localhost:8000/api/map \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "statementOfFinancialPosition": {
        "currentAssets": {
          "CashAndBankBalances": 150000,
          "Inventories": 45000,
          "TotalCurrentAssets": 195000
        },
        "TotalAssets": 195000
      }
    }
  }'
```

### Example 2: Complete Processing with Postman
1. Set the request to `POST` to `http://localhost:8000/api/process`
2. Add your financial data in the request body
3. Send and receive both mapped and tagged data

## Limitations
* The API processes one statement at a time
* Large financial statements may take longer to process
* Currently supports Singapore ACRA XBRL taxonomy version 2022.2

## Best Practices
1. Include all required fields for your jurisdiction
2. Use standard terminology for financial items
3. Validate the tagging output against your regulatory requirements
4. For large statements, consider breaking them into smaller logical sections

## Troubleshooting
* **API Key Issues**: Ensure your OpenAI API key is valid and has sufficient credits
* **Timeout Errors**: Large or complex statements may exceed processing limits
* **Missing Tags**: Check if your financial terms match the standard terminology
* **Validation Errors**: Compare your input with the example data format
* **Changes doesn't reflect to the API**:
```bash
  # Stop all Python processes (replace with proper process termination for your OS)
  # On Windows:
  taskkill /f /im python.exe

  # Restart the server
  uvicorn api:app --reload
```