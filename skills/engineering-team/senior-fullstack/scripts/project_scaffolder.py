#!/usr/bin/env python3
"""
Project Scaffolder - Monorepo Structure Generator

A comprehensive monorepo scaffolding tool that generates:
- Workspace configurations (npm, yarn, pnpm)
- Multi-package project structures
- Shared utilities and configuration packages
- Turborepo integration (optional)
- TypeScript configurations
- ESLint/Prettier setups

Part of the senior-fullstack skill package.
"""

import argparse
import json
import logging
import os
import sys
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# =============================================================================
# Enums and Data Classes
# =============================================================================

class PackageManager(Enum):
    """Supported package managers"""
    NPM = "npm"
    YARN = "yarn"
    PNPM = "pnpm"


@dataclass
class PackageConfig:
    """Configuration for a package in the monorepo"""
    name: str
    description: str
    is_shared: bool = False
    dependencies: List[str] = field(default_factory=list)
    dev_dependencies: List[str] = field(default_factory=list)
    scripts: Dict[str, str] = field(default_factory=dict)


@dataclass
class MonorepoConfig:
    """Full monorepo configuration"""
    name: str
    package_manager: PackageManager
    packages: List[str]
    include_turborepo: bool
    output_path: Path


# =============================================================================
# File Templates
# =============================================================================

class Templates:
    """Template strings for generated files"""

    @staticmethod
    def root_package_json(config: MonorepoConfig) -> Dict:
        """Generate root package.json"""
        pkg = {
            "name": config.name,
            "private": True,
            "version": "0.0.0",
            "description": f"{config.name} monorepo",
            "scripts": {
                "build": f"{config.package_manager.value} run build:all",
                "build:all": "",  # Will be set based on package manager
                "test": f"{config.package_manager.value} run test:all",
                "test:all": "",
                "lint": f"{config.package_manager.value} run lint:all",
                "lint:all": "",
                "clean": f"{config.package_manager.value} run clean:all",
                "clean:all": "",
                "dev": f"{config.package_manager.value} run dev:all",
                "dev:all": "",
            },
            "devDependencies": {
                "typescript": "^5.3.0",
                "@types/node": "^20.10.0",
                "eslint": "^8.55.0",
                "prettier": "^3.1.0",
            }
        }

        # Set workspaces based on package manager
        if config.package_manager == PackageManager.NPM:
            pkg["workspaces"] = ["packages/*"]
            pkg["scripts"]["build:all"] = "npm run build --workspaces --if-present"
            pkg["scripts"]["test:all"] = "npm run test --workspaces --if-present"
            pkg["scripts"]["lint:all"] = "npm run lint --workspaces --if-present"
            pkg["scripts"]["clean:all"] = "npm run clean --workspaces --if-present"
            pkg["scripts"]["dev:all"] = "npm run dev --workspaces --if-present"
        elif config.package_manager == PackageManager.YARN:
            pkg["workspaces"] = ["packages/*"]
            pkg["scripts"]["build:all"] = "yarn workspaces run build"
            pkg["scripts"]["test:all"] = "yarn workspaces run test"
            pkg["scripts"]["lint:all"] = "yarn workspaces run lint"
            pkg["scripts"]["clean:all"] = "yarn workspaces run clean"
            pkg["scripts"]["dev:all"] = "yarn workspaces run dev"
            pkg["packageManager"] = "yarn@4.0.0"
        else:  # pnpm
            pkg["scripts"]["build:all"] = "pnpm -r run build"
            pkg["scripts"]["test:all"] = "pnpm -r run test"
            pkg["scripts"]["lint:all"] = "pnpm -r run lint"
            pkg["scripts"]["clean:all"] = "pnpm -r run clean"
            pkg["scripts"]["dev:all"] = "pnpm -r run dev"

        # Add turborepo if enabled
        if config.include_turborepo:
            pkg["devDependencies"]["turbo"] = "^1.11.0"
            pkg["scripts"]["build"] = "turbo run build"
            pkg["scripts"]["test"] = "turbo run test"
            pkg["scripts"]["lint"] = "turbo run lint"
            pkg["scripts"]["dev"] = "turbo run dev"

        return pkg

    @staticmethod
    def pnpm_workspace_yaml(config: MonorepoConfig) -> str:
        """Generate pnpm-workspace.yaml"""
        return """packages:
  - 'packages/*'
"""

    @staticmethod
    def turbo_json(config: MonorepoConfig) -> Dict:
        """Generate turbo.json configuration"""
        return {
            "$schema": "https://turbo.build/schema.json",
            "globalDependencies": ["**/.env.*local"],
            "pipeline": {
                "build": {
                    "dependsOn": ["^build"],
                    "outputs": ["dist/**", ".next/**", "!.next/cache/**"]
                },
                "lint": {},
                "test": {
                    "dependsOn": ["build"]
                },
                "dev": {
                    "cache": False,
                    "persistent": True
                },
                "clean": {
                    "cache": False
                }
            }
        }

    @staticmethod
    def tsconfig_base() -> Dict:
        """Generate base TypeScript configuration"""
        return {
            "$schema": "https://json.schemastore.org/tsconfig",
            "display": "Default",
            "compilerOptions": {
                "composite": False,
                "declaration": True,
                "declarationMap": True,
                "esModuleInterop": True,
                "forceConsistentCasingInFileNames": True,
                "inlineSources": False,
                "isolatedModules": True,
                "moduleResolution": "node",
                "noUnusedLocals": False,
                "noUnusedParameters": False,
                "preserveWatchOutput": True,
                "skipLibCheck": True,
                "strict": True,
                "strictNullChecks": True
            },
            "exclude": ["node_modules"]
        }

    @staticmethod
    def tsconfig_package(package_name: str, references: List[str] = None) -> Dict:
        """Generate package-level TypeScript configuration"""
        config = {
            "extends": "../../tsconfig.base.json",
            "compilerOptions": {
                "outDir": "./dist",
                "rootDir": "./src",
                "module": "ESNext",
                "target": "ES2020",
                "lib": ["ES2020"]
            },
            "include": ["src/**/*"],
            "exclude": ["node_modules", "dist"]
        }

        if references:
            config["references"] = [{"path": f"../{ref}"} for ref in references]

        return config

    @staticmethod
    def eslint_config() -> Dict:
        """Generate ESLint configuration"""
        return {
            "root": True,
            "env": {
                "browser": True,
                "node": True,
                "es2022": True
            },
            "extends": [
                "eslint:recommended"
            ],
            "parserOptions": {
                "ecmaVersion": "latest",
                "sourceType": "module"
            },
            "rules": {
                "no-unused-vars": ["warn", {"argsIgnorePattern": "^_"}],
                "no-console": "warn"
            },
            "ignorePatterns": ["dist", "node_modules", "coverage"]
        }

    @staticmethod
    def prettier_config() -> Dict:
        """Generate Prettier configuration"""
        return {
            "semi": True,
            "trailingComma": "es5",
            "singleQuote": True,
            "printWidth": 100,
            "tabWidth": 2,
            "useTabs": False
        }

    @staticmethod
    def gitignore() -> str:
        """Generate .gitignore"""
        return """# Dependencies
node_modules/
.pnp
.pnp.js

# Build outputs
dist/
build/
.next/
out/

# Testing
coverage/
.nyc_output/

# IDE
.idea/
.vscode/
*.swp
*.swo

# Environment
.env
.env.local
.env.*.local

# Debug
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.pnpm-debug.log*

# Misc
.DS_Store
*.pem
Thumbs.db

# Turborepo
.turbo/

# Vercel
.vercel/
"""

    @staticmethod
    def package_package_json(
        name: str,
        full_name: str,
        description: str,
        is_shared: bool = False
    ) -> Dict:
        """Generate package-level package.json"""
        pkg = {
            "name": full_name,
            "version": "0.0.0",
            "description": description,
            "main": "./dist/index.js",
            "module": "./dist/index.mjs",
            "types": "./dist/index.d.ts",
            "files": ["dist"],
            "scripts": {
                "build": "tsc",
                "dev": "tsc --watch",
                "lint": "eslint src/",
                "test": "echo \"No tests yet\"",
                "clean": "rm -rf dist"
            },
            "devDependencies": {
                "typescript": "^5.3.0",
                "@types/node": "^20.10.0"
            }
        }

        if is_shared:
            pkg["exports"] = {
                ".": {
                    "types": "./dist/index.d.ts",
                    "import": "./dist/index.mjs",
                    "require": "./dist/index.js"
                }
            }

        return pkg

    @staticmethod
    def shared_index_ts() -> str:
        """Generate shared package index.ts"""
        return '''/**
 * Shared utilities and types for the monorepo
 */

// Re-export types
export * from './types';

// Re-export utilities
export * from './utils';

// Re-export constants
export * from './constants';
'''

    @staticmethod
    def shared_types_ts() -> str:
        """Generate shared types file"""
        return '''/**
 * Shared TypeScript types and interfaces
 */

/**
 * Generic API response wrapper
 */
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: {
    code: string;
    message: string;
  };
  meta?: {
    timestamp: string;
    requestId: string;
  };
}

/**
 * Pagination parameters
 */
export interface PaginationParams {
  page: number;
  limit: number;
  sortBy?: string;
  sortOrder?: 'asc' | 'desc';
}

/**
 * Paginated response
 */
export interface PaginatedResponse<T> extends ApiResponse<T[]> {
  pagination: {
    page: number;
    limit: number;
    total: number;
    totalPages: number;
  };
}

/**
 * User type (shared across packages)
 */
export interface User {
  id: string;
  email: string;
  name: string;
  createdAt: string;
  updatedAt: string;
}

/**
 * Environment configuration
 */
export interface EnvConfig {
  NODE_ENV: 'development' | 'production' | 'test';
  API_URL: string;
  DATABASE_URL?: string;
}
'''

    @staticmethod
    def shared_utils_ts() -> str:
        """Generate shared utils file"""
        return '''/**
 * Shared utility functions
 */

/**
 * Format a date to ISO string
 */
export function formatDate(date: Date): string {
  return date.toISOString();
}

/**
 * Generate a unique ID
 */
export function generateId(): string {
  return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
}

/**
 * Sleep for specified milliseconds
 */
export function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

/**
 * Deep clone an object
 */
export function deepClone<T>(obj: T): T {
  return JSON.parse(JSON.stringify(obj));
}

/**
 * Check if value is defined (not null or undefined)
 */
export function isDefined<T>(value: T | null | undefined): value is T {
  return value !== null && value !== undefined;
}

/**
 * Retry a function with exponential backoff
 */
export async function retry<T>(
  fn: () => Promise<T>,
  maxAttempts: number = 3,
  baseDelay: number = 1000
): Promise<T> {
  let lastError: Error | undefined;

  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error as Error;
      if (attempt < maxAttempts) {
        await sleep(baseDelay * Math.pow(2, attempt - 1));
      }
    }
  }

  throw lastError;
}
'''

    @staticmethod
    def shared_constants_ts() -> str:
        """Generate shared constants file"""
        return '''/**
 * Shared constants
 */

/**
 * HTTP status codes
 */
export const HTTP_STATUS = {
  OK: 200,
  CREATED: 201,
  NO_CONTENT: 204,
  BAD_REQUEST: 400,
  UNAUTHORIZED: 401,
  FORBIDDEN: 403,
  NOT_FOUND: 404,
  CONFLICT: 409,
  UNPROCESSABLE_ENTITY: 422,
  INTERNAL_SERVER_ERROR: 500,
} as const;

/**
 * Default pagination values
 */
export const PAGINATION_DEFAULTS = {
  PAGE: 1,
  LIMIT: 20,
  MAX_LIMIT: 100,
} as const;

/**
 * Date formats
 */
export const DATE_FORMATS = {
  ISO: 'yyyy-MM-dd',
  ISO_TIME: 'yyyy-MM-dd HH:mm:ss',
  DISPLAY: 'MMM dd, yyyy',
  DISPLAY_TIME: 'MMM dd, yyyy h:mm a',
} as const;

/**
 * Error codes
 */
export const ERROR_CODES = {
  VALIDATION_ERROR: 'VALIDATION_ERROR',
  NOT_FOUND: 'NOT_FOUND',
  UNAUTHORIZED: 'UNAUTHORIZED',
  FORBIDDEN: 'FORBIDDEN',
  INTERNAL_ERROR: 'INTERNAL_ERROR',
  RATE_LIMITED: 'RATE_LIMITED',
} as const;
'''

    @staticmethod
    def web_index_ts() -> str:
        """Generate web package index.ts"""
        return '''/**
 * Web application entry point
 */

console.log('Web application starting...');

// Import shared utilities
// import { formatDate, generateId } from '@{monorepo}/shared';

export function main(): void {
  console.log('Web app initialized');
}

main();
'''

    @staticmethod
    def api_index_ts() -> str:
        """Generate API package index.ts"""
        return '''/**
 * API server entry point
 */

console.log('API server starting...');

// Import shared utilities
// import { HTTP_STATUS, ERROR_CODES } from '@{monorepo}/shared';

export function main(): void {
  console.log('API server initialized');
  console.log('Listening on port 3001');
}

main();
'''

    @staticmethod
    def readme(config: MonorepoConfig) -> str:
        """Generate README.md"""
        pm = config.package_manager.value
        return f'''# {config.name}

A monorepo managed with {pm}{" and Turborepo" if config.include_turborepo else ""}.

## Structure

```
{config.name}/
├── packages/
│   ├── shared/     # Shared utilities and types
│   ├── web/        # Web application
│   └── api/        # API server
├── package.json
├── tsconfig.base.json
└── {"turbo.json" if config.include_turborepo else ".eslintrc.json"}
```

## Getting Started

### Prerequisites

- Node.js 18+
- {pm}

### Installation

```bash
# Install dependencies
{pm} install
```

### Development

```bash
# Start all packages in dev mode
{pm} run dev

# Build all packages
{pm} run build

# Run tests
{pm} run test

# Lint all packages
{pm} run lint
```

### Working with Packages

```bash
# Add a dependency to a specific package
{"cd packages/web && " + pm + " add react" if pm != "pnpm" else "pnpm add react --filter @" + config.name + "/web"}

# Run a script in a specific package
{"cd packages/api && " + pm + " run build" if pm != "pnpm" else "pnpm --filter @" + config.name + "/api run build"}
```

## Packages

| Package | Description |
|---------|-------------|
| `@{config.name}/shared` | Shared utilities, types, and constants |
| `@{config.name}/web` | Web application |
| `@{config.name}/api` | API server |

## License

MIT
'''


# =============================================================================
# Main Scaffolder Class
# =============================================================================

class ProjectScaffolder:
    """Monorepo project scaffolder"""

    DEFAULT_PACKAGES = ['shared', 'web', 'api']

    def __init__(self, config: MonorepoConfig, verbose: bool = False):
        if verbose:
            logging.getLogger().setLevel(logging.DEBUG)

        self.config = config
        self.verbose = verbose
        self.files_created: List[str] = []

        logger.debug("ProjectScaffolder initialized")

    def run(self) -> Dict:
        """Execute the scaffolding"""
        logger.debug("Starting scaffolding run")
        if self.verbose:
            print(f"Creating monorepo: {self.config.name}", file=sys.stderr)
            print(f"Output: {self.config.output_path}", file=sys.stderr)
            print(f"Package manager: {self.config.package_manager.value}", file=sys.stderr)

        # Create directory structure
        self._create_directories()

        # Generate root files
        self._create_root_files()

        # Generate package files
        for package in self.config.packages:
            self._create_package(package)

        # Build results
        return self._build_results()

    def _create_directories(self):
        """Create the directory structure"""
        logger.debug("Creating directory structure")
        root = self.config.output_path

        # Create root directory
        root.mkdir(parents=True, exist_ok=True)

        # Create packages directory
        packages_dir = root / 'packages'
        packages_dir.mkdir(exist_ok=True)

        # Create each package directory
        for package in self.config.packages:
            pkg_dir = packages_dir / package
            pkg_dir.mkdir(exist_ok=True)
            (pkg_dir / 'src').mkdir(exist_ok=True)

        if self.verbose:
            print(f"Created directory structure", file=sys.stderr)

    def _create_root_files(self):
        """Create root-level configuration files"""
        root = self.config.output_path

        # package.json
        self._write_json(
            root / 'package.json',
            Templates.root_package_json(self.config)
        )

        # pnpm-workspace.yaml (if pnpm)
        if self.config.package_manager == PackageManager.PNPM:
            self._write_file(
                root / 'pnpm-workspace.yaml',
                Templates.pnpm_workspace_yaml(self.config)
            )

        # turbo.json (if turborepo)
        if self.config.include_turborepo:
            self._write_json(
                root / 'turbo.json',
                Templates.turbo_json(self.config)
            )

        # tsconfig.base.json
        self._write_json(
            root / 'tsconfig.base.json',
            Templates.tsconfig_base()
        )

        # .eslintrc.json
        self._write_json(
            root / '.eslintrc.json',
            Templates.eslint_config()
        )

        # .prettierrc
        self._write_json(
            root / '.prettierrc',
            Templates.prettier_config()
        )

        # .gitignore
        self._write_file(
            root / '.gitignore',
            Templates.gitignore()
        )

        # README.md
        self._write_file(
            root / 'README.md',
            Templates.readme(self.config)
        )

        if self.verbose:
            print(f"Created root configuration files", file=sys.stderr)

    def _create_package(self, package_name: str):
        """Create a package with its files"""
        logger.debug(f"Creating package: {package_name}")
        pkg_dir = self.config.output_path / 'packages' / package_name
        full_name = f"@{self.config.name}/{package_name}"
        is_shared = package_name == 'shared'

        # Determine dependencies on shared package
        references = ['shared'] if not is_shared and 'shared' in self.config.packages else []

        # Description based on package type
        descriptions = {
            'shared': 'Shared utilities, types, and constants',
            'web': 'Web application',
            'api': 'API server',
            'config': 'Shared configuration packages',
        }
        description = descriptions.get(package_name, f'{package_name} package')

        # package.json
        self._write_json(
            pkg_dir / 'package.json',
            Templates.package_package_json(package_name, full_name, description, is_shared)
        )

        # tsconfig.json
        self._write_json(
            pkg_dir / 'tsconfig.json',
            Templates.tsconfig_package(package_name, references)
        )

        # Create source files based on package type
        src_dir = pkg_dir / 'src'

        if package_name == 'shared':
            self._write_file(src_dir / 'index.ts', Templates.shared_index_ts())
            self._write_file(src_dir / 'types.ts', Templates.shared_types_ts())
            self._write_file(src_dir / 'utils.ts', Templates.shared_utils_ts())
            self._write_file(src_dir / 'constants.ts', Templates.shared_constants_ts())
        elif package_name == 'web':
            content = Templates.web_index_ts().replace('{monorepo}', self.config.name)
            self._write_file(src_dir / 'index.ts', content)
        elif package_name == 'api':
            content = Templates.api_index_ts().replace('{monorepo}', self.config.name)
            self._write_file(src_dir / 'index.ts', content)
        else:
            # Generic package
            self._write_file(
                src_dir / 'index.ts',
                f'// {package_name} package\nexport const name = "{package_name}";\n'
            )

        if self.verbose:
            print(f"Created package: {package_name}", file=sys.stderr)

    def _write_file(self, path: Path, content: str):
        """Write content to a file"""
        with open(path, 'w') as f:
            f.write(content)
        self.files_created.append(str(path.relative_to(self.config.output_path)))

    def _write_json(self, path: Path, data: Dict):
        """Write JSON data to a file"""
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
            f.write('\n')
        self.files_created.append(str(path.relative_to(self.config.output_path)))

    def _build_results(self) -> Dict:
        """Build the results dictionary"""
        next_steps = [
            f"cd {self.config.output_path}",
            f"{self.config.package_manager.value} install",
            f"{self.config.package_manager.value} run build",
            f"{self.config.package_manager.value} run dev",
        ]

        if self.config.include_turborepo:
            next_steps.insert(2, "npx turbo login  # (optional) Enable remote caching")

        return {
            'timestamp': datetime.now().isoformat(),
            'monorepo_name': self.config.name,
            'output_path': str(self.config.output_path),
            'configuration': {
                'package_manager': self.config.package_manager.value,
                'packages': self.config.packages,
                'turborepo': self.config.include_turborepo,
            },
            'files_created': self.files_created,
            'stats': {
                'total_files': len(self.files_created),
                'packages': len(self.config.packages),
            },
            'next_steps': next_steps,
        }


# =============================================================================
# Output Formatting
# =============================================================================

class OutputFormatter:
    """Format scaffolding results for output"""

    @staticmethod
    def format_text(results: Dict) -> str:
        """Format results as human-readable text"""
        lines = []
        lines.append("=" * 60)
        lines.append("MONOREPO SCAFFOLDING COMPLETE")
        lines.append("=" * 60)
        lines.append(f"Timestamp: {results['timestamp']}")
        lines.append(f"Name: {results['monorepo_name']}")
        lines.append(f"Location: {results['output_path']}")
        lines.append("")

        # Configuration
        config = results['configuration']
        lines.append("CONFIGURATION")
        lines.append("-" * 40)
        lines.append(f"  Package Manager: {config['package_manager']}")
        lines.append(f"  Packages: {', '.join(config['packages'])}")
        lines.append(f"  Turborepo: {'Yes' if config['turborepo'] else 'No'}")
        lines.append("")

        # Stats
        stats = results['stats']
        lines.append("STATISTICS")
        lines.append("-" * 40)
        lines.append(f"  Files Created: {stats['total_files']}")
        lines.append(f"  Packages: {stats['packages']}")
        lines.append("")

        # Files
        lines.append("FILES CREATED")
        lines.append("-" * 40)
        for f in results['files_created'][:20]:
            lines.append(f"  {f}")
        if len(results['files_created']) > 20:
            lines.append(f"  ... and {len(results['files_created']) - 20} more")
        lines.append("")

        # Next steps
        lines.append("NEXT STEPS")
        lines.append("-" * 40)
        for i, step in enumerate(results['next_steps'], 1):
            lines.append(f"  {i}. {step}")
        lines.append("")

        lines.append("=" * 60)
        return "\n".join(lines)

    @staticmethod
    def format_json(results: Dict) -> str:
        """Format results as JSON"""
        return json.dumps(results, indent=2)


# =============================================================================
# CLI Entry Point
# =============================================================================

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Project Scaffolder - Monorepo structure generator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create a basic monorepo with pnpm
  %(prog)s --output ./my-project --name my-project

  # Create with npm and custom packages
  %(prog)s --output ./app --name app --manager npm --packages shared,frontend,backend

  # Create with Turborepo
  %(prog)s --output ./turbo-app --name turbo-app --turborepo

  # Create with yarn and verbose output
  %(prog)s --output ./yarn-mono --name yarn-mono --manager yarn -v

Package Managers:
  - npm: Native npm workspaces
  - yarn: Yarn workspaces (v4+)
  - pnpm: pnpm workspaces (recommended)

Default Packages:
  - shared: Shared utilities, types, and constants
  - web: Web application package
  - api: API server package

Features:
  - Workspace configuration for chosen package manager
  - TypeScript configuration with project references
  - ESLint and Prettier setup
  - Optional Turborepo integration for faster builds
  - Shared package with common utilities and types
        """
    )

    parser.add_argument(
        '--output', '-o',
        required=True,
        help='Output directory for the monorepo'
    )

    parser.add_argument(
        '--name', '-n',
        required=True,
        help='Name of the monorepo (used in package names)'
    )

    parser.add_argument(
        '--packages', '-p',
        default='shared,web,api',
        help='Comma-separated list of packages to create (default: shared,web,api)'
    )

    parser.add_argument(
        '--manager', '-m',
        choices=['npm', 'yarn', 'pnpm'],
        default='pnpm',
        help='Package manager to use (default: pnpm)'
    )

    parser.add_argument(
        '--turborepo',
        action='store_true',
        help='Include Turborepo configuration'
    )

    parser.add_argument(
        '--format',
        choices=['text', 'json'],
        default='text',
        help='Output format (default: text)'
    )

    parser.add_argument(
        '--file', '-f',
        help='Write output to file instead of stdout'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )

    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )

    args = parser.parse_args()

    # Parse package manager
    pm_map = {
        'npm': PackageManager.NPM,
        'yarn': PackageManager.YARN,
        'pnpm': PackageManager.PNPM,
    }
    package_manager = pm_map[args.manager]

    # Parse packages
    packages = [p.strip() for p in args.packages.split(',') if p.strip()]
    if not packages:
        packages = ProjectScaffolder.DEFAULT_PACKAGES

    # Validate output path
    output_path = Path(args.output).resolve()
    if output_path.exists() and any(output_path.iterdir()):
        print(f"Warning: Output directory is not empty: {output_path}", file=sys.stderr)
        # Continue anyway - will overwrite

    # Create configuration
    config = MonorepoConfig(
        name=args.name,
        package_manager=package_manager,
        packages=packages,
        include_turborepo=args.turborepo,
        output_path=output_path,
    )

    try:
        # Run scaffolding
        scaffolder = ProjectScaffolder(config, verbose=args.verbose)
        results = scaffolder.run()

        # Format output
        formatter = OutputFormatter()
        if args.format == 'json':
            output_text = formatter.format_json(results)
        else:
            output_text = formatter.format_text(results)

        # Write output
        if args.file:
            with open(args.file, 'w') as f:
                f.write(output_text)
            if args.verbose:
                print(f"Results saved to: {args.file}", file=sys.stderr)
        else:
            print(output_text)

        sys.exit(0)

    except KeyboardInterrupt:
        print("\nScaffolding interrupted", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
