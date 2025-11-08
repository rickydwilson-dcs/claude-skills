# UI Design System Tools Documentation

Complete documentation for design system Python tools.

## design_token_generator.py

Generate complete design token systems from a single brand color.

### Overview

**Purpose:** Automatically generate a full design system including color palettes, typography scales, spacing systems, shadows, and animations from a brand color.

**Key Capabilities:**
- Color palette generation (50-900 scale)
- Modular typography scale
- 8pt spacing grid system
- Shadow and elevation tokens
- Animation timing tokens
- Multiple export formats (JSON, CSS, SCSS)
- Three style presets (modern, classic, playful)

### Usage

```bash
# Modern style with brand color
python3 scripts/design_token_generator.py --brand "#0066CC" --style modern

# Classic style
python3 scripts/design_token_generator.py --brand "#0066CC" --style classic

# Playful style
python3 scripts/design_token_generator.py --brand "#8B5CF6" --style playful

# Export as CSS
python3 scripts/design_token_generator.py --brand "#0066CC" --output css

# Export as SCSS
python3 scripts/design_token_generator.py --brand "#0066CC" --output scss -f tokens.scss

# Export as JSON
python3 scripts/design_token_generator.py --brand "#0066CC" -o json -f design-tokens.json

# Verbose mode
python3 scripts/design_token_generator.py --brand "#0066CC" -v
```

### Command-Line Options

```
usage: design_token_generator.py [-h] --brand BRAND
                                 [--style {modern,classic,playful}]
                                 [--output {json,css,scss}] [--file FILE]
                                 [--verbose] [--version]

Generate design system tokens from brand color

required arguments:
  --brand BRAND         Brand color in hex format (e.g., "#0066CC")

optional arguments:
  -h, --help            show help message
  --style {modern,classic,playful}
                        Design style preset (default: modern)
  --output {json,css,scss}, -o {json,css,scss}
                        Output format (default: json)
  --file FILE, -f FILE  Write output to file
  --verbose, -v         Enable detailed output
  --version             show version
```

### Generated Tokens

**Color System:**
- Primary scale (50-900)
- Secondary scale (50-900)
- Neutral scale (50-900)
- Semantic colors (success, warning, error, info)

**Typography:**
- Font size scale (xs to 3xl)
- Line height scale
- Font weight scale
- Letter spacing

**Spacing:**
- 8pt grid system (0 to 20)
- Component-specific spacing

**Shadows:**
- 5 elevation levels (sm to 2xl)

**Animation:**
- Duration tokens
- Easing functions

### Export Formats

**JSON (Default):**
```json
{
  "color": {
    "primary": {
      "50": "#E6F2FF",
      "500": "#0066CC",
      "900": "#002952"
    }
  },
  "spacing": {
    "4": "16px"
  }
}
```

**CSS Custom Properties:**
```css
:root {
  --color-primary-50: #E6F2FF;
  --color-primary-500: #0066CC;
  --spacing-4: 16px;
}
```

**SCSS Variables:**
```scss
$color-primary-50: #E6F2FF;
$color-primary-500: #0066CC;
$spacing-4: 16px;
```

### Integration Patterns

**React/Tailwind:**
```bash
# Generate tokens
python3 scripts/design_token_generator.py --brand "#0066CC" -o json -f tokens.json

# Import in tailwind.config.js
import tokens from './tokens.json';
export default {
  theme: {
    extend: {
      colors: tokens.color
    }
  }
};
```

**Figma:**
```bash
# Export as JSON
python3 scripts/design_token_generator.py --brand "#0066CC" -o json -f figma-tokens.json

# Import to Figma using Tokens Studio plugin
```

**CSS Framework:**
```bash
# Generate CSS
python3 scripts/design_token_generator.py --brand "#0066CC" -o css -f tokens.css

# Import in your CSS
@import 'tokens.css';
```

---

**Last Updated:** 2025-11-08
**Tool Version:** 1.0.0
**Related Files:**
- [frameworks.md](frameworks.md) - Design token architecture and color systems
- [templates.md](templates.md) - Component templates and examples
