# CLAUDE.md

This file provides guidance to Claude Code when working in this repository.

## Project Overview
A specialized environment for structured financial analysis of SEC filings. The project currently focuses on analyzing NVIDIA using its 2025-Q3 10-Q filing.

## Directory Structure
- `.claude/skills/`: Domain-specific analysis frameworks and automation logic.
- `companies/`: Input data (SEC filings), analysis reports (MD), and output visualizations (charts).
  - `nvidia/`: Active analysis target.

## Analysis Skills
The workspace leverages four primary skills located in `.claude/skills/`:
1. **Income Statement Analysis**: 7-step P&L evaluation framework.
2. **Balance Sheet Analysis**: 7-step financial health and solvency framework.
3. **Cash Flow Analysis**: 5-step methodology for understanding cash generation.
4. **Financial Charts**: Python-based plotting system for Sankey, Waterfall, Bar, and Line charts.

## Workflow Patterns
1. **Data Ingestion**: Place SEC PDFs in `companies/[ticker]/inputs/sec-filings/`.
2. **Analysis**: Execute the structured analysis steps from the relevant skill.
3. **Visualization**: Use the `financial-charts` skill to generate supporting visual evidence.

## Future Improvements
- **Automated Extraction**: Develop scripts to parse tables directly from SEC PDFs into structured formats (JSON/CSV).
- **Multi-Ticker Comparison**: Expand framework to handle parallel analysis of peer groups.
- **Trend Database**: Implement a simple storage layer to track metrics across multiple quarters for historical trend analysis.
