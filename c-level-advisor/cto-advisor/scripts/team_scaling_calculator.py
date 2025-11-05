#!/usr/bin/env python3
"""
Engineering Team Scaling Calculator - Optimize team growth and structure

This tool helps CTOs and engineering leaders plan optimal team scaling strategies,
including hiring plans, budget projections, and organizational structure design.

Usage:
    python team_scaling_calculator.py team_data.json
    python team_scaling_calculator.py team_data.json --output json
    python team_scaling_calculator.py team_data.json -o json -f report.json

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

class TeamScalingCalculator:
    def __init__(self):
        self.conway_factor = 1.5  # Conway's Law impact factor
        self.brooks_factor = 0.75  # Brooks' Law diminishing returns
        
        # Optimal team structures based on size
        self.team_structures = {
            'startup': {'min': 1, 'max': 10, 'structure': 'flat'},
            'growth': {'min': 11, 'max': 50, 'structure': 'team_leads'},
            'scale': {'min': 51, 'max': 150, 'structure': 'departments'},
            'enterprise': {'min': 151, 'max': 9999, 'structure': 'divisions'}
        }
        
        # Role ratios for balanced teams
        self.role_ratios = {
            'engineering_manager': 0.125,  # 1:8 ratio
            'tech_lead': 0.167,  # 1:6 ratio
            'senior_engineer': 0.3,
            'mid_engineer': 0.4,
            'junior_engineer': 0.2,
            'devops': 0.1,
            'qa': 0.15,
            'product_manager': 0.1,
            'designer': 0.08,
            'data_engineer': 0.05
        }
    
    def calculate_scaling_plan(self, current_state: Dict, growth_targets: Dict) -> Dict:
        """Calculate optimal scaling plan"""
        results = {
            'current_analysis': self._analyze_current_state(current_state),
            'growth_timeline': self._create_growth_timeline(current_state, growth_targets),
            'hiring_plan': {},
            'team_structure': {},
            'budget_projection': {},
            'risk_factors': [],
            'recommendations': []
        }
        
        # Generate hiring plan
        results['hiring_plan'] = self._generate_hiring_plan(
            current_state,
            growth_targets
        )
        
        # Design team structure
        results['team_structure'] = self._design_team_structure(
            growth_targets['target_headcount']
        )
        
        # Calculate budget
        results['budget_projection'] = self._calculate_budget(
            results['hiring_plan'],
            current_state.get('location', 'US')
        )
        
        # Assess risks
        results['risk_factors'] = self._assess_scaling_risks(
            current_state,
            growth_targets
        )
        
        # Generate recommendations
        results['recommendations'] = self._generate_recommendations(results)
        
        return results
    
    def _analyze_current_state(self, current_state: Dict) -> Dict:
        """Analyze current team state"""
        total_engineers = current_state.get('headcount', 0)
        
        analysis = {
            'total_headcount': total_engineers,
            'team_stage': self._get_team_stage(total_engineers),
            'productivity_index': 0,
            'balance_score': 0,
            'issues': []
        }
        
        # Calculate productivity index
        if total_engineers > 0:
            velocity = current_state.get('velocity', 100)
            expected_velocity = total_engineers * 20  # baseline 20 points per engineer
            analysis['productivity_index'] = (velocity / expected_velocity) * 100
        
        # Check team balance
        roles = current_state.get('roles', {})
        analysis['balance_score'] = self._calculate_balance_score(roles, total_engineers)
        
        # Identify issues
        if analysis['productivity_index'] < 70:
            analysis['issues'].append('Low productivity - possible process or tooling issues')
        
        if analysis['balance_score'] < 60:
            analysis['issues'].append('Team imbalance - review role distribution')
        
        manager_ratio = roles.get('managers', 0) / max(total_engineers, 1)
        if manager_ratio > 0.2:
            analysis['issues'].append('Over-managed - too many managers')
        elif manager_ratio < 0.08 and total_engineers > 20:
            analysis['issues'].append('Under-managed - need more engineering managers')
        
        return analysis
    
    def _get_team_stage(self, headcount: int) -> str:
        """Determine team stage based on size"""
        for stage, config in self.team_structures.items():
            if config['min'] <= headcount <= config['max']:
                return stage
        return 'startup'
    
    def _calculate_balance_score(self, roles: Dict, total: int) -> float:
        """Calculate team balance score"""
        if total == 0:
            return 0
        
        score = 100
        ideal_ratios = self.role_ratios
        
        for role, ideal_ratio in ideal_ratios.items():
            actual_count = roles.get(role, 0)
            actual_ratio = actual_count / total
            
            # Penalize deviation from ideal ratio
            deviation = abs(actual_ratio - ideal_ratio)
            penalty = deviation * 100
            score -= min(penalty, 20)  # Max 20 point penalty per role
        
        return max(0, score)
    
    def _create_growth_timeline(self, current: Dict, targets: Dict) -> List[Dict]:
        """Create quarterly growth timeline"""
        current_headcount = current.get('headcount', 0)
        target_headcount = targets.get('target_headcount', current_headcount)
        timeline_quarters = targets.get('timeline_quarters', 4)
        
        growth_needed = target_headcount - current_headcount
        timeline = []
        
        for quarter in range(1, timeline_quarters + 1):
            # Apply Brooks' Law - diminishing returns with rapid growth
            if quarter == 1:
                quarterly_growth = math.ceil(growth_needed * 0.4)  # Front-load hiring
            else:
                remaining_growth = target_headcount - current_headcount
                quarters_left = timeline_quarters - quarter + 1
                quarterly_growth = math.ceil(remaining_growth / quarters_left)
            
            # Adjust for onboarding capacity
            max_onboarding = math.ceil(current_headcount * 0.25)  # 25% growth per quarter max
            quarterly_growth = min(quarterly_growth, max_onboarding)
            
            current_headcount += quarterly_growth
            
            timeline.append({
                'quarter': f'Q{quarter}',
                'headcount': current_headcount,
                'new_hires': quarterly_growth,
                'onboarding_capacity': max_onboarding,
                'productivity_factor': 1.0 - (0.2 * (quarterly_growth / max(current_headcount, 1)))
            })
        
        return timeline
    
    def _generate_hiring_plan(self, current: Dict, targets: Dict) -> Dict:
        """Generate detailed hiring plan"""
        current_roles = current.get('roles', {})
        target_headcount = targets.get('target_headcount', 0)
        
        hiring_plan = {
            'total_hires_needed': target_headcount - current.get('headcount', 0),
            'by_role': {},
            'by_quarter': {},
            'interview_capacity_needed': 0,
            'recruiting_resources': 0
        }
        
        # Calculate ideal role distribution
        for role, ideal_ratio in self.role_ratios.items():
            ideal_count = math.ceil(target_headcount * ideal_ratio)
            current_count = current_roles.get(role, 0)
            hires_needed = max(0, ideal_count - current_count)
            
            if hires_needed > 0:
                hiring_plan['by_role'][role] = {
                    'current': current_count,
                    'target': ideal_count,
                    'hires_needed': hires_needed,
                    'priority': self._get_role_priority(role, current_roles, target_headcount)
                }
        
        # Distribute hires across quarters
        timeline = self._create_growth_timeline(current, targets)
        for quarter_data in timeline:
            quarter = quarter_data['quarter']
            hires = quarter_data['new_hires']
            
            hiring_plan['by_quarter'][quarter] = {
                'total_hires': hires,
                'breakdown': self._distribute_quarterly_hires(hires, hiring_plan['by_role'])
            }
        
        # Calculate interview capacity (5 interviews per hire average)
        hiring_plan['interview_capacity_needed'] = hiring_plan['total_hires_needed'] * 5
        
        # Calculate recruiting resources (1 recruiter per 50 hires/year)
        annual_hires = hiring_plan['total_hires_needed'] * (4 / max(targets.get('timeline_quarters', 4), 1))
        hiring_plan['recruiting_resources'] = math.ceil(annual_hires / 50)
        
        return hiring_plan
    
    def _get_role_priority(self, role: str, current_roles: Dict, target_size: int) -> int:
        """Determine hiring priority for a role"""
        # Priority based on criticality and current gaps
        priorities = {
            'engineering_manager': 10 if target_size > 20 else 5,
            'tech_lead': 9,
            'senior_engineer': 8,
            'devops': 7 if current_roles.get('devops', 0) == 0 else 5,
            'qa': 6,
            'mid_engineer': 5,
            'product_manager': 6,
            'designer': 5,
            'data_engineer': 4,
            'junior_engineer': 3
        }
        
        return priorities.get(role, 5)
    
    def _distribute_quarterly_hires(self, total_hires: int, role_needs: Dict) -> Dict:
        """Distribute quarterly hires across roles"""
        distribution = {}
        
        # Sort roles by priority
        sorted_roles = sorted(
            role_needs.items(),
            key=lambda x: x[1]['priority'],
            reverse=True
        )
        
        remaining_hires = total_hires
        
        for role, needs in sorted_roles:
            if remaining_hires <= 0:
                break
            
            hires = min(needs['hires_needed'], max(1, remaining_hires // 3))
            distribution[role] = hires
            remaining_hires -= hires
        
        return distribution
    
    def _design_team_structure(self, target_headcount: int) -> Dict:
        """Design optimal team structure"""
        stage = self._get_team_stage(target_headcount)
        structure = {
            'organizational_model': self.team_structures[stage]['structure'],
            'teams': [],
            'reporting_structure': {},
            'communication_paths': 0
        }
        
        if stage == 'startup':
            structure['teams'] = [{
                'name': 'Core Team',
                'size': target_headcount,
                'focus': 'Full-stack'
            }]
            
        elif stage == 'growth':
            # Create 2-4 teams
            team_size = 6
            num_teams = math.ceil(target_headcount / team_size)
            
            structure['teams'] = [
                {
                    'name': f'Team {i+1}',
                    'size': team_size,
                    'focus': ['Platform', 'Product', 'Infrastructure', 'Growth'][i % 4]
                }
                for i in range(num_teams)
            ]
            
        elif stage == 'scale':
            # Create departments with multiple teams
            structure['departments'] = [
                {'name': 'Platform', 'teams': 3, 'headcount': target_headcount * 0.3},
                {'name': 'Product', 'teams': 4, 'headcount': target_headcount * 0.4},
                {'name': 'Infrastructure', 'teams': 2, 'headcount': target_headcount * 0.2},
                {'name': 'Data', 'teams': 1, 'headcount': target_headcount * 0.1}
            ]
        
        # Calculate communication paths (n*(n-1)/2)
        structure['communication_paths'] = (target_headcount * (target_headcount - 1)) // 2
        
        # Add management layers
        structure['management_layers'] = math.ceil(math.log(target_headcount, 7))
        
        return structure
    
    def _calculate_budget(self, hiring_plan: Dict, location: str) -> Dict:
        """Calculate budget projection"""
        # Average salaries by role and location (in USD)
        us_salaries = {
            'engineering_manager': 200000,
            'tech_lead': 180000,
            'senior_engineer': 160000,
            'mid_engineer': 120000,
            'junior_engineer': 85000,
            'devops': 150000,
            'qa': 100000,
            'product_manager': 150000,
            'designer': 120000,
            'data_engineer': 140000
        }

        salary_bands = {
            'US': us_salaries,
            'EU': {k: v * 0.8 for k, v in us_salaries.items()},
            'APAC': {k: v * 0.6 for k, v in us_salaries.items()}
        }
        
        location_salaries = salary_bands.get(location, salary_bands['US'])
        
        budget = {
            'annual_salary_cost': 0,
            'benefits_cost': 0,  # 30% of salary
            'equipment_cost': 0,  # $5k per hire
            'recruiting_cost': 0,  # 20% of first-year salary
            'onboarding_cost': 0,  # $10k per hire
            'total_cost': 0,
            'cost_per_hire': 0
        }
        
        for role, details in hiring_plan['by_role'].items():
            hires = details['hires_needed']
            salary = location_salaries.get(role, 100000)
            
            budget['annual_salary_cost'] += hires * salary
            budget['recruiting_cost'] += hires * salary * 0.2
        
        budget['benefits_cost'] = budget['annual_salary_cost'] * 0.3
        budget['equipment_cost'] = hiring_plan['total_hires_needed'] * 5000
        budget['onboarding_cost'] = hiring_plan['total_hires_needed'] * 10000
        
        budget['total_cost'] = sum([
            budget['annual_salary_cost'],
            budget['benefits_cost'],
            budget['equipment_cost'],
            budget['recruiting_cost'],
            budget['onboarding_cost']
        ])
        
        if hiring_plan['total_hires_needed'] > 0:
            budget['cost_per_hire'] = budget['total_cost'] / hiring_plan['total_hires_needed']
        
        return budget
    
    def _assess_scaling_risks(self, current: Dict, targets: Dict) -> List[Dict]:
        """Assess risks in scaling plan"""
        risks = []
        
        growth_rate = (targets['target_headcount'] - current['headcount']) / max(current['headcount'], 1)
        
        if growth_rate > 1.0:  # More than 100% growth
            risks.append({
                'risk': 'Rapid growth dilution',
                'impact': 'High',
                'mitigation': 'Implement strong onboarding and mentorship programs'
            })
        
        if current.get('attrition_rate', 0) > 15:
            risks.append({
                'risk': 'High attrition during scaling',
                'impact': 'High',
                'mitigation': 'Address retention issues before aggressive hiring'
            })
        
        if targets.get('timeline_quarters', 4) < 4:
            risks.append({
                'risk': 'Compressed timeline',
                'impact': 'Medium',
                'mitigation': 'Consider extending timeline or increasing recruiting resources'
            })
        
        return risks
    
    def _generate_recommendations(self, results: Dict) -> List[str]:
        """Generate scaling recommendations"""
        recommendations = []
        
        # Based on growth rate
        total_hires = results['hiring_plan']['total_hires_needed']
        current_size = results['current_analysis']['total_headcount']
        
        if current_size > 0:
            growth_rate = total_hires / current_size
            
            if growth_rate > 0.5:
                recommendations.append('Consider hiring a dedicated recruiting team')
                recommendations.append('Implement scalable onboarding processes')
                recommendations.append('Establish clear team charters and boundaries')
            
            if growth_rate > 1.0:
                recommendations.append('⚠️ High growth risk - consider slowing timeline')
                recommendations.append('Focus on senior hires first to establish culture')
                recommendations.append('Implement continuous integration practices early')
        
        # Based on structure
        if results['team_structure']['communication_paths'] > 1000:
            recommendations.append('Implement clear communication channels and tools')
            recommendations.append('Consider platform teams to reduce dependencies')
        
        # Based on balance
        if results['current_analysis']['balance_score'] < 70:
            recommendations.append('Prioritize hiring for underrepresented roles')
            recommendations.append('Consider role rotation for skill development')
        
        return recommendations

def calculate_team_scaling(current_state: Dict, growth_targets: Dict) -> str:
    """Main function to calculate team scaling"""
    calculator = TeamScalingCalculator()
    results = calculator.calculate_scaling_plan(current_state, growth_targets)

    # Format output
    output = [
        "=== Engineering Team Scaling Plan ===",
        f"",
        f"Current State Analysis:",
        f"  Current Headcount: {results['current_analysis']['total_headcount']}",
        f"  Team Stage: {results['current_analysis']['team_stage']}",
        f"  Productivity Index: {results['current_analysis']['productivity_index']:.1f}%",
        f"  Team Balance Score: {results['current_analysis']['balance_score']:.1f}/100",
        f"",
        f"Growth Plan:",
        f"  Target Headcount: {growth_targets['target_headcount']}",
        f"  Total Hires Needed: {results['hiring_plan']['total_hires_needed']}",
        f"  Timeline: {growth_targets['timeline_quarters']} quarters",
        f"",
        "Quarterly Timeline:"
    ]

    for quarter in results['growth_timeline']:
        output.append(
            f"  {quarter['quarter']}: {quarter['headcount']} total "
            f"(+{quarter['new_hires']} hires, "
            f"{quarter['productivity_factor']:.0%} productivity)"
        )

    output.extend([
        f"",
        "Hiring Priorities:"
    ])

    sorted_roles = sorted(
        results['hiring_plan']['by_role'].items(),
        key=lambda x: x[1]['priority'],
        reverse=True
    )

    for role, details in sorted_roles[:5]:
        output.append(
            f"  {role}: {details['hires_needed']} hires "
            f"(Priority: {details['priority']}/10)"
        )

    output.extend([
        f"",
        f"Budget Projection:",
        f"  Annual Salary Cost: ${results['budget_projection']['annual_salary_cost']:,.0f}",
        f"  Total Investment: ${results['budget_projection']['total_cost']:,.0f}",
        f"  Cost per Hire: ${results['budget_projection']['cost_per_hire']:,.0f}",
        f"",
        f"Team Structure:",
        f"  Model: {results['team_structure']['organizational_model']}",
        f"  Management Layers: {results['team_structure']['management_layers']}",
        f"  Communication Paths: {results['team_structure']['communication_paths']:,}",
        f"",
        "Key Recommendations:"
    ])

    for rec in results['recommendations']:
        output.append(f"  • {rec}")

    return '\n'.join(output)


def format_csv_output(results: Dict) -> str:
    """Format team_scaling results as CSV"""
    output = StringIO()
    writer = csv.writer(output)
    
    # Header row
    writer.writerow(['quarter', 'role', 'headcount', 'salary', 'total_comp', 'status'])
    
    # Write data rows
    if isinstance(results, dict) and 'growth_timeline' in results:
        for item in results.get('growth_timeline', [])[:20]:
            if isinstance(item, dict):
                writer.writerow([item.get(k, '') for k in ['quarter', 'role', 'headcount', 'salary', 'total_comp', 'status']])
    
    return output.getvalue()


def format_json_output(current_state: Dict, growth_targets: Dict) -> str:
    """Format results as JSON with metadata"""
    calculator = TeamScalingCalculator()
    results = calculator.calculate_scaling_plan(current_state, growth_targets)

    output = {
        "metadata": {
            "tool": "team_scaling_calculator.py",
            "version": "2.0.0",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        },
        "inputs": {
            "current_state": current_state,
            "growth_targets": growth_targets
        },
        "results": results
    }

    return json.dumps(output, indent=2)


def main():
    """
    Main entry point with standardized argument parsing.

    Parses command-line arguments, validates input, calculates team scaling,
    and writes output in the specified format.
    """
    parser = argparse.ArgumentParser(
        description='Calculate optimal engineering team scaling strategy with hiring plans and budget projections',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic analysis with text output
  %(prog)s team_data.json

  # JSON output for dashboards
  %(prog)s team_data.json --output json

  # Save to file
  %(prog)s team_data.json -o json -f scaling_plan.json

  # Verbose mode with detailed logging
  %(prog)s team_data.json -v

Input JSON Format:
  {
    "current_state": {
      "headcount": 25,
      "velocity": 450,
      "roles": {
        "engineering_manager": 2,
        "senior_engineer": 8,
        "mid_engineer": 10
      },
      "attrition_rate": 12,
      "location": "US"
    },
    "growth_targets": {
      "target_headcount": 75,
      "timeline_quarters": 4
    }
  }

For more information, see:
c-level-advisor/cto-advisor/SKILL.md
        """
    )

    # Positional arguments
    parser.add_argument(
        'input',
        help='JSON file with team data (current state and growth targets)'
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
                data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in input file: {e}", file=sys.stderr)
            sys.exit(1)
        except UnicodeDecodeError:
            print(f"Error: Unable to read file as UTF-8 text: {args.input}", file=sys.stderr)
            sys.exit(1)

        # Validate required fields
        if 'current_state' not in data:
            print("Error: Input JSON must contain 'current_state' object", file=sys.stderr)
            sys.exit(1)

        if 'growth_targets' not in data:
            print("Error: Input JSON must contain 'growth_targets' object", file=sys.stderr)
            sys.exit(1)

        current_state = data['current_state']
        growth_targets = data['growth_targets']

        # Validate required fields in current_state
        if 'headcount' not in current_state:
            print("Error: current_state must contain 'headcount' field", file=sys.stderr)
            sys.exit(1)

        # Validate required fields in growth_targets
        if 'target_headcount' not in growth_targets:
            print("Error: growth_targets must contain 'target_headcount' field", file=sys.stderr)
            sys.exit(1)

        if args.verbose:
            print(f"Calculating scaling plan from {current_state['headcount']} to {growth_targets['target_headcount']} headcount...", file=sys.stderr)

        # Process data
        if args.output == 'csv':
            output = format_csv_output(results)
        elif args.output == 'json':
            output = format_json_output(current_state, growth_targets)
        else:  # text (default)
            output = calculate_team_scaling(current_state, growth_targets)

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
