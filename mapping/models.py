"""
Base models for Singapore XBRL financial statement mappings
"""

# Mapping Models
from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal
from enum import Enum
import re
from datetime import date

# Enums for validation
class XBRLFiling(str, Enum):
    FULL = "Full"
    PARTIAL = "Partial"

class FinancialStatementType(str, Enum):
    COMPANY = "Company"
    CONSOLIDATED = "Consolidated"

class AccountingStandard(str, Enum):
    SFRS = "SFRS"
    SFRS_SE = "SFRS for SE"
    IFRS = "IFRS"
    OTHER = "Other"

class StatementOfFinancialPositionType(str, Enum):
    CLASSIFIED = "Classified"
    LIQUIDITY = "Liquidity-based"

class RoundingLevel(str, Enum):
    THOUSANDS = "Thousands"
    MILLIONS = "Millions"
    UNITS = "Units"

class XBRLPreparationMethod(str, Enum):
    AUTOMATED = "Automated"
    MANUAL = "Manual"
    HYBRID = "Hybrid"

class AuditOpinion(str, Enum):
    UNQUALIFIED = "Unqualified"
    QUALIFIED = "Qualified"
    ADVERSE = "Adverse"
    DISCLAIMER = "Disclaimer"

# Custom validators
def validate_currency_code(v: str) -> str:
    """Validate ISO 4217 currency code"""
    if not re.match(r'^[A-Z]{3}$', v):
        raise ValueError("Currency code must be 3 uppercase letters (ISO 4217)")
    return v

def validate_date(v: str) -> str:
    """Validate ISO 8601 date format"""
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', v):
        raise ValueError("Date must be in ISO 8601 format (YYYY-MM-DD)")
    return v

def validate_uen(v: str) -> str:
    """Validate UEN format"""
    if not re.match(r'^\d{8}[A-Z]$', v):
        raise ValueError("UEN must be 8 digits followed by 1 uppercase letter")
    return v

# Pydantic models
class FilingInformation(BaseModel):
    """Basic information about the entity and the filing"""
    NameOfCompany: str = Field(..., min_length=1, description="Registered name of the entity in BizFile")
    UniqueEntityNumber: str = Field(..., description="Unique Entity Number assigned by ACRA")
    CurrentPeriodStartDate: str = Field(..., description="Start date of the current reporting period")
    CurrentPeriodEndDate: str = Field(..., description="End date of the current reporting period")
    PriorPeriodStartDate: Optional[str] = Field(None, description="Start date of the prior reporting period for comparatives")
    TypeOfXBRLFiling: XBRLFiling = Field(..., description="Whether the filing contains full or partial XBRL information")
    NatureOfFinancialStatementsCompanyLevelOrConsolidated: FinancialStatementType = Field(..., description="Whether the statements are for the company alone or consolidated group")
    TypeOfAccountingStandardUsedToPrepareFinancialStatements: AccountingStandard = Field(..., description="Accounting standards framework used")
    DateOfAuthorisationForIssueOfFinancialStatements: str = Field(..., description="Date when the financial statements were authorized for issue")
    TypeOfStatementOfFinancialPosition: StatementOfFinancialPositionType = Field(..., description="Whether the statement of financial position is presented in current/non-current format or order of liquidity")
    WhetherTheFinancialStatementsArePreparedOnGoingConcernBasis: bool = Field(..., description="Whether the entity is a going concern")
    WhetherThereAreAnyChangesToComparativeAmounts: Optional[bool] = Field(None, description="Whether comparative amounts have been restated or reclassified")
    DescriptionOfPresentationCurrency: str = Field(..., description="Currency used for presentation of the financial statements")
    DescriptionOfFunctionalCurrency: str = Field(..., description="Primary currency of the economic environment in which the entity operates")
    LevelOfRoundingUsedInFinancialStatements: RoundingLevel = Field(..., description="Level of rounding applied to the financial data")
    DescriptionOfNatureOfEntitysOperationsAndPrincipalActivities: str = Field(
        ..., 
        min_length=20, 
        max_length=100,
        description="Provide a detailed description of the nature of the entity's operations and its principal business activities, including key operational insights."
    )
    
    PrincipalPlaceOfBusinessIfDifferentFromRegisteredOffice: str = Field(..., description="Main location where business is conducted")
    WhetherCompanyOrGroupIfConsolidatedAccountsArePreparedHasMoreThan50Employees: bool = Field(..., description="Whether the company or group has more than 50 employees")
    NameOfParentEntity: Optional[str] = Field(None, description="Immediate parent company name")
    NameOfUltimateParentOfGroup: Optional[str] = Field(None, description="Ultimate parent company name")
    TaxonomyVersion: Literal["2022.2"] = Field(..., description="Version of the XBRL taxonomy used")
    NameAndVersionOfSoftwareUsedToGenerateXBRLFile: str = Field(..., description="Software used to prepare the XBRL filing")
    HowWasXBRLFilePrepared: XBRLPreparationMethod = Field(XBRLPreparationMethod.AUTOMATED, description="Indicate how the XBRL file was prepared: automated, manual, or hybrid (default is automated).")
    
    # Pydantic V2 field validators replacing the deprecated @validator decorators
    @field_validator("UniqueEntityNumber", mode="before")
    def validate_uen_field(cls, v: str) -> str:
        return validate_uen(v)
    
    @field_validator("DescriptionOfPresentationCurrency", mode="before")
    def validate_presentation_currency(cls, v: str) -> str:
        return validate_currency_code(v)
    
    @field_validator("DescriptionOfFunctionalCurrency", mode="before")
    def validate_functional_currency(cls, v: str) -> str:
        return validate_currency_code(v)
    
    @field_validator("CurrentPeriodStartDate", mode="before")
    def validate_current_period_start(cls, v: str) -> str:
        return validate_date(v)
    
    @field_validator("CurrentPeriodEndDate", mode="before")
    def validate_current_period_end(cls, v: str) -> str:
        return validate_date(v)
    
    @field_validator("PriorPeriodStartDate", mode="before")
    def validate_prior_period_start(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        return validate_date(v)
    
    @field_validator("DateOfAuthorisationForIssueOfFinancialStatements", mode="before")
    def validate_authorisation_date(cls, v: str) -> str:
        return validate_date(v)

class DirectorsStatement(BaseModel):
    """Statements made by the directors regarding the financial statements"""
    WhetherInDirectorsOpinionFinancialStatementsAreDrawnUpSoAsToExhibitATrueAndFairView: bool = Field(..., description="Directors' opinion on whether financial statements give a true and fair view")
    WhetherThereAreReasonableGroundsToBelieveThatCompanyWillBeAbleToPayItsDebtsAsAndWhenTheyFallDueAtDateOfStatement: bool = Field(..., description="Directors' opinion on solvency of the company")

class AuditReport(BaseModel):
    """Information about the independent auditors' report"""
    TypeOfAuditOpinionInIndependentAuditorsReport: AuditOpinion = Field(..., description="Type of opinion expressed by the auditors")
    AuditingStandardsUsedToConductTheAudit: Optional[str] = Field(None, description="Auditing standards framework used for the audit")
    WhetherThereIsAnyMaterialUncertaintyRelatingToGoingConcern: Optional[bool] = Field(None, description="Whether auditors reported material uncertainty about going concern")
    WhetherInAuditorsOpinionAccountingAndOtherRecordsRequiredAreProperlyKept: Optional[bool] = Field(None, description="Auditors' opinion on whether proper accounting records have been kept")

# Current Assets
class CurrentAssets(BaseModel):
    """Current assets section"""
    CashAndBankBalances: Optional[float] = Field(None,  description="Cash and bank balances, current. Common terms: cash, cash equivalents, bank balances, cash at bank, cash on hand")
    TradeAndOtherReceivablesCurrent: Optional[float] = Field(None,  description="Trade and other receivables (including contract assets), current. Common terms: accounts receivable, trade debtors, trade receivables")
    CurrentFinanceLeaseReceivables: Optional[float] = Field(None,  description="Financial assets - lease receivables, current. Common terms: lease receivables, finance lease assets, short-term lease receivables")
    CurrentDerivativeFinancialAssets: Optional[float] = Field(None,  description="Financial assets - derivatives, current. Common terms: derivative assets, forward contracts, swap assets, option assets")
    CurrentFinancialAssetsMeasuredAtFairValueThroughProfitOrLoss: Optional[float] = Field(None,  description="Financial assets at fair value through profit or loss, current. Common terms: FVTPL assets, trading assets, fair value instruments")
    OtherCurrentFinancialAssets: Optional[int] = Field(None,  description="Other financial assets, current. Common terms: short-term investments, marketable securities, financial instruments")
    DevelopmentProperties: Optional[float] = Field(None,  description="Inventories - development properties, current. Common terms: property development, properties under development, development inventory")
    Inventories: Optional[float] = Field(None,  description="Inventories - others, current. Common terms: stock, goods for sale, raw materials, finished goods, work in progress")
    OtherCurrentNonfinancialAssets: Optional[float] = Field(None,  description="Other non-financial assets, current. Common terms: prepayments, advances, deposits, other current assets")
    NoncurrentAssetsOrDisposalGroupsClassifiedAsHeldForSaleOrAsHeldForDistributionToOwners: Optional[float] = Field(None,  description="Non-current assets held for sale. Common terms: assets held for sale, disposal groups, discontinued operations assets")
    CurrentAssets: float = Field(...,  description="Total current assets. Common terms: total current assets, current assets, short-term assets")

# Non-Current Assets
class NonCurrentAssets(BaseModel):
    """Non-current assets section"""
    TradeAndOtherReceivablesNoncurrent: Optional[float] = Field(None,  description="Trade and other receivables, non-current. Common terms: long-term receivables, non-current debtors, long-term deposits")
    NoncurrentFinanceLeaseReceivables: Optional[float] = Field(None,  description="Financial assets - lease receivables, non-current. Common terms: long-term lease receivables, non-current leasing assets")
    NoncurrentDerivativeFinancialAssets: Optional[float] = Field(None,  description="Financial assets - derivatives, non-current. Common terms: long-term derivative assets, non-current hedging instruments")
    NoncurrentFinancialAssetsMeasuredAtFairValueThroughProfitOrLoss: Optional[float] = Field(None,  description="Financial assets at fair value through P/L, non-current. Common terms: long-term FVTPL assets, non-current fair value assets")
    OtherNoncurrentFinancialAssets: Optional[float] = Field(None,  description="Other financial assets, non-current. Common terms: long-term investments, bonds held, held-to-maturity investments")
    PropertyPlantAndEquipment: Optional[float] = Field(None,  description="Property, plant and equipment. Common terms: PPE, fixed assets, tangible assets, property and equipment")
    InvestmentProperties: Optional[float] = Field(None,  description="Investment properties. Common terms: investment real estate, rental properties, property investments")
    Goodwill: Optional[float] = Field(None,  description="Goodwill. Common terms: acquisition goodwill, purchased goodwill, business combination goodwill")
    IntangibleAssetsOtherThanGoodwill: Optional[float] = Field(None,  description="Intangible assets excluding goodwill. Common terms: patents, trademarks, software, licenses, intellectual property")
    InvestmentsInSubsidiariesAssociatesOrJointVentures: Optional[float] = Field(None,  description="Investments in subsidiaries, associates and joint ventures. Common terms: equity investments, associated companies, joint ventures")
    DeferredTaxAssets: Optional[float] = Field(None,  description="Deferred tax assets. Common terms: future tax assets, tax credits, deferred taxation assets")
    OtherNoncurrentNonfinancialAssets: Optional[float] = Field(None,  description="Other non-financial assets, non-current. Common terms: long-term prepayments, non-current advances")
    NoncurrentAssets: float = Field(...,  description="Total non-current assets. Common terms: total non-current assets, long-term assets, fixed assets")

# Current Liabilities
class CurrentLiabilities(BaseModel):
    """Current liabilities section"""
    TradeAndOtherPayablesCurrent: Optional[float] = Field(None,  description="Trade and other payables, current. Common terms: accounts payable, trade creditors, accruals, trade payables")
    CurrentLoansAndBorrowings: Optional[float] = Field(None,  description="Loans and borrowings, current. Common terms: short-term borrowings, bank overdrafts, current portion of loans")
    CurrentFinancialLiabilitiesMeasuredAtFairValueThroughProfitOrLoss: Optional[float] = Field(None,  description="Financial liabilities at fair value through P/L, current. Common terms: current FVTPL liabilities, derivative liabilities")
    CurrentFinanceLeaseLiabilities: Optional[float] = Field(None,  description="Finance lease liabilities, current. Common terms: current lease obligations, short-term lease liabilities")
    OtherCurrentFinancialLiabilities: Optional[float] = Field(None,  description="Other financial liabilities, current. Common terms: other financial obligations, financial payables")
    CurrentIncomeTaxLiabilities: Optional[float] = Field(None,  description="Income tax liabilities, current. Common terms: tax payable, current tax, income tax payable")
    CurrentProvisions: Optional[float] = Field(None,  description="Provisions, current. Common terms: short-term provisions, current provisions, warranty provisions")
    OtherCurrentNonfinancialLiabilities: Optional[float] = Field(None,  description="Other non-financial liabilities, current. Common terms: deferred income, contract liabilities, advances received")
    LiabilitiesClassifiedAsHeldForSale: Optional[float] = Field(None,  description="Liabilities classified as held for sale. Common terms: disposal group liabilities, discontinued operations liabilities")
    CurrentLiabilities: float = Field(...,  description="Total current liabilities. Common terms: total current liabilities, short-term liabilities")

# Non-Current Liabilities
class NonCurrentLiabilities(BaseModel):
    """Non-current liabilities section"""
    TradeAndOtherPayablesNoncurrent: Optional[float] = Field(None,  description="Trade and other payables, non-current. Common terms: long-term payables, non-current creditors")
    NoncurrentLoansAndBorrowings: Optional[float] = Field(None,  description="Loans and borrowings, non-current. Common terms: long-term borrowings, term loans, bonds payable")
    NoncurrentFinancialLiabilitiesMeasuredAtFairValueThroughProfitOrLoss: Optional[float] = Field(None,  description="Financial liabilities at fair value through P/L, non-current. Common terms: long-term FVTPL liabilities, long-term derivatives")
    NoncurrentFinanceLeaseLiabilities: Optional[float] = Field(None,  description="Finance lease liabilities, non-current. Common terms: long-term lease obligations, long-term lease liabilities")
    OtherNoncurrentFinancialLiabilities: Optional[float] = Field(None,  description="Other financial liabilities, non-current. Common terms: other long-term financial obligations")
    DeferredTaxLiabilities: Optional[float] = Field(None,  description="Deferred tax liabilities. Common terms: future tax liabilities, deferred taxation")
    NoncurrentProvisions: Optional[float] = Field(None,  description="Provisions, non-current. Common terms: long-term provisions, decommissioning provisions, restoration provisions")
    OtherNoncurrentNonfinancialLiabilities: Optional[float] = Field(None,  description="Other non-financial liabilities, non-current. Common terms: long-term deferred income, long-term contract liabilities")
    NoncurrentLiabilities: float = Field(...,  description="Total non-current liabilities. Common terms: total non-current liabilities, long-term liabilities")

# Equity
class Equity(BaseModel):
    """Equity section"""
    ShareCapital: float = Field(...,  description="Share capital. Common terms: issued capital, paid-up capital, ordinary shares, common stock")
    TreasuryShares: Optional[float] = Field(None,  description="Treasury shares. Common terms: own shares, repurchased shares, treasury stock")
    AccumulatedProfitsLosses: float = Field(..., description="Accumulated profits or losses. Common terms: retained earnings, retained profits, accumulated earnings")
    ReservesOtherThanAccumulatedProfitsLosses: Optional[float] = Field(None, description="Other reserves. Common terms: revaluation reserve, translation reserve, hedging reserve, capital reserve")
    NoncontrollingInterests: Optional[float] = Field(None, description="Non-controlling interests. Common terms: minority interests, NCI, minority shareholders' interest")
    Equity: float = Field(..., description="Total equity. Common terms: shareholders' equity, shareholders' funds, net assets, total equity")

class StatementOfFinancialPosition(BaseModel):
    """Balance sheet information"""
    CurrentAssets: CurrentAssets
    NonCurrentAssets: NonCurrentAssets
    Assets: float = Field(...,  description="Total assets (CurrentAssets + NoncurrentAssets)")
    CurrentLiabilities: CurrentLiabilities
    NonCurrentLiabilities: NonCurrentLiabilities
    Liabilities: float = Field(...,  description="Total liabilities (CurrentLiabilities + NoncurrentLiabilities)")
    Equity: Equity
    
    class Config:
        extra = "forbid"  # Equivalent to strict() in Zod

# Income Statement
class IncomeStatement(BaseModel):
    """Income statement information"""
    Revenue: float = Field(...,  description="Revenue from contracts with customers. Common terms: turnover, sales, contract revenue, income from operations")
    OtherIncome: Optional[float] = Field(None,  description="Other income not from primary operations. Common terms: other operating income, dividend income, interest income, rental income")
    EmployeeBenefitsExpense: Optional[float] = Field(None,  description="Employee benefits expense. Common terms: staff costs, salaries, wages, personnel expenses, CPF, compensation, bonuses")
    DepreciationExpense: Optional[float] = Field(None,  description="Depreciation of property, plant and equipment. Common terms: depreciation expense, PPE depreciation, fixed asset depreciation")
    AmortisationExpense: Optional[float] = Field(None,  description="Amortisation of intangible assets. Common terms: amortization expense, goodwill amortization, intangible amortization")
    RepairsAndMaintenanceExpense: Optional[float] = Field(None,  description="Repairs and maintenance costs. Common terms: upkeep expenses, maintenance costs, repair expenses")
    SalesAndMarketingExpense: Optional[float] = Field(None,  description="Sales and marketing costs. Common terms: marketing expenses, advertising, selling expenses, promotion, distribution costs")
    OtherExpensesByNature: Optional[float] = Field(None,  description="Other operating expenses by nature. Common terms: general expenses, administrative costs, utilities, office expenses, rental expenses")
    OtherGainsLosses: Optional[float] = Field(None, description="Other gains/(losses). Common terms: foreign exchange gains/losses, forex, fair value gains/losses, disposal gains/losses")
    FinanceCosts: Optional[float] = Field(None,  description="Net finance costs. Common terms: interest expense, borrowing costs, loan interest, financing costs")
    ShareOfProfitLossOfAssociatesAndJointVenturesAccountedForUsingEquityMethod: Optional[float] = Field(None, description="Share of profits/(losses) of associates/joint ventures. Common terms: equity method investments, associate profits, joint venture results")
    ProfitLossBeforeTaxation: float = Field(..., description="Profit/(loss) before tax from continuing operations. Common terms: profit before tax, earnings before tax, EBT, PBT")
    TaxExpenseBenefitContinuingOperations: float = Field(..., description="Income tax expense/(benefit). Common terms: tax expense, taxation, income tax, tax charge")
    ProfitLossFromDiscontinuedOperations: Optional[float] = Field(None, description="Profit/(loss) from discontinued operations. Common terms: discontinued operations, disposal group results")
    ProfitLoss: float = Field(..., description="Total comprehensive income for the period. Common terms: profit for the year, net profit, profit for the period, net income")
    ProfitLossAttributableToOwnersOfCompany: float = Field(..., description="Portion attributable to parent owners. Common terms: attributable to shareholders, equity holders, owners of the company")
    ProfitLossAttributableToNoncontrollingInterests: Optional[float] = Field(None, description="Portion attributable to NCI. Common terms: non-controlling interests, minority interest, minority shareholders")
    
    class Config:
        extra = "forbid"  # Equivalent to strict() in Zod

# Trade and Other Receivables
class TradeAndOtherReceivables(BaseModel):
    """Trade and other receivables detail"""
    TradeAndOtherReceivablesDueFromThirdParties: Optional[float] = Field(None,  description="Receivables from third parties. Common terms: third party receivables, external receivables")
    TradeAndOtherReceivablesDueFromRelatedParties: Optional[float] = Field(None,  description="Receivables from related parties. Common terms: related party receivables, intercompany receivables")
    UnbilledReceivables: Optional[float] = Field(None,  description="Unbilled receivables. Common terms: contract assets, accrued income, work completed not billed")
    OtherReceivables: Optional[float] = Field(None,  description="Other receivables. Common terms: sundry receivables, miscellaneous receivables, deposits")
    TradeAndOtherReceivables: float = Field(...,  description="Total trade and other receivables. Common terms: accounts receivable, debtors, total receivables")

# Trade and Other Payables
class TradeAndOtherPayables(BaseModel):
    """Trade and other payables detail"""
    TradeAndOtherPayablesDueToThirdParties: Optional[float] = Field(None,  description="Payables to third parties. Common terms: third party payables, external payables")
    TradeAndOtherPayablesDueToRelatedParties: Optional[float] = Field(None,  description="Payables to related parties. Common terms: related party payables, intercompany payables")
    DeferredIncome: Optional[float] = Field(None,  description="Deferred income. Common terms: unearned revenue, contract liabilities, advances from customers")
    OtherPayables: Optional[float] = Field(None,  description="Other payables. Common terms: sundry payables, accruals, other creditors")
    TradeAndOtherPayables: float = Field(...,  description="Total trade and other payables. Common terms: accounts payable, creditors, total payables")
    
    class Config:
        extra = "forbid"  # Equivalent to strict() in Zod

# Revenue
class Revenue(BaseModel):
    """Revenue detail"""
    RevenueFromPropertyTransferredAtPointInTime: Optional[float] = Field(None,  description="Revenue from property at point in time. Common terms: property sales, real estate sales")
    RevenueFromGoodsTransferredAtPointInTime: Optional[float] = Field(None,  description="Revenue from goods at point in time. Common terms: product sales, goods sold, merchandise sales")
    RevenueFromServicesTransferredAtPointInTime: Optional[float] = Field(None,  description="Revenue from services at point in time. Common terms: service fees, one-time services")
    RevenueFromPropertyTransferredOverTime: Optional[float] = Field(None,  description="Revenue from property over time. Common terms: development revenue, long-term property projects")
    RevenueFromConstructionContractsOverTime: Optional[float] = Field(None,  description="Revenue from construction contracts over time. Common terms: construction revenue, contract revenue")
    RevenueFromServicesTransferredOverTime: Optional[float] = Field(None,  description="Revenue from services over time. Common terms: recurring services, subscription revenue, ongoing services")
    OtherRevenue: Optional[float] = Field(None,  description="Other revenue. Common terms: miscellaneous revenue, other income streams")
    Revenue: float = Field(...,  description="Total revenue. Common terms: total revenue, turnover, sales, total income")
    
    class Config:
        extra = "forbid"  # Equivalent to strict() in Zod

class Notes(BaseModel):
    """Notes to financial statements"""
    TradeAndOtherReceivables: TradeAndOtherReceivables
    TradeAndOtherPayables: TradeAndOtherPayables
    Revenue: Revenue
    
    class Config:
        title = "Comprehensive financial statement schema compliant with Singapore Simplified XBRL requirements"

class PartialXBRL(BaseModel):
    """Singapore XBRL schema"""
    FilingInformation: FilingInformation
    DirectorsStatement: DirectorsStatement
    AuditReport: AuditReport
    StatementOfFinancialPosition: StatementOfFinancialPosition
    IncomeStatement: IncomeStatement
    Notes: Notes