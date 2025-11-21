#!/usr/bin/env python3
"""
Stakeholder Mapper - Create stakeholder maps and engagement plans

Maps stakeholders to power-interest grid and generates engagement strategies
for process improvement initiatives. Uses deterministic algorithms only.

Usage:
    python stakeholder_mapper.py stakeholders.csv
    python stakeholder_mapper.py stakeholders.json --output mermaid
    python stakeholder_mapper.py stakeholders.csv --process process.json --verbose

Input Formats:
    CSV: name,role,department,contact,involvement,mentions,impact
    JSON: {"stakeholders": [{"name": "...", "role": "...", ...}]}

Exit Codes:
    0 - Success
    1 - Validation error
    2 - Parse error
    3 - Mapping error

Author: Claude Code
Version: 1.0.0
"""

import argparse
import csv
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Any, Tuple

# Exit codes
EXIT_SUCCESS = 0
EXIT_VALIDATION_ERROR = 1
EXIT_PARSE_ERROR = 2
EXIT_MAPPING_ERROR = 3

# Classification thresholds
INFLUENCE_THRESHOLD = 3  # 1-5 scale
INTEREST_THRESHOLD = 3   # 1-5 scale


class StakeholderMapper:
    """Maps stakeholders and creates engagement strategies"""

    def __init__(self, verbose: bool = False):
        """Initialize mapper with scoring systems"""
        self.verbose = verbose

        # Role-based influence keywords and scores
        self.influence_keywords = {
            # C-level executives
            'ceo': 5, 'chief executive': 5, 'president': 5,
            'cto': 5, 'chief technology': 5,
            'cfo': 5, 'chief financial': 5,
            'coo': 5, 'chief operating': 5,
            'cio': 5, 'chief information': 5,
            'cpo': 5, 'chief product': 5,

            # Vice presidents
            'vp': 5, 'vice president': 5, 'svp': 5, 'senior vp': 5,
            'evp': 5, 'executive vp': 5,

            # Directors
            'director': 4, 'senior director': 4, 'principal': 4,
            'head of': 4, 'chief': 4,

            # Managers
            'manager': 3, 'senior manager': 3, 'program manager': 3,
            'project manager': 3, 'product manager': 3,

            # Team leads
            'lead': 2, 'team lead': 2, 'tech lead': 2,
            'senior': 2, 'staff': 2, 'principal engineer': 2,

            # Individual contributors
            'engineer': 1, 'developer': 1, 'analyst': 1,
            'specialist': 1, 'coordinator': 1, 'associate': 1,
            'junior': 1
        }

        # Decision authority indicators (bonus points)
        self.authority_keywords = {
            'budget': 1, 'approve': 1, 'authority': 1,
            'decision': 1, 'owner': 1, 'responsible': 1,
            'accountable': 1, 'sponsor': 2, 'executive sponsor': 2
        }

        # Classification definitions
        self.classifications = {
            'Key Player': {
                'description': 'Manage Closely - High influence and high interest',
                'strategy': 'Active partnership - Weekly updates, direct involvement in decisions, co-create solutions',
                'engagement': 'Frequent (weekly/bi-weekly) face-to-face meetings, decision workshops, detailed updates',
                'priority': 'Critical',
                'risk': 'High - Must maintain strong relationship'
            },
            'Keep Satisfied': {
                'description': 'Keep Satisfied - High influence but low interest',
                'strategy': 'Meet their needs without overwhelming - Monthly updates focused on their priorities',
                'engagement': 'Monthly executive summaries, brief check-ins, high-level status reports',
                'priority': 'High',
                'risk': 'Medium - Can block if dissatisfied'
            },
            'Keep Informed': {
                'description': 'Keep Informed - Low influence but high interest',
                'strategy': 'Provide adequate information - Involve in feedback and detailed communication',
                'engagement': 'Weekly email updates, town halls, Q&A sessions, opportunities for input',
                'priority': 'Medium',
                'risk': 'Low - Can be champions/advocates'
            },
            'Monitor': {
                'description': 'Monitor - Low influence and low interest',
                'strategy': 'Minimal effort - General communications and major milestone updates',
                'engagement': 'Quarterly updates, newsletters, general communications only',
                'priority': 'Low',
                'risk': 'Low - Awareness only needed'
            }
        }

    def log(self, message: str):
        """Print verbose logging message"""
        if self.verbose:
            print(f"[DEBUG] {message}", file=sys.stderr)

    def calculate_influence(self, stakeholder: Dict[str, Any]) -> int:
        """
        Calculate influence score (1-5) based on role and authority

        Args:
            stakeholder: Dict with 'role' and optionally 'authority' keys

        Returns:
            Influence score from 1 (low) to 5 (high)
        """
        role = stakeholder.get('role', '').lower()
        authority = stakeholder.get('authority', '').lower()

        # Start with base score from role
        base_score = 1
        role_matched = False

        for keyword, score in sorted(self.influence_keywords.items(),
                                     key=lambda x: len(x[0]), reverse=True):
            if keyword in role:
                base_score = max(base_score, score)
                role_matched = True
                self.log(f"Role '{role}' matched keyword '{keyword}' -> score {score}")
                break

        # Add authority bonuses (max +2)
        authority_bonus = 0
        for keyword, bonus in self.authority_keywords.items():
            if keyword in authority or keyword in role:
                authority_bonus = max(authority_bonus, bonus)
                self.log(f"Authority keyword '{keyword}' found -> bonus {bonus}")

        # Calculate final score (capped at 5)
        final_score = min(base_score + authority_bonus, 5)

        self.log(f"Influence calculation: base={base_score}, authority_bonus={authority_bonus}, final={final_score}")

        return final_score

    def calculate_interest(self, stakeholder: Dict[str, Any],
                          process_context: Dict[str, Any] = None) -> int:
        """
        Calculate interest score (1-5) based on involvement and impact

        Args:
            stakeholder: Dict with involvement, mentions, impact data
            process_context: Optional process documentation for analysis

        Returns:
            Interest score from 1 (low) to 5 (high)
        """
        # Direct involvement (most important factor)
        involvement = stakeholder.get('involvement', 'none').lower()
        involvement_score = {
            'direct': 5,
            'primary': 5,
            'daily': 5,
            'frequent': 4,
            'regular': 4,
            'weekly': 4,
            'occasional': 3,
            'monthly': 3,
            'indirect': 2,
            'rare': 2,
            'minimal': 1,
            'none': 1
        }.get(involvement, 3)  # Default to medium

        # Mention frequency in documentation
        mentions = stakeholder.get('mentions', 0)
        if isinstance(mentions, str):
            mentions = int(mentions) if mentions.isdigit() else 0

        mention_score = min(mentions // 3 + 1, 5)  # 0-2 mentions=1, 3-5=2, etc.

        # Impact on their department
        impact = stakeholder.get('impact', 'low').lower()
        impact_score = {
            'critical': 5,
            'high': 4,
            'significant': 4,
            'medium': 3,
            'moderate': 3,
            'low': 2,
            'minimal': 1,
            'none': 1
        }.get(impact, 3)  # Default to medium

        # Weighted average (involvement counts most)
        final_score = int(
            (involvement_score * 0.5 +
             mention_score * 0.2 +
             impact_score * 0.3)
        )

        self.log(f"Interest calculation: involvement={involvement_score}, "
                f"mentions={mention_score}, impact={impact_score}, final={final_score}")

        return max(1, min(final_score, 5))

    def classify_stakeholder(self, influence: int, interest: int) -> str:
        """
        Classify stakeholder into Power-Interest grid quadrant

        Args:
            influence: Score 1-5 (power level)
            interest: Score 1-5 (interest level)

        Returns:
            Classification: Key Player, Keep Satisfied, Keep Informed, Monitor
        """
        high_influence = influence >= INFLUENCE_THRESHOLD
        high_interest = interest >= INTEREST_THRESHOLD

        if high_influence and high_interest:
            return 'Key Player'
        elif high_influence and not high_interest:
            return 'Keep Satisfied'
        elif not high_influence and high_interest:
            return 'Keep Informed'
        else:
            return 'Monitor'

    def identify_impact_areas(self, stakeholder: Dict[str, Any]) -> List[str]:
        """
        Identify areas where stakeholder has impact

        Args:
            stakeholder: Stakeholder data

        Returns:
            List of impact areas
        """
        areas = []

        role = stakeholder.get('role', '').lower()
        department = stakeholder.get('department', '').lower()

        # Budget control
        if any(kw in role for kw in ['cfo', 'finance', 'vp', 'director', 'budget']):
            areas.append('Budget')

        # Resource allocation
        if any(kw in role for kw in ['manager', 'director', 'vp', 'head', 'lead']):
            areas.append('Resources')

        # Timeline decisions
        if any(kw in role for kw in ['project manager', 'program manager', 'director', 'vp']):
            areas.append('Timeline')

        # Technical decisions
        if any(kw in role for kw in ['cto', 'architect', 'tech lead', 'engineering']):
            areas.append('Technical Decisions')

        # Strategic direction
        if any(kw in role for kw in ['ceo', 'president', 'chief', 'vp', 'strategy']):
            areas.append('Strategic Direction')

        # Process changes
        if any(kw in role for kw in ['operations', 'process', 'business analyst', 'coo']):
            areas.append('Process Changes')

        # User experience
        if any(kw in role for kw in ['product', 'ux', 'design', 'customer']):
            areas.append('User Experience')

        # Compliance
        if any(kw in role for kw in ['compliance', 'legal', 'security', 'risk']):
            areas.append('Compliance')

        # Department-specific areas
        if department:
            areas.append(f"{department.title()} Operations")

        return areas if areas else ['General Operations']

    def identify_relationships(self, stakeholder: Dict[str, Any],
                              all_stakeholders: List[Dict[str, Any]]) -> List[str]:
        """
        Identify relationships with other stakeholders

        Args:
            stakeholder: Current stakeholder
            all_stakeholders: All stakeholders in map

        Returns:
            List of relationship descriptions
        """
        relationships = []

        current_role = stakeholder.get('role', '').lower()
        current_dept = stakeholder.get('department', '')

        # Reporting relationships
        if 'reports_to' in stakeholder:
            relationships.append(f"{stakeholder['reports_to']} (reports to)")

        # Management relationships
        if any(kw in current_role for kw in ['manager', 'director', 'vp', 'ceo', 'head']):
            # Find potential direct reports in same department
            for other in all_stakeholders:
                if other.get('name') == stakeholder.get('name'):
                    continue
                if other.get('department') == current_dept:
                    other_role = other.get('role', '').lower()
                    if not any(kw in other_role for kw in ['manager', 'director', 'vp']):
                        # Likely manages this person
                        relationships.append(f"{other.get('name', 'Unknown')} (manages)")

        # Collaboration relationships (same department, similar level)
        for other in all_stakeholders:
            if other.get('name') == stakeholder.get('name'):
                continue
            if other.get('department') == current_dept:
                relationships.append(f"{other.get('name', 'Unknown')} (collaborates)")
                break  # Only add one example

        # Cross-functional relationships
        if 'stakeholder_relations' in stakeholder:
            for relation in stakeholder['stakeholder_relations']:
                relationships.append(relation)

        return relationships if relationships else ['Independent contributor']

    def generate_engagement_strategy(self, stakeholder: Dict[str, Any],
                                    classification: str,
                                    influence: int, interest: int) -> str:
        """
        Generate specific engagement strategy for stakeholder

        Args:
            stakeholder: Stakeholder data
            classification: Power-Interest classification
            influence: Influence score
            interest: Interest score

        Returns:
            Detailed engagement strategy
        """
        base_strategy = self.classifications[classification]['strategy']

        # Customize based on role
        role = stakeholder.get('role', '').lower()
        customizations = []

        if 'ceo' in role or 'president' in role:
            customizations.append("Focus on business impact and strategic alignment")
        elif 'cfo' in role or 'finance' in role:
            customizations.append("Emphasize ROI, cost savings, and budget implications")
        elif 'cto' in role or 'technology' in role:
            customizations.append("Highlight technical architecture and innovation")
        elif 'coo' in role or 'operations' in role:
            customizations.append("Focus on operational efficiency and process improvement")

        if classification == 'Key Player':
            customizations.append("Involve in key decisions and milestone reviews")
            customizations.append("Seek input on major changes before implementation")
        elif classification == 'Keep Satisfied':
            customizations.append("Keep informed of major milestones")
            customizations.append("Address concerns promptly")

        # Combine base strategy with customizations
        if customizations:
            return f"{base_strategy}. {'. '.join(customizations)}."
        return base_strategy

    def parse_csv(self, file_path: Path) -> List[Dict[str, Any]]:
        """
        Parse CSV file containing stakeholder data

        Expected columns: name, role, department, contact, involvement, mentions, impact
        Optional columns: authority, reports_to

        Args:
            file_path: Path to CSV file

        Returns:
            List of stakeholder dictionaries

        Raises:
            ValueError: If required columns missing
        """
        stakeholders = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)

                # Validate required columns
                required = {'name', 'role'}
                if not required.issubset(set(reader.fieldnames)):
                    missing = required - set(reader.fieldnames)
                    raise ValueError(f"Missing required columns: {missing}")

                for row in reader:
                    # Clean and validate data
                    stakeholder = {
                        'name': row.get('name', '').strip(),
                        'role': row.get('role', '').strip(),
                        'department': row.get('department', 'General').strip(),
                        'contact': row.get('contact', '').strip(),
                        'involvement': row.get('involvement', 'none').strip(),
                        'mentions': row.get('mentions', '0').strip(),
                        'impact': row.get('impact', 'low').strip(),
                        'authority': row.get('authority', '').strip(),
                        'reports_to': row.get('reports_to', '').strip()
                    }

                    if stakeholder['name'] and stakeholder['role']:
                        stakeholders.append(stakeholder)
                    else:
                        self.log(f"Skipping invalid row: {row}")

        except FileNotFoundError:
            raise ValueError(f"File not found: {file_path}")
        except Exception as e:
            raise ValueError(f"Error parsing CSV: {e}")

        return stakeholders

    def parse_json(self, file_path: Path) -> List[Dict[str, Any]]:
        """
        Parse JSON file containing stakeholder data

        Expected format:
        {
            "stakeholders": [
                {"name": "...", "role": "...", ...}
            ]
        }

        Args:
            file_path: Path to JSON file

        Returns:
            List of stakeholder dictionaries
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if isinstance(data, dict) and 'stakeholders' in data:
                stakeholders = data['stakeholders']
            elif isinstance(data, list):
                stakeholders = data
            else:
                raise ValueError("JSON must contain 'stakeholders' array or be an array")

            # Validate and normalize
            validated = []
            for s in stakeholders:
                if not isinstance(s, dict):
                    continue
                if 'name' not in s or 'role' not in s:
                    self.log(f"Skipping stakeholder without name/role: {s}")
                    continue

                # Normalize fields
                stakeholder = {
                    'name': s.get('name', ''),
                    'role': s.get('role', ''),
                    'department': s.get('department', 'General'),
                    'contact': s.get('contact', ''),
                    'involvement': s.get('involvement', 'none'),
                    'mentions': str(s.get('mentions', 0)),
                    'impact': s.get('impact', 'low'),
                    'authority': s.get('authority', ''),
                    'reports_to': s.get('reports_to', '')
                }
                validated.append(stakeholder)

            return validated

        except FileNotFoundError:
            raise ValueError(f"File not found: {file_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {e}")
        except Exception as e:
            raise ValueError(f"Error parsing JSON: {e}")

    def load_stakeholders(self, file_path: Path) -> List[Dict[str, Any]]:
        """
        Load stakeholders from CSV or JSON file

        Args:
            file_path: Path to input file

        Returns:
            List of stakeholder dictionaries
        """
        suffix = file_path.suffix.lower()

        if suffix == '.csv':
            return self.parse_csv(file_path)
        elif suffix == '.json':
            return self.parse_json(file_path)
        else:
            raise ValueError(f"Unsupported file format: {suffix}. Use .csv or .json")

    def map_stakeholders(self, stakeholders: List[Dict[str, Any]],
                        process_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Create complete stakeholder map with classifications and strategies

        Args:
            stakeholders: List of stakeholder data
            process_context: Optional process context for interest calculation

        Returns:
            Complete stakeholder map dictionary
        """
        if not stakeholders:
            raise ValueError("No stakeholders provided")

        mapped_stakeholders = []
        classification_counts = defaultdict(int)

        for stakeholder in stakeholders:
            self.log(f"\nProcessing stakeholder: {stakeholder.get('name')}")

            # Calculate scores
            influence = self.calculate_influence(stakeholder)
            interest = self.calculate_interest(stakeholder, process_context)

            # Classify
            classification = self.classify_stakeholder(influence, interest)
            classification_counts[classification] += 1

            # Generate engagement strategy
            engagement_strategy = self.generate_engagement_strategy(
                stakeholder, classification, influence, interest
            )

            # Identify impact areas and relationships
            impact_areas = self.identify_impact_areas(stakeholder)
            relationships = self.identify_relationships(stakeholder, stakeholders)

            # Build complete stakeholder profile
            mapped = {
                'name': stakeholder['name'],
                'role': stakeholder['role'],
                'department': stakeholder['department'],
                'contact': stakeholder.get('contact', ''),
                'influence_score': influence,
                'interest_score': interest,
                'classification': classification,
                'engagement_strategy': engagement_strategy,
                'impact_areas': impact_areas,
                'relationships': relationships[:3],  # Limit to top 3
                'priority': self.classifications[classification]['priority'],
                'risk_level': self.classifications[classification]['risk']
            }

            mapped_stakeholders.append(mapped)

        # Sort by priority (Key Player > Keep Satisfied > Keep Informed > Monitor)
        priority_order = {'Critical': 0, 'High': 1, 'Medium': 2, 'Low': 3}
        mapped_stakeholders.sort(
            key=lambda x: (priority_order[x['priority']], -x['influence_score'], -x['interest_score'])
        )

        # Create engagement plan
        engagement_plan = self._create_engagement_plan(mapped_stakeholders)

        # Build result
        result = {
            'process_name': process_context.get('name', 'Process Improvement Initiative') if process_context else 'Process Improvement Initiative',
            'analysis_date': self._get_current_date(),
            'stakeholder_count': len(mapped_stakeholders),
            'stakeholders': mapped_stakeholders,
            'classification_summary': dict(classification_counts),
            'engagement_plan': engagement_plan,
            'recommendations': self._generate_recommendations(
                mapped_stakeholders, classification_counts
            )
        }

        return result

    def _create_engagement_plan(self, stakeholders: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        """Create prioritized engagement plan"""
        plan = {
            'high_priority': [],
            'medium_priority': [],
            'low_priority': []
        }

        for s in stakeholders:
            name = s['name']
            if s['priority'] == 'Critical':
                plan['high_priority'].append(name)
            elif s['priority'] == 'High':
                plan['high_priority'].append(name)
            elif s['priority'] == 'Medium':
                plan['medium_priority'].append(name)
            else:
                plan['low_priority'].append(name)

        return plan

    def _generate_recommendations(self, stakeholders: List[Dict[str, Any]],
                                  classification_counts: Dict[str, int]) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []

        # Check for Key Players
        key_players = classification_counts.get('Key Player', 0)
        if key_players == 0:
            recommendations.append(
                "⚠️  No Key Players identified - Consider elevating project sponsor or "
                "executive champion to ensure adequate support"
            )
        elif key_players > 5:
            recommendations.append(
                "⚠️  Too many Key Players (>5) - This may slow decision-making. "
                "Consider whether all require weekly engagement."
            )

        # Check for Keep Satisfied stakeholders
        keep_satisfied = classification_counts.get('Keep Satisfied', 0)
        if keep_satisfied > 0:
            recommendations.append(
                f"Focus on keeping {keep_satisfied} high-influence stakeholders satisfied "
                "through regular but not overwhelming updates"
            )

        # Identify potential coalition opportunities
        departments = defaultdict(int)
        for s in stakeholders:
            if s['classification'] in ['Key Player', 'Keep Informed']:
                departments[s['department']] += 1

        if len(departments) > 3:
            recommendations.append(
                "Build cross-functional coalition with representatives from "
                f"{', '.join(list(departments.keys())[:3])} departments"
            )

        # Communication strategy
        total_stakeholders = len(stakeholders)
        if total_stakeholders > 20:
            recommendations.append(
                "Large stakeholder group - Consider tiered communication strategy "
                "(executive summary, detailed updates, Q&A forums)"
            )

        # Resistance management
        low_interest = sum(1 for s in stakeholders if s['interest_score'] < 3)
        if low_interest > total_stakeholders * 0.3:
            recommendations.append(
                f"30%+ stakeholders have low interest - Develop change management plan "
                "to increase engagement and reduce resistance"
            )

        return recommendations

    def _get_current_date(self) -> str:
        """Get current date in YYYY-MM-DD format"""
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d')

    def generate_mermaid(self, result: Dict[str, Any]) -> str:
        """
        Generate Mermaid diagram showing stakeholder relationships

        Args:
            result: Stakeholder map result

        Returns:
            Mermaid diagram as string
        """
        lines = ["graph TD"]

        # Define color scheme for classifications
        colors = {
            'Key Player': '#ff6b6b',
            'Keep Satisfied': '#ffa500',
            'Keep Informed': '#4ecdc4',
            'Monitor': '#95a5a6'
        }

        # Node definitions
        node_ids = {}
        for i, s in enumerate(result['stakeholders']):
            node_id = f"S{i}"
            node_ids[s['name']] = node_id

            # Create node label
            label = f"{s['name']}<br/>{s['role']}<br/>{s['classification']}"
            lines.append(f'    {node_id}["{label}"]')

        # Relationship edges (limit to top stakeholders)
        added_edges = set()
        for s in result['stakeholders'][:10]:  # Limit to top 10 for readability
            source_id = node_ids[s['name']]

            for rel in s['relationships'][:2]:  # Max 2 relationships per stakeholder
                # Parse relationship
                if '(' in rel:
                    target_name = rel.split('(')[0].strip()
                    rel_type = rel.split('(')[1].replace(')', '').strip()

                    if target_name in node_ids:
                        target_id = node_ids[target_name]
                        edge = (source_id, target_id, rel_type)

                        if edge not in added_edges:
                            lines.append(f'    {source_id} -->|{rel_type}| {target_id}')
                            added_edges.add(edge)

        # Styles
        lines.append("")
        for s in result['stakeholders']:
            node_id = node_ids[s['name']]
            color = colors.get(s['classification'], '#95a5a6')
            lines.append(f'    style {node_id} fill:{color}')

        return '\n'.join(lines)

    def format_output(self, result: Dict[str, Any], output_format: str = 'json') -> str:
        """
        Format result in requested output format

        Args:
            result: Stakeholder map result
            output_format: 'json', 'markdown', or 'mermaid'

        Returns:
            Formatted output string
        """
        if output_format == 'json':
            return json.dumps(result, indent=2)

        elif output_format == 'mermaid':
            return self.generate_mermaid(result)

        elif output_format == 'markdown':
            lines = []
            lines.append(f"# Stakeholder Analysis: {result['process_name']}")
            lines.append(f"\n**Analysis Date:** {result['analysis_date']}")
            lines.append(f"**Total Stakeholders:** {result['stakeholder_count']}")
            lines.append("")

            # Classification summary
            lines.append("## Classification Summary")
            lines.append("")
            for classification, count in result['classification_summary'].items():
                lines.append(f"- **{classification}:** {count}")
            lines.append("")

            # Engagement plan
            lines.append("## Engagement Plan")
            lines.append("")
            lines.append("### High Priority")
            for name in result['engagement_plan']['high_priority']:
                lines.append(f"- {name}")
            lines.append("")

            lines.append("### Medium Priority")
            for name in result['engagement_plan']['medium_priority']:
                lines.append(f"- {name}")
            lines.append("")

            lines.append("### Low Priority")
            for name in result['engagement_plan']['low_priority']:
                lines.append(f"- {name}")
            lines.append("")

            # Stakeholder details
            lines.append("## Stakeholder Profiles")
            lines.append("")

            for s in result['stakeholders']:
                lines.append(f"### {s['name']}")
                lines.append(f"**Role:** {s['role']}")
                lines.append(f"**Department:** {s['department']}")
                lines.append(f"**Classification:** {s['classification']}")
                lines.append(f"**Influence:** {s['influence_score']}/5 | **Interest:** {s['interest_score']}/5")
                lines.append(f"**Priority:** {s['priority']}")
                lines.append("")

                lines.append("**Engagement Strategy:**")
                lines.append(s['engagement_strategy'])
                lines.append("")

                lines.append("**Impact Areas:**")
                for area in s['impact_areas']:
                    lines.append(f"- {area}")
                lines.append("")

                lines.append("**Key Relationships:**")
                for rel in s['relationships']:
                    lines.append(f"- {rel}")
                lines.append("")

            # Recommendations
            lines.append("## Recommendations")
            lines.append("")
            for rec in result['recommendations']:
                lines.append(f"- {rec}")
            lines.append("")

            return '\n'.join(lines)

        else:
            raise ValueError(f"Unsupported output format: {output_format}")


def validate_arguments(args: argparse.Namespace) -> None:
    """
    Validate command-line arguments

    Args:
        args: Parsed arguments

    Raises:
        ValueError: If validation fails
    """
    # Check input file exists
    input_path = Path(args.input)
    if not input_path.exists():
        raise ValueError(f"Input file not found: {args.input}")

    # Check file format
    if input_path.suffix.lower() not in ['.csv', '.json']:
        raise ValueError(f"Unsupported file format: {input_path.suffix}. Use .csv or .json")

    # Check output format
    valid_formats = ['json', 'markdown', 'mermaid']
    if args.output not in valid_formats:
        raise ValueError(f"Invalid output format: {args.output}. Choose from {valid_formats}")

    # Check process context file if provided
    if args.process:
        process_path = Path(args.process)
        if not process_path.exists():
            raise ValueError(f"Process context file not found: {args.process}")
        if process_path.suffix.lower() != '.json':
            raise ValueError("Process context must be JSON file")


def main():
    """Main entry point for stakeholder mapper"""
    parser = argparse.ArgumentParser(
        description='Map stakeholders and generate engagement strategies',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic stakeholder mapping
  python stakeholder_mapper.py stakeholders.csv

  # With process context
  python stakeholder_mapper.py stakeholders.json --process process.json

  # Mermaid diagram output
  python stakeholder_mapper.py stakeholders.csv --output mermaid

  # Markdown report
  python stakeholder_mapper.py stakeholders.json --output markdown

  # Verbose logging
  python stakeholder_mapper.py stakeholders.csv --verbose

CSV Format:
  name,role,department,contact,involvement,mentions,impact
  John Smith,VP Operations,Operations,john@example.com,direct,15,high
  Jane Doe,Director IT,IT,jane@example.com,frequent,8,medium

JSON Format:
  {
    "stakeholders": [
      {
        "name": "John Smith",
        "role": "VP Operations",
        "department": "Operations",
        "involvement": "direct",
        "mentions": 15,
        "impact": "high"
      }
    ]
  }

Exit Codes:
  0 - Success
  1 - Validation error
  2 - Parse error
  3 - Mapping error
        """
    )

    # Required arguments
    parser.add_argument(
        'input',
        help='Input file (CSV or JSON) containing stakeholder data'
    )

    # Optional arguments
    parser.add_argument(
        '--output',
        choices=['json', 'markdown', 'mermaid'],
        default='json',
        help='Output format (default: json)'
    )

    parser.add_argument(
        '--process',
        help='Process context file (JSON) for enhanced interest calculation'
    )

    parser.add_argument(
        '--org-chart',
        help='Organizational chart file (JSON) for relationship mapping'
    )

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )

    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )

    # Parse arguments
    args = parser.parse_args()

    try:
        # Validate arguments
        validate_arguments(args)

        # Initialize mapper
        mapper = StakeholderMapper(verbose=args.verbose)

        # Load stakeholders
        stakeholders = mapper.load_stakeholders(Path(args.input))

        if not stakeholders:
            print("Error: No valid stakeholders found in input file", file=sys.stderr)
            sys.exit(EXIT_VALIDATION_ERROR)

        # Load process context if provided
        process_context = None
        if args.process:
            with open(args.process, 'r') as f:
                process_context = json.load(f)

        # Map stakeholders
        result = mapper.map_stakeholders(stakeholders, process_context)

        # Format and output
        output = mapper.format_output(result, args.output)
        print(output)

        sys.exit(EXIT_SUCCESS)

    except ValueError as e:
        print(f"Validation Error: {e}", file=sys.stderr)
        sys.exit(EXIT_VALIDATION_ERROR)

    except json.JSONDecodeError as e:
        print(f"Parse Error: Invalid JSON - {e}", file=sys.stderr)
        sys.exit(EXIT_PARSE_ERROR)

    except Exception as e:
        print(f"Mapping Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(EXIT_MAPPING_ERROR)


if __name__ == '__main__':
    main()
