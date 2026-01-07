# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Financial Analysis Knowledge Base focused on SEC filing analysis. The primary purpose is to provide structured frameworks and skills for analyzing company financial statements, with current emphasis on income statement (P&L) analysis.

## Architecture

**Skill-Based Structure**: All financial analysis knowledge is organized as Claude Skills under `.claude/skills/`:

```
.claude/skills/
└── income-statement-analysis/
    ├── SKILL.md              # 7-step analysis workflow
    └── references/
        ├── analysis-framework.md  # Comprehensive analysis checklist
        └── metrics-formulas.md    # Financial metrics with benchmarks
```

**Reference Data**: `companies/nvidia/inputs/sec-filings/10-q/2025-q3_form-10-q_oct26.pdf` provides a real SEC 10-Q filing example for testing analysis workflows.

## Using the Income Statement Analysis Skill

The skill triggers automatically when analyzing income statements, P&L statements, margins, revenue, or expense breakdowns. It follows a structured 7-step workflow:

1. Revenue & Growth Analysis
2. Gross Margin Evaluation
3. Operating Expenses Breakdown
4. Operating Margin Assessment
5. Time-Based Analysis (QoQ/YoY)
6. Competitive Benchmarking
7. GAAP vs Non-GAAP Reconciliation

Reference files provide detailed checklists (`analysis-framework.md`) and metric formulas with industry benchmarks (`metrics-formulas.md`).

## Key Financial Metrics

Core margins tracked: Gross Margin, Operating Margin, Net Margin. Industry benchmarks are documented for Amazon, Microsoft, Google, and Costco as reference points.

## Extending the Project

Additional analysis skills (Balance Sheet, Cash Flow Statement) can follow the same pattern:
- Create skill directory under `.claude/skills/`
- Add `SKILL.md` with workflow steps
- Add `references/` with supporting documentation

## Notes

- No build system currently configured (documentation-only project)
- Archived Python analysis tools exist in git history under `archieve/SEC-Filings-Analysis/` if restoration is needed
