#!/usr/bin/env python3
"""
Component Generator - Generate React, Vue, and Angular components with tests.

Generates frontend components with:
- TypeScript support
- Unit tests (Jest/Vitest)
- Storybook stories
- Multiple styling approaches (Tailwind, CSS Modules, Styled Components)
- Atomic Design classification

Supports React 18+, Vue 3, and Angular 17+.
Uses Python standard library only - no external dependencies required.
"""

import argparse
import json
import logging
import os
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class Framework(Enum):
    """Supported frontend frameworks."""
    REACT = "react"
    VUE = "vue"
    ANGULAR = "angular"


class ComponentType(Enum):
    """Component types."""
    FUNCTIONAL = "functional"
    CLASS = "class"  # React only
    COMPOUND = "compound"
    HOOK = "hook"  # React only


class AtomicLevel(Enum):
    """Atomic Design levels."""
    ATOM = "atom"
    MOLECULE = "molecule"
    ORGANISM = "organism"
    TEMPLATE = "template"
    PAGE = "page"


class StylingApproach(Enum):
    """Styling approaches."""
    TAILWIND = "tailwind"
    CSS_MODULES = "css-modules"
    STYLED_COMPONENTS = "styled-components"
    SCSS = "scss"
    NONE = "none"


class TestFramework(Enum):
    """Test frameworks."""
    JEST = "jest"
    VITEST = "vitest"


@dataclass
class PropDefinition:
    """Definition of a component prop."""
    name: str
    prop_type: str
    required: bool = False
    default_value: Optional[str] = None
    description: str = ""


@dataclass
class ComponentConfig:
    """Configuration for component generation."""
    name: str
    framework: Framework
    component_type: ComponentType
    atomic_level: AtomicLevel
    styling: StylingApproach
    generate_tests: bool = True
    generate_stories: bool = True
    test_framework: TestFramework = TestFramework.JEST
    props: List[PropDefinition] = field(default_factory=list)
    use_typescript: bool = True
    output_dir: Path = field(default_factory=lambda: Path("components"))
    verbose: bool = False
    dry_run: bool = False


@dataclass
class GeneratedFile:
    """Information about a generated file."""
    relative_path: str
    content: str
    file_type: str  # "component", "test", "story", "style", "index"


@dataclass
class GenerationResult:
    """Result of component generation."""
    component_name: str
    framework: str
    output_directory: str
    files: List[GeneratedFile]
    success: bool
    timestamp: str
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


class ComponentGenerator:
    """
    Frontend component generation tool supporting React, Vue, and Angular.

    Generates:
    - Component files with TypeScript
    - Props/interface definitions
    - Unit tests (Jest/Vitest)
    - Storybook stories
    - Style files (Tailwind/CSS Modules/Styled)
    - Index barrel exports
    """

    def __init__(self, config: ComponentConfig):
        if config.verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("ComponentGenerator initialized")

        self.config = config
        self.files: List[GeneratedFile] = []
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def generate(self) -> GenerationResult:
        """Generate complete component package."""
        logger.debug(f"Generating {self.config.framework.value} component: {self.config.name}")
        if self.config.verbose:
            print(f"Generating {self.config.framework.value} component: {self.config.name}")

        # Validate component name
        if not self._validate_component_name():
            logger.error(f"Invalid component name: {self.config.name}")
            return self._create_error_result("Invalid component name")

        # Generate based on framework and type
        try:
            if self.config.framework == Framework.REACT:
                if self.config.component_type == ComponentType.HOOK:
                    self._generate_react_hook()
                elif self.config.component_type == ComponentType.COMPOUND:
                    self._generate_react_compound_component()
                elif self.config.component_type == ComponentType.CLASS:
                    self._generate_react_class_component()
                else:
                    self._generate_react_functional_component()
            elif self.config.framework == Framework.VUE:
                self._generate_vue_component()
            elif self.config.framework == Framework.ANGULAR:
                self._generate_angular_component()

            # Generate tests if requested
            if self.config.generate_tests:
                self._generate_test_file()

            # Generate stories if requested
            if self.config.generate_stories:
                self._generate_story_file()

            # Generate style file if needed
            if self.config.styling not in (StylingApproach.TAILWIND, StylingApproach.NONE):
                self._generate_style_file()

            # Generate index barrel export
            self._generate_index_file()

        except Exception as e:
            logger.error(f"Component generation failed: {e}")
            self.errors.append(str(e))

        # Write files if not dry run
        if not self.config.dry_run:
            self._write_files()

        return GenerationResult(
            component_name=self.config.name,
            framework=self.config.framework.value,
            output_directory=str(self.config.output_dir / self._get_component_dir()),
            files=self.files,
            success=len(self.errors) == 0,
            timestamp=datetime.now().isoformat(),
            errors=self.errors,
            warnings=self.warnings,
        )

    def _validate_component_name(self) -> bool:
        """Validate component name format."""
        logger.debug(f"Validating component name: {self.config.name}")
        name = self.config.name

        # Hooks must start with 'use'
        if self.config.component_type == ComponentType.HOOK:
            if not name.startswith("use"):
                logger.warning("Hook names must start with 'use'")
                self.errors.append("Hook names must start with 'use' (e.g., useDebounce)")
                return False
            return bool(re.match(r'^use[A-Z][a-zA-Z0-9]*$', name))

        # Components should be PascalCase
        if not re.match(r'^[A-Z][a-zA-Z0-9]*$', name):
            logger.warning(f"Component name '{name}' should be PascalCase")
            self.warnings.append(f"Component name '{name}' should be PascalCase")

        return True

    def _get_component_dir(self) -> str:
        """Get component directory name."""
        if self.config.component_type == ComponentType.HOOK:
            return f"hooks/{self.config.name}"
        return self.config.name

    def _to_kebab_case(self, name: str) -> str:
        """Convert PascalCase to kebab-case."""
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1-\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1-\2', s1).lower()

    def _generate_props_interface(self) -> str:
        """Generate TypeScript props interface."""
        name = self.config.name
        lines = [f"export interface {name}Props {{"]

        for prop in self.config.props:
            optional = "?" if not prop.required else ""
            desc = f"  /** {prop.description} */" if prop.description else ""
            if desc:
                lines.append(desc)
            lines.append(f"  {prop.name}{optional}: {prop.prop_type};")

        # Add common props
        lines.append("  className?: string;")
        lines.append("  children?: React.ReactNode;")
        lines.append("}")

        return "\n".join(lines)

    def _generate_react_functional_component(self) -> None:
        """Generate React functional component."""
        name = self.config.name
        kebab_name = self._to_kebab_case(name)
        ext = "tsx" if self.config.use_typescript else "jsx"

        # Build imports
        imports = ["import { forwardRef"]
        if self.config.props:
            imports[0] += ", HTMLAttributes"
        imports[0] += " } from 'react';"

        if self.config.styling == StylingApproach.CSS_MODULES:
            imports.append(f"import styles from './{name}.module.css';")
        elif self.config.styling == StylingApproach.STYLED_COMPONENTS:
            imports.append("import styled from 'styled-components';")
        elif self.config.styling == StylingApproach.TAILWIND:
            imports.append("import { cn } from '@/lib/utils';")

        # Build component
        props_interface = self._generate_props_interface() if self.config.use_typescript else ""

        # Default props based on atomic level
        default_props = self._get_default_props_for_level()

        content = f'''import {{ forwardRef }} from 'react';
{chr(10).join(imports[1:]) if len(imports) > 1 else ''}

{props_interface}

/**
 * {name} component
 * Atomic Level: {self.config.atomic_level.value}
 */
export const {name} = forwardRef<HTMLDivElement, {name}Props>(
  ({{ className, children{self._format_prop_destructure()}, ...props }}, ref) => {{
    return (
      <div
        ref={{ref}}
        className={{{self._get_class_expression()}}}
        {{...props}}
      >
        {{children}}
      </div>
    );
  }}
);

{name}.displayName = '{name}';

export default {name};
'''

        self.files.append(GeneratedFile(
            relative_path=f"{name}/{name}.{ext}",
            content=content,
            file_type="component",
        ))

    def _generate_react_class_component(self) -> None:
        """Generate React class component."""
        name = self.config.name
        ext = "tsx" if self.config.use_typescript else "jsx"

        props_interface = self._generate_props_interface() if self.config.use_typescript else ""

        content = f'''import {{ Component, ReactNode }} from 'react';

{props_interface}

interface {name}State {{
  // Add state properties here
}}

/**
 * {name} class component
 * Atomic Level: {self.config.atomic_level.value}
 */
export class {name} extends Component<{name}Props, {name}State> {{
  constructor(props: {name}Props) {{
    super(props);
    this.state = {{}};
  }}

  componentDidMount(): void {{
    // Lifecycle: Component mounted
  }}

  componentWillUnmount(): void {{
    // Lifecycle: Component will unmount
  }}

  render(): ReactNode {{
    const {{ className, children{self._format_prop_destructure()} }} = this.props;

    return (
      <div className={{className}}>
        {{children}}
      </div>
    );
  }}
}}

export default {name};
'''

        self.files.append(GeneratedFile(
            relative_path=f"{name}/{name}.{ext}",
            content=content,
            file_type="component",
        ))

    def _generate_react_compound_component(self) -> None:
        """Generate React compound component with Context."""
        name = self.config.name
        ext = "tsx" if self.config.use_typescript else "jsx"

        content = f'''import {{
  createContext,
  useContext,
  useState,
  ReactNode,
  forwardRef,
}} from 'react';

// Context
interface {name}ContextValue {{
  isOpen: boolean;
  toggle: () => void;
  // Add more context values as needed
}}

const {name}Context = createContext<{name}ContextValue | null>(null);

function use{name}Context() {{
  const context = useContext({name}Context);
  if (!context) {{
    throw new Error('use{name}Context must be used within a {name}');
  }}
  return context;
}}

// Root Component
export interface {name}Props {{
  children: ReactNode;
  defaultOpen?: boolean;
  className?: string;
}}

export const {name}Root = forwardRef<HTMLDivElement, {name}Props>(
  ({{ children, defaultOpen = false, className }}, ref) => {{
    const [isOpen, setIsOpen] = useState(defaultOpen);
    const toggle = () => setIsOpen((prev) => !prev);

    return (
      <{name}Context.Provider value={{{{ isOpen, toggle }}}}>
        <div ref={{ref}} className={{className}}>
          {{children}}
        </div>
      </{name}Context.Provider>
    );
  }}
);
{name}Root.displayName = '{name}Root';

// Trigger Component
export interface {name}TriggerProps {{
  children: ReactNode;
  className?: string;
  asChild?: boolean;
}}

export const {name}Trigger = forwardRef<HTMLButtonElement, {name}TriggerProps>(
  ({{ children, className, ...props }}, ref) => {{
    const {{ toggle }} = use{name}Context();

    return (
      <button ref={{ref}} onClick={{toggle}} className={{className}} {{...props}}>
        {{children}}
      </button>
    );
  }}
);
{name}Trigger.displayName = '{name}Trigger';

// Content Component
export interface {name}ContentProps {{
  children: ReactNode;
  className?: string;
}}

export const {name}Content = forwardRef<HTMLDivElement, {name}ContentProps>(
  ({{ children, className }}, ref) => {{
    const {{ isOpen }} = use{name}Context();

    if (!isOpen) return null;

    return (
      <div ref={{ref}} className={{className}}>
        {{children}}
      </div>
    );
  }}
);
{name}Content.displayName = '{name}Content';

// Compound Component Export
export const {name} = Object.assign({name}Root, {{
  Trigger: {name}Trigger,
  Content: {name}Content,
}});

export default {name};
'''

        self.files.append(GeneratedFile(
            relative_path=f"{name}/{name}.{ext}",
            content=content,
            file_type="component",
        ))

    def _generate_react_hook(self) -> None:
        """Generate React custom hook."""
        name = self.config.name
        ext = "ts" if self.config.use_typescript else "js"

        # Common hook templates
        hook_templates = {
            "useDebounce": self._get_debounce_hook_template(),
            "useLocalStorage": self._get_local_storage_hook_template(),
            "useMediaQuery": self._get_media_query_hook_template(),
            "useClickOutside": self._get_click_outside_hook_template(),
        }

        # Use template if available, otherwise generate generic
        if name in hook_templates:
            content = hook_templates[name]
        else:
            content = self._get_generic_hook_template()

        self.files.append(GeneratedFile(
            relative_path=f"hooks/{name}/{name}.{ext}",
            content=content,
            file_type="component",
        ))

    def _get_debounce_hook_template(self) -> str:
        """Get useDebounce hook template."""
        return f'''import {{ useState, useEffect }} from 'react';

/**
 * Debounce a value by a specified delay
 * @param value - The value to debounce
 * @param delay - Delay in milliseconds (default: 500ms)
 * @returns The debounced value
 */
export function {self.config.name}<T>(value: T, delay: number = 500): T {{
  const [debouncedValue, setDebouncedValue] = useState<T>(value);

  useEffect(() => {{
    const timer = setTimeout(() => {{
      setDebouncedValue(value);
    }}, delay);

    return () => {{
      clearTimeout(timer);
    }};
  }}, [value, delay]);

  return debouncedValue;
}}

export default {self.config.name};
'''

    def _get_local_storage_hook_template(self) -> str:
        """Get useLocalStorage hook template."""
        return f'''import {{ useState, useEffect, useCallback }} from 'react';

/**
 * Sync state with localStorage
 * @param key - localStorage key
 * @param initialValue - Initial value if key doesn't exist
 * @returns [storedValue, setValue, removeValue]
 */
export function {self.config.name}<T>(
  key: string,
  initialValue: T
): [T, (value: T | ((val: T) => T)) => void, () => void] {{
  // Get initial value from localStorage or use initialValue
  const readValue = useCallback((): T => {{
    if (typeof window === 'undefined') {{
      return initialValue;
    }}

    try {{
      const item = window.localStorage.getItem(key);
      return item ? (JSON.parse(item) as T) : initialValue;
    }} catch (error) {{
      console.warn(`Error reading localStorage key "${{key}}":`, error);
      return initialValue;
    }}
  }}, [initialValue, key]);

  const [storedValue, setStoredValue] = useState<T>(readValue);

  // Return a wrapped version of useState's setter function
  const setValue = useCallback(
    (value: T | ((val: T) => T)) => {{
      try {{
        const valueToStore = value instanceof Function ? value(storedValue) : value;
        setStoredValue(valueToStore);
        if (typeof window !== 'undefined') {{
          window.localStorage.setItem(key, JSON.stringify(valueToStore));
        }}
      }} catch (error) {{
        console.warn(`Error setting localStorage key "${{key}}":`, error);
      }}
    }},
    [key, storedValue]
  );

  const removeValue = useCallback(() => {{
    try {{
      setStoredValue(initialValue);
      if (typeof window !== 'undefined') {{
        window.localStorage.removeItem(key);
      }}
    }} catch (error) {{
      console.warn(`Error removing localStorage key "${{key}}":`, error);
    }}
  }}, [initialValue, key]);

  // Listen for changes in other tabs
  useEffect(() => {{
    const handleStorageChange = (event: StorageEvent) => {{
      if (event.key === key && event.newValue !== null) {{
        setStoredValue(JSON.parse(event.newValue));
      }}
    }};

    window.addEventListener('storage', handleStorageChange);
    return () => window.removeEventListener('storage', handleStorageChange);
  }}, [key]);

  return [storedValue, setValue, removeValue];
}}

export default {self.config.name};
'''

    def _get_media_query_hook_template(self) -> str:
        """Get useMediaQuery hook template."""
        return f'''import {{ useState, useEffect }} from 'react';

/**
 * Track media query matches
 * @param query - Media query string (e.g., '(min-width: 768px)')
 * @returns Whether the media query matches
 */
export function {self.config.name}(query: string): boolean {{
  const [matches, setMatches] = useState<boolean>(() => {{
    if (typeof window !== 'undefined') {{
      return window.matchMedia(query).matches;
    }}
    return false;
  }});

  useEffect(() => {{
    if (typeof window === 'undefined') return;

    const mediaQuery = window.matchMedia(query);
    const handler = (event: MediaQueryListEvent) => {{
      setMatches(event.matches);
    }};

    // Set initial value
    setMatches(mediaQuery.matches);

    // Modern browsers
    mediaQuery.addEventListener('change', handler);

    return () => {{
      mediaQuery.removeEventListener('change', handler);
    }};
  }}, [query]);

  return matches;
}}

export default {self.config.name};
'''

    def _get_click_outside_hook_template(self) -> str:
        """Get useClickOutside hook template."""
        return f'''import {{ useEffect, useRef, RefObject }} from 'react';

/**
 * Detect clicks outside of an element
 * @param callback - Function to call when clicking outside
 * @returns Ref to attach to the element
 */
export function {self.config.name}<T extends HTMLElement = HTMLElement>(
  callback: () => void
): RefObject<T> {{
  const ref = useRef<T>(null);

  useEffect(() => {{
    const handleClick = (event: MouseEvent) => {{
      if (ref.current && !ref.current.contains(event.target as Node)) {{
        callback();
      }}
    }};

    document.addEventListener('mousedown', handleClick);
    document.addEventListener('touchstart', handleClick as unknown as EventListener);

    return () => {{
      document.removeEventListener('mousedown', handleClick);
      document.removeEventListener('touchstart', handleClick as unknown as EventListener);
    }};
  }}, [callback]);

  return ref;
}}

export default {self.config.name};
'''

    def _get_generic_hook_template(self) -> str:
        """Get generic hook template."""
        return f'''import {{ useState, useEffect, useCallback }} from 'react';

/**
 * {self.config.name} - Custom React hook
 * @description Add hook description here
 */
export function {self.config.name}() {{
  const [state, setState] = useState(null);

  useEffect(() => {{
    // Effect logic here
    return () => {{
      // Cleanup logic here
    }};
  }}, []);

  const handleAction = useCallback(() => {{
    // Action handler logic
  }}, []);

  return {{
    state,
    handleAction,
  }};
}}

export default {self.config.name};
'''

    def _generate_vue_component(self) -> None:
        """Generate Vue 3 Composition API component."""
        name = self.config.name
        kebab_name = self._to_kebab_case(name)

        # Build props interface
        props_def = self._generate_vue_props_interface()

        # Style section
        style_section = ""
        if self.config.styling == StylingApproach.CSS_MODULES:
            style_section = f'\n<style module>\n.{kebab_name} {{\n  /* Component styles */\n}}\n</style>'
        elif self.config.styling == StylingApproach.SCSS:
            style_section = f'\n<style lang="scss" scoped>\n.{kebab_name} {{\n  /* Component styles */\n}}\n</style>'
        elif self.config.styling != StylingApproach.NONE:
            style_section = f'\n<style scoped>\n.{kebab_name} {{\n  /* Component styles */\n}}\n</style>'

        content = f'''<script setup lang="ts">
import {{ computed, ref }} from 'vue';

{props_def}

const emit = defineEmits<{{
  click: [event: MouseEvent];
  change: [value: string];
}}>();

// Reactive state
const isActive = ref(false);

// Computed properties
const computedClass = computed(() => [
  '{kebab_name}',
  {{ '{kebab_name}--active': isActive.value }},
  props.className,
]);

// Methods
function handleClick(event: MouseEvent) {{
  emit('click', event);
}}
</script>

<template>
  <div :class="computedClass" @click="handleClick">
    <slot />
  </div>
</template>
{style_section}
'''

        self.files.append(GeneratedFile(
            relative_path=f"{name}/{name}.vue",
            content=content,
            file_type="component",
        ))

    def _generate_vue_props_interface(self) -> str:
        """Generate Vue props interface."""
        lines = ["interface Props {"]

        for prop in self.config.props:
            optional = "?" if not prop.required else ""
            lines.append(f"  {prop.name}{optional}: {prop.prop_type};")

        lines.append("  className?: string;")
        lines.append("}")
        lines.append("")
        lines.append("const props = withDefaults(defineProps<Props>(), {")

        for prop in self.config.props:
            if prop.default_value:
                lines.append(f"  {prop.name}: {prop.default_value},")

        lines.append("  className: '',")
        lines.append("});")

        return "\n".join(lines)

    def _generate_angular_component(self) -> None:
        """Generate Angular standalone component."""
        name = self.config.name
        kebab_name = self._to_kebab_case(name)
        selector = f"app-{kebab_name}"

        # Component TypeScript file
        ts_content = f'''import {{ Component, Input, Output, EventEmitter, ChangeDetectionStrategy }} from '@angular/core';
import {{ CommonModule }} from '@angular/common';

@Component({{
  selector: '{selector}',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './{kebab_name}.component.html',
  styleUrls: ['./{kebab_name}.component.{self._get_style_ext()}'],
  changeDetection: ChangeDetectionStrategy.OnPush,
}})
export class {name}Component {{
{self._generate_angular_inputs()}
  @Output() clicked = new EventEmitter<MouseEvent>();

  onClick(event: MouseEvent): void {{
    this.clicked.emit(event);
  }}
}}
'''

        # Component HTML template
        html_content = f'''<div class="{kebab_name}" [ngClass]="className" (click)="onClick($event)">
  <ng-content></ng-content>
</div>
'''

        # Component style file
        style_content = f'''.{kebab_name} {{
  /* Component styles */
}}
'''

        self.files.append(GeneratedFile(
            relative_path=f"{name}/{kebab_name}.component.ts",
            content=ts_content,
            file_type="component",
        ))

        self.files.append(GeneratedFile(
            relative_path=f"{name}/{kebab_name}.component.html",
            content=html_content,
            file_type="component",
        ))

        self.files.append(GeneratedFile(
            relative_path=f"{name}/{kebab_name}.component.{self._get_style_ext()}",
            content=style_content,
            file_type="style",
        ))

    def _generate_angular_inputs(self) -> str:
        """Generate Angular @Input decorators."""
        lines = []

        for prop in self.config.props:
            required = ", { required: true }" if prop.required else ""
            lines.append(f"  @Input({required}) {prop.name}!: {prop.prop_type};")

        lines.append("  @Input() className = '';")

        return "\n".join(lines)

    def _get_style_ext(self) -> str:
        """Get style file extension."""
        if self.config.styling == StylingApproach.SCSS:
            return "scss"
        return "css"

    def _generate_test_file(self) -> None:
        """Generate test file for component."""
        name = self.config.name
        test_framework = self.config.test_framework

        if self.config.framework == Framework.REACT:
            content = self._generate_react_test(name, test_framework)
            ext = "test.tsx" if self.config.use_typescript else "test.jsx"
            dir_name = f"hooks/{name}" if self.config.component_type == ComponentType.HOOK else name
            self.files.append(GeneratedFile(
                relative_path=f"{dir_name}/{name}.{ext}",
                content=content,
                file_type="test",
            ))

        elif self.config.framework == Framework.VUE:
            content = self._generate_vue_test(name, test_framework)
            self.files.append(GeneratedFile(
                relative_path=f"{name}/{name}.test.ts",
                content=content,
                file_type="test",
            ))

        elif self.config.framework == Framework.ANGULAR:
            content = self._generate_angular_test(name)
            kebab_name = self._to_kebab_case(name)
            self.files.append(GeneratedFile(
                relative_path=f"{name}/{kebab_name}.component.spec.ts",
                content=content,
                file_type="test",
            ))

    def _generate_react_test(self, name: str, test_framework: TestFramework) -> str:
        """Generate React component test."""
        if self.config.component_type == ComponentType.HOOK:
            return self._generate_react_hook_test(name, test_framework)

        describe = "describe" if test_framework == TestFramework.JEST else "describe"
        it = "it" if test_framework == TestFramework.JEST else "it"
        expect_fn = "expect"

        return f'''import {{ render, screen, fireEvent }} from '@testing-library/react';
import {{ {name} }} from './{name}';

{describe}('{name}', () => {{
  {it}('renders children correctly', () => {{
    render(<{name}>Test Content</{name}>);
    expect(screen.getByText('Test Content')).toBeInTheDocument();
  }});

  {it}('applies custom className', () => {{
    render(<{name} className="custom-class">Content</{name}>);
    {expect_fn}(screen.getByText('Content').closest('div')).toHaveClass('custom-class');
  }});

  {it}('handles click events', () => {{
    const handleClick = {test_framework == TestFramework.JEST and "jest.fn()" or "vi.fn()"};
    render(<{name} onClick={{handleClick}}>Click Me</{name}>);
    fireEvent.click(screen.getByText('Click Me'));
    {expect_fn}(handleClick).toHaveBeenCalledTimes(1);
  }});

  {it}('forwards ref correctly', () => {{
    const ref = {{ current: null }};
    render(<{name} ref={{ref}}>Content</{name}>);
    {expect_fn}(ref.current).toBeInstanceOf(HTMLDivElement);
  }});
}});
'''

    def _generate_react_hook_test(self, name: str, test_framework: TestFramework) -> str:
        """Generate React hook test."""
        return f'''import {{ renderHook, act }} from '@testing-library/react';
import {{ {name} }} from './{name}';

describe('{name}', () => {{
  it('should initialize with default value', () => {{
    const {{ result }} = renderHook(() => {name}());
    expect(result.current).toBeDefined();
  }});

  it('should update state correctly', () => {{
    const {{ result }} = renderHook(() => {name}());
    // Add specific test logic here
  }});

  it('should clean up on unmount', () => {{
    const {{ unmount }} = renderHook(() => {name}());
    unmount();
    // Verify cleanup occurred
  }});
}});
'''

    def _generate_vue_test(self, name: str, test_framework: TestFramework) -> str:
        """Generate Vue component test."""
        return f'''import {{ mount }} from '@vue/test-utils';
import {name} from './{name}.vue';

describe('{name}', () => {{
  it('renders slot content', () => {{
    const wrapper = mount({name}, {{
      slots: {{
        default: 'Test Content',
      }},
    }});
    expect(wrapper.text()).toContain('Test Content');
  }});

  it('applies custom className', () => {{
    const wrapper = mount({name}, {{
      props: {{
        className: 'custom-class',
      }},
    }});
    expect(wrapper.classes()).toContain('custom-class');
  }});

  it('emits click event', async () => {{
    const wrapper = mount({name});
    await wrapper.trigger('click');
    expect(wrapper.emitted('click')).toBeTruthy();
  }});
}});
'''

    def _generate_angular_test(self, name: str) -> str:
        """Generate Angular component test."""
        kebab_name = self._to_kebab_case(name)

        return f'''import {{ ComponentFixture, TestBed }} from '@angular/core/testing';
import {{ {name}Component }} from './{kebab_name}.component';

describe('{name}Component', () => {{
  let component: {name}Component;
  let fixture: ComponentFixture<{name}Component>;

  beforeEach(async () => {{
    await TestBed.configureTestingModule({{
      imports: [{name}Component],
    }}).compileComponents();

    fixture = TestBed.createComponent({name}Component);
    component = fixture.componentInstance;
    fixture.detectChanges();
  }});

  it('should create', () => {{
    expect(component).toBeTruthy();
  }});

  it('should apply custom className', () => {{
    component.className = 'custom-class';
    fixture.detectChanges();
    const element = fixture.nativeElement.querySelector('.{kebab_name}');
    expect(element.classList.contains('custom-class')).toBeTruthy();
  }});

  it('should emit clicked event', () => {{
    const spy = spyOn(component.clicked, 'emit');
    const element = fixture.nativeElement.querySelector('.{kebab_name}');
    element.click();
    expect(spy).toHaveBeenCalled();
  }});
}});
'''

    def _generate_story_file(self) -> None:
        """Generate Storybook story file."""
        name = self.config.name

        if self.config.component_type == ComponentType.HOOK:
            return  # Hooks don't have stories

        if self.config.framework == Framework.REACT:
            content = self._generate_react_story(name)
            self.files.append(GeneratedFile(
                relative_path=f"{name}/{name}.stories.tsx",
                content=content,
                file_type="story",
            ))

        elif self.config.framework == Framework.VUE:
            content = self._generate_vue_story(name)
            self.files.append(GeneratedFile(
                relative_path=f"{name}/{name}.stories.ts",
                content=content,
                file_type="story",
            ))

    def _generate_react_story(self, name: str) -> str:
        """Generate React Storybook story."""
        return f'''import type {{ Meta, StoryObj }} from '@storybook/react';
import {{ {name} }} from './{name}';

const meta: Meta<typeof {name}> = {{
  title: 'Components/{self.config.atomic_level.value.capitalize()}/{name}',
  component: {name},
  tags: ['autodocs'],
  parameters: {{
    layout: 'centered',
  }},
  argTypes: {{
    className: {{
      control: 'text',
      description: 'Additional CSS classes',
    }},
    children: {{
      control: 'text',
      description: 'Component content',
    }},
  }},
}};

export default meta;
type Story = StoryObj<typeof {name}>;

export const Default: Story = {{
  args: {{
    children: '{name} Content',
  }},
}};

export const WithClassName: Story = {{
  args: {{
    children: '{name} with custom class',
    className: 'custom-class',
  }},
}};

export const Interactive: Story = {{
  args: {{
    children: 'Click me',
    onClick: () => console.log('Clicked!'),
  }},
}};
'''

    def _generate_vue_story(self, name: str) -> str:
        """Generate Vue Storybook story."""
        return f'''import type {{ Meta, StoryObj }} from '@storybook/vue3';
import {name} from './{name}.vue';

const meta: Meta<typeof {name}> = {{
  title: 'Components/{self.config.atomic_level.value.capitalize()}/{name}',
  component: {name},
  tags: ['autodocs'],
  argTypes: {{
    className: {{
      control: 'text',
      description: 'Additional CSS classes',
    }},
  }},
}};

export default meta;
type Story = StoryObj<typeof {name}>;

export const Default: Story = {{
  render: (args) => ({{
    components: {{ {name} }},
    setup() {{
      return {{ args }};
    }},
    template: '<{name} v-bind="args">{name} Content</{name}>',
  }}),
}};

export const WithClassName: Story = {{
  args: {{
    className: 'custom-class',
  }},
  render: (args) => ({{
    components: {{ {name} }},
    setup() {{
      return {{ args }};
    }},
    template: '<{name} v-bind="args">Styled Content</{name}>',
  }}),
}};
'''

    def _generate_style_file(self) -> None:
        """Generate style file based on styling approach."""
        name = self.config.name
        kebab_name = self._to_kebab_case(name)

        if self.config.styling == StylingApproach.CSS_MODULES:
            content = f'''.container {{
  /* Base styles */
}}

.{kebab_name} {{
  /* Component-specific styles */
}}

.{kebab_name}--active {{
  /* Active state */
}}

.{kebab_name}--disabled {{
  /* Disabled state */
}}
'''
            self.files.append(GeneratedFile(
                relative_path=f"{name}/{name}.module.css",
                content=content,
                file_type="style",
            ))

        elif self.config.styling == StylingApproach.SCSS:
            content = f'''@use 'sass:map';

.{kebab_name} {{
  // Base styles

  &--active {{
    // Active state
  }}

  &--disabled {{
    // Disabled state
  }}

  &__inner {{
    // Inner element
  }}
}}
'''
            self.files.append(GeneratedFile(
                relative_path=f"{name}/{name}.module.scss",
                content=content,
                file_type="style",
            ))

    def _generate_index_file(self) -> None:
        """Generate barrel export index file."""
        name = self.config.name
        ext = "ts" if self.config.use_typescript else "js"

        if self.config.component_type == ComponentType.HOOK:
            content = f"export {{ default as {name}, {name} }} from './{name}';\n"
            dir_name = f"hooks/{name}"
        else:
            content = f"export {{ default as {name}, {name} }} from './{name}';\n"
            if self.config.use_typescript and self.config.framework == Framework.REACT:
                content += f"export type {{ {name}Props }} from './{name}';\n"
            dir_name = name

        self.files.append(GeneratedFile(
            relative_path=f"{dir_name}/index.{ext}",
            content=content,
            file_type="index",
        ))

    def _format_prop_destructure(self) -> str:
        """Format props for destructuring in function signature."""
        if not self.config.props:
            return ""
        return ", " + ", ".join(p.name for p in self.config.props)

    def _get_class_expression(self) -> str:
        """Get className expression based on styling approach."""
        if self.config.styling == StylingApproach.TAILWIND:
            return "cn('base-class', className)"
        elif self.config.styling == StylingApproach.CSS_MODULES:
            return "cn(styles.container, className)"
        return "className"

    def _get_default_props_for_level(self) -> Dict[str, Any]:
        """Get default props based on atomic level."""
        level_props = {
            AtomicLevel.ATOM: {"variant": "primary", "size": "md"},
            AtomicLevel.MOLECULE: {"title": "Title", "description": "Description"},
            AtomicLevel.ORGANISM: {"items": [], "onAction": None},
            AtomicLevel.TEMPLATE: {"header": None, "sidebar": None, "footer": None},
            AtomicLevel.PAGE: {"data": None, "isLoading": False},
        }
        return level_props.get(self.config.atomic_level, {})

    def _write_files(self) -> None:
        """Write generated files to disk."""
        logger.debug("Writing generated files to disk")
        base_dir = self.config.output_dir

        for file in self.files:
            file_path = base_dir / file.relative_path
            file_path.parent.mkdir(parents=True, exist_ok=True)

            try:
                with open(file_path, 'w') as f:
                    f.write(file.content)
                if self.config.verbose:
                    print(f"  Created: {file.relative_path}")
            except IOError as e:
                logger.error(f"Failed to write {file.relative_path}: {e}")
                self.errors.append(f"Failed to write {file.relative_path}: {e}")

    def _create_error_result(self, error: str) -> GenerationResult:
        """Create an error result."""
        return GenerationResult(
            component_name=self.config.name,
            framework=self.config.framework.value,
            output_directory=str(self.config.output_dir),
            files=[],
            success=False,
            timestamp=datetime.now().isoformat(),
            errors=[error],
            warnings=[],
        )


def parse_props(props_args: List[str]) -> List[PropDefinition]:
    """Parse props from CLI arguments."""
    props = []
    for prop_str in props_args:
        parts = prop_str.split(":")
        if len(parts) >= 2:
            name = parts[0]
            prop_type = parts[1]
            required = len(parts) > 2 and parts[2].lower() == "true"
            default_value = parts[3] if len(parts) > 3 else None
            props.append(PropDefinition(
                name=name,
                prop_type=prop_type,
                required=required,
                default_value=default_value,
            ))
    return props


def format_text_output(result: GenerationResult) -> str:
    """Format results as human-readable text."""
    lines = []

    lines.append("=" * 60)
    lines.append("COMPONENT GENERATION REPORT")
    lines.append("=" * 60)
    lines.append("")
    lines.append(f"Component: {result.component_name}")
    lines.append(f"Framework: {result.framework}")
    lines.append(f"Output: {result.output_directory}")
    lines.append(f"Status: {'Success' if result.success else 'Failed'}")
    lines.append("")

    if result.files:
        lines.append("FILES GENERATED")
        lines.append("-" * 60)
        for file in result.files:
            lines.append(f"  [{file.file_type:10}] {file.relative_path}")
        lines.append("")
        lines.append(f"Total: {len(result.files)} files")
        lines.append("")

    if result.errors:
        lines.append("ERRORS")
        lines.append("-" * 60)
        for error in result.errors:
            lines.append(f"  - {error}")
        lines.append("")

    if result.warnings:
        lines.append("WARNINGS")
        lines.append("-" * 60)
        for warning in result.warnings:
            lines.append(f"  - {warning}")
        lines.append("")

    lines.append("=" * 60)

    return "\n".join(lines)


def format_json_output(result: GenerationResult) -> str:
    """Format results as JSON."""
    data = {
        "metadata": {
            "tool": "component_generator",
            "version": "1.0.0",
            "timestamp": result.timestamp,
        },
        "component": {
            "name": result.component_name,
            "framework": result.framework,
            "output_directory": result.output_directory,
        },
        "files": [
            {
                "path": f.relative_path,
                "type": f.file_type,
            }
            for f in result.files
        ],
        "success": result.success,
        "errors": result.errors,
        "warnings": result.warnings,
    }

    return json.dumps(data, indent=2)


def main():
    """Main entry point with standardized CLI interface."""
    parser = argparse.ArgumentParser(
        description="Component Generator - Generate React/Vue/Angular components with tests",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s Button
  %(prog)s ProductCard --framework react --level molecule
  %(prog)s DataTable --framework vue --tests --stories
  %(prog)s NavMenu --framework angular --styling tailwind
  %(prog)s useDebounce --type hook --tests
  %(prog)s Select --type compound --complete

Frameworks:
  react     - React 18+ with TypeScript (default)
  vue       - Vue 3 Composition API with TypeScript
  angular   - Angular 17+ standalone components

Component Types:
  functional - Functional component (default)
  class      - Class component (React only)
  compound   - Compound component with Context
  hook       - Custom hook (React only)

Atomic Design Levels:
  atom      - Basic building blocks (Button, Input)
  molecule  - Simple combinations (FormField, SearchBar)
  organism  - Complex UI sections (Header, ProductCard)
  template  - Page layouts (DashboardLayout)
  page      - Full pages (HomePage)

Styling:
  tailwind          - Tailwind CSS (default)
  css-modules       - CSS Modules
  styled-components - Styled Components (React)
  scss              - SCSS modules
  none              - No styling

Exit codes:
  0 - Success
  1 - Error
        """
    )

    parser.add_argument(
        'name',
        nargs='?',
        help='Component name (PascalCase) or hook name (useXxx)'
    )

    parser.add_argument(
        '--framework', '-f',
        choices=['react', 'vue', 'angular'],
        default='react',
        help='Target framework (default: react)'
    )

    parser.add_argument(
        '--type', '-t',
        choices=['functional', 'class', 'compound', 'hook'],
        default='functional',
        help='Component type (default: functional)'
    )

    parser.add_argument(
        '--level', '-l',
        choices=['atom', 'molecule', 'organism', 'template', 'page'],
        default='molecule',
        help='Atomic design level (default: molecule)'
    )

    parser.add_argument(
        '--styling', '-s',
        choices=['tailwind', 'css-modules', 'styled-components', 'scss', 'none'],
        default='tailwind',
        help='Styling approach (default: tailwind)'
    )

    parser.add_argument(
        '--tests',
        action='store_true',
        help='Generate test file'
    )

    parser.add_argument(
        '--stories',
        action='store_true',
        help='Generate Storybook story'
    )

    parser.add_argument(
        '--complete', '-c',
        action='store_true',
        help='Generate everything (component + tests + stories)'
    )

    parser.add_argument(
        '--test-framework',
        choices=['jest', 'vitest'],
        default='jest',
        help='Test framework (default: jest)'
    )

    parser.add_argument(
        '--output', '-o',
        default='components',
        help='Output directory (default: components)'
    )

    parser.add_argument(
        '--props', '-p',
        nargs='+',
        help='Props to generate (format: name:type:required, e.g., title:string:true)'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Verbose output'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be generated without writing files'
    )

    parser.add_argument(
        '--format',
        choices=['text', 'json'],
        default='text',
        help='Output format (default: text)'
    )

    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )

    args = parser.parse_args()

    # Validate name
    if not args.name:
        parser.print_help()
        print("\nError: Component name is required")
        sys.exit(1)

    # Parse props
    props = parse_props(args.props) if args.props else []

    # Handle --complete flag
    generate_tests = args.tests or args.complete
    generate_stories = args.stories or args.complete

    # Create config
    config = ComponentConfig(
        name=args.name,
        framework=Framework(args.framework),
        component_type=ComponentType(args.type),
        atomic_level=AtomicLevel(args.level),
        styling=StylingApproach(args.styling.replace('-', '_') if '-' in args.styling else args.styling),
        generate_tests=generate_tests,
        generate_stories=generate_stories,
        test_framework=TestFramework(args.test_framework),
        props=props,
        use_typescript=True,
        output_dir=Path(args.output),
        verbose=args.verbose,
        dry_run=args.dry_run,
    )

    # Generate component
    generator = ComponentGenerator(config)
    result = generator.generate()

    # Format output
    if args.format == 'json':
        output = format_json_output(result)
    else:
        output = format_text_output(result)

    print(output)

    sys.exit(0 if result.success else 1)


if __name__ == '__main__':
    main()
