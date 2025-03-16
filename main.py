"""
Main entry point for the XBRL mapping and tagging application.
"""
import os
import json
from dotenv import load_dotenv
from pydantic_ai.models.openai import OpenAIModel
from mapping.agent import financial_statement_agent, financial_deps
from mapping.models import PartialXBRL
from tagging.agent import xbrl_tagging_agent
from tagging.dependencies import sg_xbrl_deps
from devtools import debug
import pprint
import logfire

# Load environment variables
load_dotenv()

# Configure logging
logfire.configure(console=False)
logfire.instrument_openai()

# Get API keys from environment variables
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

async def main():
    # Sample test data
    dummy_data_noise = {
        "filingInformation": {
            "CompanyName": "ACME Corporation",  # Changed from 'NameOfCompany'
            "UniqueEntityNumber": "123456789A",
            "CurrentPeriodStartDate": "2022-01-01",
            "CurrentPeriodEndDate": "2022-12-31",
            "PriorPeriodStartDate": "2021-01-01",
            "FilingType": "Full",  # Changed from 'TypeOfXBRLFiling'
            "NatureOfFinancialStatements": "Company",  # Changed from 'NatureOfFinancialStatementsCompanyLevelOrConsolidated'
            "AccountingStandardUsed": "IFRS",  # Changed from 'TypeOfAccountingStandardUsedToPrepareFinancialStatements'
            "DateOfAuthorisationForIssueOfFinancialStatements": "2023-03-15",
            "StatementOfFinancialPositionType": "Classified",  # Changed from 'TypeOfStatementOfFinancialPosition'
            "IsGoingConcernBasis": True,  # Changed from 'WhetherTheFinancialStatementsArePreparedOnGoingConcernBasis'
            "AreComparativeAmountsChanged": False,  # Changed from 'WhetherThereAreAnyChangesToComparativeAmounts'
            "PresentationCurrency": "USD",  # Changed from 'DescriptionOfPresentationCurrency'
            "FunctionalCurrency": "USD",  # Changed from 'DescriptionOfFunctionalCurrency'
            "RoundingLevel": "Units",  # Changed from 'LevelOfRoundingUsedInFinancialStatements'
            "NatureOfOperations": "Manufacturing and distribution of consumer electronics.",  # Changed from 'DescriptionOfNatureOfEntitysOperationsAndPrincipalActivities'
            "BusinessAddress": "123 Business Street, Industrial Park",  # Changed from 'PrincipalPlaceOfBusinessIfDifferentFromRegisteredOffice'
            "HasMoreThan50Employees": True,  # Changed from 'WhetherCompanyOrGroupIfConsolidatedAccountsArePreparedHasMoreThan50Employees'
            "ParentEntityName": None,  # Changed from 'NameOfParentEntity'
            "UltimateParentEntityName": None,  # Changed from 'NameOfUltimateParentOfGroup'
            "TaxonomyVersion": "2022.2",
            "SoftwareUsed": "XBRL Generator v1.0",  # Changed from 'NameAndVersionOfSoftwareUsedToGenerateXBRLFile'
            "XBRLPreparationMethod": "Automated"  # Changed from 'HowWasXBRLFilePrepared'
        },
        "directorsStatement": {
            "IsTrueAndFairView": True,  # Changed from 'WhetherInDirectorsOpinionFinancialStatementsAreDrawnUpSoAsToExhibitATrueAndFairView'
            "CanPayDebtsWhenDue": True  # Changed from 'WhetherThereAreReasonableGroundsToBelieveThatCompanyWillBeAbleToPayItsDebtsAsAndWhenTheyFallDueAtDateOfStatement'
        },
        "auditReport": {
            "AuditOpinionType": "Unqualified",  # Changed from 'TypeOfAuditOpinionInIndependentAuditorsReport'
            "AuditingStandardsUsed": "ISA",  # Changed from 'AuditingStandardsUsedToConductTheAudit'
            "IsGoingConcernUncertain": False,  # Changed from 'WhetherThereIsAnyMaterialUncertaintyRelatingToGoingConcern'
            "AreRecordsProperlyKept": True  # Changed from 'WhetherInAuditorsOpinionAccountingAndOtherRecordsRequiredAreProperlyKept'
        },
        "statementOfFinancialPosition": {
            "currentAssets": {
            "CashAndBankBalances": 150000,
            "TradeAndOtherReceivablesCurrent": 300000,
            "CurrentFinanceLeaseReceivables": 20000,
            "CurrentDerivativeFinancialAssets": 5000,
            "CurrentFinancialAssetsAtFVTPL": 10000,  # Changed from 'CurrentFinancialAssetsMeasuredAtFairValueThroughProfitOrLoss'
            "OtherCurrentFinancialAssets": 0,
            "DevelopmentProperties": 0,
            "Inventories": 45000,
            "OtherCurrentNonfinancialAssets": 0,
            "AssetsHeldForSale": 0,  # Changed from 'NoncurrentAssetsOrDisposalGroupsClassifiedAsHeldForSaleOrAsHeldForDistributionToOwners'
            "TotalCurrentAssets": 500000  # Changed from 'CurrentAssets'
            },
            "nonCurrentAssets": {
            "TradeAndOtherReceivablesNoncurrent": 200000,
            "NoncurrentFinanceLeaseReceivables": 15000,
            "NoncurrentDerivativeFinancialAssets": 7000,
            "NoncurrentFinancialAssetsAtFVTPL": 12000,  # Changed from 'NoncurrentFinancialAssetsMeasuredAtFairValueThroughProfitOrLoss'
            "OtherNoncurrentFinancialAssets": 0,
            "PropertyPlantAndEquipment": 800000,
            "InvestmentProperties": 50000,
            "Goodwill": 30000,
            "OtherIntangibleAssets": 25000,  # Changed from 'IntangibleAssetsOtherThanGoodwill'
            "InvestmentsInSubsidiariesAssociatesOrJointVentures": 100000,
            "DeferredTaxAssets": 15000,
            "OtherNoncurrentNonfinancialAssets": 0,
            "TotalNoncurrentAssets": 1200000  # Changed from 'NoncurrentAssets'
            },
            "TotalAssets": 1700000,  # Changed from 'Assets'
            "currentLiabilities": {
            "TradeAndOtherPayablesCurrent": 100000,
            "CurrentLoansAndBorrowings": 50000,
            "CurrentFinancialLiabilitiesAtFVTPL": 8000,  # Changed from 'CurrentFinancialLiabilitiesMeasuredAtFairValueThroughProfitOrLoss'
            "CurrentFinanceLeaseLiabilities": 6000,
            "OtherCurrentFinancialLiabilities": 0,
            "CurrentIncomeTaxLiabilities": 20000,
            "CurrentProvisions": 10000,
            "OtherCurrentNonfinancialLiabilities": 5000,
            "LiabilitiesHeldForSale": 0,  # Changed from 'LiabilitiesClassifiedAsHeldForSale'
            "TotalCurrentLiabilities": 200000  # Changed from 'CurrentLiabilities'
            },
            "nonCurrentLiabilities": {
            "TradeAndOtherPayablesNoncurrent": 40000,
            "NoncurrentLoansAndBorrowings": 60000,
            "NoncurrentFinancialLiabilitiesAtFVTPL": 5000,  # Changed from 'NoncurrentFinancialLiabilitiesMeasuredAtFairValueThroughProfitOrLoss'
            "NoncurrentFinanceLeaseLiabilities": 4000,
            "OtherNoncurrentFinancialLiabilities": 0,
            "DeferredTaxLiabilities": 15000,
            "NoncurrentProvisions": 7000,
            "OtherNoncurrentNonfinancialLiabilities": 0,
            "TotalNoncurrentLiabilities": 200000  # Changed from 'NoncurrentLiabilities'
            },
            "TotalLiabilities": 400000,  # Changed from 'Liabilities'
            "equity": {
            "ShareCapital": 500000,
            "TreasuryShares": 10000,
            "RetainedEarnings": 300000,  # Changed from 'AccumulatedProfitsLosses'
            "OtherReserves": 50000,  # Changed from 'ReservesOtherThanAccumulatedProfitsLosses'
            "NonControllingInterests": 0,  # Changed from 'NoncontrollingInterests'
            "TotalEquity": 790000  # Changed from 'Equity'
            }
        },
        "incomeStatement": {
            "Revenue": 1000000,
            "OtherIncome": 50000,
            "EmployeeBenefitsExpense": 200000,
            "DepreciationExpense": 50000,
            "AmortizationExpense": 10000,  # Changed from 'AmortisationExpense'
            "ProfitOrLossFromDiscontinuedOperations": 0,
            "NetProfitOrLoss": 120000,  # Changed from 'ProfitLoss'
            "ProfitOrLossAttributableToOwners": 110000,  # Changed from 'ProfitLossAttributableToOwnersOfCompany'
            "ProfitOrLossAttributableToNonControllingInterests": 10000,  # Changed from 'ProfitLossAttributableToNoncontrollingInterests'
            "RepairsAndMaintenanceExpense": 15000,
            "SalesAndMarketingExpense": 25000,
            "OtherExpenses": 10000,  # Changed from 'OtherExpensesByNature'
            "OtherGainsOrLosses": 0,  # Changed from 'OtherGainsLosses'
            "FinanceCosts": 8000,
            "ShareOfProfitOrLossOfAssociatesAndJointVentures": 0,  # Changed from 'ShareOfProfitLossOfAssociatesAndJointVenturesAccountedForUsingEquityMethod'
            "ProfitOrLossBeforeTax": 150000,  # Changed from 'ProfitLossBeforeTaxation'
            "TaxExpenseOrBenefit": 30000,  # Changed from 'TaxExpenseBenefitContinuingOperations'
        },
        "notes": {
            "tradeAndOtherReceivables": {
            "ReceivablesFromThirdParties": 25000,  # Changed from 'TradeAndOtherReceivablesDueFromThirdParties'
            "ReceivablesFromRelatedParties": 15000,  # Changed from 'TradeAndOtherReceivablesDueFromRelatedParties'
            "UnbilledReceivables": 5000,
            "OtherReceivables": 2000,
            "TotalTradeAndOtherReceivables": 45000  # Changed from 'TradeAndOtherReceivables'
            },
            "tradeAndOtherPayables": {
            "PayablesToThirdParties": 20000,  # Changed from 'TradeAndOtherPayablesDueToThirdParties'
            "PayablesToRelatedParties": 10000,  # Changed from 'TradeAndOtherPayablesDueToRelatedParties'
            "DeferredIncome": 3000,
            "OtherPayables": 2000,
            "TotalTradeAndOtherPayables": 55000  # Changed from 'TradeAndOtherPayables'
            },
            "revenue": {
            "RevenueFromPropertyAtPointInTime": 0,  # Changed from 'RevenueFromPropertyTransferredAtPointInTime'
            "RevenueFromGoodsAtPointInTime": 0,  # Changed from 'RevenueFromGoodsTransferredAtPointInTime'
            "RevenueFromServicesAtPointInTime": 0,  # Changed from 'RevenueFromServicesTransferredAtPointInTime'
            "RevenueFromPropertyOverTime": 5000,  # Changed from 'RevenueFromPropertyTransferredOverTime'
            "RevenueFromConstructionContracts": 3000,  # Changed from 'RevenueFromConstructionContractsOverTime'
            "RevenueFromServicesOverTime": 7000,  # Changed from 'RevenueFromServicesTransferredOverTime'
            "OtherRevenue": 1000,
            "TotalRevenue": 120000  # Changed from 'Revenue'
            }
        }
    }
    
    # Convert to JSON string
    dummy_data_json = json.dumps(dummy_data_noise, indent=4)
    
    # Step 1: Map the data to structured format
    result_mapping = await financial_statement_agent.run(
        f'Please map this financial statement data: {dummy_data_json}',
        deps=financial_deps
    )
    
    # Print Mapping Results
    debug(result_mapping)
    print("\nMapped Statement:")
    pprint.pprint(result_mapping.data)
    
    # Step 2: Apply XBRL tags to the mapped data
    tagged_result = await xbrl_tagging_agent.run(
        f'Please apply appropriate XBRL tags to this financial data: {result_mapping}',
        deps=sg_xbrl_deps
    )
    
    # Print tagging results
    debug(tagged_result)
    print("\nTagged XBRL Data:")
    pprint.pprint(tagged_result.get_all_tags())
    
    return result_mapping, tagged_result

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
