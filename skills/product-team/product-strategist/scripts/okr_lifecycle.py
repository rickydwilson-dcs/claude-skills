#!/usr/bin/env python3
"""
OKR Lifecycle Manager
Track, score, and analyze OKR progress throughout the quarter

Complements okr_cascade_generator.py by managing the ongoing OKR lifecycle:
- Weekly check-ins with progress tracking
- Initiative linking and coverage analysis
- End-of-quarter grading (0.0-1.0 scale)
- Retrospective generation
- Quarter-over-quarter comparison
"""

import argparse
import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Exit codes
EXIT_SUCCESS = 0
EXIT_INVALID_ARGS = 1
EXIT_FILE_NOT_FOUND = 2
EXIT_INVALID_JSON = 3
EXIT_WRITE_ERROR = 4
EXIT_VALIDATION_ERROR = 5
EXIT_KR_NOT_FOUND = 6


class OKRLifecycleManager:
    """Manage OKR lifecycle: check-ins, tracking, grading, and analysis"""

    # Scoring thresholds (from okr_methodology.md)
    SCORE_THRESHOLDS = {
        'exceeded': (1.0, 1.0),
        'green': (0.7, 0.99),
        'yellow': (0.4, 0.69),
        'red': (0.0, 0.39)
    }
    TARGET_SCORE = 0.7
    QUARTER_WEEKS = 12

    def __init__(self, verbose: bool = False):
        """Initialize with optional verbose logging"""
        if verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("OKRLifecycleManager initialized")

    def load_okrs(self, filepath: str) -> Dict:
        """Load OKR file, initializing lifecycle section if missing"""
        logger.debug(f"Loading OKRs from: {filepath}")

        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            logger.error(f"File not found: {filepath}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON: {e}")
            raise

        # Initialize lifecycle section if missing
        if 'lifecycle' not in data:
            logger.debug("Initializing lifecycle section")
            data['lifecycle'] = {
                'version': '1.0.0',
                'last_updated': datetime.now().isoformat(),
                'checkins': [],
                'initiatives': [],
                'grades': {},
                'retrospectives': []
            }

        return data

    def save_okrs(self, filepath: str, data: Dict) -> None:
        """Save updated OKR data back to file"""
        logger.debug(f"Saving OKRs to: {filepath}")

        data['lifecycle']['last_updated'] = datetime.now().isoformat()

        try:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save: {e}")
            raise

    def find_kr(self, data: Dict, kr_id: str) -> Tuple[Optional[Dict], Optional[str]]:
        """Find a KR by ID across all levels, return (kr_dict, level)"""
        okrs = data.get('okrs', {})

        # Search company level
        if 'company' in okrs:
            for obj in okrs['company'].get('objectives', []):
                for kr in obj.get('key_results', []):
                    if kr.get('id') == kr_id:
                        return kr, 'company'

        # Search product level
        if 'product' in okrs:
            for obj in okrs['product'].get('objectives', []):
                for kr in obj.get('key_results', []):
                    if kr.get('id') == kr_id:
                        return kr, 'product'

        # Search team level
        if 'teams' in okrs:
            for team in okrs['teams']:
                for obj in team.get('objectives', []):
                    for kr in obj.get('key_results', []):
                        if kr.get('id') == kr_id:
                            return kr, f"team:{team.get('team', 'unknown')}"

        return None, None

    def get_all_krs(self, data: Dict) -> List[Tuple[Dict, str, str]]:
        """Get all KRs with their objective ID and level"""
        krs = []
        okrs = data.get('okrs', {})

        # Company level
        if 'company' in okrs:
            for obj in okrs['company'].get('objectives', []):
                for kr in obj.get('key_results', []):
                    krs.append((kr, obj.get('id', ''), 'company'))

        # Product level
        if 'product' in okrs:
            for obj in okrs['product'].get('objectives', []):
                for kr in obj.get('key_results', []):
                    krs.append((kr, obj.get('id', ''), 'product'))

        # Team level
        if 'teams' in okrs:
            for team in okrs['teams']:
                for obj in team.get('objectives', []):
                    for kr in obj.get('key_results', []):
                        krs.append((kr, obj.get('id', ''), f"team:{team.get('team', '')}"))

        return krs

    def get_current_week(self) -> int:
        """Calculate current week in the quarter (1-12)"""
        now = datetime.now()
        quarter_start_month = ((now.month - 1) // 3) * 3 + 1
        quarter_start = datetime(now.year, quarter_start_month, 1)
        days_elapsed = (now - quarter_start).days
        week = min(self.QUARTER_WEEKS, max(1, (days_elapsed // 7) + 1))
        return week

    def calculate_progress(self, current: float, baseline: float, target: float) -> float:
        """Calculate progress percentage toward target"""
        if target == baseline:
            return 100.0 if current >= target else 0.0
        progress = ((current - baseline) / (target - baseline)) * 100
        return round(max(0.0, progress), 1)

    def calculate_velocity(self, checkins: List[Dict]) -> float:
        """Calculate average weekly velocity from check-in history"""
        if len(checkins) < 2:
            return 0.0

        velocities = []
        for i in range(1, len(checkins)):
            prev = checkins[i - 1]
            curr = checkins[i]
            week_diff = curr.get('week', 0) - prev.get('week', 0)
            if week_diff > 0:
                value_diff = curr.get('current_value', 0) - prev.get('current_value', 0)
                velocities.append(value_diff / week_diff)

        return round(sum(velocities) / len(velocities), 2) if velocities else 0.0

    def project_end_value(self, current: float, velocity: float, weeks_remaining: int) -> float:
        """Project end-of-quarter value based on current velocity"""
        return round(current + (velocity * weeks_remaining), 1)

    def determine_status(self, progress: float, confidence: float,
                         projected: float, target: float) -> str:
        """Determine KR status: on_track, at_risk, off_track"""
        projected_pct = (projected / target * 100) if target > 0 else 0

        if confidence >= 0.7 and (progress >= 70 or projected_pct >= 70):
            return 'on_track'
        elif confidence >= 0.4 and (progress >= 40 or projected_pct >= 50):
            return 'at_risk'
        else:
            return 'off_track'

    def record_checkin(self, data: Dict, kr_id: str, current_value: float,
                       confidence: float, notes: str = '', week: int = None) -> Dict:
        """Record a weekly check-in for a specific KR"""
        kr, level = self.find_kr(data, kr_id)
        if not kr:
            raise ValueError(f"KR not found: {kr_id}")

        baseline = kr.get('current', 0)
        target = kr.get('target', 100)

        # Get previous check-ins for this KR
        checkins = [c for c in data['lifecycle']['checkins'] if c['kr_id'] == kr_id]
        checkins.sort(key=lambda x: x.get('week', 0))

        previous_value = checkins[-1]['current_value'] if checkins else baseline

        # Calculate metrics
        current_week = week or self.get_current_week()
        progress = self.calculate_progress(current_value, baseline, target)
        velocity = current_value - previous_value
        weeks_remaining = self.QUARTER_WEEKS - current_week

        # Calculate average velocity for projection
        all_checkins = checkins + [{'week': current_week, 'current_value': current_value}]
        avg_velocity = self.calculate_velocity(all_checkins)
        projected = self.project_end_value(current_value, avg_velocity, weeks_remaining)

        status = self.determine_status(progress, confidence, projected, target)

        # Create check-in record
        checkin = {
            'id': f"CHK-{len(data['lifecycle']['checkins']) + 1:03d}",
            'kr_id': kr_id,
            'timestamp': datetime.now().isoformat(),
            'week': current_week,
            'current_value': current_value,
            'previous_value': previous_value,
            'target_value': target,
            'confidence': confidence,
            'notes': notes,
            'progress_pct': progress,
            'velocity': velocity,
            'avg_velocity': avg_velocity,
            'projected_end_value': projected,
            'status': status
        }

        data['lifecycle']['checkins'].append(checkin)
        logger.debug(f"Recorded check-in: {checkin['id']} for {kr_id}")

        return checkin

    def get_status_dashboard(self, data: Dict, level: str = 'all',
                             status_filter: str = None) -> Dict:
        """Generate current progress dashboard across all OKRs"""
        all_krs = self.get_all_krs(data)
        checkins = data['lifecycle'].get('checkins', [])

        dashboard = {
            'quarter': data.get('okrs', {}).get('company', {}).get('quarter', 'Unknown'),
            'generated_at': datetime.now().isoformat(),
            'summary': {
                'total_objectives': 0,
                'total_krs': 0,
                'health_score': 0,
                'on_track': 0,
                'at_risk': 0,
                'off_track': 0,
                'no_checkins': 0
            },
            'by_level': {
                'company': [],
                'product': [],
                'teams': []
            },
            'alerts': []
        }

        # Count objectives
        okrs = data.get('okrs', {})
        if 'company' in okrs:
            dashboard['summary']['total_objectives'] += len(okrs['company'].get('objectives', []))
        if 'product' in okrs:
            dashboard['summary']['total_objectives'] += len(okrs['product'].get('objectives', []))
        if 'teams' in okrs:
            for team in okrs['teams']:
                dashboard['summary']['total_objectives'] += len(team.get('objectives', []))

        # Process each KR
        kr_statuses = []
        current_week = self.get_current_week()

        for kr, obj_id, kr_level in all_krs:
            kr_id = kr.get('id', '')

            # Filter by level
            if level != 'all':
                if level == 'company' and kr_level != 'company':
                    continue
                elif level == 'product' and kr_level != 'product':
                    continue
                elif level == 'team' and not kr_level.startswith('team:'):
                    continue

            # Get latest check-in for this KR
            kr_checkins = [c for c in checkins if c['kr_id'] == kr_id]
            kr_checkins.sort(key=lambda x: x.get('week', 0), reverse=True)

            if kr_checkins:
                latest = kr_checkins[0]
                status = latest.get('status', 'unknown')
                progress = latest.get('progress_pct', 0)
                confidence = latest.get('confidence', 0)
                last_checkin_week = latest.get('week', 0)

                # Check for stale check-ins
                if current_week - last_checkin_week >= 2:
                    dashboard['alerts'].append({
                        'kr_id': kr_id,
                        'type': 'stale_checkin',
                        'reason': f'No check-in in {current_week - last_checkin_week} weeks'
                    })

                # Check for low confidence
                if confidence < 0.5:
                    dashboard['alerts'].append({
                        'kr_id': kr_id,
                        'type': 'low_confidence',
                        'reason': f'Confidence below 0.5 ({confidence})'
                    })
            else:
                status = 'no_checkin'
                progress = 0
                confidence = 0
                last_checkin_week = None
                dashboard['summary']['no_checkins'] += 1
                dashboard['alerts'].append({
                    'kr_id': kr_id,
                    'type': 'no_checkin',
                    'reason': 'No check-ins recorded'
                })

            # Filter by status
            if status_filter and status != status_filter:
                continue

            kr_info = {
                'kr_id': kr_id,
                'title': kr.get('title', ''),
                'objective_id': obj_id,
                'baseline': kr.get('current', 0),
                'target': kr.get('target', 0),
                'progress_pct': progress,
                'confidence': confidence,
                'status': status,
                'last_checkin_week': last_checkin_week
            }

            # Add to appropriate level
            if kr_level == 'company':
                dashboard['by_level']['company'].append(kr_info)
            elif kr_level == 'product':
                dashboard['by_level']['product'].append(kr_info)
            else:
                dashboard['by_level']['teams'].append(kr_info)

            dashboard['summary']['total_krs'] += 1
            kr_statuses.append(status)

            if status == 'on_track':
                dashboard['summary']['on_track'] += 1
            elif status == 'at_risk':
                dashboard['summary']['at_risk'] += 1
            elif status == 'off_track':
                dashboard['summary']['off_track'] += 1

        # Calculate health score
        total = len(kr_statuses)
        if total > 0:
            on_track_pct = dashboard['summary']['on_track'] / total
            at_risk_pct = dashboard['summary']['at_risk'] / total
            health = (on_track_pct * 1.0) + (at_risk_pct * 0.5)
            dashboard['summary']['health_score'] = round(health * 100, 1)

        return dashboard

    def link_initiative(self, data: Dict, kr_id: str, name: str,
                        contribution_pct: int, status: str = 'not_started') -> Dict:
        """Link an initiative to a KR"""
        kr, _ = self.find_kr(data, kr_id)
        if not kr:
            raise ValueError(f"KR not found: {kr_id}")

        if contribution_pct < 1 or contribution_pct > 100:
            raise ValueError("Contribution must be between 1 and 100")

        initiative = {
            'id': f"INIT-{len(data['lifecycle']['initiatives']) + 1:03d}",
            'name': name,
            'kr_id': kr_id,
            'contribution_pct': contribution_pct,
            'status': status,
            'completion_pct': 0,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }

        data['lifecycle']['initiatives'].append(initiative)
        logger.debug(f"Linked initiative: {initiative['id']} to {kr_id}")

        return initiative

    def list_initiatives(self, data: Dict, kr_id: str = None) -> List[Dict]:
        """List all initiatives, optionally filtered by KR"""
        initiatives = data['lifecycle'].get('initiatives', [])

        if kr_id:
            return [i for i in initiatives if i['kr_id'] == kr_id]
        return initiatives

    def update_initiative(self, data: Dict, initiative_id: str, **updates) -> Dict:
        """Update an existing initiative"""
        for init in data['lifecycle']['initiatives']:
            if init['id'] == initiative_id:
                for key, value in updates.items():
                    if key in init:
                        init[key] = value
                init['updated_at'] = datetime.now().isoformat()
                return init

        raise ValueError(f"Initiative not found: {initiative_id}")

    def get_initiative_coverage(self, data: Dict) -> Dict:
        """Analyze initiative coverage gaps"""
        all_krs = self.get_all_krs(data)
        all_kr_ids = {kr.get('id') for kr, _, _ in all_krs}
        initiatives = data['lifecycle'].get('initiatives', [])

        # KRs with initiatives
        covered_kr_ids = set(i['kr_id'] for i in initiatives)
        uncovered_kr_ids = all_kr_ids - covered_kr_ids

        # Calculate contribution per KR
        kr_contributions = {}
        for init in initiatives:
            kr_id = init['kr_id']
            kr_contributions[kr_id] = kr_contributions.get(kr_id, 0) + init['contribution_pct']

        over_committed = {kr: pct for kr, pct in kr_contributions.items() if pct > 100}
        under_committed = {kr: pct for kr, pct in kr_contributions.items() if pct < 50}

        return {
            'total_krs': len(all_kr_ids),
            'covered_krs': len(covered_kr_ids),
            'coverage_pct': round(len(covered_kr_ids) / len(all_kr_ids) * 100, 1) if all_kr_ids else 0,
            'uncovered_krs': list(uncovered_kr_ids),
            'over_committed': over_committed,
            'under_committed': under_committed,
            'total_initiatives': len(initiatives)
        }

    def auto_calculate_score(self, baseline: float, final: float, target: float) -> float:
        """Auto-calculate score based on final value vs target"""
        if target == baseline:
            return 1.0 if final >= target else 0.0

        progress = (final - baseline) / (target - baseline)
        return min(1.0, max(0.0, round(progress, 2)))

    def get_score_color(self, score: float) -> str:
        """Return color category for score"""
        if score >= 1.0:
            return 'exceeded'
        elif score >= 0.7:
            return 'green'
        elif score >= 0.4:
            return 'yellow'
        else:
            return 'red'

    def grade_kr(self, data: Dict, kr_id: str, score: float = None,
                 final_value: float = None, auto: bool = False, notes: str = '') -> Dict:
        """Grade a specific KR with manual or auto-calculated score"""
        kr, _ = self.find_kr(data, kr_id)
        if not kr:
            raise ValueError(f"KR not found: {kr_id}")

        baseline = kr.get('current', 0)
        target = kr.get('target', 100)

        # Determine final value
        if final_value is None:
            # Use latest check-in value
            checkins = [c for c in data['lifecycle']['checkins'] if c['kr_id'] == kr_id]
            if checkins:
                checkins.sort(key=lambda x: x.get('week', 0), reverse=True)
                final_value = checkins[0].get('current_value', baseline)
            else:
                final_value = baseline

        # Calculate or use provided score
        if auto or score is None:
            calculated_score = self.auto_calculate_score(baseline, final_value, target)
            auto_calculated = True
        else:
            calculated_score = max(0.0, min(1.0, score))
            auto_calculated = False

        grade = {
            'kr_id': kr_id,
            'baseline_value': baseline,
            'final_value': final_value,
            'target_value': target,
            'score': calculated_score,
            'color': self.get_score_color(calculated_score),
            'auto_calculated': auto_calculated,
            'notes': notes,
            'graded_at': datetime.now().isoformat()
        }

        # Initialize grades if needed
        if 'grades' not in data['lifecycle'] or not isinstance(data['lifecycle']['grades'], dict):
            data['lifecycle']['grades'] = {
                'quarter': data.get('okrs', {}).get('company', {}).get('quarter', 'Unknown'),
                'kr_grades': [],
                'objective_scores': {},
                'quarter_score': 0,
                'target_met': False
            }

        # Remove existing grade for this KR if present
        data['lifecycle']['grades']['kr_grades'] = [
            g for g in data['lifecycle']['grades'].get('kr_grades', [])
            if g['kr_id'] != kr_id
        ]

        data['lifecycle']['grades']['kr_grades'].append(grade)
        data['lifecycle']['grades']['graded_at'] = datetime.now().isoformat()

        # Recalculate objective and quarter scores
        self._recalculate_scores(data)

        return grade

    def grade_all_krs(self, data: Dict, auto: bool = True) -> Dict:
        """Grade all KRs at once"""
        all_krs = self.get_all_krs(data)
        grades = []

        for kr, _, _ in all_krs:
            kr_id = kr.get('id')
            if kr_id:
                grade = self.grade_kr(data, kr_id, auto=auto)
                grades.append(grade)

        return data['lifecycle']['grades']

    def _recalculate_scores(self, data: Dict) -> None:
        """Recalculate objective and quarter scores from KR grades"""
        grades = data['lifecycle'].get('grades', {})
        kr_grades = grades.get('kr_grades', [])

        if not kr_grades:
            return

        # Group grades by objective
        obj_grades = {}
        for grade in kr_grades:
            kr_id = grade['kr_id']
            # Extract objective ID (e.g., CO-1 from CO-1-KR1)
            parts = kr_id.split('-')
            if len(parts) >= 2:
                obj_id = f"{parts[0]}-{parts[1]}"
                if obj_id not in obj_grades:
                    obj_grades[obj_id] = []
                obj_grades[obj_id].append(grade['score'])

        # Calculate objective scores
        objective_scores = {}
        for obj_id, scores in obj_grades.items():
            objective_scores[obj_id] = round(sum(scores) / len(scores), 2)

        grades['objective_scores'] = objective_scores

        # Calculate quarter score
        if objective_scores:
            quarter_score = round(sum(objective_scores.values()) / len(objective_scores), 2)
            grades['quarter_score'] = quarter_score
            grades['target_met'] = quarter_score >= self.TARGET_SCORE

        # Summary by color
        color_counts = {'exceeded': 0, 'green': 0, 'yellow': 0, 'red': 0}
        for grade in kr_grades:
            color = grade.get('color', 'red')
            color_counts[color] = color_counts.get(color, 0) + 1
        grades['summary'] = color_counts

    def generate_retrospective(self, data: Dict, template: str = 'full') -> Dict:
        """Generate retrospective analysis for the quarter"""
        grades = data['lifecycle'].get('grades', {})
        kr_grades = grades.get('kr_grades', [])

        if not kr_grades:
            return {'error': 'No grades found. Run grade command first.'}

        retro = {
            'quarter': grades.get('quarter', 'Unknown'),
            'created_at': datetime.now().isoformat(),
            'template': template,
            'overall_score': grades.get('quarter_score', 0),
            'target_met': grades.get('target_met', False),
            'what_worked': [],
            'what_didnt': [],
            'patterns': {
                'consistently_strong': [],
                'consistently_weak': [],
                'improved': [],
                'declined': []
            },
            'lessons_learned': [],
            'next_quarter_recommendations': []
        }

        # Categorize KRs
        for grade in kr_grades:
            kr_id = grade['kr_id']
            score = grade['score']
            kr, _ = self.find_kr(data, kr_id)
            title = kr.get('title', kr_id) if kr else kr_id

            item = {
                'kr_id': kr_id,
                'title': title,
                'score': score,
                'color': grade.get('color', 'red')
            }

            if score >= 0.7:
                retro['what_worked'].append(item)
            elif score < 0.4:
                retro['what_didnt'].append(item)

        # Generate insights based on results
        if retro['what_worked']:
            retro['patterns']['consistently_strong'] = [
                w['kr_id'] for w in retro['what_worked'] if w['score'] >= 0.9
            ]

        if retro['what_didnt']:
            retro['patterns']['consistently_weak'] = [
                w['kr_id'] for w in retro['what_didnt'] if w['score'] < 0.3
            ]

        # Generate recommendations
        if retro['target_met']:
            retro['lessons_learned'].append('Team met overall target - maintain momentum')
            retro['next_quarter_recommendations'].append('Consider raising ambition level for next quarter')
        else:
            retro['lessons_learned'].append('Target not met - review goal-setting process')
            retro['next_quarter_recommendations'].append('Set more achievable targets or allocate more resources')

        if len(retro['what_didnt']) > len(retro['what_worked']):
            retro['lessons_learned'].append('More KRs underperformed than succeeded - review scope')
            retro['next_quarter_recommendations'].append('Focus on fewer, more impactful objectives')

        # Store retrospective
        data['lifecycle']['retrospectives'].append(retro)

        return retro

    def compare_quarters(self, current_data: Dict, previous_data: Dict,
                         metrics: List[str] = None) -> Dict:
        """Compare two quarters for trends and patterns"""
        current_grades = current_data['lifecycle'].get('grades', {})
        previous_grades = previous_data['lifecycle'].get('grades', {})

        comparison = {
            'quarters': {
                'current': current_grades.get('quarter', 'Unknown'),
                'previous': previous_grades.get('quarter', 'Unknown')
            },
            'generated_at': datetime.now().isoformat(),
            'score_comparison': {
                'current_score': current_grades.get('quarter_score', 0),
                'previous_score': previous_grades.get('quarter_score', 0),
                'delta': 0,
                'trend': 'stable'
            },
            'objective_trends': {},
            'kr_analysis': {
                'improved': [],
                'declined': [],
                'stable': [],
                'new': [],
                'removed': []
            },
            'recommendations': []
        }

        # Calculate score delta
        current_score = comparison['score_comparison']['current_score']
        previous_score = comparison['score_comparison']['previous_score']
        delta = round(current_score - previous_score, 2)
        comparison['score_comparison']['delta'] = delta

        if delta > 0.05:
            comparison['score_comparison']['trend'] = 'improving'
        elif delta < -0.05:
            comparison['score_comparison']['trend'] = 'declining'

        # Compare objective scores
        current_obj = current_grades.get('objective_scores', {})
        previous_obj = previous_grades.get('objective_scores', {})

        all_objectives = set(current_obj.keys()) | set(previous_obj.keys())
        for obj_id in all_objectives:
            curr = current_obj.get(obj_id, 0)
            prev = previous_obj.get(obj_id, 0)
            comparison['objective_trends'][obj_id] = {
                'current': curr,
                'previous': prev,
                'delta': round(curr - prev, 2)
            }

        # Compare KR grades
        current_kr_grades = {g['kr_id']: g for g in current_grades.get('kr_grades', [])}
        previous_kr_grades = {g['kr_id']: g for g in previous_grades.get('kr_grades', [])}

        all_krs = set(current_kr_grades.keys()) | set(previous_kr_grades.keys())

        for kr_id in all_krs:
            curr = current_kr_grades.get(kr_id)
            prev = previous_kr_grades.get(kr_id)

            if curr and prev:
                delta = curr['score'] - prev['score']
                if delta > 0.1:
                    comparison['kr_analysis']['improved'].append({
                        'kr_id': kr_id,
                        'previous_score': prev['score'],
                        'current_score': curr['score'],
                        'delta': round(delta, 2)
                    })
                elif delta < -0.1:
                    comparison['kr_analysis']['declined'].append({
                        'kr_id': kr_id,
                        'previous_score': prev['score'],
                        'current_score': curr['score'],
                        'delta': round(delta, 2)
                    })
                else:
                    comparison['kr_analysis']['stable'].append(kr_id)
            elif curr and not prev:
                comparison['kr_analysis']['new'].append(kr_id)
            elif prev and not curr:
                comparison['kr_analysis']['removed'].append(kr_id)

        # Generate recommendations
        if comparison['score_comparison']['trend'] == 'improving':
            comparison['recommendations'].append('Continue current momentum and practices')
        elif comparison['score_comparison']['trend'] == 'declining':
            comparison['recommendations'].append('Investigate root causes of declining performance')

        if comparison['kr_analysis']['improved']:
            comparison['recommendations'].append(
                f"Build on success: {len(comparison['kr_analysis']['improved'])} KRs improved"
            )

        if comparison['kr_analysis']['declined']:
            comparison['recommendations'].append(
                f"Address declining KRs: {len(comparison['kr_analysis']['declined'])} need attention"
            )

        return comparison


# =============================================================================
# Output Formatters
# =============================================================================

def format_checkin_text(checkin: Dict) -> str:
    """Format check-in result as human-readable text"""
    status_icons = {
        'on_track': '[===]',
        'at_risk': '[!!!]',
        'off_track': '[XXX]'
    }

    lines = [
        "=" * 60,
        "CHECK-IN RECORDED",
        "=" * 60,
        f"KR: {checkin['kr_id']}",
        f"Week: {checkin['week']} of 12",
        "",
        f"Current Value: {checkin['current_value']} (was {checkin['previous_value']})",
        f"Target: {checkin['target_value']}",
        f"Progress: {checkin['progress_pct']}%",
        "",
        f"Confidence: {checkin['confidence']}",
        f"Status: {status_icons.get(checkin['status'], '[???]')} {checkin['status'].upper()}",
        "",
        f"Weekly Velocity: {checkin['velocity']:+}",
        f"Avg Velocity: {checkin['avg_velocity']}",
        f"Projected End Value: {checkin['projected_end_value']}",
    ]

    if checkin.get('notes'):
        lines.extend(["", f"Notes: {checkin['notes']}"])

    return "\n".join(lines)


def format_status_text(dashboard: Dict) -> str:
    """Format status dashboard as human-readable text"""
    status_icons = {
        'on_track': '[===]',
        'at_risk': '[!!!]',
        'off_track': '[XXX]',
        'no_checkin': '[---]'
    }

    summary = dashboard['summary']

    lines = [
        "=" * 60,
        f"OKR LIFECYCLE DASHBOARD - {dashboard['quarter']}",
        "=" * 60,
        "",
        "SUMMARY",
        "-" * 40,
        f"Total Objectives: {summary['total_objectives']} | Total KRs: {summary['total_krs']}",
        f"Health Score: {summary['health_score']}% | Target: 70%",
        "",
        f"Status: {status_icons['on_track']} {summary['on_track']} On Track | "
        f"{status_icons['at_risk']} {summary['at_risk']} At Risk | "
        f"{status_icons['off_track']} {summary['off_track']} Off Track",
    ]

    if summary['no_checkins'] > 0:
        lines.append(f"         {status_icons['no_checkin']} {summary['no_checkins']} No Check-ins")

    # Company OKRs
    if dashboard['by_level']['company']:
        lines.extend(["", "COMPANY OKRs", "-" * 40])
        for kr in dashboard['by_level']['company']:
            icon = status_icons.get(kr['status'], '[???]')
            lines.append(
                f"  {icon} {kr['kr_id']}: {kr['title'][:40]}... | "
                f"Progress: {kr['progress_pct']}%"
            )

    # Product OKRs
    if dashboard['by_level']['product']:
        lines.extend(["", "PRODUCT OKRs", "-" * 40])
        for kr in dashboard['by_level']['product']:
            icon = status_icons.get(kr['status'], '[???]')
            lines.append(
                f"  {icon} {kr['kr_id']}: {kr['title'][:40]}... | "
                f"Progress: {kr['progress_pct']}%"
            )

    # Team OKRs
    if dashboard['by_level']['teams']:
        lines.extend(["", "TEAM OKRs", "-" * 40])
        for kr in dashboard['by_level']['teams']:
            icon = status_icons.get(kr['status'], '[???]')
            lines.append(
                f"  {icon} {kr['kr_id']}: {kr['title'][:40]}... | "
                f"Progress: {kr['progress_pct']}%"
            )

    # Alerts
    if dashboard['alerts']:
        lines.extend(["", "ALERTS", "-" * 40])
        for alert in dashboard['alerts'][:10]:  # Limit to 10 alerts
            lines.append(f"  ! {alert['kr_id']}: {alert['reason']}")

    return "\n".join(lines)


def format_initiatives_text(initiatives: List[Dict], coverage: Dict) -> str:
    """Format initiatives list as human-readable text"""
    lines = [
        "=" * 60,
        "INITIATIVE COVERAGE REPORT",
        "=" * 60,
        "",
        "COVERAGE SUMMARY",
        "-" * 40,
        f"Total KRs: {coverage['total_krs']}",
        f"KRs with Initiatives: {coverage['covered_krs']} ({coverage['coverage_pct']}%)",
        f"Total Initiatives: {coverage['total_initiatives']}",
    ]

    if coverage['uncovered_krs']:
        lines.extend(["", "UNCOVERED KRs (need initiatives):", "-" * 40])
        for kr_id in coverage['uncovered_krs'][:10]:
            lines.append(f"  - {kr_id}")

    if coverage['over_committed']:
        lines.extend(["", "OVER-COMMITTED KRs (>100% allocation):", "-" * 40])
        for kr_id, pct in coverage['over_committed'].items():
            lines.append(f"  ! {kr_id}: {pct}% allocated")

    if coverage['under_committed']:
        lines.extend(["", "UNDER-COMMITTED KRs (<50% allocation):", "-" * 40])
        for kr_id, pct in coverage['under_committed'].items():
            lines.append(f"  - {kr_id}: {pct}% allocated")

    if initiatives:
        lines.extend(["", "ALL INITIATIVES", "-" * 40])
        for init in initiatives:
            status_icon = {'not_started': '[ ]', 'in_progress': '[~]', 'completed': '[x]', 'blocked': '[!]'}
            icon = status_icon.get(init['status'], '[?]')
            lines.append(
                f"  {icon} {init['id']}: {init['name']} -> {init['kr_id']} ({init['contribution_pct']}%)"
            )

    return "\n".join(lines)


def format_grade_text(grades: Dict) -> str:
    """Format grades as human-readable text"""
    color_icons = {
        'exceeded': '[+++]',
        'green': '[===]',
        'yellow': '[~~~]',
        'red': '[---]'
    }

    lines = [
        "=" * 60,
        f"OKR GRADES - {grades.get('quarter', 'Unknown')}",
        "=" * 60,
        "",
        "QUARTER SUMMARY",
        "-" * 40,
        f"Quarter Score: {grades.get('quarter_score', 0)} (Target: 0.7)",
        f"Target Met: {'YES' if grades.get('target_met') else 'NO'}",
    ]

    summary = grades.get('summary', {})
    if summary:
        lines.extend([
            "",
            f"Exceeded (1.0): {summary.get('exceeded', 0)}",
            f"Green (0.7-0.9): {summary.get('green', 0)}",
            f"Yellow (0.4-0.6): {summary.get('yellow', 0)}",
            f"Red (0.0-0.3): {summary.get('red', 0)}",
        ])

    # Objective scores
    obj_scores = grades.get('objective_scores', {})
    if obj_scores:
        lines.extend(["", "OBJECTIVE SCORES", "-" * 40])
        for obj_id, score in sorted(obj_scores.items()):
            lines.append(f"  {obj_id}: {score}")

    # KR grades
    kr_grades = grades.get('kr_grades', [])
    if kr_grades:
        lines.extend(["", "KEY RESULT GRADES", "-" * 40])
        for grade in sorted(kr_grades, key=lambda x: x['kr_id']):
            icon = color_icons.get(grade['color'], '[???]')
            lines.append(
                f"  {icon} {grade['kr_id']}: {grade['score']} "
                f"({grade['final_value']}/{grade['target_value']})"
            )

    return "\n".join(lines)


def format_retro_text(retro: Dict) -> str:
    """Format retrospective as human-readable text"""
    lines = [
        "=" * 60,
        f"RETROSPECTIVE - {retro.get('quarter', 'Unknown')}",
        "=" * 60,
        "",
        f"Overall Score: {retro.get('overall_score', 0)}",
        f"Target Met: {'YES' if retro.get('target_met') else 'NO'}",
    ]

    # What worked
    if retro['what_worked']:
        lines.extend(["", "WHAT WORKED (Score >= 0.7)", "-" * 40])
        for item in retro['what_worked']:
            lines.append(f"  [+] {item['kr_id']}: {item['title'][:50]}... ({item['score']})")

    # What didn't work
    if retro['what_didnt']:
        lines.extend(["", "WHAT DIDN'T WORK (Score < 0.4)", "-" * 40])
        for item in retro['what_didnt']:
            lines.append(f"  [-] {item['kr_id']}: {item['title'][:50]}... ({item['score']})")

    # Lessons learned
    if retro['lessons_learned']:
        lines.extend(["", "LESSONS LEARNED", "-" * 40])
        for lesson in retro['lessons_learned']:
            lines.append(f"  * {lesson}")

    # Recommendations
    if retro['next_quarter_recommendations']:
        lines.extend(["", "NEXT QUARTER RECOMMENDATIONS", "-" * 40])
        for rec in retro['next_quarter_recommendations']:
            lines.append(f"  -> {rec}")

    return "\n".join(lines)


def format_compare_text(comparison: Dict) -> str:
    """Format comparison as human-readable text"""
    trend_icons = {'improving': '[+]', 'declining': '[-]', 'stable': '[=]'}

    quarters = comparison['quarters']
    score_comp = comparison['score_comparison']

    lines = [
        "=" * 60,
        f"QUARTER COMPARISON: {quarters['previous']} vs {quarters['current']}",
        "=" * 60,
        "",
        "SCORE COMPARISON",
        "-" * 40,
        f"Previous Score: {score_comp['previous_score']}",
        f"Current Score: {score_comp['current_score']}",
        f"Delta: {score_comp['delta']:+.2f}",
        f"Trend: {trend_icons.get(score_comp['trend'], '[?]')} {score_comp['trend'].upper()}",
    ]

    # Objective trends
    obj_trends = comparison.get('objective_trends', {})
    if obj_trends:
        lines.extend(["", "OBJECTIVE TRENDS", "-" * 40])
        for obj_id, trend in sorted(obj_trends.items()):
            delta = trend['delta']
            icon = '[+]' if delta > 0.05 else '[-]' if delta < -0.05 else '[=]'
            lines.append(f"  {icon} {obj_id}: {trend['previous']} -> {trend['current']} ({delta:+.2f})")

    # KR analysis
    kr = comparison['kr_analysis']
    if kr['improved']:
        lines.extend(["", f"IMPROVED KRs ({len(kr['improved'])})", "-" * 40])
        for item in kr['improved'][:5]:
            lines.append(f"  [+] {item['kr_id']}: {item['previous_score']} -> {item['current_score']}")

    if kr['declined']:
        lines.extend(["", f"DECLINED KRs ({len(kr['declined'])})", "-" * 40])
        for item in kr['declined'][:5]:
            lines.append(f"  [-] {item['kr_id']}: {item['previous_score']} -> {item['current_score']}")

    # Recommendations
    if comparison['recommendations']:
        lines.extend(["", "RECOMMENDATIONS", "-" * 40])
        for rec in comparison['recommendations']:
            lines.append(f"  -> {rec}")

    return "\n".join(lines)


def format_json_output(data: Dict, subcommand: str) -> str:
    """Format any result as JSON with metadata"""
    result = {
        'metadata': {
            'tool': 'okr_lifecycle',
            'version': '1.0.0',
            'command': subcommand,
            'generated_at': datetime.now().isoformat()
        },
        'result': data
    }
    return json.dumps(result, indent=2)


def format_csv_output(data: Dict, subcommand: str) -> str:
    """Format tabular results as CSV"""
    import io
    csv_output = io.StringIO()

    if subcommand == 'status':
        csv_output.write('level,kr_id,title,objective_id,progress_pct,confidence,status,last_checkin_week\n')
        for level, krs in data.get('by_level', {}).items():
            for kr in krs:
                csv_output.write(
                    f"{level},{kr['kr_id']},\"{kr['title']}\",{kr['objective_id']},"
                    f"{kr['progress_pct']},{kr['confidence']},{kr['status']},{kr['last_checkin_week']}\n"
                )

    elif subcommand == 'grade':
        csv_output.write('kr_id,baseline,final,target,score,color,auto_calculated\n')
        for grade in data.get('kr_grades', []):
            csv_output.write(
                f"{grade['kr_id']},{grade['baseline_value']},{grade['final_value']},"
                f"{grade['target_value']},{grade['score']},{grade['color']},{grade['auto_calculated']}\n"
            )

    elif subcommand == 'initiatives':
        csv_output.write('id,name,kr_id,contribution_pct,status,completion_pct\n')
        for init in data:
            csv_output.write(
                f"{init['id']},\"{init['name']}\",{init['kr_id']},"
                f"{init['contribution_pct']},{init['status']},{init['completion_pct']}\n"
            )

    return csv_output.getvalue()


# =============================================================================
# Main CLI
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='OKR Lifecycle Manager - Track, score, and analyze OKR progress',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Record weekly check-in
  %(prog)s checkin okrs.json CO-1-KR1 108000 --confidence 0.8

  # View status dashboard
  %(prog)s status okrs.json

  # Link initiative to KR
  %(prog)s initiatives okrs.json link --kr-id CO-1-KR1 --name "Q1 Campaign"

  # Grade all KRs automatically
  %(prog)s grade okrs.json --all --auto

  # Generate retrospective
  %(prog)s retro okrs.json

  # Compare quarters
  %(prog)s compare q1_okrs.json q4_okrs.json

For more information, see the skill documentation.
        """
    )

    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0.0')

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # -------------------------------------------------------------------------
    # checkin subcommand
    # -------------------------------------------------------------------------
    checkin_parser = subparsers.add_parser('checkin', help='Record weekly progress check-in')
    checkin_parser.add_argument('okr_file', help='Path to OKR JSON file')
    checkin_parser.add_argument('kr_id', help='Key Result ID (e.g., CO-1-KR1)')
    checkin_parser.add_argument('current_value', type=float, help='Current metric value')
    checkin_parser.add_argument('--confidence', type=float, default=0.7,
                                help='Confidence level 0.0-1.0 (default: 0.7)')
    checkin_parser.add_argument('--notes', default='', help='Check-in notes')
    checkin_parser.add_argument('--week', type=int, help='Override week number')
    checkin_parser.add_argument('-o', '--output', choices=['text', 'json'], default='text',
                                help='Output format')
    checkin_parser.add_argument('-f', '--file', help='Write output to file')

    # -------------------------------------------------------------------------
    # status subcommand
    # -------------------------------------------------------------------------
    status_parser = subparsers.add_parser('status', help='View current OKR progress dashboard')
    status_parser.add_argument('okr_file', help='Path to OKR JSON file')
    status_parser.add_argument('--level', choices=['all', 'company', 'product', 'team'],
                               default='all', help='Filter by OKR level')
    status_parser.add_argument('--filter', choices=['on_track', 'at_risk', 'off_track'],
                               help='Filter by status')
    status_parser.add_argument('-o', '--output', choices=['text', 'json', 'csv'], default='text',
                               help='Output format')
    status_parser.add_argument('-f', '--file', help='Write output to file')

    # -------------------------------------------------------------------------
    # initiatives subcommand
    # -------------------------------------------------------------------------
    init_parser = subparsers.add_parser('initiatives', help='Link and manage OKR initiatives')
    init_parser.add_argument('okr_file', help='Path to OKR JSON file')
    init_parser.add_argument('action', choices=['link', 'list', 'update', 'coverage'],
                             help='Action to perform')
    init_parser.add_argument('--kr-id', help='Key Result ID to link')
    init_parser.add_argument('--name', help='Initiative name')
    init_parser.add_argument('--contribution', type=int, default=50,
                             help='Contribution percentage (1-100)')
    init_parser.add_argument('--status', choices=['not_started', 'in_progress', 'completed', 'blocked'],
                             default='not_started', help='Initiative status')
    init_parser.add_argument('--initiative-id', help='Initiative ID (for update)')
    init_parser.add_argument('--completion', type=int, help='Completion percentage (0-100)')
    init_parser.add_argument('-o', '--output', choices=['text', 'json', 'csv'], default='text',
                             help='Output format')
    init_parser.add_argument('-f', '--file', help='Write output to file')

    # -------------------------------------------------------------------------
    # grade subcommand
    # -------------------------------------------------------------------------
    grade_parser = subparsers.add_parser('grade', help='Score OKRs at end of quarter')
    grade_parser.add_argument('okr_file', help='Path to OKR JSON file')
    grade_parser.add_argument('--kr-id', help='Specific KR to grade')
    grade_parser.add_argument('--score', type=float, help='Manual score 0.0-1.0')
    grade_parser.add_argument('--final-value', type=float, help='Final metric value')
    grade_parser.add_argument('--auto', action='store_true',
                              help='Auto-calculate score from values')
    grade_parser.add_argument('--all', action='store_true', help='Grade all KRs')
    grade_parser.add_argument('--notes', default='', help='Grading notes')
    grade_parser.add_argument('-o', '--output', choices=['text', 'json', 'csv'], default='text',
                              help='Output format')
    grade_parser.add_argument('-f', '--file', help='Write output to file')

    # -------------------------------------------------------------------------
    # retro subcommand
    # -------------------------------------------------------------------------
    retro_parser = subparsers.add_parser('retro', help='Generate retrospective analysis')
    retro_parser.add_argument('okr_file', help='Path to OKR JSON file')
    retro_parser.add_argument('--template', choices=['full', 'summary', 'lessons'],
                              default='full', help='Retrospective template')
    retro_parser.add_argument('-o', '--output', choices=['text', 'json'], default='text',
                              help='Output format')
    retro_parser.add_argument('-f', '--file', help='Write output to file')

    # -------------------------------------------------------------------------
    # compare subcommand
    # -------------------------------------------------------------------------
    compare_parser = subparsers.add_parser('compare', help='Compare quarter-over-quarter performance')
    compare_parser.add_argument('current_file', help='Current quarter OKR file')
    compare_parser.add_argument('previous_file', help='Previous quarter OKR file')
    compare_parser.add_argument('-o', '--output', choices=['text', 'json'], default='text',
                                help='Output format')
    compare_parser.add_argument('-f', '--file', help='Write output to file')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(EXIT_INVALID_ARGS)

    try:
        manager = OKRLifecycleManager(verbose=args.verbose)
        output = ""

        # ---------------------------------------------------------------------
        # Execute commands
        # ---------------------------------------------------------------------

        if args.command == 'checkin':
            data = manager.load_okrs(args.okr_file)
            checkin = manager.record_checkin(
                data, args.kr_id, args.current_value,
                args.confidence, args.notes, args.week
            )
            manager.save_okrs(args.okr_file, data)

            if args.output == 'json':
                output = format_json_output(checkin, 'checkin')
            else:
                output = format_checkin_text(checkin)

        elif args.command == 'status':
            data = manager.load_okrs(args.okr_file)
            dashboard = manager.get_status_dashboard(data, args.level, args.filter)

            if args.output == 'json':
                output = format_json_output(dashboard, 'status')
            elif args.output == 'csv':
                output = format_csv_output(dashboard, 'status')
            else:
                output = format_status_text(dashboard)

        elif args.command == 'initiatives':
            data = manager.load_okrs(args.okr_file)

            if args.action == 'link':
                if not args.kr_id or not args.name:
                    print("Error: --kr-id and --name required for link action", file=sys.stderr)
                    sys.exit(EXIT_INVALID_ARGS)

                initiative = manager.link_initiative(
                    data, args.kr_id, args.name, args.contribution, args.status
                )
                manager.save_okrs(args.okr_file, data)
                result = initiative

            elif args.action == 'list':
                result = manager.list_initiatives(data, args.kr_id)

            elif args.action == 'update':
                if not args.initiative_id:
                    print("Error: --initiative-id required for update action", file=sys.stderr)
                    sys.exit(EXIT_INVALID_ARGS)

                updates = {}
                if args.status:
                    updates['status'] = args.status
                if args.completion is not None:
                    updates['completion_pct'] = args.completion

                result = manager.update_initiative(data, args.initiative_id, **updates)
                manager.save_okrs(args.okr_file, data)

            elif args.action == 'coverage':
                result = manager.get_initiative_coverage(data)

            coverage = manager.get_initiative_coverage(data)
            initiatives = manager.list_initiatives(data)

            if args.output == 'json':
                output = format_json_output({'initiatives': initiatives, 'coverage': coverage}, 'initiatives')
            elif args.output == 'csv':
                output = format_csv_output(initiatives, 'initiatives')
            else:
                output = format_initiatives_text(initiatives, coverage)

        elif args.command == 'grade':
            data = manager.load_okrs(args.okr_file)

            if args.all:
                grades = manager.grade_all_krs(data, auto=args.auto)
            elif args.kr_id:
                manager.grade_kr(
                    data, args.kr_id, args.score, args.final_value, args.auto, args.notes
                )
                grades = data['lifecycle']['grades']
            else:
                print("Error: --kr-id or --all required", file=sys.stderr)
                sys.exit(EXIT_INVALID_ARGS)

            manager.save_okrs(args.okr_file, data)

            if args.output == 'json':
                output = format_json_output(grades, 'grade')
            elif args.output == 'csv':
                output = format_csv_output(grades, 'grade')
            else:
                output = format_grade_text(grades)

        elif args.command == 'retro':
            data = manager.load_okrs(args.okr_file)
            retro = manager.generate_retrospective(data, args.template)
            manager.save_okrs(args.okr_file, data)

            if args.output == 'json':
                output = format_json_output(retro, 'retro')
            else:
                output = format_retro_text(retro)

        elif args.command == 'compare':
            current_data = manager.load_okrs(args.current_file)
            previous_data = manager.load_okrs(args.previous_file)
            comparison = manager.compare_quarters(current_data, previous_data)

            if args.output == 'json':
                output = format_json_output(comparison, 'compare')
            else:
                output = format_compare_text(comparison)

        # ---------------------------------------------------------------------
        # Output results
        # ---------------------------------------------------------------------

        if hasattr(args, 'file') and args.file:
            try:
                with open(args.file, 'w') as f:
                    f.write(output)
                print(f"Output saved to: {args.file}")
            except Exception as e:
                print(f"Error writing output file: {e}", file=sys.stderr)
                sys.exit(EXIT_WRITE_ERROR)
        else:
            print(output)

        sys.exit(EXIT_SUCCESS)

    except FileNotFoundError as e:
        print(f"Error: File not found - {e}", file=sys.stderr)
        sys.exit(EXIT_FILE_NOT_FOUND)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON - {e}", file=sys.stderr)
        sys.exit(EXIT_INVALID_JSON)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(EXIT_VALIDATION_ERROR)
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
