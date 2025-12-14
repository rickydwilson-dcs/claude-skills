#!/usr/bin/env python3
"""
Retrospective Format Selector - Intelligent Format Recommendation

Recommends optimal retrospective format based on team context, sprint health,
time constraints, and focus areas. Leverages the 8-format knowledge base in
references/retro-formats.md for comprehensive facilitation guidance.

Supported Formats:
1. Start/Stop/Continue - Quick format for new teams
2. Glad/Sad/Mad - Emotional check-in and morale assessment
3. 4Ls (Liked/Learned/Lacked/Longed For) - Deeper reflection with learning focus
4. Sailboat - Visual teams, risk assessment focus
5. Timeline - Detailed sprint review, pattern identification
6. Starfish - Granular feedback (Keep/Less/More/Stop/Start)
7. Speed Dating - Large teams, fresh perspectives
8. Three Little Pigs - Technical/architecture focus
"""

import argparse
import json
import logging
import sys
from datetime import datetime
from typing import Dict, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class RetroFormatSelector:
    """Select optimal retrospective format based on team context"""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        if verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        self.formats = self._initialize_formats()
        logger.debug("RetroFormatSelector initialized")

    def _initialize_formats(self) -> Dict[str, Dict]:
        """Initialize the 8 retrospective formats with metadata"""
        return {
            'start_stop_continue': {
                'name': 'Start/Stop/Continue',
                'duration': 60,
                'best_for': ['new_teams', 'quick_format', 'simple_issues'],
                'team_size': {'min': 3, 'max': 12, 'optimal': 6},
                'focus_areas': ['process', 'habits'],
                'complexity': 'low',
                'energy_level': 'medium',
                'description': 'Simple three-column format focusing on behaviors to start, stop, and continue.',
                'facilitation_tip': 'Great for first-time retros or when time is limited. Keep voting simple.'
            },
            'glad_sad_mad': {
                'name': 'Glad/Sad/Mad',
                'duration': 75,
                'best_for': ['emotional_checkin', 'morale_assessment', 'team_health'],
                'team_size': {'min': 3, 'max': 10, 'optimal': 6},
                'focus_areas': ['emotional', 'morale'],
                'complexity': 'low',
                'energy_level': 'medium',
                'description': 'Emotional check-in format that surfaces feelings and team morale.',
                'facilitation_tip': 'Create psychological safety first. Acknowledge emotions without dismissing them.'
            },
            '4ls': {
                'name': '4Ls (Liked/Learned/Lacked/Longed For)',
                'duration': 90,
                'best_for': ['learning_focus', 'deeper_reflection', 'growth_mindset'],
                'team_size': {'min': 4, 'max': 12, 'optimal': 7},
                'focus_areas': ['learning', 'growth', 'process'],
                'complexity': 'medium',
                'energy_level': 'medium',
                'description': 'Four-quadrant format emphasizing learning and improvement opportunities.',
                'facilitation_tip': 'Spend extra time on Learned section to extract knowledge transfer opportunities.'
            },
            'sailboat': {
                'name': 'Sailboat',
                'duration': 90,
                'best_for': ['visual_teams', 'risk_assessment', 'goal_orientation'],
                'team_size': {'min': 4, 'max': 15, 'optimal': 8},
                'focus_areas': ['risks', 'goals', 'blockers'],
                'complexity': 'medium',
                'energy_level': 'high',
                'description': 'Visual metaphor with wind (propellers), anchors, rocks (risks), and island (goals).',
                'facilitation_tip': 'Draw the sailboat on whiteboard. Great for identifying risks and blockers.'
            },
            'timeline': {
                'name': 'Timeline',
                'duration': 90,
                'best_for': ['detailed_review', 'pattern_identification', 'complex_sprints'],
                'team_size': {'min': 4, 'max': 12, 'optimal': 7},
                'focus_areas': ['events', 'patterns', 'process'],
                'complexity': 'high',
                'energy_level': 'medium',
                'description': 'Chronological sprint review mapping events and emotions over time.',
                'facilitation_tip': 'Plot events first, then add emotion indicators. Look for correlations.'
            },
            'starfish': {
                'name': 'Starfish',
                'duration': 90,
                'best_for': ['granular_feedback', 'nuanced_improvement', 'mature_teams'],
                'team_size': {'min': 4, 'max': 12, 'optimal': 7},
                'focus_areas': ['process', 'habits', 'practices'],
                'complexity': 'medium',
                'energy_level': 'medium',
                'description': 'Five-point format: Keep Doing, Less Of, More Of, Stop Doing, Start Doing.',
                'facilitation_tip': 'More granular than Start/Stop/Continue. Good for teams ready for nuanced feedback.'
            },
            'speed_dating': {
                'name': 'Speed Dating',
                'duration': 60,
                'best_for': ['large_teams', 'fresh_perspectives', 'quiet_voices'],
                'team_size': {'min': 8, 'max': 20, 'optimal': 12},
                'focus_areas': ['collaboration', 'perspectives'],
                'complexity': 'medium',
                'energy_level': 'high',
                'description': 'Rotating pair discussions with full-group synthesis.',
                'facilitation_tip': 'Pair people who don\'t usually work together. Mix up perspectives.'
            },
            'three_little_pigs': {
                'name': 'Three Little Pigs',
                'duration': 75,
                'best_for': ['technical_decisions', 'architecture_review', 'stability_focus'],
                'team_size': {'min': 4, 'max': 10, 'optimal': 6},
                'focus_areas': ['technical', 'architecture', 'stability'],
                'complexity': 'medium',
                'energy_level': 'medium',
                'description': 'Straw/Stick/Brick metaphor for code and system stability assessment.',
                'facilitation_tip': 'Excellent after tech debt discussions or post-incident reviews.'
            }
        }

    def recommend_format(self,
                         team_size: int = 6,
                         time_available: int = 60,
                         focus: str = 'process',
                         health_score: Optional[int] = None,
                         previous_formats: Optional[List[str]] = None,
                         team_maturity: str = 'intermediate') -> Dict:
        """
        Recommend optimal retrospective format.

        Args:
            team_size: Number of team members
            time_available: Minutes available for retro
            focus: Focus area (process/emotional/technical/learning/risks)
            health_score: Sprint health score (0-100) from metrics calculator
            previous_formats: Recent formats used (for rotation)
            team_maturity: Team experience level (new/intermediate/mature)

        Returns:
            Recommendation with primary format, alternatives, and rationale
        """
        logger.debug(f"Recommending format: team_size={team_size}, time={time_available}, focus={focus}")
        scores = {}
        rationales = {}

        for key, fmt in self.formats.items():
            score = 0
            reasons = []

            # Team size fit (0-30 points)
            size_score = self._score_team_size(team_size, fmt['team_size'])
            score += size_score
            if size_score >= 25:
                reasons.append(f"Optimal for team size {team_size}")

            # Time fit (0-25 points)
            time_score = self._score_time_fit(time_available, fmt['duration'])
            score += time_score
            if time_score >= 20:
                reasons.append(f"Fits within {time_available} min time constraint")

            # Focus area match (0-25 points)
            if focus in fmt['focus_areas']:
                score += 25
                reasons.append(f"Matches '{focus}' focus area")
            elif any(f in fmt['focus_areas'] for f in ['process', 'habits']):
                score += 10  # Generic formats get partial credit

            # Team maturity match (0-10 points)
            maturity_score = self._score_maturity(team_maturity, fmt['complexity'])
            score += maturity_score

            # Health score adjustment (0-10 points)
            if health_score is not None:
                health_adjustment = self._score_health_adjustment(health_score, fmt, focus)
                score += health_adjustment
                if health_adjustment > 5:
                    reasons.append("Well-suited for current sprint health")

            # Rotation bonus (avoid recent formats)
            if previous_formats and key not in previous_formats:
                score += 5
                reasons.append("Fresh format (not used recently)")
            elif previous_formats and key in previous_formats:
                score -= 10  # Penalty for recent use

            scores[key] = score
            rationales[key] = reasons

        # Sort by score
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        primary_key = ranked[0][0]
        alternatives = [k for k, _ in ranked[1:4]]  # Top 3 alternatives

        return {
            'recommended_format': primary_key,
            'format_details': self.formats[primary_key],
            'confidence_score': ranked[0][1],
            'rationale': rationales[primary_key],
            'alternatives': [
                {'format': k, 'score': scores[k], 'details': self.formats[k]}
                for k in alternatives
            ],
            'context': {
                'team_size': team_size,
                'time_available': time_available,
                'focus': focus,
                'health_score': health_score,
                'team_maturity': team_maturity
            }
        }

    def _score_team_size(self, actual: int, spec: Dict) -> int:
        """Score team size fit (0-30)"""
        if actual == spec['optimal']:
            return 30
        elif spec['min'] <= actual <= spec['max']:
            # Distance from optimal
            distance = abs(actual - spec['optimal'])
            return max(15, 30 - distance * 3)
        else:
            return 5  # Out of range but still possible

    def _score_time_fit(self, available: int, required: int) -> int:
        """Score time fit (0-25)"""
        if available >= required:
            return 25
        elif available >= required * 0.8:
            return 15  # Can compress
        elif available >= required * 0.6:
            return 8   # Will feel rushed
        else:
            return 0   # Not feasible

    def _score_maturity(self, maturity: str, complexity: str) -> int:
        """Score team maturity match (0-10)"""
        if maturity == 'new' and complexity == 'low':
            return 10
        elif maturity == 'intermediate' and complexity in ['low', 'medium']:
            return 10
        elif maturity == 'mature':
            return 10  # Mature teams can handle any
        elif maturity == 'new' and complexity == 'high':
            return 2   # Too complex for new teams
        else:
            return 6

    def _score_health_adjustment(self, health_score: int, fmt: Dict, focus: str) -> int:
        """Score based on sprint health (0-10)"""
        if health_score < 60:
            # Poor health - favor emotional/retrospective formats
            if 'emotional' in fmt['focus_areas'] or 'morale' in fmt['focus_areas']:
                return 10
            elif 'risks' in fmt['focus_areas']:
                return 8
        elif health_score < 80:
            # Moderate - favor process improvement
            if 'process' in fmt['focus_areas']:
                return 8
        else:
            # Good health - favor learning/growth
            if 'learning' in fmt['focus_areas'] or 'growth' in fmt['focus_areas']:
                return 10
        return 5

    def get_facilitation_guide(self, format_key: str) -> Dict:
        """
        Get detailed facilitation guide for a format.

        Args:
            format_key: Format identifier

        Returns:
            Complete facilitation guide
        """
        logger.debug(f"Getting facilitation guide for: {format_key}")
        if format_key not in self.formats:
            logger.warning(f"Unknown format requested: {format_key}")
            return {'error': f'Unknown format: {format_key}'}

        fmt = self.formats[format_key]

        guides = {
            'start_stop_continue': {
                'setup': 'Create three columns on whiteboard or Miro: Start, Stop, Continue',
                'process': [
                    '1. Silent brainstorming: Team adds items to columns (10 min)',
                    '2. Group similar items and remove duplicates (5 min)',
                    '3. Discuss each category, prioritize by dots/votes (20 min)',
                    '4. Select 2-3 concrete action items with owners (10 min)'
                ],
                'timebox': {'brainstorm': 10, 'grouping': 5, 'discussion': 20, 'actions': 10},
                'materials': ['Whiteboard/Miro', 'Sticky notes', 'Voting dots'],
                'common_pitfalls': [
                    'Items too vague - push for specifics',
                    'Too many items - limit to top 3 per category',
                    'No owners for actions - assign before leaving'
                ]
            },
            'glad_sad_mad': {
                'setup': 'Create three emotional zones with appropriate colors (green/blue/red)',
                'process': [
                    '1. Set the stage - establish psychological safety (5 min)',
                    '2. Silent brainstorming on sticky notes (10 min)',
                    '3. Share items one person at a time (15 min)',
                    '4. Group themes and discuss (20 min)',
                    '5. Convert feelings to actions (10 min)'
                ],
                'timebox': {'setup': 5, 'brainstorm': 10, 'sharing': 15, 'discussion': 20, 'actions': 10},
                'materials': ['Colored zones', 'Sticky notes', 'Tissues (really)'],
                'common_pitfalls': [
                    'Dismissing emotions - acknowledge all feelings',
                    'Blame game - redirect to "what can WE control"',
                    'Skipping Mad section - it\'s important to surface frustrations'
                ]
            },
            '4ls': {
                'setup': 'Create four quadrants: Liked, Learned, Lacked, Longed For',
                'process': [
                    '1. Individual reflection (10 min)',
                    '2. Round-robin sharing (20 min)',
                    '3. Group similar items (10 min)',
                    '4. Deep dive on top items per quadrant (20 min)',
                    '5. Action planning with knowledge sharing focus (15 min)'
                ],
                'timebox': {'reflection': 10, 'sharing': 20, 'grouping': 10, 'discussion': 20, 'actions': 15},
                'materials': ['4-quadrant board', 'Sticky notes', 'Timer'],
                'common_pitfalls': [
                    'Rushing Learned section - this has most value',
                    'Lacked becoming complaint session - focus on solutions',
                    'Not capturing knowledge transfer opportunities'
                ]
            },
            'sailboat': {
                'setup': 'Draw sailboat with: Island (goal), Wind, Anchors, Rocks (risks)',
                'process': [
                    '1. Explain metaphor clearly (5 min)',
                    '2. Team adds items to each area (15 min)',
                    '3. Group and discuss wind/propellers (10 min)',
                    '4. Discuss anchors and how to remove (15 min)',
                    '5. Identify rocks/risks ahead (15 min)',
                    '6. Create action plan prioritizing anchor removal (15 min)'
                ],
                'timebox': {'explain': 5, 'brainstorm': 15, 'wind': 10, 'anchors': 15, 'rocks': 15, 'actions': 15},
                'materials': ['Large whiteboard', 'Colored markers', 'Sticky notes'],
                'common_pitfalls': [
                    'Focusing only on negatives - celebrate wind/propellers',
                    'Vague rocks - push for specific risks',
                    'Not connecting to sprint goal (island)'
                ]
            },
            'timeline': {
                'setup': 'Draw timeline with sprint days across top, emotion scale on side',
                'process': [
                    '1. Draw sprint timeline (5 min)',
                    '2. Team adds events chronologically (15 min)',
                    '3. Add emotion indicators to events (10 min)',
                    '4. Identify patterns and correlations (20 min)',
                    '5. Discuss high and low points (20 min)',
                    '6. Extract learnings and actions (15 min)'
                ],
                'timebox': {'setup': 5, 'events': 15, 'emotions': 10, 'patterns': 20, 'discussion': 20, 'actions': 15},
                'materials': ['Large timeline board', 'Colored sticky notes', 'Emotion stickers'],
                'common_pitfalls': [
                    'Events too generic - get specific about what happened',
                    'Ignoring emotion patterns - they reveal important insights',
                    'Not identifying early warning signs for future'
                ]
            },
            'starfish': {
                'setup': 'Create 5-point star: Keep, Less Of, More Of, Stop, Start',
                'process': [
                    '1. Explain each category with examples (5 min)',
                    '2. Silent brainstorming (15 min)',
                    '3. Share and group items (15 min)',
                    '4. Discuss each point of star (25 min)',
                    '5. Vote on top actions (10 min)',
                    '6. Create action plan (15 min)'
                ],
                'timebox': {'explain': 5, 'brainstorm': 15, 'sharing': 15, 'discussion': 25, 'voting': 10, 'actions': 15},
                'materials': ['5-point star template', 'Sticky notes', 'Voting dots'],
                'common_pitfalls': [
                    'Confusing Less Of with Stop - less vs eliminate',
                    'Empty Keep section - celebrate what works',
                    'Not being specific enough about quantities for Less/More'
                ]
            },
            'speed_dating': {
                'setup': 'Create pairs list, prepare rotation timer, synthesis board',
                'process': [
                    '1. Create intentional pairs (2 min)',
                    '2. Round 1: "What went well?" pairs discussion (10 min)',
                    '3. Rotate pairs (2 min)',
                    '4. Round 2: "What could improve?" (10 min)',
                    '5. Rotate pairs (2 min)',
                    '6. Round 3: "What should we try?" (10 min)',
                    '7. Full group synthesis (15 min)',
                    '8. Action planning (10 min)'
                ],
                'timebox': {'pairing': 2, 'round1': 10, 'rotate1': 2, 'round2': 10, 'rotate2': 2, 'round3': 10, 'synthesis': 15, 'actions': 10},
                'materials': ['Pair rotation list', 'Timer', 'Synthesis board'],
                'common_pitfalls': [
                    'Same pairs who usually work together - mix it up',
                    'Dominant voices in pairs - emphasize equal time',
                    'Lost themes in synthesis - capture as you go'
                ]
            },
            'three_little_pigs': {
                'setup': 'Create three houses: Straw (fragile), Sticks (needs work), Brick (solid)',
                'process': [
                    '1. Explain metaphor with code/system examples (5 min)',
                    '2. Team identifies items for each house (15 min)',
                    '3. Group and discuss straw house (fragile) (15 min)',
                    '4. Discuss stick house (needs improvement) (15 min)',
                    '5. Celebrate brick house (solid) (10 min)',
                    '6. Prioritize straw→stick→brick improvements (15 min)'
                ],
                'timebox': {'explain': 5, 'brainstorm': 15, 'straw': 15, 'stick': 15, 'brick': 10, 'actions': 15},
                'materials': ['Three house drawings', 'Sticky notes', 'Red/yellow/green markers'],
                'common_pitfalls': [
                    'Only technical items - include process/practices',
                    'Everything is straw - push for brick examples',
                    'Not connecting to technical debt backlog'
                ]
            }
        }

        guide = guides.get(format_key, {})
        return {
            'format': fmt,
            'facilitation_guide': guide,
            'total_duration': fmt['duration'],
            'recommended_for': fmt['best_for']
        }


def format_text_output(recommendation: Dict, guide: Optional[Dict] = None) -> str:
    """Format results as human-readable text"""
    output = []
    output.append("=" * 60)
    output.append("RETROSPECTIVE FORMAT RECOMMENDATION")
    output.append("=" * 60)

    fmt = recommendation['format_details']
    output.append(f"\n🎯 RECOMMENDED: {fmt['name']}")
    output.append("-" * 60)
    output.append(f"Duration: {fmt['duration']} minutes")
    output.append(f"Complexity: {fmt['complexity'].upper()}")
    output.append(f"Team Size: {fmt['team_size']['min']}-{fmt['team_size']['max']} (optimal: {fmt['team_size']['optimal']})")
    output.append(f"\nDescription: {fmt['description']}")
    output.append(f"\n💡 Facilitation Tip: {fmt['facilitation_tip']}")

    output.append(f"\n📊 SELECTION RATIONALE (Score: {recommendation['confidence_score']})")
    output.append("-" * 60)
    for reason in recommendation['rationale']:
        output.append(f"  ✓ {reason}")

    ctx = recommendation['context']
    output.append(f"\n📋 YOUR CONTEXT")
    output.append("-" * 60)
    output.append(f"  Team Size: {ctx['team_size']}")
    output.append(f"  Time Available: {ctx['time_available']} min")
    output.append(f"  Focus Area: {ctx['focus']}")
    if ctx['health_score']:
        output.append(f"  Sprint Health: {ctx['health_score']}/100")
    output.append(f"  Team Maturity: {ctx['team_maturity']}")

    if recommendation['alternatives']:
        output.append(f"\n🔄 ALTERNATIVES")
        output.append("-" * 60)
        for alt in recommendation['alternatives']:
            output.append(f"  • {alt['details']['name']} (Score: {alt['score']}) - {alt['details']['duration']} min")

    if guide:
        g = guide['facilitation_guide']
        output.append(f"\n📖 FACILITATION GUIDE")
        output.append("-" * 60)
        output.append(f"Setup: {g.get('setup', 'N/A')}")
        output.append(f"\nProcess:")
        for step in g.get('process', []):
            output.append(f"  {step}")
        output.append(f"\nTimeboxes:")
        for phase, mins in g.get('timebox', {}).items():
            output.append(f"  {phase}: {mins} min")
        output.append(f"\nMaterials Needed:")
        for mat in g.get('materials', []):
            output.append(f"  • {mat}")
        output.append(f"\nCommon Pitfalls:")
        for pitfall in g.get('common_pitfalls', []):
            output.append(f"  ⚠️  {pitfall}")

    output.append("")
    output.append("=" * 60)
    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(
        description='Recommend optimal retrospective format based on team context',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic recommendation
  %(prog)s --team-size 8 --time 60

  # With focus area
  %(prog)s --team-size 6 --time 90 --focus technical

  # Full context with health score
  %(prog)s --team-size 7 --time 60 --focus emotional --health-score 65

  # Avoid recently used formats
  %(prog)s --team-size 8 --time 90 --previous sailboat 4ls

  # Get full facilitation guide
  %(prog)s --team-size 6 --time 60 --output-guide

  # List all available formats
  %(prog)s --list-formats

Focus Areas:
  process    - Process improvement, workflow optimization
  emotional  - Team morale, feelings, psychological safety
  technical  - Architecture, code quality, technical debt
  learning   - Knowledge sharing, skill growth
  risks      - Risk identification, blockers, dependencies

Available Formats:
  start_stop_continue, glad_sad_mad, 4ls, sailboat,
  timeline, starfish, speed_dating, three_little_pigs
        """
    )

    parser.add_argument(
        '--team-size',
        type=int,
        default=6,
        help='Number of team members (default: 6)'
    )
    parser.add_argument(
        '--time',
        type=int,
        default=60,
        help='Time available in minutes (default: 60)'
    )
    parser.add_argument(
        '--focus',
        type=str,
        default='process',
        choices=['process', 'emotional', 'technical', 'learning', 'risks', 'collaboration'],
        help='Focus area for retrospective (default: process)'
    )
    parser.add_argument(
        '--health-score',
        type=int,
        help='Sprint health score 0-100 (from sprint_metrics_calculator)'
    )
    parser.add_argument(
        '--previous',
        nargs='+',
        type=str,
        help='Recently used formats to avoid (for rotation)'
    )
    parser.add_argument(
        '--maturity',
        type=str,
        default='intermediate',
        choices=['new', 'intermediate', 'mature'],
        help='Team maturity level (default: intermediate)'
    )
    parser.add_argument(
        '--output-guide',
        action='store_true',
        help='Include full facilitation guide in output'
    )
    parser.add_argument(
        '--list-formats',
        action='store_true',
        help='List all available formats and exit'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output as JSON'
    )
    parser.add_argument(
        '--output', '-o',
        help='Write output to file'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )

    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )

    args = parser.parse_args()

    selector = RetroFormatSelector(verbose=args.verbose)

    # List formats mode
    if args.list_formats:
        print("Available Retrospective Formats:")
        print("-" * 50)
        for key, fmt in selector.formats.items():
            print(f"\n{key}:")
            print(f"  Name: {fmt['name']}")
            print(f"  Duration: {fmt['duration']} min")
            print(f"  Best For: {', '.join(fmt['best_for'])}")
            print(f"  Focus: {', '.join(fmt['focus_areas'])}")
        return

    # Get recommendation
    if args.verbose:
        print(f"Analyzing context: team={args.team_size}, time={args.time}, focus={args.focus}", file=sys.stderr)

    recommendation = selector.recommend_format(
        team_size=args.team_size,
        time_available=args.time,
        focus=args.focus,
        health_score=args.health_score,
        previous_formats=args.previous,
        team_maturity=args.maturity
    )

    # Get facilitation guide if requested
    guide = None
    if args.output_guide:
        guide = selector.get_facilitation_guide(recommendation['recommended_format'])

    # Format output
    if args.json:
        result = {
            'metadata': {
                'tool': 'retro_format_selector',
                'version': '1.0.0',
                'generated_at': datetime.now().isoformat()
            },
            'recommendation': recommendation
        }
        if guide:
            result['facilitation_guide'] = guide

        output = json.dumps(result, indent=2)
    else:
        output = format_text_output(recommendation, guide)

    # Write output
    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"Output saved to: {args.output}")
        except Exception as e:
            print(f"Error writing output: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(output)


if __name__ == "__main__":
    main()
