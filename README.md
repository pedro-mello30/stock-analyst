# Economics Workspace

Structured financial analysis environment for SEC filings and corporate valuation.

## Project State
This workspace is in its early stages, focused on building robust analysis frameworks using Claude Skills. Current analysis is centered on **NVIDIA (NVDA)** using their **Q3 FY2026 10-Q** filing.

## Core Capabilities
- **Structured Analysis**: Defined workflows for Income Statement, Balance Sheet, and Cash Flow Statement analysis under `.claude/skills/`.
- **Data Visualization**: Integrated Python charting engine for creating financial Sankey diagrams, waterfall charts, and trend lines.
- **Company-Centric Org**: Data, analysis reports, and charts are organized by ticker within the `companies/` directory.

## Current Focus
1. Refining the NVIDIA Q3 2025 analysis.
2. Perfecting the financial charting theme system.
3. Establishing baseline metrics for modern tech companies.

## Future Roadmap
- [ ] **Data Extraction Pipeline**: Automation scripts to extract financial tables from SEC PDFs into structured JSON/CSV data.
- [ ] **DCF Model Integration**: Standardized Discounted Cash Flow modeling templates.
- [ ] **Peer Benchmarking**: Tools to automatically compare a target company against a set of competitors.
- [ ] **Knowledge Graph**: Linking financial metrics across quarters to visualize long-term performance shifts.

## Usage
Analysis frameworks are implemented as Claude Skills. Trigger them by asking for an analysis of a specific financial statement or by calling the charting skill for visualizations.
