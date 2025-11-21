#!/usr/bin/env python3
"""
Process Parser - Universal process documentation parser

Parses process documentation from multiple input formats (URLs, text files,
images, transcripts) and generates structured JSON output.

Usage:
    python process_parser.py --input FILE [--output FILE] [--format json] [--verbose]
    python process_parser.py --url URL [--output FILE]
    python process_parser.py --input sketch.png --type image [--output FILE]

Author: Claude Skills - Business Analyst Toolkit
Version: 1.0.0
License: MIT
"""

import argparse
import json
import re
import sys
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from html.parser import HTMLParser
import os

# Optional dependencies (graceful fallback)
try:
    from PIL import Image
    import pytesseract
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False

# Schema version
SCHEMA_VERSION = "1.0"


class HTMLTextExtractor(HTMLParser):
    """Extract text content from HTML"""

    def __init__(self):
        super().__init__()
        self.text = []
        self.skip_tags = {'script', 'style', 'head', 'meta', 'link'}
        self.current_tag = None

    def handle_starttag(self, tag, attrs):
        self.current_tag = tag

    def handle_data(self, data):
        if self.current_tag not in self.skip_tags:
            text = data.strip()
            if text:
                self.text.append(text)

    def get_text(self):
        return '\n'.join(self.text)


class ProcessParser:
    """Main process parser class"""

    def __init__(self, input_source: str, input_type: Optional[str] = None, verbose: bool = False):
        self.source = input_source
        self.type = input_type or self._detect_type()
        self.verbose = verbose
        self.process_id = str(uuid.uuid4())[:8]

    def _detect_type(self) -> str:
        """Auto-detect input type from source"""
        if self.source.startswith(('http://', 'https://')):
            return 'url'
        elif os.path.isfile(self.source):
            ext = os.path.splitext(self.source)[1].lower()
            if ext in ['.png', '.jpg', '.jpeg', '.gif', '.bmp']:
                return 'image'
            elif ext in ['.txt', '.md', '.markdown']:
                return 'text'
            else:
                return 'text'  # Default to text
        elif os.path.isdir(self.source):
            return 'directory'
        else:
            return 'text'

    def parse(self) -> Dict:
        """Parse input and return structured process JSON"""
        if self.verbose:
            print(f"📄 Parsing {self.type}: {self.source}")

        # Route to appropriate handler
        if self.type == 'url':
            content = self._parse_url()
        elif self.type == 'image':
            content = self._parse_image()
        elif self.type == 'text':
            content = self._parse_text()
        elif self.type == 'transcript':
            content = self._parse_transcript()
        elif self.type == 'directory':
            content = self._parse_directory()
        else:
            raise ValueError(f"Unsupported input type: {self.type}")

        if not content:
            raise ValueError("No content could be extracted from input")

        # Extract process structure from text content
        process = self._extract_process(content)

        # Add metadata
        process['schema_version'] = SCHEMA_VERSION
        process['process_id'] = self.process_id
        process['source'] = {
            'type': self.type,
            'location': self.source,
            'parsed_at': datetime.utcnow().isoformat() + 'Z'
        }
        process['metadata'] = {
            'created_at': datetime.utcnow().isoformat() + 'Z',
            'version': '1.0',
            'tags': []
        }

        # Calculate overall confidence
        if process['steps']:
            avg_confidence = sum(s.get('confidence', 0.5) for s in process['steps']) / len(process['steps'])
            process['confidence_score'] = round(avg_confidence, 2)
        else:
            process['confidence_score'] = 0.0

        if self.verbose:
            self._print_summary(process)

        return process

    def _parse_url(self) -> str:
        """Fetch and parse URL content"""
        try:
            # Add user agent to avoid 403 errors
            headers = {'User-Agent': 'Mozilla/5.0 (process-parser/1.0)'}
            req = Request(self.source, headers=headers)

            with urlopen(req, timeout=10) as response:
                html = response.read().decode('utf-8', errors='ignore')

            # Extract text from HTML
            parser = HTMLTextExtractor()
            parser.feed(html)
            text = parser.get_text()

            if self.verbose:
                print(f"✅ Fetched {len(text)} characters from URL")

            return text

        except HTTPError as e:
            raise ValueError(f"HTTP error {e.code}: {e.reason}")
        except URLError as e:
            raise ValueError(f"URL error: {e.reason}")
        except Exception as e:
            raise ValueError(f"Failed to fetch URL: {str(e)}")

    def _parse_image(self) -> str:
        """Parse image using OCR"""
        if not OCR_AVAILABLE:
            print("⚠️  OCR not available (pip install pytesseract Pillow)")
            print("📝 Please extract text manually and save as .txt file")
            return None

        try:
            image = Image.open(self.source)
            text = pytesseract.image_to_string(image)

            if self.verbose:
                print(f"✅ Extracted {len(text)} characters via OCR")

            return text

        except Exception as e:
            print(f"❌ OCR failed: {e}")
            print("📝 Please extract text manually")
            return None

    def _parse_text(self) -> str:
        """Read text file"""
        try:
            with open(self.source, 'r', encoding='utf-8') as f:
                text = f.read()

            if self.verbose:
                print(f"✅ Read {len(text)} characters from file")

            return text

        except FileNotFoundError:
            raise ValueError(f"File not found: {self.source}")
        except Exception as e:
            raise ValueError(f"Failed to read file: {str(e)}")

    def _parse_transcript(self) -> str:
        """Parse conversation transcript"""
        # For now, treat like text file
        # In future, could add speaker detection, turn-taking analysis
        return self._parse_text()

    def _parse_directory(self) -> str:
        """Parse multiple files in directory"""
        texts = []
        for filename in os.listdir(self.source):
            filepath = os.path.join(self.source, filename)
            if os.path.isfile(filepath):
                ext = os.path.splitext(filename)[1].lower()
                if ext in ['.txt', '.md', '.markdown']:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        texts.append(f.read())

        if self.verbose:
            print(f"✅ Read {len(texts)} files from directory")

        return '\n\n'.join(texts)

    def _extract_process(self, content: str) -> Dict:
        """Extract process structure from text content"""
        process = {
            'process_name': self._extract_process_name(content),
            'process_description': self._extract_description(content),
            'process_owner': self._extract_owner(content),
            'steps': [],
            'roles': [],
            'gaps': []
        }

        # Extract steps
        steps = self._extract_steps(content)
        process['steps'] = steps

        # Extract unique roles
        roles = set()
        for step in steps:
            if step.get('role'):
                roles.add(step['role'])
        process['roles'] = sorted(list(roles))

        # Identify basic gaps
        gaps = self._identify_gaps(process)
        process['gaps'] = gaps

        return process

    def _extract_process_name(self, content: str) -> str:
        """Extract process name from content"""
        # Try various patterns
        patterns = [
            r'(?:^|\n)#\s+(.+?)(?:\n|$)',  # Markdown H1
            r'(?:^|\n)Process:\s*(.+?)(?:\n|$)',  # "Process: Name"
            r'(?:^|\n)Title:\s*(.+?)(?:\n|$)',  # "Title: Name"
            r'(?:^|\n)(.+?)\s+Process(?:\n|$)',  # "Name Process"
        ]

        for pattern in patterns:
            match = re.search(pattern, content, re.IGNORECASE | re.MULTILINE)
            if match:
                return match.group(1).strip()

        # Default: use first line or "Untitled Process"
        first_line = content.split('\n')[0].strip()
        if first_line and len(first_line) < 100:
            return first_line

        return "Untitled Process"

    def _extract_description(self, content: str) -> str:
        """Extract process description"""
        # Look for description section
        patterns = [
            r'Description:\s*(.+?)(?:\n\n|\n#|\Z)',
            r'Overview:\s*(.+?)(?:\n\n|\n#|\Z)',
            r'Summary:\s*(.+?)(?:\n\n|\n#|\Z)',
        ]

        for pattern in patterns:
            match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
            if match:
                desc = match.group(1).strip()
                # Limit to 500 chars
                return desc[:500] + ('...' if len(desc) > 500 else '')

        return ""

    def _extract_owner(self, content: str) -> str:
        """Extract process owner"""
        patterns = [
            r'Owner:\s*(.+?)(?:\n|$)',
            r'Process Owner:\s*(.+?)(?:\n|$)',
            r'Responsible:\s*(.+?)(?:\n|$)',
        ]

        for pattern in patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return match.group(1).strip()

        return ""

    def _extract_steps(self, content: str) -> List[Dict]:
        """Extract process steps from content"""
        steps = []
        step_counter = 1

        # Pattern 1: Numbered lists (most common)
        # Example: "1. Step name (30 min) - Role"
        numbered_pattern = r'(?:^|\n)\s*(\d+)[\.\)]\s*(.+?)(?=\n\s*\d+[\.\)]|\n\n|\Z)'
        matches = re.finditer(numbered_pattern, content, re.MULTILINE | re.DOTALL)

        for match in matches:
            step_num = match.group(1)
            step_text = match.group(2).strip()
            step = self._parse_step_text(step_text, step_counter)
            steps.append(step)
            step_counter += 1

        # Pattern 2: Bullet lists
        if not steps:
            bullet_pattern = r'(?:^|\n)\s*[-*•]\s*(.+?)(?=\n\s*[-*•]|\n\n|\Z)'
            matches = re.finditer(bullet_pattern, content, re.MULTILINE | re.DOTALL)

            for match in matches:
                step_text = match.group(1).strip()
                step = self._parse_step_text(step_text, step_counter)
                steps.append(step)
                step_counter += 1

        # Pattern 3: "Step X:" format
        if not steps:
            step_pattern = r'(?:^|\n)Step\s+(\d+|[A-Z]):\s*(.+?)(?=\n(?:Step\s+\d+|\n)|\Z)'
            matches = re.finditer(step_pattern, content, re.IGNORECASE | re.MULTILINE | re.DOTALL)

            for match in matches:
                step_text = match.group(2).strip()
                step = self._parse_step_text(step_text, step_counter)
                steps.append(step)
                step_counter += 1

        # If still no steps found, try sentence-based extraction
        if not steps:
            sentences = re.split(r'[.!?]\s+', content)
            for sentence in sentences[:20]:  # Limit to first 20 sentences
                if len(sentence) > 10 and self._looks_like_step(sentence):
                    step = self._parse_step_text(sentence, step_counter)
                    steps.append(step)
                    step_counter += 1

        return steps

    def _looks_like_step(self, text: str) -> bool:
        """Check if text looks like a process step"""
        # Action verbs that indicate steps
        action_verbs = [
            'create', 'submit', 'review', 'approve', 'send', 'receive',
            'analyze', 'prepare', 'complete', 'verify', 'validate', 'check',
            'process', 'update', 'generate', 'assign', 'notify', 'document'
        ]

        text_lower = text.lower()
        return any(verb in text_lower for verb in action_verbs)

    def _parse_step_text(self, text: str, sequence: int) -> Dict:
        """Parse individual step text to extract metadata"""
        step = {
            'id': f"step_{sequence:03d}",
            'name': text.split('\n')[0].strip()[:100],  # First line, max 100 chars
            'description': text.strip(),
            'sequence': sequence,
            'confidence': 0.8  # Default confidence
        }

        # Extract role (in parentheses or after dash)
        role_patterns = [
            r'\(([^)]+?)\)',  # (Role Name)
            r'-\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*$',  # - Role Name
            r'by\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',  # by Role Name
        ]
        for pattern in role_patterns:
            match = re.search(pattern, text)
            if match:
                role = match.group(1).strip()
                if not role.isdigit() and len(role) < 50:  # Not a number, reasonable length
                    step['role'] = role
                    break

        # Extract duration (in minutes, hours, days)
        duration_patterns = [
            r'(\d+)\s*(?:min|minute)s?',
            r'(\d+)\s*(?:hr|hour)s?',
            r'(\d+)\s*(?:day)s?',
        ]
        for i, pattern in enumerate(duration_patterns):
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                value = int(match.group(1))
                if i == 0:  # minutes
                    step['duration_minutes'] = value
                elif i == 1:  # hours
                    step['duration_minutes'] = value * 60
                elif i == 2:  # days
                    step['duration_minutes'] = value * 60 * 24
                break

        # Extract effort (person-hours)
        effort_patterns = [
            r'(\d+(?:\.\d+)?)\s*person-?hours?',
            r'(\d+(?:\.\d+)?)\s*hrs?\s+effort',
        ]
        for pattern in effort_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                step['effort_hours'] = float(match.group(1))
                break

        # Extract inputs/outputs
        if 'input:' in text.lower():
            inputs_match = re.search(r'input:\s*(.+?)(?:\n|output:|$)', text, re.IGNORECASE)
            if inputs_match:
                inputs = [i.strip() for i in inputs_match.group(1).split(',')]
                step['inputs'] = inputs

        if 'output:' in text.lower():
            outputs_match = re.search(r'output:\s*(.+?)(?:\n|$)', text, re.IGNORECASE)
            if outputs_match:
                outputs = [o.strip() for o in outputs_match.group(1).split(',')]
                step['outputs'] = outputs

        # Extract decisions
        if '?' in text or 'if' in text.lower() or 'decide' in text.lower():
            step['decisions'] = [{'question': text[:200], 'criteria': '', 'options': []}]

        # Adjust confidence based on extracted info
        info_count = sum([
            'role' in step,
            'duration_minutes' in step,
            'effort_hours' in step,
            'inputs' in step,
            'outputs' in step
        ])
        step['confidence'] = min(0.5 + (info_count * 0.1), 1.0)

        return step

    def _identify_gaps(self, process: Dict) -> List[Dict]:
        """Identify basic gaps in process definition"""
        gaps = []

        # Check process-level gaps
        if not process.get('process_owner'):
            gaps.append({
                'type': 'missing_info',
                'severity': 'high',
                'description': 'No process owner identified',
                'impact': 'Unclear accountability and governance'
            })

        if not process.get('process_description'):
            gaps.append({
                'type': 'missing_info',
                'severity': 'medium',
                'description': 'No process description provided',
                'impact': 'Context and purpose unclear'
            })

        # Check step-level gaps
        for step in process['steps']:
            step_id = step['id']
            step_name = step['name']

            if not step.get('role'):
                gaps.append({
                    'type': 'undefined_role',
                    'severity': 'high',
                    'step_id': step_id,
                    'description': f"Step '{step_name}' has no assigned role",
                    'impact': 'Unclear accountability'
                })

            if not step.get('duration_minutes'):
                gaps.append({
                    'type': 'missing_info',
                    'severity': 'medium',
                    'step_id': step_id,
                    'description': f"Step '{step_name}' has no duration estimate",
                    'impact': 'Cannot calculate cycle time'
                })

            if step.get('decisions') and not step['decisions'][0].get('criteria'):
                gaps.append({
                    'type': 'missing_decision',
                    'severity': 'high',
                    'step_id': step_id,
                    'description': f"Step '{step_name}' has decision without criteria",
                    'impact': 'Inconsistent decision-making'
                })

        return gaps

    def _print_summary(self, process: Dict):
        """Print process parsing summary"""
        print(f"\n✅ Parsed process: {process['process_name']}")
        print(f"📊 Extracted {len(process['steps'])} steps, {len(process['roles'])} roles")

        if process['gaps']:
            critical = sum(1 for g in process['gaps'] if g['severity'] == 'critical')
            high = sum(1 for g in process['gaps'] if g['severity'] == 'high')
            medium = sum(1 for g in process['gaps'] if g['severity'] == 'medium')

            print(f"⚠️  {len(process['gaps'])} gaps identified", end='')
            if critical:
                print(f" ({critical} critical", end='')
            if high:
                print(f", {high} high" if critical else f" ({high} high", end='')
            if medium:
                print(f", {medium} medium)", end='')
            print(")")
        else:
            print("✨ No major gaps identified")

        print(f"💯 Confidence score: {process['confidence_score']:.0%}")


def main():
    parser = argparse.ArgumentParser(
        description='Process Parser - Universal process documentation parser',
        epilog='Examples:\n'
               '  python process_parser.py --input process.md --output process.json\n'
               '  python process_parser.py --url "https://company.com/process"\n'
               '  python process_parser.py --input sketch.png --type image\n',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('--input', type=str, help='Input file or directory path')
    input_group.add_argument('--url', type=str, help='URL to process documentation')

    parser.add_argument('--type', type=str, choices=['url', 'text', 'image', 'transcript', 'directory'],
                        help='Input type (auto-detected if not specified)')
    parser.add_argument('--output', type=str, help='Output JSON file path (default: stdout)')
    parser.add_argument('--format', type=str, default='json', choices=['json', 'yaml'],
                        help='Output format (default: json)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')

    args = parser.parse_args()

    try:
        # Parse input
        source = args.url if args.url else args.input
        process_parser = ProcessParser(source, args.type, args.verbose)
        process = process_parser.parse()

        # Format output
        if args.format == 'json':
            output = json.dumps(process, indent=2, ensure_ascii=False)
        elif args.format == 'yaml':
            # Simple YAML output (no external dependency)
            output = json.dumps(process, indent=2)
            print("⚠️  YAML output requires PyYAML (pip install pyyaml)")
            print("📝 Outputting JSON instead")
        else:
            output = json.dumps(process, indent=2, ensure_ascii=False)

        # Write output
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"💾 Saved to: {args.output}")
        else:
            print(output)

        sys.exit(0)

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
