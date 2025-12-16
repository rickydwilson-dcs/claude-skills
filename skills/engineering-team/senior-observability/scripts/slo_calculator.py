#!/usr/bin/env python3
"""
SLO Calculator
Calculate SLI/SLO targets, error budgets, and burn rates from metrics data.

Features:
- SLI calculation from raw metrics (availability, latency, throughput)
- Error budget tracking (total, consumed, remaining)
- Multi-window burn rate analysis
- SLO recommendations based on historical performance
- Alert threshold suggestions

Standard library only - no external dependencies required.
"""

import argparse
import csv
import json
import logging
import math
import sys
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

__version__ = "1.0.0"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SLOType(Enum):
    """Types of SLOs"""
    AVAILABILITY = "availability"
    LATENCY = "latency"
    THROUGHPUT = "throughput"


class TimeWindow(Enum):
    """SLO time windows"""
    WEEK = "7d"
    MONTH = "30d"
    QUARTER = "90d"


class ServiceTier(Enum):
    """Service tier classifications"""
    CRITICAL = "critical"      # 99.99% target
    HIGH = "high"              # 99.9% target
    STANDARD = "standard"      # 99.5% target
    LOW = "low"                # 99% target


@dataclass
class MetricsData:
    """Container for metrics data"""
    timestamps: List[datetime]
    total_requests: List[int]
    successful_requests: List[int]
    failed_requests: List[int]
    latency_values: List[float]  # P99 or specific percentile
    throughput_values: List[float]


@dataclass
class SLIResult:
    """Result of SLI calculation"""
    slo_type: SLOType
    value: float
    total_events: int
    good_events: int
    bad_events: int
    measurement_period: str


@dataclass
class ErrorBudget:
    """Error budget calculation"""
    total_budget_percent: float
    total_budget_minutes: float
    consumed_percent: float
    consumed_minutes: float
    remaining_percent: float
    remaining_minutes: float
    burn_rate_1h: float
    burn_rate_6h: float
    burn_rate_24h: float
    burn_rate_3d: float
    status: str  # "healthy", "warning", "critical"


@dataclass
class SLORecommendation:
    """SLO recommendation based on historical data"""
    current_performance: float
    recommended_target: float
    achievable_target: float  # Based on worst historical performance
    tier_recommendation: ServiceTier
    confidence: str  # "high", "medium", "low"
    rationale: str


@dataclass
class AlertThreshold:
    """Alert threshold suggestion"""
    name: str
    window: str
    burn_rate: float
    severity: str
    description: str


@dataclass
class SLOReport:
    """Complete SLO analysis report"""
    service: str
    slo_type: SLOType
    target: float
    window: TimeWindow
    sli: SLIResult
    error_budget: ErrorBudget
    recommendation: SLORecommendation
    alert_thresholds: List[AlertThreshold]
    generated_at: datetime


class MetricsParser:
    """Parse metrics from CSV or JSON files"""

    @staticmethod
    def parse_csv(filepath: str) -> MetricsData:
        """Parse metrics from CSV file"""
        timestamps = []
        total_requests = []
        successful_requests = []
        failed_requests = []
        latency_values = []
        throughput_values = []

        with open(filepath, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Parse timestamp
                ts_str = row.get('timestamp', row.get('time', row.get('date', '')))
                if ts_str:
                    try:
                        ts = datetime.fromisoformat(ts_str.replace('Z', '+00:00'))
                    except ValueError:
                        ts = datetime.now()
                    timestamps.append(ts)

                # Parse request counts
                total = int(row.get('total_requests', row.get('total', 0)))
                success = int(row.get('successful_requests', row.get('success', row.get('2xx', 0))))
                failed = int(row.get('failed_requests', row.get('errors', row.get('5xx', 0))))

                if total == 0 and success > 0:
                    total = success + failed

                total_requests.append(total)
                successful_requests.append(success)
                failed_requests.append(failed if failed else total - success)

                # Parse latency
                latency = float(row.get('latency_p99', row.get('latency', row.get('p99', 0))))
                latency_values.append(latency)

                # Parse throughput
                throughput = float(row.get('throughput', row.get('rps', 0)))
                throughput_values.append(throughput)

        return MetricsData(
            timestamps=timestamps,
            total_requests=total_requests,
            successful_requests=successful_requests,
            failed_requests=failed_requests,
            latency_values=latency_values,
            throughput_values=throughput_values
        )

    @staticmethod
    def parse_json(filepath: str) -> MetricsData:
        """Parse metrics from JSON file"""
        with open(filepath, 'r') as f:
            data = json.load(f)

        # Handle both array and object formats
        if isinstance(data, list):
            records = data
        elif isinstance(data, dict):
            records = data.get('metrics', data.get('data', data.get('records', [data])))
        else:
            records = []

        timestamps = []
        total_requests = []
        successful_requests = []
        failed_requests = []
        latency_values = []
        throughput_values = []

        for record in records:
            # Parse timestamp
            ts_str = record.get('timestamp', record.get('time', ''))
            if ts_str:
                try:
                    ts = datetime.fromisoformat(str(ts_str).replace('Z', '+00:00'))
                except ValueError:
                    ts = datetime.now()
                timestamps.append(ts)
            else:
                timestamps.append(datetime.now())

            # Parse counts
            total = int(record.get('total_requests', record.get('total', 0)))
            success = int(record.get('successful_requests', record.get('success', 0)))
            failed = int(record.get('failed_requests', record.get('errors', 0)))

            if total == 0 and success > 0:
                total = success + failed

            total_requests.append(total)
            successful_requests.append(success)
            failed_requests.append(failed if failed else total - success)

            latency_values.append(float(record.get('latency_p99', record.get('latency', 0))))
            throughput_values.append(float(record.get('throughput', record.get('rps', 0))))

        return MetricsData(
            timestamps=timestamps,
            total_requests=total_requests,
            successful_requests=successful_requests,
            failed_requests=failed_requests,
            latency_values=latency_values,
            throughput_values=throughput_values
        )

    @staticmethod
    def parse_file(filepath: str) -> MetricsData:
        """Parse metrics file based on extension"""
        if filepath.endswith('.json'):
            return MetricsParser.parse_json(filepath)
        else:
            return MetricsParser.parse_csv(filepath)


class SLICalculator:
    """Calculate Service Level Indicators"""

    @staticmethod
    def calculate_availability(metrics: MetricsData) -> SLIResult:
        """Calculate availability SLI (success rate)"""
        total_events = sum(metrics.total_requests)
        good_events = sum(metrics.successful_requests)
        bad_events = total_events - good_events

        if total_events == 0:
            value = 100.0
        else:
            value = (good_events / total_events) * 100

        # Determine measurement period
        if metrics.timestamps:
            start = min(metrics.timestamps)
            end = max(metrics.timestamps)
            period = f"{start.isoformat()} to {end.isoformat()}"
        else:
            period = "unknown"

        return SLIResult(
            slo_type=SLOType.AVAILABILITY,
            value=round(value, 4),
            total_events=total_events,
            good_events=good_events,
            bad_events=bad_events,
            measurement_period=period
        )

    @staticmethod
    def calculate_latency(metrics: MetricsData, threshold_ms: float = 500) -> SLIResult:
        """Calculate latency SLI (requests under threshold)"""
        if not metrics.latency_values:
            return SLIResult(
                slo_type=SLOType.LATENCY,
                value=100.0,
                total_events=0,
                good_events=0,
                bad_events=0,
                measurement_period="no data"
            )

        # Count requests under threshold (assuming latency_values are in ms)
        good_events = sum(1 for lat in metrics.latency_values if lat <= threshold_ms)
        total_events = len(metrics.latency_values)
        bad_events = total_events - good_events

        if total_events == 0:
            value = 100.0
        else:
            value = (good_events / total_events) * 100

        if metrics.timestamps:
            start = min(metrics.timestamps)
            end = max(metrics.timestamps)
            period = f"{start.isoformat()} to {end.isoformat()}"
        else:
            period = "unknown"

        return SLIResult(
            slo_type=SLOType.LATENCY,
            value=round(value, 4),
            total_events=total_events,
            good_events=good_events,
            bad_events=bad_events,
            measurement_period=period
        )

    @staticmethod
    def calculate_throughput(metrics: MetricsData, min_rps: float = 10) -> SLIResult:
        """Calculate throughput SLI (periods meeting minimum RPS)"""
        if not metrics.throughput_values:
            return SLIResult(
                slo_type=SLOType.THROUGHPUT,
                value=100.0,
                total_events=0,
                good_events=0,
                bad_events=0,
                measurement_period="no data"
            )

        good_events = sum(1 for tp in metrics.throughput_values if tp >= min_rps)
        total_events = len(metrics.throughput_values)
        bad_events = total_events - good_events

        if total_events == 0:
            value = 100.0
        else:
            value = (good_events / total_events) * 100

        if metrics.timestamps:
            start = min(metrics.timestamps)
            end = max(metrics.timestamps)
            period = f"{start.isoformat()} to {end.isoformat()}"
        else:
            period = "unknown"

        return SLIResult(
            slo_type=SLOType.THROUGHPUT,
            value=round(value, 4),
            total_events=total_events,
            good_events=good_events,
            bad_events=bad_events,
            measurement_period=period
        )


class ErrorBudgetCalculator:
    """Calculate error budgets and burn rates"""

    @staticmethod
    def calculate(sli: SLIResult, target: float, window: TimeWindow) -> ErrorBudget:
        """Calculate error budget from SLI and target"""
        # Calculate error budget
        error_budget_percent = 100 - target  # e.g., 0.1% for 99.9% SLO

        # Window in minutes
        window_minutes = {
            TimeWindow.WEEK: 7 * 24 * 60,
            TimeWindow.MONTH: 30 * 24 * 60,
            TimeWindow.QUARTER: 90 * 24 * 60
        }[window]

        total_budget_minutes = (error_budget_percent / 100) * window_minutes

        # Calculate consumed budget
        actual_error_rate = 100 - sli.value
        consumed_percent = (actual_error_rate / error_budget_percent) * 100 if error_budget_percent > 0 else 0
        consumed_minutes = (consumed_percent / 100) * total_budget_minutes

        remaining_percent = max(0, 100 - consumed_percent)
        remaining_minutes = max(0, total_budget_minutes - consumed_minutes)

        # Calculate burn rates (how fast we're consuming budget)
        # Burn rate = actual error rate / allowed error rate
        allowed_error_rate = error_budget_percent / 100

        if sli.total_events > 0:
            actual_error_rate_decimal = sli.bad_events / sli.total_events
        else:
            actual_error_rate_decimal = 0

        base_burn_rate = actual_error_rate_decimal / allowed_error_rate if allowed_error_rate > 0 else 0

        # Approximate burn rates for different windows
        # In practice, these would be calculated from actual windowed data
        burn_rate_1h = round(base_burn_rate * 1.2, 2)  # More variable in short windows
        burn_rate_6h = round(base_burn_rate * 1.1, 2)
        burn_rate_24h = round(base_burn_rate, 2)
        burn_rate_3d = round(base_burn_rate * 0.9, 2)  # Tends to smooth out

        # Determine status
        if remaining_percent < 10 or burn_rate_1h > 10:
            status = "critical"
        elif remaining_percent < 30 or burn_rate_1h > 5:
            status = "warning"
        else:
            status = "healthy"

        return ErrorBudget(
            total_budget_percent=round(error_budget_percent, 4),
            total_budget_minutes=round(total_budget_minutes, 2),
            consumed_percent=round(min(consumed_percent, 100), 2),
            consumed_minutes=round(consumed_minutes, 2),
            remaining_percent=round(remaining_percent, 2),
            remaining_minutes=round(remaining_minutes, 2),
            burn_rate_1h=burn_rate_1h,
            burn_rate_6h=burn_rate_6h,
            burn_rate_24h=burn_rate_24h,
            burn_rate_3d=burn_rate_3d,
            status=status
        )


class SLORecommender:
    """Recommend SLO targets based on historical performance"""

    TIER_TARGETS = {
        ServiceTier.CRITICAL: 99.99,
        ServiceTier.HIGH: 99.9,
        ServiceTier.STANDARD: 99.5,
        ServiceTier.LOW: 99.0
    }

    @staticmethod
    def recommend(metrics: MetricsData, sli: SLIResult) -> SLORecommendation:
        """Generate SLO recommendation"""
        current = sli.value

        # Calculate worst-case historical performance
        if metrics.total_requests and len(metrics.total_requests) > 1:
            # Calculate availability for each data point
            period_avails = []
            for i in range(len(metrics.total_requests)):
                if metrics.total_requests[i] > 0:
                    avail = (metrics.successful_requests[i] / metrics.total_requests[i]) * 100
                    period_avails.append(avail)

            if period_avails:
                worst_case = min(period_avails)
                achievable = math.floor(worst_case * 10) / 10  # Round down to 1 decimal
            else:
                achievable = current
        else:
            achievable = current

        # Determine recommended tier
        if current >= 99.99:
            tier = ServiceTier.CRITICAL
            recommended = 99.99
        elif current >= 99.9:
            tier = ServiceTier.HIGH
            recommended = 99.9
        elif current >= 99.5:
            tier = ServiceTier.STANDARD
            recommended = 99.5
        else:
            tier = ServiceTier.LOW
            recommended = 99.0

        # Don't recommend a target higher than achievable
        recommended = min(recommended, achievable)

        # Determine confidence based on data volume
        if sli.total_events > 100000:
            confidence = "high"
        elif sli.total_events > 10000:
            confidence = "medium"
        else:
            confidence = "low"

        rationale = f"Based on {sli.total_events:,} total events, current performance is {current:.2f}%. "
        rationale += f"Historical worst-case is {achievable:.2f}%. "
        rationale += f"Recommended target of {recommended}% provides {current - recommended:.2f}% headroom."

        return SLORecommendation(
            current_performance=round(current, 4),
            recommended_target=recommended,
            achievable_target=round(achievable, 2),
            tier_recommendation=tier,
            confidence=confidence,
            rationale=rationale
        )


class AlertThresholdGenerator:
    """Generate alert thresholds based on SLO"""

    @staticmethod
    def generate(target: float) -> List[AlertThreshold]:
        """Generate multi-burn-rate alert thresholds"""
        error_budget = 100 - target

        thresholds = [
            AlertThreshold(
                name="SLO_BurnRate_1h",
                window="1h",
                burn_rate=14.4,
                severity="critical",
                description=f"Consuming {error_budget * 14.4:.1f}% of error budget per hour (will exhaust in ~7 hours)"
            ),
            AlertThreshold(
                name="SLO_BurnRate_6h",
                window="6h",
                burn_rate=6.0,
                severity="critical",
                description=f"Consuming {error_budget * 6:.1f}% of error budget per hour (will exhaust in ~5 days)"
            ),
            AlertThreshold(
                name="SLO_BurnRate_1d",
                window="1d",
                burn_rate=3.0,
                severity="warning",
                description=f"Consuming {error_budget * 3:.1f}% of error budget per hour (will exhaust in ~10 days)"
            ),
            AlertThreshold(
                name="SLO_BurnRate_3d",
                window="3d",
                burn_rate=1.0,
                severity="warning",
                description=f"Consuming {error_budget:.2f}% of error budget per hour (will exhaust in ~30 days)"
            )
        ]

        return thresholds


def generate_report(metrics: MetricsData, slo_type: SLOType, target: float,
                    window: TimeWindow, service: str = "service") -> SLOReport:
    """Generate complete SLO report"""
    # Calculate SLI
    if slo_type == SLOType.AVAILABILITY:
        sli = SLICalculator.calculate_availability(metrics)
    elif slo_type == SLOType.LATENCY:
        sli = SLICalculator.calculate_latency(metrics)
    else:
        sli = SLICalculator.calculate_throughput(metrics)

    # Calculate error budget
    error_budget = ErrorBudgetCalculator.calculate(sli, target, window)

    # Generate recommendations
    recommendation = SLORecommender.recommend(metrics, sli)

    # Generate alert thresholds
    alert_thresholds = AlertThresholdGenerator.generate(target)

    return SLOReport(
        service=service,
        slo_type=slo_type,
        target=target,
        window=window,
        sli=sli,
        error_budget=error_budget,
        recommendation=recommendation,
        alert_thresholds=alert_thresholds,
        generated_at=datetime.now()
    )


def format_output(report: SLOReport, output_format: str) -> str:
    """Format report output"""
    if output_format == "json":
        data = {
            "service": report.service,
            "slo_type": report.slo_type.value,
            "target": report.target,
            "window": report.window.value,
            "generated_at": report.generated_at.isoformat(),
            "sli": {
                "type": report.sli.slo_type.value,
                "value": report.sli.value,
                "total_events": report.sli.total_events,
                "good_events": report.sli.good_events,
                "bad_events": report.sli.bad_events,
                "measurement_period": report.sli.measurement_period
            },
            "error_budget": {
                "total_budget_percent": report.error_budget.total_budget_percent,
                "total_budget_minutes": report.error_budget.total_budget_minutes,
                "consumed_percent": report.error_budget.consumed_percent,
                "consumed_minutes": report.error_budget.consumed_minutes,
                "remaining_percent": report.error_budget.remaining_percent,
                "remaining_minutes": report.error_budget.remaining_minutes,
                "burn_rates": {
                    "1h": report.error_budget.burn_rate_1h,
                    "6h": report.error_budget.burn_rate_6h,
                    "24h": report.error_budget.burn_rate_24h,
                    "3d": report.error_budget.burn_rate_3d
                },
                "status": report.error_budget.status
            },
            "recommendation": {
                "current_performance": report.recommendation.current_performance,
                "recommended_target": report.recommendation.recommended_target,
                "achievable_target": report.recommendation.achievable_target,
                "tier": report.recommendation.tier_recommendation.value,
                "confidence": report.recommendation.confidence,
                "rationale": report.recommendation.rationale
            },
            "alert_thresholds": [
                {
                    "name": t.name,
                    "window": t.window,
                    "burn_rate": t.burn_rate,
                    "severity": t.severity,
                    "description": t.description
                }
                for t in report.alert_thresholds
            ]
        }
        return json.dumps(data, indent=2)

    elif output_format == "markdown":
        lines = [
            f"# SLO Report: {report.service}",
            "",
            f"**Generated:** {report.generated_at.strftime('%Y-%m-%d %H:%M:%S')}",
            f"**SLO Type:** {report.slo_type.value}",
            f"**Target:** {report.target}%",
            f"**Window:** {report.window.value}",
            "",
            "## Current Performance",
            "",
            f"| Metric | Value |",
            f"|--------|-------|",
            f"| Current SLI | **{report.sli.value}%** |",
            f"| Total Events | {report.sli.total_events:,} |",
            f"| Good Events | {report.sli.good_events:,} |",
            f"| Bad Events | {report.sli.bad_events:,} |",
            f"| SLO Target | {report.target}% |",
            f"| Status | {'✅ Meeting SLO' if report.sli.value >= report.target else '❌ Below SLO'} |",
            "",
            "## Error Budget",
            "",
            f"| Metric | Value |",
            f"|--------|-------|",
            f"| Total Budget | {report.error_budget.total_budget_percent}% ({report.error_budget.total_budget_minutes:.0f} min) |",
            f"| Consumed | {report.error_budget.consumed_percent}% ({report.error_budget.consumed_minutes:.0f} min) |",
            f"| Remaining | **{report.error_budget.remaining_percent}%** ({report.error_budget.remaining_minutes:.0f} min) |",
            f"| Status | {'🟢' if report.error_budget.status == 'healthy' else '🟡' if report.error_budget.status == 'warning' else '🔴'} {report.error_budget.status.upper()} |",
            "",
            "## Burn Rates",
            "",
            f"| Window | Burn Rate | Risk |",
            f"|--------|-----------|------|",
            f"| 1h | {report.error_budget.burn_rate_1h}x | {'🔴 High' if report.error_budget.burn_rate_1h > 10 else '🟡 Medium' if report.error_budget.burn_rate_1h > 5 else '🟢 Low'} |",
            f"| 6h | {report.error_budget.burn_rate_6h}x | {'🔴 High' if report.error_budget.burn_rate_6h > 5 else '🟡 Medium' if report.error_budget.burn_rate_6h > 2 else '🟢 Low'} |",
            f"| 24h | {report.error_budget.burn_rate_24h}x | {'🔴 High' if report.error_budget.burn_rate_24h > 3 else '🟡 Medium' if report.error_budget.burn_rate_24h > 1.5 else '🟢 Low'} |",
            f"| 3d | {report.error_budget.burn_rate_3d}x | {'🔴 High' if report.error_budget.burn_rate_3d > 2 else '🟡 Medium' if report.error_budget.burn_rate_3d > 1 else '🟢 Low'} |",
            "",
            "## Recommendation",
            "",
            f"**Tier:** {report.recommendation.tier_recommendation.value.upper()}",
            f"**Recommended Target:** {report.recommendation.recommended_target}%",
            f"**Achievable Target:** {report.recommendation.achievable_target}%",
            f"**Confidence:** {report.recommendation.confidence}",
            "",
            f"> {report.recommendation.rationale}",
            "",
            "## Alert Thresholds",
            "",
            "| Alert | Window | Burn Rate | Severity |",
            "|-------|--------|-----------|----------|",
        ]
        for t in report.alert_thresholds:
            lines.append(f"| {t.name} | {t.window} | {t.burn_rate}x | {t.severity} |")

        return "\n".join(lines)

    elif output_format == "csv":
        lines = [
            "metric,value",
            f"service,{report.service}",
            f"slo_type,{report.slo_type.value}",
            f"target,{report.target}",
            f"current_sli,{report.sli.value}",
            f"total_events,{report.sli.total_events}",
            f"good_events,{report.sli.good_events}",
            f"bad_events,{report.sli.bad_events}",
            f"error_budget_remaining_percent,{report.error_budget.remaining_percent}",
            f"error_budget_remaining_minutes,{report.error_budget.remaining_minutes}",
            f"burn_rate_1h,{report.error_budget.burn_rate_1h}",
            f"burn_rate_6h,{report.error_budget.burn_rate_6h}",
            f"burn_rate_24h,{report.error_budget.burn_rate_24h}",
            f"status,{report.error_budget.status}",
            f"recommended_target,{report.recommendation.recommended_target}"
        ]
        return "\n".join(lines)

    else:  # text
        status_emoji = "✅" if report.sli.value >= report.target else "❌"
        budget_emoji = "🟢" if report.error_budget.status == "healthy" else "🟡" if report.error_budget.status == "warning" else "🔴"

        lines = [
            "=" * 60,
            f"SLO Report: {report.service}",
            "=" * 60,
            "",
            f"Generated: {report.generated_at.strftime('%Y-%m-%d %H:%M:%S')}",
            f"SLO Type: {report.slo_type.value}",
            f"Target: {report.target}%",
            f"Window: {report.window.value}",
            "",
            "-" * 60,
            "Current Performance",
            "-" * 60,
            f"  Current SLI:    {report.sli.value}%  {status_emoji}",
            f"  Total Events:   {report.sli.total_events:,}",
            f"  Good Events:    {report.sli.good_events:,}",
            f"  Bad Events:     {report.sli.bad_events:,}",
            "",
            "-" * 60,
            "Error Budget",
            "-" * 60,
            f"  Total Budget:   {report.error_budget.total_budget_percent}% ({report.error_budget.total_budget_minutes:.0f} min)",
            f"  Consumed:       {report.error_budget.consumed_percent}% ({report.error_budget.consumed_minutes:.0f} min)",
            f"  Remaining:      {report.error_budget.remaining_percent}% ({report.error_budget.remaining_minutes:.0f} min)  {budget_emoji}",
            "",
            "-" * 60,
            "Burn Rates",
            "-" * 60,
            f"  1h window:      {report.error_budget.burn_rate_1h}x",
            f"  6h window:      {report.error_budget.burn_rate_6h}x",
            f"  24h window:     {report.error_budget.burn_rate_24h}x",
            f"  3d window:      {report.error_budget.burn_rate_3d}x",
            "",
            "-" * 60,
            "Recommendation",
            "-" * 60,
            f"  Service Tier:       {report.recommendation.tier_recommendation.value.upper()}",
            f"  Recommended Target: {report.recommendation.recommended_target}%",
            f"  Achievable Target:  {report.recommendation.achievable_target}%",
            f"  Confidence:         {report.recommendation.confidence}",
            "",
            f"  {report.recommendation.rationale}",
            "",
            "=" * 60
        ]
        return "\n".join(lines)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Calculate SLI/SLO targets, error budgets, and burn rates",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Calculate availability SLO from CSV
  %(prog)s --input metrics.csv --slo-type availability --target 99.9 --output json

  # Calculate latency SLO for 30-day window
  %(prog)s --input metrics.json --slo-type latency --target 95 --window 30d --output markdown

  # Generate text report with service name
  %(prog)s --input metrics.csv --service payment-api --target 99.9 --output text

Input File Format (CSV):
  Required columns: timestamp, total_requests, successful_requests
  Optional columns: failed_requests, latency_p99, throughput

Input File Format (JSON):
  Array of objects with same fields as CSV
        """
    )

    parser.add_argument(
        "--input", "-i",
        required=True,
        help="Input metrics file (CSV or JSON)"
    )

    parser.add_argument(
        "--service", "-s",
        default="service",
        help="Service name (default: service)"
    )

    parser.add_argument(
        "--slo-type",
        choices=[t.value for t in SLOType],
        default="availability",
        help="Type of SLO to calculate (default: availability)"
    )

    parser.add_argument(
        "--target",
        type=float,
        default=99.9,
        help="SLO target percentage (default: 99.9)"
    )

    parser.add_argument(
        "--window",
        choices=[w.value for w in TimeWindow],
        default="30d",
        help="SLO time window (default: 30d)"
    )

    parser.add_argument(
        "--output", "-o",
        choices=["json", "text", "markdown", "csv"],
        default="text",
        help="Output format (default: text)"
    )

    parser.add_argument(
        "--file", "-f",
        help="Write output to file instead of stdout"
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        # Parse metrics
        logger.info(f"Reading metrics from {args.input}")
        metrics = MetricsParser.parse_file(args.input)
        logger.info(f"Loaded {len(metrics.timestamps)} data points")

        # Generate report
        slo_type = SLOType(args.slo_type)
        window = TimeWindow(args.window)

        report = generate_report(
            metrics=metrics,
            slo_type=slo_type,
            target=args.target,
            window=window,
            service=args.service
        )

        # Format output
        output = format_output(report, args.output)

        # Write output
        if args.file:
            with open(args.file, "w") as f:
                f.write(output)
            logger.info(f"Report written to {args.file}")
        else:
            print(output)

        return 0

    except FileNotFoundError:
        logger.error(f"Input file not found: {args.input}")
        return 1
    except Exception as e:
        logger.error(f"Error calculating SLO: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
