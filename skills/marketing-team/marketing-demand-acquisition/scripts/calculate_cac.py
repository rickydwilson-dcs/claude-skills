#!/usr/bin/env python3
"""
CAC (Customer Acquisition Cost) Calculator

Calculate blended and channel-specific CAC for marketing campaigns.
Supports multiple time periods and channel breakdowns.
"""

import csv
import json
import logging
import sys
from io import StringIO
from typing import Dict, List

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def calculate_cac(total_spend: float, customers_acquired: int) -> float:
    """Calculate basic CAC"""
    logger.debug(f"Calculating CAC: spend=${total_spend}, customers={customers_acquired}")

    if customers_acquired == 0:
        logger.warning("No customers acquired - CAC calculation returns 0")
        return 0.0
    return round(total_spend / customers_acquired, 2)

def calculate_channel_cac(channel_data: List[Dict]) -> Dict:
    """
    Calculate CAC per channel

    Args:
        channel_data: List of dicts with 'channel', 'spend', 'customers' keys

    Returns:
        Dict with channel CAC breakdown and blended CAC
    """
    logger.debug(f"Calculating CAC for {len(channel_data)} channels")

    if not channel_data:
        logger.warning("No channel data provided")
        return {}

    results = {}
    total_spend = 0
    total_customers = 0
    
    for channel in channel_data:
        name = channel['channel']
        spend = channel['spend']
        customers = channel['customers']
        
        cac = calculate_cac(spend, customers)
        results[name] = {
            'spend': spend,
            'customers': customers,
            'cac': cac
        }
        
        total_spend += spend
        total_customers += customers
    
    results['blended'] = {
        'total_spend': total_spend,
        'total_customers': total_customers,
        'blended_cac': calculate_cac(total_spend, total_customers)
    }
    
    return results

def format_text_output(results: Dict, show_benchmarks: bool = False) -> str:
    """Format CAC results as text"""
    output = []
    output.append("=" * 60)
    output.append("CAC CALCULATION RESULTS")
    output.append("=" * 60)
    output.append("")

    for channel, data in results.items():
        if channel == 'blended':
            output.append("-" * 60)
            output.append("BLENDED CAC")
            output.append(f"  Total Spend: ${data['total_spend']:,.2f}")
            output.append(f"  Total Customers: {data['total_customers']:,}")
            output.append(f"  Blended CAC: ${data['blended_cac']:,.2f}")
        else:
            output.append(f"{channel.upper()}")
            output.append(f"  Spend: ${data['spend']:,.2f}")
            output.append(f"  Customers: {data['customers']:,}")
            output.append(f"  CAC: ${data['cac']:,.2f}")
            output.append("")

    if show_benchmarks:
        output.append("")
        output.append("=" * 60)
        output.append("B2B SAAS BENCHMARKS (Series A)")
        output.append("=" * 60)
        output.append("LinkedIn Ads:   $150-$400")
        output.append("Google Search:  $80-$250")
        output.append("SEO/Organic:    $50-$150")
        output.append("Partnerships:   $100-$300")
        output.append("Blended Target: <$300")

    return '\n'.join(output)

def format_csv_output(results: Dict) -> str:
    """Format CAC results as CSV"""
    output = StringIO()
    writer = csv.writer(output)

    # Header row
    writer.writerow(['channel', 'spend', 'customers', 'cac', 'benchmark_min', 'benchmark_max', 'status'])

    # Benchmark data
    benchmarks = {
        'LinkedIn Ads': {'min': 150, 'max': 400},
        'Google Search': {'min': 80, 'max': 250},
        'SEO/Organic': {'min': 50, 'max': 150},
        'Partnerships': {'min': 100, 'max': 300},
    }

    # Write channel data
    for channel, data in results.items():
        if channel == 'blended':
            continue
        spend = data.get('spend', 0)
        customers = data.get('customers', 0)
        cac = data.get('cac', 0)
        benchmark = benchmarks.get(channel, {'min': 0, 'max': 999999})
        status = 'good' if benchmark['min'] <= cac <= benchmark['max'] else 'review'
        writer.writerow([channel, spend, customers, cac, benchmark['min'], benchmark['max'], status])

    # Blended CAC row
    if 'blended' in results:
        blended = results['blended']
        writer.writerow(['BLENDED', blended.get('total_spend', 0), blended.get('total_customers', 0),
                        blended.get('blended_cac', 0), '<', '300', 'pass'])

    return output.getvalue()

def format_json_output(results: Dict) -> str:
    """Format CAC results as JSON"""
    output = {
        "metadata": {
            "tool": "calculate_cac.py",
            "version": "1.0.0"
        },
        "results": results,
        "benchmarks": {
            "linkedin_ads": {"min": 150, "max": 400},
            "google_search": {"min": 80, "max": 250},
            "seo_organic": {"min": 50, "max": 150},
            "partnerships": {"min": 100, "max": 300},
            "blended_target": {"max": 300}
        }
    }
    return json.dumps(output, indent=2)

def load_channel_data_from_json(file_path: str) -> List[Dict]:
    """Load channel data from JSON file"""
    logger.debug(f"Loading channel data from: {file_path}")

    import json
    from pathlib import Path

    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except FileNotFoundError as e:
        logger.error(f"File not found: {file_path}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in file: {file_path}")
        raise

    # Support both array format and object format
    if isinstance(data, list):
        logger.debug(f"Loaded {len(data)} channels from array format")
        return data
    elif isinstance(data, dict) and 'channels' in data:
        logger.debug(f"Loaded {len(data['channels'])} channels from object format")
        return data['channels']
    else:
        logger.error("JSON file has invalid format")
        raise ValueError("JSON file must contain an array of channel data or an object with 'channels' key")

def main():
    import argparse
    from pathlib import Path

    parser = argparse.ArgumentParser(
        description='Calculate Customer Acquisition Cost (CAC) for marketing channels',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Calculate from JSON file
  %(prog)s channel-data.json

  # With JSON output
  %(prog)s channel-data.json --output json

  # Save to file with benchmarks
  %(prog)s channel-data.json --benchmarks --file results.txt

  # Use example data
  %(prog)s --example

JSON Input Format:
  [
    {"channel": "LinkedIn Ads", "spend": 15000, "customers": 10},
    {"channel": "Google Search", "spend": 12000, "customers": 20}
  ]

Or:
  {
    "channels": [
      {"channel": "LinkedIn Ads", "spend": 15000, "customers": 10}
    ]
  }

For more information, see the skill documentation.
        """
    )

    # Positional arguments
    parser.add_argument(
        'input',
        nargs='?',
        help='JSON file with channel data (or use --example)'
    )

    # Optional arguments
    parser.add_argument(
        '--example',
        action='store_true',
        help='Run with example data (no input file needed)'
    )

    parser.add_argument(
        '--benchmarks', '-b',
        action='store_true',
        help='Include B2B SaaS benchmark data in output'
    )

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
        version='%(prog)s 1.0.0'
    )

    args = parser.parse_args()

    # Set logging level based on verbose flag
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Verbose logging enabled")

    try:
        # Get channel data
        if args.example:
            logger.info("Using example channel data")

            channel_data = [
                {'channel': 'LinkedIn Ads', 'spend': 15000, 'customers': 10},
                {'channel': 'Google Search', 'spend': 12000, 'customers': 20},
                {'channel': 'SEO/Organic', 'spend': 5000, 'customers': 15},
                {'channel': 'Partnerships', 'spend': 3000, 'customers': 5},
            ]
        elif args.input:
            # Validate input file
            input_path = Path(args.input)

            if not input_path.exists():
                print(f"Error: Input file not found: {args.input}", file=sys.stderr)
                sys.exit(1)

            if not input_path.is_file():
                logger.error(f"Path is not a file: {args.input}")
                print(f"Error: Path is not a file: {args.input}", file=sys.stderr)
                sys.exit(1)

            logger.info(f"Reading channel data from: {args.input}")

            try:
                channel_data = load_channel_data_from_json(str(input_path))
            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON file: {e}")
                print(f"Error: Invalid JSON file: {e}", file=sys.stderr)
                sys.exit(3)
            except ValueError as e:
                logger.error(f"Invalid data format: {e}")
                print(f"Error: {e}", file=sys.stderr)
                sys.exit(3)
        else:
            logger.error("No input file or --example flag provided")
            print("Error: Either provide an input file or use --example", file=sys.stderr)
            print("Run with --help for usage information", file=sys.stderr)
            sys.exit(2)

        logger.info(f"Processing {len(channel_data)} channels")

        # Calculate CAC
        results = calculate_channel_cac(channel_data)

        # Format output
        if args.output == 'csv':
            output = format_csv_output(results)
        elif args.output == 'json':
            output = format_json_output(results)
        else:
            output = format_text_output(results, show_benchmarks=args.benchmarks)

        # Write output
        if args.file:
            try:
                output_path = Path(args.file)
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(output)

                logger.info(f"Results written to: {args.file}")
                if not args.verbose:
                    print(f"Output saved to: {args.file}")

            except PermissionError as e:
                logger.error(f"Permission denied writing to: {args.file}")
                print(f"Error: Permission denied writing to: {args.file}", file=sys.stderr)
                sys.exit(4)
            except Exception as e:
                logger.error(f"Error writing output file: {e}")
                print(f"Error writing output file: {e}", file=sys.stderr)
                sys.exit(4)
        else:
            print(output)

        sys.exit(0)

    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        print(f"Error: File not found: {e}", file=sys.stderr)
        sys.exit(1)

    except PermissionError as e:
        logger.error(f"Permission denied: {e}")
        print(f"Error: Permission denied: {e}", file=sys.stderr)
        sys.exit(1)

    except KeyboardInterrupt:
        logger.warning("Operation cancelled by user")
        print("\nOperation cancelled by user", file=sys.stderr)
        sys.exit(130)

    except Exception as e:
        logger.error(f"Unexpected error occurred: {e}")
        print(f"Error: Unexpected error occurred: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
