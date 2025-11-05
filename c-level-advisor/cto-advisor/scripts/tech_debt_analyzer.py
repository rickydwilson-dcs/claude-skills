#!/usr/bin/env python3
"""
Technical Debt Analyzer - Assess and prioritize technical debt across systems

This tool helps CTOs and engineering leaders quantify technical debt, assess risks,
prioritize reduction actions, and create roadmaps for debt reduction initiatives.

Usage:
    python tech_debt_analyzer.py system_data.json
    python tech_debt_analyzer.py system_data.json --output json
    python tech_debt_analyzer.py system_data.json -o json -f debt_report.json

Author: claude-skills
Version: 2.0.0
Last Updated: 2025-11-05
"""

import argparse
import json
import csv
from io import StringIO
import math
import sys
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime

class TechDebtAnalyzer:
    def __init__(self):
        self.debt_categories = {
            'architecture': {
                'weight': 0.25,
                'indicators': [
                    'monolithic_design', 'tight_coupling', 'no_microservices',
                    'legacy_patterns', 'no_api_gateway', 'synchronous_only'
                ]
            },
            'code_quality': {
                'weight': 0.20,
                'indicators': [
                    'low_test_coverage', 'high_complexity', 'code_duplication',
                    'no_documentation', 'inconsistent_standards', 'legacy_language'
                ]
            },
            'infrastructure': {
                'weight': 0.20,
                'indicators': [
                    'manual_deployments', 'no_ci_cd', 'single_points_failure',
                    'no_monitoring', 'no_auto_scaling', 'outdated_servers'
                ]
            },
            'security': {
                'weight': 0.20,
                'indicators': [
                    'outdated_dependencies', 'no_security_scans', 'plain_text_secrets',
                    'no_encryption', 'missing_auth', 'no_audit_logs'
                ]
            },
            'performance': {
                'weight': 0.15,
                'indicators': [
                    'slow_response_times', 'no_caching', 'inefficient_queries',
                    'memory_leaks', 'no_optimization', 'blocking_operations'
                ]
            }
        }
        
        self.impact_matrix = {
            'user_impact': {'weight': 0.30, 'score': 0},
            'developer_velocity': {'weight': 0.25, 'score': 0},
            'system_reliability': {'weight': 0.20, 'score': 0},
            'scalability': {'weight': 0.15, 'score': 0},
            'maintenance_cost': {'weight': 0.10, 'score': 0}
        }
    
    def analyze_system(self, system_data: Dict) -> Dict:
        """Analyze a system for technical debt"""
        results = {
            'timestamp': datetime.now().isoformat(),
            'system_name': system_data.get('name', 'Unknown'),
            'debt_score': 0,
            'debt_level': '',
            'category_scores': {},
            'prioritized_actions': [],
            'estimated_effort': {},
            'risk_assessment': {},
            'recommendations': []
        }
        
        # Calculate debt scores by category
        total_debt_score = 0
        for category, config in self.debt_categories.items():
            category_score = self._calculate_category_score(
                system_data.get(category, {}), 
                config['indicators']
            )
            weighted_score = category_score * config['weight']
            results['category_scores'][category] = {
                'raw_score': category_score,
                'weighted_score': weighted_score,
                'level': self._get_level(category_score)
            }
            total_debt_score += weighted_score
        
        results['debt_score'] = round(total_debt_score, 2)
        results['debt_level'] = self._get_level(total_debt_score)
        
        # Calculate impact and prioritize
        results['prioritized_actions'] = self._prioritize_actions(
            results['category_scores'],
            system_data.get('business_context', {})
        )
        
        # Estimate effort
        results['estimated_effort'] = self._estimate_effort(
            results['prioritized_actions'],
            system_data.get('team_size', 5)
        )
        
        # Risk assessment
        results['risk_assessment'] = self._assess_risks(
            results['debt_score'],
            system_data.get('system_criticality', 'medium')
        )
        
        # Generate recommendations
        results['recommendations'] = self._generate_recommendations(results)
        
        return results
    
    def _calculate_category_score(self, category_data: Dict, indicators: List) -> float:
        """Calculate score for a specific category"""
        if not category_data:
            return 50.0  # Default middle score if no data
        
        total_score = 0
        count = 0
        
        for indicator in indicators:
            if indicator in category_data:
                # Score from 0 (no debt) to 100 (high debt)
                total_score += category_data[indicator]
                count += 1
        
        return (total_score / count) if count > 0 else 50.0
    
    def _get_level(self, score: float) -> str:
        """Convert numerical score to level"""
        if score < 20:
            return 'Low'
        elif score < 40:
            return 'Medium-Low'
        elif score < 60:
            return 'Medium'
        elif score < 80:
            return 'Medium-High'
        else:
            return 'Critical'
    
    def _prioritize_actions(self, category_scores: Dict, business_context: Dict) -> List:
        """Prioritize technical debt reduction actions"""
        actions = []
        
        for category, scores in category_scores.items():
            if scores['raw_score'] > 60:  # Focus on high debt areas
                priority = self._calculate_priority(
                    scores['raw_score'],
                    category,
                    business_context
                )
                
                action = {
                    'category': category,
                    'priority': priority,
                    'score': scores['raw_score'],
                    'action_items': self._get_action_items(category, scores['level'])
                }
                actions.append(action)
        
        # Sort by priority
        actions.sort(key=lambda x: x['priority'], reverse=True)
        return actions[:5]  # Top 5 priorities
    
    def _calculate_priority(self, score: float, category: str, context: Dict) -> float:
        """Calculate priority based on score and business context"""
        base_priority = score
        
        # Adjust based on business context
        if context.get('growth_phase') == 'rapid' and category in ['scalability', 'performance']:
            base_priority *= 1.5
        
        if context.get('compliance_required') and category == 'security':
            base_priority *= 2.0
        
        if context.get('cost_pressure') and category == 'infrastructure':
            base_priority *= 1.3
        
        return min(100, base_priority)
    
    def _get_action_items(self, category: str, level: str) -> List[str]:
        """Get specific action items based on category and level"""
        actions = {
            'architecture': {
                'Critical': [
                    'Immediate: Create architecture migration roadmap',
                    'Week 1: Identify service boundaries for decomposition',
                    'Month 1: Begin extracting first microservice',
                    'Month 2: Implement API gateway',
                    'Quarter: Complete critical service separation'
                ],
                'Medium-High': [
                    'Month 1: Document current architecture',
                    'Month 2: Design target architecture',
                    'Quarter: Begin gradual migration',
                    'Monitor: Track coupling metrics'
                ]
            },
            'code_quality': {
                'Critical': [
                    'Immediate: Implement code quality gates',
                    'Week 1: Set up automated testing pipeline',
                    'Month 1: Achieve 40% test coverage',
                    'Month 2: Refactor critical modules',
                    'Quarter: Reach 70% test coverage'
                ],
                'Medium-High': [
                    'Month 1: Establish coding standards',
                    'Month 2: Implement code review process',
                    'Quarter: Gradual refactoring plan'
                ]
            },
            'infrastructure': {
                'Critical': [
                    'Immediate: Implement basic CI/CD',
                    'Week 1: Set up monitoring and alerts',
                    'Month 1: Automate critical deployments',
                    'Month 2: Implement disaster recovery',
                    'Quarter: Full infrastructure as code'
                ],
                'Medium-High': [
                    'Month 1: Document infrastructure',
                    'Month 2: Begin automation',
                    'Quarter: Modernize critical components'
                ]
            },
            'security': {
                'Critical': [
                    'Immediate: Security audit and patching',
                    'Week 1: Implement secrets management',
                    'Month 1: Set up vulnerability scanning',
                    'Month 2: Implement security training',
                    'Quarter: Achieve compliance standards'
                ],
                'Medium-High': [
                    'Month 1: Security assessment',
                    'Month 2: Implement security tools',
                    'Quarter: Regular security reviews'
                ]
            },
            'performance': {
                'Critical': [
                    'Immediate: Performance profiling',
                    'Week 1: Implement caching strategy',
                    'Month 1: Optimize database queries',
                    'Month 2: Implement CDN',
                    'Quarter: Re-architect bottlenecks'
                ],
                'Medium-High': [
                    'Month 1: Performance baseline',
                    'Month 2: Optimization plan',
                    'Quarter: Incremental improvements'
                ]
            }
        }
        
        return actions.get(category, {}).get(level, ['Create action plan'])
    
    def _estimate_effort(self, actions: List, team_size: int) -> Dict:
        """Estimate effort required for debt reduction"""
        total_story_points = 0
        effort_breakdown = {}
        
        for action in actions:
            # Estimate based on category and score
            base_points = action['score'] * 2  # Higher debt = more effort
            
            if action['category'] == 'architecture':
                points = base_points * 1.5  # Architecture changes are complex
            elif action['category'] == 'security':
                points = base_points * 1.2  # Security requires careful work
            else:
                points = base_points
            
            effort_breakdown[action['category']] = {
                'story_points': round(points),
                'sprints': math.ceil(points / (team_size * 20)),  # 20 points per dev per sprint
                'developers_needed': math.ceil(points / 100)
            }
            total_story_points += points
        
        return {
            'total_story_points': round(total_story_points),
            'estimated_sprints': math.ceil(total_story_points / (team_size * 20)),
            'recommended_team_size': max(team_size, math.ceil(total_story_points / 200)),
            'breakdown': effort_breakdown
        }
    
    def _assess_risks(self, debt_score: float, criticality: str) -> Dict:
        """Assess risks associated with technical debt"""
        risk_level = 'Low'
        
        if debt_score > 70 and criticality == 'high':
            risk_level = 'Critical'
        elif debt_score > 60 or criticality == 'high':
            risk_level = 'High'
        elif debt_score > 40:
            risk_level = 'Medium'
        
        risks = {
            'overall_risk': risk_level,
            'specific_risks': []
        }
        
        if debt_score > 60:
            risks['specific_risks'].extend([
                'System failure risk increasing',
                'Developer productivity declining',
                'Innovation velocity blocked',
                'Maintenance costs escalating'
            ])
        
        if debt_score > 80:
            risks['specific_risks'].extend([
                'Competitive disadvantage emerging',
                'Talent retention risk',
                'Customer satisfaction impact',
                'Potential data breach vulnerability'
            ])
        
        return risks
    
    def _generate_recommendations(self, results: Dict) -> List[str]:
        """Generate strategic recommendations"""
        recommendations = []
        
        # Overall strategy based on debt level
        if results['debt_level'] == 'Critical':
            recommendations.append('🚨 URGENT: Dedicate 40% of engineering capacity to debt reduction')
            recommendations.append('Create dedicated debt reduction team')
            recommendations.append('Implement weekly debt reduction reviews')
            recommendations.append('Consider temporary feature freeze')
        elif results['debt_level'] in ['Medium-High', 'High']:
            recommendations.append('Allocate 25-30% of sprints to debt reduction')
            recommendations.append('Establish technical debt budget')
            recommendations.append('Implement debt prevention practices')
        else:
            recommendations.append('Maintain 15-20% ongoing debt reduction allocation')
            recommendations.append('Focus on prevention over correction')
        
        # Category-specific recommendations
        for category, scores in results['category_scores'].items():
            if scores['raw_score'] > 70:
                if category == 'architecture':
                    recommendations.append(f'Consider hiring architecture specialist')
                elif category == 'security':
                    recommendations.append(f'Engage security audit firm')
                elif category == 'performance':
                    recommendations.append(f'Implement performance SLA monitoring')
        
        # Team recommendations
        effort = results.get('estimated_effort', {})
        if effort.get('recommended_team_size', 0) > effort.get('total_story_points', 0) / 200:
            recommendations.append(f"Scale team to {effort['recommended_team_size']} engineers")
        
        return recommendations

def analyze_technical_debt(system_config: Dict) -> str:
    """Main function to analyze technical debt"""
    analyzer = TechDebtAnalyzer()
    results = analyzer.analyze_system(system_config)

    # Format output
    output = [
        f"=== Technical Debt Analysis Report ===",
        f"System: {results['system_name']}",
        f"Analysis Date: {results['timestamp'][:10]}",
        f"",
        f"OVERALL DEBT SCORE: {results['debt_score']}/100 ({results['debt_level']})",
        f"",
        "Category Breakdown:"
    ]

    for category, scores in results['category_scores'].items():
        output.append(f"  {category.title()}: {scores['raw_score']:.1f} ({scores['level']})")

    output.extend([
        f"",
        "Risk Assessment:",
        f"  Overall Risk: {results['risk_assessment']['overall_risk']}"
    ])

    for risk in results['risk_assessment']['specific_risks']:
        output.append(f"  • {risk}")

    output.extend([
        f"",
        "Effort Estimation:",
        f"  Total Story Points: {results['estimated_effort']['total_story_points']}",
        f"  Estimated Sprints: {results['estimated_effort']['estimated_sprints']}",
        f"  Recommended Team Size: {results['estimated_effort']['recommended_team_size']}",
        f"",
        "Top Priority Actions:"
    ])

    for i, action in enumerate(results['prioritized_actions'][:3], 1):
        output.append(f"\n{i}. {action['category'].title()} (Priority: {action['priority']:.0f})")
        for item in action['action_items'][:3]:
            output.append(f"   - {item}")

    output.extend([
        f"",
        "Strategic Recommendations:"
    ])

    for rec in results['recommendations']:
        output.append(f"  • {rec}")

    return '\n'.join(output)


def format_csv_output(system_config: Dict) -> str:
    """Format technical debt analysis results as CSV"""
    analyzer = TechDebtAnalyzer()
    results = analyzer.analyze_system(system_config)

    output = StringIO()
    writer = csv.writer(output)

    # Header row
    writer.writerow(['category', 'issue', 'severity', 'effort_days', 'priority', 'status'])

    # Write prioritized actions
    for action in results.get('prioritized_actions', [])[:10]:
        writer.writerow([
            action.get('category', ''),
            f"{action.get('category', 'issue').title()} improvement",
            action.get('category', '').upper(),
            int(action.get('priority', 1) * 5),  # Estimate days
            int(action.get('priority', 0)),
            'open'
        ])

    return output.getvalue()

def format_json_output(system_config: Dict) -> str:
    """Format results as JSON with metadata"""
    analyzer = TechDebtAnalyzer()
    results = analyzer.analyze_system(system_config)

    output = {
        "metadata": {
            "tool": "tech_debt_analyzer.py",
            "version": "2.0.0",
            "timestamp": datetime.now().isoformat()
        },
        "inputs": {
            "system_config": system_config
        },
        "results": results
    }

    return json.dumps(output, indent=2)


def main():
    """
    Main entry point with standardized argument parsing.

    Parses command-line arguments, validates input, analyzes technical debt,
    and writes output in the specified format.
    """
    parser = argparse.ArgumentParser(
        description='Analyze technical debt across architecture, code quality, infrastructure, security, and performance',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic analysis with text output
  %(prog)s system_data.json

  # JSON output for engineering dashboards
  %(prog)s system_data.json --output json

  # Save to file
  %(prog)s system_data.json -o json -f debt_report.json

  # Verbose mode with detailed logging
  %(prog)s system_data.json -v

Input JSON Format:
  {
    "name": "Legacy E-commerce Platform",
    "architecture": {
      "monolithic_design": 80,
      "tight_coupling": 70,
      "no_microservices": 90,
      "legacy_patterns": 60
    },
    "code_quality": {
      "low_test_coverage": 75,
      "high_complexity": 65,
      "code_duplication": 55
    },
    "infrastructure": {
      "manual_deployments": 70,
      "no_ci_cd": 60,
      "no_monitoring": 40
    },
    "security": {
      "outdated_dependencies": 85,
      "no_security_scans": 70
    },
    "performance": {
      "slow_response_times": 60,
      "no_caching": 50
    },
    "team_size": 8,
    "system_criticality": "high",
    "business_context": {
      "growth_phase": "rapid",
      "compliance_required": true,
      "cost_pressure": false
    }
  }

Debt Score Scale:
  0-100 where higher = more technical debt
  Categories: architecture, code_quality, infrastructure, security, performance
  Levels: Low, Medium-Low, Medium, Medium-High, Critical

For more information, see:
c-level-advisor/cto-advisor/SKILL.md
        """
    )

    # Positional arguments
    parser.add_argument(
        'input',
        help='JSON file with system technical debt data'
    )

    # Optional arguments
    parser.add_argument(
        '--output', '-o',
        choices=['text', 'json', 'csv'],
        default='text',
        help='Output format: text (default), json, or csv'
    )

    parser.add_argument(
        '--file', '-f',
        help='Write output to file instead of stdout'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output with detailed information'
    )

    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 2.0.0'
    )

    # Parse arguments
    args = parser.parse_args()

    try:
        # Validate input file
        input_path = Path(args.input)

        if not input_path.exists():
            print(f"Error: Input file not found: {args.input}", file=sys.stderr)
            sys.exit(1)

        if not input_path.is_file():
            print(f"Error: Path is not a file: {args.input}", file=sys.stderr)
            sys.exit(1)

        # Read input content
        if args.verbose:
            print(f"Reading input file: {args.input}", file=sys.stderr)

        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                system_config = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in input file: {e}", file=sys.stderr)
            sys.exit(1)
        except UnicodeDecodeError:
            print(f"Error: Unable to read file as UTF-8 text: {args.input}", file=sys.stderr)
            sys.exit(1)

        # Validate system_config has name
        if 'name' not in system_config:
            system_config['name'] = 'System'  # Set default if missing

        if args.verbose:
            system_name = system_config.get('name', 'System')
            print(f"Analyzing technical debt for {system_name}...", file=sys.stderr)

        # Process data
        if args.output == 'csv':
            output = format_csv_output(system_config)
        elif args.output == 'json':
            output = format_json_output(system_config)
        else:  # text (default)
            output = analyze_technical_debt(system_config)

        # Write output to file or stdout
        if args.file:
            try:
                output_path = Path(args.file)
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(output)

                if args.verbose:
                    print(f"Results written to: {args.file}", file=sys.stderr)
                else:
                    print(f"Output saved to: {args.file}")

            except PermissionError:
                print(f"Error: Permission denied writing to: {args.file}", file=sys.stderr)
                sys.exit(4)
            except Exception as e:
                print(f"Error writing output file: {e}", file=sys.stderr)
                sys.exit(4)
        else:
            # Print to stdout
            print(output)

        # Success
        sys.exit(0)

    except FileNotFoundError as e:
        print(f"Error: File not found: {e}", file=sys.stderr)
        sys.exit(1)

    except PermissionError as e:
        print(f"Error: Permission denied: {e}", file=sys.stderr)
        sys.exit(1)

    except ValueError as e:
        print(f"Error: Invalid input: {e}", file=sys.stderr)
        sys.exit(3)

    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        sys.exit(130)

    except Exception as e:
        print(f"Error: Unexpected error occurred: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
