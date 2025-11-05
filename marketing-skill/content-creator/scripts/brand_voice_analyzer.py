#!/usr/bin/env python3
"""
Brand Voice Analyzer - Analyzes content to establish and maintain brand voice consistency
"""

import re
from typing import Dict, List, Tuple
import json
import csv
from io import StringIO

class BrandVoiceAnalyzer:
    def __init__(self):
        self.voice_dimensions = {
            'formality': {
                'formal': ['hereby', 'therefore', 'furthermore', 'pursuant', 'regarding'],
                'casual': ['hey', 'cool', 'awesome', 'stuff', 'yeah', 'gonna']
            },
            'tone': {
                'professional': ['expertise', 'solution', 'optimize', 'leverage', 'strategic'],
                'friendly': ['happy', 'excited', 'love', 'enjoy', 'together', 'share']
            },
            'perspective': {
                'authoritative': ['proven', 'research shows', 'experts agree', 'data indicates'],
                'conversational': ['you might', 'let\'s explore', 'we think', 'imagine if']
            }
        }
    
    def analyze_text(self, text: str) -> Dict:
        """Analyze text for brand voice characteristics"""
        text_lower = text.lower()
        word_count = len(text.split())
        
        results = {
            'word_count': word_count,
            'readability_score': self._calculate_readability(text),
            'voice_profile': {},
            'sentence_analysis': self._analyze_sentences(text),
            'recommendations': []
        }
        
        # Analyze voice dimensions
        for dimension, categories in self.voice_dimensions.items():
            dim_scores = {}
            for category, keywords in categories.items():
                score = sum(1 for keyword in keywords if keyword in text_lower)
                dim_scores[category] = score
            
            # Determine dominant voice
            if sum(dim_scores.values()) > 0:
                dominant = max(dim_scores, key=dim_scores.get)
                results['voice_profile'][dimension] = {
                    'dominant': dominant,
                    'scores': dim_scores
                }
        
        # Generate recommendations
        results['recommendations'] = self._generate_recommendations(results)
        
        return results
    
    def _calculate_readability(self, text: str) -> float:
        """Calculate Flesch Reading Ease score"""
        sentences = re.split(r'[.!?]+', text)
        words = text.split()
        syllables = sum(self._count_syllables(word) for word in words)
        
        if len(sentences) == 0 or len(words) == 0:
            return 0
        
        avg_sentence_length = len(words) / len(sentences)
        avg_syllables_per_word = syllables / len(words)
        
        # Flesch Reading Ease formula
        score = 206.835 - 1.015 * avg_sentence_length - 84.6 * avg_syllables_per_word
        return max(0, min(100, score))
    
    def _count_syllables(self, word: str) -> int:
        """Count syllables in a word (simplified)"""
        word = word.lower()
        vowels = 'aeiou'
        syllable_count = 0
        previous_was_vowel = False
        
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not previous_was_vowel:
                syllable_count += 1
            previous_was_vowel = is_vowel
        
        # Adjust for silent e
        if word.endswith('e'):
            syllable_count -= 1
        
        return max(1, syllable_count)
    
    def _analyze_sentences(self, text: str) -> Dict:
        """Analyze sentence structure"""
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if not sentences:
            return {'average_length': 0, 'variety': 'low'}
        
        lengths = [len(s.split()) for s in sentences]
        avg_length = sum(lengths) / len(lengths) if lengths else 0
        
        # Calculate variety
        if len(set(lengths)) < 3:
            variety = 'low'
        elif len(set(lengths)) < 5:
            variety = 'medium'
        else:
            variety = 'high'
        
        return {
            'average_length': round(avg_length, 1),
            'variety': variety,
            'count': len(sentences)
        }
    
    def _generate_recommendations(self, analysis: Dict) -> List[str]:
        """Generate recommendations based on analysis"""
        recommendations = []
        
        # Readability recommendations
        if analysis['readability_score'] < 30:
            recommendations.append("Consider simplifying language for better readability")
        elif analysis['readability_score'] > 70:
            recommendations.append("Content is very easy to read - consider if this matches your audience")
        
        # Sentence variety
        if analysis['sentence_analysis']['variety'] == 'low':
            recommendations.append("Vary sentence length for better flow and engagement")
        
        # Voice consistency
        if analysis['voice_profile']:
            recommendations.append("Maintain consistent voice across all content")
        
        return recommendations

def format_csv_output(results: Dict) -> str:
    """Format results as CSV"""
    output = StringIO()
    writer = csv.writer(output)

    # Write header row with key metrics
    writer.writerow(['metric', 'value', 'status'])

    # Write core metrics
    writer.writerow(['word_count', results['word_count'], 'pass'])
    writer.writerow(['readability_score', f"{results['readability_score']:.1f}/100",
                     'pass' if 60 <= results['readability_score'] <= 100 else 'needs_improvement'])

    # Write voice profile metrics
    for dimension, profile in results['voice_profile'].items():
        writer.writerow([f"{dimension}_dominant", profile['dominant'], 'pass'])
        for category, score in profile['scores'].items():
            writer.writerow([f"{dimension}_{category}", score, 'pass'])

    # Write sentence analysis
    writer.writerow(['avg_sentence_length', f"{results['sentence_analysis']['average_length']} words", 'pass'])
    writer.writerow(['sentence_variety', results['sentence_analysis']['variety'], 'pass'])
    writer.writerow(['total_sentences', results['sentence_analysis']['count'], 'pass'])

    return output.getvalue()

def analyze_content(content: str, output_format: str = 'json') -> str:
    """Main function to analyze content"""
    analyzer = BrandVoiceAnalyzer()
    results = analyzer.analyze_text(content)

    if output_format == 'csv':
        return format_csv_output(results)
    elif output_format == 'json':
        return json.dumps(results, indent=2)
    else:
        # Human-readable format
        output = [
            f"=== Brand Voice Analysis ===",
            f"Word Count: {results['word_count']}",
            f"Readability Score: {results['readability_score']:.1f}/100",
            f"",
            f"Voice Profile:"
        ]

        for dimension, profile in results['voice_profile'].items():
            output.append(f"  {dimension.title()}: {profile['dominant']}")

        output.extend([
            f"",
            f"Sentence Analysis:",
            f"  Average Length: {results['sentence_analysis']['average_length']} words",
            f"  Variety: {results['sentence_analysis']['variety']}",
            f"  Total Sentences: {results['sentence_analysis']['count']}",
            f"",
            f"Recommendations:"
        ])

        for rec in results['recommendations']:
            output.append(f"  • {rec}")

        return '\n'.join(output)

if __name__ == "__main__":
    import sys
    import argparse
    from pathlib import Path

    parser = argparse.ArgumentParser(
        description='Analyze content for brand voice consistency',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s content.txt
  %(prog)s content.txt --output json
  %(prog)s content.txt -o json --file results.json
  %(prog)s content.txt -o text -v

For more information, see the skill documentation.
        """
    )

    # Positional arguments
    parser.add_argument(
        'input',
        help='Content file to analyze'
    )

    # Optional arguments
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
        if args.verbose:
            print(f"Reading input file: {args.input}", file=sys.stderr)

        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            print(f"Error: Unable to read file as text: {args.input}", file=sys.stderr)
            print("Hint: Ensure file is UTF-8 encoded text", file=sys.stderr)
            sys.exit(1)

        if args.verbose:
            print(f"Analyzing {len(content)} characters...", file=sys.stderr)

        # Process content
        output = analyze_content(content, args.output)

        # Write output
        if args.file:
            try:
                output_path = Path(args.file)
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(output)

                if args.verbose:
                    print(f"Results written to: {args.file}", file=sys.stderr)
                else:
                    print(f"Output saved to: {args.file}")

            except PermissionError:
                print(f"Error: Permission denied writing to: {args.file}", file=sys.stderr)
                sys.exit(4)
            except Exception as e:
                print(f"Error writing output file: {e}", file=sys.stderr)
                sys.exit(4)
        else:
            print(output)

        sys.exit(0)

    except FileNotFoundError as e:
        print(f"Error: File not found: {e}", file=sys.stderr)
        sys.exit(1)

    except PermissionError as e:
        print(f"Error: Permission denied: {e}", file=sys.stderr)
        sys.exit(1)

    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        sys.exit(130)

    except Exception as e:
        print(f"Error: Unexpected error occurred: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)
