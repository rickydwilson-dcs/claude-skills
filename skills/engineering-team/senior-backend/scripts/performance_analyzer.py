#!/usr/bin/env python3
"""
Performance Analyzer - Backend Performance Analysis Tool

Analyzes backend application performance metrics, identifies bottlenecks,
and provides optimization recommendations for APIs, databases, and services.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

class PerformanceAnalyzer:
    """Analyzes backend performance metrics and identifies optimization opportunities"""

    PERFORMANCE_THRESHOLDS = {
        'api_response_time': {
            'excellent': 100,  # ms
            'good': 300,
            'acceptable': 1000,
            'poor': 3000
        },
        'database_query_time': {
            'excellent': 50,
            'good': 200,
            'acceptable': 500,
            'poor': 1000
        },
        'memory_usage': {
            'excellent': 50,  # %
            'good': 70,
            'acceptable': 85,
            'poor': 95
        },
        'cpu_usage': {
            'excellent': 40,
            'good': 60,
            'acceptable': 80,
            'poor': 95
        }
    }

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.metrics = {}
        self.bottlenecks = []
        self.recommendations = []

    def analyze_api_performance(self, response_times: List[float]) -> Dict:
        """Analyze API endpoint response times"""
        if not response_times:
            return {'status': 'no_data'}

        avg_time = sum(response_times) / len(response_times)
        min_time = min(response_times)
        max_time = max(response_times)
        p95 = sorted(response_times)[int(len(response_times) * 0.95)] if response_times else 0
        p99 = sorted(response_times)[int(len(response_times) * 0.99)] if response_times else 0

        # Determine performance level
        threshold = self.PERFORMANCE_THRESHOLDS['api_response_time']
        if avg_time <= threshold['excellent']:
            status = 'excellent'
        elif avg_time <= threshold['good']:
            status = 'good'
        elif avg_time <= threshold['acceptable']:
            status = 'acceptable'
        else:
            status = 'poor'

        analysis = {
            'average_ms': round(avg_time, 2),
            'min_ms': round(min_time, 2),
            'max_ms': round(max_time, 2),
            'p95_ms': round(p95, 2),
            'p99_ms': round(p99, 2),
            'status': status,
            'sample_count': len(response_times)
        }

        # Identify bottlenecks
        if status in ['acceptable', 'poor']:
            self.bottlenecks.append({
                'type': 'api_performance',
                'severity': 'high' if status == 'poor' else 'medium',
                'message': f"API response time {avg_time:.0f}ms exceeds target",
                'metric': analysis
            })

        return analysis

    def analyze_database_performance(self, query_times: List[float], query_types: List[str] = None) -> Dict:
        """Analyze database query performance"""
        if not query_times:
            return {'status': 'no_data'}

        avg_time = sum(query_times) / len(query_times)
        slow_queries = [t for t in query_times if t > 1000]  # > 1 second

        threshold = self.PERFORMANCE_THRESHOLDS['database_query_time']
        if avg_time <= threshold['excellent']:
            status = 'excellent'
        elif avg_time <= threshold['good']:
            status = 'good'
        elif avg_time <= threshold['acceptable']:
            status = 'acceptable'
        else:
            status = 'poor'

        analysis = {
            'average_ms': round(avg_time, 2),
            'slow_query_count': len(slow_queries),
            'slow_query_percentage': round((len(slow_queries) / len(query_times)) * 100, 1),
            'total_queries': len(query_times),
            'status': status
        }

        # Identify bottlenecks
        if len(slow_queries) > 0:
            self.bottlenecks.append({
                'type': 'database_performance',
                'severity': 'high' if len(slow_queries) > len(query_times) * 0.1 else 'medium',
                'message': f"{len(slow_queries)} slow queries detected (>{1000}ms)",
                'metric': analysis
            })

        return analysis

    def analyze_resource_usage(self, cpu_usage: float, memory_usage: float) -> Dict:
        """Analyze CPU and memory usage"""
        analysis = {
            'cpu_usage_percent': round(cpu_usage, 1),
            'memory_usage_percent': round(memory_usage, 1)
        }

        # CPU analysis
        cpu_threshold = self.PERFORMANCE_THRESHOLDS['cpu_usage']
        if cpu_usage >= cpu_threshold['poor']:
            analysis['cpu_status'] = 'critical'
            self.bottlenecks.append({
                'type': 'cpu_usage',
                'severity': 'high',
                'message': f"CPU usage critically high: {cpu_usage:.1f}%"
            })
        elif cpu_usage >= cpu_threshold['acceptable']:
            analysis['cpu_status'] = 'high'
        elif cpu_usage >= cpu_threshold['good']:
            analysis['cpu_status'] = 'moderate'
        else:
            analysis['cpu_status'] = 'normal'

        # Memory analysis
        mem_threshold = self.PERFORMANCE_THRESHOLDS['memory_usage']
        if memory_usage >= mem_threshold['poor']:
            analysis['memory_status'] = 'critical'
            self.bottlenecks.append({
                'type': 'memory_usage',
                'severity': 'high',
                'message': f"Memory usage critically high: {memory_usage:.1f}%"
            })
        elif memory_usage >= mem_threshold['acceptable']:
            analysis['memory_status'] = 'high'
        elif memory_usage >= mem_threshold['good']:
            analysis['memory_status'] = 'moderate'
        else:
            analysis['memory_status'] = 'normal'

        return analysis

    def generate_recommendations(self) -> List[str]:
        """Generate optimization recommendations based on bottlenecks"""
        recommendations = []

        # Group bottlenecks by type
        bottleneck_types = set(b['type'] for b in self.bottlenecks)

        for btype in bottleneck_types:
            if btype == 'api_performance':
                recommendations.extend([
                    "Implement response caching (Redis/Memcached) for frequently accessed data",
                    "Add database query optimization and indexing",
                    "Consider implementing pagination for large result sets",
                    "Use asynchronous processing for non-critical operations"
                ])
            elif btype == 'database_performance':
                recommendations.extend([
                    "Add database indexes on frequently queried columns",
                    "Review and optimize N+1 query patterns",
                    "Implement query result caching",
                    "Use database query explain plans to identify slow queries"
                ])
            elif btype == 'cpu_usage':
                recommendations.extend([
                    "Optimize CPU-intensive algorithms and operations",
                    "Implement job queues for background processing",
                    "Consider horizontal scaling (add more instances)",
                    "Profile code to identify CPU hotspots"
                ])
            elif btype == 'memory_usage':
                recommendations.extend([
                    "Review memory leaks and implement proper cleanup",
                    "Optimize data structures and reduce object retention",
                    "Implement pagination to reduce memory footprint",
                    "Increase heap size or upgrade instance type"
                ])

        # General recommendations
        recommendations.extend([
            "Set up APM (Application Performance Monitoring) tool",
            "Implement distributed tracing for request flows",
            "Create performance baselines and alerts"
        ])

        return recommendations[:10]  # Return top 10

    def calculate_performance_score(self) -> int:
        """Calculate overall performance score (0-100)"""
        score = 100

        for bottleneck in self.bottlenecks:
            if bottleneck['severity'] == 'high':
                score -= 20
            elif bottleneck['severity'] == 'medium':
                score -= 10
            else:
                score -= 5

        return max(0, min(100, score))

    def print_report(self, metrics: Dict):
        """Print human-readable performance report"""
        print("\n" + "="*60)
        print("BACKEND PERFORMANCE ANALYSIS")
        print("="*60)

        if 'api_performance' in metrics:
            api = metrics['api_performance']
            print(f"\nAPI Performance:")
            print(f"   Average Response Time: {api['average_ms']}ms")
            print(f"   P95: {api['p95_ms']}ms | P99: {api['p99_ms']}ms")
            print(f"   Range: {api['min_ms']}ms - {api['max_ms']}ms")
            print(f"   Status: {api['status'].upper()}")

        if 'database_performance' in metrics:
            db = metrics['database_performance']
            print(f"\nDatabase Performance:")
            print(f"   Average Query Time: {db['average_ms']}ms")
            print(f"   Slow Queries: {db['slow_query_count']} ({db['slow_query_percentage']}%)")
            print(f"   Total Queries: {db['total_queries']}")
            print(f"   Status: {db['status'].upper()}")

        if 'resource_usage' in metrics:
            res = metrics['resource_usage']
            print(f"\nResource Usage:")
            print(f"   CPU: {res['cpu_usage_percent']}% ({res['cpu_status']})")
            print(f"   Memory: {res['memory_usage_percent']}% ({res['memory_status']})")

        if 'performance_score' in metrics:
            score = metrics['performance_score']
            print(f"\nPerformance Score: {score}/100")

        if self.bottlenecks:
            print(f"\nBottlenecks Identified ({len(self.bottlenecks)}):")
            for i, b in enumerate(self.bottlenecks, 1):
                print(f"   {i}. [{b['severity'].upper()}] {b['message']}")

        if self.recommendations:
            print(f"\nOptimization Recommendations:")
            for i, rec in enumerate(self.recommendations[:8], 1):
                print(f"   {i}. {rec}")

        print("\n" + "="*60)

def main():
    parser = argparse.ArgumentParser(
        description="Analyze backend application performance and identify bottlenecks",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze API performance
  %(prog)s --api-times 120 150 180 95 210

  # Full performance analysis
  %(prog)s --api-times 120 150 180 --db-times 45 60 120 --cpu 75 --memory 68

  # JSON output
  %(prog)s --api-times 120 150 180 --json
        """
    )

    parser.add_argument(
        '--api-times',
        nargs='+',
        type=float,
        help='API response times in milliseconds (space-separated)'
    )
    parser.add_argument(
        '--db-times',
        nargs='+',
        type=float,
        help='Database query times in milliseconds (space-separated)'
    )
    parser.add_argument(
        '--cpu',
        type=float,
        help='CPU usage percentage'
    )
    parser.add_argument(
        '--memory',
        type=float,
        help='Memory usage percentage'
    )
    parser.add_argument(
        '--file',
        help='JSON file with performance metrics'
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
    parser.add_argument(
        '-o', '--output',
        help='Output file path'
    )

    args = parser.parse_args()

    analyzer = PerformanceAnalyzer(verbose=args.verbose)
    metrics = {}

    # Load from file if provided
    if args.file:
        try:
            with open(args.file, 'r') as f:
                data = json.load(f)
                args.api_times = data.get('api_times', [])
                args.db_times = data.get('db_times', [])
                args.cpu = data.get('cpu_usage')
                args.memory = data.get('memory_usage')
        except Exception as e:
            print(f"Error loading file: {e}", file=sys.stderr)
            sys.exit(1)

    # Analyze API performance
    if args.api_times:
        metrics['api_performance'] = analyzer.analyze_api_performance(args.api_times)

    # Analyze database performance
    if args.db_times:
        metrics['database_performance'] = analyzer.analyze_database_performance(args.db_times)

    # Analyze resource usage
    if args.cpu is not None and args.memory is not None:
        metrics['resource_usage'] = analyzer.analyze_resource_usage(args.cpu, args.memory)

    if not metrics:
        parser.print_help()
        sys.exit(0)

    # Generate recommendations
    analyzer.recommendations = analyzer.generate_recommendations()
    metrics['recommendations'] = analyzer.recommendations
    metrics['bottlenecks'] = analyzer.bottlenecks
    metrics['performance_score'] = analyzer.calculate_performance_score()

    # Output
    if args.json:
        output = json.dumps(metrics, indent=2)
        if args.output:
            Path(args.output).write_text(output)
            print(f"Report written to {args.output}")
        else:
            print(output)
    else:
        analyzer.print_report(metrics)

if __name__ == "__main__":
    main()
