#!/usr/bin/env python3
"""
Financial Analyzer for SEC Filings

Calculates financial ratios, identifies trends, and provides benchmarking.
Comprehensive analysis engine for investment research and thesis generation.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple, Union
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FinancialAnalyzer:
    """Main class for financial analysis and ratio calculations."""

    def __init__(self):
        self.analysis_results = {}
        self.trend_analysis = {}
        self.benchmarking = {}

    def analyze_financial_statements(self, financial_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Complete financial statement analysis.

        Args:
            financial_data: Normalized financial data from file_processor

        Returns:
            Comprehensive analysis results
        """
        analysis = {}

        # Calculate financial ratios
        ratios = self._calculate_financial_ratios(financial_data)
        analysis['ratios'] = ratios

        # Perform trend analysis
        trends = self._identify_trends(financial_data)
        analysis['trends'] = trends

        # Calculate growth rates
        growth_rates = self._calculate_growth_rates(financial_data)
        analysis['growth_rates'] = growth_rates

        # Assess financial health
        health_score = self._assess_financial_health(ratios)
        analysis['financial_health'] = health_score

        self.analysis_results = analysis
        return analysis

    def calculate_liquidity_ratios(self, balance_sheet: Dict[str, Any]) -> Dict[str, float]:
        """
        Calculate liquidity ratios from balance sheet data.

        Args:
            balance_sheet: Balance sheet data with periods as keys

        Returns:
            Dictionary of liquidity ratios
        """
        ratios = {}

        for period, data in balance_sheet.items():
            try:
                current_assets = data.get('total_current_assets', 0)
                current_liabilities = data.get('total_current_liabilities', 0)
                cash = data.get('cash_and_cash_equivalents', 0)
                marketable_securities = data.get('marketable_securities', 0)
                inventory = data.get('inventory', 0)

                # Current Ratio
                if current_liabilities != 0:
                    ratios[f'current_ratio_{period}'] = current_assets / current_liabilities
                else:
                    ratios[f'current_ratio_{period}'] = None

                # Quick Ratio (Acid-test)
                quick_assets = current_assets - inventory
                if current_liabilities != 0:
                    ratios[f'quick_ratio_{period}'] = quick_assets / current_liabilities
                else:
                    ratios[f'quick_ratio_{period}'] = None

                # Cash Ratio
                cash_and_equivalents = cash + marketable_securities
                if current_liabilities != 0:
                    ratios[f'cash_ratio_{period}'] = cash_and_equivalents / current_liabilities
                else:
                    ratios[f'cash_ratio_{period}'] = None

            except Exception as e:
                logger.warning(f"Error calculating liquidity ratios for {period}: {e}")
                continue

        return ratios

    def calculate_profitability_ratios(self, income_statement: Dict[str, Any],
                                     balance_sheet: Optional[Dict[str, Any]] = None) -> Dict[str, float]:
        """
        Calculate profitability ratios from income statement and balance sheet data.

        Args:
            income_statement: Income statement data
            balance_sheet: Optional balance sheet data for ROE calculation

        Returns:
            Dictionary of profitability ratios
        """
        ratios = {}

        for period, data in income_statement.items():
            try:
                revenue = data.get('revenue', 0)
                cost_of_goods_sold = data.get('cost_of_goods_sold', 0)
                gross_profit = data.get('gross_profit', revenue - cost_of_goods_sold)
                operating_income = data.get('operating_income', 0)
                net_income = data.get('net_income', 0)

                # Gross Margin
                if revenue != 0:
                    ratios[f'gross_margin_{period}'] = gross_profit / revenue
                else:
                    ratios[f'gross_margin_{period}'] = None

                # Operating Margin
                if revenue != 0:
                    ratios[f'operating_margin_{period}'] = operating_income / revenue
                else:
                    ratios[f'operating_margin_{period}'] = None

                # Net Margin
                if revenue != 0:
                    ratios[f'net_margin_{period}'] = net_income / revenue
                else:
                    ratios[f'net_margin_{period}'] = None

                # Return on Assets (ROA) - needs balance sheet
                if balance_sheet and period in balance_sheet:
                    total_assets = balance_sheet[period].get('total_assets', 0)
                    if total_assets != 0:
                        ratios[f'roa_{period}'] = net_income / total_assets
                    else:
                        ratios[f'roa_{period}'] = None

                # Return on Equity (ROE) - needs balance sheet
                if balance_sheet and period in balance_sheet:
                    total_equity = balance_sheet[period].get('total_equity', 0)
                    if total_equity != 0:
                        ratios[f'roe_{period}'] = net_income / total_equity
                    else:
                        ratios[f'roe_{period}'] = None

            except Exception as e:
                logger.warning(f"Error calculating profitability ratios for {period}: {e}")
                continue

        return ratios

    def calculate_efficiency_ratios(self, financial_data: Dict[str, Any]) -> Dict[str, float]:
        """
        Calculate efficiency ratios from financial data.

        Args:
            financial_data: Complete financial data

        Returns:
            Dictionary of efficiency ratios
        """
        ratios = {}
        income_statement = financial_data.get('income_statement', {})
        balance_sheet = financial_data.get('balance_sheet', {})

        for period in income_statement.keys():
            try:
                revenue = income_statement[period].get('revenue', 0)
                cost_of_goods_sold = income_statement[period].get('cost_of_goods_sold', 0)

                # Asset Turnover
                if period in balance_sheet:
                    total_assets = balance_sheet[period].get('total_assets', 0)
                    if total_assets != 0:
                        ratios[f'asset_turnover_{period}'] = revenue / total_assets
                    else:
                        ratios[f'asset_turnover_{period}'] = None

                # Inventory Turnover
                if period in balance_sheet:
                    inventory = balance_sheet[period].get('inventory', 0)
                    if inventory != 0:
                        ratios[f'inventory_turnover_{period}'] = cost_of_goods_sold / inventory
                    else:
                        ratios[f'inventory_turnover_{period}'] = None

                # Receivables Turnover
                if period in balance_sheet:
                    accounts_receivable = balance_sheet[period].get('accounts_receivable', 0)
                    if accounts_receivable != 0:
                        ratios[f'receivables_turnover_{period}'] = revenue / accounts_receivable
                    else:
                        ratios[f'receivables_turnover_{period}'] = None

            except Exception as e:
                logger.warning(f"Error calculating efficiency ratios for {period}: {e}")
                continue

        return ratios

    def calculate_leverage_ratios(self, financial_data: Dict[str, Any]) -> Dict[str, float]:
        """
        Calculate leverage ratios from financial data.

        Args:
            financial_data: Complete financial data

        Returns:
            Dictionary of leverage ratios
        """
        ratios = {}
        income_statement = financial_data.get('income_statement', {})
        balance_sheet = financial_data.get('balance_sheet', {})

        for period in income_statement.keys():
            try:
                # Debt-to-Equity Ratio
                if period in balance_sheet:
                    total_debt = balance_sheet[period].get('total_liabilities', 0)
                    total_equity = balance_sheet[period].get('total_equity', 0)
                    if total_equity != 0:
                        ratios[f'debt_to_equity_{period}'] = total_debt / total_equity
                    else:
                        ratios[f'debt_to_equity_{period}'] = None

                # Debt-to-Assets Ratio
                if period in balance_sheet:
                    total_debt = balance_sheet[period].get('total_liabilities', 0)
                    total_assets = balance_sheet[period].get('total_assets', 0)
                    if total_assets != 0:
                        ratios[f'debt_to_assets_{period}'] = total_debt / total_assets
                    else:
                        ratios[f'debt_to_assets_{period}'] = None

                # Interest Coverage Ratio
                operating_income = income_statement[period].get('operating_income', 0)
                interest_expense = income_statement[period].get('interest_expense', 0)
                if interest_expense != 0:
                    ratios[f'interest_coverage_{period}'] = operating_income / interest_expense
                else:
                    ratios[f'interest_coverage_{period}'] = None

            except Exception as e:
                logger.warning(f"Error calculating leverage ratios for {period}: {e}")
                continue

        return ratios

    def _calculate_financial_ratios(self, financial_data: Dict[str, Any]) -> Dict[str, Dict[str, float]]:
        """Internal method to calculate all financial ratios."""
        ratios = {}

        balance_sheet = financial_data.get('balance_sheet', {})
        income_statement = financial_data.get('income_statement', {})

        # Calculate all ratio categories
        ratios['liquidity'] = self.calculate_liquidity_ratios(balance_sheet)
        ratios['profitability'] = self.calculate_profitability_ratios(income_statement, balance_sheet)
        ratios['efficiency'] = self.calculate_efficiency_ratios(financial_data)
        ratios['leverage'] = self.calculate_leverage_ratios(financial_data)

        return ratios

    def _identify_trends(self, financial_data: Dict[str, Any]) -> Dict[str, Any]:
        """Identify financial trends over time."""
        trends = {}

        # Extract time series data
        time_series = self._extract_time_series(financial_data)

        for metric, values in time_series.items():
            if len(values) >= 2:
                # Calculate trend direction and strength
                trend_analysis = self._analyze_trend(values)
                trends[metric] = trend_analysis

        return trends

    def _extract_time_series(self, financial_data: Dict[str, Any]) -> Dict[str, List[float]]:
        """Extract time series data for key metrics."""
        time_series = {}

        # Extract from income statement
        income_statement = financial_data.get('income_statement', {})
        for period, data in income_statement.items():
            for key, value in data.items():
                if key not in time_series:
                    time_series[key] = []
                time_series[key].append(float(value) if value is not None else 0.0)

        # Extract from balance sheet
        balance_sheet = financial_data.get('balance_sheet', {})
        for period, data in balance_sheet.items():
            for key, value in data.items():
                metric_key = f"balance_{key}"
                if metric_key not in time_series:
                    time_series[metric_key] = []
                time_series[metric_key].append(float(value) if value is not None else 0.0)

        return time_series

    def _analyze_trend(self, values: List[float]) -> Dict[str, Any]:
        """Analyze trend direction and strength."""
        if len(values) < 2:
            return {'direction': 'insufficient_data', 'strength': 0.0}

        # Calculate percentage change
        if values[0] == 0:
            pct_change = 0.0
        else:
            pct_change = ((values[-1] - values[0]) / abs(values[0])) * 100

        # Calculate linear trend
        x = list(range(len(values)))
        y = values

        try:
            slope = np.polyfit(x, y, 1)[0]
            correlation = np.corrcoef(x, y)[0, 1]
        except:
            slope = 0.0
            correlation = 0.0

        # Determine trend direction
        if pct_change > 5:
            direction = 'strong_up'
        elif pct_change > 1:
            direction = 'moderate_up'
        elif pct_change > -1:
            direction = 'stable'
        elif pct_change > -5:
            direction = 'moderate_down'
        else:
            direction = 'strong_down'

        return {
            'direction': direction,
            'percentage_change': pct_change,
            'slope': slope,
            'correlation': abs(correlation) if not np.isnan(correlation) else 0.0,
            'values': values
        }

    def _calculate_growth_rates(self, financial_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate growth rates for key metrics."""
        growth_rates = {}

        # Extract comparable periods
        income_statement = financial_data.get('income_statement', {})
        balance_sheet = financial_data.get('balance_sheet', {})

        periods = sorted(income_statement.keys())
        if len(periods) < 2:
            return growth_rates

        for metric in ['revenue', 'net_income', 'total_assets', 'total_equity']:
            growth_rate = self._calculate_metric_growth(metric, periods, income_statement, balance_sheet)
            if growth_rate is not None:
                growth_rates[metric] = growth_rate

        return growth_rates

    def _calculate_metric_growth(self, metric: str, periods: List[str],
                               income_statement: Dict[str, Any],
                               balance_sheet: Dict[str, Any]) -> Optional[Dict[str, float]]:
        """Calculate growth rate for a specific metric."""
        try:
            current_value = None
            previous_value = None

            # Find values in income statement
            if metric in income_statement.get(periods[-1], {}):
                current_value = income_statement[periods[-1]][metric]
            if metric in income_statement.get(periods[-2], {}):
                previous_value = income_statement[periods[-2]][metric]

            # Find values in balance sheet
            if current_value is None and metric in balance_sheet.get(periods[-1], {}):
                current_value = balance_sheet[periods[-1]][metric]
            if previous_value is None and metric in balance_sheet.get(periods[-2], {}):
                previous_value = balance_sheet[periods[-2]][metric]

            if current_value is not None and previous_value is not None and previous_value != 0:
                growth_rate = ((current_value - previous_value) / abs(previous_value)) * 100
                return {
                    'period': f"{periods[-2]} to {periods[-1]}",
                    'growth_rate': growth_rate,
                    'current_value': current_value,
                    'previous_value': previous_value
                }

        except Exception as e:
            logger.warning(f"Error calculating growth rate for {metric}: {e}")

        return None

    def _assess_financial_health(self, ratios: Dict[str, Dict[str, float]]) -> Dict[str, Any]:
        """Assess overall financial health based on ratios."""
        health_score = 0.0
        max_score = 0.0
        issues = []

        # Liquidity assessment
        liquidity_ratios = ratios.get('liquidity', {})
        current_ratio = self._get_latest_ratio(liquidity_ratios, 'current_ratio')
        if current_ratio is not None:
            max_score += 25.0
            if current_ratio >= 1.5:
                health_score += 25.0
            elif current_ratio >= 1.0:
                health_score += 12.5
            else:
                issues.append(f"Low current ratio: {current_ratio:.2f}")

        # Profitability assessment
        profitability_ratios = ratios.get('profitability', {})
        net_margin = self._get_latest_ratio(profitability_ratios, 'net_margin')
        if net_margin is not None:
            max_score += 25.0
            if net_margin >= 0.1:
                health_score += 25.0
            elif net_margin >= 0.05:
                health_score += 12.5
            else:
                issues.append(f"Low net margin: {net_margin:.2%}")

        # Leverage assessment
        leverage_ratios = ratios.get('leverage', {})
        debt_to_equity = self._get_latest_ratio(leverage_ratios, 'debt_to_equity')
        if debt_to_equity is not None:
            max_score += 25.0
            if debt_to_equity <= 1.0:
                health_score += 25.0
            elif debt_to_equity <= 2.0:
                health_score += 12.5
            else:
                issues.append(f"High debt-to-equity ratio: {debt_to_equity:.2f}")

        # Efficiency assessment
        efficiency_ratios = ratios.get('efficiency', {})
        asset_turnover = self._get_latest_ratio(efficiency_ratios, 'asset_turnover')
        if asset_turnover is not None:
            max_score += 25.0
            if asset_turnover >= 0.5:
                health_score += 25.0
            elif asset_turnover >= 0.25:
                health_score += 12.5
            else:
                issues.append(f"Low asset turnover: {asset_turnover:.2f}")

        # Calculate final score
        final_score = (health_score / max_score) * 100 if max_score > 0 else 0.0

        # Determine health level
        if final_score >= 80:
            health_level = 'Excellent'
        elif final_score >= 60:
            health_level = 'Good'
        elif final_score >= 40:
            health_level = 'Fair'
        else:
            health_level = 'Poor'

        return {
            'score': final_score,
            'level': health_level,
            'issues': issues,
            'max_score': max_score,
            'current_score': health_score
        }

    def _get_latest_ratio(self, ratios: Dict[str, float], ratio_name: str) -> Optional[float]:
        """Get the most recent value for a specific ratio."""
        latest_values = [v for k, v in ratios.items() if ratio_name in k]
        return latest_values[-1] if latest_values else None

    def benchmark_ratios(self, company_ratios: Dict[str, float],
                        industry_benchmarks: Dict[str, float]) -> Dict[str, Any]:
        """
        Benchmark company ratios against industry standards.

        Args:
            company_ratios: Company's financial ratios
            industry_benchmarks: Industry standard ratios

        Returns:
            Benchmarking analysis
        """
        benchmarking = {}

        for ratio_name, company_value in company_ratios.items():
            if ratio_name in industry_benchmarks:
                industry_value = industry_benchmarks[ratio_name]
                difference = company_value - industry_value
                percentage_diff = (difference / industry_value) * 100 if industry_value != 0 else 0

                benchmarking[ratio_name] = {
                    'company_value': company_value,
                    'industry_value': industry_value,
                    'difference': difference,
                    'percentage_difference': percentage_diff,
                    'performance': self._assess_performance(company_value, industry_value, ratio_name)
                }

        self.benchmarking = benchmarking
        return benchmarking

    def _assess_performance(self, company_value: float, industry_value: float,
                          ratio_name: str) -> str:
        """Assess whether company performance is above or below industry standard."""
        if ratio_name in ['current_ratio', 'quick_ratio', 'cash_ratio']:
            # Higher is better for liquidity ratios
            return 'Above' if company_value > industry_value else 'Below'
        elif ratio_name in ['gross_margin', 'net_margin', 'roe', 'roa']:
            # Higher is better for profitability ratios
            return 'Above' if company_value > industry_value else 'Below'
        elif ratio_name in ['debt_to_equity', 'debt_to_assets']:
            # Lower is better for leverage ratios
            return 'Above' if company_value < industry_value else 'Below'
        else:
            # Default: higher is better
            return 'Above' if company_value > industry_value else 'Below'


def main():
    """Example usage of FinancialAnalyzer."""
    analyzer = FinancialAnalyzer()

    # Example financial data structure
    sample_data = {
        'income_statement': {
            '2023': {
                'revenue': 1000000,
                'cost_of_goods_sold': 600000,
                'gross_profit': 400000,
                'operating_income': 200000,
                'net_income': 150000
            },
            '2022': {
                'revenue': 800000,
                'cost_of_goods_sold': 480000,
                'gross_profit': 320000,
                'operating_income': 160000,
                'net_income': 120000
            }
        },
        'balance_sheet': {
            '2023': {
                'total_current_assets': 500000,
                'cash_and_cash_equivalents': 100000,
                'inventory': 150000,
                'total_assets': 1200000,
                'total_current_liabilities': 250000,
                'total_liabilities': 600000,
                'total_equity': 600000
            },
            '2022': {
                'total_current_assets': 450000,
                'cash_and_cash_equivalents': 90000,
                'inventory': 140000,
                'total_assets': 1100000,
                'total_current_liabilities': 220000,
                'total_liabilities': 550000,
                'total_equity': 550000
            }
        }
    }

    # Analyze financial statements
    results = analyzer.analyze_financial_statements(sample_data)

    print("Financial Analysis Results:")
    print(f"Ratios: {results['ratios']}")
    print(f"Trends: {results['trends']}")
    print(f"Financial Health: {results['financial_health']}")


if __name__ == "__main__":
    main()