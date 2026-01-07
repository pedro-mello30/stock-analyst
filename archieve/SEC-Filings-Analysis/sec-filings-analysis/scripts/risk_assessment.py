#!/usr/bin/env python3
"""
Risk Assessment for SEC Filings Analysis

Analyzes qualitative risk factors from management discussion and provides
risk scoring and categorization for investment analysis.
"""

import re
import logging
from typing import Dict, List, Any, Optional, Tuple, Union
from collections import defaultdict
import numpy as np
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RiskAssessment:
    """Main class for qualitative risk factor analysis."""

    def __init__(self):
        self.risk_factors = []
        self.risk_categories = {}
        self.risk_scores = {}
        self.risk_summary = {}

        # Risk keyword patterns for different categories
        self.risk_patterns = {
            'market_risks': [
                r'(?i)economic.*conditions?',
                r'(?i)market.*demand',
                r'(?i)competition',
                r'(?i)customer.*concentration',
                r'(?i)pricing.*pressure',
                r'(?i)supply.*chain',
                r'(?i)commodity.*price',
                r'(?i)foreign.*exchange',
                r'(?i)interest.*rate'
            ],
            'operational_risks': [
                r'(?i)operational.*efficiency',
                r'(?i)technology.*disruption',
                r'(?i)cyber.*security',
                r'(?i)data.*breach',
                r'(?i)system.*failure',
                r'(?i)vendor.*reliance',
                r'(?i)intellectual.*property',
                r'(?i)talent.*acquisition',
                r'(?i)workforce.*issues'
            ],
            'financial_risks': [
                r'(?i)liquidity.*risk',
                r'(?i)credit.*risk',
                r'(?i)debt.*obligation',
                r'(?i)capital.*requirement',
                r'(?i)financial.*covenant',
                r'(?i)rating.*agency',
                r'(?i)cost.*structure',
                r'(?i)cash.*flow.*risk'
            ],
            'regulatory_risks': [
                r'(?i)regulatory.*change',
                r'(?i)legal.*proceeding',
                r'(?i)compliance.*cost',
                r'(?i)environmental.*regulation',
                r'(?i)tax.*policy',
                r'(?i)trade.*policy',
                r'(?i)antitrust',
                r'(?i)data.*privacy'
            ]
        }

        # Risk severity scoring patterns
        self.severity_indicators = {
            'high': [
                r'(?i)(materially|significantly|substantially).*adverse',
                r'(?i)could.*result.*in.*significant',
                r'(?i)may.*have.*material.*impact',
                r'(?i)substantial.*risk',
                r'(?i)critical.*dependence'
            ],
            'medium': [
                r'(?i)could.*negatively.*affect',
                r'(?i)may.*impact',
                r'(?i)potential.*risk',
                r'(?i)challenges.*faced',
                r'(?i)uncertainties.*exist'
            ],
            'low': [
                r'(?i)minor.*impact',
                r'(?i)routine.*matter',
                r'(?i)standard.*practice',
                r'(?i)expected.*fluctuation'
            ]
        }

    def extract_risk_factors(self, filing_text: str) -> List[Dict[str, Any]]:
        """
        Extract risk factors from SEC filing text.

        Args:
            filing_text: Full text of SEC filing

        Returns:
            List of extracted risk factors with metadata
        """
        risk_factors = []

        # Find risk factor sections
        risk_section_patterns = [
            r'(?i)risk.*factors?.*?(?=item\s*\d+\.|management.*discussion|quantitative.*market|forward.*looking)',
            r'(?i)risk.*disclosure.*?(?=item\s*\d+\.|management.*discussion|quantitative.*market|forward.*looking)',
            r'(?i)management.*discussion.*analysis.*?(?=item\s*\d+\.|quantitative.*market|forward.*looking)'
        ]

        for pattern in risk_section_patterns:
            matches = re.findall(pattern, filing_text, re.DOTALL | re.IGNORECASE)
            for match in matches:
                factors = self._parse_risk_section(match)
                risk_factors.extend(factors)

        # If no specific sections found, search for risk mentions throughout document
        if not risk_factors:
            risk_factors = self._search_general_risks(filing_text)

        self.risk_factors = risk_factors
        return risk_factors

    def classify_risks(self, risk_factors: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Classify risks into categories.

        Args:
            risk_factors: List of risk factors

        Returns:
            Dictionary of categorized risks
        """
        categorized_risks = defaultdict(list)

        for risk in risk_factors:
            text = risk.get('text', '')
            category = self._classify_risk_category(text)
            risk['category'] = category
            risk['category_confidence'] = self._calculate_category_confidence(text, category)

            categorized_risks[category].append(risk)

        self.risk_categories = dict(categorized_risks)
        return self.risk_categories

    def assess_risk_severity(self, risk_factors: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Assess risk severity and impact.

        Args:
            risk_factors: List of risk factors

        Returns:
            Risk assessment summary with scoring
        """
        risk_assessment = {}

        for risk in risk_factors:
            text = risk.get('text', '')
            severity = self._assess_risk_severity_level(text)
            impact_score = self._calculate_impact_score(text, severity)
            likelihood = self._assess_likelihood(text)

            risk['severity'] = severity
            risk['impact_score'] = impact_score
            risk['likelihood'] = likelihood
            risk['overall_risk_score'] = impact_score * likelihood

        # Calculate category-level risk scores
        category_scores = self._calculate_category_scores(risk_factors)

        # Calculate overall risk profile
        overall_risk_score = np.mean([r.get('overall_risk_score', 0) for r in risk_factors])

        risk_assessment = {
            'individual_risks': risk_factors,
            'category_scores': category_scores,
            'overall_risk_score': overall_risk_score,
            'risk_distribution': self._calculate_risk_distribution(risk_factors),
            'top_risks': self._identify_top_risks(risk_factors)
        }

        self.risk_scores = risk_assessment
        return risk_assessment

    def generate_risk_summary(self, risk_assessment: Dict[str, Any],
                            company_name: str = "Company") -> Dict[str, Any]:
        """
        Generate comprehensive risk summary.

        Args:
            risk_assessment: Complete risk assessment results
            company_name: Company name for summary

        Returns:
            Risk summary report
        """
        summary = {
            'executive_summary': self._create_executive_summary(risk_assessment, company_name),
            'risk_categories': self._create_category_summaries(risk_assessment),
            'mitigation_strategies': self._suggest_mitigation_strategies(risk_assessment),
            'risk_trends': self._analyze_risk_trends(risk_assessment),
            'recommendations': self._generate_recommendations(risk_assessment)
        }

        self.risk_summary = summary
        return summary

    def _parse_risk_section(self, section_text: str) -> List[Dict[str, Any]]:
        """Parse risk factors from a specific section."""
        risk_factors = []

        # Split section into individual risk items
        risk_items = re.split(r'\n\s*\d+\.\s+|\n\s*[A-Z][A-Z\s]+\s*\n', section_text)

        for item in risk_items:
            if len(item.strip()) > 50:  # Filter out very short items
                risk_factors.append({
                    'text': self._clean_risk_text(item),
                    'source_section': 'risk_factors',
                    'extraction_confidence': 0.8
                })

        return risk_factors

    def _search_general_risks(self, text: str) -> List[Dict[str, Any]]:
        """Search for risk mentions throughout the document."""
        risk_factors = []

        # Look for sentences containing risk-related keywords
        risk_keywords = [
            'risk', 'adverse', 'uncertainty', 'challenge', 'threat', 'exposure',
            'vulnerability', 'liability', 'obligation', 'commitment'
        ]

        sentences = re.split(r'[.!?]+', text)
        for sentence in sentences:
            sentence = sentence.strip()
            if any(keyword in sentence.lower() for keyword in risk_keywords):
                risk_factors.append({
                    'text': sentence,
                    'source_section': 'general_text',
                    'extraction_confidence': 0.3
                })

        return risk_factors

    def _classify_risk_category(self, text: str) -> str:
        """Classify risk into category based on keyword matching."""
        text_lower = text.lower()
        category_scores = {}

        for category, patterns in self.risk_patterns.items():
            score = 0
            for pattern in patterns:
                matches = re.findall(pattern, text_lower)
                score += len(matches) * 0.5  # Weight each match
            category_scores[category] = score

        # Return category with highest score
        if category_scores:
            return max(category_scores, key=category_scores.get)
        else:
            return 'general'

    def _calculate_category_confidence(self, text: str, category: str) -> float:
        """Calculate confidence score for category classification."""
        text_lower = text.lower()
        patterns = self.risk_patterns.get(category, [])
        total_matches = 0

        for pattern in patterns:
            matches = re.findall(pattern, text_lower)
            total_matches += len(matches)

        # Normalize confidence (0.0 to 1.0)
        confidence = min(total_matches * 0.2, 1.0)
        return confidence

    def _assess_risk_severity_level(self, text: str) -> str:
        """Assess severity level of a risk factor."""
        text_lower = text.lower()

        for severity, patterns in self.severity_indicators.items():
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    return severity

        return 'medium'  # Default severity

    def _calculate_impact_score(self, text: str, severity: str) -> float:
        """Calculate numerical impact score for a risk."""
        severity_weights = {'low': 1.0, 'medium': 3.0, 'high': 5.0}
        base_score = severity_weights.get(severity, 3.0)

        # Adjust based on specific keywords
        text_lower = text.lower()
        if any(word in text_lower for word in ['material', 'significant', 'substantial']):
            base_score *= 1.5
        elif any(word in text_lower for word in ['minor', 'routine', 'standard']):
            base_score *= 0.7

        return min(base_score, 5.0)  # Cap at 5.0

    def _assess_likelihood(self, text: str) -> float:
        """Assess likelihood of risk occurrence."""
        text_lower = text.lower()

        # Likelihood indicators
        high_likelihood = ['will', 'expected', 'likely', 'probable']
        medium_likelihood = ['may', 'could', 'possible', 'potential']
        low_likelihood = ['unlikely', 'remote', 'minimal']

        likelihood_score = 0.5  # Default medium likelihood

        if any(word in text_lower for word in high_likelihood):
            likelihood_score = 0.8
        elif any(word in text_lower for word in medium_likelihood):
            likelihood_score = 0.5
        elif any(word in text_lower for word in low_likelihood):
            likelihood_score = 0.2

        return likelihood_score

    def _calculate_category_scores(self, risk_factors: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calculate average risk scores by category."""
        category_scores = defaultdict(list)

        for risk in risk_factors:
            category = risk.get('category', 'general')
            score = risk.get('overall_risk_score', 0)
            category_scores[category].append(score)

        # Calculate weighted averages
        weighted_scores = {}
        for category, scores in category_scores.items():
            weighted_scores[category] = {
                'average_score': np.mean(scores),
                'max_score': max(scores),
                'risk_count': len(scores),
                'severity_distribution': self._get_severity_distribution([r for r in risk_factors if r.get('category') == category])
            }

        return weighted_scores

    def _calculate_risk_distribution(self, risk_factors: List[Dict[str, Any]]) -> Dict[str, int]:
        """Calculate distribution of risks by severity."""
        distribution = defaultdict(int)

        for risk in risk_factors:
            severity = risk.get('severity', 'medium')
            distribution[severity] += 1

        return dict(distribution)

    def _identify_top_risks(self, risk_factors: List[Dict[str, Any]], top_n: int = 5) -> List[Dict[str, Any]]:
        """Identify top N highest risk factors."""
        sorted_risks = sorted(risk_factors, key=lambda x: x.get('overall_risk_score', 0), reverse=True)
        return sorted_risks[:top_n]

    def _create_executive_summary(self, risk_assessment: Dict[str, Any], company_name: str) -> Dict[str, Any]:
        """Create executive summary of risk assessment."""
        overall_score = risk_assessment.get('overall_risk_score', 0)
        category_scores = risk_assessment.get('category_scores', {})
        top_risks = risk_assessment.get('top_risks', [])

        # Risk level classification
        if overall_score >= 4.0:
            risk_level = 'High'
        elif overall_score >= 2.5:
            risk_level = 'Medium'
        else:
            risk_level = 'Low'

        summary = {
            'company': company_name,
            'assessment_date': datetime.now().strftime('%Y-%m-%d'),
            'overall_risk_level': risk_level,
            'overall_risk_score': round(overall_score, 2),
            'total_risks_identified': len(risk_assessment.get('individual_risks', [])),
            'highest_risk_categories': self._get_highest_risk_categories(category_scores),
            'key_risks': [r.get('text', '')[:100] + '...' for r in top_risks[:3]],
            'risk_mitigation_status': self._assess_mitigation_status(risk_assessment)
        }

        return summary

    def _create_category_summaries(self, risk_assessment: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """Create detailed summaries for each risk category."""
        category_scores = risk_assessment.get('category_scores', {})
        summaries = {}

        for category, scores in category_scores.items():
            summaries[category] = {
                'risk_count': scores.get('risk_count', 0),
                'average_score': round(scores.get('average_score', 0), 2),
                'max_score': round(scores.get('max_score', 0), 2),
                'severity_breakdown': scores.get('severity_distribution', {}),
                'description': self._get_category_description(category),
                'monitoring_priority': self._calculate_monitoring_priority(scores)
            }

        return summaries

    def _suggest_mitigation_strategies(self, risk_assessment: Dict[str, Any]) -> Dict[str, List[str]]:
        """Suggest mitigation strategies based on risk assessment."""
        category_scores = risk_assessment.get('category_scores', {})
        strategies = {}

        for category, scores in category_scores.items():
            avg_score = scores.get('average_score', 0)
            strategies[category] = self._get_mitigation_strategies_for_category(category, avg_score)

        return strategies

    def _analyze_risk_trends(self, risk_assessment: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze trends in risk factors (placeholder for historical analysis)."""
        # This would typically compare with previous filings
        # For now, return basic analysis
        return {
            'trend_direction': 'stable',  # Would be calculated from historical data
            'new_risks_identified': 0,    # Would compare with previous period
            'risks_resolved': 0,          # Would track resolved risks
            'risk_evolution': 'No significant changes detected'
        }

    def _generate_recommendations(self, risk_assessment: Dict[str, Any]) -> List[str]:
        """Generate actionable recommendations based on risk assessment."""
        recommendations = []
        overall_score = risk_assessment.get('overall_risk_score', 0)
        category_scores = risk_assessment.get('category_scores', {})

        # Overall recommendations based on risk level
        if overall_score >= 4.0:
            recommendations.append("HIGH RISK: Consider reducing exposure or implementing additional risk mitigation measures")
            recommendations.append("Review risk management policies and procedures")
        elif overall_score >= 2.5:
            recommendations.append("MEDIUM RISK: Monitor risk factors closely and review mitigation strategies")
        else:
            recommendations.append("LOW RISK: Maintain current monitoring practices")

        # Category-specific recommendations
        for category, scores in category_scores.items():
            if scores.get('average_score', 0) > 3.0:
                recommendations.append(f"Focus on {category.replace('_', ' ')} risk management")

        return recommendations

    def _clean_risk_text(self, text: str) -> str:
        """Clean and normalize risk factor text."""
        # Remove extra whitespace and normalize
        text = re.sub(r'\s+', ' ', text.strip())
        # Remove leading/trailing punctuation
        text = re.sub(r'^[^\w\s]+|[^\w\s]+$', '', text)
        return text

    def _get_severity_distribution(self, risks: List[Dict[str, Any]]) -> Dict[str, int]:
        """Get distribution of severities for a list of risks."""
        distribution = defaultdict(int)
        for risk in risks:
            severity = risk.get('severity', 'medium')
            distribution[severity] += 1
        return dict(distribution)

    def _get_highest_risk_categories(self, category_scores: Dict[str, Dict[str, Any]]) -> List[str]:
        """Get list of highest risk categories."""
        sorted_categories = sorted(category_scores.items(),
                                 key=lambda x: x[1].get('average_score', 0),
                                 reverse=True)
        return [cat for cat, _ in sorted_categories[:3]]

    def _assess_mitigation_status(self, risk_assessment: Dict[str, Any]) -> str:
        """Assess the current mitigation status."""
        # This would typically analyze mitigation measures mentioned in the filing
        return "Mitigation measures under review"

    def _get_category_description(self, category: str) -> str:
        """Get description for risk category."""
        descriptions = {
            'market_risks': 'Risks related to economic conditions, market demand, competition, and external factors',
            'operational_risks': 'Risks related to business operations, technology, and organizational capabilities',
            'financial_risks': 'Risks related to financial performance, liquidity, and capital structure',
            'regulatory_risks': 'Risks related to legal, regulatory, and compliance matters',
            'general': 'General business risks not fitting specific categories'
        }
        return descriptions.get(category, 'Risk category description not available')

    def _calculate_monitoring_priority(self, scores: Dict[str, Any]) -> str:
        """Calculate monitoring priority for a risk category."""
        avg_score = scores.get('average_score', 0)
        risk_count = scores.get('risk_count', 0)

        if avg_score >= 4.0 or risk_count >= 5:
            return 'High'
        elif avg_score >= 2.5 or risk_count >= 3:
            return 'Medium'
        else:
            return 'Low'

    def _get_mitigation_strategies_for_category(self, category: str, avg_score: float) -> List[str]:
        """Get mitigation strategies for a specific category."""
        base_strategies = {
            'market_risks': [
                'Diversify customer base and geographic exposure',
                'Implement hedging strategies for currency and commodity risks',
                'Monitor competitive landscape and market trends'
            ],
            'operational_risks': [
                'Invest in cybersecurity infrastructure',
                'Develop business continuity plans',
                'Strengthen vendor management processes'
            ],
            'financial_risks': [
                'Maintain adequate liquidity reserves',
                'Monitor debt covenants and credit ratings',
                'Implement robust financial controls'
            ],
            'regulatory_risks': [
                'Establish compliance monitoring systems',
                'Maintain relationships with regulatory bodies',
                'Implement regular legal reviews'
            ]
        }

        strategies = base_strategies.get(category, ['Review general risk management practices'])

        # Add specific recommendations based on risk level
        if avg_score >= 4.0:
            strategies.insert(0, "IMMEDIATE ACTION REQUIRED: Implement additional controls")

        return strategies


def main():
    """Example usage of RiskAssessment."""
    assessor = RiskAssessment()

    # Sample risk text from a filing
    sample_text = """
    The Company faces various risks in its operations. The global economic conditions remain uncertain and could negatively impact our business.
    We are exposed to foreign exchange rate fluctuations which may adversely affect our financial results. Competition in our industry is intense
    and pricing pressures could materially affect our profitability. Cybersecurity threats are increasing and a data breach could have significant
    consequences. We rely on key suppliers and any disruption in our supply chain could impact our operations. Changes in regulatory requirements
    may result in additional compliance costs. Our debt levels are significant and could limit our financial flexibility.
    """

    # Analyze risks
    risk_factors = assessor.extract_risk_factors(sample_text)
    categorized_risks = assessor.classify_risks(risk_factors)
    risk_assessment = assessor.assess_risk_severity(risk_factors)
    risk_summary = assessor.generate_risk_summary(risk_assessment, "Sample Company")

    print("Risk Assessment Results:")
    print(f"Total risks identified: {len(risk_factors)}")
    print(f"Overall risk score: {risk_summary['executive_summary']['overall_risk_score']}")
    print(f"Risk categories: {list(categorized_risks.keys())}")


if __name__ == "__main__":
    main()