#!/usr/bin/env python3
"""
Chart Generator for SEC Filings Analysis

Creates professional financial charts including ratio analysis, trend charts,
and waterfall charts for investment reports and presentations.
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from typing import Dict, List, Any, Optional, Tuple, Union
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import logging
import re

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set matplotlib style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")


class ChartGenerator:
    """Main class for generating professional financial charts."""

    def __init__(self, output_dir: str = "charts"):
        """
        Initialize chart generator.

        Args:
            output_dir: Directory to save generated charts
        """
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Chart styling configuration
        self.colors = {
            'primary': '#2E86AB',
            'secondary': '#A23B72',
            'tertiary': '#F18F01',
            'success': '#C73E1D',
            'background': '#FFFFFF',
            'text': '#333333'
        }

    def create_ratio_analysis_chart(self, ratios_data: Dict[str, Dict[str, float]],
                                   company_name: str = "Company") -> str:
        """
        Create ratio analysis chart showing key ratios over time.

        Args:
            ratios_data: Ratio data with time series
            company_name: Company name for chart title

        Returns:
            File path of saved chart
        """
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle(f'{company_name} - Financial Ratio Analysis', fontsize=16, fontweight='bold')

        # Liquidity Ratios
        self._plot_ratio_trend(ratios_data.get('liquidity', {}),
                             ['current_ratio', 'quick_ratio'],
                             axes[0, 0], 'Liquidity Ratios', 'Current/Quick Ratio')

        # Profitability Ratios
        self._plot_ratio_trend(ratios_data.get('profitability', {}),
                             ['gross_margin', 'net_margin', 'roe'],
                             axes[0, 1], 'Profitability Ratios', 'Margin/ROE (%)')

        # Leverage Ratios
        self._plot_ratio_trend(ratios_data.get('leverage', {}),
                             ['debt_to_equity', 'debt_to_assets'],
                             axes[1, 0], 'Leverage Ratios', 'Debt Ratios')

        # Efficiency Ratios
        self._plot_ratio_trend(ratios_data.get('efficiency', {}),
                             ['asset_turnover', 'inventory_turnover'],
                             axes[1, 1], 'Efficiency Ratios', 'Turnover Ratio')

        plt.tight_layout()
        output_path = os.path.join(self.output_dir, f"{company_name.replace(' ', '_')}_ratio_analysis.png")
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()

        logger.info(f"Ratio analysis chart saved: {output_path}")
        return output_path

    def create_trend_analysis_chart(self, financial_data: Dict[str, Any],
                                  company_name: str = "Company") -> str:
        """
        Create trend analysis chart showing key financial metrics over time.

        Args:
            financial_data: Financial data with time series
            company_name: Company name for chart title

        Returns:
            File path of saved chart
        """
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle(f'{company_name} - Financial Trend Analysis', fontsize=16, fontweight='bold')

        # Revenue Trend
        revenue_data = self._extract_metric_trend(financial_data, 'revenue')
        self._plot_financial_trend(revenue_data, axes[0, 0], 'Revenue Trend', 'Revenue ($)', 'blue')

        # Net Income Trend
        net_income_data = self._extract_metric_trend(financial_data, 'net_income')
        self._plot_financial_trend(net_income_data, axes[0, 1], 'Net Income Trend', 'Net Income ($)', 'green')

        # Margin Trend
        margin_data = self._calculate_margin_trend(financial_data)
        self._plot_financial_trend(margin_data, axes[1, 0], 'Profit Margin Trend', 'Margin (%)', 'orange')

        # EPS Trend (if available)
        eps_data = self._extract_metric_trend(financial_data, 'eps')
        self._plot_financial_trend(eps_data, axes[1, 1], 'EPS Trend', 'EPS ($)', 'red')

        plt.tight_layout()
        output_path = os.path.join(self.output_dir, f"{company_name.replace(' ', '_')}_trend_analysis.png")
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()

        logger.info(f"Trend analysis chart saved: {output_path}")
        return output_path

    def create_waterfall_chart(self, cash_flow_data: Dict[str, Dict[str, float]],
                             company_name: str = "Company") -> str:
        """
        Create waterfall chart for cash flow analysis.

        Args:
            cash_flow_data: Cash flow data with components
            company_name: Company name for chart title

        Returns:
            File path of saved chart
        """
        fig, ax = plt.subplots(figsize=(14, 8))

        # Prepare data
        components = []
        values = []
        colors = []

        # Get the most recent period data
        latest_period = max(cash_flow_data.keys()) if cash_flow_data else None
        if not latest_period:
            logger.warning("No cash flow data available for waterfall chart")
            return None

        period_data = cash_flow_data[latest_period]

        # Define cash flow components in order
        component_order = [
            'net_income',
            'depreciation_amortization',
            'changes_in_working_capital',
            'capital_expenditures',
            'free_cash_flow'
        ]

        for component in component_order:
            if component in period_data:
                components.append(component.replace('_', ' ').title())
                value = period_data[component]
                values.append(value)
                colors.append('green' if value >= 0 else 'red')

        # Create waterfall chart
        self._plot_waterfall(components, values, colors, ax, company_name)

        output_path = os.path.join(self.output_dir, f"{company_name.replace(' ', '_')}_cash_flow_waterfall.png")
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()

        logger.info(f"Waterfall chart saved: {output_path}")
        return output_path

    def create_executive_summary_charts(self, key_metrics: Dict[str, float],
                                      company_name: str = "Company") -> Dict[str, str]:
        """
        Create executive summary dashboard charts.

        Args:
            key_metrics: Key financial metrics
            company_name: Company name for chart titles

        Returns:
            Dictionary of chart file paths
        """
        charts = {}

        # Create pie chart for revenue breakdown (if available)
        if 'revenue_by_segment' in key_metrics:
            chart_path = self._create_pie_chart(key_metrics['revenue_by_segment'],
                                              f"{company_name} - Revenue by Segment",
                                              f"{company_name.replace(' ', '_')}_revenue_breakdown.png")
            charts['revenue_breakdown'] = chart_path

        # Create bar chart for key ratios
        ratios = {k: v for k, v in key_metrics.items() if 'ratio' in k.lower()}
        if ratios:
            chart_path = self._create_bar_chart(ratios,
                                              f"{company_name} - Key Ratios",
                                              f"{company_name.replace(' ', '_')}_key_ratios.png")
            charts['key_ratios'] = chart_path

        # Create gauge chart for financial health score
        if 'financial_health_score' in key_metrics:
            chart_path = self._create_gauge_chart(key_metrics['financial_health_score'],
                                                f"{company_name} - Financial Health",
                                                f"{company_name.replace(' ', '_')}_health_score.png")
            charts['health_score'] = chart_path

        # Create risk heatmap (if risk data available)
        if 'risk_factors' in key_metrics:
            chart_path = self._create_risk_heatmap(key_metrics['risk_factors'],
                                                 f"{company_name} - Risk Assessment",
                                                 f"{company_name.replace(' ', '_')}_risk_heatmap.png")
            charts['risk_heatmap'] = chart_path

        return charts

    def create_comparative_analysis_chart(self, companies_data: Dict[str, Dict[str, float]],
                                        metric: str, company_name: str = "Company") -> str:
        """
        Create comparative analysis chart for multiple companies.

        Args:
            companies_data: Data for multiple companies
            metric: Metric to compare
            company_name: Reference company name

        Returns:
            File path of saved chart
        """
        fig, ax = plt.subplots(figsize=(12, 8))

        companies = list(companies_data.keys())
        values = [companies_data[comp].get(metric, 0) for comp in companies]

        bars = ax.bar(companies, values, color=self.colors['primary'], alpha=0.8)

        # Highlight the reference company
        if company_name in companies:
            idx = companies.index(company_name)
            bars[idx].set_color(self.colors['secondary'])

        ax.set_title(f'{metric.replace("_", " ").title()} - Company Comparison', fontsize=14, fontweight='bold')
        ax.set_ylabel(metric.replace('_', ' ').title())
        ax.set_xlabel('Companies')
        ax.grid(True, alpha=0.3)

        # Add value labels on bars
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + max(values)*0.01,
                   f'{value:.2f}', ha='center', va='bottom')

        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        output_path = os.path.join(self.output_dir, f"{company_name.replace(' ', '_')}_comparative_{metric}.png")
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()

        logger.info(f"Comparative analysis chart saved: {output_path}")
        return output_path

    def export_charts_to_png(self, chart_objects: List[Any],
                           company_name: str) -> Dict[str, str]:
        """
        Export multiple chart objects to PNG files.

        Args:
            chart_objects: List of matplotlib figure objects
            company_name: Company name for file naming

        Returns:
            Dictionary of chart descriptions and file paths
        """
        exported_charts = {}

        for i, chart_obj in enumerate(chart_objects):
            filename = f"{company_name.replace(' ', '_')}_chart_{i+1}.png"
            output_path = os.path.join(self.output_dir, filename)

            chart_obj.savefig(output_path, dpi=300, bbox_inches='tight')
            exported_charts[f"chart_{i+1}"] = output_path

        logger.info(f"Exported {len(chart_objects)} charts for {company_name}")
        return exported_charts

    def _plot_ratio_trend(self, ratios_dict: Dict[str, float], ratio_names: List[str],
                         ax, title: str, ylabel: str):
        """Plot ratio trends for specific ratio types."""
        periods = []
        ratio_data = {name: [] for name in ratio_names}

        # Extract periods and data
        for key, value in ratios_dict.items():
            for ratio_name in ratio_names:
                if ratio_name in key.lower():
                    # Extract period from key (assuming format like 'current_ratio_2023')
                    period_match = re.search(r'(\d{4})$', key)
                    if period_match:
                        period = period_match.group(1)
                        if period not in periods:
                            periods.append(period)
                        ratio_data[ratio_name].append(value)

        # Plot each ratio
        for i, ratio_name in enumerate(ratio_names):
            if ratio_data[ratio_name]:
                ax.plot(range(len(periods)), ratio_data[ratio_name],
                       marker='o', label=ratio_name.replace('_', ' ').title(),
                       color=self.colors['primary'] if i == 0 else self.colors['secondary'])

        ax.set_title(title, fontweight='bold')
        ax.set_ylabel(ylabel)
        ax.set_xticks(range(len(periods)))
        ax.set_xticklabels(periods)
        ax.legend()
        ax.grid(True, alpha=0.3)

    def _plot_financial_trend(self, data: List[Tuple[str, float]], ax, title: str,
                            ylabel: str, color: str):
        """Plot financial metric trends."""
        if not data:
            ax.text(0.5, 0.5, 'No Data Available', ha='center', va='center', transform=ax.transAxes)
            ax.set_title(title)
            return

        periods, values = zip(*data)

        ax.plot(range(len(periods)), values, marker='o', color=color, linewidth=2)
        ax.fill_between(range(len(periods)), values, alpha=0.3, color=color)

        ax.set_title(title, fontweight='bold')
        ax.set_ylabel(ylabel)
        ax.set_xticks(range(len(periods)))
        ax.set_xticklabels(periods)
        ax.grid(True, alpha=0.3)

    def _plot_waterfall(self, labels: List[str], values: List[float],
                       colors: List[str], ax, company_name: str):
        """Create waterfall chart."""
        # Calculate cumulative values
        cumulative = [0]
        for i, value in enumerate(values[:-1]):
            cumulative.append(cumulative[-1] + value)

        # Plot bars
        bars = ax.bar(range(len(labels)), values, color=colors, alpha=0.8)

        # Add connectors
        for i in range(len(cumulative) - 1):
            ax.plot([i, i + 1], [cumulative[i + 1], cumulative[i + 1]],
                   color='black', linewidth=1)

        # Add value labels
        for i, (bar, value) in enumerate(zip(bars, values)):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + max(values)*0.02,
                   f'${value:,.0f}', ha='center', va='bottom', fontweight='bold')

        ax.set_title(f'{company_name} - Cash Flow Waterfall Analysis', fontsize=14, fontweight='bold')
        ax.set_ylabel('Cash Flow ($)')
        ax.set_xticks(range(len(labels)))
        ax.set_xticklabels(labels, rotation=45, ha='right')
        ax.grid(True, alpha=0.3)

    def _extract_metric_trend(self, financial_data: Dict[str, Any], metric: str) -> List[Tuple[str, float]]:
        """Extract time series data for a specific metric."""
        trend_data = []

        # Check income statement
        income_statement = financial_data.get('income_statement', {})
        for period, data in income_statement.items():
            if metric in data:
                trend_data.append((period, float(data[metric])))

        # Check balance sheet
        balance_sheet = financial_data.get('balance_sheet', {})
        for period, data in balance_sheet.items():
            metric_key = f"{period}_{metric}"
            if metric in data:
                trend_data.append((period, float(data[metric])))

        # Sort by period
        trend_data.sort(key=lambda x: x[0])
        return trend_data

    def _calculate_margin_trend(self, financial_data: Dict[str, Any]) -> List[Tuple[str, float]]:
        """Calculate margin trend from revenue and net income."""
        margin_data = []

        income_statement = financial_data.get('income_statement', {})
        for period, data in income_statement.items():
            revenue = data.get('revenue', 0)
            net_income = data.get('net_income', 0)

            if revenue != 0:
                margin = (net_income / revenue) * 100
                margin_data.append((period, margin))

        margin_data.sort(key=lambda x: x[0])
        return margin_data

    def _create_pie_chart(self, data: Dict[str, float], title: str, filename: str) -> str:
        """Create pie chart."""
        fig, ax = plt.subplots(figsize=(10, 8))

        labels = list(data.keys())
        values = list(data.values())

        wedges, texts, autotexts = ax.pie(values, labels=labels, autopct='%1.1f%%',
                                         colors=plt.cm.Set3.colors,
                                         startangle=90)

        ax.set_title(title, fontsize=14, fontweight='bold')

        output_path = os.path.join(self.output_dir, filename)
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()

        return output_path

    def _create_bar_chart(self, data: Dict[str, float], title: str, filename: str) -> str:
        """Create bar chart."""
        fig, ax = plt.subplots(figsize=(12, 6))

        labels = list(data.keys())
        values = list(data.values())

        bars = ax.bar(labels, values, color=self.colors['primary'], alpha=0.8)

        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_ylabel('Value')

        # Add value labels
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + max(values)*0.01,
                   f'{value:.2f}', ha='center', va='bottom')

        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        output_path = os.path.join(self.output_dir, filename)
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()

        return output_path

    def _create_gauge_chart(self, score: float, title: str, filename: str) -> str:
        """Create gauge chart for financial health score."""
        fig, ax = plt.subplots(figsize=(10, 8), subplot_kw={'projection': 'polar'})

        # Normalize score to 0-1 range
        normalized_score = min(max(score / 100, 0), 1)

        # Create gauge
        theta = np.linspace(0, np.pi, 100)
        radius = np.ones_like(theta)

        # Color based on score
        if score >= 80:
            color = 'green'
        elif score >= 60:
            color = 'yellow'
        else:
            color = 'red'

        ax.plot(theta, radius, 'k-', linewidth=2)
        ax.fill_between(theta, 0, radius, color=color, alpha=0.3)

        # Add needle
        needle_angle = normalized_score * np.pi
        ax.plot([needle_angle, needle_angle], [0, 1], 'k-', linewidth=4)

        ax.set_ylim(0, 1.2)
        ax.set_theta_zero_location('W')
        ax.set_theta_direction(1)
        ax.set_thetagrids([0, 45, 90, 135, 180], ['0', '25', '50', '75', '100'])
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)

        output_path = os.path.join(self.output_dir, filename)
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()

        return output_path

    def _create_risk_heatmap(self, risk_data: Dict[str, float], title: str, filename: str) -> str:
        """Create risk heatmap."""
        fig, ax = plt.subplots(figsize=(10, 6))

        # Create heatmap data
        risk_categories = list(risk_data.keys())
        risk_scores = [[score] for score in risk_data.values()]

        im = ax.imshow(risk_scores, cmap='Reds', aspect='auto')

        # Set ticks and labels
        ax.set_yticks(range(len(risk_categories)))
        ax.set_yticklabels(risk_categories)
        ax.set_xticks([])
        ax.set_xlabel('Risk Level')

        # Add colorbar
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Risk Score')

        ax.set_title(title, fontsize=14, fontweight='bold')
        plt.tight_layout()

        output_path = os.path.join(self.output_dir, filename)
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()

        return output_path


def main():
    """Example usage of ChartGenerator."""
    generator = ChartGenerator()

    # Sample data for demonstration
    sample_ratios = {
        'liquidity': {
            'current_ratio_2023': 1.5,
            'current_ratio_2022': 1.3,
            'quick_ratio_2023': 1.2,
            'quick_ratio_2022': 1.0
        },
        'profitability': {
            'gross_margin_2023': 0.45,
            'gross_margin_2022': 0.42,
            'net_margin_2023': 0.12,
            'net_margin_2022': 0.10
        }
    }

    sample_financial_data = {
        'income_statement': {
            '2023': {'revenue': 1000000, 'net_income': 150000},
            '2022': {'revenue': 800000, 'net_income': 120000}
        }
    }

    # Generate charts
    ratio_chart = generator.create_ratio_analysis_chart(sample_ratios, "Sample Company")
    trend_chart = generator.create_trend_analysis_chart(sample_financial_data, "Sample Company")

    print(f"Generated charts:")
    print(f"- Ratio Analysis: {ratio_chart}")
    print(f"- Trend Analysis: {trend_chart}")


if __name__ == "__main__":
    main()