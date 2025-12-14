#!/usr/bin/env python3
"""
Technical Debt Scorer - Aggregate analysis findings to calculate comprehensive debt scores

This tool consolidates findings from all legacy codebase analysis tools (inventory,
security, performance, quality, architecture) to compute an overall technical debt
score with business impact translation, effort estimation, and prioritized recommendations.

Usage:
    python technical_debt_scorer.py --input analysis_results/
    python technical_debt_scorer.py -i consolidated.json --output json
    python technical_debt_scorer.py -i results/ -o csv -f debt_report.csv --team-size 8
    python technical_debt_scorer.py -i results/ --business-context cost_params.json -v

Features:
    - Aggregates findings from all analysis tools
    - Calculates weighted debt scores by category
    - Estimates remediation effort in hours and sprints
    - Prioritizes debt items by business impact
    - Identifies quick wins (high impact, low effort)
    - Translates technical debt to business risk
    - Generates actionable recommendations

Author: claude-skills
Version: 1.0.0
Last Updated: 2025-12-13
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime
from io import StringIO
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import argparse
import csv
import json
import logging
import math
import sys


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class DebtItem:
    """Individual technical debt item"""
    category: str
    severity: str
    title: str
    description: str
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    impact_score: float = 0.0
    effort_hours: float = 0.0
    remediation_cost: float = 0.0
    business_risk: str = "medium"
    recommendation: str = ""

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class CategoryScore:
    """Debt score for a specific category"""
    category: str
    raw_score: float
    weighted_score: float
    weight: float
    issue_count: int
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int
    debt_level: str

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class EffortEstimate:
    """Remediation effort estimation"""
    total_hours: float
    total_sprints: float
    by_severity: Dict[str, float] = field(default_factory=dict)
    by_category: Dict[str, float] = field(default_factory=dict)
    team_size: int = 5
    sprint_capacity_hours: float = 160.0  # 2 weeks * 5 days * 8 hours * 2 (50% capacity)

    def to_dict(self) -> Dict:
        return asdict(self)


class TechnicalDebtScorer:
    """Main scorer class for technical debt analysis"""

    # Category weights (must sum to 1.0)
    CATEGORY_WEIGHTS = {
        'security': 0.25,
        'code_quality': 0.25,
        'architecture': 0.20,
        'performance': 0.20,
        'documentation': 0.10
    }

    # Severity multipliers for impact scoring
    SEVERITY_MULTIPLIERS = {
        'critical': 4.0,
        'high': 3.0,
        'medium': 2.0,
        'low': 1.0
    }

    # Effort estimation (hours per issue by severity)
    EFFORT_ESTIMATES = {
        'critical': 40.0,  # 1 week
        'high': 20.0,      # 0.5 week
        'medium': 8.0,     # 1 day
        'low': 2.0         # 0.25 day
    }

    # Business context defaults
    DEFAULT_BUSINESS_CONTEXT = {
        'developer_hourly_rate': 100.0,
        'outage_cost_per_hour': 10000.0,
        'security_breach_cost': 500000.0,
        'customer_churn_rate': 0.05,
        'revenue_per_customer': 1000.0
    }

    def __init__(self, team_size: int = 5, business_context: Optional[Dict] = None, verbose: bool = False):
        self.team_size = team_size
        self.business_context = business_context or self.DEFAULT_BUSINESS_CONTEXT
        self.verbose = verbose
        if verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("TechnicalDebtScorer initialized")
        self.debt_items: List[DebtItem] = []
        self.category_scores: Dict[str, CategoryScore] = {}

    def load_analysis_results(self, input_path: Path) -> Dict:
        """Load analysis results from directory or single file"""
        if self.verbose:
            print(f"Loading analysis results from: {input_path}")

        results = {
            'inventory': {},
            'security': {},
            'performance': {},
            'quality': {},
            'architecture': {}
        }

        if input_path.is_file():
            # Single consolidated JSON file
            with open(input_path, 'r') as f:
                data = json.load(f)
                # Try to extract individual analysis results
                if 'inventory' in data:
                    results = data
                else:
                    # Assume it's a consolidated format - parse structure
                    results = self._parse_consolidated_format(data)
        else:
            # Directory with multiple JSON files
            file_mapping = {
                'inventory.json': 'inventory',
                'security.json': 'security',
                'performance.json': 'performance',
                'quality.json': 'quality',
                'architecture.json': 'architecture'
            }

            for filename, key in file_mapping.items():
                file_path = input_path / filename
                if file_path.exists():
                    with open(file_path, 'r') as f:
                        results[key] = json.load(f)
                    if self.verbose:
                        print(f"  Loaded {filename}")
                else:
                    if self.verbose:
                        print(f"  Warning: {filename} not found, skipping")

        return results

    def _parse_consolidated_format(self, data: Dict) -> Dict:
        """Parse consolidated JSON format into individual analysis results"""
        # Try to intelligently parse the structure
        results = {
            'inventory': {},
            'security': {},
            'performance': {},
            'quality': {},
            'architecture': {}
        }

        # Map common keys to categories
        if 'vulnerabilities' in data or 'security_issues' in data:
            results['security'] = data
        if 'bottlenecks' in data or 'performance_issues' in data:
            results['performance'] = data
        if 'code_issues' in data or 'quality_metrics' in data:
            results['quality'] = data
        if 'architectural_issues' in data or 'design_patterns' in data:
            results['architecture'] = data
        if 'files' in data or 'technologies' in data:
            results['inventory'] = data

        return results

    def extract_debt_items(self, analysis_results: Dict) -> List[DebtItem]:
        """Extract debt items from all analysis results"""
        if self.verbose:
            print("\nExtracting debt items from analysis results...")

        debt_items = []

        # Extract security issues
        security_data = analysis_results.get('security', {})
        if 'vulnerabilities' in security_data:
            for vuln in security_data['vulnerabilities']:
                debt_items.append(DebtItem(
                    category='security',
                    severity=vuln.get('severity', 'medium'),
                    title=vuln.get('title', vuln.get('type', 'Security Issue')),
                    description=vuln.get('description', ''),
                    file_path=vuln.get('file_path'),
                    line_number=vuln.get('line_number'),
                    recommendation=vuln.get('remediation', '')
                ))

        # Extract performance issues
        performance_data = analysis_results.get('performance', {})
        if 'bottlenecks' in performance_data:
            for bottleneck in performance_data['bottlenecks']:
                debt_items.append(DebtItem(
                    category='performance',
                    severity=bottleneck.get('severity', 'medium'),
                    title=bottleneck.get('title', bottleneck.get('type', 'Performance Issue')),
                    description=bottleneck.get('description', ''),
                    file_path=bottleneck.get('file_path'),
                    line_number=bottleneck.get('line_number'),
                    recommendation=bottleneck.get('optimization', '')
                ))

        # Extract code quality issues
        quality_data = analysis_results.get('quality', {})
        if 'issues' in quality_data:
            for issue in quality_data['issues']:
                debt_items.append(DebtItem(
                    category='code_quality',
                    severity=issue.get('severity', 'medium'),
                    title=issue.get('title', issue.get('type', 'Quality Issue')),
                    description=issue.get('description', ''),
                    file_path=issue.get('file_path'),
                    line_number=issue.get('line_number'),
                    recommendation=issue.get('fix', '')
                ))

        # Extract architectural issues
        architecture_data = analysis_results.get('architecture', {})
        if 'issues' in architecture_data:
            for issue in architecture_data['issues']:
                debt_items.append(DebtItem(
                    category='architecture',
                    severity=issue.get('severity', 'medium'),
                    title=issue.get('title', issue.get('type', 'Architecture Issue')),
                    description=issue.get('description', ''),
                    recommendation=issue.get('recommendation', '')
                ))

        # Extract documentation issues from inventory
        inventory_data = analysis_results.get('inventory', {})
        if 'documentation_gaps' in inventory_data:
            for gap in inventory_data['documentation_gaps']:
                debt_items.append(DebtItem(
                    category='documentation',
                    severity='low',
                    title=gap.get('title', 'Missing Documentation'),
                    description=gap.get('description', ''),
                    file_path=gap.get('file_path'),
                    recommendation='Add comprehensive documentation'
                ))

        if self.verbose:
            print(f"  Extracted {len(debt_items)} debt items")

        return debt_items

    def calculate_impact_scores(self, debt_items: List[DebtItem]) -> None:
        """Calculate impact scores for each debt item"""
        if self.verbose:
            print("\nCalculating impact scores...")

        for item in debt_items:
            # Base score from severity
            base_score = self.SEVERITY_MULTIPLIERS[item.severity]

            # Category multiplier (security and architecture have higher impact)
            category_multiplier = {
                'security': 1.5,
                'architecture': 1.3,
                'performance': 1.2,
                'code_quality': 1.0,
                'documentation': 0.8
            }.get(item.category, 1.0)

            # Calculate final impact score (0-100 scale)
            item.impact_score = (base_score * category_multiplier * 10.0)

            # Estimate effort
            item.effort_hours = self.EFFORT_ESTIMATES[item.severity]

            # Calculate remediation cost
            item.remediation_cost = item.effort_hours * self.business_context['developer_hourly_rate']

            # Assess business risk
            if item.severity == 'critical':
                if item.category == 'security':
                    item.business_risk = 'catastrophic'
                else:
                    item.business_risk = 'critical'
            elif item.severity == 'high':
                item.business_risk = 'high'
            elif item.severity == 'medium':
                item.business_risk = 'medium'
            else:
                item.business_risk = 'low'

    def calculate_category_scores(self, debt_items: List[DebtItem]) -> Dict[str, CategoryScore]:
        """Calculate debt scores by category"""
        if self.verbose:
            print("\nCalculating category scores...")

        category_scores = {}

        for category, weight in self.CATEGORY_WEIGHTS.items():
            category_items = [item for item in debt_items if item.category == category]

            # Count by severity
            critical_count = sum(1 for item in category_items if item.severity == 'critical')
            high_count = sum(1 for item in category_items if item.severity == 'high')
            medium_count = sum(1 for item in category_items if item.severity == 'medium')
            low_count = sum(1 for item in category_items if item.severity == 'low')

            # Calculate weighted severity score
            total_severity_points = (
                critical_count * self.SEVERITY_MULTIPLIERS['critical'] +
                high_count * self.SEVERITY_MULTIPLIERS['high'] +
                medium_count * self.SEVERITY_MULTIPLIERS['medium'] +
                low_count * self.SEVERITY_MULTIPLIERS['low']
            )

            # Normalize to 0-100 scale (100 = no debt)
            # Assume baseline: 0 issues = 100, 10+ critical issues = 0
            max_severity_points = 40  # Roughly 10 critical issues
            raw_score = max(0, 100 - (total_severity_points / max_severity_points * 100))

            # Apply weight
            weighted_score = raw_score * weight

            # Determine debt level
            if raw_score >= 80:
                debt_level = 'Low'
            elif raw_score >= 60:
                debt_level = 'Medium'
            elif raw_score >= 40:
                debt_level = 'High'
            else:
                debt_level = 'Critical'

            category_scores[category] = CategoryScore(
                category=category,
                raw_score=raw_score,
                weighted_score=weighted_score,
                weight=weight,
                issue_count=len(category_items),
                critical_count=critical_count,
                high_count=high_count,
                medium_count=medium_count,
                low_count=low_count,
                debt_level=debt_level
            )

            if self.verbose:
                print(f"  {category}: {raw_score:.1f}/100 ({debt_level})")

        return category_scores

    def calculate_overall_debt_score(self, category_scores: Dict[str, CategoryScore]) -> Tuple[float, str]:
        """Calculate overall debt score from category scores"""
        # Sum weighted scores
        total_weighted_score = sum(score.weighted_score for score in category_scores.values())

        # Overall score is weighted sum (0-100, where 100 = no debt)
        overall_score = total_weighted_score

        # Determine overall debt level
        if overall_score >= 80:
            debt_level = 'Low'
        elif overall_score >= 60:
            debt_level = 'Medium'
        elif overall_score >= 40:
            debt_level = 'High'
        else:
            debt_level = 'Critical'

        return overall_score, debt_level

    def estimate_remediation_effort(self, debt_items: List[DebtItem]) -> EffortEstimate:
        """Estimate total remediation effort"""
        if self.verbose:
            print("\nEstimating remediation effort...")

        # Calculate by severity
        by_severity = {
            'critical': sum(item.effort_hours for item in debt_items if item.severity == 'critical'),
            'high': sum(item.effort_hours for item in debt_items if item.severity == 'high'),
            'medium': sum(item.effort_hours for item in debt_items if item.severity == 'medium'),
            'low': sum(item.effort_hours for item in debt_items if item.severity == 'low')
        }

        # Calculate by category
        by_category = {}
        for category in self.CATEGORY_WEIGHTS.keys():
            by_category[category] = sum(
                item.effort_hours for item in debt_items if item.category == category
            )

        total_hours = sum(by_severity.values())

        # Calculate sprints (assuming team works at 50% capacity on debt)
        sprint_capacity = self.team_size * 80  # 2 weeks * 5 days * 8 hours * 50%
        total_sprints = math.ceil(total_hours / sprint_capacity)

        estimate = EffortEstimate(
            total_hours=total_hours,
            total_sprints=total_sprints,
            by_severity=by_severity,
            by_category=by_category,
            team_size=self.team_size,
            sprint_capacity_hours=sprint_capacity
        )

        if self.verbose:
            print(f"  Total effort: {total_hours:.1f} hours ({total_sprints} sprints)")

        return estimate

    def prioritize_debt_items(self, debt_items: List[DebtItem]) -> List[DebtItem]:
        """Prioritize debt items by impact score"""
        # Sort by impact score (descending), then by effort (ascending for tie-breaking)
        return sorted(debt_items, key=lambda x: (-x.impact_score, x.effort_hours))

    def identify_quick_wins(self, debt_items: List[DebtItem], min_impact: float = 30.0, max_effort: float = 8.0) -> List[DebtItem]:
        """Identify quick win items (high impact, low effort)"""
        quick_wins = [
            item for item in debt_items
            if item.impact_score >= min_impact and item.effort_hours <= max_effort
        ]
        return sorted(quick_wins, key=lambda x: -x.impact_score)

    def assess_business_risk(self, debt_items: List[DebtItem], category_scores: Dict[str, CategoryScore]) -> Dict:
        """Assess business risk from technical debt"""
        risk_assessment = {
            'overall_risk': 'medium',
            'security_risk': {
                'level': 'medium',
                'potential_cost': 0.0,
                'description': ''
            },
            'reliability_risk': {
                'level': 'medium',
                'potential_cost': 0.0,
                'description': ''
            },
            'velocity_risk': {
                'level': 'medium',
                'impact': '',
                'description': ''
            },
            'scalability_risk': {
                'level': 'medium',
                'description': ''
            }
        }

        # Security risk
        security_score = category_scores.get('security')
        if security_score:
            critical_vulns = security_score.critical_count
            if critical_vulns > 0:
                risk_assessment['security_risk']['level'] = 'critical'
                risk_assessment['security_risk']['potential_cost'] = self.business_context['security_breach_cost']
                risk_assessment['security_risk']['description'] = f"{critical_vulns} critical vulnerabilities pose significant breach risk"
            elif security_score.debt_level in ['High', 'Critical']:
                risk_assessment['security_risk']['level'] = 'high'
                risk_assessment['security_risk']['potential_cost'] = self.business_context['security_breach_cost'] * 0.5
                risk_assessment['security_risk']['description'] = "Multiple security issues increase attack surface"

        # Reliability risk (performance + architecture)
        performance_score = category_scores.get('performance')
        architecture_score = category_scores.get('architecture')

        avg_reliability_score = (
            (performance_score.raw_score if performance_score else 100) +
            (architecture_score.raw_score if architecture_score else 100)
        ) / 2

        if avg_reliability_score < 40:
            risk_assessment['reliability_risk']['level'] = 'high'
            risk_assessment['reliability_risk']['potential_cost'] = self.business_context['outage_cost_per_hour'] * 8  # 1 day outage
            risk_assessment['reliability_risk']['description'] = "Poor architecture and performance increase outage risk"
        elif avg_reliability_score < 60:
            risk_assessment['reliability_risk']['level'] = 'medium'
            risk_assessment['reliability_risk']['potential_cost'] = self.business_context['outage_cost_per_hour'] * 2
            risk_assessment['reliability_risk']['description'] = "Performance bottlenecks may cause service degradation"

        # Velocity risk (code quality)
        quality_score = category_scores.get('code_quality')
        if quality_score and quality_score.raw_score < 60:
            risk_assessment['velocity_risk']['level'] = 'high'
            risk_assessment['velocity_risk']['impact'] = '30-50% slower feature delivery'
            risk_assessment['velocity_risk']['description'] = "Poor code quality significantly slows development"

        # Scalability risk (architecture)
        if architecture_score and architecture_score.raw_score < 50:
            risk_assessment['scalability_risk']['level'] = 'high'
            risk_assessment['scalability_risk']['description'] = "Architectural limitations prevent horizontal scaling"

        # Overall risk
        risk_levels = [
            risk_assessment['security_risk']['level'],
            risk_assessment['reliability_risk']['level'],
            risk_assessment['velocity_risk']['level'],
            risk_assessment['scalability_risk']['level']
        ]

        if 'critical' in risk_levels:
            risk_assessment['overall_risk'] = 'critical'
        elif risk_levels.count('high') >= 2:
            risk_assessment['overall_risk'] = 'high'
        elif 'high' in risk_levels:
            risk_assessment['overall_risk'] = 'medium'
        else:
            risk_assessment['overall_risk'] = 'low'

        return risk_assessment

    def generate_recommendations(self, debt_items: List[DebtItem], category_scores: Dict[str, CategoryScore], quick_wins: List[DebtItem]) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []

        # Critical items first
        critical_items = [item for item in debt_items if item.severity == 'critical']
        if critical_items:
            recommendations.append(
                f"URGENT: Address {len(critical_items)} critical issues immediately "
                f"(estimated {sum(item.effort_hours for item in critical_items):.0f} hours)"
            )

        # Quick wins
        if quick_wins:
            recommendations.append(
                f"Start with {len(quick_wins)} quick wins to build momentum "
                f"(high impact, low effort: ~{sum(item.effort_hours for item in quick_wins):.0f} hours total)"
            )

        # Category-specific recommendations
        for category, score in sorted(category_scores.items(), key=lambda x: x[1].raw_score):
            if score.debt_level in ['High', 'Critical']:
                if category == 'security':
                    recommendations.append(
                        f"Security debt is {score.debt_level.lower()} - implement security scanning, "
                        f"patch vulnerabilities, and establish secure coding standards"
                    )
                elif category == 'code_quality':
                    recommendations.append(
                        f"Code quality is {score.debt_level.lower()} - refactor complex code, "
                        f"increase test coverage, and enforce linting standards"
                    )
                elif category == 'architecture':
                    recommendations.append(
                        f"Architecture debt is {score.debt_level.lower()} - decouple components, "
                        f"document design decisions, and establish architectural patterns"
                    )
                elif category == 'performance':
                    recommendations.append(
                        f"Performance debt is {score.debt_level.lower()} - optimize bottlenecks, "
                        f"implement caching, and establish performance monitoring"
                    )
                elif category == 'documentation':
                    recommendations.append(
                        f"Documentation is lacking - add API docs, architecture diagrams, "
                        f"and onboarding guides"
                    )

        # Strategic recommendation
        total_items = len(debt_items)
        if total_items > 50:
            recommendations.append(
                f"With {total_items} total debt items, allocate 20-30% of sprint capacity "
                f"to debt reduction over the next 3-6 months"
            )
        elif total_items > 20:
            recommendations.append(
                f"Allocate 15-20% of sprint capacity to address the {total_items} debt items "
                f"over the next 2-3 months"
            )

        return recommendations

    def analyze(self, input_path: Path) -> Dict:
        """Main analysis method"""
        # Load analysis results
        analysis_results = self.load_analysis_results(input_path)

        # Extract debt items
        self.debt_items = self.extract_debt_items(analysis_results)

        if not self.debt_items:
            return {
                'error': 'No debt items found in analysis results',
                'timestamp': datetime.now().isoformat()
            }

        # Calculate impact scores
        self.calculate_impact_scores(self.debt_items)

        # Calculate category scores
        self.category_scores = self.calculate_category_scores(self.debt_items)

        # Calculate overall debt score
        overall_score, debt_level = self.calculate_overall_debt_score(self.category_scores)

        # Estimate remediation effort
        effort_estimate = self.estimate_remediation_effort(self.debt_items)

        # Prioritize debt items
        prioritized_items = self.prioritize_debt_items(self.debt_items)

        # Identify quick wins
        quick_wins = self.identify_quick_wins(self.debt_items)

        # Assess business risk
        risk_assessment = self.assess_business_risk(self.debt_items, self.category_scores)

        # Generate recommendations
        recommendations = self.generate_recommendations(self.debt_items, self.category_scores, quick_wins)

        # Compile results
        results = {
            'timestamp': datetime.now().isoformat(),
            'overall_debt_score': round(overall_score, 2),
            'debt_level': debt_level,
            'total_debt_items': len(self.debt_items),
            'category_scores': {k: v.to_dict() for k, v in self.category_scores.items()},
            'effort_estimate': effort_estimate.to_dict(),
            'prioritized_items': [item.to_dict() for item in prioritized_items[:20]],  # Top 20
            'quick_wins': [item.to_dict() for item in quick_wins],
            'risk_assessment': risk_assessment,
            'recommendations': recommendations,
            'business_context': self.business_context
        }

        return results


def format_text_output(results: Dict) -> str:
    """Format results as human-readable text report"""
    output = StringIO()

    output.write("=" * 80 + "\n")
    output.write("TECHNICAL DEBT SCORE REPORT\n")
    output.write("=" * 80 + "\n\n")

    # Executive Summary
    output.write("EXECUTIVE SUMMARY\n")
    output.write("-" * 80 + "\n")
    output.write(f"Overall Debt Score: {results['overall_debt_score']:.1f}/100\n")
    output.write(f"Debt Level: {results['debt_level']}\n")
    output.write(f"Total Debt Items: {results['total_debt_items']}\n")
    output.write(f"Generated: {results['timestamp']}\n\n")

    # Effort Estimate
    effort = results['effort_estimate']
    output.write(f"Remediation Effort: {effort['total_hours']:.0f} hours ({effort['total_sprints']} sprints)\n")
    output.write(f"Team Size: {effort['team_size']} developers\n")
    output.write(f"Sprint Capacity: {effort['sprint_capacity_hours']:.0f} hours/sprint\n\n")

    # Category Scores
    output.write("CATEGORY SCORES\n")
    output.write("-" * 80 + "\n")
    for category, score in results['category_scores'].items():
        bar_length = int(score['raw_score'] / 5)
        bar = "█" * bar_length + "░" * (20 - bar_length)
        output.write(f"{category.upper():20s} {bar} {score['raw_score']:5.1f}/100 ({score['debt_level']})\n")
        output.write(f"                     Issues: {score['issue_count']} ")
        output.write(f"(Critical: {score['critical_count']}, High: {score['high_count']}, ")
        output.write(f"Medium: {score['medium_count']}, Low: {score['low_count']})\n\n")

    # Risk Assessment
    output.write("BUSINESS RISK ASSESSMENT\n")
    output.write("-" * 80 + "\n")
    risk = results['risk_assessment']
    output.write(f"Overall Risk: {risk['overall_risk'].upper()}\n\n")

    output.write(f"Security Risk: {risk['security_risk']['level'].upper()}\n")
    output.write(f"  {risk['security_risk']['description']}\n")
    if risk['security_risk']['potential_cost'] > 0:
        output.write(f"  Potential Cost: ${risk['security_risk']['potential_cost']:,.0f}\n")
    output.write("\n")

    output.write(f"Reliability Risk: {risk['reliability_risk']['level'].upper()}\n")
    output.write(f"  {risk['reliability_risk']['description']}\n")
    if risk['reliability_risk']['potential_cost'] > 0:
        output.write(f"  Potential Cost: ${risk['reliability_risk']['potential_cost']:,.0f}\n")
    output.write("\n")

    output.write(f"Velocity Risk: {risk['velocity_risk']['level'].upper()}\n")
    output.write(f"  {risk['velocity_risk']['description']}\n")
    if risk['velocity_risk'].get('impact'):
        output.write(f"  Impact: {risk['velocity_risk']['impact']}\n")
    output.write("\n")

    # Quick Wins
    if results['quick_wins']:
        output.write("QUICK WINS (High Impact, Low Effort)\n")
        output.write("-" * 80 + "\n")
        for i, item in enumerate(results['quick_wins'][:10], 1):
            output.write(f"{i}. [{item['severity'].upper()}] {item['title']}\n")
            output.write(f"   Impact: {item['impact_score']:.1f}/100 | Effort: {item['effort_hours']:.1f}h | Cost: ${item['remediation_cost']:,.0f}\n")
            if item['file_path']:
                output.write(f"   File: {item['file_path']}")
                if item['line_number']:
                    output.write(f":{item['line_number']}")
                output.write("\n")
            output.write("\n")

    # Top Priority Items
    output.write("TOP PRIORITY ITEMS\n")
    output.write("-" * 80 + "\n")
    for i, item in enumerate(results['prioritized_items'][:10], 1):
        output.write(f"{i}. [{item['severity'].upper()}] {item['title']}\n")
        output.write(f"   Category: {item['category']} | Impact: {item['impact_score']:.1f}/100 | ")
        output.write(f"Effort: {item['effort_hours']:.1f}h\n")
        output.write(f"   Business Risk: {item['business_risk'].upper()}\n")
        if item['description']:
            output.write(f"   {item['description'][:100]}\n")
        output.write("\n")

    # Recommendations
    output.write("RECOMMENDATIONS\n")
    output.write("-" * 80 + "\n")
    for i, rec in enumerate(results['recommendations'], 1):
        output.write(f"{i}. {rec}\n\n")

    output.write("=" * 80 + "\n")

    return output.getvalue()


def format_csv_output(results: Dict) -> str:
    """Format debt items as CSV"""
    output = StringIO()
    writer = csv.writer(output)

    # Header
    writer.writerow([
        'Category', 'Severity', 'Title', 'Description', 'File Path', 'Line Number',
        'Impact Score', 'Effort (hours)', 'Cost ($)', 'Business Risk', 'Recommendation'
    ])

    # Write all items
    for item in results['prioritized_items']:
        writer.writerow([
            item['category'],
            item['severity'],
            item['title'],
            item['description'],
            item['file_path'] or '',
            item['line_number'] or '',
            f"{item['impact_score']:.2f}",
            f"{item['effort_hours']:.2f}",
            f"{item['remediation_cost']:.2f}",
            item['business_risk'],
            item['recommendation']
        ])

    return output.getvalue()


def main():
    parser = argparse.ArgumentParser(
        description='Calculate comprehensive technical debt scores from analysis results',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze results from directory
  python technical_debt_scorer.py --input analysis_results/

  # Analyze consolidated JSON file
  python technical_debt_scorer.py -i consolidated_results.json

  # Generate JSON output
  python technical_debt_scorer.py -i results/ -o json -f debt_score.json

  # Generate CSV with custom team size
  python technical_debt_scorer.py -i results/ -o csv --team-size 8

  # Verbose mode with business context
  python technical_debt_scorer.py -i results/ --business-context costs.json -v
        """
    )

    parser.add_argument('--input', '-i', required=True,
                       help='Input directory with JSON files or single consolidated JSON file')
    parser.add_argument('--output', '-o', choices=['text', 'json', 'csv'], default='text',
                       help='Output format (default: text)')
    parser.add_argument('--file', '-f', help='Output file path (default: stdout)')
    parser.add_argument('--team-size', type=int, default=5,
                       help='Development team size for effort estimation (default: 5)')
    parser.add_argument('--business-context',
                       help='JSON file with business cost/risk parameters')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose output')

    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )

    args = parser.parse_args()

    # Validate input path
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input path does not exist: {args.input}", file=sys.stderr)
        sys.exit(1)

    # Load business context if provided
    business_context = None
    if args.business_context:
        context_path = Path(args.business_context)
        if context_path.exists():
            with open(context_path, 'r') as f:
                business_context = json.load(f)
        else:
            print(f"Warning: Business context file not found: {args.business_context}", file=sys.stderr)

    # Create scorer
    scorer = TechnicalDebtScorer(
        team_size=args.team_size,
        business_context=business_context,
        verbose=args.verbose
    )

    # Run analysis
    try:
        results = scorer.analyze(input_path)

        if 'error' in results:
            print(f"Error: {results['error']}", file=sys.stderr)
            sys.exit(1)

        # Format output
        if args.output == 'json':
            output_str = json.dumps(results, indent=2)
        elif args.output == 'csv':
            output_str = format_csv_output(results)
        else:  # text
            output_str = format_text_output(results)

        # Write output
        if args.file:
            with open(args.file, 'w') as f:
                f.write(output_str)
            if args.verbose:
                print(f"\nResults written to: {args.file}")
        else:
            print(output_str)

    except Exception as e:
        print(f"Error during analysis: {str(e)}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
