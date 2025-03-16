"""
Models for XBRL tagging operations.
"""
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional


class FinancialTag(BaseModel):
    """Model for a single financial tag with standard XBRL attributes from Singapore ACRA taxonomy"""
    prefix: str = Field("sg-as", description="Taxonomy prefix (e.g., 'sg-as' for Singapore Account Standards)")
    element_name: str = Field(..., description="Official element name in the taxonomy (e.g., 'Revenue')")
    element_id: str = Field(..., description="Full element ID including prefix (e.g., 'sg-as_Revenue')")
    abstract: bool = Field(default=False, description="Whether tag represents an abstract concept")
    data_type: str = Field("xbrli:monetaryItemType", description="XBRL data type")
    balance_type: Optional[str] = Field(None, description="Balance type: 'debit' or 'credit'")
    period_type: str = Field("instant", description="Time period type: 'instant' or 'duration'")
    substitution_group: str = Field("xbrli:item", description="XBRL substitution group")


class TaggedValue(BaseModel):
    """A financial value with associated XBRL tags"""
    value: Any = Field(..., description="The financial value")
    tags: List[FinancialTag] = Field(default_factory=list, description="Tags associated with this element name")
    
    def add_tag(self, tag: FinancialTag) -> None:
        """Add a tag to this value"""
        self.tags.append(tag)
        
    def __str__(self):
        """String representation of the value"""
        return f"{self.value}"

#----------------------------------------------------------------------------------------------------------------------------------------------
# FILLING INFORMATION
#----------------------------------------------------------------------------------------------------------------------------------------------

class FilingInformationWithTags(BaseModel):
    """Filing information with tags"""
    NameOfCompany: TaggedValue
    UniqueEntityNumber: TaggedValue
    CurrentPeriodStartDate: TaggedValue
    CurrentPeriodEndDate: TaggedValue
    PriorPeriodStartDate: Optional[TaggedValue] = None
    TypeOfXBRLFiling: TaggedValue
    NatureOfFinancialStatementsCompanyLevelOrConsolidated: TaggedValue
    TypeOfAccountingStandardUsedToPrepareFinancialStatements: TaggedValue
    DateOfAuthorisationForIssueOfFinancialStatements: TaggedValue
    TypeOfStatementOfFinancialPosition: TaggedValue
    WhetherTheFinancialStatementsArePreparedOnGoingConcernBasis: TaggedValue
    WhetherThereAreAnyChangesToComparativeAmounts: Optional[TaggedValue] = None
    DescriptionOfPresentationCurrency: TaggedValue
    DescriptionOfFunctionalCurrency: TaggedValue
    LevelOfRoundingUsedInFinancialStatements: TaggedValue
    DescriptionOfNatureOfEntitysOperationsAndPrincipalActivities: TaggedValue
    PrincipalPlaceOfBusinessIfDifferentFromRegisteredOffice: TaggedValue
    WhetherCompanyOrGroupIfConsolidatedAccountsArePreparedHasMoreThan50Employees: TaggedValue
    NameOfParentEntity: Optional[TaggedValue] = None
    NameOfUltimateParentOfGroup: Optional[TaggedValue] = None
    TaxonomyVersion: TaggedValue
    NameAndVersionOfSoftwareUsedToGenerateXBRLFile: TaggedValue
    HowWasXBRLFilePrepared: TaggedValue
    meta_tags: List[FinancialTag] = Field(default_factory=list, description="Tags for the entire filing information")


class DirectorsStatementWithTags(BaseModel):
    """Directors' statement with tags"""
    WhetherInDirectorsOpinionFinancialStatementsAreDrawnUpSoAsToExhibitATrueAndFairView: TaggedValue
    WhetherThereAreReasonableGroundsToBelieveThatCompanyWillBeAbleToPayItsDebtsAsAndWhenTheyFallDueAtDateOfStatement: TaggedValue
    meta_tags: List[FinancialTag] = Field(default_factory=list, description="Tags for the entire directors' statement")


class AuditReportWithTags(BaseModel):
    """Audit report with tags"""
    TypeOfAuditOpinionInIndependentAuditorsReport: TaggedValue
    AuditingStandardsUsedToConductTheAudit: Optional[TaggedValue] = None
    WhetherThereIsAnyMaterialUncertaintyRelatingToGoingConcern: Optional[TaggedValue] = None
    WhetherInAuditorsOpinionAccountingAndOtherRecordsRequiredAreProperlyKept: Optional[TaggedValue] = None
    meta_tags: List[FinancialTag] = Field(default_factory=list, description="Tags for the entire audit report")

#----------------------------------------------------------------------------------------------------------------------------------------------
# STATEMENT OF FINANCIAL POSITION
#----------------------------------------------------------------------------------------------------------------------------------------------

# Current Assets with Tags
class CurrentAssetsWithTags(BaseModel):
    """Current assets section with tags"""
    CashAndBankBalances: Optional[TaggedValue] = None
    TradeAndOtherReceivablesCurrent: Optional[TaggedValue] = None
    CurrentFinanceLeaseReceivables: Optional[TaggedValue] = None
    CurrentDerivativeFinancialAssets: Optional[TaggedValue] = None
    CurrentFinancialAssetsMeasuredAtFairValueThroughProfitOrLoss: Optional[TaggedValue] = None
    OtherCurrentFinancialAssets: Optional[TaggedValue] = None
    DevelopmentProperties: Optional[TaggedValue] = None
    Inventories: Optional[TaggedValue] = None
    OtherCurrentNonfinancialAssets: Optional[TaggedValue] = None
    NoncurrentAssetsOrDisposalGroupsClassifiedAsHeldForSaleOrAsHeldForDistributionToOwners: Optional[TaggedValue] = None
    CurrentAssets: TaggedValue
    

# Non-Current Assets with Tags
class NonCurrentAssetsWithTags(BaseModel):
    """Non-current assets section with tags"""
    TradeAndOtherReceivablesNoncurrent: Optional[TaggedValue] = None
    NoncurrentFinanceLeaseReceivables: Optional[TaggedValue] = None
    NoncurrentDerivativeFinancialAssets: Optional[TaggedValue] = None
    NoncurrentFinancialAssetsMeasuredAtFairValueThroughProfitOrLoss: Optional[TaggedValue] = None
    OtherNoncurrentFinancialAssets: Optional[TaggedValue] = None
    PropertyPlantAndEquipment: Optional[TaggedValue] = None
    InvestmentProperties: Optional[TaggedValue] = None
    Goodwill: Optional[TaggedValue] = None
    IntangibleAssetsOtherThanGoodwill: Optional[TaggedValue] = None
    InvestmentsInSubsidiariesAssociatesOrJointVentures: Optional[TaggedValue] = None
    DeferredTaxAssets: Optional[TaggedValue] = None
    OtherNoncurrentNonfinancialAssets: Optional[TaggedValue] = None
    NoncurrentAssets: TaggedValue


# Current Liabilities with Tags
class CurrentLiabilitiesWithTags(BaseModel):
    """Current liabilities section with tags"""
    TradeAndOtherPayablesCurrent: Optional[TaggedValue] = None
    CurrentLoansAndBorrowings: Optional[TaggedValue] = None
    CurrentFinancialLiabilitiesMeasuredAtFairValueThroughProfitOrLoss: Optional[TaggedValue] = None
    CurrentFinanceLeaseLiabilities: Optional[TaggedValue] = None
    OtherCurrentFinancialLiabilities: Optional[TaggedValue] = None
    CurrentIncomeTaxLiabilities: Optional[TaggedValue] = None
    CurrentProvisions: Optional[TaggedValue] = None
    OtherCurrentNonfinancialLiabilities: Optional[TaggedValue] = None
    LiabilitiesClassifiedAsHeldForSale: Optional[TaggedValue] = None
    CurrentLiabilities: TaggedValue


# Non-Current Liabilities with Tags
class NonCurrentLiabilitiesWithTags(BaseModel):
    """Non-current liabilities section with tags"""
    TradeAndOtherPayablesNoncurrent: Optional[TaggedValue] = None
    NoncurrentLoansAndBorrowings: Optional[TaggedValue] = None
    NoncurrentFinancialLiabilitiesMeasuredAtFairValueThroughProfitOrLoss: Optional[TaggedValue] = None
    NoncurrentFinanceLeaseLiabilities: Optional[TaggedValue] = None
    OtherNoncurrentFinancialLiabilities: Optional[TaggedValue] = None
    DeferredTaxLiabilities: Optional[TaggedValue] = None
    NoncurrentProvisions: Optional[TaggedValue] = None
    OtherNoncurrentNonfinancialLiabilities: Optional[TaggedValue] = None
    NoncurrentLiabilities: TaggedValue


# Equity with Tags
class EquityWithTags(BaseModel):
    """Equity section with tags"""
    ShareCapital: TaggedValue
    TreasuryShares: Optional[TaggedValue] = None
    AccumulatedProfitsLosses: TaggedValue
    ReservesOtherThanAccumulatedProfitsLosses: Optional[TaggedValue] = None
    NoncontrollingInterests: Optional[TaggedValue] = None
    Equity: TaggedValue


# Statement of Financial Position with Tags
class StatementOfFinancialPositionWithTags(BaseModel):
    """Statement of financial position with tags"""
    currentAssets: CurrentAssetsWithTags
    nonCurrentAssets: NonCurrentAssetsWithTags
    Assets: TaggedValue
    currentLiabilities: CurrentLiabilitiesWithTags
    nonCurrentLiabilities: NonCurrentLiabilitiesWithTags  
    Liabilities: TaggedValue
    equity: EquityWithTags
    meta_tags: List[FinancialTag] = Field(default_factory=list, description="Tags for the entire statement")
    
    class Config:
        extra = "forbid"
        
    def validate_balance(self) -> bool:
        """
        Validate that Assets = Liabilities + Equity
        
        Returns:
            bool: True if balanced, False otherwise
        """
        # Allow for a small rounding difference
        tolerance = 0.01
        
        # Get values for comparison
        assets = self.Assets.value
        liabilities = self.Liabilities.value
        equity = self.equity.Equity.value
        
        balance_diff = abs(assets - (liabilities + equity))
        return balance_diff <= tolerance
    
    def add_meta_tag(self, tag: FinancialTag) -> None:
        """Add a statement-level tag"""
        self.meta_tags.append(tag)
    
    def get_all_tags(self) -> Dict[str, List[FinancialTag]]:
        """Get all tags organized by field path"""
        all_tags = {}
        
        # Add meta tags
        if self.meta_tags:
            all_tags["statement"] = self.meta_tags
        
        # Helper function to extract tags from a section
        def extract_section_tags(section, prefix):
            for field_name, field_value in section.__dict__.items():
                if isinstance(field_value, TaggedValue) and field_value.tags:
                    all_tags[f"{prefix}.{field_name}"] = field_value.tags
        
        # Extract tags from each section
        extract_section_tags(self.currentAssets, "currentAssets")
        extract_section_tags(self.nonCurrentAssets, "nonCurrentAssets")
        extract_section_tags(self.currentLiabilities, "currentLiabilities")
        extract_section_tags(self.nonCurrentLiabilities, "nonCurrentLiabilities")
        extract_section_tags(self.equity, "equity")
        
        # Add top-level fields
        if self.Assets.tags:
            all_tags["Assets"] = self.Assets.tags
        if self.Liabilities.tags:
            all_tags["Liabilities"] = self.Liabilities.tags
            
        return all_tags

#----------------------------------------------------------------------------------------------------------------------------------------------
# STATEMENT OF PROFIT OR LOSS
#----------------------------------------------------------------------------------------------------------------------------------------------

class StatementOfProfitOrLossWithTags(BaseModel):
    """Statement of Profit or Loss that supports tags on each field"""
    revenue: TaggedValue
    other_income: Optional[TaggedValue] = None
    employee_benefits_expense: Optional[TaggedValue] = None
    depreciation_expense: Optional[TaggedValue] = None
    amortisation_expense: Optional[TaggedValue] = None
    repairs_maintenance_expense: Optional[TaggedValue] = None
    sales_marketing_expense: Optional[TaggedValue] = None
    other_expenses: Optional[TaggedValue] = None
    other_gains_losses: Optional[TaggedValue] = None
    finance_costs_net: Optional[TaggedValue] = None
    share_of_profit_loss_associates: Optional[TaggedValue] = None
    profit_loss_before_taxation: TaggedValue
    income_tax_expense_benefit: TaggedValue
    profit_loss_discontinued_operations: Optional[TaggedValue] = None
    total_profit_loss: Optional[TaggedValue] = None
    profit_loss_attributable_to_owners: Optional[TaggedValue] = None
    profit_loss_attributable_to_non_controlling: Optional[TaggedValue] = None
    meta_tags: List[FinancialTag] = Field(default_factory=list, description="Tags for the entire statement")

#----------------------------------------------------------------------------------------------------------------------------------------------
# NOTES SECTION
#----------------------------------------------------------------------------------------------------------------------------------------------

# Notes section with tags
class TradeAndOtherReceivablesWithTags(BaseModel):
    """Trade and other receivables with tags"""
    TradeAndOtherReceivablesDueFromThirdParties: Optional[TaggedValue] = None
    TradeAndOtherReceivablesDueFromRelatedParties: Optional[TaggedValue] = None
    UnbilledReceivables: Optional[TaggedValue] = None
    OtherReceivables: Optional[TaggedValue] = None
    TradeAndOtherReceivables: TaggedValue
    meta_tags: List[FinancialTag] = Field(default_factory=list, description="Tags for trade and other receivables section")

class TradeAndOtherPayablesWithTags(BaseModel):
    """Trade and other payables with tags"""
    TradeAndOtherPayablesDueToThirdParties: Optional[TaggedValue] = None
    TradeAndOtherPayablesDueToRelatedParties: Optional[TaggedValue] = None
    DeferredIncome: Optional[TaggedValue] = None
    OtherPayables: Optional[TaggedValue] = None
    TradeAndOtherPayables: TaggedValue
    meta_tags: List[FinancialTag] = Field(default_factory=list, description="Tags for trade and other payables section")

class RevenueWithTags(BaseModel):
    """Revenue details with tags"""
    RevenueFromPropertyTransferredAtPointInTime: Optional[TaggedValue] = None
    RevenueFromGoodsTransferredAtPointInTime: Optional[TaggedValue] = None
    RevenueFromServicesTransferredAtPointInTime: Optional[TaggedValue] = None
    RevenueFromPropertyTransferredOverTime: Optional[TaggedValue] = None
    RevenueFromConstructionContractsOverTime: Optional[TaggedValue] = None
    RevenueFromServicesTransferredOverTime: Optional[TaggedValue] = None
    OtherRevenue: Optional[TaggedValue] = None
    Revenue: TaggedValue
    meta_tags: List[FinancialTag] = Field(default_factory=list, description="Tags for revenue section")

class NotesWithTags(BaseModel):
    """Notes to financial statements with tags"""
    tradeAndOtherReceivables: TradeAndOtherReceivablesWithTags
    tradeAndOtherPayables: TradeAndOtherPayablesWithTags
    revenue: RevenueWithTags
    meta_tags: List[FinancialTag] = Field(default_factory=list, description="Tags for the entire notes section")
    
    class Config:
        title = "Comprehensive financial statement schema with XBRL tags compliant with Singapore Simplified XBRL requirements"

#----------------------------------------------------------------------------------------------------------------------------------------------
# COMBINED MODEL
#----------------------------------------------------------------------------------------------------------------------------------------------

class PartialXBRLWithTags(BaseModel):
    """Singapore XBRL schema with tags"""
    filingInformation: FilingInformationWithTags
    directorsStatement: DirectorsStatementWithTags
    auditReport: AuditReportWithTags
    statementOfFinancialPosition: StatementOfFinancialPositionWithTags
    incomeStatement: StatementOfProfitOrLossWithTags
    notes: NotesWithTags
    meta_tags: List[FinancialTag] = Field(default_factory=list, description="Tags for the entire XBRL document")
    
    def get_all_tags(self) -> Dict[str, List[FinancialTag]]:
        """Get all tags organized by field path"""
        all_tags = {}
        
        # Add document-level meta tags
        if self.meta_tags:
            all_tags["document"] = self.meta_tags
            
        # Add section-level meta tags
        if self.filingInformation.meta_tags:
            all_tags["filingInformation"] = self.filingInformation.meta_tags
        if self.directorsStatement.meta_tags:
            all_tags["directorsStatement"] = self.directorsStatement.meta_tags
        if self.auditReport.meta_tags:
            all_tags["auditReport"] = self.auditReport.meta_tags
        if self.statementOfFinancialPosition.meta_tags:
            all_tags["statementOfFinancialPosition"] = self.statementOfFinancialPosition.meta_tags
        if self.incomeStatement.meta_tags:
            all_tags["incomeStatement"] = self.incomeStatement.meta_tags
        if self.notes.meta_tags:
            all_tags["notes"] = self.notes.meta_tags
            
        # Add field-level tags from each section using a recursive helper function
        def extract_tagged_values(obj, prefix=""):
            for field_name, field_value in obj.__dict__.items():
                if field_name == "meta_tags":
                    continue
                    
                field_path = f"{prefix}.{field_name}" if prefix else field_name
                
                if isinstance(field_value, TaggedValue) and field_value.tags:
                    all_tags[field_path] = field_value.tags
                elif isinstance(field_value, BaseModel):
                    extract_tagged_values(field_value, field_path)
        
        # Extract tags from each section
        extract_tagged_values(self.filingInformation, "filingInformation")
        extract_tagged_values(self.directorsStatement, "directorsStatement")
        extract_tagged_values(self.auditReport, "auditReport")
        extract_tagged_values(self.statementOfFinancialPosition, "statementOfFinancialPosition")
        extract_tagged_values(self.incomeStatement, "incomeStatement") 
        extract_tagged_values(self.notes, "notes")
        
        return all_tags
