#!/usr/bin/env python3
"""
KPI Calculator - Calculate process KPIs and efficiency metrics

This tool calculates standard process KPIs including cycle time, throughput,
error rates, and Six Sigma metrics from process execution data.

Usage:
    python kpi_calculator.py executions.csv --baseline baseline.json
    python kpi_calculator.py executions.json --output markdown --include-charts
    python kpi_calculator.py executions.csv --process process.json --period 30
    python kpi_calculator.py --help

Input Formats:
    - JSON: List of execution objects with timestamps and outcomes
    - CSV: Columns for execution_id, start_time, end_time, status, cost

Exit Codes:
    0 - Success
    1 - Validation error
    2 - Parse error
    3 - Calculation error
"""

import argparse
import json
import sys
import csv
import statistics
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import math
from collections import defaultdict

EXIT_SUCCESS = 0
EXIT_VALIDATION_ERROR = 1
EXIT_PARSE_ERROR = 2
EXIT_CALCULATION_ERROR = 3

class KPICalculator:
    """Calculates process KPIs and efficiency metrics"""

    def __init__(self, verbose: bool = False):
        """Initialize calculator with verbosity setting"""
        self.verbose = verbose

        # Six Sigma DPMO to Sigma Level lookup (approximate)
        self.sigma_lookup = [
            (691462, 1.0),
            (308538, 2.0),
            (158655, 2.5),
            (66807, 3.0),
            (22750, 3.5),
            (6210, 4.0),
            (1350, 4.5),
            (233, 5.0),
            (32, 5.5),
            (3.4, 6.0)
        ]

    def log(self, message: str):
        """Log verbose message"""
        if self.verbose:
            print(f"[INFO] {message}", file=sys.stderr)

    def parse_input_data(self, input_path: Path) -> List[Dict[str, Any]]:
        """Parse execution data from JSON or CSV file"""
        self.log(f"Parsing input file: {input_path}")

        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")

        suffix = input_path.suffix.lower()

        if suffix == '.json':
            return self._parse_json(input_path)
        elif suffix == '.csv':
            return self._parse_csv(input_path)
        else:
            raise ValueError(f"Unsupported file format: {suffix}. Use .json or .csv")

    def _parse_json(self, path: Path) -> List[Dict[str, Any]]:
        """Parse JSON execution data"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if isinstance(data, dict) and 'executions' in data:
                executions = data['executions']
            elif isinstance(data, list):
                executions = data
            else:
                raise ValueError("JSON must be list or dict with 'executions' key")

            self.log(f"Parsed {len(executions)} executions from JSON")
            return executions

        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {e}")

    def _parse_csv(self, path: Path) -> List[Dict[str, Any]]:
        """Parse CSV execution data"""
        executions = []

        try:
            with open(path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    executions.append(row)

            self.log(f"Parsed {len(executions)} executions from CSV")
            return executions

        except csv.Error as e:
            raise ValueError(f"Invalid CSV: {e}")

    def parse_baseline(self, baseline_path: Optional[Path]) -> Optional[Dict[str, Any]]:
        """Parse baseline metrics from JSON file"""
        if not baseline_path:
            return None

        self.log(f"Parsing baseline: {baseline_path}")

        if not baseline_path.exists():
            raise FileNotFoundError(f"Baseline file not found: {baseline_path}")

        try:
            with open(baseline_path, 'r', encoding='utf-8') as f:
                baseline = json.load(f)
            return baseline
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid baseline JSON: {e}")

    def parse_process_definition(self, process_path: Optional[Path]) -> Optional[Dict[str, Any]]:
        """Parse process definition from JSON file"""
        if not process_path:
            return None

        self.log(f"Parsing process definition: {process_path}")

        if not process_path.exists():
            raise FileNotFoundError(f"Process file not found: {process_path}")

        try:
            with open(process_path, 'r', encoding='utf-8') as f:
                process = json.load(f)
            return process
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid process JSON: {e}")

    def normalize_execution_data(self, executions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Normalize execution data to consistent format"""
        normalized = []

        for i, exec_data in enumerate(executions):
            try:
                normalized_exec = {
                    'execution_id': exec_data.get('execution_id') or exec_data.get('id') or f"EXC-{i+1}",
                    'start_time': self._parse_datetime(exec_data.get('start_time') or exec_data.get('start')),
                    'end_time': self._parse_datetime(exec_data.get('end_time') or exec_data.get('end')),
                    'status': exec_data.get('status', 'completed').lower(),
                    'cost': float(exec_data.get('cost', 0)),
                    'error': exec_data.get('error', False) or exec_data.get('status', '').lower() in ['error', 'failed'],
                    'rework': exec_data.get('rework', False) or exec_data.get('rework_required', False),
                    'notes': exec_data.get('notes', '')
                }

                # Calculate duration in hours
                if normalized_exec['start_time'] and normalized_exec['end_time']:
                    duration = normalized_exec['end_time'] - normalized_exec['start_time']
                    normalized_exec['duration_hours'] = duration.total_seconds() / 3600
                else:
                    normalized_exec['duration_hours'] = float(exec_data.get('duration_hours', 0))

                normalized.append(normalized_exec)

            except Exception as e:
                self.log(f"Warning: Skipping invalid execution record {i}: {e}")
                continue

        self.log(f"Normalized {len(normalized)} executions")
        return normalized

    def _parse_datetime(self, dt_str: Any) -> Optional[datetime]:
        """Parse datetime string in various formats"""
        if not dt_str:
            return None

        if isinstance(dt_str, datetime):
            return dt_str

        # Try common formats
        formats = [
            '%Y-%m-%d %H:%M:%S',
            '%Y-%m-%dT%H:%M:%S',
            '%Y-%m-%d %H:%M:%S.%f',
            '%Y-%m-%dT%H:%M:%S.%f',
            '%Y-%m-%dT%H:%M:%SZ',
            '%Y-%m-%d',
            '%m/%d/%Y %H:%M:%S',
            '%m/%d/%Y'
        ]

        for fmt in formats:
            try:
                return datetime.strptime(str(dt_str), fmt)
            except ValueError:
                continue

        return None

    def filter_by_period(self, executions: List[Dict[str, Any]], days: Optional[int]) -> List[Dict[str, Any]]:
        """Filter executions by time period"""
        if not days:
            return executions

        cutoff = datetime.now() - timedelta(days=days)
        filtered = [
            e for e in executions
            if e.get('start_time') and e['start_time'] >= cutoff
        ]

        self.log(f"Filtered to {len(filtered)} executions in last {days} days")
        return filtered

    def calculate_kpis(self, executions: List[Dict[str, Any]],
                       baseline: Optional[Dict[str, Any]] = None,
                       process: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Calculate all KPIs from execution data"""
        self.log("Calculating KPIs...")

        if not executions:
            raise ValueError("No execution data provided")

        # Get process name
        process_name = "Process"
        if process and 'process_name' in process:
            process_name = process['process_name']

        # Calculate analysis period
        period = self._calculate_period(executions)

        # Calculate individual KPIs
        cycle_time = self.calculate_cycle_time(executions, baseline)
        throughput = self.calculate_throughput(executions, period, baseline)
        error_rate = self.calculate_error_rate(executions, baseline)
        rework_rate = self.calculate_rework_rate(executions, baseline)
        cost_per_exec = self.calculate_cost_per_execution(executions, baseline)
        first_pass_yield = self.calculate_first_pass_yield(executions, baseline)

        # Calculate Six Sigma metrics
        six_sigma = self.calculate_six_sigma_metrics(error_rate['percentage'])

        # Analyze trends
        trends = self.analyze_trends(executions)

        # Identify outliers
        outliers = self.identify_outliers(executions)

        # Generate recommendations
        recommendations = self.generate_recommendations(
            cycle_time, throughput, error_rate, rework_rate,
            first_pass_yield, six_sigma, outliers
        )

        return {
            'process_name': process_name,
            'analysis_period': period,
            'kpis': {
                'cycle_time': cycle_time,
                'throughput': throughput,
                'error_rate': error_rate,
                'rework_rate': rework_rate,
                'cost_per_execution': cost_per_exec,
                'first_pass_yield': first_pass_yield
            },
            'six_sigma': six_sigma,
            'trends': trends,
            'outliers': outliers,
            'recommendations': recommendations
        }

    def _calculate_period(self, executions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate analysis period from execution data"""
        dates = [e['start_time'] for e in executions if e.get('start_time')]

        if not dates:
            return {
                'start': None,
                'end': None,
                'executions': len(executions)
            }

        return {
            'start': min(dates).strftime('%Y-%m-%d'),
            'end': max(dates).strftime('%Y-%m-%d'),
            'executions': len(executions)
        }

    def calculate_cycle_time(self, executions: List[Dict[str, Any]],
                            baseline: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate cycle time statistics"""
        durations = [e['duration_hours'] for e in executions if e.get('duration_hours', 0) > 0]

        if not durations:
            return {
                'average_hours': 0,
                'median_hours': 0,
                'std_dev': 0,
                'min': 0,
                'max': 0,
                'status': 'unknown'
            }

        avg = statistics.mean(durations)
        median = statistics.median(durations)
        std_dev = statistics.stdev(durations) if len(durations) > 1 else 0

        result = {
            'average_hours': round(avg, 1),
            'median_hours': round(median, 1),
            'std_dev': round(std_dev, 1),
            'min': round(min(durations), 1),
            'max': round(max(durations), 1)
        }

        # Compare to baseline
        if baseline and 'cycle_time' in baseline:
            baseline_val = baseline['cycle_time']
            improvement = ((baseline_val - avg) / baseline_val) * 100
            result['baseline'] = baseline_val
            result['improvement'] = f"{improvement:+.1f}%"
            result['status'] = self._get_status(improvement, 0, 10)
        else:
            result['status'] = 'unknown'

        return result

    def calculate_throughput(self, executions: List[Dict[str, Any]],
                            period: Dict[str, Any],
                            baseline: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate throughput metrics"""
        count = len(executions)

        # Calculate days in period
        if period['start'] and period['end']:
            start = datetime.strptime(period['start'], '%Y-%m-%d')
            end = datetime.strptime(period['end'], '%Y-%m-%d')
            days = (end - start).days + 1
        else:
            days = 30  # Default assumption

        per_day = count / days if days > 0 else 0
        per_week = per_day * 7
        per_month = per_day * 30

        result = {
            'per_day': round(per_day, 1),
            'per_week': round(per_week, 1),
            'per_month': round(per_month, 1)
        }

        # Compare to baseline
        if baseline and 'throughput' in baseline:
            baseline_val = baseline['throughput']
            improvement = ((per_month - baseline_val) / baseline_val) * 100
            result['baseline'] = baseline_val
            result['improvement'] = f"{improvement:+.1f}%"
            result['status'] = self._get_status(improvement, 0, 10)
        else:
            result['status'] = 'unknown'

        return result

    def calculate_error_rate(self, executions: List[Dict[str, Any]],
                            baseline: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate error rate"""
        total = len(executions)
        errors = sum(1 for e in executions if e.get('error', False))

        percentage = (errors / total * 100) if total > 0 else 0

        result = {
            'percentage': round(percentage, 1),
            'count': errors
        }

        # Compare to baseline (lower is better)
        if baseline and 'error_rate' in baseline:
            baseline_val = baseline['error_rate']
            improvement = ((baseline_val - percentage) / baseline_val) * 100
            result['baseline'] = baseline_val
            result['improvement'] = f"{improvement:+.1f}%"
            result['status'] = self._get_status(improvement, 0, 10)
        else:
            # Status based on absolute value
            if percentage < 5:
                result['status'] = 'green'
            elif percentage < 10:
                result['status'] = 'yellow'
            else:
                result['status'] = 'red'

        return result

    def calculate_rework_rate(self, executions: List[Dict[str, Any]],
                             baseline: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate rework rate"""
        total = len(executions)
        reworks = sum(1 for e in executions if e.get('rework', False))

        percentage = (reworks / total * 100) if total > 0 else 0

        result = {
            'percentage': round(percentage, 1),
            'count': reworks
        }

        # Compare to baseline (lower is better)
        if baseline and 'rework_rate' in baseline:
            baseline_val = baseline['rework_rate']
            improvement = ((baseline_val - percentage) / baseline_val) * 100
            result['baseline'] = baseline_val
            result['improvement'] = f"{improvement:+.1f}%"
            result['status'] = self._get_status(improvement, 0, 10)
        else:
            # Status based on absolute value
            if percentage < 10:
                result['status'] = 'green'
            elif percentage < 20:
                result['status'] = 'yellow'
            else:
                result['status'] = 'red'

        return result

    def calculate_cost_per_execution(self, executions: List[Dict[str, Any]],
                                    baseline: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate cost per execution"""
        costs = [e.get('cost', 0) for e in executions if e.get('cost', 0) > 0]

        if not costs:
            return {
                'amount': 0,
                'currency': 'USD',
                'status': 'unknown'
            }

        avg_cost = statistics.mean(costs)

        result = {
            'amount': round(avg_cost, 2),
            'currency': 'USD'
        }

        # Compare to baseline (lower is better)
        if baseline and 'cost_per_execution' in baseline:
            baseline_val = baseline['cost_per_execution']
            improvement = ((baseline_val - avg_cost) / baseline_val) * 100
            result['baseline'] = baseline_val
            result['improvement'] = f"{improvement:+.1f}%"
            result['status'] = self._get_status(improvement, 0, 10)
        else:
            result['status'] = 'unknown'

        return result

    def calculate_first_pass_yield(self, executions: List[Dict[str, Any]],
                                   baseline: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate first-pass yield (no errors or rework)"""
        total = len(executions)
        first_pass = sum(1 for e in executions
                        if not e.get('error', False) and not e.get('rework', False))

        percentage = (first_pass / total * 100) if total > 0 else 0

        result = {
            'percentage': round(percentage, 1)
        }

        # Compare to baseline
        if baseline and 'first_pass_yield' in baseline:
            baseline_val = baseline['first_pass_yield']
            improvement = ((percentage - baseline_val) / baseline_val) * 100
            result['baseline'] = baseline_val
            result['improvement'] = f"{improvement:+.1f}%"
            result['status'] = self._get_status(improvement, 0, 10)
        else:
            # Status based on absolute value
            if percentage >= 90:
                result['status'] = 'green'
            elif percentage >= 70:
                result['status'] = 'yellow'
            else:
                result['status'] = 'red'

        return result

    def calculate_six_sigma_metrics(self, error_rate_percentage: float,
                                    opportunities: int = 1,
                                    target_sigma: float = 4.0) -> Dict[str, Any]:
        """Calculate Six Sigma metrics from error rate"""
        # Convert error rate to DPMO (Defects Per Million Opportunities)
        dpmo = error_rate_percentage * 10000 * opportunities

        # Calculate sigma level
        sigma_level = self.dpmo_to_sigma(dpmo)

        # Calculate gap to target
        gap = target_sigma - sigma_level

        return {
            'dpmo': round(dpmo),
            'sigma_level': round(sigma_level, 1),
            'target_sigma': target_sigma,
            'gap': round(gap, 1)
        }

    def dpmo_to_sigma(self, dpmo: float) -> float:
        """Convert DPMO to Sigma Level using lookup table"""
        if dpmo <= 0:
            return 6.0

        # Find closest match in lookup table
        for dpmo_threshold, sigma in self.sigma_lookup:
            if dpmo >= dpmo_threshold:
                return sigma

        return 6.0

    def analyze_trends(self, executions: List[Dict[str, Any]]) -> Dict[str, str]:
        """Analyze trends over time"""
        # Sort by start time
        sorted_execs = sorted(
            [e for e in executions if e.get('start_time')],
            key=lambda x: x['start_time']
        )

        if len(sorted_execs) < 4:
            return {
                'cycle_time_trend': 'insufficient_data',
                'error_rate_trend': 'insufficient_data',
                'throughput_trend': 'insufficient_data'
            }

        # Split into halves
        mid = len(sorted_execs) // 2
        first_half = sorted_execs[:mid]
        second_half = sorted_execs[mid:]

        # Cycle time trend
        first_avg_ct = statistics.mean([e['duration_hours'] for e in first_half if e.get('duration_hours', 0) > 0]) if first_half else 0
        second_avg_ct = statistics.mean([e['duration_hours'] for e in second_half if e.get('duration_hours', 0) > 0]) if second_half else 0

        if second_avg_ct < first_avg_ct * 0.95:
            ct_trend = 'improving'
        elif second_avg_ct > first_avg_ct * 1.05:
            ct_trend = 'declining'
        else:
            ct_trend = 'stable'

        # Error rate trend
        first_errors = sum(1 for e in first_half if e.get('error', False)) / len(first_half) if first_half else 0
        second_errors = sum(1 for e in second_half if e.get('error', False)) / len(second_half) if second_half else 0

        if second_errors < first_errors * 0.95:
            error_trend = 'improving'
        elif second_errors > first_errors * 1.05:
            error_trend = 'declining'
        else:
            error_trend = 'stable'

        # Throughput trend (more in second half is better)
        throughput_ratio = len(second_half) / len(first_half) if first_half else 1

        if throughput_ratio > 1.05:
            throughput_trend = 'improving'
        elif throughput_ratio < 0.95:
            throughput_trend = 'declining'
        else:
            throughput_trend = 'stable'

        return {
            'cycle_time_trend': ct_trend,
            'error_rate_trend': error_trend,
            'throughput_trend': throughput_trend
        }

    def identify_outliers(self, executions: List[Dict[str, Any]],
                         std_dev_threshold: float = 2.0) -> List[Dict[str, Any]]:
        """Identify outlier executions"""
        durations = [e['duration_hours'] for e in executions if e.get('duration_hours', 0) > 0]

        if len(durations) < 3:
            return []

        mean = statistics.mean(durations)
        std_dev = statistics.stdev(durations)

        outliers = []
        for exec_data in executions:
            duration = exec_data.get('duration_hours', 0)
            if duration > 0:
                deviation = abs(duration - mean) / std_dev if std_dev > 0 else 0

                if deviation > std_dev_threshold:
                    outliers.append({
                        'execution_id': exec_data['execution_id'],
                        'metric': 'cycle_time',
                        'value': round(duration, 1),
                        'deviation': f"{deviation:.1f} std dev",
                        'reason': exec_data.get('notes', 'Unknown')
                    })

        return outliers

    def generate_recommendations(self, cycle_time: Dict, throughput: Dict,
                                error_rate: Dict, rework_rate: Dict,
                                first_pass_yield: Dict, six_sigma: Dict,
                                outliers: List[Dict]) -> List[str]:
        """Generate actionable recommendations based on KPIs"""
        recommendations = []

        # Error rate recommendations
        if error_rate['percentage'] > 5:
            recommendations.append(
                f"Focus on reducing error rate from {error_rate['percentage']}% to <5% target"
            )

        # Rework rate recommendations
        if rework_rate['percentage'] > 10:
            recommendations.append(
                f"Reduce rework rate from {rework_rate['percentage']}% to <10% target"
            )

        # Cycle time recommendations
        if outliers:
            max_outlier = max(outliers, key=lambda x: x['value'])
            recommendations.append(
                f"Investigate outliers with >{max_outlier['value']} hour cycle time"
            )

        # Six Sigma recommendations
        if six_sigma['gap'] > 0:
            target_dpmo = 6210 if six_sigma['target_sigma'] == 4.0 else 233
            recommendations.append(
                f"Target Six Sigma level {six_sigma['target_sigma']} "
                f"(reduce DPMO from {six_sigma['dpmo']:,} to {target_dpmo:,})"
            )

        # First-pass yield recommendations
        if first_pass_yield['percentage'] < 80:
            recommendations.append(
                f"Improve first-pass yield from {first_pass_yield['percentage']}% to >80%"
            )

        # Positive reinforcement
        if cycle_time.get('status') == 'green':
            recommendations.append(
                "Continue cycle time improvements - maintain current practices"
            )

        if not recommendations:
            recommendations.append("Process performing well - maintain current standards")

        return recommendations

    def _get_status(self, improvement: float, yellow_threshold: float,
                   green_threshold: float) -> str:
        """Get status color based on improvement percentage"""
        if improvement >= green_threshold:
            return 'green'
        elif improvement >= yellow_threshold:
            return 'yellow'
        elif improvement >= -yellow_threshold:
            return 'yellow'
        else:
            return 'red'

    def generate_ascii_chart(self, data: List[float], labels: Optional[List[str]] = None,
                           max_width: int = 20) -> List[str]:
        """Generate ASCII bar chart"""
        if not data:
            return []

        max_val = max(data)
        min_val = min(data)

        # Normalize to 0-max_width range
        if max_val == min_val:
            normalized = [max_width // 2] * len(data)
        else:
            normalized = [
                int((val - min_val) / (max_val - min_val) * max_width)
                for val in data
            ]

        # Generate chart lines
        chart = []
        for i, width in enumerate(normalized):
            label = labels[i] if labels and i < len(labels) else f"Item {i+1}"
            bar = '█' * width
            value = data[i]
            chart.append(f"{label}: {bar} {value:.1f}")

        return chart

    def format_output_json(self, kpis: Dict[str, Any]) -> str:
        """Format output as JSON"""
        return json.dumps(kpis, indent=2)

    def format_output_markdown(self, kpis: Dict[str, Any],
                              include_charts: bool = False) -> str:
        """Format output as Markdown report"""
        md = []

        # Header
        md.append(f"# Process KPI Report: {kpis['process_name']}\n")

        # Analysis Period
        md.append("## Analysis Period")
        period = kpis['analysis_period']
        if period['start'] and period['end']:
            md.append(f"- Period: {period['start']} to {period['end']}")
        md.append(f"- Executions: {period['executions']}\n")

        # Key Performance Indicators
        md.append("## Key Performance Indicators\n")

        # Cycle Time
        ct = kpis['kpis']['cycle_time']
        md.append("### Cycle Time")
        md.append(f"- **Current**: {ct['average_hours']} hours (avg)")
        if 'baseline' in ct:
            arrow = '↓' if '-' not in ct['improvement'] else '↑'
            status_emoji = self._get_status_emoji(ct['status'])
            md.append(f"- **Baseline**: {ct['baseline']} hours")
            md.append(f"- **Improvement**: {arrow} {ct['improvement']} {status_emoji}")
        md.append(f"- **Range**: {ct['min']} - {ct['max']} hours")
        md.append(f"- **Std Dev**: {ct['std_dev']} hours\n")

        # Error Rate
        er = kpis['kpis']['error_rate']
        md.append("### Error Rate")
        md.append(f"- **Current**: {er['percentage']}%")
        md.append(f"- **Count**: {er['count']}")
        md.append("- **Target**: <5%")
        if 'baseline' in er:
            status_emoji = self._get_status_emoji(er['status'])
            md.append(f"- **Status**: {status_emoji} {er['status'].upper()}\n")
        else:
            md.append(f"- **Status**: {er['status'].upper()}\n")

        # Throughput
        tp = kpis['kpis']['throughput']
        md.append("### Throughput")
        md.append(f"- **Current**: {tp['per_day']}/day ({tp['per_week']}/week)")
        if 'baseline' in tp:
            arrow = '↑' if '-' not in tp['improvement'] else '↓'
            status_emoji = self._get_status_emoji(tp['status'])
            md.append(f"- **Improvement**: {arrow} {tp['improvement']} {status_emoji}\n")
        else:
            md.append("")

        # Rework Rate
        rr = kpis['kpis']['rework_rate']
        md.append("### Rework Rate")
        md.append(f"- **Current**: {rr['percentage']}%")
        md.append(f"- **Count**: {rr['count']}")
        if 'baseline' in rr:
            status_emoji = self._get_status_emoji(rr['status'])
            md.append(f"- **Status**: {status_emoji} {rr['status'].upper()}\n")
        else:
            md.append("")

        # First-Pass Yield
        fpy = kpis['kpis']['first_pass_yield']
        md.append("### First-Pass Yield")
        md.append(f"- **Current**: {fpy['percentage']}%")
        if 'baseline' in fpy:
            status_emoji = self._get_status_emoji(fpy['status'])
            md.append(f"- **Improvement**: {fpy['improvement']} {status_emoji}\n")
        else:
            md.append("")

        # Cost Per Execution
        cpe = kpis['kpis']['cost_per_execution']
        if cpe['amount'] > 0:
            md.append("### Cost Per Execution")
            md.append(f"- **Current**: ${cpe['amount']} {cpe['currency']}")
            if 'baseline' in cpe:
                status_emoji = self._get_status_emoji(cpe['status'])
                md.append(f"- **Improvement**: {cpe['improvement']} {status_emoji}\n")
            else:
                md.append("")

        # Six Sigma Analysis
        ss = kpis['six_sigma']
        md.append("## Six Sigma Analysis")
        md.append(f"- **Sigma Level**: {ss['sigma_level']}")
        md.append(f"- **Target**: {ss['target_sigma']}")
        md.append(f"- **Gap**: {ss['gap']} levels")
        md.append(f"- **DPMO**: {ss['dpmo']:,}\n")

        # Trends
        trends = kpis['trends']
        md.append("## Trends")
        md.append(f"- **Cycle Time**: {trends['cycle_time_trend']}")
        md.append(f"- **Error Rate**: {trends['error_rate_trend']}")
        md.append(f"- **Throughput**: {trends['throughput_trend']}\n")

        # Outliers
        if kpis['outliers']:
            md.append("## Outliers")
            for outlier in kpis['outliers'][:5]:  # Limit to 5
                md.append(f"- **{outlier['execution_id']}**: "
                         f"{outlier['metric']} = {outlier['value']} "
                         f"({outlier['deviation']})")
                if outlier['reason']:
                    md.append(f"  - Reason: {outlier['reason']}")
            md.append("")

        # Recommendations
        md.append("## Recommendations")
        for i, rec in enumerate(kpis['recommendations'], 1):
            md.append(f"{i}. {rec}")

        return '\n'.join(md)

    def format_output_csv(self, kpis: Dict[str, Any]) -> str:
        """Format output as CSV"""
        lines = []
        lines.append("metric,value,baseline,improvement,status")

        # Cycle time
        ct = kpis['kpis']['cycle_time']
        lines.append(f"cycle_time_avg,{ct['average_hours']},"
                    f"{ct.get('baseline', '')},"
                    f"{ct.get('improvement', '')},"
                    f"{ct.get('status', '')}")

        # Error rate
        er = kpis['kpis']['error_rate']
        lines.append(f"error_rate,{er['percentage']},"
                    f"{er.get('baseline', '')},"
                    f"{er.get('improvement', '')},"
                    f"{er.get('status', '')}")

        # Throughput
        tp = kpis['kpis']['throughput']
        lines.append(f"throughput_per_day,{tp['per_day']},"
                    f"{tp.get('baseline', '')},"
                    f"{tp.get('improvement', '')},"
                    f"{tp.get('status', '')}")

        # Rework rate
        rr = kpis['kpis']['rework_rate']
        lines.append(f"rework_rate,{rr['percentage']},"
                    f"{rr.get('baseline', '')},"
                    f"{rr.get('improvement', '')},"
                    f"{rr.get('status', '')}")

        # First-pass yield
        fpy = kpis['kpis']['first_pass_yield']
        lines.append(f"first_pass_yield,{fpy['percentage']},"
                    f"{fpy.get('baseline', '')},"
                    f"{fpy.get('improvement', '')},"
                    f"{fpy.get('status', '')}")

        # Six Sigma
        ss = kpis['six_sigma']
        lines.append(f"sigma_level,{ss['sigma_level']},{ss['target_sigma']},{ss['gap']},")

        return '\n'.join(lines)

    def _get_status_emoji(self, status: str) -> str:
        """Get emoji for status"""
        emoji_map = {
            'green': '🟢',
            'yellow': '🟡',
            'red': '🔴',
            'unknown': '⚪'
        }
        return emoji_map.get(status, '⚪')


def main():
    parser = argparse.ArgumentParser(
        description='Calculate process KPIs and efficiency metrics',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Calculate KPIs from CSV file
  python kpi_calculator.py executions.csv

  # With baseline comparison
  python kpi_calculator.py executions.json --baseline baseline.json

  # Filter to last 30 days
  python kpi_calculator.py executions.csv --period 30

  # Output as Markdown with charts
  python kpi_calculator.py executions.json --output markdown --include-charts

  # Output as CSV
  python kpi_calculator.py executions.csv --output csv > kpis.csv

Exit Codes:
  0 - Success
  1 - Validation error
  2 - Parse error
  3 - Calculation error
        """
    )

    parser.add_argument('input', type=Path,
                       help='Input file (JSON or CSV) with execution data')
    parser.add_argument('--process', type=Path,
                       help='Process definition file (JSON)')
    parser.add_argument('--baseline', type=Path,
                       help='Baseline metrics file (JSON)')
    parser.add_argument('--period', type=int,
                       help='Analysis period in days (filters to last N days)')
    parser.add_argument('--output', choices=['json', 'markdown', 'csv'],
                       default='json',
                       help='Output format (default: json)')
    parser.add_argument('--include-charts', action='store_true',
                       help='Include ASCII charts in markdown output')
    parser.add_argument('--verbose', action='store_true',
                       help='Enable verbose logging')

    args = parser.parse_args()

    calculator = KPICalculator(verbose=args.verbose)

    try:
        # Parse input data
        executions = calculator.parse_input_data(args.input)

        if not executions:
            print("Error: No execution data found in input file", file=sys.stderr)
            sys.exit(EXIT_VALIDATION_ERROR)

        # Normalize data
        executions = calculator.normalize_execution_data(executions)

        # Filter by period if specified
        if args.period:
            executions = calculator.filter_by_period(executions, args.period)

        if not executions:
            print(f"Error: No executions found in last {args.period} days", file=sys.stderr)
            sys.exit(EXIT_VALIDATION_ERROR)

        # Parse baseline if provided
        baseline = calculator.parse_baseline(args.baseline)

        # Parse process definition if provided
        process = calculator.parse_process_definition(args.process)

        # Calculate KPIs
        kpis = calculator.calculate_kpis(executions, baseline, process)

        # Format output
        if args.output == 'json':
            output = calculator.format_output_json(kpis)
        elif args.output == 'markdown':
            output = calculator.format_output_markdown(kpis, args.include_charts)
        elif args.output == 'csv':
            output = calculator.format_output_csv(kpis)

        print(output)
        sys.exit(EXIT_SUCCESS)

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(EXIT_VALIDATION_ERROR)
    except ValueError as e:
        print(f"Validation error: {e}", file=sys.stderr)
        sys.exit(EXIT_VALIDATION_ERROR)
    except json.JSONDecodeError as e:
        print(f"Parse error: {e}", file=sys.stderr)
        sys.exit(EXIT_PARSE_ERROR)
    except Exception as e:
        print(f"Calculation error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(EXIT_CALCULATION_ERROR)


if __name__ == '__main__':
    main()
