#!/usr/bin/env python3
"""
Sprint Metrics Calculator - Agile Team Performance Analysis

Calculates sprint metrics including velocity, burndown, completion rate, and team capacity.
Provides actionable insights for sprint retrospectives and planning.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from statistics import mean, stdev

class SprintMetricsCalculator:
    """Calculates and analyzes sprint metrics for agile teams"""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.metrics = {
            'calculated_at': datetime.now().isoformat(),
            'velocity': 0,
            'completion_rate': 0,
            'sprint_health': 'unknown',
            'recommendations': []
        }

    def calculate_velocity(self, story_points: List[int]) -> Dict:
        """Calculate team velocity from completed story points"""
        if not story_points:
            return {'average': 0, 'trend': 'unknown', 'stability': 'unknown'}

        avg_velocity = mean(story_points)
        velocity_stdev = stdev(story_points) if len(story_points) > 1 else 0

        # Determine trend (last 3 sprints vs previous)
        trend = 'stable'
        if len(story_points) >= 6:
            recent_avg = mean(story_points[-3:])
            previous_avg = mean(story_points[-6:-3])
            if recent_avg > previous_avg * 1.1:
                trend = 'increasing'
            elif recent_avg < previous_avg * 0.9:
                trend = 'decreasing'

        # Determine stability (coefficient of variation)
        stability = 'stable'
        if avg_velocity > 0:
            cv = (velocity_stdev / avg_velocity) * 100
            if cv > 30:
                stability = 'volatile'
            elif cv > 15:
                stability = 'moderate'

        return {
            'average': round(avg_velocity, 1),
            'current': story_points[-1] if story_points else 0,
            'min': min(story_points),
            'max': max(story_points),
            'std_dev': round(velocity_stdev, 1),
            'trend': trend,
            'stability': stability
        }

    def calculate_completion_rate(self, committed: int, completed: int) -> Dict:
        """Calculate sprint completion rate"""
        if committed == 0:
            return {'rate': 0, 'status': 'no_commitment'}

        rate = (completed / committed) * 100

        status = 'excellent'  # >= 95%
        if rate < 70:
            status = 'poor'
        elif rate < 85:
            status = 'needs_improvement'
        elif rate < 95:
            status = 'good'

        return {
            'rate': round(rate, 1),
            'committed': committed,
            'completed': completed,
            'incomplete': committed - completed,
            'status': status
        }

    def calculate_burndown_health(self, ideal_remaining: List[int], actual_remaining: List[int]) -> Dict:
        """Analyze burndown chart health"""
        if len(ideal_remaining) != len(actual_remaining):
            return {'health': 'unknown', 'warning': 'Data length mismatch'}

        # Calculate deviation from ideal
        deviations = [actual - ideal for actual, ideal in zip(actual_remaining, ideal_remaining)]
        avg_deviation = mean(deviations)

        health = 'on_track'
        if avg_deviation > 0:
            if avg_deviation > mean(ideal_remaining) * 0.2:
                health = 'behind_schedule'
            else:
                health = 'slightly_behind'
        elif avg_deviation < -mean(ideal_remaining) * 0.1:
            health = 'ahead_of_schedule'

        return {
            'health': health,
            'avg_deviation': round(avg_deviation, 1),
            'final_variance': actual_remaining[-1] - ideal_remaining[-1] if ideal_remaining else 0
        }

    def calculate_capacity_utilization(self, team_capacity: int, story_points_completed: int) -> Dict:
        """Calculate team capacity utilization"""
        if team_capacity == 0:
            return {'utilization': 0, 'status': 'unknown'}

        utilization = (story_points_completed / team_capacity) * 100

        status = 'optimal'  # 80-95%
        if utilization < 60:
            status = 'under_utilized'
        elif utilization < 80:
            status = 'moderate'
        elif utilization > 100:
            status = 'over_committed'
        elif utilization > 95:
            status = 'high_utilization'

        return {
            'utilization': round(utilization, 1),
            'capacity': team_capacity,
            'completed': story_points_completed,
            'remaining_capacity': max(0, team_capacity - story_points_completed),
            'status': status
        }

    def generate_sprint_insights(self, velocity: Dict, completion: Dict, capacity: Dict) -> List[str]:
        """Generate actionable insights from metrics"""
        insights = []

        # Velocity insights
        if velocity['stability'] == 'volatile':
            insights.append(
                "⚠️  Velocity is volatile. Review story estimation accuracy and team composition changes."
            )
        if velocity['trend'] == 'decreasing':
            insights.append(
                "📉 Velocity is decreasing. Investigate impediments, technical debt, or team morale issues."
            )
        elif velocity['trend'] == 'increasing':
            insights.append(
                "📈 Velocity is increasing. Great work! Document what's working well."
            )

        # Completion insights
        if completion['status'] == 'poor':
            insights.append(
                "❌ Low completion rate. Consider reducing sprint commitment or improving estimation."
            )
        elif completion['status'] == 'excellent':
            insights.append(
                "✅ Excellent completion rate! Team is delivering consistently."
            )

        # Capacity insights
        if capacity['status'] == 'over_committed':
            insights.append(
                "⚠️  Team is over-committed. Reduce next sprint's commitment by 15-20%."
            )
        elif capacity['status'] == 'under_utilized':
            insights.append(
                "💡 Team has excess capacity. Consider pulling additional stories or addressing impediments."
            )
        elif capacity['status'] == 'optimal':
            insights.append(
                "✨ Optimal capacity utilization. Maintain current sprint sizing."
            )

        return insights

    def calculate_sprint_health_score(self, velocity: Dict, completion: Dict, capacity: Dict) -> int:
        """Calculate overall sprint health score (0-100)"""
        score = 100

        # Velocity component (30 points)
        if velocity['stability'] == 'volatile':
            score -= 15
        elif velocity['stability'] == 'moderate':
            score -= 7

        if velocity['trend'] == 'decreasing':
            score -= 15

        # Completion component (40 points)
        completion_rate = completion['rate']
        if completion_rate < 70:
            score -= 40
        elif completion_rate < 85:
            score -= 20
        elif completion_rate < 95:
            score -= 5

        # Capacity component (30 points)
        if capacity['status'] in ['over_committed', 'under_utilized']:
            score -= 20
        elif capacity['status'] in ['high_utilization', 'moderate']:
            score -= 10

        return max(0, min(100, score))

    def print_metrics_report(self, metrics: Dict):
        """Print human-readable metrics report"""
        print("\n" + "="*60)
        print("SPRINT METRICS REPORT")
        print("="*60)

        if 'velocity' in metrics:
            v = metrics['velocity']
            print(f"\n📊 Velocity Analysis:")
            print(f"   Current: {v['current']} points")
            print(f"   Average: {v['average']} points")
            print(f"   Range: {v['min']} - {v['max']} points")
            print(f"   Trend: {v['trend'].upper()}")
            print(f"   Stability: {v['stability'].upper()}")

        if 'completion' in metrics:
            c = metrics['completion']
            print(f"\n✅ Completion Rate:")
            print(f"   Rate: {c['rate']}%")
            print(f"   Committed: {c['committed']} points")
            print(f"   Completed: {c['completed']} points")
            print(f"   Incomplete: {c['incomplete']} points")
            print(f"   Status: {c['status'].upper().replace('_', ' ')}")

        if 'capacity' in metrics:
            cap = metrics['capacity']
            print(f"\n⚡ Capacity Utilization:")
            print(f"   Utilization: {cap['utilization']}%")
            print(f"   Team Capacity: {cap['capacity']} points")
            print(f"   Completed: {cap['completed']} points")
            print(f"   Status: {cap['status'].upper().replace('_', ' ')}")

        if 'health_score' in metrics:
            print(f"\n🏥 Sprint Health Score: {metrics['health_score']}/100")

        if 'insights' in metrics and metrics['insights']:
            print(f"\n💡 Insights & Recommendations:")
            for i, insight in enumerate(metrics['insights'], 1):
                print(f"   {insight}")

        print("\n" + "="*60)

def main():
    parser = argparse.ArgumentParser(
        description="Calculate sprint metrics and generate insights for agile teams",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Calculate velocity from story points
  %(prog)s --velocity 23 25 21 28 24

  # Calculate completion rate
  %(prog)s --committed 30 --completed 27

  # Full sprint analysis
  %(prog)s --velocity 23 25 21 --committed 25 --completed 21 --capacity 25

  # JSON output
  %(prog)s --velocity 23 25 21 --json
        """
    )

    parser.add_argument(
        '--velocity',
        nargs='+',
        type=int,
        help='Story points completed per sprint (space-separated list)'
    )
    parser.add_argument(
        '--committed',
        type=int,
        help='Story points committed for current sprint'
    )
    parser.add_argument(
        '--completed',
        type=int,
        help='Story points completed in current sprint'
    )
    parser.add_argument(
        '--capacity',
        type=int,
        help='Team capacity in story points'
    )
    parser.add_argument(
        '--burndown-ideal',
        nargs='+',
        type=int,
        help='Ideal remaining work per day (space-separated)'
    )
    parser.add_argument(
        '--burndown-actual',
        nargs='+',
        type=int,
        help='Actual remaining work per day (space-separated)'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output as JSON'
    )

    args = parser.parse_args()

    if not any([args.velocity, args.committed, args.burndown_ideal]):
        parser.print_help()
        sys.exit(0)

    calculator = SprintMetricsCalculator(verbose=args.verbose)
    results = {}

    # Calculate velocity
    if args.velocity:
        results['velocity'] = calculator.calculate_velocity(args.velocity)

    # Calculate completion rate
    if args.committed and args.completed is not None:
        results['completion'] = calculator.calculate_completion_rate(
            args.committed, args.completed
        )

    # Calculate capacity utilization
    if args.capacity and args.completed is not None:
        results['capacity'] = calculator.calculate_capacity_utilization(
            args.capacity, args.completed
        )

    # Calculate burndown health
    if args.burndown_ideal and args.burndown_actual:
        results['burndown'] = calculator.calculate_burndown_health(
            args.burndown_ideal, args.burndown_actual
        )

    # Generate insights if we have enough data
    if 'velocity' in results and 'completion' in results and 'capacity' in results:
        results['insights'] = calculator.generate_sprint_insights(
            results['velocity'],
            results['completion'],
            results['capacity']
        )
        results['health_score'] = calculator.calculate_sprint_health_score(
            results['velocity'],
            results['completion'],
            results['capacity']
        )

    # Output results
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        calculator.print_metrics_report(results)

if __name__ == "__main__":
    main()
