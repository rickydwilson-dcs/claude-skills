#!/usr/bin/env python3
"""
API Load Tester
HTTP load generation tool for performance benchmarking and capacity planning.

Features:
- Concurrent request handling with configurable user count
- Latency percentiles (P50, P95, P99)
- Throughput measurement (RPS, KB/s)
- Multiple HTTP methods (GET, POST, PUT, DELETE)
- Custom headers and payload support
- HTML and JSON report generation

Standard library only - no external dependencies required.
"""

import argparse
import json
import logging
import ssl
import statistics
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class RequestResult:
    """Result of a single HTTP request"""
    success: bool
    status_code: int
    response_time_ms: float
    response_size_bytes: int
    error_message: Optional[str] = None


@dataclass
class LoadTestMetrics:
    """Aggregated metrics from load test"""
    total_requests: int
    successful_requests: int
    failed_requests: int
    total_time_seconds: float
    min_response_time_ms: float
    max_response_time_ms: float
    avg_response_time_ms: float
    median_response_time_ms: float
    p95_response_time_ms: float
    p99_response_time_ms: float
    requests_per_second: float
    throughput_bytes_per_second: float
    error_rate_percent: float
    status_code_distribution: Dict[int, int] = field(default_factory=dict)
    error_distribution: Dict[str, int] = field(default_factory=dict)


class APILoadTester:
    """HTTP load testing tool for API performance benchmarking."""

    def __init__(self, url: str, concurrent_users: int = 10, total_requests: int = 100,
                 method: str = "GET", headers: Optional[Dict[str, str]] = None,
                 payload: Optional[str] = None, timeout: int = 30, verbose: bool = False):
        if verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("APILoadTester initialized")

        self.url = url
        self.concurrent_users = concurrent_users
        self.total_requests = total_requests
        self.method = method.upper()
        self.headers = headers or {}
        self.payload = payload
        self.timeout = timeout
        self.verbose = verbose
        self.results: List[RequestResult] = []
        self._ssl_context = ssl.create_default_context()
        self._ssl_context.check_hostname = False
        self._ssl_context.verify_mode = ssl.CERT_NONE

    def _make_request(self) -> RequestResult:
        """Execute a single HTTP request and measure response time"""
        logger.debug(f"Making {self.method} request to {self.url}")
        start_time = time.perf_counter()
        try:
            data = self.payload.encode('utf-8') if self.payload else None
            request = urllib.request.Request(self.url, data=data, headers=self.headers, method=self.method)
            if 'User-Agent' not in self.headers:
                request.add_header('User-Agent', 'APILoadTester/1.0')
            if data and 'Content-Type' not in self.headers:
                request.add_header('Content-Type', 'application/json')

            with urllib.request.urlopen(request, timeout=self.timeout, context=self._ssl_context) as response:
                response_data = response.read()
                return RequestResult(True, response.status, (time.perf_counter() - start_time) * 1000, len(response_data))

        except urllib.error.HTTPError as e:
            logger.error(f"HTTP error {e.code}: {e.reason}")
            return RequestResult(False, e.code, (time.perf_counter() - start_time) * 1000, 0, f"HTTP {e.code}: {e.reason}")
        except urllib.error.URLError as e:
            logger.error(f"URL error: {str(e.reason)}")
            return RequestResult(False, 0, (time.perf_counter() - start_time) * 1000, 0, f"URL Error: {str(e.reason)}")
        except Exception as e:
            logger.error(f"Request exception: {str(e)}")
            return RequestResult(False, 0, (time.perf_counter() - start_time) * 1000, 0, str(e))

    def _worker(self, request_count: int) -> List[RequestResult]:
        """Worker function to execute multiple requests"""
        results = []
        for _ in range(request_count):
            result = self._make_request()
            results.append(result)
            if self.verbose:
                status = "OK" if result.success else "FAIL"
                print(f"  [{status}] {result.response_time_ms:.2f}ms - {result.status_code}")
        return results

    def run(self) -> LoadTestMetrics:
        """Execute the load test and return metrics"""
        logger.debug(f"Starting load test: {self.url} with {self.concurrent_users} users, {self.total_requests} requests")
        if self.verbose:
            print(f"Starting load test: {self.url}")
            print(f"  Users: {self.concurrent_users}, Requests: {self.total_requests}, Method: {self.method}\n")

        requests_per_worker = self.total_requests // self.concurrent_users
        extra_requests = self.total_requests % self.concurrent_users
        work_distribution = [requests_per_worker + (1 if i < extra_requests else 0) for i in range(self.concurrent_users)]

        start_time = time.perf_counter()
        all_results = []
        with ThreadPoolExecutor(max_workers=self.concurrent_users) as executor:
            futures = [executor.submit(self._worker, count) for count in work_distribution]
            for future in as_completed(futures):
                all_results.extend(future.result())

        self.results = all_results
        return self._calculate_metrics(time.perf_counter() - start_time)

    def _calculate_metrics(self, total_time: float) -> LoadTestMetrics:
        """Calculate aggregated metrics from results"""
        logger.debug("Calculating load test metrics")
        if not self.results:
            logger.warning("No results to calculate metrics from")
            return LoadTestMetrics(0, 0, 0, total_time, 0, 0, 0, 0, 0, 0, 0, 0, 0)

        successful = [r for r in self.results if r.success]
        failed = [r for r in self.results if not r.success]
        response_times = sorted([r.response_time_ms for r in self.results])

        def percentile(data: List[float], p: float) -> float:
            if not data:
                return 0.0
            k = (len(data) - 1) * (p / 100)
            f, c = int(k), min(int(k) + 1, len(data) - 1)
            return data[f] + (k - f) * (data[c] - data[f])

        status_codes: Dict[int, int] = {}
        for r in self.results:
            status_codes[r.status_code] = status_codes.get(r.status_code, 0) + 1

        errors: Dict[str, int] = {}
        for r in failed:
            if r.error_message:
                errors[r.error_message] = errors.get(r.error_message, 0) + 1

        total_bytes = sum(r.response_size_bytes for r in self.results)

        return LoadTestMetrics(
            total_requests=len(self.results), successful_requests=len(successful), failed_requests=len(failed),
            total_time_seconds=total_time, min_response_time_ms=min(response_times), max_response_time_ms=max(response_times),
            avg_response_time_ms=statistics.mean(response_times), median_response_time_ms=statistics.median(response_times),
            p95_response_time_ms=percentile(response_times, 95), p99_response_time_ms=percentile(response_times, 99),
            requests_per_second=len(self.results) / total_time if total_time > 0 else 0,
            throughput_bytes_per_second=total_bytes / total_time if total_time > 0 else 0,
            error_rate_percent=(len(failed) / len(self.results) * 100) if self.results else 0,
            status_code_distribution=status_codes, error_distribution=errors
        )


def format_text_report(metrics: LoadTestMetrics, url: str, method: str, concurrent_users: int) -> str:
    """Generate human-readable text report"""
    lines = [
        "=" * 70, "API LOAD TEST RESULTS", "=" * 70, "",
        "TEST CONFIGURATION", "-" * 40,
        f"  URL:              {url}", f"  Method:           {method}",
        f"  Concurrent Users: {concurrent_users}", f"  Total Requests:   {metrics.total_requests}",
        f"  Test Duration:    {metrics.total_time_seconds:.2f}s", "",
        "REQUEST STATISTICS", "-" * 40,
        f"  Successful:       {metrics.successful_requests}", f"  Failed:           {metrics.failed_requests}",
        f"  Error Rate:       {metrics.error_rate_percent:.2f}%", "",
        "RESPONSE TIME (ms)", "-" * 40,
        f"  Min:              {metrics.min_response_time_ms:.2f}", f"  Max:              {metrics.max_response_time_ms:.2f}",
        f"  Average:          {metrics.avg_response_time_ms:.2f}", f"  Median (P50):     {metrics.median_response_time_ms:.2f}",
        f"  P95:              {metrics.p95_response_time_ms:.2f}", f"  P99:              {metrics.p99_response_time_ms:.2f}", "",
        "THROUGHPUT", "-" * 40,
        f"  Requests/sec:     {metrics.requests_per_second:.2f}",
        f"  Throughput:       {metrics.throughput_bytes_per_second / 1024:.2f} KB/s", ""
    ]
    if metrics.status_code_distribution:
        lines.extend(["STATUS CODE DISTRIBUTION", "-" * 40])
        for code, count in sorted(metrics.status_code_distribution.items()):
            pct = (count / metrics.total_requests * 100) if metrics.total_requests else 0
            lines.append(f"  {code}: {count} ({pct:.1f}%)")
        lines.append("")
    if metrics.error_distribution:
        lines.extend(["ERROR DISTRIBUTION", "-" * 40])
        for error, count in sorted(metrics.error_distribution.items(), key=lambda x: -x[1])[:5]:
            lines.append(f"  {error}: {count}")
        lines.append("")
    lines.append("=" * 70)
    return "\n".join(lines)


def format_json_output(metrics: LoadTestMetrics, url: str, method: str, concurrent_users: int) -> str:
    """Generate JSON output"""
    return json.dumps({
        "metadata": {"tool": "api_load_tester", "version": "1.0.0", "timestamp": datetime.now().isoformat(),
                     "url": url, "method": method, "concurrent_users": concurrent_users},
        "summary": {"total_requests": metrics.total_requests, "successful_requests": metrics.successful_requests,
                    "failed_requests": metrics.failed_requests, "total_time_seconds": round(metrics.total_time_seconds, 3),
                    "error_rate_percent": round(metrics.error_rate_percent, 2)},
        "response_times_ms": {"min": round(metrics.min_response_time_ms, 2), "max": round(metrics.max_response_time_ms, 2),
                              "avg": round(metrics.avg_response_time_ms, 2), "median": round(metrics.median_response_time_ms, 2),
                              "p95": round(metrics.p95_response_time_ms, 2), "p99": round(metrics.p99_response_time_ms, 2)},
        "throughput": {"requests_per_second": round(metrics.requests_per_second, 2),
                       "kb_per_second": round(metrics.throughput_bytes_per_second / 1024, 2)},
        "status_codes": metrics.status_code_distribution, "errors": metrics.error_distribution
    }, indent=2)


def format_html_report(metrics: LoadTestMetrics, url: str, method: str, concurrent_users: int) -> str:
    """Generate HTML report"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    error_color = "#28a745" if metrics.error_rate_percent < 1 else ("#ffc107" if metrics.error_rate_percent < 5 else "#dc3545")
    p95_color = "#28a745" if metrics.p95_response_time_ms < 200 else ("#ffc107" if metrics.p95_response_time_ms < 500 else "#dc3545")
    status_rows = "".join(f"<tr><td>{code}</td><td>{count}</td><td>{(count / metrics.total_requests * 100):.1f}%</td></tr>"
                          for code, count in sorted(metrics.status_code_distribution.items()))
    error_section = ""
    if metrics.error_distribution:
        error_rows = "".join(f"<tr><td>{error}</td><td>{count}</td></tr>"
                             for error, count in sorted(metrics.error_distribution.items(), key=lambda x: -x[1])[:10])
        error_section = f'<div class="card"><h2>Error Distribution</h2><table><tr><th>Error</th><th>Count</th></tr>{error_rows}</table></div>'

    return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>API Load Test - {timestamp}</title>
<style>body{{font-family:-apple-system,sans-serif;background:#f5f5f5;padding:20px}}.container{{max-width:1200px;margin:0 auto}}
h1{{color:#2c3e50}}.timestamp{{color:#666;margin-bottom:30px}}.card{{background:white;border-radius:8px;padding:20px;margin-bottom:20px;box-shadow:0 2px 4px rgba(0,0,0,0.1)}}
.card h2{{color:#34495e;border-bottom:2px solid #3498db;padding-bottom:10px}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:20px}}
.metric{{text-align:center;padding:15px;background:#f8f9fa;border-radius:6px}}.metric-value{{font-size:2em;font-weight:bold;color:#2c3e50}}.metric-label{{color:#666;margin-top:5px}}
table{{width:100%;border-collapse:collapse}}th,td{{padding:12px;text-align:left;border-bottom:1px solid #ddd}}th{{background:#f8f9fa}}
.config-list{{list-style:none;padding:0}}.config-list li{{padding:8px 0;border-bottom:1px solid #eee}}.config-list strong{{display:inline-block;width:150px}}</style></head>
<body><div class="container"><h1>API Load Test Report</h1><p class="timestamp">Generated: {timestamp}</p>
<div class="card"><h2>Test Configuration</h2><ul class="config-list"><li><strong>URL:</strong> {url}</li><li><strong>Method:</strong> {method}</li>
<li><strong>Concurrent Users:</strong> {concurrent_users}</li><li><strong>Total Requests:</strong> {metrics.total_requests}</li>
<li><strong>Test Duration:</strong> {metrics.total_time_seconds:.2f}s</li></ul></div>
<div class="grid"><div class="card"><h2>Request Summary</h2><div class="grid">
<div class="metric"><div class="metric-value" style="color:#28a745">{metrics.successful_requests}</div><div class="metric-label">Successful</div></div>
<div class="metric"><div class="metric-value" style="color:#dc3545">{metrics.failed_requests}</div><div class="metric-label">Failed</div></div>
<div class="metric"><div class="metric-value" style="color:{error_color}">{metrics.error_rate_percent:.2f}%</div><div class="metric-label">Error Rate</div></div></div></div>
<div class="card"><h2>Throughput</h2><div class="grid">
<div class="metric"><div class="metric-value">{metrics.requests_per_second:.1f}</div><div class="metric-label">Requests/sec</div></div>
<div class="metric"><div class="metric-value">{metrics.throughput_bytes_per_second / 1024:.1f}</div><div class="metric-label">KB/sec</div></div></div></div></div>
<div class="card"><h2>Response Time (ms)</h2><table><tr><th>Metric</th><th>Value</th></tr>
<tr><td>Minimum</td><td>{metrics.min_response_time_ms:.2f}</td></tr><tr><td>Average</td><td>{metrics.avg_response_time_ms:.2f}</td></tr>
<tr><td>Median (P50)</td><td>{metrics.median_response_time_ms:.2f}</td></tr><tr><td>P95</td><td style="color:{p95_color}">{metrics.p95_response_time_ms:.2f}</td></tr>
<tr><td>P99</td><td>{metrics.p99_response_time_ms:.2f}</td></tr><tr><td>Maximum</td><td>{metrics.max_response_time_ms:.2f}</td></tr></table></div>
<div class="card"><h2>Status Code Distribution</h2><table><tr><th>Status</th><th>Count</th><th>Percentage</th></tr>{status_rows}</table></div>
{error_section}</div></body></html>"""


def main():
    parser = argparse.ArgumentParser(
        description="API Load Tester - HTTP load generation and performance benchmarking",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s http://localhost:3000/api/users
  %(prog)s http://localhost:3000/api/posts --users 50 --requests 500
  %(prog)s http://localhost:3000/api/users -u 100 -r 1000 --format json
  %(prog)s http://localhost:3000/api/users --method POST --data '{"name":"test"}'
  %(prog)s http://localhost:3000/api/posts --format html --save report.html

Performance Targets:
  - P95 latency < 200ms for typical endpoints
  - Error rate < 1%% under normal load
  - RPS > 1000 for health check endpoints
        """)

    parser.add_argument('url', nargs='?', help='Target URL to test')
    parser.add_argument('--users', '-u', type=int, default=10, dest='concurrent_users', help='Concurrent users (default: 10)')
    parser.add_argument('--requests', '-r', type=int, default=100, dest='total_requests', help='Total requests (default: 100)')
    parser.add_argument('--method', '-m', choices=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'], default='GET', help='HTTP method')
    parser.add_argument('--data', '-d', help='Request body (JSON string or @filename)')
    parser.add_argument('--headers', '-H', help='Custom headers (JSON string or @filename)')
    parser.add_argument('--timeout', '-t', type=int, default=30, help='Request timeout in seconds')
    parser.add_argument('--format', '-f', choices=['text', 'json', 'html'], default='text', help='Output format')
    parser.add_argument('--save', '-s', help='Save report to file')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show progress')
    parser.add_argument('--version', action='version', version='%(prog)s 1.0.0')

    args = parser.parse_args()

    if not args.url:
        parser.print_help()
        print("\nError: URL argument is required")
        sys.exit(1)

    headers = {}
    if args.headers:
        if args.headers.startswith('@'):
            with open(args.headers[1:], 'r') as f:
                headers = json.load(f)
        else:
            headers = json.loads(args.headers)

    payload = None
    if args.data:
        if args.data.startswith('@'):
            with open(args.data[1:], 'r') as f:
                payload = f.read()
        else:
            payload = args.data

    tester = APILoadTester(args.url, args.concurrent_users, args.total_requests, args.method, headers, payload, args.timeout, args.verbose)

    try:
        metrics = tester.run()
    except KeyboardInterrupt:
        print("\nTest interrupted")
        sys.exit(130)

    if args.format == 'json':
        output = format_json_output(metrics, args.url, args.method, args.concurrent_users)
    elif args.format == 'html':
        output = format_html_report(metrics, args.url, args.method, args.concurrent_users)
    else:
        output = format_text_report(metrics, args.url, args.method, args.concurrent_users)

    if args.save:
        with open(args.save, 'w') as f:
            f.write(output)
        print(f"Report saved to: {args.save}")
    else:
        print(output)

    if metrics.error_rate_percent > 50:
        sys.exit(2)


if __name__ == '__main__':
    main()
