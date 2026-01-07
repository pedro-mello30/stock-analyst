---
name: sec-filings-analysis
description: Comprehensive SEC filings analysis skill for analyzing 10-K, 10-Q, and 8-K filings with financial ratio calculations, risk assessment, and professional report generation. Use when analyzing SEC filings, financial statements, or creating investment theses with charts and visualizations.
---

# SEC Filings Analysis Skill

## Overview

This skill provides a complete solution for analyzing SEC filings (10-K, 10-Q, 8-K) and financial statements. It extracts financial data from PDF, HTML, and Excel formats, calculates key financial ratios, assesses risk factors, generates professional charts, and produces detailed analysis reports and investment theses.

**When to Use This Skill:**
- Analyzing SEC filings for investment research
- Creating financial analysis reports
- Generating investment theses with data visualization
- Comparing company financial performance
- Risk factor assessment from qualitative disclosures

## Quick Start

### Basic Usage
```bash
# Analyze a 10-K filing and generate detailed report
python sec_filing_analyzer.py --file form-10k-apple-2024.pdf --report-type analysis

# Create investment thesis from quarterly filing
python sec_filing_analyzer.py --file form-10q-nvidia-q3-2025.pdf --report-type thesis

# Batch process multiple filings
python sec_filing_analyzer.py --directory sec_filings/ --output reports/
```

### Supported File Types
- **PDF**: SEC filings with embedded financial statements
- **HTML**: Web-based SEC filings and investor presentations
- **Excel**: Financial statement spreadsheets and data files

## Analysis Capabilities

### 1. Financial Ratio Analysis
**Purpose**: Calculate and analyze key financial metrics across multiple periods

**Key Ratios:**
- **Liquidity**: Current ratio, Quick ratio, Cash ratio
- **Profitability**: Gross margin, Operating margin, Net margin, ROE
- **Efficiency**: Asset turnover, Inventory turnover, Receivables turnover
- **Leverage**: Debt-to-equity, Debt-to-assets, Interest coverage

**Usage Example:**
```python
from scripts.financial_analyzer import calculate_profitability_ratios

# Calculate ratios from income statement data
ratios = calculate_profitability_ratios(income_statement_data)
print(f"Gross Margin: {ratios['gross_margin']:.2%}")
```

### 2. Trend Analysis
**Purpose**: Identify financial trends and performance patterns over time

**Analysis Features:**
- Year-over-Year (YoY) growth rates
- Quarter-over-Quarter (QoQ) changes
- Multi-period trend visualization
- Performance benchmarking

**Output:** Trend charts showing revenue, EPS, and margin evolution

### 3. Risk Factor Assessment
**Purpose**: Analyze qualitative risk factors from management discussion

**Risk Categories:**
- **Market Risks**: Economic conditions, competitive landscape
- **Operational Risks**: Supply chain, technology, regulatory
- **Financial Risks**: Liquidity, credit, currency exposure
- **Regulatory Risks**: Legal compliance, industry regulations

**Features:**
- Automatic risk factor extraction
- Risk severity scoring
- Categorical classification
- Executive summary generation

### 4. Chart Generation
**Purpose**: Create professional financial visualizations

**Chart Types:**
- **Ratio Analysis Charts**: Multi-line charts showing key ratios over time
- **Trend Analysis Charts**: Revenue, EPS, and margin evolution
- **Waterfall Charts**: Cash flow components and financial changes
- **Executive Summary Dashboards**: Key metrics visualization

**Output Formats:** High-resolution PNG, embeddable in reports

## Report Generation

### 1. Detailed Analysis Report (PPTX)
**Format**: 15-20 slide professional presentation
**Content**:
- Executive summary with key findings
- Financial highlights and performance metrics
- Ratio analysis with trend charts
- Risk assessment and mitigation strategies
- Valuation metrics and comparables
- Investment recommendations

### 2. Investment Thesis (DOCX)
**Format**: 8-10 page comprehensive document
**Content**:
- Company overview and business model
- Industry analysis and competitive positioning
- Financial analysis and projections
- Risk assessment and scenario analysis
- Valuation methodology and price targets
- Investment thesis and conclusion

### 3. Executive Summary (PPTX)
**Format**: 5-7 slide high-level overview
**Content**: Key metrics, investment highlights, risks, and recommendations

## Workflow

### Step 1: File Processing
```python
from scripts.file_processor import extract_pdf_data

# Extract structured data from SEC filing
financial_data = extract_pdf_data("form-10k-company-2024.pdf")
```

### Step 2: Financial Analysis
```python
from scripts.financial_analyzer import analyze_financial_statements

# Calculate ratios and identify trends
analysis_results = analyze_financial_statements(financial_data)
```

### Step 3: Risk Assessment
```python
from scripts.risk_assessment import assess_company_risks

# Analyze qualitative risk factors
risk_assessment = assess_company_risks(filing_text)
```

### Step 4: Chart Generation
```python
from scripts.chart_generator import create_financial_charts

# Generate professional visualizations
charts = create_financial_charts(analysis_results)
```

### Step 5: Report Assembly
```python
from scripts.report_generator import generate_analysis_report

# Create comprehensive analysis report
report = generate_analysis_report(company_data, charts, risk_assessment)
```

## Integration with Analysis Guides

This skill integrates with your existing analysis framework from `resources.md`:

- **Income Statement Analysis**: Used in profitability ratio calculations
- **Balance Sheet Analysis**: Applied to liquidity and leverage ratios
- **Cash Flow Analysis**: Core component of waterfall charts
- **Stock Types and Valuation**: Incorporated into investment thesis framework

## Best Practices

### Data Quality
- Always validate extracted financial data
- Cross-reference multiple data sources when available
- Handle missing or inconsistent data appropriately

### Analysis Standards
- Use consistent calculation methods across periods
- Benchmark against relevant industry peers
- Consider both absolute and relative performance

### Report Quality
- Ensure all charts are properly labeled and sourced
- Maintain consistent formatting and branding
- Include clear executive summaries for busy investors

## Examples

### Example 1: Quarterly Analysis
**Input**: NVIDIA Form 10-Q for Q3 2025
**Output**: Detailed analysis report with revenue trends, margin analysis, and risk assessment

### Example 2: Annual Review
**Input**: Apple Inc. Form 10-K for 2024
**Output**: Comprehensive investment thesis with valuation analysis and long-term outlook

### Example 3: Comparative Analysis
**Input**: Multiple 10-K filings from competitors
**Output**: Industry benchmarking report with competitive positioning analysis

## Resources

This skill includes specialized resource directories:

### scripts/
Core analysis engine with executable Python modules:
- `file_processor.py`: Multi-format SEC filing extraction
- `financial_analyzer.py`: Financial ratio and trend analysis
- `risk_assessment.py`: Qualitative risk factor analysis
- `chart_generator.py`: Professional chart creation
- `report_generator.py`: PPTX/DOCX report assembly

### references/
Detailed documentation and analysis frameworks:
- `financial_metrics.md`: Key ratio definitions and formulas
- `sec_filing_types.md`: 10-K, 10-Q, 8-K breakdowns and analysis opportunities
- `chart_templates.md`: Chart specifications and formatting standards
- `analysis_framework.md`: Step-by-step analysis methodology

### assets/
Professional templates and chart assets:
- `templates/analysis_report.pptx`: 15-20 slide detailed analysis template
- `templates/investment_thesis.docx`: 8-10 page investment thesis template
- `templates/executive_summary.pptx`: 5-7 slide executive summary template
- `charts/`: Template files for professional chart creation

**Note:** This skill is designed for professional financial analysis and investment research. Always verify results and consider multiple data sources for critical decisions.
