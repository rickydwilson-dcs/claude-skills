# Frontend Python Tools Documentation

Comprehensive documentation for Python CLI tools including component generation, bundle analysis, and frontend scaffolding.

## component_generator.py

Automated React/Next.js component generation tool with TypeScript, tests, and stories.

### Overview

Generates production-ready React components with TypeScript definitions, unit tests, Storybook stories, and CSS modules or Tailwind styles. Supports multiple component patterns (functional, compound, HOC) and atomic design levels.

### Usage

**Basic Commands:**
```bash
# Generate basic component
python scripts/component_generator.py Button --type component

# Generate compound component
python scripts/component_generator.py Select --type compound

# Generate with Storybook stories
python scripts/component_generator.py Card --stories

# Generate with tests
python scripts/component_generator.py Modal --tests

# Generate complete component (tests + stories + styles)
python scripts/component_generator.py ProductCard --complete

# Show help
python scripts/component_generator.py --help
```

**Available Options:**
- `name`: Component name (required, PascalCase)
- `--type/-t`: Component type (component, compound, hoc, hook) - default: component
- `--level/-l`: Atomic design level (atom, molecule, organism, template) - default: molecule
- `--styling/-s`: Styling approach (css-modules, tailwind, styled-components) - default: tailwind
- `--tests`: Generate test file
- `--stories`: Generate Storybook story
- `--complete/-c`: Generate everything (component + tests + stories)
- `--output/-o`: Output directory - default: components/
- `--verbose/-v`: Show detailed output

### Component Types

**Functional Component:**
```bash
python scripts/component_generator.py Button --type component --complete

# Generates:
# components/Button/
# ├── Button.tsx
# ├── Button.test.tsx
# ├── Button.stories.tsx
# └── index.ts
```

**Compound Component:**
```bash
python scripts/component_generator.py Select --type compound --complete

# Generates Select with sub-components:
# - Select.tsx (main component)
# - Select.Trigger
# - Select.Options
# - Select.Option
```

**Custom Hook:**
```bash
python scripts/component_generator.py useDebounce --type hook --tests

# Generates:
# hooks/
# ├── useDebounce.ts
# └── useDebounce.test.ts
```

### Generated Component Structure

**Button Component Example:**
```typescript
// components/Button/Button.tsx
import { ButtonHTMLAttributes, forwardRef } from 'react';
import { cva, type VariantProps } from 'class-variance-authority';

const buttonVariants = cva(
  'inline-flex items-center justify-center rounded-md font-medium transition-colors',
  {
    variants: {
      variant: {
        primary: 'bg-blue-600 text-white hover:bg-blue-700',
        secondary: 'bg-gray-200 text-gray-900 hover:bg-gray-300'
      },
      size: {
        sm: 'h-8 px-3 text-sm',
        md: 'h-10 px-4',
        lg: 'h-12 px-6 text-lg'
      }
    },
    defaultVariants: {
      variant: 'primary',
      size: 'md'
    }
  }
);

export interface ButtonProps
  extends ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  isLoading?: boolean;
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, isLoading, children, ...props }, ref) => {
    return (
      <button
        ref={ref}
        className={buttonVariants({ variant, size, className })}
        disabled={isLoading || props.disabled}
        {...props}
      >
        {isLoading && <Spinner className="mr-2" />}
        {children}
      </button>
    );
  }
);

Button.displayName = 'Button';

// components/Button/Button.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from './Button';

describe('Button', () => {
  it('renders correctly', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('handles click events', () => {
    const onClick = jest.fn();
    render(<Button onClick={onClick}>Click</Button>);
    fireEvent.click(screen.getByText('Click'));
    expect(onClick).toHaveBeenCalledTimes(1);
  });
});

// components/Button/Button.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { Button } from './Button';

const meta: Meta<typeof Button> = {
  title: 'UI/Button',
  component: Button,
  tags: ['autodocs']
};

export default meta;
type Story = StoryObj<typeof Button>;

export const Primary: Story = {
  args: {
    children: 'Button',
    variant: 'primary'
  }
};

export const Loading: Story = {
  args: {
    children: 'Loading',
    isLoading: true
  }
};
```

### Output Example

```bash
$ python scripts/component_generator.py ProductCard --complete --level molecule

🎨 Component Generator
======================

Component: ProductCard
Type: Component
Level: Molecule
Styling: Tailwind CSS
Tests: Yes
Stories: Yes

Creating component structure... ✓
Generating ProductCard.tsx... ✓
Generating ProductCard.test.tsx... ✓
Generating ProductCard.stories.tsx... ✓
Creating index.ts... ✓

✅ Component created successfully!

Files created:
  components/ProductCard/ProductCard.tsx
  components/ProductCard/ProductCard.test.tsx
  components/ProductCard/ProductCard.stories.tsx
  components/ProductCard/index.ts

Next steps:
  1. Import: import { ProductCard } from '@/components/ProductCard'
  2. Run tests: npm test ProductCard
  3. View stories: npm run storybook
```

### Common Workflows

**Create UI Component Library:**
```bash
# Atoms
python scripts/component_generator.py Button --level atom --complete
python scripts/component_generator.py Input --level atom --complete
python scripts/component_generator.py Label --level atom --complete

# Molecules
python scripts/component_generator.py FormField --level molecule --complete
python scripts/component_generator.py SearchBar --level molecule --complete

# Organisms
python scripts/component_generator.py Navigation --level organism --complete
python scripts/component_generator.py LoginForm --level organism --complete
```

---

## bundle_analyzer.py

Advanced bundle analysis tool for identifying optimization opportunities in Next.js/React applications.

### Overview

Analyzes webpack bundle output to identify large dependencies, duplicate packages, unused code, and optimization opportunities. Provides actionable recommendations for reducing bundle size.

### Usage

**Basic Commands:**
```bash
# Analyze Next.js build
python scripts/bundle_analyzer.py .next/

# Analyze with treemap visualization
python scripts/bundle_analyzer.py .next/ --visualize

# Generate HTML report
python scripts/bundle_analyzer.py .next/ --output html --save report.html

# Show detailed analysis
python scripts/bundle_analyzer.py .next/ --verbose

# Show help
python scripts/bundle_analyzer.py --help
```

**Available Options:**
- `path`: Path to build directory (required)
- `--output/-o`: Output format (text, json, html) - default: text
- `--save/-s`: Save report to file
- `--visualize/-v`: Generate treemap visualization
- `--threshold/-t`: Size threshold in KB for warnings - default: 500
- `--verbose`: Show detailed breakdown
- `--compare/-c`: Compare with previous build

### Analysis Features

**Bundle Size Analysis:**
- Total bundle size
- Per-page bundle sizes
- Shared chunks analysis
- First-load JS size

**Dependency Analysis:**
- Largest dependencies
- Duplicate packages
- Unused dependencies
- Tree-shaking opportunities

**Optimization Recommendations:**
- Code splitting suggestions
- Dynamic import opportunities
- Image optimization needs
- Font loading optimization

### Output Example

```bash
$ python scripts/bundle_analyzer.py .next/ --verbose

📊 Bundle Analyzer
==================

Build Directory: .next/
Framework: Next.js 14.0.0
Build Type: Production

Bundle Size Summary:
--------------------
Total Size: 2.4 MB
First Load JS: 387 KB
Shared Chunks: 142 KB

Per-Page Analysis:
------------------
/ (index)
  First Load: 387 KB
  Page-specific: 12 KB
  Status: ✓ Good

/dashboard
  First Load: 542 KB
  Page-specific: 187 KB
  Status: ⚠️  Large (>500KB)

/products
  First Load: 423 KB
  Page-specific: 68 KB
  Status: ✓ Good

Largest Dependencies:
---------------------
1. lodash (72 KB) - Consider lodash-es for tree-shaking
2. moment (68 KB) - Replace with date-fns (smaller)
3. recharts (156 KB) - Consider dynamic import
4. @tanstack/react-query (45 KB)
5. react-hook-form (32 KB)

Duplicate Packages:
-------------------
1. react (3 versions: 18.2.0, 18.1.0, 17.0.2)
   - Used by: react-dom, styled-components, react-query
   - Recommendation: Update all to single version

Issues Found:
-------------
⚠️  Dashboard page exceeds 500KB first load
    - Recommendation: Split heavy components
    - Consider: Dynamic imports for charts

⚠️  Duplicate React versions detected
    - Recommendation: Update package-lock.json
    - Run: npm dedupe

⚠️  Large moment.js dependency
    - Recommendation: Replace with date-fns
    - Potential savings: ~50KB

Optimization Opportunities:
--------------------------
1. Dynamic Import Charts
   - Current: 156KB in main bundle
   - Potential savings: 140KB
   - Implementation: const Chart = dynamic(() => import('./Chart'))

2. Replace moment with date-fns
   - Current: 68KB
   - New size: 15KB
   - Savings: 53KB

3. Use lodash-es instead of lodash
   - Current: 72KB (all functions)
   - Potential: 8KB (tree-shaken)
   - Savings: 64KB

Total Potential Savings: 257KB (10.7% reduction)

✅ Analysis complete!
```

### HTML Report Features

```bash
# Generate interactive HTML report
python scripts/bundle_analyzer.py .next/ --output html --save report.html

# Report includes:
# - Interactive treemap of bundle
# - Clickable dependency graph
# - Timeline of bundle growth
# - Optimization checklist
# - Before/after comparisons
```

### Common Workflows

**Pre-Deployment Analysis:**
```bash
# 1. Build production
npm run build

# 2. Analyze bundle
python scripts/bundle_analyzer.py .next/ --verbose

# 3. Generate report for team
python scripts/bundle_analyzer.py .next/ --output html --save pre-deploy-report.html

# 4. Review and optimize
# Implement recommended changes

# 5. Re-analyze
npm run build
python scripts/bundle_analyzer.py .next/ --compare pre-deploy-report.html
```

**Continuous Monitoring:**
```bash
# Add to CI/CD pipeline
npm run build
python scripts/bundle_analyzer.py .next/ --output json --save bundle-stats.json

# Compare with baseline
python scripts/bundle_analyzer.py .next/ --compare baseline-bundle-stats.json

# Fail if bundle grows >10%
if [ bundle_growth > 10% ]; then exit 1; fi
```

---

## frontend_scaffolder.py

Complete Next.js/React project scaffolding tool with modern tech stack.

### Overview

Generates production-ready Next.js or React projects with TypeScript, Tailwind CSS, React Query, Zustand, testing setup, and CI/CD configuration.

### Usage

**Basic Commands:**
```bash
# Create Next.js App Router project
python scripts/frontend_scaffolder.py my-app --framework nextjs

# Create React + Vite project
python scripts/frontend_scaffolder.py my-app --framework react-vite

# Create with all features
python scripts/frontend_scaffolder.py my-app --framework nextjs --complete

# Minimal setup
python scripts/frontend_scaffolder.py my-app --framework nextjs --minimal

# Show help
python scripts/frontend_scaffolder.py --help
```

**Available Options:**
- `name`: Project name (required)
- `--framework/-f`: Framework (nextjs, react-vite, remix) - default: nextjs
- `--styling/-s`: Styling (tailwind, css-modules, styled-components) - default: tailwind
- `--state`: State management (zustand, redux, jotai, none) - default: zustand
- `--forms`: Form library (react-hook-form, formik, none) - default: react-hook-form
- `--complete/-c`: Include all features
- `--minimal/-m`: Minimal setup
- `--auth`: Include authentication setup
- `--analytics`: Include analytics (Google Analytics, Plausible)
- `--output/-o`: Output directory

### Generated Project Structure

**Next.js App Router:**
```
my-app/
├── app/
│   ├── (auth)/
│   │   ├── login/
│   │   └── register/
│   ├── dashboard/
│   │   └── page.tsx
│   ├── layout.tsx
│   └── page.tsx
├── components/
│   ├── ui/
│   │   ├── Button.tsx
│   │   ├── Input.tsx
│   │   └── Modal.tsx
│   └── layouts/
│       └── DashboardLayout.tsx
├── lib/
│   ├── api.ts
│   ├── auth.ts
│   └── utils.ts
├── hooks/
│   ├── useDebounce.ts
│   └── useLocalStorage.ts
├── stores/
│   └── userStore.ts
├── styles/
│   └── globals.css
├── public/
├── tests/
│   ├── unit/
│   └── integration/
├── .env.local
├── .env.example
├── next.config.js
├── tailwind.config.ts
├── tsconfig.json
├── jest.config.js
├── package.json
└── README.md
```

### Features Included

**Complete Setup (--complete):**
- TypeScript configuration
- Tailwind CSS with custom theme
- React Query for data fetching
- Zustand for state management
- React Hook Form with Zod validation
- Jest + Testing Library setup
- Storybook configuration
- ESLint + Prettier
- Husky pre-commit hooks
- GitHub Actions CI/CD
- Docker configuration
- Authentication setup (optional)

**Minimal Setup (--minimal):**
- Basic Next.js/React setup
- TypeScript
- Tailwind CSS (basic)
- Essential utilities only

### Output Example

```bash
$ python scripts/frontend_scaffolder.py my-app --framework nextjs --complete

🚀 Frontend Scaffolder
======================

Project: my-app
Framework: Next.js 14 (App Router)
Styling: Tailwind CSS
State: Zustand
Forms: React Hook Form
Auth: Enabled
Analytics: Google Analytics

Creating project structure... ✓
Installing dependencies... ✓
Configuring TypeScript... ✓
Setting up Tailwind CSS... ✓
Generating components... ✓
Setting up testing... ✓
Configuring CI/CD... ✓

✅ Project created successfully!

Next steps:
  cd my-app
  npm run dev

Your app will be available at http://localhost:3000

Additional commands:
  npm run build      # Build for production
  npm test           # Run tests
  npm run lint       # Lint code
  npm run storybook  # Start Storybook
```

### Common Workflows

**New Project Setup:**
```bash
# 1. Scaffold project
python scripts/frontend_scaffolder.py my-app --framework nextjs --complete

# 2. Start development
cd my-app
npm run dev

# 3. Create first page
npm run generate:component HomePage --level template

# 4. Configure environment
cp .env.example .env.local
# Edit .env.local with API keys
```

This comprehensive tool documentation covers all frontend development automation needs.
