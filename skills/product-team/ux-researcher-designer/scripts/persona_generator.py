#!/usr/bin/env python3
"""
Data-Driven Persona Generator
Creates research-backed user personas from user data and interviews
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple
from collections import Counter, defaultdict
import random

class PersonaGenerator:
    """Generate data-driven personas from user research"""
    
    def __init__(self):
        self.persona_components = {
            'demographics': ['age', 'location', 'occupation', 'education', 'income'],
            'psychographics': ['goals', 'frustrations', 'motivations', 'values'],
            'behaviors': ['tech_savviness', 'usage_frequency', 'preferred_devices', 'key_activities'],
            'needs': ['functional', 'emotional', 'social']
        }
        
        self.archetype_templates = {
            'power_user': {
                'characteristics': ['tech-savvy', 'frequent user', 'early adopter', 'efficiency-focused'],
                'goals': ['maximize productivity', 'automate workflows', 'access advanced features'],
                'frustrations': ['slow performance', 'limited customization', 'lack of shortcuts'],
                'quote': "I need tools that can keep up with my workflow"
            },
            'casual_user': {
                'characteristics': ['occasional user', 'basic needs', 'prefers simplicity'],
                'goals': ['accomplish specific tasks', 'easy to use', 'minimal learning curve'],
                'frustrations': ['complexity', 'too many options', 'unclear navigation'],
                'quote': "I just want it to work without having to think about it"
            },
            'business_user': {
                'characteristics': ['professional context', 'ROI-focused', 'team collaboration'],
                'goals': ['improve team efficiency', 'track metrics', 'integrate with tools'],
                'frustrations': ['lack of reporting', 'poor collaboration features', 'no enterprise features'],
                'quote': "I need to show clear value to my stakeholders"
            },
            'mobile_first': {
                'characteristics': ['primarily mobile', 'on-the-go usage', 'quick interactions'],
                'goals': ['access anywhere', 'quick actions', 'offline capability'],
                'frustrations': ['poor mobile experience', 'desktop-only features', 'slow loading'],
                'quote': "My phone is my primary computing device"
            }
        }
    
    def generate_persona_from_data(self, user_data: List[Dict], 
                                  interview_insights: List[Dict] = None) -> Dict:
        """Generate persona from user data and optional interview insights"""
        
        # Analyze user data for patterns
        patterns = self._analyze_user_patterns(user_data)
        
        # Identify persona archetype
        archetype = self._identify_archetype(patterns)
        
        # Generate persona
        persona = {
            'name': self._generate_name(archetype),
            'archetype': archetype,
            'tagline': self._generate_tagline(patterns),
            'demographics': self._aggregate_demographics(user_data),
            'psychographics': self._extract_psychographics(patterns, interview_insights),
            'behaviors': self._analyze_behaviors(user_data),
            'needs_and_goals': self._identify_needs(patterns, interview_insights),
            'frustrations': self._extract_frustrations(patterns, interview_insights),
            'scenarios': self._generate_scenarios(archetype, patterns),
            'quote': self._select_quote(interview_insights, archetype),
            'data_points': self._calculate_data_points(user_data),
            'design_implications': self._derive_design_implications(patterns)
        }
        
        return persona
    
    def _analyze_user_patterns(self, user_data: List[Dict]) -> Dict:
        """Analyze patterns in user data"""
        
        patterns = {
            'usage_frequency': defaultdict(int),
            'feature_usage': defaultdict(int),
            'devices': defaultdict(int),
            'contexts': defaultdict(int),
            'pain_points': [],
            'success_metrics': []
        }
        
        for user in user_data:
            # Frequency patterns
            freq = user.get('usage_frequency', 'medium')
            patterns['usage_frequency'][freq] += 1
            
            # Feature usage
            for feature in user.get('features_used', []):
                patterns['feature_usage'][feature] += 1
            
            # Device patterns
            device = user.get('primary_device', 'desktop')
            patterns['devices'][device] += 1
            
            # Context patterns
            context = user.get('usage_context', 'work')
            patterns['contexts'][context] += 1
            
            # Pain points
            if 'pain_points' in user:
                patterns['pain_points'].extend(user['pain_points'])
        
        return patterns
    
    def _identify_archetype(self, patterns: Dict) -> str:
        """Identify persona archetype based on patterns"""
        
        # Simple heuristic-based archetype identification
        freq_pattern = max(patterns['usage_frequency'].items(), key=lambda x: x[1])[0] if patterns['usage_frequency'] else 'medium'
        device_pattern = max(patterns['devices'].items(), key=lambda x: x[1])[0] if patterns['devices'] else 'desktop'
        
        if freq_pattern == 'daily' and len(patterns['feature_usage']) > 10:
            return 'power_user'
        elif device_pattern in ['mobile', 'tablet']:
            return 'mobile_first'
        elif patterns['contexts'].get('work', 0) > patterns['contexts'].get('personal', 0):
            return 'business_user'
        else:
            return 'casual_user'
    
    def _generate_name(self, archetype: str) -> str:
        """Generate persona name based on archetype"""
        
        names = {
            'power_user': ['Alex', 'Sam', 'Jordan', 'Morgan'],
            'casual_user': ['Pat', 'Jamie', 'Casey', 'Riley'],
            'business_user': ['Taylor', 'Cameron', 'Avery', 'Blake'],
            'mobile_first': ['Quinn', 'Skylar', 'River', 'Sage']
        }
        
        name_pool = names.get(archetype, names['casual_user'])
        first_name = random.choice(name_pool)
        
        roles = {
            'power_user': 'the Power User',
            'casual_user': 'the Casual User',
            'business_user': 'the Business Professional',
            'mobile_first': 'the Mobile Native'
        }
        
        return f"{first_name} {roles[archetype]}"
    
    def _generate_tagline(self, patterns: Dict) -> str:
        """Generate persona tagline"""
        
        freq = max(patterns['usage_frequency'].items(), key=lambda x: x[1])[0] if patterns['usage_frequency'] else 'regular'
        context = max(patterns['contexts'].items(), key=lambda x: x[1])[0] if patterns['contexts'] else 'general'
        
        return f"A {freq} user who primarily uses the product for {context} purposes"
    
    def _aggregate_demographics(self, user_data: List[Dict]) -> Dict:
        """Aggregate demographic information"""
        
        demographics = {
            'age_range': '',
            'location_type': '',
            'occupation_category': '',
            'education_level': '',
            'tech_proficiency': ''
        }
        
        if not user_data:
            return demographics
        
        # Age range
        ages = [u.get('age', 30) for u in user_data if 'age' in u]
        if ages:
            avg_age = sum(ages) / len(ages)
            if avg_age < 25:
                demographics['age_range'] = '18-24'
            elif avg_age < 35:
                demographics['age_range'] = '25-34'
            elif avg_age < 45:
                demographics['age_range'] = '35-44'
            else:
                demographics['age_range'] = '45+'
        
        # Location type
        locations = [u.get('location_type', 'urban') for u in user_data if 'location_type' in u]
        if locations:
            demographics['location_type'] = Counter(locations).most_common(1)[0][0]
        
        # Tech proficiency
        tech_scores = [u.get('tech_proficiency', 5) for u in user_data if 'tech_proficiency' in u]
        if tech_scores:
            avg_tech = sum(tech_scores) / len(tech_scores)
            if avg_tech < 3:
                demographics['tech_proficiency'] = 'Beginner'
            elif avg_tech < 7:
                demographics['tech_proficiency'] = 'Intermediate'
            else:
                demographics['tech_proficiency'] = 'Advanced'
        
        return demographics
    
    def _extract_psychographics(self, patterns: Dict, interviews: List[Dict] = None) -> Dict:
        """Extract psychographic information"""
        
        psychographics = {
            'motivations': [],
            'values': [],
            'attitudes': [],
            'lifestyle': ''
        }
        
        # Extract from patterns
        if patterns['usage_frequency'].get('daily', 0) > 0:
            psychographics['motivations'].append('Efficiency')
            psychographics['values'].append('Time-saving')
        
        if patterns['devices'].get('mobile', 0) > patterns['devices'].get('desktop', 0):
            psychographics['lifestyle'] = 'On-the-go, mobile-first'
            psychographics['values'].append('Flexibility')
        
        # Extract from interviews if available
        if interviews:
            for interview in interviews:
                if 'motivations' in interview:
                    psychographics['motivations'].extend(interview['motivations'])
                if 'values' in interview:
                    psychographics['values'].extend(interview['values'])
        
        # Deduplicate
        psychographics['motivations'] = list(set(psychographics['motivations']))[:5]
        psychographics['values'] = list(set(psychographics['values']))[:5]
        
        return psychographics
    
    def _analyze_behaviors(self, user_data: List[Dict]) -> Dict:
        """Analyze user behaviors"""
        
        behaviors = {
            'usage_patterns': [],
            'feature_preferences': [],
            'interaction_style': '',
            'learning_preference': ''
        }
        
        if not user_data:
            return behaviors
        
        # Usage patterns
        frequencies = [u.get('usage_frequency', 'medium') for u in user_data]
        freq_counter = Counter(frequencies)
        behaviors['usage_patterns'] = [f"{freq}: {count} users" for freq, count in freq_counter.most_common(3)]
        
        # Feature preferences
        all_features = []
        for user in user_data:
            all_features.extend(user.get('features_used', []))
        
        feature_counter = Counter(all_features)
        behaviors['feature_preferences'] = [feat for feat, count in feature_counter.most_common(5)]
        
        # Interaction style
        if len(behaviors['feature_preferences']) > 10:
            behaviors['interaction_style'] = 'Exploratory - uses many features'
        else:
            behaviors['interaction_style'] = 'Focused - uses core features'
        
        return behaviors
    
    def _identify_needs(self, patterns: Dict, interviews: List[Dict] = None) -> Dict:
        """Identify user needs and goals"""
        
        needs = {
            'primary_goals': [],
            'secondary_goals': [],
            'functional_needs': [],
            'emotional_needs': []
        }
        
        # Derive from usage patterns
        if patterns['usage_frequency'].get('daily', 0) > 0:
            needs['primary_goals'].append('Complete tasks efficiently')
            needs['functional_needs'].append('Speed and performance')
        
        if patterns['contexts'].get('work', 0) > 0:
            needs['primary_goals'].append('Professional productivity')
            needs['functional_needs'].append('Integration with work tools')
        
        # Common emotional needs
        needs['emotional_needs'] = [
            'Feel confident using the product',
            'Trust the system with data',
            'Feel supported when issues arise'
        ]
        
        # Extract from interviews
        if interviews:
            for interview in interviews:
                if 'goals' in interview:
                    needs['primary_goals'].extend(interview['goals'][:2])
                if 'needs' in interview:
                    needs['functional_needs'].extend(interview['needs'][:3])
        
        return needs
    
    def _extract_frustrations(self, patterns: Dict, interviews: List[Dict] = None) -> List[str]:
        """Extract user frustrations"""
        
        frustrations = []
        
        # Common frustrations from patterns
        if patterns['pain_points']:
            frustration_counter = Counter(patterns['pain_points'])
            frustrations = [pain for pain, count in frustration_counter.most_common(5)]
        
        # Add archetype-specific frustrations if not enough from data
        if len(frustrations) < 3:
            frustrations.extend([
                'Slow loading times',
                'Confusing navigation',
                'Lack of mobile optimization'
            ])
        
        return frustrations[:5]
    
    def _generate_scenarios(self, archetype: str, patterns: Dict) -> List[Dict]:
        """Generate usage scenarios"""
        
        scenarios = []
        
        # Common scenarios based on archetype
        scenario_templates = {
            'power_user': [
                {
                    'title': 'Bulk Processing',
                    'context': 'Monday morning, needs to process week\'s data',
                    'goal': 'Complete batch operations quickly',
                    'steps': ['Import data', 'Apply bulk actions', 'Export results'],
                    'pain_points': ['No keyboard shortcuts', 'Slow processing']
                }
            ],
            'casual_user': [
                {
                    'title': 'Quick Task',
                    'context': 'Needs to complete single task',
                    'goal': 'Get in, complete task, get out',
                    'steps': ['Find feature', 'Complete task', 'Save/Exit'],
                    'pain_points': ['Can\'t find feature', 'Too many steps']
                }
            ],
            'business_user': [
                {
                    'title': 'Team Collaboration',
                    'context': 'Working with team on project',
                    'goal': 'Share and collaborate efficiently',
                    'steps': ['Create content', 'Share with team', 'Track feedback'],
                    'pain_points': ['No real-time collaboration', 'Poor permission management']
                }
            ],
            'mobile_first': [
                {
                    'title': 'On-the-Go Access',
                    'context': 'Commuting, needs quick access',
                    'goal': 'Complete task on mobile',
                    'steps': ['Open mobile app', 'Quick action', 'Sync with desktop'],
                    'pain_points': ['Feature parity issues', 'Poor mobile UX']
                }
            ]
        }
        
        return scenario_templates.get(archetype, scenario_templates['casual_user'])
    
    def _select_quote(self, interviews: List[Dict] = None, archetype: str = 'casual_user') -> str:
        """Select representative quote"""
        
        if interviews:
            # Try to find a real quote
            for interview in interviews:
                if 'quotes' in interview and interview['quotes']:
                    return interview['quotes'][0]
        
        # Use archetype default
        return self.archetype_templates[archetype]['quote']
    
    def _calculate_data_points(self, user_data: List[Dict]) -> Dict:
        """Calculate supporting data points"""
        
        return {
            'sample_size': len(user_data),
            'confidence_level': 'High' if len(user_data) > 50 else 'Medium' if len(user_data) > 20 else 'Low',
            'last_updated': 'Current',
            'validation_method': 'Quantitative analysis + Qualitative interviews'
        }
    
    def _derive_design_implications(self, patterns: Dict) -> List[str]:
        """Derive design implications from persona"""
        
        implications = []
        
        # Based on frequency
        if patterns['usage_frequency'].get('daily', 0) > patterns['usage_frequency'].get('weekly', 0):
            implications.append('Optimize for speed and efficiency')
            implications.append('Provide keyboard shortcuts and power features')
        else:
            implications.append('Focus on discoverability and guidance')
            implications.append('Simplify onboarding experience')
        
        # Based on device
        if patterns['devices'].get('mobile', 0) > 0:
            implications.append('Mobile-first responsive design')
            implications.append('Touch-optimized interactions')
        
        # Based on context
        if patterns['contexts'].get('work', 0) > patterns['contexts'].get('personal', 0):
            implications.append('Professional visual design')
            implications.append('Enterprise features (SSO, audit logs)')
        
        return implications[:5]
    
    def format_persona_output(self, persona: Dict) -> str:
        """Format persona for display"""
        
        output = []
        output.append("=" * 60)
        output.append(f"PERSONA: {persona['name']}")
        output.append("=" * 60)
        output.append(f"\n📝 {persona['tagline']}\n")
        
        output.append(f"Archetype: {persona['archetype'].replace('_', ' ').title()}")
        output.append(f"Quote: \"{persona['quote']}\"\n")
        
        output.append("👤 Demographics:")
        for key, value in persona['demographics'].items():
            if value:
                output.append(f"  • {key.replace('_', ' ').title()}: {value}")
        
        output.append("\n🧠 Psychographics:")
        if persona['psychographics']['motivations']:
            output.append(f"  Motivations: {', '.join(persona['psychographics']['motivations'])}")
        if persona['psychographics']['values']:
            output.append(f"  Values: {', '.join(persona['psychographics']['values'])}")
        
        output.append("\n🎯 Goals & Needs:")
        for goal in persona['needs_and_goals'].get('primary_goals', [])[:3]:
            output.append(f"  • {goal}")
        
        output.append("\n😤 Frustrations:")
        for frustration in persona['frustrations'][:3]:
            output.append(f"  • {frustration}")
        
        output.append("\n📊 Behaviors:")
        for pref in persona['behaviors'].get('feature_preferences', [])[:3]:
            output.append(f"  • Frequently uses: {pref}")
        
        output.append("\n💡 Design Implications:")
        for implication in persona['design_implications']:
            output.append(f"  → {implication}")
        
        output.append(f"\n📈 Data: Based on {persona['data_points']['sample_size']} users")
        output.append(f"    Confidence: {persona['data_points']['confidence_level']}")
        
        return "\n".join(output)

def create_sample_user_data():
    """Create sample user data for testing"""
    return [
        {
            'user_id': f'user_{i}',
            'age': 25 + (i % 30),
            'usage_frequency': ['daily', 'weekly', 'monthly'][i % 3],
            'features_used': ['dashboard', 'reports', 'settings', 'sharing', 'export'][:3 + (i % 3)],
            'primary_device': ['desktop', 'mobile', 'tablet'][i % 3],
            'usage_context': ['work', 'personal'][i % 2],
            'tech_proficiency': 3 + (i % 7),
            'pain_points': ['slow loading', 'confusing UI', 'missing features'][:(i % 3) + 1]
        }
        for i in range(30)
    ]

def format_json_output(persona: Dict) -> str:
    """Format persona as JSON with metadata"""
    result = {
        'metadata': {
            'tool': 'persona_generator',
            'version': '1.0.0',
            'archetype': persona['archetype']
        },
        'persona': persona
    }
    return json.dumps(result, indent=2)

def format_csv_output(persona: Dict) -> str:
    """Format persona as CSV"""
    import io
    csv_output = io.StringIO()

    # CSV header
    csv_output.write('category,attribute,value\n')

    # Demographics
    for key, value in persona['demographics'].items():
        if value:
            csv_output.write(f"demographics,{key},{value}\n")

    # Goals
    for goal in persona['needs_and_goals'].get('primary_goals', []):
        csv_output.write(f"goals,primary,\"{goal}\"\n")

    # Frustrations
    for frustration in persona['frustrations']:
        csv_output.write(f"frustrations,pain_point,\"{frustration}\"\n")

    return csv_output.getvalue()

def load_user_data_from_json(filepath: str) -> List[Dict]:
    """Load user data from JSON file"""
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
            # Support both array format and object with 'users' key
            if isinstance(data, list):
                return data
            elif isinstance(data, dict) and 'users' in data:
                return data['users']
            else:
                print("Error: JSON file must contain array of users or object with 'users' key", file=sys.stderr)
                sys.exit(1)
    except FileNotFoundError:
        print(f"Error: Input file not found: {filepath}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in file: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description='Generate data-driven user personas from research data',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate persona from sample data
  %(prog)s

  # Generate persona from user data file
  %(prog)s --data users.json

  # Export as JSON
  %(prog)s --data users.json --output json

  # Export as CSV for spreadsheet
  %(prog)s -o csv -f persona.csv

  # Verbose output
  %(prog)s --data users.json --verbose

For more information, see the skill documentation.
        """
    )

    parser.add_argument('--data', help='JSON file with user data (optional, uses sample if not provided)')
    parser.add_argument('--output', '-o', choices=['text', 'json', 'csv'], default='text',
                       help='Output format (default: text)')
    parser.add_argument('--file', '-f', help='Write output to file instead of stdout')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output with detailed information')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0.0')

    args = parser.parse_args()

    try:
        generator = PersonaGenerator()

        # Load user data (from file or use sample)
        if args.data:
            if args.verbose:
                print(f"Loading user data from: {args.data}", file=sys.stderr)

            input_path = Path(args.data)
            if not input_path.exists():
                print(f"Error: Input file not found: {args.data}", file=sys.stderr)
                sys.exit(1)

            user_data = load_user_data_from_json(args.data)
        else:
            if args.verbose:
                print("Using sample user data", file=sys.stderr)
            user_data = create_sample_user_data()

        if args.verbose:
            print(f"Analyzing {len(user_data)} users", file=sys.stderr)

        # Optional interview insights (could be expanded to load from file)
        interview_insights = [
            {
                'quotes': ["I need to see all my data in one place"],
                'motivations': ['Efficiency', 'Control'],
                'goals': ['Save time', 'Make better decisions']
            }
        ]

        # Generate persona
        persona = generator.generate_persona_from_data(user_data, interview_insights)

        if args.verbose:
            print(f"Generated persona: {persona['name']}", file=sys.stderr)
            print(f"Archetype: {persona['archetype']}", file=sys.stderr)

        # Format output
        if args.output == 'json':
            output = format_json_output(persona)
        elif args.output == 'csv':
            output = format_csv_output(persona)
        else:  # text
            output = generator.format_persona_output(persona)

        # Write output
        if args.file:
            try:
                with open(args.file, 'w') as f:
                    f.write(output)
                if args.verbose:
                    print(f"Results written to: {args.file}", file=sys.stderr)
                else:
                    print(f"Output saved to: {args.file}")
            except Exception as e:
                print(f"Error writing output file: {e}", file=sys.stderr)
                sys.exit(4)
        else:
            print(output)

        sys.exit(0)

    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
