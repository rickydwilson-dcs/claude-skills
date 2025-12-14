#!/usr/bin/env python3
"""
SEO Content Optimizer - Analyzes and optimizes content for SEO
"""

import csv
import json
import logging
import re
from io import StringIO
from typing import Dict, List, Set

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SEOOptimizer:
    def __init__(self, verbose: bool = False):
        if verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("SEOOptimizer initialized")

        # Common stop words to filter
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
            'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
            'would', 'could', 'should', 'may', 'might', 'must', 'can', 'shall'
        }
        
        # SEO best practices
        self.best_practices = {
            'title_length': (50, 60),
            'meta_description_length': (150, 160),
            'url_length': (50, 60),
            'paragraph_length': (40, 150),
            'heading_keyword_placement': True,
            'keyword_density': (0.01, 0.03)  # 1-3%
        }
    
    def analyze(self, content: str, target_keyword: str = None,
                secondary_keywords: List[str] = None) -> Dict:
        """Analyze content for SEO optimization"""
        logger.debug("Starting SEO analysis")

        if not content or not content.strip():
            logger.warning("Empty or whitespace-only content provided")
            return {
                'content_length': 0,
                'keyword_analysis': {},
                'structure_analysis': {},
                'readability': {'score': 0, 'level': 'Unknown'},
                'meta_suggestions': {},
                'optimization_score': 0,
                'recommendations': ['No content to analyze']
            }

        logger.debug(f"Analyzing content: {len(content)} characters, keyword: {target_keyword}")

        analysis = {
            'content_length': len(content.split()),
            'keyword_analysis': {},
            'structure_analysis': self._analyze_structure(content),
            'readability': self._analyze_readability(content),
            'meta_suggestions': {},
            'optimization_score': 0,
            'recommendations': []
        }
        
        # Keyword analysis
        if target_keyword:
            analysis['keyword_analysis'] = self._analyze_keywords(
                content, target_keyword, secondary_keywords or []
            )
        
        # Generate meta suggestions
        analysis['meta_suggestions'] = self._generate_meta_suggestions(
            content, target_keyword
        )
        
        # Calculate optimization score
        analysis['optimization_score'] = self._calculate_seo_score(analysis)
        
        # Generate recommendations
        analysis['recommendations'] = self._generate_recommendations(analysis)
        
        return analysis
    
    def _analyze_keywords(self, content: str, primary: str,
                         secondary: List[str]) -> Dict:
        """Analyze keyword usage and density"""
        logger.debug(f"Analyzing keywords: primary='{primary}', secondary={len(secondary) if secondary else 0}")

        content_lower = content.lower()
        word_count = len(content.split())
        
        results = {
            'primary_keyword': {
                'keyword': primary,
                'count': content_lower.count(primary.lower()),
                'density': 0,
                'in_title': False,
                'in_headings': False,
                'in_first_paragraph': False
            },
            'secondary_keywords': [],
            'lsi_keywords': []
        }
        
        # Calculate primary keyword metrics
        if word_count > 0:
            results['primary_keyword']['density'] = (
                results['primary_keyword']['count'] / word_count
            )
        
        # Check keyword placement
        first_para = content.split('\n\n')[0] if '\n\n' in content else content[:200]
        results['primary_keyword']['in_first_paragraph'] = (
            primary.lower() in first_para.lower()
        )
        
        # Analyze secondary keywords
        for keyword in secondary:
            count = content_lower.count(keyword.lower())
            results['secondary_keywords'].append({
                'keyword': keyword,
                'count': count,
                'density': count / word_count if word_count > 0 else 0
            })
        
        # Extract potential LSI keywords
        results['lsi_keywords'] = self._extract_lsi_keywords(content, primary)
        
        return results
    
    def _analyze_structure(self, content: str) -> Dict:
        """Analyze content structure for SEO"""
        logger.debug("Analyzing content structure")

        lines = content.split('\n')
        
        structure = {
            'headings': {'h1': 0, 'h2': 0, 'h3': 0, 'total': 0},
            'paragraphs': 0,
            'lists': 0,
            'images': 0,
            'links': {'internal': 0, 'external': 0},
            'avg_paragraph_length': 0
        }
        
        paragraphs = []
        current_para = []
        
        for line in lines:
            # Count headings
            if line.startswith('# '):
                structure['headings']['h1'] += 1
                structure['headings']['total'] += 1
            elif line.startswith('## '):
                structure['headings']['h2'] += 1
                structure['headings']['total'] += 1
            elif line.startswith('### '):
                structure['headings']['h3'] += 1
                structure['headings']['total'] += 1
            
            # Count lists
            if line.strip().startswith(('- ', '* ', '1. ')):
                structure['lists'] += 1
            
            # Count links
            internal_links = len(re.findall(r'\[.*?\]\(/.*?\)', line))
            external_links = len(re.findall(r'\[.*?\]\(https?://.*?\)', line))
            structure['links']['internal'] += internal_links
            structure['links']['external'] += external_links
            
            # Track paragraphs
            if line.strip() and not line.startswith('#'):
                current_para.append(line)
            elif current_para:
                paragraphs.append(' '.join(current_para))
                current_para = []
        
        if current_para:
            paragraphs.append(' '.join(current_para))
        
        structure['paragraphs'] = len(paragraphs)
        
        if paragraphs:
            avg_length = sum(len(p.split()) for p in paragraphs) / len(paragraphs)
            structure['avg_paragraph_length'] = round(avg_length, 1)
        
        return structure
    
    def _analyze_readability(self, content: str) -> Dict:
        """Analyze content readability"""
        logger.debug("Analyzing readability")

        sentences = re.split(r'[.!?]+', content)
        words = content.split()

        if not sentences or not words:
            logger.warning("No sentences or words found for readability analysis")
            return {'score': 0, 'level': 'Unknown'}
        
        avg_sentence_length = len(words) / len(sentences)
        
        # Simple readability scoring
        if avg_sentence_length < 15:
            level = 'Easy'
            score = 90
        elif avg_sentence_length < 20:
            level = 'Moderate'
            score = 70
        elif avg_sentence_length < 25:
            level = 'Difficult'
            score = 50
        else:
            level = 'Very Difficult'
            score = 30
        
        return {
            'score': score,
            'level': level,
            'avg_sentence_length': round(avg_sentence_length, 1)
        }
    
    def _extract_lsi_keywords(self, content: str, primary_keyword: str) -> List[str]:
        """Extract potential LSI (semantically related) keywords"""
        words = re.findall(r'\b[a-z]+\b', content.lower())
        word_freq = {}
        
        # Count word frequencies
        for word in words:
            if word not in self.stop_words and len(word) > 3:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Sort by frequency and return top related terms
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        
        # Filter out the primary keyword and return top 10
        lsi_keywords = []
        for word, count in sorted_words:
            if word != primary_keyword.lower() and count > 1:
                lsi_keywords.append(word)
            if len(lsi_keywords) >= 10:
                break
        
        return lsi_keywords
    
    def _generate_meta_suggestions(self, content: str, keyword: str = None) -> Dict:
        """Generate SEO meta tag suggestions"""
        # Extract first sentence for description base
        sentences = re.split(r'[.!?]+', content)
        first_sentence = sentences[0] if sentences else content[:160]
        
        suggestions = {
            'title': '',
            'meta_description': '',
            'url_slug': '',
            'og_title': '',
            'og_description': ''
        }
        
        if keyword:
            # Title suggestion
            suggestions['title'] = f"{keyword.title()} - Complete Guide"
            if len(suggestions['title']) > 60:
                suggestions['title'] = keyword.title()[:57] + "..."
            
            # Meta description
            desc_base = f"Learn everything about {keyword}. {first_sentence}"
            if len(desc_base) > 160:
                desc_base = desc_base[:157] + "..."
            suggestions['meta_description'] = desc_base
            
            # URL slug
            suggestions['url_slug'] = re.sub(r'[^a-z0-9-]+', '-', 
                                            keyword.lower()).strip('-')
            
            # Open Graph tags
            suggestions['og_title'] = suggestions['title']
            suggestions['og_description'] = suggestions['meta_description']
        
        return suggestions
    
    def _calculate_seo_score(self, analysis: Dict) -> int:
        """Calculate overall SEO optimization score"""
        score = 0
        max_score = 100
        
        # Content length scoring (20 points)
        if 300 <= analysis['content_length'] <= 2500:
            score += 20
        elif 200 <= analysis['content_length'] < 300:
            score += 10
        elif analysis['content_length'] > 2500:
            score += 15
        
        # Keyword optimization (30 points)
        if analysis['keyword_analysis']:
            kw_data = analysis['keyword_analysis']['primary_keyword']
            
            # Density scoring
            if 0.01 <= kw_data['density'] <= 0.03:
                score += 15
            elif 0.005 <= kw_data['density'] < 0.01:
                score += 8
            
            # Placement scoring
            if kw_data['in_first_paragraph']:
                score += 10
            if kw_data.get('in_headings'):
                score += 5
        
        # Structure scoring (25 points)
        struct = analysis['structure_analysis']
        if struct['headings']['total'] > 0:
            score += 10
        if struct['paragraphs'] >= 3:
            score += 10
        if struct['links']['internal'] > 0 or struct['links']['external'] > 0:
            score += 5
        
        # Readability scoring (25 points)
        readability_score = analysis['readability']['score']
        score += int(readability_score * 0.25)
        
        return min(score, max_score)
    
    def _generate_recommendations(self, analysis: Dict) -> List[str]:
        """Generate SEO improvement recommendations"""
        recommendations = []
        
        # Content length recommendations
        if analysis['content_length'] < 300:
            recommendations.append(
                f"Increase content length to at least 300 words (currently {analysis['content_length']})"
            )
        elif analysis['content_length'] > 3000:
            recommendations.append(
                "Consider breaking long content into multiple pages or adding a table of contents"
            )
        
        # Keyword recommendations
        if analysis['keyword_analysis']:
            kw_data = analysis['keyword_analysis']['primary_keyword']
            
            if kw_data['density'] < 0.01:
                recommendations.append(
                    f"Increase keyword density for '{kw_data['keyword']}' (currently {kw_data['density']:.2%})"
                )
            elif kw_data['density'] > 0.03:
                recommendations.append(
                    f"Reduce keyword density to avoid over-optimization (currently {kw_data['density']:.2%})"
                )
            
            if not kw_data['in_first_paragraph']:
                recommendations.append(
                    "Include primary keyword in the first paragraph"
                )
        
        # Structure recommendations
        struct = analysis['structure_analysis']
        if struct['headings']['total'] == 0:
            recommendations.append("Add headings (H1, H2, H3) to improve content structure")
        if struct['links']['internal'] == 0:
            recommendations.append("Add internal links to related content")
        if struct['avg_paragraph_length'] > 150:
            recommendations.append("Break up long paragraphs for better readability")
        
        # Readability recommendations
        if analysis['readability']['avg_sentence_length'] > 20:
            recommendations.append("Simplify sentences for better readability")
        
        return recommendations

def format_csv_output(results: Dict) -> str:
    """Format SEO results as CSV"""
    output = StringIO()
    writer = csv.writer(output)

    # Header row
    writer.writerow(['metric', 'value', 'target', 'status'])

    # SEO Score
    seo_score = results.get('optimization_score', 0)
    writer.writerow(['seo_score', seo_score, '80+', 'pass' if seo_score >= 80 else 'needs_improvement'])

    # Content metrics
    writer.writerow(['content_length', results.get('content_length', 0), '300-2500', 'pass'])

    # Structure metrics
    struct = results.get('structure_analysis', {})
    writer.writerow(['headings', struct.get('headings', {}).get('total', 0), '3+', 'pass'])
    writer.writerow(['paragraphs', struct.get('paragraphs', 0), '3+', 'pass'])
    writer.writerow(['avg_paragraph_length', f"{struct.get('avg_paragraph_length', 0)}", '40-150', 'pass'])
    writer.writerow(['internal_links', struct.get('links', {}).get('internal', 0), '1+', 'pass'])
    writer.writerow(['external_links', struct.get('links', {}).get('external', 0), '1+', 'pass'])

    # Readability
    readability = results.get('readability', {})
    writer.writerow(['readability_score', readability.get('score', 0), '50+', 'pass'])
    writer.writerow(['readability_level', readability.get('level', 'Unknown'), 'Easy-Moderate', 'pass'])

    # Keyword metrics
    if results.get('keyword_analysis'):
        kw = results['keyword_analysis'].get('primary_keyword', {})
        writer.writerow(['primary_keyword', kw.get('keyword', ''), '', 'pass'])
        writer.writerow(['keyword_count', kw.get('count', 0), '1+', 'pass'])
        writer.writerow(['keyword_density', f"{kw.get('density', 0):.2%}", '1-3%', 'pass'])
        writer.writerow(['keyword_in_first_para', 'yes' if kw.get('in_first_paragraph') else 'no', 'yes', 'pass'])

    # Meta suggestions
    if results.get('meta_suggestions'):
        meta = results['meta_suggestions']
        writer.writerow(['suggested_title', meta.get('title', ''), '', 'pass'])
        writer.writerow(['suggested_url_slug', meta.get('url_slug', ''), '', 'pass'])

    return output.getvalue()

def optimize_content(content: str, keyword: str = None,
                     secondary_keywords: List[str] = None, output_format: str = 'text', verbose: bool = False) -> str:
    """Main function to optimize content"""
    logger.debug(f"Optimizing content with format: {output_format}")

    optimizer = SEOOptimizer(verbose=verbose)

    # Parse secondary keywords from comma-separated string if provided
    if secondary_keywords and isinstance(secondary_keywords, str):
        secondary_keywords = [kw.strip() for kw in secondary_keywords.split(',')]

    results = optimizer.analyze(content, keyword, secondary_keywords)

    # Return CSV format if requested
    if output_format == 'csv':
        return format_csv_output(results)
    # Return JSON format if requested
    elif output_format == 'json':
        return json.dumps(results, indent=2)

    # Format text output
    output = [
        "=== SEO Content Analysis ===",
        f"Overall SEO Score: {results['optimization_score']}/100",
        f"Content Length: {results['content_length']} words",
        f"",
        "Content Structure:",
        f"  Headings: {results['structure_analysis']['headings']['total']}",
        f"  Paragraphs: {results['structure_analysis']['paragraphs']}",
        f"  Avg Paragraph Length: {results['structure_analysis']['avg_paragraph_length']} words",
        f"  Internal Links: {results['structure_analysis']['links']['internal']}",
        f"  External Links: {results['structure_analysis']['links']['external']}",
        f"",
        f"Readability: {results['readability']['level']} (Score: {results['readability']['score']})",
        f""
    ]

    if results['keyword_analysis']:
        kw = results['keyword_analysis']['primary_keyword']
        output.extend([
            "Keyword Analysis:",
            f"  Primary Keyword: {kw['keyword']}",
            f"  Count: {kw['count']}",
            f"  Density: {kw['density']:.2%}",
            f"  In First Paragraph: {'Yes' if kw['in_first_paragraph'] else 'No'}",
            f""
        ])

        if results['keyword_analysis']['lsi_keywords']:
            output.append("  Related Keywords Found:")
            for lsi in results['keyword_analysis']['lsi_keywords'][:5]:
                output.append(f"    • {lsi}")
            output.append("")

    if results['meta_suggestions']:
        output.extend([
            "Meta Tag Suggestions:",
            f"  Title: {results['meta_suggestions']['title']}",
            f"  Description: {results['meta_suggestions']['meta_description']}",
            f"  URL Slug: {results['meta_suggestions']['url_slug']}",
            f""
        ])

    output.extend([
        "Recommendations:",
    ])

    for rec in results['recommendations']:
        output.append(f"  • {rec}")

    return '\n'.join(output)

if __name__ == "__main__":
    import sys
    import argparse
    from pathlib import Path

    parser = argparse.ArgumentParser(
        description='SEO content optimizer with keyword analysis',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic analysis
  %(prog)s content.txt

  # With keyword targeting
  %(prog)s content.txt --keyword "python programming"

  # With secondary keywords
  %(prog)s content.txt -k "python" -s "coding,development,tutorial"

  # JSON output to file
  %(prog)s content.txt -k "python" -o json -f results.json

For more information, see the skill documentation.
        """
    )

    # Positional arguments
    parser.add_argument(
        'input',
        help='Content file to optimize'
    )

    # Optional arguments
    parser.add_argument(
        '--keyword', '-k',
        help='Primary keyword for optimization'
    )

    parser.add_argument(
        '--secondary', '-s',
        help='Comma-separated secondary keywords'
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

    try:
        # Validate input file
        input_path = Path(args.input)

        if not input_path.exists():
            print(f"Error: Input file not found: {args.input}", file=sys.stderr)
            sys.exit(1)

        if not input_path.is_file():
            print(f"Error: Path is not a file: {args.input}", file=sys.stderr)
            sys.exit(1)

        # Read content
        logger.info(f"Reading input file: {args.input}")

        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError as e:
            logger.error(f"Unable to read file as text: {args.input}")
            print(f"Error: Unable to read file as text: {args.input}", file=sys.stderr)
            print("Hint: Ensure file is UTF-8 encoded text", file=sys.stderr)
            sys.exit(1)

        logger.info(f"Processing {len(content)} characters")
        if args.keyword:
            logger.info(f"Primary keyword: {args.keyword}")
        if args.secondary:
            logger.info(f"Secondary keywords: {args.secondary}")

        # Process content
        output = optimize_content(content, args.keyword, args.secondary, args.output, args.verbose)

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
