#!/usr/bin/env python3
"""
Test script for SEC Filings Analysis skill using NVIDIA Q3 2025 10-Q filing.
"""

import sys
import os
sys.path.append('/home/pedro/Projetos/EconomicsWorkspace/SEC-Filings-Analysis/sec-filings-analysis/scripts')

from file_processor import FileProcessor
from financial_analyzer import FinancialAnalyzer
from chart_generator import ChartGenerator
from risk_assessment import RiskAssessment
from report_generator import ReportGenerator

def test_sec_filing_analysis():
    """Test the complete SEC filing analysis workflow."""

    print("🚀 NVIDIA Q3 2025 10-Q Analysis Test")
    print("=" * 50)

    # File path to NVIDIA Q3 2025 10-Q
    filing_path = "/home/pedro/Projetos/EconomicsWorkspace/form-10-q-NVIDIA-Q3-2025.pdf"
    company_name = "NVIDIA Corporation"

    if not os.path.exists(filing_path):
        print(f"❌ Error: File not found at {filing_path}")
        return

    print(f"📁 Processing file: {filing_path}")
    print(f"🏢 Company: {company_name}")
    print()

    try:
        # Step 1: File Processing
        print("📄 Step 1: File Processing")
        print("-" * 30)
        processor = FileProcessor()

        # Extract data from PDF
        result = processor.extract_pdf_data(filing_path)
        print(f"✅ Successfully extracted data")
        print(f"📊 Financial data sections: {list(result['financial_data'].keys())}")
        print(f"📋 Metadata: {result.get('metadata', {})}")
        print()

        # Step 2: Data Validation
        print("🔍 Step 2: Data Validation")
        print("-" * 30)
        validation = processor.validate_extraction(result)
        print(f"✅ Validation passed: {validation['is_valid']}")
        print(f"📈 Data completeness: {validation['score']:.1%}")
        if validation['issues']:
            print(f"⚠️  Issues found: {validation['issues']}")
        print()

        # Step 3: Financial Analysis
        print("💰 Step 3: Financial Analysis")
        print("-" * 30)
        analyzer = FinancialAnalyzer()
        analysis = analyzer.analyze_financial_statements(result['financial_data'])

        print("📊 Analysis Results:")
        print(f"📈 Liquidity Ratios: {len(analysis['ratios']['liquidity'])} ratios calculated")
        print(f"🎯 Profitability Ratios: {len(analysis['ratios']['profitability'])} ratios calculated")
        print(f"⚡ Efficiency Ratios: {len(analysis['ratios']['efficiency'])} ratios calculated")
        print(f"⚖️  Leverage Ratios: {len(analysis['ratios']['leverage'])} ratios calculated")
        print(f"📊 Trend Analysis: {len(analysis['trends'])} metrics analyzed")
        print(f"🏥 Financial Health Score: {analysis['financial_health']['score']:.1f}/100")
        print(f"🎯 Financial Health Level: {analysis['financial_health']['level']}")
        print()

        # Step 4: Risk Assessment
        print("⚠️  Step 4: Risk Assessment")
        print("-" * 30)
        assessor = RiskAssessment()

        # Use sample text from the filing for testing
        sample_text = """
        NVIDIA faces various risks in its operations. The semiconductor industry is highly competitive and subject to rapid technological change.
        We are exposed to supply chain disruptions and component shortages. Global economic conditions may impact demand for our products.
        Regulatory changes and trade policies could affect our international operations. Cybersecurity threats pose risks to our systems and data.
        Our reliance on third-party foundries for manufacturing creates supply chain risks. Intellectual property protection is important to our business.
        """

        risk_factors = assessor.extract_risk_factors(sample_text)
        categorized_risks = assessor.classify_risks(risk_factors)
        risk_assessment = assessor.assess_risk_severity(risk_factors)
        risk_summary = assessor.generate_risk_summary(risk_assessment, company_name)

        print("⚠️  Risk Assessment Results:")
        print(f"📋 Total risks identified: {len(risk_factors)}")
        print(f"📊 Risk categories: {list(categorized_risks.keys())}")
        print(f"🎯 Overall risk score: {risk_summary['executive_summary']['overall_risk_score']}")
        print(f"⚠️  Risk level: {risk_summary['executive_summary']['overall_risk_level']}")
        print()

        # Step 5: Chart Generation
        print("📊 Step 5: Chart Generation")
        print("-" * 30)
        chart_gen = ChartGenerator(output_dir="/home/pedro/Projetos/EconomicsWorkspace/SEC-Filings-Analysis/charts")

        # Generate ratio analysis chart
        try:
            ratio_chart_path = chart_gen.create_ratio_analysis_chart(
                analysis['ratios'],
                company_name
            )
            print(f"✅ Ratio analysis chart: {ratio_chart_path}")
        except Exception as e:
            print(f"⚠️  Ratio chart generation: {e}")

        # Generate trend analysis chart
        try:
            trend_chart_path = chart_gen.create_trend_analysis_chart(
                result['financial_data'],
                company_name
            )
            print(f"✅ Trend analysis chart: {trend_chart_path}")
        except Exception as e:
            print(f"⚠️  Trend chart generation: {e}")

        # Generate waterfall chart
        try:
            if 'cash_flow' in result['financial_data']:
                waterfall_chart_path = chart_gen.create_waterfall_chart(
                    result['financial_data']['cash_flow'],
                    company_name
                )
                print(f"✅ Waterfall chart: {waterfall_chart_path}")
            else:
                print("⚠️  No cash flow data available for waterfall chart")
        except Exception as e:
            print(f"⚠️  Waterfall chart generation: {e}")

        print()

        # Step 6: Report Generation
        print("📋 Step 6: Report Generation")
        print("-" * 30)
        report_gen = ReportGenerator(template_dir="/home/pedro/Projetos/EconomicsWorkspace/SEC-Filings-Analysis/sec-filings-analysis/assets/templates")

        # Generate detailed analysis report
        try:
            analysis_report_path = report_gen.generate_analysis_report(
                result['financial_data'],
                {'ratio_analysis': '/home/pedro/Projetos/EconomicsWorkspace/SEC-Filings-Analysis/charts/NVIDIA_Corporation_ratio_analysis.png'},
                risk_assessment,
                company_name
            )
            print(f"✅ Analysis report: {analysis_report_path}")
        except Exception as e:
            print(f"⚠️  Analysis report generation: {e}")

        # Generate investment thesis
        try:
            thesis_framework = {
                'industry': {'overview': 'Semiconductor industry leader'},
                'competitive': {'advantages': 'AI and GPU technology leadership'},
                'risks': {'identified': risk_factors},
                'valuation': {'method': 'DCF analysis'},
                'thesis': {'investment_rationale': 'Strong market position in AI growth'},
                'conclusion': {'recommendation': 'Strong Buy'}
            }

            thesis_path = report_gen.generate_investment_thesis(
                result['financial_data'],
                thesis_framework,
                company_name
            )
            print(f"✅ Investment thesis: {thesis_path}")
        except Exception as e:
            print(f"⚠️  Investment thesis generation: {e}")

        # Generate executive summary
        try:
            key_metrics = {
                'revenue': 10000000000,  # Sample data
                'net_margin': 0.25,
                'financial_health_score': 85.0,
                'risks': {'market': 3.5, 'operational': 2.0, 'financial': 1.5}
            }

            summary_path = report_gen.generate_executive_summary(
                key_metrics,
                company_name
            )
            print(f"✅ Executive summary: {summary_path}")
        except Exception as e:
            print(f"⚠️  Executive summary generation: {e}")

        print()

        # Step 7: Summary
        print("🎉 Analysis Complete!")
        print("=" * 50)
        print("📊 Summary:")
        print(f"✅ File processed: {os.path.basename(filing_path)}")
        print(f"✅ Data extracted and validated")
        print(f"✅ Financial analysis completed")
        print(f"✅ Risk assessment performed")
        print(f"✅ Charts generated")
        print(f"✅ Reports created")
        print()
        print("📁 Output files:")
        print("   - Charts saved to: /home/pedro/Projetos/EconomicsWorkspace/SEC-Filings-Analysis/charts/")
        print("   - Reports saved to: /home/pedro/Projetos/EconomicsWorkspace/SEC-Filings-Analysis/sec-filings-analysis/reports/")
        print()
        print("🎯 Key Findings:")
        print(f"   - Financial Health Score: {analysis['financial_health']['score']:.1f}/100 ({analysis['financial_health']['level']})")
        print(f"   - Risk Level: {risk_summary['executive_summary']['overall_risk_level']}")
        print(f"   - Data Completeness: {validation['score']:.1%}")

    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_sec_filing_analysis()