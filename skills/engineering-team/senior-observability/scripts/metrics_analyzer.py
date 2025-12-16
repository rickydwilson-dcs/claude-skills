#!/usr/bin/env python3
"""
Metrics Analyzer
Analyze metrics patterns to detect anomalies, trends, and optimization opportunities.

Features:
- Statistical baseline calculation (mean, median, percentiles, std dev)
- Anomaly detection (Z-score, IQR-based)
- Trend analysis (increasing, decreasing, stable, seasonal)
- Correlation analysis between metrics
- Cardinality analysis for high-cardinality metric optimization
- Actionable recommendations

Standard library only - no external dependencies required.
"""

import argparse
import csv
import json
import logging
import math
import sys
from collections import defaultdict
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


class AnalysisType(Enum):
    """Types of analysis"""
    ANOMALY = "anomaly"
    TREND = "trend"
    CORRELATION = "correlation"
    BASELINE = "baseline"
    CARDINALITY = "cardinality"


class TrendDirection(Enum):
    """Trend directions"""
    INCREASING = "increasing"
    DECREASING = "decreasing"
    STABLE = "stable"
    SEASONAL = "seasonal"
    VOLATILE = "volatile"


class AnomalySeverity(Enum):
    """Anomaly severity levels"""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class MetricData:
    """Single metric time series"""
    name: str
    timestamps: List[datetime]
    values: List[float]
    labels: Dict[str, str] = field(default_factory=dict)


@dataclass
class BaselineStats:
    """Statistical baseline for a metric"""
    metric_name: str
    count: int
    mean: float
    median: float
    std_dev: float
    min_val: float
    max_val: float
    p50: float
    p90: float
    p95: float
    p99: float
    iqr: float  # Interquartile range


@dataclass
class Anomaly:
    """Detected anomaly"""
    metric_name: str
    timestamp: datetime
    value: float
    expected_value: float
    deviation: float  # Number of standard deviations
    severity: AnomalySeverity
    method: str  # "zscore" or "iqr"


@dataclass
class TrendAnalysis:
    """Trend analysis result"""
    metric_name: str
    direction: TrendDirection
    slope: float  # Change per time unit
    r_squared: float  # Fit quality (0-1)
    change_percent: float  # Total change as percentage
    volatility: float  # Coefficient of variation
    seasonality_detected: bool


@dataclass
class CorrelationResult:
    """Correlation between two metrics"""
    metric_a: str
    metric_b: str
    correlation: float  # -1 to 1
    strength: str  # "strong", "moderate", "weak", "none"
    direction: str  # "positive", "negative"


@dataclass
class CardinalityAnalysis:
    """Cardinality analysis for a metric"""
    metric_name: str
    total_series: int
    unique_labels: Dict[str, int]  # label -> unique values count
    high_cardinality_labels: List[str]
    estimated_memory_mb: float
    recommendations: List[str]


@dataclass
class AnalysisReport:
    """Complete analysis report"""
    analysis_type: AnalysisType
    metrics_analyzed: List[str]
    baselines: List[BaselineStats]
    anomalies: List[Anomaly]
    trends: List[TrendAnalysis]
    correlations: List[CorrelationResult]
    cardinality: List[CardinalityAnalysis]
    recommendations: List[str]
    generated_at: datetime


class MetricsParser:
    """Parse metrics from various file formats"""

    @staticmethod
    def parse_csv(filepath: str) -> List[MetricData]:
        """Parse metrics from CSV file"""
        metrics_dict: Dict[str, MetricData] = {}

        with open(filepath, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Get timestamp
                ts_str = row.get('timestamp', row.get('time', row.get('date', '')))
                try:
                    ts = datetime.fromisoformat(ts_str.replace('Z', '+00:00'))
                except (ValueError, TypeError):
                    ts = datetime.now()

                # Process each numeric column as a metric
                for key, value in row.items():
                    if key in ('timestamp', 'time', 'date'):
                        continue

                    try:
                        val = float(value)
                    except (ValueError, TypeError):
                        continue

                    if key not in metrics_dict:
                        metrics_dict[key] = MetricData(
                            name=key,
                            timestamps=[],
                            values=[]
                        )

                    metrics_dict[key].timestamps.append(ts)
                    metrics_dict[key].values.append(val)

        return list(metrics_dict.values())

    @staticmethod
    def parse_json(filepath: str) -> List[MetricData]:
        """Parse metrics from JSON file"""
        with open(filepath, 'r') as f:
            data = json.load(f)

        metrics_dict: Dict[str, MetricData] = {}

        # Handle different JSON formats
        if isinstance(data, list):
            records = data
        elif isinstance(data, dict):
            records = data.get('metrics', data.get('data', [data]))
        else:
            records = []

        for record in records:
            # Get timestamp
            ts_str = record.get('timestamp', record.get('time', ''))
            try:
                ts = datetime.fromisoformat(str(ts_str).replace('Z', '+00:00'))
            except (ValueError, TypeError):
                ts = datetime.now()

            # Process each numeric field
            for key, value in record.items():
                if key in ('timestamp', 'time', 'date', 'labels'):
                    continue

                try:
                    val = float(value)
                except (ValueError, TypeError):
                    continue

                if key not in metrics_dict:
                    metrics_dict[key] = MetricData(
                        name=key,
                        timestamps=[],
                        values=[],
                        labels=record.get('labels', {})
                    )

                metrics_dict[key].timestamps.append(ts)
                metrics_dict[key].values.append(val)

        return list(metrics_dict.values())

    @staticmethod
    def parse_file(filepath: str) -> List[MetricData]:
        """Parse metrics file based on extension"""
        if filepath.endswith('.json'):
            return MetricsParser.parse_json(filepath)
        else:
            return MetricsParser.parse_csv(filepath)


class StatisticsCalculator:
    """Calculate statistical measures"""

    @staticmethod
    def mean(values: List[float]) -> float:
        """Calculate mean"""
        if not values:
            return 0.0
        return sum(values) / len(values)

    @staticmethod
    def median(values: List[float]) -> float:
        """Calculate median"""
        if not values:
            return 0.0
        sorted_vals = sorted(values)
        n = len(sorted_vals)
        mid = n // 2
        if n % 2 == 0:
            return (sorted_vals[mid - 1] + sorted_vals[mid]) / 2
        return sorted_vals[mid]

    @staticmethod
    def std_dev(values: List[float], mean: float = None) -> float:
        """Calculate standard deviation"""
        if len(values) < 2:
            return 0.0
        if mean is None:
            mean = StatisticsCalculator.mean(values)
        variance = sum((x - mean) ** 2 for x in values) / (len(values) - 1)
        return math.sqrt(variance)

    @staticmethod
    def percentile(values: List[float], p: float) -> float:
        """Calculate percentile (0-100)"""
        if not values:
            return 0.0
        sorted_vals = sorted(values)
        k = (len(sorted_vals) - 1) * (p / 100)
        f = math.floor(k)
        c = math.ceil(k)
        if f == c:
            return sorted_vals[int(k)]
        d0 = sorted_vals[int(f)] * (c - k)
        d1 = sorted_vals[int(c)] * (k - f)
        return d0 + d1

    @staticmethod
    def iqr(values: List[float]) -> float:
        """Calculate interquartile range"""
        q75 = StatisticsCalculator.percentile(values, 75)
        q25 = StatisticsCalculator.percentile(values, 25)
        return q75 - q25

    @staticmethod
    def coefficient_of_variation(values: List[float]) -> float:
        """Calculate coefficient of variation (volatility)"""
        if not values:
            return 0.0
        mean = StatisticsCalculator.mean(values)
        if mean == 0:
            return 0.0
        std = StatisticsCalculator.std_dev(values, mean)
        return std / abs(mean)


class BaselineCalculator:
    """Calculate metric baselines"""

    @staticmethod
    def calculate(metric: MetricData) -> BaselineStats:
        """Calculate baseline statistics for a metric"""
        values = metric.values

        if not values:
            return BaselineStats(
                metric_name=metric.name,
                count=0,
                mean=0.0,
                median=0.0,
                std_dev=0.0,
                min_val=0.0,
                max_val=0.0,
                p50=0.0,
                p90=0.0,
                p95=0.0,
                p99=0.0,
                iqr=0.0
            )

        mean = StatisticsCalculator.mean(values)
        std_dev = StatisticsCalculator.std_dev(values, mean)

        return BaselineStats(
            metric_name=metric.name,
            count=len(values),
            mean=round(mean, 4),
            median=round(StatisticsCalculator.median(values), 4),
            std_dev=round(std_dev, 4),
            min_val=round(min(values), 4),
            max_val=round(max(values), 4),
            p50=round(StatisticsCalculator.percentile(values, 50), 4),
            p90=round(StatisticsCalculator.percentile(values, 90), 4),
            p95=round(StatisticsCalculator.percentile(values, 95), 4),
            p99=round(StatisticsCalculator.percentile(values, 99), 4),
            iqr=round(StatisticsCalculator.iqr(values), 4)
        )


class AnomalyDetector:
    """Detect anomalies in metrics"""

    @staticmethod
    def detect_zscore(metric: MetricData, threshold: float = 3.0) -> List[Anomaly]:
        """Detect anomalies using Z-score method"""
        anomalies = []
        values = metric.values

        if len(values) < 3:
            return anomalies

        mean = StatisticsCalculator.mean(values)
        std_dev = StatisticsCalculator.std_dev(values, mean)

        if std_dev == 0:
            return anomalies

        for i, (ts, val) in enumerate(zip(metric.timestamps, values)):
            z_score = abs(val - mean) / std_dev
            if z_score >= threshold:
                severity = AnomalySeverity.HIGH if z_score >= threshold * 2 else \
                           AnomalySeverity.MEDIUM if z_score >= threshold * 1.5 else \
                           AnomalySeverity.LOW

                anomalies.append(Anomaly(
                    metric_name=metric.name,
                    timestamp=ts,
                    value=round(val, 4),
                    expected_value=round(mean, 4),
                    deviation=round(z_score, 2),
                    severity=severity,
                    method="zscore"
                ))

        return anomalies

    @staticmethod
    def detect_iqr(metric: MetricData, multiplier: float = 1.5) -> List[Anomaly]:
        """Detect anomalies using IQR method"""
        anomalies = []
        values = metric.values

        if len(values) < 4:
            return anomalies

        q25 = StatisticsCalculator.percentile(values, 25)
        q75 = StatisticsCalculator.percentile(values, 75)
        iqr = q75 - q25

        if iqr == 0:
            return anomalies

        lower_bound = q25 - multiplier * iqr
        upper_bound = q75 + multiplier * iqr
        median = StatisticsCalculator.median(values)

        for ts, val in zip(metric.timestamps, values):
            if val < lower_bound or val > upper_bound:
                deviation = abs(val - median) / iqr if iqr > 0 else 0
                severity = AnomalySeverity.HIGH if deviation >= 3 else \
                           AnomalySeverity.MEDIUM if deviation >= 2 else \
                           AnomalySeverity.LOW

                anomalies.append(Anomaly(
                    metric_name=metric.name,
                    timestamp=ts,
                    value=round(val, 4),
                    expected_value=round(median, 4),
                    deviation=round(deviation, 2),
                    severity=severity,
                    method="iqr"
                ))

        return anomalies


class TrendAnalyzer:
    """Analyze metric trends"""

    @staticmethod
    def analyze(metric: MetricData) -> TrendAnalysis:
        """Analyze trend for a metric"""
        values = metric.values
        n = len(values)

        if n < 2:
            return TrendAnalysis(
                metric_name=metric.name,
                direction=TrendDirection.STABLE,
                slope=0.0,
                r_squared=0.0,
                change_percent=0.0,
                volatility=0.0,
                seasonality_detected=False
            )

        # Simple linear regression
        x_vals = list(range(n))
        x_mean = sum(x_vals) / n
        y_mean = sum(values) / n

        numerator = sum((x - x_mean) * (y - y_mean) for x, y in zip(x_vals, values))
        denominator = sum((x - x_mean) ** 2 for x in x_vals)

        slope = numerator / denominator if denominator != 0 else 0

        # R-squared calculation
        y_pred = [y_mean + slope * (x - x_mean) for x in x_vals]
        ss_res = sum((y - yp) ** 2 for y, yp in zip(values, y_pred))
        ss_tot = sum((y - y_mean) ** 2 for y in values)
        r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0

        # Change percentage
        if values[0] != 0:
            change_percent = ((values[-1] - values[0]) / abs(values[0])) * 100
        else:
            change_percent = 0 if values[-1] == 0 else 100

        # Volatility (coefficient of variation)
        volatility = StatisticsCalculator.coefficient_of_variation(values)

        # Determine direction
        if volatility > 0.5:
            direction = TrendDirection.VOLATILE
        elif abs(slope) < 0.01 * y_mean if y_mean != 0 else 0.01:
            direction = TrendDirection.STABLE
        elif slope > 0:
            direction = TrendDirection.INCREASING
        else:
            direction = TrendDirection.DECREASING

        # Simple seasonality check (look for repeating patterns)
        seasonality = TrendAnalyzer._check_seasonality(values)

        return TrendAnalysis(
            metric_name=metric.name,
            direction=direction,
            slope=round(slope, 6),
            r_squared=round(r_squared, 4),
            change_percent=round(change_percent, 2),
            volatility=round(volatility, 4),
            seasonality_detected=seasonality
        )

    @staticmethod
    def _check_seasonality(values: List[float], min_periods: int = 3) -> bool:
        """Simple seasonality detection"""
        if len(values) < min_periods * 2:
            return False

        # Check for repeating patterns by comparing segments
        segment_size = len(values) // min_periods

        if segment_size < 2:
            return False

        segments = [values[i:i+segment_size] for i in range(0, len(values) - segment_size + 1, segment_size)]

        if len(segments) < 2:
            return False

        # Compare first and second half patterns
        correlations = []
        for i in range(len(segments) - 1):
            if len(segments[i]) == len(segments[i+1]):
                corr = TrendAnalyzer._simple_correlation(segments[i], segments[i+1])
                correlations.append(corr)

        if correlations:
            avg_corr = sum(correlations) / len(correlations)
            return avg_corr > 0.7

        return False

    @staticmethod
    def _simple_correlation(x: List[float], y: List[float]) -> float:
        """Calculate simple correlation coefficient"""
        n = len(x)
        if n != len(y) or n < 2:
            return 0.0

        x_mean = sum(x) / n
        y_mean = sum(y) / n

        numerator = sum((xi - x_mean) * (yi - y_mean) for xi, yi in zip(x, y))
        denom_x = math.sqrt(sum((xi - x_mean) ** 2 for xi in x))
        denom_y = math.sqrt(sum((yi - y_mean) ** 2 for yi in y))

        if denom_x == 0 or denom_y == 0:
            return 0.0

        return numerator / (denom_x * denom_y)


class CorrelationAnalyzer:
    """Analyze correlations between metrics"""

    @staticmethod
    def analyze(metrics: List[MetricData]) -> List[CorrelationResult]:
        """Analyze correlations between all metric pairs"""
        results = []

        for i, metric_a in enumerate(metrics):
            for metric_b in metrics[i+1:]:
                # Align time series
                aligned_a, aligned_b = CorrelationAnalyzer._align_series(metric_a, metric_b)

                if len(aligned_a) < 3:
                    continue

                corr = TrendAnalyzer._simple_correlation(aligned_a, aligned_b)

                # Determine strength
                abs_corr = abs(corr)
                if abs_corr >= 0.7:
                    strength = "strong"
                elif abs_corr >= 0.4:
                    strength = "moderate"
                elif abs_corr >= 0.2:
                    strength = "weak"
                else:
                    strength = "none"

                direction = "positive" if corr > 0 else "negative"

                results.append(CorrelationResult(
                    metric_a=metric_a.name,
                    metric_b=metric_b.name,
                    correlation=round(corr, 4),
                    strength=strength,
                    direction=direction
                ))

        return results

    @staticmethod
    def _align_series(a: MetricData, b: MetricData) -> Tuple[List[float], List[float]]:
        """Align two time series by timestamp"""
        a_dict = dict(zip(a.timestamps, a.values))
        b_dict = dict(zip(b.timestamps, b.values))

        common_ts = set(a_dict.keys()) & set(b_dict.keys())

        aligned_a = [a_dict[ts] for ts in sorted(common_ts)]
        aligned_b = [b_dict[ts] for ts in sorted(common_ts)]

        return aligned_a, aligned_b


class CardinalityAnalyzer:
    """Analyze metric cardinality"""

    # Approximate bytes per metric series in Prometheus
    BYTES_PER_SERIES = 3000  # ~3KB per series

    @staticmethod
    def analyze(metrics: List[MetricData]) -> List[CardinalityAnalysis]:
        """Analyze cardinality for metrics"""
        results = []

        # Group metrics by base name (before labels)
        metric_groups: Dict[str, List[MetricData]] = defaultdict(list)
        for m in metrics:
            base_name = m.name.split('{')[0]
            metric_groups[base_name].append(m)

        for base_name, group in metric_groups.items():
            total_series = len(group)

            # Collect all unique label values
            label_values: Dict[str, set] = defaultdict(set)
            for m in group:
                for label, value in m.labels.items():
                    label_values[label].add(value)

            unique_labels = {k: len(v) for k, v in label_values.items()}

            # Identify high cardinality labels (>100 unique values)
            high_cardinality = [
                label for label, count in unique_labels.items()
                if count > 100
            ]

            # Estimate memory usage
            estimated_memory = (total_series * CardinalityAnalyzer.BYTES_PER_SERIES) / (1024 * 1024)

            # Generate recommendations
            recommendations = []
            if high_cardinality:
                recommendations.append(
                    f"Consider removing or aggregating high-cardinality labels: {', '.join(high_cardinality)}"
                )
            if total_series > 10000:
                recommendations.append(
                    f"High series count ({total_series:,}). Consider reducing label cardinality or aggregating metrics."
                )
            if estimated_memory > 100:
                recommendations.append(
                    f"Estimated memory usage ({estimated_memory:.1f} MB) is high. Review retention and cardinality."
                )

            results.append(CardinalityAnalysis(
                metric_name=base_name,
                total_series=total_series,
                unique_labels=unique_labels,
                high_cardinality_labels=high_cardinality,
                estimated_memory_mb=round(estimated_memory, 2),
                recommendations=recommendations
            ))

        return results


class RecommendationGenerator:
    """Generate optimization recommendations"""

    @staticmethod
    def generate(report: AnalysisReport) -> List[str]:
        """Generate recommendations based on analysis"""
        recommendations = []

        # Anomaly-based recommendations
        if report.anomalies:
            high_severity = [a for a in report.anomalies if a.severity == AnomalySeverity.HIGH]
            if high_severity:
                recommendations.append(
                    f"Investigate {len(high_severity)} high-severity anomalies detected"
                )

        # Trend-based recommendations
        for trend in report.trends:
            if trend.direction == TrendDirection.INCREASING and trend.change_percent > 50:
                recommendations.append(
                    f"{trend.metric_name}: Significant increase ({trend.change_percent:.1f}%). "
                    f"Consider capacity planning."
                )
            elif trend.direction == TrendDirection.VOLATILE:
                recommendations.append(
                    f"{trend.metric_name}: High volatility detected (CV={trend.volatility:.2f}). "
                    f"Investigate stability issues."
                )
            if trend.seasonality_detected:
                recommendations.append(
                    f"{trend.metric_name}: Seasonal pattern detected. "
                    f"Consider time-based scaling policies."
                )

        # Correlation-based recommendations
        strong_correlations = [c for c in report.correlations if c.strength == "strong"]
        if strong_correlations:
            for corr in strong_correlations[:3]:  # Top 3
                recommendations.append(
                    f"Strong {corr.direction} correlation ({corr.correlation:.2f}) between "
                    f"{corr.metric_a} and {corr.metric_b}. Consider combining in dashboards."
                )

        # Cardinality-based recommendations
        for card in report.cardinality:
            recommendations.extend(card.recommendations)

        return recommendations


def run_analysis(metrics: List[MetricData], analysis_type: AnalysisType,
                 threshold: float = 3.0) -> AnalysisReport:
    """Run specified analysis type"""
    baselines = []
    anomalies = []
    trends = []
    correlations = []
    cardinality = []

    # Always calculate baselines
    for metric in metrics:
        baselines.append(BaselineCalculator.calculate(metric))

    if analysis_type == AnalysisType.ANOMALY or analysis_type == AnalysisType.BASELINE:
        for metric in metrics:
            anomalies.extend(AnomalyDetector.detect_zscore(metric, threshold))

    if analysis_type == AnalysisType.TREND or analysis_type == AnalysisType.BASELINE:
        for metric in metrics:
            trends.append(TrendAnalyzer.analyze(metric))

    if analysis_type == AnalysisType.CORRELATION:
        correlations = CorrelationAnalyzer.analyze(metrics)

    if analysis_type == AnalysisType.CARDINALITY:
        cardinality = CardinalityAnalyzer.analyze(metrics)

    report = AnalysisReport(
        analysis_type=analysis_type,
        metrics_analyzed=[m.name for m in metrics],
        baselines=baselines,
        anomalies=anomalies,
        trends=trends,
        correlations=correlations,
        cardinality=cardinality,
        recommendations=[],
        generated_at=datetime.now()
    )

    # Generate recommendations
    report.recommendations = RecommendationGenerator.generate(report)

    return report


def format_output(report: AnalysisReport, output_format: str) -> str:
    """Format analysis report"""
    if output_format == "json":
        data = {
            "analysis_type": report.analysis_type.value,
            "metrics_analyzed": report.metrics_analyzed,
            "generated_at": report.generated_at.isoformat(),
            "baselines": [
                {
                    "metric": b.metric_name,
                    "count": b.count,
                    "mean": b.mean,
                    "median": b.median,
                    "std_dev": b.std_dev,
                    "min": b.min_val,
                    "max": b.max_val,
                    "p50": b.p50,
                    "p90": b.p90,
                    "p95": b.p95,
                    "p99": b.p99
                }
                for b in report.baselines
            ],
            "anomalies": [
                {
                    "metric": a.metric_name,
                    "timestamp": a.timestamp.isoformat(),
                    "value": a.value,
                    "expected": a.expected_value,
                    "deviation": a.deviation,
                    "severity": a.severity.value,
                    "method": a.method
                }
                for a in report.anomalies
            ],
            "trends": [
                {
                    "metric": t.metric_name,
                    "direction": t.direction.value,
                    "slope": t.slope,
                    "r_squared": t.r_squared,
                    "change_percent": t.change_percent,
                    "volatility": t.volatility,
                    "seasonal": t.seasonality_detected
                }
                for t in report.trends
            ],
            "correlations": [
                {
                    "metric_a": c.metric_a,
                    "metric_b": c.metric_b,
                    "correlation": c.correlation,
                    "strength": c.strength,
                    "direction": c.direction
                }
                for c in report.correlations
            ],
            "cardinality": [
                {
                    "metric": c.metric_name,
                    "total_series": c.total_series,
                    "unique_labels": c.unique_labels,
                    "high_cardinality_labels": c.high_cardinality_labels,
                    "estimated_memory_mb": c.estimated_memory_mb
                }
                for c in report.cardinality
            ],
            "recommendations": report.recommendations
        }
        return json.dumps(data, indent=2)

    elif output_format == "markdown":
        lines = [
            f"# Metrics Analysis Report",
            "",
            f"**Analysis Type:** {report.analysis_type.value}",
            f"**Generated:** {report.generated_at.strftime('%Y-%m-%d %H:%M:%S')}",
            f"**Metrics Analyzed:** {len(report.metrics_analyzed)}",
            "",
        ]

        if report.baselines:
            lines.extend([
                "## Baselines",
                "",
                "| Metric | Count | Mean | Median | Std Dev | P95 | P99 |",
                "|--------|-------|------|--------|---------|-----|-----|"
            ])
            for b in report.baselines:
                lines.append(f"| {b.metric_name} | {b.count:,} | {b.mean:.2f} | {b.median:.2f} | {b.std_dev:.2f} | {b.p95:.2f} | {b.p99:.2f} |")
            lines.append("")

        if report.anomalies:
            lines.extend([
                "## Anomalies",
                "",
                "| Metric | Timestamp | Value | Expected | Deviation | Severity |",
                "|--------|-----------|-------|----------|-----------|----------|"
            ])
            for a in report.anomalies[:20]:  # Limit to 20
                lines.append(f"| {a.metric_name} | {a.timestamp.strftime('%Y-%m-%d %H:%M')} | {a.value:.2f} | {a.expected_value:.2f} | {a.deviation:.1f}σ | {a.severity.value} |")
            if len(report.anomalies) > 20:
                lines.append(f"\n*...and {len(report.anomalies) - 20} more anomalies*")
            lines.append("")

        if report.trends:
            lines.extend([
                "## Trends",
                "",
                "| Metric | Direction | Change % | Volatility | R² |",
                "|--------|-----------|----------|------------|-----|"
            ])
            for t in report.trends:
                lines.append(f"| {t.metric_name} | {t.direction.value} | {t.change_percent:+.1f}% | {t.volatility:.2f} | {t.r_squared:.2f} |")
            lines.append("")

        if report.correlations:
            lines.extend([
                "## Correlations",
                "",
                "| Metric A | Metric B | Correlation | Strength |",
                "|----------|----------|-------------|----------|"
            ])
            for c in report.correlations:
                lines.append(f"| {c.metric_a} | {c.metric_b} | {c.correlation:+.2f} | {c.strength} |")
            lines.append("")

        if report.recommendations:
            lines.extend([
                "## Recommendations",
                ""
            ])
            for i, rec in enumerate(report.recommendations, 1):
                lines.append(f"{i}. {rec}")
            lines.append("")

        return "\n".join(lines)

    elif output_format == "csv":
        lines = ["metric,count,mean,median,std_dev,min,max,p95,p99"]
        for b in report.baselines:
            lines.append(f"{b.metric_name},{b.count},{b.mean},{b.median},{b.std_dev},{b.min_val},{b.max_val},{b.p95},{b.p99}")
        return "\n".join(lines)

    else:  # text
        lines = [
            "=" * 60,
            f"Metrics Analysis Report ({report.analysis_type.value})",
            "=" * 60,
            "",
            f"Generated: {report.generated_at.strftime('%Y-%m-%d %H:%M:%S')}",
            f"Metrics analyzed: {len(report.metrics_analyzed)}",
            ""
        ]

        if report.baselines:
            lines.extend([
                "-" * 60,
                "Baselines",
                "-" * 60
            ])
            for b in report.baselines:
                lines.append(f"  {b.metric_name}:")
                lines.append(f"    Count: {b.count:,}  Mean: {b.mean:.2f}  Std: {b.std_dev:.2f}")
                lines.append(f"    P50: {b.p50:.2f}  P95: {b.p95:.2f}  P99: {b.p99:.2f}")
            lines.append("")

        if report.anomalies:
            lines.extend([
                "-" * 60,
                f"Anomalies ({len(report.anomalies)} detected)",
                "-" * 60
            ])
            for a in report.anomalies[:10]:
                emoji = "🔴" if a.severity == AnomalySeverity.HIGH else "🟡" if a.severity == AnomalySeverity.MEDIUM else "🟢"
                lines.append(f"  {emoji} {a.metric_name}: {a.value:.2f} (expected {a.expected_value:.2f}, {a.deviation:.1f}σ)")
            if len(report.anomalies) > 10:
                lines.append(f"  ...and {len(report.anomalies) - 10} more")
            lines.append("")

        if report.trends:
            lines.extend([
                "-" * 60,
                "Trends",
                "-" * 60
            ])
            for t in report.trends:
                emoji = "📈" if t.direction == TrendDirection.INCREASING else \
                        "📉" if t.direction == TrendDirection.DECREASING else \
                        "📊" if t.direction == TrendDirection.VOLATILE else "➡️"
                lines.append(f"  {emoji} {t.metric_name}: {t.direction.value} ({t.change_percent:+.1f}%)")
            lines.append("")

        if report.recommendations:
            lines.extend([
                "-" * 60,
                "Recommendations",
                "-" * 60
            ])
            for rec in report.recommendations:
                lines.append(f"  • {rec}")
            lines.append("")

        lines.append("=" * 60)
        return "\n".join(lines)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Analyze metrics for anomalies, trends, and optimization opportunities",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Detect anomalies in metrics
  %(prog)s --input metrics.csv --analysis-type anomaly --threshold 3.0 --output json

  # Analyze trends
  %(prog)s --input metrics.json --analysis-type trend --output markdown

  # Find correlations between metrics
  %(prog)s --input metrics.csv --analysis-type correlation --output text

  # Analyze cardinality for optimization
  %(prog)s --input metrics.csv --analysis-type cardinality --output json

Analysis Types:
  anomaly      - Detect statistical anomalies using Z-score and IQR methods
  trend        - Analyze metric trends (increasing, decreasing, volatile)
  correlation  - Find correlations between different metrics
  baseline     - Calculate statistical baselines with anomaly detection
  cardinality  - Analyze metric cardinality for memory optimization
        """
    )

    parser.add_argument(
        "--input", "-i",
        required=True,
        help="Input metrics file (CSV or JSON)"
    )

    parser.add_argument(
        "--analysis-type", "-a",
        choices=[t.value for t in AnalysisType],
        default="anomaly",
        help="Type of analysis to perform (default: anomaly)"
    )

    parser.add_argument(
        "--metrics", "-m",
        help="Comma-separated metric names to analyze (analyzes all if not specified)"
    )

    parser.add_argument(
        "--threshold", "-t",
        type=float,
        default=3.0,
        help="Anomaly detection threshold in standard deviations (default: 3.0)"
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
        logger.info(f"Loaded {len(metrics)} metrics")

        # Filter metrics if specified
        if args.metrics:
            metric_names = [m.strip() for m in args.metrics.split(",")]
            metrics = [m for m in metrics if m.name in metric_names]
            logger.info(f"Filtered to {len(metrics)} metrics")

        if not metrics:
            logger.error("No metrics found to analyze")
            return 1

        # Run analysis
        analysis_type = AnalysisType(args.analysis_type)
        report = run_analysis(metrics, analysis_type, args.threshold)

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
        logger.error(f"Error analyzing metrics: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
