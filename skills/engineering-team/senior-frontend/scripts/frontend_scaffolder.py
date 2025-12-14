#!/usr/bin/env python3
"""
Frontend Scaffolder - Generate production-ready frontend projects.

Scaffolds complete frontend projects with:
- Next.js 14+ (App Router), Vite + React, or Nuxt 3
- TypeScript configuration
- Tailwind CSS / CSS Modules styling
- State management (Zustand, Pinia)
- Testing setup (Jest/Vitest + Testing Library)
- Docker configuration
- CI/CD (GitHub Actions)
- ESLint + Prettier

Uses Python standard library only - no external dependencies required.
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
from typing import Any, Dict, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ProjectFramework(Enum):
    """Supported frontend frameworks."""
    NEXTJS = "nextjs"
    VITE_REACT = "vite-react"
    NUXT = "nuxt"


class StateManagement(Enum):
    """State management options."""
    ZUSTAND = "zustand"
    PINIA = "pinia"
    REDUX = "redux"
    JOTAI = "jotai"
    NONE = "none"


class Styling(Enum):
    """Styling approaches."""
    TAILWIND = "tailwind"
    CSS_MODULES = "css-modules"


class PackageManager(Enum):
    """Package managers."""
    NPM = "npm"
    YARN = "yarn"
    PNPM = "pnpm"


@dataclass
class ProjectConfig:
    """Configuration for project scaffolding."""
    name: str
    framework: ProjectFramework
    output_dir: Path
    styling: Styling = Styling.TAILWIND
    state_management: StateManagement = StateManagement.ZUSTAND
    package_manager: PackageManager = PackageManager.NPM
    include_auth: bool = False
    include_testing: bool = True
    include_storybook: bool = False
    include_docker: bool = True
    include_ci: bool = True
    include_husky: bool = True
    verbose: bool = False
    dry_run: bool = False


@dataclass
class ScaffoldingResult:
    """Result of project scaffolding."""
    project_name: str
    framework: str
    output_path: str
    directories_created: List[str]
    files_created: List[str]
    total_files: int
    success: bool
    timestamp: str
    next_steps: List[str]
    errors: List[str] = field(default_factory=list)


class FrontendScaffolder:
    """
    Complete frontend project scaffolding tool.

    Generates production-ready projects with:
    - Next.js 14+ (App Router)
    - Vite + React 18
    - Nuxt 3

    Includes:
    - TypeScript configuration
    - Tailwind CSS / CSS Modules
    - State management (Zustand/Pinia)
    - Testing (Jest/Vitest + Testing Library)
    - Docker configuration
    - CI/CD (GitHub Actions)
    - Husky + lint-staged
    - ESLint + Prettier
    """

    def __init__(self, config: ProjectConfig):
        if config.verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("FrontendScaffolder initialized")

        self.config = config
        self.files_created: List[str] = []
        self.directories_created: List[str] = []
        self.errors: List[str] = []

    def scaffold(self) -> ScaffoldingResult:
        """Execute complete project scaffolding."""
        logger.debug(f"Scaffolding {self.config.framework.value} project: {self.config.name}")
        if self.config.verbose:
            print(f"Scaffolding {self.config.framework.value} project: {self.config.name}")

        project_dir = self.config.output_dir / self.config.name

        try:
            # Create base directory structure
            self._create_directory_structure(project_dir)

            # Generate framework-specific files
            if self.config.framework == ProjectFramework.NEXTJS:
                self._scaffold_nextjs(project_dir)
            elif self.config.framework == ProjectFramework.VITE_REACT:
                self._scaffold_vite_react(project_dir)
            elif self.config.framework == ProjectFramework.NUXT:
                self._scaffold_nuxt(project_dir)

            # Generate shared configuration files
            self._create_package_json(project_dir)
            self._create_tsconfig(project_dir)
            self._create_eslint_config(project_dir)
            self._create_prettier_config(project_dir)
            self._create_gitignore(project_dir)
            self._create_env_files(project_dir)

            # Generate styling configuration
            if self.config.styling == Styling.TAILWIND:
                self._create_tailwind_config(project_dir)

            # Generate optional components
            if self.config.include_testing:
                self._create_testing_config(project_dir)

            if self.config.include_docker:
                self._create_docker_files(project_dir)

            if self.config.include_ci:
                self._create_github_actions(project_dir)

            if self.config.include_husky:
                self._create_husky_config(project_dir)

            # Create base components
            self._create_base_components(project_dir)

            # Create utility files
            self._create_utils(project_dir)

            # Create state management
            if self.config.state_management != StateManagement.NONE:
                self._create_state_store(project_dir)

            # Create README
            self._create_readme(project_dir)

        except Exception as e:
            logger.error(f"Scaffolding failed: {e}")
            self.errors.append(str(e))

        # Generate next steps
        next_steps = self._get_next_steps()

        return ScaffoldingResult(
            project_name=self.config.name,
            framework=self.config.framework.value,
            output_path=str(project_dir),
            directories_created=self.directories_created,
            files_created=self.files_created,
            total_files=len(self.files_created),
            success=len(self.errors) == 0,
            timestamp=datetime.now().isoformat(),
            next_steps=next_steps,
            errors=self.errors,
        )

    def _create_directory_structure(self, project_dir: Path) -> None:
        """Create base directory structure."""
        logger.debug(f"Creating directory structure for {self.config.framework.value}")
        if self.config.framework == ProjectFramework.NEXTJS:
            dirs = [
                "app",
                "app/api",
                "components/ui",
                "components/layouts",
                "lib",
                "hooks",
                "types",
                "public",
            ]
        elif self.config.framework == ProjectFramework.VITE_REACT:
            dirs = [
                "src",
                "src/components/ui",
                "src/components/layouts",
                "src/lib",
                "src/hooks",
                "src/pages",
                "src/types",
                "public",
            ]
        else:  # Nuxt
            dirs = [
                "components",
                "composables",
                "layouts",
                "pages",
                "plugins",
                "public",
                "types",
                "utils",
            ]

        # Add common directories
        dirs.extend([
            "tests",
            ".github/workflows",
        ])

        if self.config.include_docker:
            dirs.append(".docker")

        if self.config.state_management != StateManagement.NONE:
            if self.config.framework == ProjectFramework.VITE_REACT:
                dirs.append("src/stores")
            elif self.config.framework == ProjectFramework.NEXTJS:
                dirs.append("stores")
            else:
                dirs.append("stores")

        for dir_path in dirs:
            full_path = project_dir / dir_path
            if not self.config.dry_run:
                full_path.mkdir(parents=True, exist_ok=True)
            self.directories_created.append(dir_path)
            if self.config.verbose:
                print(f"  Created directory: {dir_path}")

        if not dirs:
            logger.warning("No directories to create")

    def _write_file(self, project_dir: Path, relative_path: str, content: str) -> None:
        """Write a file to the project."""
        logger.debug(f"Writing file: {relative_path}")
        file_path = project_dir / relative_path

        if not self.config.dry_run:
            try:
                file_path.parent.mkdir(parents=True, exist_ok=True)
                with open(file_path, 'w') as f:
                    f.write(content)
            except IOError as e:
                logger.error(f"Failed to write {relative_path}: {e}")
                raise

        self.files_created.append(relative_path)
        if self.config.verbose:
            print(f"  Created file: {relative_path}")

    def _scaffold_nextjs(self, project_dir: Path) -> None:
        """Scaffold Next.js 14 App Router project."""
        # app/layout.tsx
        layout_content = '''import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: '%s',
  description: 'A modern Next.js application',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  );
}
''' % self.config.name
        self._write_file(project_dir, "app/layout.tsx", layout_content)

        # app/page.tsx
        page_content = '''export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <h1 className="text-4xl font-bold">Welcome to %s</h1>
      <p className="mt-4 text-lg text-gray-600">
        Built with Next.js 14, TypeScript, and Tailwind CSS
      </p>
    </main>
  );
}
''' % self.config.name
        self._write_file(project_dir, "app/page.tsx", page_content)

        # app/globals.css
        globals_css = '''@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --foreground-rgb: 0, 0, 0;
  --background-rgb: 255, 255, 255;
}

@media (prefers-color-scheme: dark) {
  :root {
    --foreground-rgb: 255, 255, 255;
    --background-rgb: 0, 0, 0;
  }
}

body {
  color: rgb(var(--foreground-rgb));
  background: rgb(var(--background-rgb));
}
'''
        self._write_file(project_dir, "app/globals.css", globals_css)

        # app/api/health/route.ts
        api_health = '''import { NextResponse } from 'next/server';

export async function GET() {
  return NextResponse.json({
    status: 'ok',
    timestamp: new Date().toISOString(),
  });
}
'''
        self._write_file(project_dir, "app/api/health/route.ts", api_health)

        # next.config.js
        next_config = '''/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // Enable experimental features as needed
  // experimental: {},
};

module.exports = nextConfig;
'''
        self._write_file(project_dir, "next.config.js", next_config)

    def _scaffold_vite_react(self, project_dir: Path) -> None:
        """Scaffold Vite + React project."""
        # src/main.tsx
        main_content = '''import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
'''
        self._write_file(project_dir, "src/main.tsx", main_content)

        # src/App.tsx
        app_content = '''function App() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-900">Welcome to %s</h1>
        <p className="mt-4 text-lg text-gray-600">
          Built with Vite, React, TypeScript, and Tailwind CSS
        </p>
      </div>
    </div>
  );
}

export default App;
''' % self.config.name
        self._write_file(project_dir, "src/App.tsx", app_content)

        # src/index.css
        index_css = '''@tailwind base;
@tailwind components;
@tailwind utilities;
'''
        self._write_file(project_dir, "src/index.css", index_css)

        # src/vite-env.d.ts
        vite_env = '''/// <reference types="vite/client" />
'''
        self._write_file(project_dir, "src/vite-env.d.ts", vite_env)

        # index.html
        index_html = '''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>%s</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
''' % self.config.name
        self._write_file(project_dir, "index.html", index_html)

        # vite.config.ts
        vite_config = '''import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 3000,
  },
});
'''
        self._write_file(project_dir, "vite.config.ts", vite_config)

    def _scaffold_nuxt(self, project_dir: Path) -> None:
        """Scaffold Nuxt 3 project."""
        # app.vue
        app_vue = '''<template>
  <NuxtLayout>
    <NuxtPage />
  </NuxtLayout>
</template>
'''
        self._write_file(project_dir, "app.vue", app_vue)

        # pages/index.vue
        index_vue = '''<script setup lang="ts">
useHead({
  title: '%s',
});
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100">
    <div class="text-center">
      <h1 class="text-4xl font-bold text-gray-900">Welcome to %s</h1>
      <p class="mt-4 text-lg text-gray-600">
        Built with Nuxt 3, Vue 3, TypeScript, and Tailwind CSS
      </p>
    </div>
  </div>
</template>
''' % (self.config.name, self.config.name)
        self._write_file(project_dir, "pages/index.vue", index_vue)

        # layouts/default.vue
        default_layout = '''<template>
  <div>
    <slot />
  </div>
</template>
'''
        self._write_file(project_dir, "layouts/default.vue", default_layout)

        # nuxt.config.ts
        nuxt_config = '''export default defineNuxtConfig({
  devtools: { enabled: true },
  css: ['~/assets/css/main.css'],
  postcss: {
    plugins: {
      tailwindcss: {},
      autoprefixer: {},
    },
  },
  modules: [
    '@pinia/nuxt',
  ],
});
'''
        self._write_file(project_dir, "nuxt.config.ts", nuxt_config)

        # assets/css/main.css
        main_css = '''@tailwind base;
@tailwind components;
@tailwind utilities;
'''
        self._write_file(project_dir, "assets/css/main.css", main_css)

    def _create_package_json(self, project_dir: Path) -> None:
        """Generate package.json with appropriate dependencies."""
        name = self.config.name.lower().replace(" ", "-")

        # Base dependencies
        deps: Dict[str, str] = {}
        dev_deps: Dict[str, str] = {
            "typescript": "^5.3.3",
            "@types/node": "^20.10.0",
            "prettier": "^3.1.0",
            "eslint": "^8.55.0",
        }

        scripts: Dict[str, str] = {}

        # Framework-specific configuration
        if self.config.framework == ProjectFramework.NEXTJS:
            deps.update({
                "next": "^14.0.4",
                "react": "^18.2.0",
                "react-dom": "^18.2.0",
            })
            dev_deps.update({
                "@types/react": "^18.2.0",
                "@types/react-dom": "^18.2.0",
                "eslint-config-next": "^14.0.4",
            })
            scripts.update({
                "dev": "next dev",
                "build": "next build",
                "start": "next start",
                "lint": "next lint",
            })

        elif self.config.framework == ProjectFramework.VITE_REACT:
            deps.update({
                "react": "^18.2.0",
                "react-dom": "^18.2.0",
            })
            dev_deps.update({
                "@types/react": "^18.2.0",
                "@types/react-dom": "^18.2.0",
                "@vitejs/plugin-react": "^4.2.1",
                "vite": "^5.0.0",
                "eslint-plugin-react-hooks": "^4.6.0",
                "eslint-plugin-react-refresh": "^0.4.5",
            })
            scripts.update({
                "dev": "vite",
                "build": "tsc && vite build",
                "preview": "vite preview",
                "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
            })

        else:  # Nuxt
            dev_deps.update({
                "nuxt": "^3.9.0",
                "vue": "^3.4.0",
                "@pinia/nuxt": "^0.5.1",
                "pinia": "^2.1.7",
            })
            scripts.update({
                "dev": "nuxt dev",
                "build": "nuxt build",
                "generate": "nuxt generate",
                "preview": "nuxt preview",
                "lint": "eslint .",
            })

        # Styling dependencies
        if self.config.styling == Styling.TAILWIND:
            dev_deps.update({
                "tailwindcss": "^3.4.0",
                "postcss": "^8.4.32",
                "autoprefixer": "^10.4.16",
            })

        # State management
        if self.config.state_management == StateManagement.ZUSTAND:
            deps["zustand"] = "^4.4.7"
        elif self.config.state_management == StateManagement.REDUX:
            deps.update({
                "@reduxjs/toolkit": "^2.0.1",
                "react-redux": "^9.0.4",
            })
        elif self.config.state_management == StateManagement.JOTAI:
            deps["jotai"] = "^2.6.0"
        elif self.config.state_management == StateManagement.PINIA:
            if self.config.framework != ProjectFramework.NUXT:
                deps["pinia"] = "^2.1.7"

        # Testing dependencies
        if self.config.include_testing:
            dev_deps.update({
                "@testing-library/jest-dom": "^6.1.5",
            })
            if self.config.framework == ProjectFramework.VITE_REACT:
                dev_deps.update({
                    "vitest": "^1.1.0",
                    "@testing-library/react": "^14.1.2",
                    "jsdom": "^23.0.1",
                })
                scripts["test"] = "vitest"
                scripts["test:coverage"] = "vitest run --coverage"
            else:
                dev_deps.update({
                    "jest": "^29.7.0",
                    "@testing-library/react": "^14.1.2",
                    "jest-environment-jsdom": "^29.7.0",
                })
                scripts["test"] = "jest"
                scripts["test:coverage"] = "jest --coverage"

        # Husky
        if self.config.include_husky:
            dev_deps.update({
                "husky": "^8.0.3",
                "lint-staged": "^15.2.0",
            })
            scripts["prepare"] = "husky install"

        # Common scripts
        scripts.update({
            "format": "prettier --write .",
            "format:check": "prettier --check .",
            "typecheck": "tsc --noEmit",
        })

        package_json = {
            "name": name,
            "version": "0.1.0",
            "private": True,
            "scripts": scripts,
            "dependencies": deps,
            "devDependencies": dev_deps,
        }

        # Lint-staged config
        if self.config.include_husky:
            package_json["lint-staged"] = {
                "*.{js,jsx,ts,tsx}": ["eslint --fix", "prettier --write"],
                "*.{json,md,css,scss}": ["prettier --write"],
            }

        content = json.dumps(package_json, indent=2)
        self._write_file(project_dir, "package.json", content)

    def _create_tsconfig(self, project_dir: Path) -> None:
        """Generate TypeScript configuration."""
        if self.config.framework == ProjectFramework.NEXTJS:
            tsconfig = {
                "compilerOptions": {
                    "target": "ES2017",
                    "lib": ["dom", "dom.iterable", "esnext"],
                    "allowJs": True,
                    "skipLibCheck": True,
                    "strict": True,
                    "noEmit": True,
                    "esModuleInterop": True,
                    "module": "esnext",
                    "moduleResolution": "bundler",
                    "resolveJsonModule": True,
                    "isolatedModules": True,
                    "jsx": "preserve",
                    "incremental": True,
                    "plugins": [{"name": "next"}],
                    "paths": {
                        "@/*": ["./*"]
                    }
                },
                "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
                "exclude": ["node_modules"]
            }
        elif self.config.framework == ProjectFramework.VITE_REACT:
            tsconfig = {
                "compilerOptions": {
                    "target": "ES2020",
                    "useDefineForClassFields": True,
                    "lib": ["ES2020", "DOM", "DOM.Iterable"],
                    "module": "ESNext",
                    "skipLibCheck": True,
                    "moduleResolution": "bundler",
                    "allowImportingTsExtensions": True,
                    "resolveJsonModule": True,
                    "isolatedModules": True,
                    "noEmit": True,
                    "jsx": "react-jsx",
                    "strict": True,
                    "noUnusedLocals": True,
                    "noUnusedParameters": True,
                    "noFallthroughCasesInSwitch": True,
                    "paths": {
                        "@/*": ["./src/*"]
                    }
                },
                "include": ["src"],
                "references": [{"path": "./tsconfig.node.json"}]
            }

            # Also create tsconfig.node.json for Vite
            tsconfig_node = {
                "compilerOptions": {
                    "composite": True,
                    "skipLibCheck": True,
                    "module": "ESNext",
                    "moduleResolution": "bundler",
                    "allowSyntheticDefaultImports": True
                },
                "include": ["vite.config.ts"]
            }
            self._write_file(project_dir, "tsconfig.node.json", json.dumps(tsconfig_node, indent=2))
        else:  # Nuxt
            tsconfig = {
                "extends": "./.nuxt/tsconfig.json"
            }

        content = json.dumps(tsconfig, indent=2)
        self._write_file(project_dir, "tsconfig.json", content)

    def _create_tailwind_config(self, project_dir: Path) -> None:
        """Generate Tailwind CSS configuration."""
        if self.config.framework == ProjectFramework.NEXTJS:
            content_paths = [
                "./pages/**/*.{js,ts,jsx,tsx,mdx}",
                "./components/**/*.{js,ts,jsx,tsx,mdx}",
                "./app/**/*.{js,ts,jsx,tsx,mdx}",
            ]
        elif self.config.framework == ProjectFramework.VITE_REACT:
            content_paths = [
                "./index.html",
                "./src/**/*.{js,ts,jsx,tsx}",
            ]
        else:  # Nuxt
            content_paths = [
                "./components/**/*.{js,vue,ts}",
                "./layouts/**/*.vue",
                "./pages/**/*.vue",
                "./plugins/**/*.{js,ts}",
                "./app.vue",
            ]

        config = '''/** @type {import('tailwindcss').Config} */
module.exports = {
  content: %s,
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          100: '#dbeafe',
          200: '#bfdbfe',
          300: '#93c5fd',
          400: '#60a5fa',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
          800: '#1e40af',
          900: '#1e3a8a',
        },
      },
    },
  },
  plugins: [],
};
''' % json.dumps(content_paths, indent=4)

        self._write_file(project_dir, "tailwind.config.js", config)

        # postcss.config.js
        postcss_config = '''module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
};
'''
        self._write_file(project_dir, "postcss.config.js", postcss_config)

    def _create_eslint_config(self, project_dir: Path) -> None:
        """Generate ESLint configuration."""
        if self.config.framework == ProjectFramework.NEXTJS:
            config = {
                "extends": ["next/core-web-vitals", "prettier"],
                "rules": {
                    "no-console": "warn",
                    "no-unused-vars": "off",
                    "@typescript-eslint/no-unused-vars": "error"
                }
            }
        elif self.config.framework == ProjectFramework.VITE_REACT:
            config = {
                "root": True,
                "env": {"browser": True, "es2020": True},
                "extends": [
                    "eslint:recommended",
                    "plugin:@typescript-eslint/recommended",
                    "plugin:react-hooks/recommended",
                    "prettier"
                ],
                "ignorePatterns": ["dist", ".eslintrc.cjs"],
                "parser": "@typescript-eslint/parser",
                "plugins": ["react-refresh"],
                "rules": {
                    "react-refresh/only-export-components": ["warn", {"allowConstantExport": True}]
                }
            }
        else:  # Nuxt
            config = {
                "extends": ["@nuxt/eslint-config", "prettier"],
                "rules": {
                    "no-console": "warn"
                }
            }

        content = json.dumps(config, indent=2)
        self._write_file(project_dir, ".eslintrc.json", content)

    def _create_prettier_config(self, project_dir: Path) -> None:
        """Generate Prettier configuration."""
        config = {
            "semi": True,
            "singleQuote": True,
            "tabWidth": 2,
            "trailingComma": "es5",
            "printWidth": 100,
            "bracketSpacing": True,
            "arrowParens": "always",
            "endOfLine": "lf"
        }

        content = json.dumps(config, indent=2)
        self._write_file(project_dir, ".prettierrc", content)

        # .prettierignore
        ignore = '''node_modules
.next
dist
build
.nuxt
coverage
'''
        self._write_file(project_dir, ".prettierignore", ignore)

    def _create_gitignore(self, project_dir: Path) -> None:
        """Generate .gitignore file."""
        content = '''# Dependencies
node_modules
.pnp
.pnp.js

# Testing
coverage

# Next.js
.next/
out/

# Nuxt
.nuxt/
.output/

# Vite
dist/

# Production
build

# Misc
.DS_Store
*.pem

# Debug
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.pnpm-debug.log*

# Local env files
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# Vercel
.vercel

# TypeScript
*.tsbuildinfo
next-env.d.ts

# IDE
.idea
.vscode
*.swp
*.swo

# Husky
.husky/_
'''
        self._write_file(project_dir, ".gitignore", content)

    def _create_env_files(self, project_dir: Path) -> None:
        """Generate environment files."""
        env_example = '''# App Configuration
NEXT_PUBLIC_APP_NAME=%s
NEXT_PUBLIC_APP_URL=http://localhost:3000

# API Configuration
# API_URL=https://api.example.com
# API_KEY=your-api-key-here

# Database (if needed)
# DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# Authentication (if needed)
# AUTH_SECRET=your-secret-key-here
''' % self.config.name

        self._write_file(project_dir, ".env.example", env_example)
        self._write_file(project_dir, ".env.local", "# Local environment variables\n")

    def _create_testing_config(self, project_dir: Path) -> None:
        """Generate testing configuration."""
        if self.config.framework == ProjectFramework.VITE_REACT:
            # vitest.config.ts
            vitest_config = '''import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./tests/setup.ts'],
  },
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
});
'''
            self._write_file(project_dir, "vitest.config.ts", vitest_config)
        else:
            # jest.config.js
            jest_config = '''const nextJest = require('next/jest');

const createJestConfig = nextJest({
  dir: './',
});

const customJestConfig = {
  setupFilesAfterEnv: ['<rootDir>/tests/setup.ts'],
  testEnvironment: 'jest-environment-jsdom',
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/$1',
  },
};

module.exports = createJestConfig(customJestConfig);
'''
            self._write_file(project_dir, "jest.config.js", jest_config)

        # tests/setup.ts
        setup_content = '''import '@testing-library/jest-dom';

// Add any global test setup here
'''
        self._write_file(project_dir, "tests/setup.ts", setup_content)

        # Sample test file
        if self.config.framework == ProjectFramework.NEXTJS:
            test_file = '''import { render, screen } from '@testing-library/react';
import Home from '@/app/page';

describe('Home', () => {
  it('renders the welcome message', () => {
    render(<Home />);
    expect(screen.getByText(/Welcome to/i)).toBeInTheDocument();
  });
});
'''
            self._write_file(project_dir, "tests/app/page.test.tsx", test_file)
        elif self.config.framework == ProjectFramework.VITE_REACT:
            test_file = '''import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import App from '@/App';

describe('App', () => {
  it('renders the welcome message', () => {
    render(<App />);
    expect(screen.getByText(/Welcome to/i)).toBeInTheDocument();
  });
});
'''
            self._write_file(project_dir, "tests/App.test.tsx", test_file)

    def _create_docker_files(self, project_dir: Path) -> None:
        """Generate Docker configuration."""
        if self.config.framework == ProjectFramework.NEXTJS:
            dockerfile = '''FROM node:20-alpine AS base

# Install dependencies only when needed
FROM base AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm ci

# Rebuild the source code only when needed
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .

RUN npm run build

# Production image
FROM base AS runner
WORKDIR /app

ENV NODE_ENV production

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT 3000
ENV HOSTNAME "0.0.0.0"

CMD ["node", "server.js"]
'''
        else:
            dockerfile = '''FROM node:20-alpine AS base

WORKDIR /app

# Install dependencies
COPY package.json package-lock.json* ./
RUN npm ci

# Copy source files
COPY . .

# Build the application
RUN npm run build

# Production stage
FROM nginx:alpine AS production
COPY --from=base /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
'''

        self._write_file(project_dir, "Dockerfile", dockerfile)

        # docker-compose.yml
        compose = '''version: '3.8'

services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
    restart: unless-stopped
'''
        self._write_file(project_dir, "docker-compose.yml", compose)

        # .dockerignore
        dockerignore = '''node_modules
.next
.nuxt
dist
.git
.gitignore
README.md
.env.local
.env.*.local
'''
        self._write_file(project_dir, ".dockerignore", dockerignore)

    def _create_github_actions(self, project_dir: Path) -> None:
        """Generate GitHub Actions workflows."""
        ci_workflow = '''name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  lint-and-test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run linter
        run: npm run lint

      - name: Type check
        run: npm run typecheck

      - name: Run tests
        run: npm test

  build:
    runs-on: ubuntu-latest
    needs: lint-and-test

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Build application
        run: npm run build
'''
        self._write_file(project_dir, ".github/workflows/ci.yml", ci_workflow)

    def _create_husky_config(self, project_dir: Path) -> None:
        """Generate Husky and lint-staged configuration."""
        pre_commit = '''#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

npx lint-staged
'''
        self._write_file(project_dir, ".husky/pre-commit", pre_commit)

        # commitlint config (optional)
        commitlint = '''module.exports = {
  extends: ['@commitlint/config-conventional'],
};
'''
        self._write_file(project_dir, "commitlint.config.js", commitlint)

    def _create_base_components(self, project_dir: Path) -> None:
        """Create base UI components."""
        if self.config.framework == ProjectFramework.NUXT:
            return  # Nuxt uses different component structure

        # Determine component directory
        comp_dir = "components/ui" if self.config.framework == ProjectFramework.NEXTJS else "src/components/ui"

        # Button component
        button = '''import { forwardRef, ButtonHTMLAttributes } from 'react';
import { cn } from '@/lib/utils';

export interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = 'primary', size = 'md', children, ...props }, ref) => {
    const variantStyles = {
      primary: 'bg-primary-600 text-white hover:bg-primary-700',
      secondary: 'bg-gray-200 text-gray-900 hover:bg-gray-300',
      outline: 'border border-gray-300 bg-transparent hover:bg-gray-100',
      ghost: 'bg-transparent hover:bg-gray-100',
    };

    const sizeStyles = {
      sm: 'h-8 px-3 text-sm',
      md: 'h-10 px-4',
      lg: 'h-12 px-6 text-lg',
    };

    return (
      <button
        ref={ref}
        className={cn(
          'inline-flex items-center justify-center rounded-md font-medium transition-colors',
          'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500',
          'disabled:pointer-events-none disabled:opacity-50',
          variantStyles[variant],
          sizeStyles[size],
          className
        )}
        {...props}
      >
        {children}
      </button>
    );
  }
);

Button.displayName = 'Button';
'''
        self._write_file(project_dir, f"{comp_dir}/Button.tsx", button)

        # Input component
        input_comp = '''import { forwardRef, InputHTMLAttributes } from 'react';
import { cn } from '@/lib/utils';

export interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  error?: boolean;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ className, error, ...props }, ref) => {
    return (
      <input
        ref={ref}
        className={cn(
          'flex h-10 w-full rounded-md border px-3 py-2 text-sm',
          'bg-white ring-offset-white file:border-0 file:bg-transparent',
          'placeholder:text-gray-500',
          'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary-500',
          'disabled:cursor-not-allowed disabled:opacity-50',
          error ? 'border-red-500' : 'border-gray-300',
          className
        )}
        {...props}
      />
    );
  }
);

Input.displayName = 'Input';
'''
        self._write_file(project_dir, f"{comp_dir}/Input.tsx", input_comp)

        # Index file
        index = '''export { Button } from './Button';
export type { ButtonProps } from './Button';
export { Input } from './Input';
export type { InputProps } from './Input';
'''
        self._write_file(project_dir, f"{comp_dir}/index.ts", index)

    def _create_utils(self, project_dir: Path) -> None:
        """Create utility files."""
        lib_dir = "lib" if self.config.framework == ProjectFramework.NEXTJS else "src/lib"

        # cn utility (className merger)
        cn_util = '''import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
'''

        # Simplified version without dependencies
        cn_simple = '''export function cn(...classes: (string | undefined | null | false)[]): string {
  return classes.filter(Boolean).join(' ');
}
'''
        self._write_file(project_dir, f"{lib_dir}/utils.ts", cn_simple)

        # API utility
        api_util = '''const API_URL = process.env.NEXT_PUBLIC_API_URL || '/api';

interface FetchOptions extends RequestInit {
  params?: Record<string, string>;
}

export async function fetcher<T>(
  endpoint: string,
  options: FetchOptions = {}
): Promise<T> {
  const { params, ...fetchOptions } = options;

  let url = `${API_URL}${endpoint}`;
  if (params) {
    const searchParams = new URLSearchParams(params);
    url += `?${searchParams.toString()}`;
  }

  const response = await fetch(url, {
    headers: {
      'Content-Type': 'application/json',
      ...fetchOptions.headers,
    },
    ...fetchOptions,
  });

  if (!response.ok) {
    throw new Error(`API Error: ${response.status}`);
  }

  return response.json();
}
'''
        self._write_file(project_dir, f"{lib_dir}/api.ts", api_util)

    def _create_state_store(self, project_dir: Path) -> None:
        """Create state management store."""
        if self.config.state_management == StateManagement.NONE:
            return

        stores_dir = "stores" if self.config.framework == ProjectFramework.NEXTJS else "src/stores"

        if self.config.state_management == StateManagement.ZUSTAND:
            store = '''import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface UserState {
  user: { id: string; name: string; email: string } | null;
  isAuthenticated: boolean;
  setUser: (user: UserState['user']) => void;
  logout: () => void;
}

export const useUserStore = create<UserState>()(
  persist(
    (set) => ({
      user: null,
      isAuthenticated: false,
      setUser: (user) => set({ user, isAuthenticated: !!user }),
      logout: () => set({ user: null, isAuthenticated: false }),
    }),
    {
      name: 'user-storage',
    }
  )
);

// App-wide UI state
interface UIState {
  theme: 'light' | 'dark';
  sidebarOpen: boolean;
  toggleTheme: () => void;
  toggleSidebar: () => void;
}

export const useUIStore = create<UIState>()((set) => ({
  theme: 'light',
  sidebarOpen: true,
  toggleTheme: () =>
    set((state) => ({ theme: state.theme === 'light' ? 'dark' : 'light' })),
  toggleSidebar: () =>
    set((state) => ({ sidebarOpen: !state.sidebarOpen })),
}));
'''
            self._write_file(project_dir, f"{stores_dir}/index.ts", store)

        elif self.config.state_management == StateManagement.PINIA:
            store = '''import { defineStore } from 'pinia';

interface User {
  id: string;
  name: string;
  email: string;
}

export const useUserStore = defineStore('user', {
  state: () => ({
    user: null as User | null,
    isAuthenticated: false,
  }),

  getters: {
    userName: (state) => state.user?.name ?? 'Guest',
  },

  actions: {
    setUser(user: User | null) {
      this.user = user;
      this.isAuthenticated = !!user;
    },
    logout() {
      this.user = null;
      this.isAuthenticated = false;
    },
  },
});
'''
            self._write_file(project_dir, f"{stores_dir}/user.ts", store)

    def _create_readme(self, project_dir: Path) -> None:
        """Generate README.md file."""
        framework_name = {
            ProjectFramework.NEXTJS: "Next.js 14",
            ProjectFramework.VITE_REACT: "Vite + React",
            ProjectFramework.NUXT: "Nuxt 3",
        }[self.config.framework]

        readme = f'''# {self.config.name}

A modern {framework_name} application with TypeScript and Tailwind CSS.

## Tech Stack

- **Framework:** {framework_name}
- **Language:** TypeScript
- **Styling:** {"Tailwind CSS" if self.config.styling == Styling.TAILWIND else "CSS Modules"}
- **State Management:** {self.config.state_management.value.title() if self.config.state_management != StateManagement.NONE else "None"}
- **Testing:** {"Jest" if self.config.framework == ProjectFramework.NEXTJS else "Vitest"} + Testing Library
- **Linting:** ESLint + Prettier

## Getting Started

### Prerequisites

- Node.js 18+
- npm/yarn/pnpm

### Installation

```bash
# Install dependencies
{self.config.package_manager.value} install

# Start development server
{self.config.package_manager.value} run dev
```

### Available Scripts

| Command | Description |
|---------|-------------|
| `dev` | Start development server |
| `build` | Build for production |
| `lint` | Run ESLint |
| `test` | Run tests |
| `format` | Format code with Prettier |

## Project Structure

```
{self.config.name}/
{"app/" if self.config.framework == ProjectFramework.NEXTJS else "src/"
}├── {"components/" if self.config.framework == ProjectFramework.NEXTJS else ""}
│   ├── ui/          # Reusable UI components
│   └── layouts/     # Layout components
├── {"lib/" if self.config.framework == ProjectFramework.NEXTJS else "lib/"}
├── {"hooks/" if self.config.framework == ProjectFramework.NEXTJS else "hooks/"}
├── {"stores/" if self.config.state_management != StateManagement.NONE else ""}
└── tests/
```

## License

MIT
'''
        self._write_file(project_dir, "README.md", readme)

    def _get_next_steps(self) -> List[str]:
        """Generate next steps for the user."""
        pm = self.config.package_manager.value
        steps = [
            f"cd {self.config.name}",
            f"{pm} install",
            f"{pm} run dev",
        ]

        if self.config.include_husky:
            steps.insert(2, f"{pm} run prepare  # Setup Husky hooks")

        return steps


def format_text_output(result: ScaffoldingResult) -> str:
    """Format results as human-readable text."""
    lines = []

    lines.append("=" * 70)
    lines.append("PROJECT SCAFFOLDING REPORT")
    lines.append("=" * 70)
    lines.append("")
    lines.append(f"Project: {result.project_name}")
    lines.append(f"Framework: {result.framework}")
    lines.append(f"Output: {result.output_path}")
    lines.append(f"Status: {'Success' if result.success else 'Failed'}")
    lines.append("")

    if result.directories_created:
        lines.append("DIRECTORIES CREATED")
        lines.append("-" * 70)
        for dir_path in result.directories_created[:15]:
            lines.append(f"  {dir_path}/")
        if len(result.directories_created) > 15:
            lines.append(f"  ... and {len(result.directories_created) - 15} more")
        lines.append("")

    if result.files_created:
        lines.append("FILES CREATED")
        lines.append("-" * 70)
        for file_path in result.files_created[:20]:
            lines.append(f"  {file_path}")
        if len(result.files_created) > 20:
            lines.append(f"  ... and {len(result.files_created) - 20} more")
        lines.append("")
        lines.append(f"Total: {result.total_files} files")
        lines.append("")

    if result.errors:
        lines.append("ERRORS")
        lines.append("-" * 70)
        for error in result.errors:
            lines.append(f"  - {error}")
        lines.append("")

    lines.append("NEXT STEPS")
    lines.append("-" * 70)
    for i, step in enumerate(result.next_steps, 1):
        lines.append(f"  {i}. {step}")
    lines.append("")

    lines.append("=" * 70)

    return "\n".join(lines)


def format_json_output(result: ScaffoldingResult) -> str:
    """Format results as JSON."""
    data = {
        "metadata": {
            "tool": "frontend_scaffolder",
            "version": "1.0.0",
            "timestamp": result.timestamp,
        },
        "project": {
            "name": result.project_name,
            "framework": result.framework,
            "output_path": result.output_path,
        },
        "summary": {
            "directories_created": len(result.directories_created),
            "files_created": result.total_files,
        },
        "directories": result.directories_created,
        "files": result.files_created,
        "success": result.success,
        "errors": result.errors,
        "next_steps": result.next_steps,
    }

    return json.dumps(data, indent=2)


def main():
    """Main entry point with standardized CLI interface."""
    parser = argparse.ArgumentParser(
        description="Frontend Scaffolder - Generate production-ready frontend projects",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s my-app
  %(prog)s my-app --framework nextjs --complete
  %(prog)s my-app --framework vite-react --state zustand
  %(prog)s my-app --framework nuxt --state pinia
  %(prog)s my-app --minimal

Frameworks:
  nextjs      - Next.js 14+ with App Router (default)
  vite-react  - Vite + React 18
  nuxt        - Nuxt 3

State Management:
  zustand     - Zustand (React, default)
  pinia       - Pinia (Vue/Nuxt)
  redux       - Redux Toolkit
  jotai       - Jotai
  none        - No state management

Styling:
  tailwind    - Tailwind CSS (default)
  css-modules - CSS Modules

Generated Structure (Next.js):
  my-app/
  +-- app/
  |   +-- layout.tsx
  |   +-- page.tsx
  |   +-- globals.css
  +-- components/
  |   +-- ui/
  |   +-- layouts/
  +-- lib/
  +-- hooks/
  +-- stores/
  +-- tests/
  +-- .github/workflows/
  +-- package.json
  +-- tsconfig.json
  +-- tailwind.config.js
  +-- Dockerfile

Exit codes:
  0 - Success
  1 - Error
        """
    )

    parser.add_argument(
        'name',
        nargs='?',
        help='Project name'
    )

    parser.add_argument(
        '--framework', '-f',
        choices=['nextjs', 'vite-react', 'nuxt'],
        default='nextjs',
        help='Frontend framework (default: nextjs)'
    )

    parser.add_argument(
        '--state', '-s',
        choices=['zustand', 'pinia', 'redux', 'jotai', 'none'],
        default='zustand',
        help='State management (default: zustand)'
    )

    parser.add_argument(
        '--styling',
        choices=['tailwind', 'css-modules'],
        default='tailwind',
        help='Styling approach (default: tailwind)'
    )

    parser.add_argument(
        '--package-manager', '-p',
        choices=['npm', 'yarn', 'pnpm'],
        default='npm',
        help='Package manager (default: npm)'
    )

    parser.add_argument(
        '--output', '-o',
        default='.',
        help='Output directory (default: current)'
    )

    parser.add_argument(
        '--complete', '-c',
        action='store_true',
        help='Include all features (testing, docker, ci, husky)'
    )

    parser.add_argument(
        '--minimal', '-m',
        action='store_true',
        help='Minimal setup (no testing, docker, ci)'
    )

    parser.add_argument(
        '--auth',
        action='store_true',
        help='Include authentication scaffolding'
    )

    parser.add_argument(
        '--no-testing',
        action='store_true',
        help='Skip testing setup'
    )

    parser.add_argument(
        '--storybook',
        action='store_true',
        help='Include Storybook'
    )

    parser.add_argument(
        '--no-docker',
        action='store_true',
        help='Skip Docker configuration'
    )

    parser.add_argument(
        '--no-ci',
        action='store_true',
        help='Skip CI/CD configuration'
    )

    parser.add_argument(
        '--no-husky',
        action='store_true',
        help='Skip Husky setup'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Verbose output'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be created without writing files'
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
        print("\nError: Project name is required")
        sys.exit(1)

    # Handle --complete and --minimal flags
    if args.minimal:
        include_testing = False
        include_docker = False
        include_ci = False
        include_husky = False
    elif args.complete:
        include_testing = True
        include_docker = True
        include_ci = True
        include_husky = True
    else:
        include_testing = not args.no_testing
        include_docker = not args.no_docker
        include_ci = not args.no_ci
        include_husky = not args.no_husky

    # Auto-select state management for Nuxt
    state_management = args.state
    if args.framework == "nuxt" and state_management == "zustand":
        state_management = "pinia"  # Default to Pinia for Nuxt

    # Create config
    config = ProjectConfig(
        name=args.name,
        framework=ProjectFramework(args.framework.replace("-", "_")),
        output_dir=Path(args.output),
        styling=Styling(args.styling.replace("-", "_")),
        state_management=StateManagement(state_management),
        package_manager=PackageManager(args.package_manager),
        include_auth=args.auth,
        include_testing=include_testing,
        include_storybook=args.storybook,
        include_docker=include_docker,
        include_ci=include_ci,
        include_husky=include_husky,
        verbose=args.verbose,
        dry_run=args.dry_run,
    )

    # Scaffold project
    scaffolder = FrontendScaffolder(config)
    result = scaffolder.scaffold()

    # Format output
    if args.format == 'json':
        output = format_json_output(result)
    else:
        output = format_text_output(result)

    print(output)

    sys.exit(0 if result.success else 1)


if __name__ == '__main__':
    main()
