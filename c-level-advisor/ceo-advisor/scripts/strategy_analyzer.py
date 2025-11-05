#!/usr/bin/env python3
"""
Strategic Planning Analyzer - Comprehensive business strategy assessment tool

This tool helps CEOs and business leaders perform comprehensive strategic analysis
using multiple frameworks (SWOT, Porter's Five Forces, BCG Matrix) with actionable
recommendations and implementation roadmaps.

Usage:
    python strategy_analyzer.py company_data.json
    python strategy_analyzer.py company_data.json --output json
    python strategy_analyzer.py company_data.json -o json -f strategy_report.json

Author: claude-skills
Version: 2.0.0
Last Updated: 2025-11-05
"""

import argparse
import json
import math
import sys
import csv
from io import StringIO
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime, timedelta

class StrategyAnalyzer:
    def __init__(self):
        self.strategic_pillars = {
            'market_position': {
                'weight': 0.25,
                'factors': ['market_share', 'brand_strength', 'competitive_advantage', 'customer_loyalty']
            },
            'financial_health': {
                'weight': 0.25,
                'factors': ['revenue_growth', 'profitability', 'cash_flow', 'unit_economics']
            },
            'operational_excellence': {
                'weight': 0.20,
                'factors': ['efficiency', 'quality', 'scalability', 'innovation']
            },
            'organizational_capability': {
                'weight': 0.20,
                'factors': ['talent', 'culture', 'leadership', 'agility']
            },
            'growth_potential': {
                'weight': 0.10,
                'factors': ['market_size', 'expansion_opportunities', 'product_pipeline', 'partnerships']
            }
        }
        
        self.strategic_frameworks = {
            'porter_five_forces': [
                'competitive_rivalry',
                'supplier_power', 
                'buyer_power',
                'threat_of_substitution',
                'threat_of_new_entry'
            ],
            'swot': ['strengths', 'weaknesses', 'opportunities', 'threats'],
            'bcg_matrix': ['stars', 'cash_cows', 'question_marks', 'dogs'],
            'ansoff_matrix': ['market_penetration', 'market_development', 'product_development', 'diversification']
        }
    
    def analyze_strategic_position(self, company_data: Dict) -> Dict:
        """Comprehensive strategic analysis"""
        results = {
            'timestamp': datetime.now().isoformat(),
            'company': company_data.get('name', 'Company'),
            'strategic_health_score': 0,
            'pillar_analysis': {},
            'framework_analysis': {},
            'strategic_options': [],
            'risk_assessment': {},
            'recommendations': [],
            'roadmap': {}
        }
        
        # Analyze strategic pillars
        total_score = 0
        for pillar, config in self.strategic_pillars.items():
            pillar_score = self._analyze_pillar(
                company_data.get(pillar, {}),
                config['factors']
            )
            weighted_score = pillar_score * config['weight']
            results['pillar_analysis'][pillar] = {
                'score': pillar_score,
                'weighted_score': weighted_score,
                'level': self._get_level(pillar_score),
                'factors': self._get_pillar_details(company_data.get(pillar, {}), config['factors'])
            }
            total_score += weighted_score
        
        results['strategic_health_score'] = round(total_score, 1)
        
        # Framework analysis
        results['framework_analysis'] = self._apply_frameworks(company_data)
        
        # Generate strategic options
        results['strategic_options'] = self._generate_strategic_options(
            results['pillar_analysis'],
            company_data.get('context', {})
        )
        
        # Risk assessment
        results['risk_assessment'] = self._assess_strategic_risks(
            company_data,
            results['strategic_options']
        )
        
        # Generate roadmap
        results['roadmap'] = self._create_strategic_roadmap(
            results['strategic_options'],
            company_data.get('timeline', 12)
        )
        
        # Generate recommendations
        results['recommendations'] = self._generate_recommendations(results)
        
        return results
    
    def _analyze_pillar(self, pillar_data: Dict, factors: List) -> float:
        """Analyze a strategic pillar"""
        if not pillar_data:
            return 50.0
        
        total_score = 0
        count = 0
        
        for factor in factors:
            if factor in pillar_data:
                score = pillar_data[factor]
                total_score += score
                count += 1
        
        return (total_score / count) if count > 0 else 50.0
    
    def _get_pillar_details(self, pillar_data: Dict, factors: List) -> List[Dict]:
        """Get detailed factor analysis"""
        details = []
        
        for factor in factors:
            score = pillar_data.get(factor, 50)
            details.append({
                'factor': factor.replace('_', ' ').title(),
                'score': score,
                'status': 'Strong' if score >= 70 else 'Adequate' if score >= 40 else 'Weak'
            })
        
        return details
    
    def _get_level(self, score: float) -> str:
        """Convert score to level"""
        if score >= 80:
            return 'Excellent'
        elif score >= 70:
            return 'Strong'
        elif score >= 50:
            return 'Adequate'
        elif score >= 30:
            return 'Weak'
        else:
            return 'Critical'
    
    def _apply_frameworks(self, company_data: Dict) -> Dict:
        """Apply strategic frameworks"""
        frameworks = {}
        
        # SWOT Analysis
        swot_data = company_data.get('swot', {})
        frameworks['swot'] = {
            'strengths': swot_data.get('strengths', [
                'Strong brand recognition',
                'Experienced leadership team',
                'Robust technology platform'
            ]),
            'weaknesses': swot_data.get('weaknesses', [
                'Limited geographic presence',
                'High customer acquisition cost',
                'Technical debt'
            ]),
            'opportunities': swot_data.get('opportunities', [
                'Growing market demand',
                'M&A opportunities',
                'New product categories'
            ]),
            'threats': swot_data.get('threats', [
                'Increasing competition',
                'Regulatory changes',
                'Economic uncertainty'
            ])
        }
        
        # Porter's Five Forces
        forces = company_data.get('competitive_forces', {})
        frameworks['porter_analysis'] = {
            'competitive_rivalry': forces.get('rivalry', 70),
            'supplier_power': forces.get('suppliers', 40),
            'buyer_power': forces.get('buyers', 60),
            'threat_of_substitutes': forces.get('substitutes', 50),
            'threat_of_new_entrants': forces.get('new_entrants', 45),
            'overall_attractiveness': self._calculate_industry_attractiveness(forces)
        }
        
        # BCG Matrix for product portfolio
        products = company_data.get('products', [])
        frameworks['portfolio_analysis'] = self._analyze_portfolio(products)
        
        return frameworks
    
    def _calculate_industry_attractiveness(self, forces: Dict) -> float:
        """Calculate industry attractiveness from Porter's forces"""
        # Lower forces = more attractive industry
        rivalry = 100 - forces.get('rivalry', 50)
        supplier = 100 - forces.get('suppliers', 50)
        buyer = 100 - forces.get('buyers', 50)
        substitutes = 100 - forces.get('substitutes', 50)
        new_entrants = 100 - forces.get('new_entrants', 50)
        
        avg = (rivalry + supplier + buyer + substitutes + new_entrants) / 5
        return round(avg, 1)
    
    def _analyze_portfolio(self, products: List) -> Dict:
        """Analyze product portfolio using BCG matrix"""
        portfolio = {
            'stars': [],
            'cash_cows': [],
            'question_marks': [],
            'dogs': []
        }
        
        for product in products:
            growth = product.get('market_growth', 0)
            share = product.get('market_share', 0)
            
            if growth > 10 and share > 50:
                portfolio['stars'].append(product.get('name', 'Product'))
            elif growth <= 10 and share > 50:
                portfolio['cash_cows'].append(product.get('name', 'Product'))
            elif growth > 10 and share <= 50:
                portfolio['question_marks'].append(product.get('name', 'Product'))
            else:
                portfolio['dogs'].append(product.get('name', 'Product'))
        
        return portfolio
    
    def _generate_strategic_options(self, pillar_analysis: Dict, context: Dict) -> List[Dict]:
        """Generate strategic options based on analysis"""
        options = []
        
        # Check market position
        market_score = pillar_analysis['market_position']['score']
        if market_score < 60:
            options.append({
                'name': 'Market Leadership Initiative',
                'type': 'market_penetration',
                'description': 'Aggressive market share capture through competitive pricing and marketing',
                'investment': 'High',
                'timeframe': '12-18 months',
                'expected_impact': 'Increase market share by 10-15%',
                'priority': 9
            })
        
        # Check financial health
        financial_score = pillar_analysis['financial_health']['score']
        if financial_score < 50:
            options.append({
                'name': 'Profitability Turnaround',
                'type': 'operational_excellence',
                'description': 'Cost reduction and revenue optimization program',
                'investment': 'Medium',
                'timeframe': '6-9 months',
                'expected_impact': 'Improve margins by 5-8%',
                'priority': 10
            })
        
        # Check growth potential
        growth_score = pillar_analysis['growth_potential']['score']
        if growth_score > 70:
            options.append({
                'name': 'Expansion Strategy',
                'type': 'market_development',
                'description': 'Enter new geographic markets or customer segments',
                'investment': 'High',
                'timeframe': '18-24 months',
                'expected_impact': 'Revenue growth of 30-40%',
                'priority': 8
            })
        
        # Innovation opportunities
        if context.get('industry_disruption', False):
            options.append({
                'name': 'Digital Transformation',
                'type': 'innovation',
                'description': 'Comprehensive digitalization of business processes and customer experience',
                'investment': 'Very High',
                'timeframe': '24-36 months',
                'expected_impact': 'Future-proof business model',
                'priority': 9
            })
        
        # M&A opportunities
        if context.get('cash_available', 0) > 100000000:
            options.append({
                'name': 'Strategic Acquisition',
                'type': 'acquisition',
                'description': 'Acquire complementary businesses or competitors',
                'investment': 'Very High',
                'timeframe': '6-12 months',
                'expected_impact': 'Instant scale and capability',
                'priority': 7
            })
        
        # Sort by priority
        options.sort(key=lambda x: x['priority'], reverse=True)
        
        return options[:5]  # Top 5 strategic options
    
    def _assess_strategic_risks(self, company_data: Dict, strategic_options: List) -> Dict:
        """Assess strategic risks"""
        risks = {
            'execution_risk': self._calculate_execution_risk(company_data),
            'market_risk': self._calculate_market_risk(company_data),
            'financial_risk': self._calculate_financial_risk(company_data),
            'competitive_risk': self._calculate_competitive_risk(company_data),
            'regulatory_risk': company_data.get('regulatory_risk', 30),
            'overall_risk': 0,
            'mitigation_strategies': []
        }
        
        # Calculate overall risk
        risk_values = [
            risks['execution_risk'],
            risks['market_risk'],
            risks['financial_risk'],
            risks['competitive_risk'],
            risks['regulatory_risk']
        ]
        risks['overall_risk'] = sum(risk_values) / len(risk_values)
        
        # Generate mitigation strategies
        if risks['execution_risk'] > 60:
            risks['mitigation_strategies'].append({
                'risk': 'Execution',
                'strategy': 'Strengthen PMO, hire experienced executives, implement OKRs'
            })
        
        if risks['market_risk'] > 60:
            risks['mitigation_strategies'].append({
                'risk': 'Market',
                'strategy': 'Diversify revenue streams, build strategic partnerships'
            })
        
        if risks['financial_risk'] > 60:
            risks['mitigation_strategies'].append({
                'risk': 'Financial',
                'strategy': 'Improve cash management, secure credit facilities, optimize working capital'
            })
        
        return risks
    
    def _calculate_execution_risk(self, data: Dict) -> float:
        """Calculate execution risk"""
        org_capability = data.get('organizational_capability', {})
        
        factors = [
            100 - org_capability.get('leadership', 50),
            100 - org_capability.get('talent', 50),
            100 - org_capability.get('agility', 50),
            data.get('complexity_score', 50)
        ]
        
        return sum(factors) / len(factors)
    
    def _calculate_market_risk(self, data: Dict) -> float:
        """Calculate market risk"""
        market = data.get('market_position', {})
        
        factors = [
            100 - market.get('market_share', 50),
            data.get('market_volatility', 50),
            data.get('customer_concentration', 50)
        ]
        
        return sum(factors) / len(factors)
    
    def _calculate_financial_risk(self, data: Dict) -> float:
        """Calculate financial risk"""
        financial = data.get('financial_health', {})
        
        factors = [
            100 - financial.get('cash_flow', 50),
            100 - financial.get('profitability', 50),
            data.get('debt_ratio', 50),
            data.get('burn_rate', 50) if 'burn_rate' in data else 30
        ]
        
        return sum(factors) / len(factors)
    
    def _calculate_competitive_risk(self, data: Dict) -> float:
        """Calculate competitive risk"""
        forces = data.get('competitive_forces', {})
        
        return (forces.get('rivalry', 50) + forces.get('new_entrants', 50)) / 2
    
    def _create_strategic_roadmap(self, options: List, timeline_months: int) -> Dict:
        """Create implementation roadmap"""
        roadmap = {
            'phases': [],
            'milestones': [],
            'resource_requirements': {},
            'success_metrics': []
        }
        
        # Define phases
        phases = [
            {
                'phase': 'Foundation',
                'months': '0-3',
                'focus': 'Build capabilities and quick wins',
                'initiatives': []
            },
            {
                'phase': 'Acceleration',
                'months': '3-9',
                'focus': 'Execute core strategies',
                'initiatives': []
            },
            {
                'phase': 'Scale',
                'months': '9-18',
                'focus': 'Expand and optimize',
                'initiatives': []
            },
            {
                'phase': 'Transform',
                'months': '18+',
                'focus': 'Long-term transformation',
                'initiatives': []
            }
        ]
        
        # Assign initiatives to phases
        for i, option in enumerate(options[:4]):
            if i == 0:
                phases[0]['initiatives'].append(option['name'])
            elif i == 1:
                phases[1]['initiatives'].append(option['name'])
            elif i == 2:
                phases[2]['initiatives'].append(option['name'])
            else:
                phases[3]['initiatives'].append(option['name'])
        
        roadmap['phases'] = phases
        
        # Define key milestones
        roadmap['milestones'] = [
            {'month': 3, 'milestone': 'Complete foundation phase', 'success_criteria': 'Core team hired, processes defined'},
            {'month': 6, 'milestone': 'First major initiative launch', 'success_criteria': 'KPIs showing positive trend'},
            {'month': 12, 'milestone': 'Strategic review', 'success_criteria': 'ROI demonstrated, strategy validated'},
            {'month': 18, 'milestone': 'Scale achievement', 'success_criteria': 'Market position improved, financial targets met'}
        ]
        
        # Resource requirements
        roadmap['resource_requirements'] = {
            'leadership': 'C-suite alignment and commitment',
            'financial': '$X million investment over 18 months',
            'human': 'Additional 20-30 FTEs across functions',
            'technology': 'Platform upgrades and new tools',
            'external': 'Consultants and advisors as needed'
        }
        
        # Success metrics
        roadmap['success_metrics'] = [
            'Revenue growth: 25% YoY',
            'Market share: +5 percentage points',
            'EBITDA margin: +8 percentage points',
            'Customer NPS: >70',
            'Employee engagement: >80%'
        ]
        
        return roadmap
    
    def _generate_recommendations(self, results: Dict) -> List[str]:
        """Generate strategic recommendations"""
        recommendations = []
        
        # Based on overall score
        score = results['strategic_health_score']
        if score < 40:
            recommendations.append('🚨 URGENT: Immediate turnaround required - consider bringing in crisis management team')
            recommendations.append('Focus on cash preservation and core business stabilization')
        elif score < 60:
            recommendations.append('⚠️ Strategic repositioning needed - prioritize 2-3 key initiatives')
            recommendations.append('Strengthen weak pillars before pursuing growth')
        elif score < 80:
            recommendations.append('✓ Solid position - focus on selective improvements and growth')
            recommendations.append('Invest in innovation and market expansion')
        else:
            recommendations.append('⭐ Excellent position - maintain momentum and explore bold moves')
            recommendations.append('Consider industry disruption or category creation')
        
        # Based on specific weaknesses
        for pillar, analysis in results['pillar_analysis'].items():
            if analysis['score'] < 50:
                if pillar == 'market_position':
                    recommendations.append(f'Strengthen {pillar}: Launch competitive differentiation program')
                elif pillar == 'financial_health':
                    recommendations.append(f'Improve {pillar}: Implement profitability improvement plan')
                elif pillar == 'organizational_capability':
                    recommendations.append(f'Build {pillar}: Invest in talent and culture transformation')
        
        # Based on opportunities
        if results['framework_analysis']['porter_analysis']['overall_attractiveness'] > 70:
            recommendations.append('Industry is attractive - consider aggressive expansion')
        
        # Risk-based recommendations
        if results['risk_assessment']['overall_risk'] > 60:
            recommendations.append('High risk profile - implement comprehensive risk management')
        
        return recommendations

def analyze_strategy(company_data: Dict) -> str:
    """Main function to analyze strategy"""
    analyzer = StrategyAnalyzer()
    results = analyzer.analyze_strategic_position(company_data)

    # Format output
    output = [
        f"=== Strategic Analysis Report ===",
        f"Company: {results['company']}",
        f"Date: {results['timestamp'][:10]}",
        f"",
        f"STRATEGIC HEALTH SCORE: {results['strategic_health_score']}/100",
        f"",
        "Strategic Pillars:"
    ]

    for pillar, analysis in results['pillar_analysis'].items():
        output.append(f"  {pillar.replace('_', ' ').title()}: {analysis['score']:.1f} ({analysis['level']})")
        for factor in analysis['factors'][:2]:  # Show top 2 factors
            output.append(f"    • {factor['factor']}: {factor['status']}")

    output.extend([
        f"",
        "Strategic Options:"
    ])

    for i, option in enumerate(results['strategic_options'][:3], 1):
        output.append(f"\n{i}. {option['name']} (Priority: {option['priority']}/10)")
        output.append(f"   Type: {option['type']}")
        output.append(f"   Investment: {option['investment']}")
        output.append(f"   Timeframe: {option['timeframe']}")
        output.append(f"   Impact: {option['expected_impact']}")

    output.extend([
        f"",
        f"Risk Assessment:",
        f"  Overall Risk: {results['risk_assessment']['overall_risk']:.1f}%",
        f"  Execution Risk: {results['risk_assessment']['execution_risk']:.1f}%",
        f"  Market Risk: {results['risk_assessment']['market_risk']:.1f}%",
        f"  Financial Risk: {results['risk_assessment']['financial_risk']:.1f}%",
        f"",
        "Strategic Roadmap:"
    ])

    for phase in results['roadmap']['phases'][:3]:
        output.append(f"  {phase['phase']} ({phase['months']}): {phase['focus']}")
        for initiative in phase['initiatives']:
            output.append(f"    • {initiative}")

    output.extend([
        f"",
        "Key Recommendations:"
    ])

    for rec in results['recommendations'][:5]:
        output.append(f"  • {rec}")

    return '\n'.join(output)


def format_csv_output(company_data: Dict) -> str:
    """Format strategic analysis results as CSV"""
    analyzer = StrategyAnalyzer()
    results = analyzer.analyze_strategic_position(company_data)

    output = StringIO()
    writer = csv.writer(output)

    # Header row - pillar scores
    writer.writerow(['pillar', 'score', 'weighted_score', 'level', 'status'])

    # Write pillar analysis
    for pillar, data in results.get('pillar_analysis', {}).items():
        writer.writerow([
            pillar.replace('_', ' ').title(),
            data.get('score', 0),
            f"{data.get('weighted_score', 0):.2f}",
            data.get('level', 'Unknown'),
            'pass'
        ])

    # Summary rows
    writer.writerow(['', '', '', '', ''])
    writer.writerow(['STRATEGIC_HEALTH_SCORE', results.get('strategic_health_score', 0), '', 'pass', ''])

    return output.getvalue()

def format_json_output(company_data: Dict) -> str:
    """Format results as JSON with metadata"""
    analyzer = StrategyAnalyzer()
    results = analyzer.analyze_strategic_position(company_data)

    output = {
        "metadata": {
            "tool": "strategy_analyzer.py",
            "version": "2.0.0",
            "timestamp": datetime.now().isoformat()
        },
        "inputs": {
            "company_data": company_data
        },
        "results": results
    }

    return json.dumps(output, indent=2)


def main():
    """
    Main entry point with standardized argument parsing.

    Parses command-line arguments, validates input, performs strategic analysis,
    and writes output in the specified format.
    """
    parser = argparse.ArgumentParser(
        description='Comprehensive business strategy analysis with SWOT, Porter\'s Five Forces, BCG Matrix, and strategic roadmap',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic analysis with text output
  %(prog)s company_data.json

  # JSON output for board presentations
  %(prog)s company_data.json --output json

  # Save to file
  %(prog)s company_data.json -o json -f strategy_report.json

  # Verbose mode with detailed logging
  %(prog)s company_data.json -v

Input JSON Format:
  {
    "name": "TechCorp Inc.",
    "market_position": {
      "market_share": 35,
      "brand_strength": 65,
      "competitive_advantage": 70,
      "customer_loyalty": 60
    },
    "financial_health": {
      "revenue_growth": 45,
      "profitability": 40,
      "cash_flow": 55,
      "unit_economics": 60
    },
    "organizational_capability": {
      "talent": 70,
      "culture": 65,
      "leadership": 75,
      "agility": 60
    },
    "growth_potential": {
      "market_size": 80,
      "expansion_opportunities": 70,
      "product_pipeline": 60,
      "partnerships": 55
    },
    "competitive_forces": {
      "rivalry": 70,
      "suppliers": 40,
      "buyers": 60,
      "substitutes": 50,
      "new_entrants": 45
    },
    "context": {
      "industry_disruption": true,
      "cash_available": 150000000
    },
    "timeline": 18
  }

For more information, see:
c-level-advisor/ceo-advisor/SKILL.md
        """
    )

    # Positional arguments
    parser.add_argument(
        'input',
        help='JSON file with company strategic data'
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
                company_data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in input file: {e}", file=sys.stderr)
            sys.exit(1)
        except UnicodeDecodeError:
            print(f"Error: Unable to read file as UTF-8 text: {args.input}", file=sys.stderr)
            sys.exit(1)

        # Validate company_data has name
        if 'name' not in company_data:
            company_data['name'] = 'Company'  # Set default if missing

        if args.verbose:
            print(f"Analyzing strategic position for {company_data.get('name', 'Company')}...", file=sys.stderr)

        # Process data
        if args.output == 'csv':
            output = format_csv_output(company_data)
        elif args.output == 'json':
            output = format_json_output(company_data)
        else:  # text (default)
            output = analyze_strategy(company_data)

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
