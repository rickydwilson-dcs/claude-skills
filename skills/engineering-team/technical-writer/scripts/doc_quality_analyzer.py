#!/usr/bin/env python3
"""
Documentation Quality Analyzer - Analyzes markdown documentation for quality, completeness, and readability
"""

import re
import json
import os
from typing import Dict, List, Tuple
from pathlib import Path


class DocumentQualityAnalyzer:
    def __init__(self):
        """Initialize the documentation quality analyzer"""

        # Required sections for complete documentation
        self.required_sections = {'overview', 'installation', 'usage'}

        # Readability thresholds
        self.readability_targets = {
            'flesch_reading_ease': (60, 80),  # Easy to fairly easy
            'flesch_kincaid_grade': (6, 10),  # 6th-10th grade level
            'gunning_fog': (8, 12),  # High school level
            'avg_sentence_length': (15, 25)  # Optimal range
        }

        # Common placeholder patterns
        self.placeholder_patterns = [
            r'\[TODO\]',
            r'\[TBD\]',
            r'\[FIXME\]',
            r'placeholder',
            r'lorem ipsum',
            r'coming soon',
            r'\[insert.*?\]',
            r'\{.*?\}',
            r'xxx+',
        ]

    def analyze_file(self, file_path: str, checks: List[str] = None) -> Dict:
        """Analyze a single markdown file for quality"""

        if checks is None:
            checks = ['structure', 'links', 'completeness', 'readability']

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            return {
                'file': file_path,
                'error': 'Unable to read file as UTF-8 text'
            }
        except FileNotFoundError:
            return {
                'file': file_path,
                'error': 'File not found'
            }

        analysis = {
            'file': file_path,
            'overall_score': 0,
            'breakdown': {},
            'issues': [],
            'recommendations': []
        }

        # Perform requested checks
        if 'structure' in checks:
            structure_score, structure_issues = self._check_structure(content)
            analysis['breakdown']['structure'] = structure_score
            analysis['issues'].extend(structure_issues)

        if 'readability' in checks:
            readability_score, readability_metrics, readability_issues = self._check_readability(content)
            analysis['breakdown']['readability'] = readability_score
            analysis['readability_metrics'] = readability_metrics
            analysis['issues'].extend(readability_issues)

        if 'completeness' in checks:
            completeness_score, completeness_issues = self._check_completeness(content)
            analysis['breakdown']['completeness'] = completeness_score
            analysis['issues'].extend(completeness_issues)

        if 'links' in checks:
            links_score, links_issues = self._check_links(content, file_path)
            analysis['breakdown']['links'] = links_score
            analysis['issues'].extend(links_issues)

        # Calculate overall score
        if analysis['breakdown']:
            analysis['overall_score'] = round(
                sum(analysis['breakdown'].values()) / len(analysis['breakdown'])
            )

        # Generate recommendations
        analysis['recommendations'] = self._generate_recommendations(analysis)

        return analysis

    def analyze_directory(self, directory: str, checks: List[str] = None) -> List[Dict]:
        """Analyze all markdown files in a directory"""

        results = []
        dir_path = Path(directory)

        if not dir_path.exists():
            return [{'error': f'Directory not found: {directory}'}]

        if not dir_path.is_dir():
            return [{'error': f'Not a directory: {directory}'}]

        # Find all markdown files recursively
        md_files = list(dir_path.rglob('*.md'))

        if not md_files:
            return [{'error': f'No markdown files found in: {directory}'}]

        for md_file in md_files:
            result = self.analyze_file(str(md_file), checks)
            results.append(result)

        return results

    def _check_structure(self, content: str) -> Tuple[int, List[Dict]]:
        """Check document structure and heading hierarchy"""

        score = 100
        issues = []
        lines = content.split('\n')

        # Extract headings
        headings = []
        for line_num, line in enumerate(lines, 1):
            if line.strip().startswith('#'):
                level = len(line) - len(line.lstrip('#'))
                text = line.lstrip('#').strip()
                headings.append({
                    'level': level,
                    'text': text,
                    'line': line_num
                })

        # Check for at least one H1
        h1_count = sum(1 for h in headings if h['level'] == 1)
        if h1_count == 0:
            score -= 20
            issues.append({
                'type': 'structure',
                'severity': 'high',
                'line': 1,
                'message': 'Missing H1 heading (document title)'
            })
        elif h1_count > 1:
            score -= 10
            issues.append({
                'type': 'structure',
                'severity': 'medium',
                'line': headings[1]['line'] if len(headings) > 1 else 1,
                'message': f'Multiple H1 headings found ({h1_count}). Use only one H1 for document title.'
            })

        # Check heading hierarchy (no skipping levels)
        prev_level = 0
        for heading in headings:
            if heading['level'] > prev_level + 1 and prev_level > 0:
                score -= 5
                issues.append({
                    'type': 'structure',
                    'severity': 'medium',
                    'line': heading['line'],
                    'message': f'Heading hierarchy skip: H{prev_level} to H{heading["level"]} (use H{prev_level + 1})'
                })
            prev_level = heading['level']

        # Check for required sections
        section_names = {h['text'].lower() for h in headings}
        missing_sections = self.required_sections - section_names

        for section in missing_sections:
            score -= 15
            issues.append({
                'type': 'structure',
                'severity': 'high',
                'line': None,
                'message': f'Missing required section: "{section.title()}"'
            })

        # Check for empty sections (heading followed immediately by another heading)
        for i in range(len(headings) - 1):
            current_heading = headings[i]
            next_heading = headings[i + 1]

            # Check if there's substantial content between headings
            content_between = '\n'.join(lines[current_heading['line']:next_heading['line'] - 1])
            content_between = content_between.strip().lstrip('#').strip()

            if len(content_between.split()) < 10:
                score -= 5
                issues.append({
                    'type': 'structure',
                    'severity': 'medium',
                    'line': current_heading['line'],
                    'message': f'Section "{current_heading["text"]}" appears empty or has minimal content'
                })

        return max(0, score), issues

    def _check_readability(self, content: str) -> Tuple[int, Dict, List[Dict]]:
        """Analyze readability using multiple metrics"""

        score = 100
        issues = []

        # Remove markdown formatting for text analysis
        text = self._strip_markdown(content)

        # Split into sentences
        sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]

        # Split into words
        words = text.split()

        if not sentences or not words:
            return 0, {}, [{
                'type': 'readability',
                'severity': 'high',
                'line': None,
                'message': 'Document has insufficient content for readability analysis'
            }]

        # Calculate basic metrics
        num_sentences = len(sentences)
        num_words = len(words)
        num_syllables = sum(self._count_syllables(word) for word in words)

        avg_sentence_length = num_words / num_sentences
        avg_syllables_per_word = num_syllables / num_words

        # Flesch Reading Ease (0-100, higher is easier)
        flesch_reading_ease = 206.835 - 1.015 * avg_sentence_length - 84.6 * avg_syllables_per_word
        flesch_reading_ease = max(0, min(100, flesch_reading_ease))

        # Flesch-Kincaid Grade Level
        flesch_kincaid_grade = 0.39 * avg_sentence_length + 11.8 * avg_syllables_per_word - 15.59
        flesch_kincaid_grade = max(0, flesch_kincaid_grade)

        # Gunning Fog Index
        complex_words = sum(1 for word in words if self._count_syllables(word) >= 3)
        gunning_fog = 0.4 * (avg_sentence_length + 100 * (complex_words / num_words))

        metrics = {
            'flesch_reading_ease': round(flesch_reading_ease, 1),
            'flesch_kincaid_grade': round(flesch_kincaid_grade, 1),
            'gunning_fog': round(gunning_fog, 1),
            'avg_sentence_length': round(avg_sentence_length, 1),
            'num_sentences': num_sentences,
            'num_words': num_words,
            'num_syllables': num_syllables
        }

        # Score readability metrics
        if not (self.readability_targets['flesch_reading_ease'][0] <= flesch_reading_ease <= self.readability_targets['flesch_reading_ease'][1]):
            score -= 15
            if flesch_reading_ease < 50:
                issues.append({
                    'type': 'readability',
                    'severity': 'medium',
                    'line': None,
                    'message': f'Text is difficult to read (Flesch: {flesch_reading_ease:.1f}). Target: 60-80. Simplify sentences and vocabulary.'
                })
            elif flesch_reading_ease > 90:
                issues.append({
                    'type': 'readability',
                    'severity': 'low',
                    'line': None,
                    'message': f'Text may be too simple (Flesch: {flesch_reading_ease:.1f}). Consider adding more technical detail.'
                })

        if flesch_kincaid_grade > self.readability_targets['flesch_kincaid_grade'][1]:
            score -= 10
            issues.append({
                'type': 'readability',
                'severity': 'medium',
                'line': None,
                'message': f'Text requires grade {flesch_kincaid_grade:.1f} reading level. Target: 6-10. Simplify language.'
            })

        if gunning_fog > self.readability_targets['gunning_fog'][1]:
            score -= 10
            issues.append({
                'type': 'readability',
                'severity': 'medium',
                'line': None,
                'message': f'High complexity (Gunning Fog: {gunning_fog:.1f}). Reduce complex words and sentence length.'
            })

        if avg_sentence_length > self.readability_targets['avg_sentence_length'][1]:
            score -= 10
            issues.append({
                'type': 'readability',
                'severity': 'medium',
                'line': None,
                'message': f'Sentences too long (avg: {avg_sentence_length:.1f} words). Target: 15-25 words. Break into shorter sentences.'
            })

        # Check for very long sentences
        for i, sentence in enumerate(sentences, 1):
            sentence_words = len(sentence.split())
            if sentence_words > 40:
                score -= 5
                issues.append({
                    'type': 'readability',
                    'severity': 'low',
                    'line': None,
                    'message': f'Very long sentence ({sentence_words} words). Consider breaking into multiple sentences.'
                })

        return max(0, score), metrics, issues

    def _check_completeness(self, content: str) -> Tuple[int, List[Dict]]:
        """Check for completeness and placeholders"""

        score = 100
        issues = []
        lines = content.split('\n')

        # Check for TODOs and placeholders
        for line_num, line in enumerate(lines, 1):
            for pattern in self.placeholder_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    score -= 5
                    issues.append({
                        'type': 'completeness',
                        'severity': 'medium',
                        'line': line_num,
                        'message': f'Placeholder or TODO found: "{line.strip()[:50]}..."'
                    })
                    break

        # Check for code blocks without language specification
        code_blocks = re.findall(r'^```(\w*)\n', content, re.MULTILINE)
        unspecified_blocks = sum(1 for lang in code_blocks if not lang)

        if unspecified_blocks > 0:
            score -= 10
            issues.append({
                'type': 'completeness',
                'severity': 'medium',
                'line': None,
                'message': f'{unspecified_blocks} code block(s) missing language specification. Add language for syntax highlighting.'
            })

        # Check for broken images (no alt text)
        images = re.findall(r'!\[(.*?)\]\((.*?)\)', content)
        for img_num, (alt_text, img_path) in enumerate(images, 1):
            if not alt_text.strip():
                score -= 5
                issues.append({
                    'type': 'completeness',
                    'severity': 'medium',
                    'line': None,
                    'message': f'Image {img_num} missing alt text: {img_path}'
                })

        # Check for empty links
        links = re.findall(r'\[(.*?)\]\((.*?)\)', content)
        for link_num, (link_text, url) in enumerate(links, 1):
            if not link_text.strip():
                score -= 5
                issues.append({
                    'type': 'completeness',
                    'severity': 'high',
                    'line': None,
                    'message': f'Link {link_num} has empty text: {url}'
                })
            if not url.strip():
                score -= 10
                issues.append({
                    'type': 'completeness',
                    'severity': 'high',
                    'line': None,
                    'message': f'Link has empty URL: [{link_text}]()'
                })

        # Check for minimum content length
        word_count = len(content.split())
        if word_count < 100:
            score -= 20
            issues.append({
                'type': 'completeness',
                'severity': 'high',
                'line': None,
                'message': f'Document is very short ({word_count} words). Add more detailed content.'
            })
        elif word_count < 300:
            score -= 10
            issues.append({
                'type': 'completeness',
                'severity': 'medium',
                'line': None,
                'message': f'Document is short ({word_count} words). Consider adding more detail and examples.'
            })

        return max(0, score), issues

    def _check_links(self, content: str, file_path: str) -> Tuple[int, List[Dict]]:
        """Check internal markdown links"""

        score = 100
        issues = []

        # Extract all markdown links
        links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)

        base_dir = Path(file_path).parent

        for link_text, url in links:
            # Skip external links (http/https)
            if url.startswith(('http://', 'https://', 'mailto:', '#')):
                continue

            # Check if internal file link exists
            link_path = base_dir / url.split('#')[0]  # Remove anchor

            if not link_path.exists():
                score -= 10
                issues.append({
                    'type': 'links',
                    'severity': 'high',
                    'line': None,
                    'message': f'Broken internal link: [{link_text}]({url})'
                })

        # Check for anchor links within document
        headings = re.findall(r'^#+\s+(.+)$', content, re.MULTILINE)
        heading_anchors = {self._create_anchor(h) for h in headings}

        anchor_links = re.findall(r'\[([^\]]+)\]\(#([^)]+)\)', content)
        for link_text, anchor in anchor_links:
            if anchor not in heading_anchors:
                score -= 5
                issues.append({
                    'type': 'links',
                    'severity': 'medium',
                    'line': None,
                    'message': f'Anchor link may be broken: [{link_text}](#{anchor})'
                })

        return max(0, score), issues

    def _generate_recommendations(self, analysis: Dict) -> List[str]:
        """Generate actionable recommendations based on analysis"""

        recommendations = []
        breakdown = analysis.get('breakdown', {})

        # Overall score recommendations
        overall = analysis.get('overall_score', 0)
        if overall < 50:
            recommendations.append('Document needs significant improvement across multiple areas. Start with high-severity issues.')
        elif overall < 70:
            recommendations.append('Document quality is below target. Focus on addressing medium and high-severity issues.')
        elif overall >= 85:
            recommendations.append('Document quality is excellent. Maintain current standards.')

        # Structure recommendations
        if breakdown.get('structure', 100) < 80:
            recommendations.append('Improve document structure: ensure proper heading hierarchy and include required sections.')

        # Readability recommendations
        if breakdown.get('readability', 100) < 70:
            metrics = analysis.get('readability_metrics', {})
            if metrics.get('flesch_reading_ease', 100) < 60:
                recommendations.append('Simplify language and sentence structure for better readability.')
            if metrics.get('avg_sentence_length', 0) > 25:
                recommendations.append('Break long sentences into shorter, clearer statements.')

        # Completeness recommendations
        if breakdown.get('completeness', 100) < 80:
            recommendations.append('Address placeholder text, add missing alt text for images, and specify languages for code blocks.')

        # Links recommendations
        if breakdown.get('links', 100) < 80:
            recommendations.append('Fix broken internal links and verify anchor references.')

        # Issue count recommendation
        issue_count = len(analysis.get('issues', []))
        if issue_count > 10:
            recommendations.append(f'{issue_count} issues found. Prioritize high-severity issues first.')

        return recommendations

    def _strip_markdown(self, content: str) -> str:
        """Remove markdown formatting for text analysis"""

        # Remove code blocks
        content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
        content = re.sub(r'`[^`]+`', '', content)

        # Remove headings markers
        content = re.sub(r'^#+\s+', '', content, flags=re.MULTILINE)

        # Remove links but keep text
        content = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', content)

        # Remove images
        content = re.sub(r'!\[([^\]]*)\]\([^)]+\)', '', content)

        # Remove bold/italic
        content = re.sub(r'\*\*([^*]+)\*\*', r'\1', content)
        content = re.sub(r'\*([^*]+)\*', r'\1', content)
        content = re.sub(r'__([^_]+)__', r'\1', content)
        content = re.sub(r'_([^_]+)_', r'\1', content)

        # Remove list markers
        content = re.sub(r'^\s*[-*+]\s+', '', content, flags=re.MULTILINE)
        content = re.sub(r'^\s*\d+\.\s+', '', content, flags=re.MULTILINE)

        # Remove horizontal rules
        content = re.sub(r'^[-*_]{3,}$', '', content, flags=re.MULTILINE)

        return content

    def _count_syllables(self, word: str) -> int:
        """Approximate syllable count for a word"""

        word = word.lower().strip()

        # Remove non-alphabetic characters
        word = re.sub(r'[^a-z]', '', word)

        if len(word) <= 3:
            return 1

        # Count vowel groups
        vowels = 'aeiouy'
        syllable_count = 0
        previous_was_vowel = False

        for char in word:
            is_vowel = char in vowels
            if is_vowel and not previous_was_vowel:
                syllable_count += 1
            previous_was_vowel = is_vowel

        # Adjust for silent 'e'
        if word.endswith('e'):
            syllable_count -= 1

        # Ensure at least one syllable
        if syllable_count == 0:
            syllable_count = 1

        return syllable_count

    def _create_anchor(self, heading: str) -> str:
        """Create GitHub-style anchor from heading"""

        anchor = heading.lower()
        anchor = re.sub(r'[^\w\s-]', '', anchor)
        anchor = re.sub(r'[\s_]+', '-', anchor)
        anchor = anchor.strip('-')

        return anchor


def format_text_output(results: List[Dict], verbose: bool = False) -> str:
    """Format analysis results as human-readable text"""

    output = []

    for result in results:
        if 'error' in result:
            output.append(f"❌ Error: {result['error']}")
            output.append("")
            continue

        file_name = Path(result['file']).name
        overall = result['overall_score']

        # Overall score with emoji
        if overall >= 85:
            emoji = "✅"
            status = "Excellent"
        elif overall >= 70:
            emoji = "⚠️"
            status = "Good"
        elif overall >= 50:
            emoji = "⚠️"
            status = "Needs Improvement"
        else:
            emoji = "❌"
            status = "Poor"

        output.append(f"{emoji} {file_name}")
        output.append("=" * 60)
        output.append(f"Overall Score: {overall}/100 ({status})")
        output.append("")

        # Breakdown scores
        if result['breakdown']:
            output.append("📊 Score Breakdown:")
            for category, score in result['breakdown'].items():
                bar = _create_bar(score)
                output.append(f"  {category.title():<15} {score:>3}/100 {bar}")
            output.append("")

        # Readability metrics
        if 'readability_metrics' in result:
            metrics = result['readability_metrics']
            output.append("📖 Readability Metrics:")
            output.append(f"  Flesch Reading Ease:  {metrics['flesch_reading_ease']:.1f} (60-80 target)")
            output.append(f"  Flesch-Kincaid Grade: {metrics['flesch_kincaid_grade']:.1f} (6-10 target)")
            output.append(f"  Gunning Fog Index:    {metrics['gunning_fog']:.1f} (8-12 target)")
            output.append(f"  Avg Sentence Length:  {metrics['avg_sentence_length']:.1f} words (15-25 target)")
            output.append("")

        # Issues
        if result['issues']:
            output.append(f"⚠️  Issues Found ({len(result['issues'])}):")

            # Group by severity
            high = [i for i in result['issues'] if i['severity'] == 'high']
            medium = [i for i in result['issues'] if i['severity'] == 'medium']
            low = [i for i in result['issues'] if i['severity'] == 'low']

            for severity, issues_list in [('high', high), ('medium', medium), ('low', low)]:
                if issues_list:
                    emoji_map = {'high': '🔴', 'medium': '🟡', 'low': '🔵'}
                    output.append(f"\n  {emoji_map[severity]} {severity.upper()}:")
                    for issue in issues_list[:10 if not verbose else None]:
                        line_info = f"Line {issue['line']}: " if issue['line'] else ""
                        output.append(f"    • {line_info}{issue['message']}")

                    if not verbose and len(issues_list) > 10:
                        output.append(f"    ... and {len(issues_list) - 10} more (use --verbose to see all)")
            output.append("")

        # Recommendations
        if result['recommendations']:
            output.append("💡 Recommendations:")
            for rec in result['recommendations']:
                output.append(f"  • {rec}")
            output.append("")

        output.append("")

    return '\n'.join(output)


def _create_bar(score: int, width: int = 20) -> str:
    """Create a visual progress bar"""
    filled = int((score / 100) * width)
    bar = '█' * filled + '░' * (width - filled)
    return bar


def main():
    """Main entry point for CLI"""
    import sys
    import argparse

    parser = argparse.ArgumentParser(
        description='Documentation Quality Analyzer - Analyze markdown documentation for quality, completeness, and readability',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze a single file
  %(prog)s README.md

  # Analyze with quality threshold
  %(prog)s docs/ --threshold 80

  # JSON output for CI/CD integration
  %(prog)s README.md --format json

  # Check specific aspects
  %(prog)s README.md --check structure --check links

  # Verbose output with all issues
  %(prog)s docs/ --verbose

Exit Codes:
  0 - Success (score >= threshold)
  1 - Below threshold
  2 - Error occurred

For more information, see the skill documentation.
        """
    )

    # Positional arguments
    parser.add_argument(
        'path',
        help='File or directory to analyze'
    )

    # Optional arguments
    parser.add_argument(
        '--format', '-o',
        choices=['text', 'json'],
        default='text',
        help='Output format: text (default) or json'
    )

    parser.add_argument(
        '--threshold', '-t',
        type=int,
        default=70,
        help='Minimum quality score (0-100, default: 70)'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed output with all issues'
    )

    parser.add_argument(
        '--check',
        action='append',
        choices=['structure', 'links', 'completeness', 'readability'],
        help='Specific checks to run (default: all). Can be specified multiple times.'
    )

    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )

    args = parser.parse_args()

    try:
        # Initialize analyzer
        analyzer = DocumentQualityAnalyzer()

        # Check if path exists
        path = Path(args.path)
        if not path.exists():
            print(f"❌ Error: Path not found: {args.path}", file=sys.stderr)
            sys.exit(2)

        # Analyze file or directory
        if path.is_file():
            if not args.path.endswith('.md'):
                print(f"⚠️  Warning: File does not have .md extension: {args.path}", file=sys.stderr)

            results = [analyzer.analyze_file(str(path), args.check)]
        else:
            if args.verbose:
                print(f"Analyzing markdown files in: {args.path}", file=sys.stderr)

            results = analyzer.analyze_directory(str(path), args.check)

        # Check for errors
        if any('error' in r for r in results):
            if args.format == 'json':
                print(json.dumps(results, indent=2))
            else:
                print(format_text_output(results, args.verbose))
            sys.exit(2)

        # Output results
        if args.format == 'json':
            print(json.dumps(results, indent=2))
        else:
            print(format_text_output(results, args.verbose))

        # Check threshold
        avg_score = sum(r['overall_score'] for r in results) / len(results)

        if avg_score < args.threshold:
            if args.format == 'text':
                print(f"❌ Quality check failed: Average score {avg_score:.1f} is below threshold {args.threshold}")
            sys.exit(1)
        else:
            if args.format == 'text' and args.verbose:
                print(f"✅ Quality check passed: Average score {avg_score:.1f} meets threshold {args.threshold}")

        sys.exit(0)

    except KeyboardInterrupt:
        print("\n⚠️  Operation cancelled by user", file=sys.stderr)
        sys.exit(130)

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(2)


if __name__ == "__main__":
    main()
