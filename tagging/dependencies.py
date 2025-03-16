"""
Dependencies for XBRL tagging operations.
"""
from dataclasses import dataclass
from typing import Dict, List, Optional
from .models import FinancialTag

# Tagging Dependencies
@dataclass
class XBRLTaxonomyDependencies:
    """Dependencies for XBRL tagging operations"""
    taxonomy_name: str
    entity_name: str
    mandatory_fields: Dict[str, bool]
    field_tags: Dict[str, List[FinancialTag]]
    statement_tags: List[FinancialTag]
    reporting_year: Optional[str] = None # Set to None since we're not using it currently

# Filing information XBRL taxonomy tags

SG_XBRL_FILING_TAGS = {
    "DisclosureOfFilingInformationAbstract": [
        FinancialTag(
            prefix="sg-dei",
            element_name="DisclosureOfFilingInformationAbstract",
            element_id="sg-dei_DisclosureOfFilingInformationAbstract",
            abstract=True,
            data_type="xbrli:stringItemType",
            balance_type=None,
            period_type="duration",
            substitution_group="xbrli:item",
            description="Abstract container element for filing information section that groups related disclosure items"
        )
    ],
    "NameOfCompany": [
        FinancialTag(
            prefix="sg-dei",
            element_name="NameOfCompany",
            element_id="sg-dei_NameOfCompany",
            abstract=False,
            data_type="xbrli:stringItemType",
            balance_type=None,
            period_type="duration",
            substitution_group="xbrli:item",
            description="The legal registered name of the entity filing the financial statements as recorded with ACRA"
        )
    ],
    "UniqueEntityNumber": [
        FinancialTag(
            prefix="sg-dei",
            element_name="UniqueEntityNumber",
            element_id="sg-dei_UniqueEntityNumber",
            abstract=False,
            data_type="sg-types:UENItemType",
            balance_type=None,
            period_type="duration",
            substitution_group="xbrli:item",
            description="The Unique Entity Number (UEN) issued by ACRA, formatted as 8 digits followed by 1 uppercase letter"
        )
    ],
    "CurrentPeriodStartDate": [
        FinancialTag(
            prefix="sg-dei",
            element_name="CurrentPeriodStartDate",
            element_id="sg-dei_CurrentPeriodStartDate",
            abstract=False,
            data_type="xbrli:dateItemType",
            balance_type=None,
            period_type="instant",
            substitution_group="xbrli:item",
            description="The first day of the current financial reporting period (e.g., January 1, 2023)"
        )
    ],
    "CurrentPeriodEndDate": [
        FinancialTag(
            prefix="sg-dei",
            element_name="CurrentPeriodEndDate",
            element_id="sg-dei_CurrentPeriodEndDate",
            abstract=False,
            data_type="xbrli:dateItemType",
            balance_type=None,
            period_type="instant",
            substitution_group="xbrli:item",
            description="The last day of the current financial reporting period (e.g., December 31, 2023)"
        )
    ],
    "PriorPeriodStartDate": [
        FinancialTag(
            prefix="sg-dei",
            element_name="PriorPeriodStartDate",
            element_id="sg-dei_PriorPeriodStartDate",
            abstract=False,
            data_type="xbrli:dateItemType",
            balance_type=None,
            period_type="instant",
            substitution_group="xbrli:item",
            description="The first day of the previous financial reporting period used for comparative figures"
        )
    ],
    "TypeOfXBRLFiling": [
        FinancialTag(
            prefix="sg-dei",
            element_name="TypeOfXBRLFiling",
            element_id="sg-dei_TypeOfXBRLFiling",
            abstract=False,
            data_type="sg-types:XBRLFilingItemType",
            balance_type=None,
            period_type="duration",
            substitution_group="xbrli:item",
            description="Indicates whether the filing contains full or partial XBRL information (Full/Partial)"
        )
    ],
    "NatureOfFinancialStatementsCompanyLevelOrConsolidated": [
        FinancialTag(
            prefix="sg-dei",
            element_name="NatureOfFinancialStatementsCompanyLevelOrConsolidated",
            element_id="sg-dei_NatureOfFinancialStatementsCompanyLevelOrConsolidated",
            abstract=False,
            data_type="sg-types:NatureOfFinancialStatementsItemType",
            balance_type=None,
            period_type="duration",
            substitution_group="xbrli:item",
            description="Specifies whether the statements are for the company alone (separate) or for the consolidated group"
        )
    ],
    "TypeOfAccountingStandardUsedToPrepareFinancialStatements": [
        FinancialTag(
            prefix="sg-dei",
            element_name="TypeOfAccountingStandardUsedToPrepareFinancialStatements",
            element_id="sg-dei_TypeOfAccountingStandardUsedToPrepareFinancialStatements",
            abstract=False,
            data_type="sg-types:AccountingStandardsItemType",
            balance_type=None,
            period_type="duration",
            substitution_group="xbrli:item",
            description="The accounting standards framework used to prepare the financial statements (SFRS, SFRS for SE, IFRS, or Other)"
        )
    ],
    "DateOfAuthorisationForIssueOfFinancialStatements": [
        FinancialTag(
            prefix="sg-as",
            element_name="DateOfAuthorisationForIssueOfFinancialStatements",
            element_id="sg-as_DateOfAuthorisationForIssueOfFinancialStatements",
            abstract=False,
            data_type="xbrli:dateItemType",
            balance_type=None,
            period_type="instant",
            substitution_group="xbrli:item",
            description="Date when the directors authorized the financial statements for issuance, typically the board approval date"
        )
    ],
    "TypeOfStatementOfFinancialPosition": [
        FinancialTag(
            prefix="sg-dei",
            element_name="TypeOfStatementOfFinancialPosition",
            element_id="sg-dei_TypeOfStatementOfFinancialPosition",
            abstract=False,
            data_type="sg-types:StatementOfFinancialPositionItemType",
            balance_type=None,
            period_type="duration",
            substitution_group="xbrli:item",
            description="Format used for the balance sheet - either classified (current/non-current) or liquidity-based"
        )
    ],
    "WhetherFinancialStatementsArePreparedOnGoingConcernBasis": [
        FinancialTag(
            prefix="sg-dei",
            element_name="WhetherFinancialStatementsArePreparedOnGoingConcernBasis",
            element_id="sg-dei_WhetherFinancialStatementsArePreparedOnGoingConcernBasis",
            abstract=False,
            data_type="sg-types:YesNoItemType",
            balance_type=None,
            period_type="duration",
            substitution_group="xbrli:item",
            description="Indicates whether the entity is considered a going concern for the preparation of financial statements"
        )
    ],
    "WhetherThereAreChangesToComparativeAmountsDueToRestatementsReclassificationOrOtherReasons": [
        FinancialTag(
            prefix="sg-dei",
            element_name="WhetherThereAreChangesToComparativeAmountsDueToRestatementsReclassificationOrOtherReasons",
            element_id="sg-dei_WhetherThereAreChangesToComparativeAmountsDueToRestatementsReclassificationOrOtherReasons",
            abstract=False,
            data_type="sg-types:YesNoItemType",
            balance_type=None,
            period_type="duration",
            substitution_group="xbrli:item",
            description="Indicates if prior year figures have been restated, reclassified, or otherwise modified"
        )
    ],
    "DescriptionOfPresentationCurrency": [
        FinancialTag(
            prefix="sg-dei",
            element_name="DescriptionOfPresentationCurrency",
            element_id="sg-dei_DescriptionOfPresentationCurrency",
            abstract=False,
            data_type="sg-types:CurrencyCodeItemType",
            balance_type=None,
            period_type="duration",
            substitution_group="xbrli:item",
            description="The ISO 4217 currency code used for presenting the financial statements (e.g., SGD, USD)"
        )
    ],
    "DescriptionOfFunctionalCurrency": [
        FinancialTag(
            prefix="sg-as",
            element_name="DescriptionOfFunctionalCurrency",
            element_id="sg-as_DescriptionOfFunctionalCurrency",
            abstract=False,
            data_type="sg-types:CurrencyCodeItemType",
            balance_type=None,
            period_type="duration",
            substitution_group="xbrli:item",
            description="The ISO 4217 currency code of the primary economic environment in which the entity operates"
        )
    ],
    "LevelOfRoundingUsedInFinancialStatements": [
        FinancialTag(
            prefix="sg-dei",
            element_name="LevelOfRoundingUsedInFinancialStatements",
            element_id="sg-dei_LevelOfRoundingUsedInFinancialStatements",
            abstract=False,
            data_type="sg-types:LevelOfRoundingItemType",
            balance_type=None,
            period_type="duration",
            substitution_group="xbrli:item",
            description="The level of rounding applied to numeric values (Units, Thousands, Millions)"
        )
    ],
    "DescriptionOfNatureOfEntitysOperationsAndPrincipalActivities": [
        FinancialTag(
            prefix="sg-as",
            element_name="DescriptionOfNatureOfEntitysOperationsAndPrincipalActivities",
            element_id="sg-as_DescriptionOfNatureOfEntitysOperationsAndPrincipalActivities",
            abstract=False,
            data_type="xbrli:stringItemType",
            balance_type=None,
            period_type="duration",
            substitution_group="xbrli:item",
            description="A brief description of the company's main business activities and operations"
        )
    ],
    "PrincipalPlaceOfBusinessIfDifferentFromRegisteredOffice": [
        FinancialTag(
            prefix="sg-as",
            element_name="PrincipalPlaceOfBusinessIfDifferentFromRegisteredOffice",
            element_id="sg-as_PrincipalPlaceOfBusinessIfDifferentFromRegisteredOffice",
            abstract=False,
            data_type="xbrli:stringItemType",
            balance_type=None,
            period_type="duration",
            substitution_group="xbrli:item",
            description="The main location where business is conducted if different from the registered office address"
        )
    ],
    "WhetherCompanyOrGroupIfConsolidatedAccountsArePreparedHasMoreThan50Employees": [
        FinancialTag(
            prefix="sg-dei",
            element_name="WhetherCompanyOrGroupIfConsolidatedAccountsArePreparedHasMoreThan50Employees",
            element_id="sg-dei_WhetherCompanyOrGroupIfConsolidatedAccountsArePreparedHasMoreThan50Employees",
            abstract=False,
            data_type="sg-types:YesNoItemType",
            balance_type=None,
            period_type="duration",
            substitution_group="xbrli:item",
            description="Indicates whether the company or group has more than 50 employees, affecting certain disclosure requirements"
        )
    ],
    "NameOfParentEntity": [
        FinancialTag(
            prefix="sg-as",
            element_name="NameOfParentEntity",
            element_id="sg-as_NameOfParentEntity",
            abstract=False,
            data_type="xbrli:stringItemType",
            balance_type=None,
            period_type="duration",
            substitution_group="xbrli:item",
            description="The name of the immediate parent company that owns or controls the reporting entity"
        )
    ],
    "NameOfUltimateParentOfGroup": [
        FinancialTag(
            prefix="sg-as",
            element_name="NameOfUltimateParentOfGroup",
            element_id="sg-as_NameOfUltimateParentOfGroup",
            abstract=False,
            data_type="xbrli:stringItemType",
            balance_type=None,
            period_type="duration",
            substitution_group="xbrli:item",
            description="The name of the topmost parent company in the corporate structure that ultimately controls the reporting entity"
        )
    ],
    "DetailsOfInstanceDocumentAbstract": [
        FinancialTag(
            prefix="sg-dei",
            element_name="DetailsOfInstanceDocumentAbstract",
            element_id="sg-dei_DetailsOfInstanceDocumentAbstract",
            abstract=True,
            data_type="xbrli:stringItemType",
            balance_type=None,
            period_type="duration",
            substitution_group="xbrli:item",
            description="Abstract container element that groups technical information about the XBRL instance document"
        )
    ],
    "TaxonomyVersion": [
        FinancialTag(
            prefix="sg-dei",
            element_name="TaxonomyVersion",
            element_id="sg-dei_TaxonomyVersion",
            abstract=False,
            data_type="sg-types:TaxonomyVersionItemType",
            balance_type=None,
            period_type="duration",
            substitution_group="xbrli:item",
            description="The version of the ACRA XBRL taxonomy used for preparing the filing (e.g., 2022.2)"
        )
    ],
    "NameAndVersionOfSoftwareUsedToGenerateInstanceDocument": [
        FinancialTag(
            prefix="sg-dei",
            element_name="NameAndVersionOfSoftwareUsedToGenerateInstanceDocument",
            element_id="sg-dei_NameAndVersionOfSoftwareUsedToGenerateInstanceDocument",
            abstract=False,
            data_type="xbrli:stringItemType",
            balance_type=None,
            period_type="duration",
            substitution_group="xbrli:item",
            description="Information about the software application and version used to create the XBRL filing"
        )
    ],
    "HowWasXBRLInstanceDocumentPrepared": [
        FinancialTag(
            prefix="sg-dei",
            element_name="HowWasXBRLInstanceDocumentPrepared",
            element_id="sg-dei_HowWasXBRLInstanceDocumentPrepared",
            abstract=False,
            data_type="sg-types:PreparationOfXBRLFileItemType",
            balance_type=None,
            period_type="duration",
            substitution_group="xbrli:item",
            description="The method used to create the XBRL filing (Automated, Manual, or Hybrid)"
        )
    ]
}
# statement-level tags
SG_XBRL_FILING_STATEMENT_TAGS = [
    FinancialTag(
        prefix="sg-dei",
        element_name="DisclosureOfFilingInformationAbstract",
        element_id="sg-dei_DisclosureOfFilingInformationAbstract",
        abstract=True,
        data_type="xbrli:stringItemType",
        balance_type=None,
        period_type="duration",
        substitution_group="xbrli:item",
        description="Abstract container element that represents the entire filing information section of the report"
    ),
    FinancialTag(
        prefix="sg-dei",
        element_name="DetailsOfInstanceDocumentAbstract",
        element_id="sg-dei_DetailsOfInstanceDocumentAbstract",
        abstract=True,
        data_type="xbrli:stringItemType",
        balance_type=None,
        period_type="duration",
        substitution_group="xbrli:item",
        description="Abstract container element that groups technical metadata about the XBRL document itself"
    )
]

MANDATORY_FILING_TAGS = {
    "NameOfCompany": True,
    "UniqueEntityNumber": True,
    "CurrentPeriodStartDate": True,
    "CurrentPeriodEndDate": True,
    "TypeOfXBRLFiling": True,
    "NatureOfFinancialStatementsCompanyLevelOrConsolidated": True,
    "TypeOfAccountingStandardUsedToPrepareFinancialStatements": True,
    "DateOfAuthorisationForIssueOfFinancialStatements": True,
    "TypeOfStatementOfFinancialPosition": True,
    "WhetherFinancialStatementsArePreparedOnGoingConcernBasis": True,
    "DescriptionOfPresentationCurrency": True,
    "DescriptionOfFunctionalCurrency": True,
    "LevelOfRoundingUsedInFinancialStatements": True,
    "DescriptionOfNatureOfEntitysOperationsAndPrincipalActivities": True,
    "PrincipalPlaceOfBusinessIfDifferentFromRegisteredOffice": True,
    "WhetherCompanyOrGroupIfConsolidatedAccountsArePreparedHasMoreThan50Employees": True,
    "TaxonomyVersion": True
}

#----------------------------------------------------------------------------------------------------------------------------------------------
# Statement by directors XBRL taxonomy tags
#----------------------------------------------------------------------------------------------------------------------------------------------

SG_XBRL_DIRECTORS_TAGS = {
    "DisclosureInStatementByDirectorsAbstract": [
        FinancialTag(
            prefix="sg-dei",
            element_name="DisclosureInStatementByDirectorsAbstract",
            element_id="sg-dei_DisclosureInStatementByDirectorsAbstract",
            abstract=True,
            data_type="xbrli:stringItemType",
            balance_type=None,
            period_type="duration",
            substitution_group="xbrli:item",
            description="Abstract container element that groups all directors' statement disclosures"
        )
    ],
    "WhetherInDirectorsOpinionFinancialStatementsAreDrawnUpSoAsToExhibitATrueAndFairView": [
        FinancialTag(
            prefix="sg-dei",
            element_name="WhetherInDirectorsOpinionFinancialStatementsAreDrawnUpSoAsToExhibitATrueAndFairView",
            element_id="sg-dei_WhetherInDirectorsOpinionFinancialStatementsAreDrawnUpSoAsToExhibitATrueAndFairView",
            abstract=False,
            data_type="sg-types:YesNoItemType",
            balance_type=None,
            period_type="duration",
            substitution_group="xbrli:item",
            description="Directors' confirmation that financial statements give a true and fair view of the company's financial position and performance"
        )
    ],
    "WhetherThereAreReasonableGroundsToBelieveThatCompanyWillBeAbleToPayItsDebtsAsAndWhenTheyFallDueAtDateOfStatement": [
        FinancialTag(
            prefix="sg-dei",
            element_name="WhetherThereAreReasonableGroundsToBelieveThatCompanyWillBeAbleToPayItsDebtsAsAndWhenTheyFallDueAtDateOfStatement",
            element_id="sg-dei_WhetherThereAreReasonableGroundsToBelieveThatCompanyWillBeAbleToPayItsDebtsAsAndWhenTheyFallDueAtDateOfStatement",
            abstract=False,
            data_type="sg-types:YesNoItemType",
            balance_type=None,
            period_type="duration",
            substitution_group="xbrli:item",
            description="Directors' assessment of the company's solvency and ability to pay debts when due (going concern statement)"
        )
    ]
}

# statement-level tags
SG_XBRL_DIRECTORS_STATEMENT_TAGS = [
    FinancialTag(
        prefix="sg-dei",
        element_name="DisclosureInStatementByDirectorsAbstract",
        element_id="sg-dei_DisclosureInStatementByDirectorsAbstract",
        abstract=True,
        data_type="xbrli:stringItemType",
        balance_type=None,
        period_type="duration",
        substitution_group="xbrli:item",
        description="Parent container for the entire statement by directors section"
    )
]

MANDATORY_DIRECTORS_TAGS = {
    "WhetherInDirectorsOpinionFinancialStatementsAreDrawnUpSoAsToExhibitATrueAndFairView": True,
    "WhetherThereAreReasonableGroundsToBelieveThatCompanyWillBeAbleToPayItsDebtsAsAndWhenTheyFallDueAtDateOfStatement": True
}

#----------------------------------------------------------------------------------------------------------------------------------------------
# Independent auditors' report XBRL taxonomy tags
#----------------------------------------------------------------------------------------------------------------------------------------------

SG_XBRL_AUDIT_TAGS = {
    "DisclosuresInIndependentAuditorsReportAbstract": [
        FinancialTag(
            prefix="sg-ssa",
            element_name="DisclosuresInIndependentAuditorsReportAbstract",
            element_id="sg-ssa_DisclosuresInIndependentAuditorsReportAbstract",
            abstract=True,
            data_type="xbrli:stringItemType",
            balance_type=None,
            period_type="duration",
            substitution_group="xbrli:item",
            description="Abstract container element that groups all disclosures related to the independent auditors' report"
        )
    ],
    "TypeOfAuditOpinionInIndependentAuditorsReport": [
        FinancialTag(
            prefix="sg-ssa",
            element_name="TypeOfAuditOpinionInIndependentAuditorsReport",
            element_id="sg-ssa_TypeOfAuditOpinionInIndependentAuditorsReport",
            abstract=False,
            data_type="xbrli:stringItemType",
            balance_type=None,
            period_type="duration",
            substitution_group="xbrli:item",
            description="The type of opinion expressed by the auditor in their report (Unqualified, Qualified, Adverse, or Disclaimer of Opinion)"
        )
    ],
    "AuditingStandardsUsedToConductAudit": [
        FinancialTag(
            prefix="sg-ssa",
            element_name="AuditingStandardsUsedToConductAudit",
            element_id="sg-ssa_AuditingStandardsUsedToConductAudit",
            abstract=False,
            data_type="xbrli:stringItemType",
            balance_type=None,
            period_type="duration",
            substitution_group="xbrli:item",
            description="The framework of auditing standards used to conduct the audit (e.g., Singapore Standards on Auditing, International Standards on Auditing)"
        )
    ],
    "WhetherThereIsAnyMaterialUncertaintyRelatingToGoingConcern": [
        FinancialTag(
            prefix="sg-ssa",
            element_name="WhetherThereIsAnyMaterialUncertaintyRelatingToGoingConcern",
            element_id="sg-ssa_WhetherThereIsAnyMaterialUncertaintyRelatingToGoingConcern",
            abstract=False,
            data_type="sg-types:YesNoItemType",
            balance_type=None,
            period_type="duration",
            substitution_group="xbrli:item",
            description="Indicates whether the auditor has identified any material uncertainty related to events or conditions that may cast significant doubt on the entity's ability to continue as a going concern"
        )
    ],
    "WhetherInAuditorsOpinionAccountingAndOtherRecordsRequiredAreProperlyKeptInAccordanceWithCompaniesAct": [
        FinancialTag(
            prefix="sg-ssa",
            element_name="WhetherInAuditorsOpinionAccountingAndOtherRecordsRequiredAreProperlyKeptInAccordanceWithCompaniesAct",
            element_id="sg-ssa_WhetherInAuditorsOpinionAccountingAndOtherRecordsRequiredAreProperlyKeptInAccordanceWithCompaniesAct",
            abstract=False,
            data_type="sg-types:YesNoItemType",
            balance_type=None,
            period_type="duration",
            substitution_group="xbrli:item",
            description="The auditor's opinion on whether proper accounting and other records have been kept by the company as required by the Singapore Companies Act"
        )
    ]
}

# statement-level tags
SG_XBRL_AUDIT_STATEMENT_TAGS = [
    FinancialTag(
        prefix="sg-ssa",
        element_name="DisclosuresInIndependentAuditorsReportAbstract",
        element_id="sg-ssa_DisclosuresInIndependentAuditorsReportAbstract",
        abstract=True,
        data_type="xbrli:stringItemType",
        balance_type=None,
        period_type="duration",
        substitution_group="xbrli:item",
        description="Parent container element for the entire independent auditors' report section"
    )
]

MANDATORY_AUDIT_TAGS = {
    "TypeOfAuditOpinionInIndependentAuditorsReport": True,
    "AuditingStandardsUsedToConductAudit": False,  # Optional based on Tag.md
    "WhetherThereIsAnyMaterialUncertaintyRelatingToGoingConcern": False,  # Optional based on Tag.md
    "WhetherInAuditorsOpinionAccountingAndOtherRecordsRequiredAreProperlyKeptInAccordanceWithCompaniesAct": False  # Optional based on Tag.md
}

#----------------------------------------------------------------------------------------------------------------------------------------------
# Statement of financial position XBRL taxonomy tags - Assets section
#----------------------------------------------------------------------------------------------------------------------------------------------

SG_XBRL_FINANCIAL_POSITION_TAGS = {
    "StatementOfFinancialPositionLineItems": [
        FinancialTag(
            prefix="sg-as",
            element_name="StatementOfFinancialPositionLineItems",
            element_id="sg-as_StatementOfFinancialPositionLineItems",
            abstract=True,
            data_type="xbrli:stringItemType",
            balance_type=None,
            period_type="duration",
            substitution_group="xbrli:item",
            description="Abstract container for all statement of financial position line items"
        )
    ],
    "AssetsAbstract": [
        FinancialTag(
            prefix="sg-as",
            element_name="AssetsAbstract",
            element_id="sg-as_AssetsAbstract",
            abstract=True,
            data_type="xbrli:stringItemType",
            balance_type=None,
            period_type="duration",
            substitution_group="xbrli:item",
            description="Abstract container for all asset categories (current and non-current)"
        )
    ],
    "CurrentAssetsAbstract": [
        FinancialTag(
            prefix="sg-as",
            element_name="CurrentAssetsAbstract",
            element_id="sg-as_CurrentAssetsAbstract",
            abstract=True,
            data_type="xbrli:stringItemType",
            balance_type=None,
            period_type="duration",
            substitution_group="xbrli:item",
            description="Abstract container for assets expected to be converted into cash or consumed within one year"
        )
    ],
    "CashAndBankBalances": [
        FinancialTag(
            prefix="sg-as",
            element_name="CashAndBankBalances",
            element_id="sg-as_CashAndBankBalances",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="debit",
            period_type="instant",
            substitution_group="xbrli:item",
            description="Cash on hand and demand deposits with banks, including short-term highly liquid investments"
        )
    ],
    "TradeAndOtherReceivablesCurrent": [
        FinancialTag(
            prefix="sg-as",
            element_name="TradeAndOtherReceivablesCurrent",
            element_id="sg-as_TradeAndOtherReceivablesCurrent",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="debit",
            period_type="instant",
            substitution_group="xbrli:item",
            description="Amounts due from customers for goods sold or services rendered and other short-term receivables"
        )
    ],
    "CurrentFinanceLeaseReceivables": [
        FinancialTag(
            prefix="sg-as",
            element_name="CurrentFinanceLeaseReceivables",
            element_id="sg-as_CurrentFinanceLeaseReceivables",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="debit",
            period_type="instant",
            substitution_group="xbrli:item",
            description="Current portion of finance lease receivables where the entity is the lessor"
        )
    ],
    "CurrentDerivativeFinancialAssets": [
        FinancialTag(
            prefix="sg-as",
            element_name="CurrentDerivativeFinancialAssets",
            element_id="sg-as_CurrentDerivativeFinancialAssets",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="debit",
            period_type="instant",
            substitution_group="xbrli:item",
            description="Current derivative instruments with positive fair values (e.g., forwards, swaps, options)"
        )
    ],
    "CurrentFinancialAssetsMeasuredAtFairValueThroughProfitOrLoss": [
        FinancialTag(
            prefix="sg-as",
            element_name="CurrentFinancialAssetsMeasuredAtFairValueThroughProfitOrLoss",
            element_id="sg-as_CurrentFinancialAssetsMeasuredAtFairValueThroughProfitOrLoss",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="debit",
            period_type="instant",
            substitution_group="xbrli:item",
            description="Current financial assets designated or classified as at fair value through profit or loss"
        )
    ],
    "OtherCurrentFinancialAssets": [
        FinancialTag(
            prefix="sg-as",
            element_name="OtherCurrentFinancialAssets",
            element_id="sg-as_OtherCurrentFinancialAssets",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="debit",
            period_type="instant",
            substitution_group="xbrli:item",
            description="Other current financial assets not specifically classified elsewhere"
        )
    ],
    "DevelopmentProperties": [
        FinancialTag(
            prefix="sg-as",
            element_name="DevelopmentProperties",
            element_id="sg-as_DevelopmentProperties",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="debit",
            period_type="instant",
            substitution_group="xbrli:item",
            description="Properties acquired or being constructed for sale in the ordinary course of business"
        )
    ],
    "Inventories": [
        FinancialTag(
            prefix="sg-as",
            element_name="Inventories",
            element_id="sg-as_Inventories",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="debit",
            period_type="instant",
            substitution_group="xbrli:item",
            description="Assets held for sale in ordinary course of business, in production, or as materials to be consumed"
        )
    ],
    "OtherCurrentNonfinancialAssets": [
        FinancialTag(
            prefix="sg-as",
            element_name="OtherCurrentNonfinancialAssets",
            element_id="sg-as_OtherCurrentNonfinancialAssets",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="debit",
            period_type="instant",
            substitution_group="xbrli:item",
            description="Other current non-financial assets such as prepayments and advances"
        )
    ],
    "NoncurrentAssetsOrDisposalGroupsClassifiedAsHeldForSaleOrAsHeldForDistributionToOwners": [
        FinancialTag(
            prefix="sg-as",
            element_name="NoncurrentAssetsOrDisposalGroupsClassifiedAsHeldForSaleOrAsHeldForDistributionToOwners",
            element_id="sg-as_NoncurrentAssetsOrDisposalGroupsClassifiedAsHeldForSaleOrAsHeldForDistributionToOwners",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="debit",
            period_type="instant",
            substitution_group="xbrli:item",
            description="Non-current assets or disposal groups held for sale or distribution to owners"
        )
    ],
    "CurrentAssets": [
        FinancialTag(
            prefix="sg-as",
            element_name="CurrentAssets",
            element_id="sg-as_CurrentAssets",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="debit",
            period_type="instant",
            substitution_group="xbrli:item",
            description="Total of all current assets expected to be converted to cash or consumed within one operating cycle"
        )
    ],
    "NoncurrentAssetsAbstract": [
        FinancialTag(
            prefix="sg-as",
            element_name="NoncurrentAssetsAbstract",
            element_id="sg-as_NoncurrentAssetsAbstract",
            abstract=True,
            data_type="xbrli:stringItemType",
            balance_type=None,
            period_type="duration",
            substitution_group="xbrli:item",
            description="Abstract container for assets not expected to be converted into cash within one year"
        )
    ],
    "TradeAndOtherReceivablesNoncurrent": [
        FinancialTag(
            prefix="sg-as",
            element_name="TradeAndOtherReceivablesNoncurrent",
            element_id="sg-as_TradeAndOtherReceivablesNoncurrent",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="debit",
            period_type="instant",
            substitution_group="xbrli:item",
            description="Long-term receivables not expected to be collected within one year"
        )
    ],
    "NoncurrentFinanceLeaseReceivables": [
        FinancialTag(
            prefix="sg-as",
            element_name="NoncurrentFinanceLeaseReceivables",
            element_id="sg-as_NoncurrentFinanceLeaseReceivables",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="debit",
            period_type="instant",
            substitution_group="xbrli:item",
            description="Long-term portion of finance lease receivables where the entity is the lessor"
        )
    ],
    "NoncurrentDerivativeFinancialAssets": [
        FinancialTag(
            prefix="sg-as",
            element_name="NoncurrentDerivativeFinancialAssets",
            element_id="sg-as_NoncurrentDerivativeFinancialAssets",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="debit",
            period_type="instant",
            substitution_group="xbrli:item",
            description="Long-term derivative instruments with positive fair values (e.g., interest rate swaps)"
        )
    ],
    "NoncurrentFinancialAssetsMeasuredAtFairValueThroughProfitOrLoss": [
        FinancialTag(
            prefix="sg-as",
            element_name="NoncurrentFinancialAssetsMeasuredAtFairValueThroughProfitOrLoss",
            element_id="sg-as_NoncurrentFinancialAssetsMeasuredAtFairValueThroughProfitOrLoss",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="debit",
            period_type="instant",
            substitution_group="xbrli:item",
            description="Long-term financial assets designated or classified as at fair value through profit or loss"
        )
    ],
    "OtherNoncurrentFinancialAssets": [
        FinancialTag(
            prefix="sg-as",
            element_name="OtherNoncurrentFinancialAssets",
            element_id="sg-as_OtherNoncurrentFinancialAssets",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="debit",
            period_type="instant",
            substitution_group="xbrli:item",
            description="Other long-term financial assets not specifically classified elsewhere"
        )
    ],
    "PropertyPlantAndEquipment": [
        FinancialTag(
            prefix="sg-as",
            element_name="PropertyPlantAndEquipment",
            element_id="sg-as_PropertyPlantAndEquipment",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="debit",
            period_type="instant",
            substitution_group="xbrli:item",
            description="Tangible assets used in operations over more than one period (e.g., land, buildings, machinery)"
        )
    ],
    "InvestmentProperties": [
        FinancialTag(
            prefix="sg-as",
            element_name="InvestmentProperties",
            element_id="sg-as_InvestmentProperties",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="debit",
            period_type="instant",
            substitution_group="xbrli:item",
            description="Properties held to earn rentals or for capital appreciation rather than for use in production"
        )
    ],
    "Goodwill": [
        FinancialTag(
            prefix="sg-as",
            element_name="Goodwill",
            element_id="sg-as_Goodwill",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="debit",
            period_type="instant",
            substitution_group="xbrli:item",
            description="An asset representing future economic benefits arising from other assets acquired in a business combination"
        )
    ],
    "IntangibleAssetsOtherThanGoodwill": [
        FinancialTag(
            prefix="sg-as",
            element_name="IntangibleAssetsOtherThanGoodwill",
            element_id="sg-as_IntangibleAssetsOtherThanGoodwill",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="debit",
            period_type="instant",
            substitution_group="xbrli:item",
            description="Identifiable non-monetary assets without physical substance (e.g., patents, trademarks, software)"
        )
    ],
    "InvestmentsInSubsidiariesAssociatesOrJointVentures": [
        FinancialTag(
            prefix="sg-as",
            element_name="InvestmentsInSubsidiariesAssociatesOrJointVentures",
            element_id="sg-as_InvestmentsInSubsidiariesAssociatesOrJointVentures",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="debit",
            period_type="instant",
            substitution_group="xbrli:item",
            description="Long-term investments in subsidiaries, associates, or joint ventures"
        )
    ],
    "DeferredTaxAssets": [
        FinancialTag(
            prefix="sg-as",
            element_name="DeferredTaxAssets",
            element_id="sg-as_DeferredTaxAssets",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="debit",
            period_type="instant",
            substitution_group="xbrli:item",
            description="Income tax recoverable in future periods in respect of deductible temporary differences"
        )
    ],
    "OtherNoncurrentNonfinancialAssets": [
        FinancialTag(
            prefix="sg-as",
            element_name="OtherNoncurrentNonfinancialAssets",
            element_id="sg-as_OtherNoncurrentNonfinancialAssets",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="debit",
            period_type="instant",
            substitution_group="xbrli:item",
            description="Other long-term non-financial assets not specifically classified elsewhere"
        )
    ],
    "NoncurrentAssets": [
        FinancialTag(
            prefix="sg-as",
            element_name="NoncurrentAssets",
            element_id="sg-as_NoncurrentAssets",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="debit",
            period_type="instant",
            substitution_group="xbrli:item",
            description="Total of all non-current assets with economic benefits expected beyond one year"
        )
    ],
    "Assets": [
        FinancialTag(
            prefix="sg-as",
            element_name="Assets",
            element_id="sg-as_Assets",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="debit",
            period_type="instant",
            substitution_group="xbrli:item",
            description="Total of all current and non-current resources controlled by the entity from which future economic benefits are expected"
        )
    ],
    "LiabilitiesAbstract": [
        FinancialTag(
            prefix="sg-as",
            element_name="LiabilitiesAbstract",
            element_id="sg-as_LiabilitiesAbstract",
            abstract=True,
            data_type="xbrli:stringItemType",
            balance_type=None,
            period_type="duration",
            substitution_group="xbrli:item",
            description="Abstract container for all liability categories (current and non-current)"
        )
    ],
    "CurrentLiabilitiesAbstract": [
        FinancialTag(
            prefix="sg-as",
            element_name="CurrentLiabilitiesAbstract",
            element_id="sg-as_CurrentLiabilitiesAbstract",
            abstract=True,
            data_type="xbrli:stringItemType",
            balance_type=None,
            period_type="duration",
            substitution_group="xbrli:item",
            description="Abstract container for all obligations expected to be settled within one operating cycle"
        )
    ],
    "TradeAndOtherPayablesCurrent": [
        FinancialTag(
            prefix="sg-as",
            element_name="TradeAndOtherPayablesCurrent",
            element_id="sg-as_TradeAndOtherPayablesCurrent",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="credit",
            period_type="instant",
            substitution_group="xbrli:item",
            description="Amounts owed to suppliers for goods and services received, and other short-term payables"
        )
    ],
    "CurrentLoansAndBorrowings": [
        FinancialTag(
            prefix="sg-as",
            element_name="CurrentLoansAndBorrowings",
            element_id="sg-as_CurrentLoansAndBorrowings",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="credit",
            period_type="instant",
            substitution_group="xbrli:item",
            description="Short-term debt and current portions of long-term debt due within one year"
        )
    ],
    "CurrentFinancialLiabilitiesMeasuredAtFairValueThroughProfitOrLoss": [
        FinancialTag(
            prefix="sg-as",
            element_name="CurrentFinancialLiabilitiesMeasuredAtFairValueThroughProfitOrLoss",
            element_id="sg-as_CurrentFinancialLiabilitiesMeasuredAtFairValueThroughProfitOrLoss",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="credit",
            period_type="instant",
            substitution_group="xbrli:item",
            description="Current financial liabilities designated or classified as at fair value through profit or loss"
        )
    ],
    "CurrentFinanceLeaseLiabilities": [
        FinancialTag(
            prefix="sg-as",
            element_name="CurrentFinanceLeaseLiabilities",
            element_id="sg-as_CurrentFinanceLeaseLiabilities",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="credit",
            period_type="instant",
            substitution_group="xbrli:item",
            description="Current portion of obligations under finance leases due within one year"
        )
    ],
    "OtherCurrentFinancialLiabilities": [
        FinancialTag(
            prefix="sg-as",
            element_name="OtherCurrentFinancialLiabilities",
            element_id="sg-as_OtherCurrentFinancialLiabilities",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="credit",
            period_type="instant",
            substitution_group="xbrli:item",
            description="Other current financial liabilities not specifically classified elsewhere"
        )
    ],
    "CurrentIncomeTaxLiabilities": [
        FinancialTag(
            prefix="sg-as",
            element_name="CurrentIncomeTaxLiabilities",
            element_id="sg-as_CurrentIncomeTaxLiabilities",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="credit",
            period_type="instant",
            substitution_group="xbrli:item",
            description="Unpaid income taxes for the current and prior periods"
        )
    ],
    "CurrentProvisions": [
        FinancialTag(
            prefix="sg-as",
            element_name="CurrentProvisions",
            element_id="sg-as_CurrentProvisions",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="credit",
            period_type="instant",
            substitution_group="xbrli:item",
            description="Provisions expected to be settled within one year (e.g., warranties, legal claims)"
        )
    ],
    "OtherCurrentNonfinancialLiabilities": [
        FinancialTag(
            prefix="sg-as",
            element_name="OtherCurrentNonfinancialLiabilities",
            element_id="sg-as_OtherCurrentNonfinancialLiabilities",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="credit",
            period_type="instant",
            substitution_group="xbrli:item",
            description="Other current non-financial obligations (e.g., deferred revenue, customer advances)"
        )
    ],
    "LiabilitiesClassifiedAsHeldForSale": [
        FinancialTag(
            prefix="sg-as",
            element_name="LiabilitiesClassifiedAsHeldForSale",
            element_id="sg-as_LiabilitiesClassifiedAsHeldForSale",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="credit",
            period_type="instant",
            substitution_group="xbrli:item",
            description="Liabilities associated with assets classified as held for sale"
        )
    ],
    "CurrentLiabilities": [
        FinancialTag(
            prefix="sg-as",
            element_name="CurrentLiabilities",
            element_id="sg-as_CurrentLiabilities",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="credit",
            period_type="instant",
            substitution_group="xbrli:item",
            description="Total of all liabilities expected to be settled within one operating cycle"
        )
    ],
    "NoncurrentLiabilitiesAbstract": [
        FinancialTag(
            prefix="sg-as",
            element_name="NoncurrentLiabilitiesAbstract",
            element_id="sg-as_NoncurrentLiabilitiesAbstract",
            abstract=True,
            data_type="xbrli:stringItemType",
            balance_type=None,
            period_type="duration",
            substitution_group="xbrli:item",
            description="Abstract container for all obligations expected to be settled beyond one year"
        )
    ],
    "TradeAndOtherPayablesNoncurrent": [
        FinancialTag(
            prefix="sg-as",
            element_name="TradeAndOtherPayablesNoncurrent",
            element_id="sg-as_TradeAndOtherPayablesNoncurrent",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="credit",
            period_type="instant",
            substitution_group="xbrli:item",
            description="Long-term payables not expected to be settled within one year"
        )
    ],
    "NoncurrentLoansAndBorrowings": [
        FinancialTag(
            prefix="sg-as",
            element_name="NoncurrentLoansAndBorrowings",
            element_id="sg-as_NoncurrentLoansAndBorrowings",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="credit",
            period_type="instant",
            substitution_group="xbrli:item",
            description="Long-term debt and borrowings due beyond one year (e.g., bonds, term loans)"
        )
    ],
    "NoncurrentFinancialLiabilitiesMeasuredAtFairValueThroughProfitOrLoss": [
        FinancialTag(
            prefix="sg-as",
            element_name="NoncurrentFinancialLiabilitiesMeasuredAtFairValueThroughProfitOrLoss",
            element_id="sg-as_NoncurrentFinancialLiabilitiesMeasuredAtFairValueThroughProfitOrLoss",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="credit",
            period_type="instant",
            substitution_group="xbrli:item",
            description="Long-term financial liabilities designated or classified as at fair value through profit or loss"
        )
    ],
    "NoncurrentFinanceLeaseLiabilities": [
        FinancialTag(
            prefix="sg-as",
            element_name="NoncurrentFinanceLeaseLiabilities",
            element_id="sg-as_NoncurrentFinanceLeaseLiabilities",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="credit",
            period_type="instant",
            substitution_group="xbrli:item",
            description="Long-term portion of obligations under finance leases due beyond one year"
        )
    ],
    "OtherNoncurrentFinancialLiabilities": [
        FinancialTag(
            prefix="sg-as",
            element_name="OtherNoncurrentFinancialLiabilities",
            element_id="sg-as_OtherNoncurrentFinancialLiabilities",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="credit",
            period_type="instant",
            substitution_group="xbrli:item",
            description="Other long-term financial liabilities not specifically classified elsewhere"
        )
    ],
    "DeferredTaxLiabilities": [
        FinancialTag(
            prefix="sg-as",
            element_name="DeferredTaxLiabilities",
            element_id="sg-as_DeferredTaxLiabilities",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="credit",
            period_type="instant",
            substitution_group="xbrli:item",
            description="Future income tax obligations from taxable temporary differences"
        )
    ],
    "NoncurrentProvisions": [
        FinancialTag(
            prefix="sg-as",
            element_name="NoncurrentProvisions",
            element_id="sg-as_NoncurrentProvisions",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="credit",
            period_type="instant",
            substitution_group="xbrli:item",
            description="Long-term provisions expected to be settled beyond one year (e.g., asset retirement obligations)"
        )
    ],
    "OtherNoncurrentNonfinancialLiabilities": [
        FinancialTag(
            prefix="sg-as",
            element_name="OtherNoncurrentNonfinancialLiabilities",
            element_id="sg-as_OtherNoncurrentNonfinancialLiabilities",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="credit",
            period_type="instant",
            substitution_group="xbrli:item",
            description="Other long-term non-financial obligations (e.g., long-term deferred revenue)"
        )
    ],
    "NoncurrentLiabilities": [
        FinancialTag(
            prefix="sg-as",
            element_name="NoncurrentLiabilities",
            element_id="sg-as_NoncurrentLiabilities",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="credit",
            period_type="instant",
            substitution_group="xbrli:item",
            description="Total of all liabilities expected to be settled beyond one year"
        )
    ],
    "Liabilities": [
        FinancialTag(
            prefix="sg-as",
            element_name="Liabilities",
            element_id="sg-as_Liabilities",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="credit",
            period_type="instant",
            substitution_group="xbrli:item",
            description="Total of all current and non-current obligations that are present obligations arising from past events"
        )
    ],
    "EquityAbstract": [
        FinancialTag(
            prefix="sg-as",
            element_name="EquityAbstract",
            element_id="sg-as_EquityAbstract",
            abstract=True,
            data_type="xbrli:stringItemType",
            balance_type=None,
            period_type="duration",
            substitution_group="xbrli:item",
            description="Abstract container for all equity components representing residual interest in the assets after deducting liabilities"
        )
    ],
    "ShareCapital": [
        FinancialTag(
            prefix="sg-as",
            element_name="ShareCapital",
            element_id="sg-as_ShareCapital",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="credit",
            period_type="instant",
            substitution_group="xbrli:item",
            description="Nominal value of issued share capital, including share premium"
        )
    ],
    "TreasuryShares": [
        FinancialTag(
            prefix="sg-as",
            element_name="TreasuryShares",
            element_id="sg-as_TreasuryShares",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="debit",
            period_type="instant",
            substitution_group="xbrli:item",
            description="Own shares repurchased and held by the entity, shown as a deduction from equity"
        )
    ],
    "AccumulatedProfitsLosses": [
        FinancialTag(
            prefix="sg-as",
            element_name="AccumulatedProfitsLosses",
            element_id="sg-as_AccumulatedProfitsLosses",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="credit",
            period_type="instant",
            substitution_group="xbrli:item",
            description="Cumulative net profits or losses that have not been distributed to shareholders or transferred to reserves"
        )
    ],
    "ReservesOtherThanAccumulatedProfitsLosses": [
        FinancialTag(
            prefix="sg-as",
            element_name="ReservesOtherThanAccumulatedProfitsLosses",
            element_id="sg-as_ReservesOtherThanAccumulatedProfitsLosses",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="credit",
            period_type="instant",
            substitution_group="xbrli:item",
            description="Various reserves such as revaluation, translation, hedging, and other statutory or discretionary reserves"
        )
    ],
    "NoncontrollingInterests": [
        FinancialTag(
            prefix="sg-as",
            element_name="NoncontrollingInterests",
            element_id="sg-as_NoncontrollingInterests",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="credit",
            period_type="instant",
            substitution_group="xbrli:item",
            description="Equity in a subsidiary not attributable to the parent (minority interests)"
        )
    ],
    "Equity": [
        FinancialTag(
            prefix="sg-as",
            element_name="Equity",
            element_id="sg-as_Equity",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="credit",
            period_type="instant",
            substitution_group="xbrli:item",
            description="Total residual interest in the assets after deducting all liabilities (net assets)"
        )
    ]
}

# statement-level tags
SG_XBRL_FINANCIAL_POSITION_STATEMENT_TAGS = [
    FinancialTag(
        prefix="sg-as",
        element_name="StatementOfFinancialPositionLineItems",
        element_id="sg-as_StatementOfFinancialPositionLineItems",
        abstract=True,
        data_type="xbrli:stringItemType",
        balance_type=None,
        period_type="duration",
        substitution_group="xbrli:item",
        description="Parent container element for the entire statement of financial position"
    ),
    FinancialTag(
        prefix="sg-as",
        element_name="AssetsAbstract",
        element_id="sg-as_AssetsAbstract",
        abstract=True,
        data_type="xbrli:stringItemType",
        balance_type=None,
        period_type="duration",
        substitution_group="xbrli:item",
        description="Section container for all asset categories in the statement of financial position"
    ),
    FinancialTag(
        prefix="sg-as",
        element_name="LiabilitiesAbstract",
        element_id="sg-as_LiabilitiesAbstract",
        abstract=True,
        data_type="xbrli:stringItemType",
        balance_type=None,
        period_type="duration",
        substitution_group="xbrli:item",
        description="Section container for all liability categories in the statement of financial position"
    ),
    FinancialTag(
        prefix="sg-as",
        element_name="EquityAbstract",
        element_id="sg-as_EquityAbstract",
        abstract=True,
        data_type="xbrli:stringItemType",
        balance_type=None,
        period_type="duration",
        substitution_group="xbrli:item",
        description="Section container for all equity components in the statement of financial position"
    )
]

MANDATORY_FINANCIAL_POSITION_TAGS = {
    "CurrentAssets": True,
    "NoncurrentAssets": True,
    "Assets": True,
    "CurrentLiabilities": True,
    "NoncurrentLiabilities": True,
    "Liabilities": True,
    "ShareCapital": True,
    "AccumulatedProfitsLosses": True,
    "Equity": True
}

#----------------------------------------------------------------------------------------------------------------------------------------------
# Income statement XBRL taxonomy tags
# -----------------------------------------------------------------------------------------------------------------------------------------------

SG_XBRL_INCOME_STATEMENT_TAGS = {
    "StatementOfProfitOrLossLineItems": [
        FinancialTag(
            prefix="sg-as",
            element_name="StatementOfProfitOrLossLineItems",
            element_id="sg-as_StatementOfProfitOrLossLineItems",
            abstract=True,
            data_type="xbrli:stringItemType",
            balance_type=None,
            period_type="duration",
            substitution_group="xbrli:item",
            description="Abstract container for all statement of profit or loss line items"
        )
    ],
    "ProfitLossAbstract": [
        FinancialTag(
            prefix="sg-as",
            element_name="ProfitLossAbstract",
            element_id="sg-as_ProfitLossAbstract",
            abstract=True,
            data_type="xbrli:stringItemType",
            balance_type=None,
            period_type="duration",
            substitution_group="xbrli:item",
            description="Abstract container for profit or loss section items"
        )
    ],
    "Revenue": [
        FinancialTag(
            prefix="sg-as",
            element_name="Revenue",
            element_id="sg-as_Revenue",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="credit",
            period_type="duration",
            substitution_group="xbrli:item",
            description="Income arising from the ordinary activities of the entity (sales, fees, interest, dividends, etc.)"
        )
    ],
    "OtherIncome": [
        FinancialTag(
            prefix="sg-as",
            element_name="OtherIncome",
            element_id="sg-as_OtherIncome",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="credit",
            period_type="duration",
            substitution_group="xbrli:item",
            description="Income from sources other than primary operations (rental, dividend income, government grants, etc.)"
        )
    ],
    "EmployeeBenefitsExpense": [
        FinancialTag(
            prefix="sg-as",
            element_name="EmployeeBenefitsExpense",
            element_id="sg-as_EmployeeBenefitsExpense",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="debit",
            period_type="duration",
            substitution_group="xbrli:item",
            description="All forms of compensation paid to employees (salaries, wages, CPF contributions, bonuses, etc.)"
        )
    ],
    "DepreciationExpense": [
        FinancialTag(
            prefix="sg-as",
            element_name="DepreciationExpense",
            element_id="sg-as_DepreciationExpense",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="debit",
            period_type="duration",
            substitution_group="xbrli:item",
            description="Systematic allocation of the depreciable amount of tangible assets over their useful lives"
        )
    ],
    "AmortisationExpense": [
        FinancialTag(
            prefix="sg-as",
            element_name="AmortisationExpense",
            element_id="sg-as_AmortisationExpense",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="debit",
            period_type="duration",
            substitution_group="xbrli:item",
            description="Systematic allocation of the depreciable amount of intangible assets over their useful lives"
        )
    ],
    "RepairsAndMaintenanceExpense": [
        FinancialTag(
            prefix="sg-as",
            element_name="RepairsAndMaintenanceExpense",
            element_id="sg-as_RepairsAndMaintenanceExpense",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="debit",
            period_type="duration",
            substitution_group="xbrli:item",
            description="Costs incurred to maintain and repair assets to keep them in good working condition"
        )
    ],
    "SalesAndMarketingExpense": [
        FinancialTag(
            prefix="sg-as",
            element_name="SalesAndMarketingExpense",
            element_id="sg-as_SalesAndMarketingExpense",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="debit",
            period_type="duration",
            substitution_group="xbrli:item",
            description="Expenses related to promoting and selling products or services (advertising, marketing, etc.)"
        )
    ],
    "OtherExpensesByNature": [
        FinancialTag(
            prefix="sg-as",
            element_name="OtherExpensesByNature",
            element_id="sg-as_OtherExpensesByNature",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="debit",
            period_type="duration",
            substitution_group="xbrli:item",
            description="Other operating expenses not specifically classified elsewhere (utilities, rent, professional fees, etc.)"
        )
    ],
    "OtherGainsLosses": [
        FinancialTag(
            prefix="sg-as",
            element_name="OtherGainsLosses",
            element_id="sg-as_OtherGainsLosses",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="credit",
            period_type="duration",
            substitution_group="xbrli:item",
            description="Gains or losses from non-operating activities (foreign exchange, asset disposals, fair value changes)"
        )
    ],
    "FinanceCosts": [
        FinancialTag(
            prefix="sg-as",
            element_name="FinanceCosts",
            element_id="sg-as_FinanceCosts",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="debit",
            period_type="duration",
            substitution_group="xbrli:item",
            description="Interest and other costs incurred in connection with borrowing funds (interest expense, finance charges)"
        )
    ],
    "ShareOfProfitLossOfAssociatesAndJointVenturesAccountedForUsingEquityMethod": [
        FinancialTag(
            prefix="sg-as",
            element_name="ShareOfProfitLossOfAssociatesAndJointVenturesAccountedForUsingEquityMethod",
            element_id="sg-as_ShareOfProfitLossOfAssociatesAndJointVenturesAccountedForUsingEquityMethod",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="credit",
            period_type="duration",
            substitution_group="xbrli:item",
            description="Entity's share of the profit or loss of equity-accounted associates and joint ventures"
        )
    ],
    "ProfitLossBeforeTaxation": [
        FinancialTag(
            prefix="sg-as",
            element_name="ProfitLossBeforeTaxation",
            element_id="sg-as_ProfitLossBeforeTaxation",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="credit",
            period_type="duration",
            substitution_group="xbrli:item",
            description="Profit or loss before deduction of income tax expense (revenues minus expenses before tax)"
        )
    ],
    "TaxExpenseBenefitContinuingOperations": [
        FinancialTag(
            prefix="sg-as",
            element_name="TaxExpenseBenefitContinuingOperations",
            element_id="sg-as_TaxExpenseBenefitContinuingOperations",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="debit",
            period_type="duration",
            substitution_group="xbrli:item",
            description="Income tax expense or benefit for continuing operations (current and deferred tax)"
        )
    ],
    "ProfitLossFromDiscontinuedOperations": [
        FinancialTag(
            prefix="sg-as",
            element_name="ProfitLossFromDiscontinuedOperations",
            element_id="sg-as_ProfitLossFromDiscontinuedOperations",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="credit",
            period_type="duration",
            substitution_group="xbrli:item",
            description="Profit or loss from discontinued operations (business components disposed of or held for sale)"
        )
    ],
    "ProfitLoss": [
        FinancialTag(
            prefix="sg-as",
            element_name="ProfitLoss",
            element_id="sg-as_ProfitLoss",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="credit",
            period_type="duration",
            substitution_group="xbrli:item",
            description="Total profit or loss for the period (net income or net loss for the reporting period)"
        )
    ],
    "ProfitLossAttributableToAbstract": [
        FinancialTag(
            prefix="sg-as",
            element_name="ProfitLossAttributableToAbstract",
            element_id="sg-as_ProfitLossAttributableToAbstract",
            abstract=True,
            data_type="xbrli:stringItemType",
            balance_type=None,
            period_type="duration",
            substitution_group="xbrli:item",
            description="Abstract container for allocation of profit or loss between parent owners and non-controlling interests"
        )
    ],
    "ProfitLossAttributableToOwnersOfCompany": [
        FinancialTag(
            prefix="sg-as",
            element_name="ProfitLossAttributableToOwnersOfCompany",
            element_id="sg-as_ProfitLossAttributableToOwnersOfCompany",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="credit",
            period_type="duration",
            substitution_group="xbrli:item",
            description="Portion of profit or loss attributable to equity holders of the parent company"
        )
    ],
    "ProfitLossAttributableToNoncontrollingInterests": [
        FinancialTag(
            prefix="sg-as",
            element_name="ProfitLossAttributableToNoncontrollingInterests",
            element_id="sg-as_ProfitLossAttributableToNoncontrollingInterests",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="credit",
            period_type="duration",
            substitution_group="xbrli:item",
            description="Portion of profit or loss attributable to non-controlling interests (minority shareholders)"
        )
    ]
}

# statement-level tags
SG_XBRL_INCOME_STATEMENT_STATEMENT_TAGS = [
    FinancialTag(
        prefix="sg-as",
        element_name="StatementOfProfitOrLossLineItems",
        element_id="sg-as_StatementOfProfitOrLossLineItems",
        abstract=True,
        data_type="xbrli:stringItemType",
        balance_type=None,
        period_type="duration",
        substitution_group="xbrli:item",
        description="Parent container element for the entire statement of profit or loss"
    ),
    FinancialTag(
        prefix="sg-as",
        element_name="ProfitLossAbstract",
        element_id="sg-as_ProfitLossAbstract",
        abstract=True,
        data_type="xbrli:stringItemType",
        balance_type=None,
        period_type="duration",
        substitution_group="xbrli:item",
        description="Section container for the main profit or loss components"
    ),
    FinancialTag(
        prefix="sg-as",
        element_name="ProfitLossAttributableToAbstract",
        element_id="sg-as_ProfitLossAttributableToAbstract",
        abstract=True,
        data_type="xbrli:stringItemType",
        balance_type=None,
        period_type="duration",
        substitution_group="xbrli:item",
        description="Section container for profit or loss attribution breakdown"
    )
]

MANDATORY_INCOME_STATEMENT_TAGS = {
    "Revenue": True,
    "ProfitLossBeforeTaxation": True,
    "TaxExpenseBenefitContinuingOperations": True,
    "ProfitLoss": True,
    "ProfitLossAttributableToOwnersOfCompany": True
}

#----------------------------------------------------------------------------------------------------------------------------------------------
# Note - Trade and other receivables XBRL taxonomy tags
# -----------------------------------------------------------------------------------------------------------------------------------------------

SG_XBRL_RECEIVABLES_TAGS = {
    "TradeAndOtherReceivablesAbstract": [
        FinancialTag(
            prefix="sg-as",
            element_name="TradeAndOtherReceivablesAbstract",
            element_id="sg-as_TradeAndOtherReceivablesAbstract",
            abstract=True,
            data_type="xbrli:stringItemType",
            balance_type=None,
            period_type="duration",
            substitution_group="xbrli:item",
            description="Abstract container element for trade and other receivables note disclosures"
        )
    ],
    "DisclosureOfDetailedInformationAboutTradeAndOtherReceivablesTable": [
        FinancialTag(
            prefix="sg-as",
            element_name="DisclosureOfDetailedInformationAboutTradeAndOtherReceivablesTable",
            element_id="sg-as_DisclosureOfDetailedInformationAboutTradeAndOtherReceivablesTable",
            abstract=True,
            data_type="xbrldt:hypercubeItem",
            balance_type=None,
            period_type="duration",
            substitution_group="xbrldt:hypercubeItem",
            description="Table structure for organizing trade and other receivables disclosures with dimensions"
        )
    ],
    "ConsolidatedAndSeparateFinancialStatementsAxis": [
        FinancialTag(
            prefix="sg-as",
            element_name="ConsolidatedAndSeparateFinancialStatementsAxis",
            element_id="sg-as_ConsolidatedAndSeparateFinancialStatementsAxis",
            abstract=True,
            data_type="xbrldt:dimensionItem",
            balance_type=None,
            period_type="duration",
            substitution_group="xbrldt:dimensionItem",
            description="Dimension to distinguish between consolidated and separate financial statement data"
        )
    ],
    "DisclosureOfDetailedInformationAboutTradeAndOtherReceivablesLineItems": [
        FinancialTag(
            prefix="sg-as",
            element_name="DisclosureOfDetailedInformationAboutTradeAndOtherReceivablesLineItems",
            element_id="sg-as_DisclosureOfDetailedInformationAboutTradeAndOtherReceivablesLineItems",
            abstract=True,
            data_type="xbrli:stringItemType",
            balance_type=None,
            period_type="duration",
            substitution_group="xbrli:item",
            description="Container for the line items in the trade and other receivables note"
        )
    ],
    "TradeAndOtherReceivablesDueFromThirdParties": [
        FinancialTag(
            prefix="sg-as",
            element_name="TradeAndOtherReceivablesDueFromThirdParties",
            element_id="sg-as_TradeAndOtherReceivablesDueFromThirdParties",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="debit",
            period_type="instant",
            substitution_group="xbrli:item",
            description="Amounts due from third parties for goods sold or services provided (trade debtors)"
        )
    ],
    "TradeAndOtherReceivablesDueFromRelatedParties": [
        FinancialTag(
            prefix="sg-as",
            element_name="TradeAndOtherReceivablesDueFromRelatedParties",
            element_id="sg-as_TradeAndOtherReceivablesDueFromRelatedParties",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="debit",
            period_type="instant",
            substitution_group="xbrli:item",
            description="Amounts due from related parties such as subsidiaries, associates, or other affiliated entities"
        )
    ],
    "UnbilledReceivables": [
        FinancialTag(
            prefix="sg-as",
            element_name="UnbilledReceivables",
            element_id="sg-as_UnbilledReceivables",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="debit",
            period_type="instant",
            substitution_group="xbrli:item",
            description="Amounts earned but not yet billed to customers (contract assets, accrued revenue)"
        )
    ],
    "OtherReceivables": [
        FinancialTag(
            prefix="sg-as",
            element_name="OtherReceivables",
            element_id="sg-as_OtherReceivables",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="debit",
            period_type="instant",
            substitution_group="xbrli:item",
            description="Other receivables not specifically classified elsewhere (deposits, loans, advances, etc.)"
        )
    ],
    "TradeAndOtherReceivables": [
        FinancialTag(
            prefix="sg-as",
            element_name="TradeAndOtherReceivables",
            element_id="sg-as_TradeAndOtherReceivables",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="debit",
            period_type="instant",
            substitution_group="xbrli:item",
            description="Total trade and other receivables, representing all receivable amounts combined"
        )
    ]
}

# statement-level tags
SG_XBRL_RECEIVABLES_STATEMENT_TAGS = [
    FinancialTag(
        prefix="sg-as",
        element_name="TradeAndOtherReceivablesAbstract",
        element_id="sg-as_TradeAndOtherReceivablesAbstract",
        abstract=True,
        data_type="xbrli:stringItemType",
        balance_type=None,
        period_type="duration",
        substitution_group="xbrli:item",
        description="Parent container for the entire trade and other receivables note"
    ),
    FinancialTag(
        prefix="sg-as",
        element_name="DisclosureOfDetailedInformationAboutTradeAndOtherReceivablesLineItems",
        element_id="sg-as_DisclosureOfDetailedInformationAboutTradeAndOtherReceivablesLineItems",
        abstract=True,
        data_type="xbrli:stringItemType",
        balance_type=None,
        period_type="duration",
        substitution_group="xbrli:item",
        description="Section container for the trade and other receivables breakdown line items"
    )
]

MANDATORY_RECEIVABLES_TAGS = {
    "TradeAndOtherReceivables": True  # Only the total is typically mandatory
}

#----------------------------------------------------------------------------------------------------------------------------------------------
# Note - Trade and other payables XBRL taxonomy tags
# -----------------------------------------------------------------------------------------------------------------------------------------------

SG_XBRL_PAYABLES_TAGS = {
    "TradeAndOtherPayablesAbstract": [
        FinancialTag(
            prefix="sg-as",
            element_name="TradeAndOtherPayablesAbstract",
            element_id="sg-as_TradeAndOtherPayablesAbstract",
            abstract=True,
            data_type="xbrli:stringItemType",
            balance_type=None,
            period_type="duration",
            substitution_group="xbrli:item",
            description="Abstract container element for trade and other payables note disclosures"
        )
    ],
    "DisclosureOfDetailedInformationAboutTradeAndOtherPayablesTable": [
        FinancialTag(
            prefix="sg-as",
            element_name="DisclosureOfDetailedInformationAboutTradeAndOtherPayablesTable",
            element_id="sg-as_DisclosureOfDetailedInformationAboutTradeAndOtherPayablesTable",
            abstract=True,
            data_type="xbrldt:hypercubeItem",
            balance_type=None,
            period_type="duration",
            substitution_group="xbrldt:hypercubeItem",
            description="Table structure for organizing trade and other payables disclosures with dimensions"
        )
    ],
    "ConsolidatedAndSeparateFinancialStatementsAxis": [
        FinancialTag(
            prefix="sg-as",
            element_name="ConsolidatedAndSeparateFinancialStatementsAxis",
            element_id="sg-as_ConsolidatedAndSeparateFinancialStatementsAxis",
            abstract=True,
            data_type="xbrldt:dimensionItem",
            balance_type=None,
            period_type="duration",
            substitution_group="xbrldt:dimensionItem",
            description="Dimension to distinguish between consolidated and separate financial statement data"
        )
    ],
    "DisclosureOfDetailedInformationAboutTradeAndOtherPayablesLineItems": [
        FinancialTag(
            prefix="sg-as",
            element_name="DisclosureOfDetailedInformationAboutTradeAndOtherPayablesLineItems",
            element_id="sg-as_DisclosureOfDetailedInformationAboutTradeAndOtherPayablesLineItems",
            abstract=True,
            data_type="xbrli:stringItemType",
            balance_type=None,
            period_type="duration",
            substitution_group="xbrli:item",
            description="Container for the line items in the trade and other payables note"
        )
    ],
    "TradeAndOtherPayablesDueToThirdParties": [
        FinancialTag(
            prefix="sg-as",
            element_name="TradeAndOtherPayablesDueToThirdParties",
            element_id="sg-as_TradeAndOtherPayablesDueToThirdParties",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="credit",
            period_type="instant",
            substitution_group="xbrli:item",
            description="Amounts owed to third-party suppliers for goods or services received (trade creditors)"
        )
    ],
    "TradeAndOtherPayablesDueToRelatedParties": [
        FinancialTag(
            prefix="sg-as",
            element_name="TradeAndOtherPayablesDueToRelatedParties",
            element_id="sg-as_TradeAndOtherPayablesDueToRelatedParties",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="credit",
            period_type="instant",
            substitution_group="xbrli:item",
            description="Amounts owed to related parties such as subsidiaries, associates, or other affiliated entities"
        )
    ],
    "DeferredIncome": [
        FinancialTag(
            prefix="sg-as",
            element_name="DeferredIncome",
            element_id="sg-as_DeferredIncome",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="credit",
            period_type="instant",
            substitution_group="xbrli:item",
            description="Revenue received but not yet earned (unearned revenue, contract liabilities, advances from customers)"
        )
    ],
    "OtherPayables": [
        FinancialTag(
            prefix="sg-as",
            element_name="OtherPayables",
            element_id="sg-as_OtherPayables",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="credit",
            period_type="instant",
            substitution_group="xbrli:item",
            description="Other payables not specifically classified elsewhere (accruals, deferred expenses, etc.)"
        )
    ],
    "TradeAndOtherPayables": [
        FinancialTag(
            prefix="sg-as",
            element_name="TradeAndOtherPayables",
            element_id="sg-as_TradeAndOtherPayables",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="credit",
            period_type="instant",
            substitution_group="xbrli:item",
            description="Total trade and other payables, representing all payable amounts combined"
        )
    ]
}

# statement-level tags
SG_XBRL_PAYABLES_STATEMENT_TAGS = [
    FinancialTag(
        prefix="sg-as",
        element_name="TradeAndOtherPayablesAbstract",
        element_id="sg-as_TradeAndOtherPayablesAbstract",
        abstract=True,
        data_type="xbrli:stringItemType",
        balance_type=None,
        period_type="duration",
        substitution_group="xbrli:item",
        description="Parent container for the entire trade and other payables note"
    ),
    FinancialTag(
        prefix="sg-as",
        element_name="DisclosureOfDetailedInformationAboutTradeAndOtherPayablesLineItems",
        element_id="sg-as_DisclosureOfDetailedInformationAboutTradeAndOtherPayablesLineItems",
        abstract=True,
        data_type="xbrli:stringItemType",
        balance_type=None,
        period_type="duration",
        substitution_group="xbrli:item",
        description="Section container for the trade and other payables breakdown line items"
    )
]

MANDATORY_PAYABLES_TAGS = {
    "TradeAndOtherPayables": True  # Only the total is typically mandatory
}

#----------------------------------------------------------------------------------------------------------------------------------------------
# Note - Revenue XBRL taxonomy tags
# -----------------------------------------------------------------------------------------------------------------------------------------------

SG_XBRL_REVENUE_TAGS = {
    "DisclosureOfRevenueAbstract": [
        FinancialTag(
            prefix="sg-as",
            element_name="DisclosureOfRevenueAbstract",
            element_id="sg-as_DisclosureOfRevenueAbstract",
            abstract=True,
            data_type="xbrli:stringItemType",
            balance_type=None,
            period_type="duration",
            substitution_group="xbrli:item",
            description="Abstract container element for revenue note disclosures"
        )
    ],
    "DisclosureOfRevenueTable": [
        FinancialTag(
            prefix="sg-as",
            element_name="DisclosureOfRevenueTable",
            element_id="sg-as_DisclosureOfRevenueTable",
            abstract=True,
            data_type="xbrldt:hypercubeItem",
            balance_type=None,
            period_type="duration",
            substitution_group="xbrldt:hypercubeItem",
            description="Table structure for organizing revenue disclosures with dimensions"
        )
    ],
    "ConsolidatedAndSeparateFinancialStatementsAxis": [
        FinancialTag(
            prefix="sg-as",
            element_name="ConsolidatedAndSeparateFinancialStatementsAxis",
            element_id="sg-as_ConsolidatedAndSeparateFinancialStatementsAxis",
            abstract=True,
            data_type="xbrldt:dimensionItem",
            balance_type=None,
            period_type="duration",
            substitution_group="xbrldt:dimensionItem",
            description="Dimension to distinguish between consolidated and separate financial statement data"
        )
    ],
    "DisclosureOfRevenueLineItems": [
        FinancialTag(
            prefix="sg-as",
            element_name="DisclosureOfRevenueLineItems",
            element_id="sg-as_DisclosureOfRevenueLineItems",
            abstract=True,
            data_type="xbrli:stringItemType",
            balance_type=None,
            period_type="duration",
            substitution_group="xbrli:item",
            description="Container for the line items in the revenue note"
        )
    ],
    "RevenueAbstract": [
        FinancialTag(
            prefix="sg-as",
            element_name="RevenueAbstract",
            element_id="sg-as_RevenueAbstract",
            abstract=True,
            data_type="xbrli:stringItemType",
            balance_type=None,
            period_type="duration",
            substitution_group="xbrli:item",
            description="Abstract container for grouping revenue breakdown items"
        )
    ],
    "RevenueFromPropertyTransferredAtPointInTime": [
        FinancialTag(
            prefix="sg-as",
            element_name="RevenueFromPropertyTransferredAtPointInTime",
            element_id="sg-as_RevenueFromPropertyTransferredAtPointInTime",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="credit",
            period_type="duration",
            substitution_group="xbrli:item",
            description="Revenue recognized from property sales when control transfers at a specific point in time"
        )
    ],
    "RevenueFromGoodsTransferredAtPointInTime": [
        FinancialTag(
            prefix="sg-as",
            element_name="RevenueFromGoodsTransferredAtPointInTime",
            element_id="sg-as_RevenueFromGoodsTransferredAtPointInTime",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="credit",
            period_type="duration",
            substitution_group="xbrli:item",
            description="Revenue recognized from sale of goods when control transfers at a specific point in time"
        )
    ],
    "RevenueFromServicesTransferredAtPointInTime": [
        FinancialTag(
            prefix="sg-as",
            element_name="RevenueFromServicesTransferredAtPointInTime",
            element_id="sg-as_RevenueFromServicesTransferredAtPointInTime",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="credit",
            period_type="duration",
            substitution_group="xbrli:item",
            description="Revenue recognized from services delivered at a specific point in time rather than over time"
        )
    ],
    "RevenueFromPropertyTransferredOverTime": [
        FinancialTag(
            prefix="sg-as",
            element_name="RevenueFromPropertyTransferredOverTime",
            element_id="sg-as_RevenueFromPropertyTransferredOverTime",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="credit",
            period_type="duration",
            substitution_group="xbrli:item",
            description="Revenue recognized from property development where control transfers gradually over time"
        )
    ],
    "RevenueFromConstructionContractsOverTime": [
        FinancialTag(
            prefix="sg-as",
            element_name="RevenueFromConstructionContractsOverTime",
            element_id="sg-as_RevenueFromConstructionContractsOverTime",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="credit",
            period_type="duration",
            substitution_group="xbrli:item",
            description="Revenue recognized from construction contracts over time using progress measurements"
        )
    ],
    "RevenueFromServicesTransferredOverTime": [
        FinancialTag(
            prefix="sg-as",
            element_name="RevenueFromServicesTransferredOverTime",
            element_id="sg-as_RevenueFromServicesTransferredOverTime",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="credit",
            period_type="duration",
            substitution_group="xbrli:item",
            description="Revenue recognized from services that are delivered over time (e.g., subscription services)"
        )
    ],
    "OtherRevenue": [
        FinancialTag(
            prefix="sg-as",
            element_name="OtherRevenue",
            element_id="sg-as_OtherRevenue",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="credit",
            period_type="duration",
            substitution_group="xbrli:item",
            description="Revenue from other sources not specifically classified elsewhere"
        )
    ],
    "Revenue": [
        FinancialTag(
            prefix="sg-as",
            element_name="Revenue",
            element_id="sg-as_Revenue",
            abstract=False,
            data_type="xbrli:monetaryItemType",
            balance_type="credit",
            period_type="duration",
            substitution_group="xbrli:item",
            description="Total revenue from all sources combined"
        )
    ]
}

# statement-level tags
SG_XBRL_REVENUE_STATEMENT_TAGS = [
    FinancialTag(
        prefix="sg-as",
        element_name="DisclosureOfRevenueAbstract",
        element_id="sg-as_DisclosureOfRevenueAbstract",
        abstract=True,
        data_type="xbrli:stringItemType",
        balance_type=None,
        period_type="duration",
        substitution_group="xbrli:item",
        description="Parent container for the entire revenue note"
    ),
    FinancialTag(
        prefix="sg-as",
        element_name="RevenueAbstract",
        element_id="sg-as_RevenueAbstract",
        abstract=True,
        data_type="xbrli:stringItemType",
        balance_type=None,
        period_type="duration",
        substitution_group="xbrli:item",
        description="Section container for the revenue breakdown items"
    )
]

MANDATORY_REVENUE_TAGS = {
    "Revenue": True  # Only the total is typically mandatory
}

# Combine all tag dictionaries
SG_XBRL_TAXONOMY = {
    **SG_XBRL_FILING_TAGS,
    **SG_XBRL_DIRECTORS_TAGS,
    **SG_XBRL_AUDIT_TAGS,
    **SG_XBRL_FINANCIAL_POSITION_TAGS,  # This already includes liabilities and equity
    **SG_XBRL_INCOME_STATEMENT_TAGS,
    **SG_XBRL_RECEIVABLES_TAGS,
    **SG_XBRL_PAYABLES_TAGS,
    **SG_XBRL_REVENUE_TAGS
}

# Combine all statement-level tags
SG_XBRL_STATEMENT_TAGS = (
    SG_XBRL_FILING_STATEMENT_TAGS + 
    SG_XBRL_DIRECTORS_STATEMENT_TAGS + 
    SG_XBRL_AUDIT_STATEMENT_TAGS + 
    SG_XBRL_FINANCIAL_POSITION_STATEMENT_TAGS +
    SG_XBRL_INCOME_STATEMENT_STATEMENT_TAGS + 
    SG_XBRL_RECEIVABLES_STATEMENT_TAGS + 
    SG_XBRL_PAYABLES_STATEMENT_TAGS + 
    SG_XBRL_REVENUE_STATEMENT_TAGS
)

# Combine all mandatory field dictionaries
MANDATORY_TAGS = {
    **MANDATORY_FILING_TAGS,
    **MANDATORY_DIRECTORS_TAGS,
    **MANDATORY_AUDIT_TAGS,
    **MANDATORY_FINANCIAL_POSITION_TAGS,  # This already includes liabilities and equity
    **MANDATORY_INCOME_STATEMENT_TAGS,
    **MANDATORY_RECEIVABLES_TAGS,
    **MANDATORY_PAYABLES_TAGS,
    **MANDATORY_REVENUE_TAGS
}

# Create the dependency instance with the comprehensive tag collections
sg_xbrl_deps = XBRLTaxonomyDependencies(
    taxonomy_name="sg-as-2022-02",
    entity_name="Default Company",
    mandatory_fields=MANDATORY_TAGS,
    field_tags=SG_XBRL_TAXONOMY,
    statement_tags=SG_XBRL_STATEMENT_TAGS,
    reporting_year="2022"
)