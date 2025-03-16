"""
Dependencies for the financial statement mapping agent.
"""
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class FinancialTermDeps:
    """Dependencies for financial term mapping"""
    income_statement_terms: Dict[str, List[str]]
    financial_position_terms: Dict[str, List[str]]
    
    def __post_init__(self):
        """Ensure all terms are lowercase for case-insensitive matching"""
        self.income_statement_terms = {
            k: [t.lower() for t in terms] for k, terms in self.income_statement_terms.items()
        }
        self.financial_position_terms = {
            k: [t.lower() for t in terms] for k, terms in self.financial_position_terms.items()
        }

# Create term mappings
position_terms = {
    "currentAssets.CashAndBankBalances": ["cash", "bank", "cash equivalents", "cash at bank", "cash on hand"],
    "currentAssets.TradeAndOtherReceivablesCurrent": ["trade receivables", "accounts receivable", "trade debtors", "contract assets", "current receivables"],
    "currentAssets.CurrentFinanceLeaseReceivables": ["lease receivables", "finance lease assets", "short-term lease receivables"],
    "currentAssets.CurrentDerivativeFinancialAssets": ["derivatives", "forward contracts", "swap assets", "option assets", "current derivative assets"],
    "currentAssets.CurrentFinancialAssetsMeasuredAtFairValueThroughProfitOrLoss": ["fvtpl", "fair value", "trading assets", "fair value instruments", "current financial assets at fair value"],
    "currentAssets.Inventories": ["inventory", "stock", "goods for sale", "raw materials", "finished goods", "work in progress"],
    "currentAssets.OtherCurrentNonfinancialAssets": ["prepayments", "advances", "deposits", "other current assets"],
    "currentAssets.CurrentAssets": ["total current assets", "current assets", "short-term assets"],
    
    "nonCurrentAssets.PropertyPlantAndEquipment": ["ppe", "fixed assets", "tangible assets", "property and equipment", "plant and equipment"],
    "nonCurrentAssets.InvestmentProperties": ["investment property", "investment real estate", "rental properties", "property investments"],
    "nonCurrentAssets.Goodwill": ["goodwill", "acquisition goodwill", "purchased goodwill"],
    "nonCurrentAssets.IntangibleAssetsOtherThanGoodwill": ["intangible assets", "patents", "trademarks", "software", "licenses", "intellectual property"],
    "nonCurrentAssets.InvestmentsInSubsidiariesAssociatesOrJointVentures": ["investments in subsidiaries", "investments in associates", "equity investments", "joint ventures"],
    "nonCurrentAssets.DeferredTaxAssets": ["deferred tax assets", "future tax assets", "tax credits"],
    "nonCurrentAssets.NoncurrentAssets": ["total non-current assets", "long-term assets", "fixed assets"],
    
    "currentLiabilities.TradeAndOtherPayablesCurrent": ["trade payables", "accounts payable", "trade creditors", "accruals", "current payables"],
    "currentLiabilities.CurrentLoansAndBorrowings": ["short-term borrowings", "bank overdrafts", "current portion of loans", "current loans"],
    "currentLiabilities.CurrentFinanceLeaseLiabilities": ["current lease obligations", "short-term lease liabilities", "lease liabilities current"],
    "currentLiabilities.CurrentIncomeTaxLiabilities": ["tax payable", "current tax", "income tax payable"],
    "currentLiabilities.CurrentProvisions": ["short-term provisions", "current provisions", "warranty provisions"],
    "currentLiabilities.CurrentLiabilities": ["total current liabilities", "short-term liabilities"],
    
    "nonCurrentLiabilities.NoncurrentLoansAndBorrowings": ["long-term borrowings", "term loans", "bonds payable", "non-current loans"],
    "nonCurrentLiabilities.NoncurrentFinanceLeaseLiabilities": ["long-term lease obligations", "long-term lease liabilities", "non-current lease liabilities"],
    "nonCurrentLiabilities.DeferredTaxLiabilities": ["deferred tax liabilities", "future tax liabilities", "deferred taxation"],
    "nonCurrentLiabilities.NoncurrentProvisions": ["long-term provisions", "decommissioning provisions", "restoration provisions"],
    "nonCurrentLiabilities.NoncurrentLiabilities": ["total non-current liabilities", "long-term liabilities"],
    
    "equity.ShareCapital": ["share capital", "issued capital", "paid-up capital", "ordinary shares", "common stock"],
    "equity.TreasuryShares": ["treasury shares", "own shares", "repurchased shares", "treasury stock"],
    "equity.AccumulatedProfitsLosses": ["retained earnings", "accumulated profits", "retained profits", "accumulated earnings"],
    "equity.ReservesOtherThanAccumulatedProfitsLosses": ["reserves", "revaluation reserve", "translation reserve", "hedging reserve", "capital reserve"],
    "equity.NoncontrollingInterests": ["minority interests", "nci", "minority shareholders' interest", "non-controlling interests"],
    "equity.Equity": ["total equity", "shareholders' equity", "shareholders' funds", "net assets"],
    
    "Assets": ["total assets", "assets"],
    "Liabilities": ["total liabilities", "liabilities"]
}

income_terms = {
    "Revenue": ["revenue", "turnover", "sales", "contract", "income from operations"],
    "OtherIncome": ["other income", "other operating income", "other revenue", "dividend income", "interest income", "rental income"],
    "EmployeeBenefitsExpense": ["employee", "staff", "personnel", "salaries", "wages", "cpf", "compensation", "bonuses"],
    "DepreciationExpense": ["depreciation", "property, plant and equipment", "ppe", "fixed assets", "depreciate"],
    "AmortisationExpense": ["amortisation", "amortization", "intangible assets", "goodwill", "amortize"],
    "RepairsAndMaintenanceExpense": ["repairs", "maintenance", "upkeep", "repair expenses", "maintenance costs"],
    "SalesAndMarketingExpense": ["sales", "marketing", "advertising", "promotion", "selling expenses", "distribution costs"],
    "OtherExpensesByNature": ["other expenses", "general expenses", "administrative", "utilities", "office expenses", "rental expenses"],
    "OtherGainsLosses": ["other gains", "other losses", "foreign exchange", "forex", "fair value", "disposal gains", "disposal losses"],
    "FinanceCosts": ["finance costs", "interest expense", "borrowing costs", "loan interest", "financing costs"],
    "ShareOfProfitLossOfAssociatesAndJointVenturesAccountedForUsingEquityMethod": ["associates", "joint ventures", "equity method", "share of profit", "share of loss"],
    "ProfitLossBeforeTaxation": ["profit before tax", "earnings before tax", "profit before income tax", "pbt", "ebt"],
    "TaxExpenseBenefitContinuingOperations": ["income tax", "tax expense", "taxation", "tax charge", "income tax expense"],
    "ProfitLossFromDiscontinuedOperations": ["discontinued operations", "disposal group", "discontinued business"],
    "ProfitLoss": ["profit for the year", "net profit", "profit for the period", "net income", "total comprehensive income"],
    "ProfitLossAttributableToOwnersOfCompany": ["attributable to owners", "attributable to shareholders", "equity holders", "owners of the company"],
    "ProfitLossAttributableToNoncontrollingInterests": ["non-controlling interests", "minority interest", "minority shareholders", "nci"]
}

# Create an instance of the dependencies
financial_deps = FinancialTermDeps(income_terms, position_terms)
