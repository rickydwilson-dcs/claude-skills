#!/usr/bin/env python3
"""
Fullstack Scaffolder - Complete Application Template Generator

A comprehensive fullstack application scaffolding tool that generates:
- Multiple frontend frameworks (Next.js, Nuxt, SvelteKit, Vite React)
- Multiple backend frameworks (Express, FastAPI, Fastify)
- Docker configuration
- CI/CD pipelines (GitHub Actions)
- Testing infrastructure
- Development tooling (ESLint, Prettier, TypeScript)

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

class FrontendFramework(Enum):
    """Supported frontend frameworks"""
    NEXTJS = "nextjs"
    NUXT = "nuxt"
    SVELTEKIT = "sveltekit"
    VITE_REACT = "vite-react"


class BackendFramework(Enum):
    """Supported backend frameworks"""
    EXPRESS = "express"
    FASTAPI = "fastapi"
    FASTIFY = "fastify"


class Database(Enum):
    """Supported databases"""
    POSTGRES = "postgres"
    MONGODB = "mongodb"
    SQLITE = "sqlite"
    NONE = "none"


@dataclass
class ProjectConfig:
    """Full project configuration"""
    name: str
    frontend: FrontendFramework
    backend: BackendFramework
    database: Database
    include_docker: bool
    include_ci: bool
    include_testing: bool
    output_path: Path


# =============================================================================
# File Templates - Frontend
# =============================================================================

class FrontendTemplates:
    """Templates for frontend frameworks"""

    @staticmethod
    def nextjs_package_json(name: str) -> Dict:
        """Next.js package.json"""
        return {
            "name": f"{name}-frontend",
            "version": "0.1.0",
            "private": True,
            "scripts": {
                "dev": "next dev",
                "build": "next build",
                "start": "next start",
                "lint": "next lint",
                "test": "jest"
            },
            "dependencies": {
                "next": "^14.0.0",
                "react": "^18.2.0",
                "react-dom": "^18.2.0"
            },
            "devDependencies": {
                "@types/node": "^20.10.0",
                "@types/react": "^18.2.0",
                "@types/react-dom": "^18.2.0",
                "typescript": "^5.3.0",
                "eslint": "^8.55.0",
                "eslint-config-next": "^14.0.0"
            }
        }

    @staticmethod
    def nextjs_tsconfig() -> Dict:
        """Next.js tsconfig.json"""
        return {
            "compilerOptions": {
                "target": "es5",
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
                "paths": {"@/*": ["./src/*"]}
            },
            "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
            "exclude": ["node_modules"]
        }

    @staticmethod
    def nextjs_layout(name: str) -> str:
        """Next.js root layout"""
        return f'''import type {{ Metadata }} from 'next';
import './globals.css';

export const metadata: Metadata = {{
  title: '{name}',
  description: 'A fullstack application',
}};

export default function RootLayout({{
  children,
}}: {{
  children: React.ReactNode;
}}) {{
  return (
    <html lang="en">
      <body>{{children}}</body>
    </html>
  );
}}
'''

    @staticmethod
    def nextjs_page() -> str:
        """Next.js home page"""
        return '''export default function Home() {
  return (
    <main className="min-h-screen p-8">
      <h1 className="text-4xl font-bold mb-4">Welcome</h1>
      <p className="text-lg text-gray-600">
        Your fullstack application is ready.
      </p>
    </main>
  );
}
'''

    @staticmethod
    def nextjs_globals_css() -> str:
        """Next.js global styles"""
        return '''@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --foreground-rgb: 0, 0, 0;
  --background-start-rgb: 214, 219, 220;
  --background-end-rgb: 255, 255, 255;
}

body {
  color: rgb(var(--foreground-rgb));
  background: linear-gradient(
    to bottom,
    transparent,
    rgb(var(--background-end-rgb))
  ) rgb(var(--background-start-rgb));
}
'''

    @staticmethod
    def vite_react_package_json(name: str) -> Dict:
        """Vite React package.json"""
        return {
            "name": f"{name}-frontend",
            "private": True,
            "version": "0.0.0",
            "type": "module",
            "scripts": {
                "dev": "vite",
                "build": "tsc && vite build",
                "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
                "preview": "vite preview",
                "test": "vitest"
            },
            "dependencies": {
                "react": "^18.2.0",
                "react-dom": "^18.2.0",
                "react-router-dom": "^6.20.0"
            },
            "devDependencies": {
                "@types/react": "^18.2.0",
                "@types/react-dom": "^18.2.0",
                "@typescript-eslint/eslint-plugin": "^6.13.0",
                "@typescript-eslint/parser": "^6.13.0",
                "@vitejs/plugin-react": "^4.2.0",
                "eslint": "^8.55.0",
                "eslint-plugin-react-hooks": "^4.6.0",
                "eslint-plugin-react-refresh": "^0.4.5",
                "typescript": "^5.3.0",
                "vite": "^5.0.0",
                "vitest": "^1.0.0"
            }
        }

    @staticmethod
    def vite_config() -> str:
        """Vite configuration"""
        return '''import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:3001',
        changeOrigin: true,
      },
    },
  },
});
'''

    @staticmethod
    def vite_app_tsx() -> str:
        """Vite React App.tsx"""
        return '''import { useState } from 'react';
import './App.css';

function App() {
  const [count, setCount] = useState(0);

  return (
    <div className="App">
      <h1>Fullstack Application</h1>
      <div className="card">
        <button onClick={() => setCount((c) => c + 1)}>
          Count is {count}
        </button>
        <p>
          Edit <code>src/App.tsx</code> and save to test HMR
        </p>
      </div>
    </div>
  );
}

export default App;
'''


# =============================================================================
# File Templates - Backend
# =============================================================================

class BackendTemplates:
    """Templates for backend frameworks"""

    @staticmethod
    def express_package_json(name: str, database: Database) -> Dict:
        """Express package.json"""
        deps = {
            "express": "^4.18.2",
            "cors": "^2.8.5",
            "helmet": "^7.1.0",
            "dotenv": "^16.3.1",
        }

        if database == Database.POSTGRES:
            deps["pg"] = "^8.11.0"
            deps["prisma"] = "^5.7.0"
            deps["@prisma/client"] = "^5.7.0"
        elif database == Database.MONGODB:
            deps["mongoose"] = "^8.0.0"
        elif database == Database.SQLITE:
            deps["better-sqlite3"] = "^9.2.0"

        return {
            "name": f"{name}-backend",
            "version": "1.0.0",
            "main": "dist/index.js",
            "scripts": {
                "dev": "ts-node-dev --respawn src/index.ts",
                "build": "tsc",
                "start": "node dist/index.js",
                "lint": "eslint src/",
                "test": "jest"
            },
            "dependencies": deps,
            "devDependencies": {
                "@types/express": "^4.17.21",
                "@types/cors": "^2.8.17",
                "@types/node": "^20.10.0",
                "typescript": "^5.3.0",
                "ts-node-dev": "^2.0.0",
                "eslint": "^8.55.0",
                "@typescript-eslint/parser": "^6.13.0",
                "@typescript-eslint/eslint-plugin": "^6.13.0"
            }
        }

    @staticmethod
    def express_index_ts(database: Database) -> str:
        """Express main entry point"""
        db_import = ""
        db_init = ""

        if database == Database.POSTGRES:
            db_import = "import { PrismaClient } from '@prisma/client';\n"
            db_init = "\nexport const prisma = new PrismaClient();\n"
        elif database == Database.MONGODB:
            db_import = "import mongoose from 'mongoose';\n"
            db_init = """
const MONGODB_URI = process.env.MONGODB_URI || 'mongodb://localhost:27017/app';
mongoose.connect(MONGODB_URI).then(() => {
  console.log('Connected to MongoDB');
}).catch((err) => {
  console.error('MongoDB connection error:', err);
});
"""

        return f'''import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import dotenv from 'dotenv';
{db_import}
dotenv.config();

const app = express();
const PORT = process.env.PORT || 3001;
{db_init}
// Middleware
app.use(helmet());
app.use(cors());
app.use(express.json());

// Health check
app.get('/health', (req, res) => {{
  res.json({{ status: 'ok', timestamp: new Date().toISOString() }});
}});

// API routes
app.get('/api', (req, res) => {{
  res.json({{ message: 'API is running' }});
}});

// Error handling
app.use((err: Error, req: express.Request, res: express.Response, next: express.NextFunction) => {{
  console.error(err.stack);
  res.status(500).json({{ error: 'Internal Server Error' }});
}});

app.listen(PORT, () => {{
  console.log(`Server running on port ${{PORT}}`);
}});
'''

    @staticmethod
    def express_tsconfig() -> Dict:
        """Express tsconfig.json"""
        return {
            "compilerOptions": {
                "target": "ES2020",
                "module": "commonjs",
                "lib": ["ES2020"],
                "outDir": "./dist",
                "rootDir": "./src",
                "strict": True,
                "esModuleInterop": True,
                "skipLibCheck": True,
                "forceConsistentCasingInFileNames": True,
                "resolveJsonModule": True,
                "declaration": True,
                "declarationMap": True,
                "sourceMap": True
            },
            "include": ["src/**/*"],
            "exclude": ["node_modules", "dist"]
        }

    @staticmethod
    def fastapi_main_py(database: Database) -> str:
        """FastAPI main.py"""
        db_import = ""
        db_init = ""

        if database == Database.POSTGRES:
            db_import = """from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
"""
            db_init = """
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://localhost/app")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
"""
        elif database == Database.MONGODB:
            db_import = "from motor.motor_asyncio import AsyncIOMotorClient\n"
            db_init = """
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGODB_URI)
db = client.app
"""

        return f'''import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
{db_import}
app = FastAPI(
    title="API",
    description="Fullstack API",
    version="1.0.0"
)
{db_init}
# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class HealthResponse(BaseModel):
    status: str
    timestamp: str


class MessageResponse(BaseModel):
    message: str


@app.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="ok",
        timestamp=datetime.utcnow().isoformat()
    )


@app.get("/api", response_model=MessageResponse)
async def api_root():
    return MessageResponse(message="API is running")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3001)
'''

    @staticmethod
    def fastapi_requirements(database: Database) -> str:
        """FastAPI requirements.txt"""
        reqs = [
            "fastapi>=0.104.0",
            "uvicorn[standard]>=0.24.0",
            "pydantic>=2.5.0",
            "python-dotenv>=1.0.0",
        ]

        if database == Database.POSTGRES:
            reqs.extend(["sqlalchemy>=2.0.0", "psycopg2-binary>=2.9.0", "alembic>=1.12.0"])
        elif database == Database.MONGODB:
            reqs.extend(["motor>=3.3.0", "pymongo>=4.6.0"])
        elif database == Database.SQLITE:
            reqs.extend(["sqlalchemy>=2.0.0", "aiosqlite>=0.19.0"])

        return "\n".join(reqs) + "\n"

    @staticmethod
    def fastify_package_json(name: str, database: Database) -> Dict:
        """Fastify package.json"""
        deps = {
            "fastify": "^4.24.0",
            "@fastify/cors": "^8.4.0",
            "@fastify/helmet": "^11.1.0",
            "dotenv": "^16.3.1",
        }

        if database == Database.POSTGRES:
            deps["@prisma/client"] = "^5.7.0"
        elif database == Database.MONGODB:
            deps["mongoose"] = "^8.0.0"

        return {
            "name": f"{name}-backend",
            "version": "1.0.0",
            "main": "dist/index.js",
            "scripts": {
                "dev": "ts-node-dev --respawn src/index.ts",
                "build": "tsc",
                "start": "node dist/index.js",
                "lint": "eslint src/",
                "test": "jest"
            },
            "dependencies": deps,
            "devDependencies": {
                "@types/node": "^20.10.0",
                "typescript": "^5.3.0",
                "ts-node-dev": "^2.0.0",
                "eslint": "^8.55.0",
                "prisma": "^5.7.0" if database == Database.POSTGRES else None
            }
        }

    @staticmethod
    def fastify_index_ts() -> str:
        """Fastify main entry point"""
        return '''import Fastify from 'fastify';
import cors from '@fastify/cors';
import helmet from '@fastify/helmet';
import dotenv from 'dotenv';

dotenv.config();

const fastify = Fastify({
  logger: true
});

const PORT = parseInt(process.env.PORT || '3001', 10);

// Register plugins
fastify.register(cors, {
  origin: ['http://localhost:3000'],
});
fastify.register(helmet);

// Health check
fastify.get('/health', async () => {
  return { status: 'ok', timestamp: new Date().toISOString() };
});

// API root
fastify.get('/api', async () => {
  return { message: 'API is running' };
});

// Start server
const start = async () => {
  try {
    await fastify.listen({ port: PORT, host: '0.0.0.0' });
    console.log(`Server running on port ${PORT}`);
  } catch (err) {
    fastify.log.error(err);
    process.exit(1);
  }
};

start();
'''


# =============================================================================
# File Templates - Docker
# =============================================================================

class DockerTemplates:
    """Docker configuration templates"""

    @staticmethod
    def dockerfile_frontend(framework: FrontendFramework) -> str:
        """Frontend Dockerfile"""
        if framework == FrontendFramework.NEXTJS:
            return '''FROM node:20-alpine AS base

# Install dependencies only when needed
FROM base AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm ci

# Build
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

# Production
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
CMD ["node", "server.js"]
'''
        else:
            return '''FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
'''

    @staticmethod
    def dockerfile_backend(framework: BackendFramework) -> str:
        """Backend Dockerfile"""
        if framework == BackendFramework.FASTAPI:
            return '''FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 3001

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3001"]
'''
        else:
            return '''FROM node:20-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY --from=build /app/dist ./dist
EXPOSE 3001
CMD ["node", "dist/index.js"]
'''

    @staticmethod
    def docker_compose(config: ProjectConfig) -> str:
        """Docker Compose configuration"""
        db_service = ""
        db_env = ""

        if config.database == Database.POSTGRES:
            db_service = '''
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: app
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
'''
            db_env = '''
      DATABASE_URL: postgresql://postgres:postgres@postgres:5432/app'''
        elif config.database == Database.MONGODB:
            db_service = '''
  mongodb:
    image: mongo:7
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db
'''
            db_env = '''
      MONGODB_URI: mongodb://mongodb:27017/app'''

        volumes = ""
        if config.database == Database.POSTGRES:
            volumes = "\nvolumes:\n  postgres_data:"
        elif config.database == Database.MONGODB:
            volumes = "\nvolumes:\n  mongodb_data:"

        return f'''version: '3.8'

services:
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - API_URL=http://backend:3001
    depends_on:
      - backend

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "3001:3001"
    environment:
      - NODE_ENV=production{db_env}
{f"    depends_on:" if config.database != Database.NONE else ""}
{f"      - {'postgres' if config.database == Database.POSTGRES else 'mongodb'}" if config.database not in [Database.NONE, Database.SQLITE] else ""}
{db_service}{volumes}
'''


# =============================================================================
# File Templates - CI/CD
# =============================================================================

class CITemplates:
    """CI/CD configuration templates"""

    @staticmethod
    def github_actions_ci() -> str:
        """GitHub Actions CI workflow"""
        return '''name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install frontend dependencies
        working-directory: ./frontend
        run: npm ci

      - name: Lint frontend
        working-directory: ./frontend
        run: npm run lint

      - name: Install backend dependencies
        working-directory: ./backend
        run: npm ci

      - name: Lint backend
        working-directory: ./backend
        run: npm run lint

  test:
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install frontend dependencies
        working-directory: ./frontend
        run: npm ci

      - name: Test frontend
        working-directory: ./frontend
        run: npm test

      - name: Install backend dependencies
        working-directory: ./backend
        run: npm ci

      - name: Test backend
        working-directory: ./backend
        run: npm test

  build:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Build frontend
        working-directory: ./frontend
        run: |
          npm ci
          npm run build

      - name: Build backend
        working-directory: ./backend
        run: |
          npm ci
          npm run build
'''


# =============================================================================
# File Templates - Common
# =============================================================================

class CommonTemplates:
    """Common file templates"""

    @staticmethod
    def gitignore() -> str:
        """Root .gitignore"""
        return '''# Dependencies
node_modules/
__pycache__/
*.pyc
.venv/

# Build
dist/
build/
.next/
out/

# Environment
.env
.env.local
.env.*.local

# IDE
.idea/
.vscode/
*.swp

# Testing
coverage/
.nyc_output/

# Logs
*.log
npm-debug.log*

# Misc
.DS_Store
Thumbs.db
'''

    @staticmethod
    def env_example(database: Database) -> str:
        """Example environment file"""
        db_vars = ""
        if database == Database.POSTGRES:
            db_vars = "\n# Database\nDATABASE_URL=postgresql://postgres:postgres@localhost:5432/app"
        elif database == Database.MONGODB:
            db_vars = "\n# Database\nMONGODB_URI=mongodb://localhost:27017/app"
        elif database == Database.SQLITE:
            db_vars = "\n# Database\nDATABASE_URL=file:./dev.db"

        return f'''# Server
PORT=3001
NODE_ENV=development

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:3001
{db_vars}
'''

    @staticmethod
    def makefile(config: ProjectConfig) -> str:
        """Makefile for common commands"""
        return f'''# Makefile for {config.name}

.PHONY: install dev build test lint clean docker-up docker-down

# Install all dependencies
install:
\tcd frontend && npm install
\tcd backend && {"pip install -r requirements.txt" if config.backend == BackendFramework.FASTAPI else "npm install"}

# Start development servers
dev:
\t@echo "Starting development servers..."
\t@cd frontend && npm run dev &
\t@cd backend && {"uvicorn main:app --reload --port 3001" if config.backend == BackendFramework.FASTAPI else "npm run dev"}

# Build for production
build:
\tcd frontend && npm run build
\tcd backend && {"echo 'No build step for Python'" if config.backend == BackendFramework.FASTAPI else "npm run build"}

# Run tests
test:
\tcd frontend && npm test
\tcd backend && {"pytest" if config.backend == BackendFramework.FASTAPI else "npm test"}

# Run linters
lint:
\tcd frontend && npm run lint
\tcd backend && {"ruff check ." if config.backend == BackendFramework.FASTAPI else "npm run lint"}

# Clean build artifacts
clean:
\trm -rf frontend/node_modules frontend/.next frontend/dist
\trm -rf backend/node_modules backend/dist backend/__pycache__
{f"""
# Docker commands
docker-up:
\tdocker-compose up -d

docker-down:
\tdocker-compose down
""" if config.include_docker else ""}
'''

    @staticmethod
    def readme(config: ProjectConfig) -> str:
        """Project README"""
        docker_section = ""
        if config.include_docker:
            docker_section = """
## Docker

```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f
```
"""

        return f'''# {config.name}

A fullstack application with {config.frontend.value} frontend and {config.backend.value} backend.

## Tech Stack

- **Frontend:** {config.frontend.value}
- **Backend:** {config.backend.value}
- **Database:** {config.database.value if config.database != Database.NONE else "None configured"}

## Getting Started

### Prerequisites

- Node.js 18+
{"- Python 3.11+" if config.backend == BackendFramework.FASTAPI else ""}
{"- Docker (optional)" if config.include_docker else ""}

### Installation

```bash
# Install all dependencies
make install

# Or manually:
cd frontend && npm install
cd ../backend && {"pip install -r requirements.txt" if config.backend == BackendFramework.FASTAPI else "npm install"}
```

### Development

```bash
# Start both frontend and backend
make dev

# Or manually:
# Terminal 1 - Frontend
cd frontend && npm run dev

# Terminal 2 - Backend
cd backend && {"uvicorn main:app --reload --port 3001" if config.backend == BackendFramework.FASTAPI else "npm run dev"}
```

### Building

```bash
make build
```
{docker_section}
## Project Structure

```
{config.name}/
├── frontend/          # {config.frontend.value} application
│   ├── src/
│   └── package.json
├── backend/           # {config.backend.value} API
│   ├── src/
│   └── {"requirements.txt" if config.backend == BackendFramework.FASTAPI else "package.json"}
├── docker-compose.yml
├── Makefile
└── README.md
```

## License

MIT
'''


# =============================================================================
# Main Scaffolder Class
# =============================================================================

class FullstackScaffolder:
    """Fullstack application scaffolder"""

    def __init__(self, config: ProjectConfig, verbose: bool = False):
        if verbose:
            logging.getLogger().setLevel(logging.DEBUG)

        self.config = config
        self.verbose = verbose
        self.files_created: List[str] = []

        logger.debug("FullstackScaffolder initialized")

    def run(self) -> Dict:
        """Execute the scaffolding"""
        logger.debug("Starting scaffolding run")
        if self.verbose:
            print(f"Creating fullstack app: {self.config.name}", file=sys.stderr)
            print(f"Frontend: {self.config.frontend.value}", file=sys.stderr)
            print(f"Backend: {self.config.backend.value}", file=sys.stderr)

        # Create directory structure
        self._create_directories()

        # Create frontend
        self._create_frontend()

        # Create backend
        self._create_backend()

        # Create root files
        self._create_root_files()

        # Create Docker if enabled
        if self.config.include_docker:
            self._create_docker()

        # Create CI if enabled
        if self.config.include_ci:
            self._create_ci()

        return self._build_results()

    def _create_directories(self):
        """Create the directory structure"""
        logger.debug("Creating directory structure")
        root = self.config.output_path
        root.mkdir(parents=True, exist_ok=True)

        # Frontend
        frontend = root / 'frontend'
        frontend.mkdir(exist_ok=True)
        (frontend / 'src').mkdir(exist_ok=True)

        if self.config.frontend == FrontendFramework.NEXTJS:
            (frontend / 'src' / 'app').mkdir(exist_ok=True)
            (frontend / 'public').mkdir(exist_ok=True)
        else:
            (frontend / 'src' / 'components').mkdir(exist_ok=True)
            (frontend / 'public').mkdir(exist_ok=True)

        # Backend
        backend = root / 'backend'
        backend.mkdir(exist_ok=True)
        if self.config.backend != BackendFramework.FASTAPI:
            (backend / 'src').mkdir(exist_ok=True)

        # GitHub workflows
        if self.config.include_ci:
            (root / '.github' / 'workflows').mkdir(parents=True, exist_ok=True)

        if self.verbose:
            print("Created directory structure", file=sys.stderr)

    def _create_frontend(self):
        """Create frontend files"""
        logger.debug(f"Creating frontend ({self.config.frontend.value})")
        frontend = self.config.output_path / 'frontend'

        if self.config.frontend == FrontendFramework.NEXTJS:
            self._write_json(
                frontend / 'package.json',
                FrontendTemplates.nextjs_package_json(self.config.name)
            )
            self._write_json(
                frontend / 'tsconfig.json',
                FrontendTemplates.nextjs_tsconfig()
            )
            self._write_file(
                frontend / 'src' / 'app' / 'layout.tsx',
                FrontendTemplates.nextjs_layout(self.config.name)
            )
            self._write_file(
                frontend / 'src' / 'app' / 'page.tsx',
                FrontendTemplates.nextjs_page()
            )
            self._write_file(
                frontend / 'src' / 'app' / 'globals.css',
                FrontendTemplates.nextjs_globals_css()
            )
        else:
            self._write_json(
                frontend / 'package.json',
                FrontendTemplates.vite_react_package_json(self.config.name)
            )
            self._write_file(
                frontend / 'vite.config.ts',
                FrontendTemplates.vite_config()
            )
            self._write_file(
                frontend / 'src' / 'App.tsx',
                FrontendTemplates.vite_app_tsx()
            )
            # Index.html for Vite
            self._write_file(
                frontend / 'index.html',
                '''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>App</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
'''
            )
            self._write_file(
                frontend / 'src' / 'main.tsx',
                '''import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
'''
            )

        if self.verbose:
            print(f"Created frontend ({self.config.frontend.value})", file=sys.stderr)

    def _create_backend(self):
        """Create backend files"""
        logger.debug(f"Creating backend ({self.config.backend.value})")
        backend = self.config.output_path / 'backend'

        if self.config.backend == BackendFramework.FASTAPI:
            self._write_file(
                backend / 'main.py',
                BackendTemplates.fastapi_main_py(self.config.database)
            )
            self._write_file(
                backend / 'requirements.txt',
                BackendTemplates.fastapi_requirements(self.config.database)
            )
        elif self.config.backend == BackendFramework.FASTIFY:
            self._write_json(
                backend / 'package.json',
                BackendTemplates.fastify_package_json(self.config.name, self.config.database)
            )
            self._write_file(
                backend / 'src' / 'index.ts',
                BackendTemplates.fastify_index_ts()
            )
            self._write_json(
                backend / 'tsconfig.json',
                BackendTemplates.express_tsconfig()
            )
        else:  # Express
            self._write_json(
                backend / 'package.json',
                BackendTemplates.express_package_json(self.config.name, self.config.database)
            )
            self._write_file(
                backend / 'src' / 'index.ts',
                BackendTemplates.express_index_ts(self.config.database)
            )
            self._write_json(
                backend / 'tsconfig.json',
                BackendTemplates.express_tsconfig()
            )

        if self.verbose:
            print(f"Created backend ({self.config.backend.value})", file=sys.stderr)

    def _create_root_files(self):
        """Create root-level files"""
        root = self.config.output_path

        self._write_file(root / '.gitignore', CommonTemplates.gitignore())
        self._write_file(root / '.env.example', CommonTemplates.env_example(self.config.database))
        self._write_file(root / 'Makefile', CommonTemplates.makefile(self.config))
        self._write_file(root / 'README.md', CommonTemplates.readme(self.config))

        if self.verbose:
            print("Created root configuration files", file=sys.stderr)

    def _create_docker(self):
        """Create Docker configuration"""
        root = self.config.output_path

        self._write_file(
            root / 'frontend' / 'Dockerfile',
            DockerTemplates.dockerfile_frontend(self.config.frontend)
        )
        self._write_file(
            root / 'backend' / 'Dockerfile',
            DockerTemplates.dockerfile_backend(self.config.backend)
        )
        self._write_file(
            root / 'docker-compose.yml',
            DockerTemplates.docker_compose(self.config)
        )

        if self.verbose:
            print("Created Docker configuration", file=sys.stderr)

    def _create_ci(self):
        """Create CI/CD configuration"""
        self._write_file(
            self.config.output_path / '.github' / 'workflows' / 'ci.yml',
            CITemplates.github_actions_ci()
        )

        if self.verbose:
            print("Created CI/CD configuration", file=sys.stderr)

    def _write_file(self, path: Path, content: str):
        """Write content to a file"""
        with open(path, 'w') as f:
            f.write(content)
        self.files_created.append(str(path.relative_to(self.config.output_path)))

    def _write_json(self, path: Path, data: Dict):
        """Write JSON data to a file"""
        # Filter out None values
        filtered = {k: v for k, v in data.items() if v is not None}
        if 'devDependencies' in filtered:
            filtered['devDependencies'] = {
                k: v for k, v in filtered['devDependencies'].items() if v is not None
            }

        with open(path, 'w') as f:
            json.dump(filtered, f, indent=2)
            f.write('\n')
        self.files_created.append(str(path.relative_to(self.config.output_path)))

    def _build_results(self) -> Dict:
        """Build the results dictionary"""
        next_steps = [
            f"cd {self.config.output_path}",
            "make install  # Install dependencies",
            "make dev      # Start development servers",
        ]

        if self.config.include_docker:
            next_steps.insert(2, "docker-compose up -d  # Or use Docker")

        return {
            'timestamp': datetime.now().isoformat(),
            'project_name': self.config.name,
            'output_path': str(self.config.output_path),
            'configuration': {
                'frontend': self.config.frontend.value,
                'backend': self.config.backend.value,
                'database': self.config.database.value,
                'docker': self.config.include_docker,
                'ci': self.config.include_ci,
                'testing': self.config.include_testing,
            },
            'files_created': self.files_created,
            'stats': {
                'total_files': len(self.files_created),
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
        lines.append("FULLSTACK SCAFFOLDING COMPLETE")
        lines.append("=" * 60)
        lines.append(f"Timestamp: {results['timestamp']}")
        lines.append(f"Project: {results['project_name']}")
        lines.append(f"Location: {results['output_path']}")
        lines.append("")

        config = results['configuration']
        lines.append("CONFIGURATION")
        lines.append("-" * 40)
        lines.append(f"  Frontend: {config['frontend']}")
        lines.append(f"  Backend: {config['backend']}")
        lines.append(f"  Database: {config['database']}")
        lines.append(f"  Docker: {'Yes' if config['docker'] else 'No'}")
        lines.append(f"  CI/CD: {'Yes' if config['ci'] else 'No'}")
        lines.append("")

        stats = results['stats']
        lines.append("STATISTICS")
        lines.append("-" * 40)
        lines.append(f"  Files Created: {stats['total_files']}")
        lines.append("")

        lines.append("FILES CREATED")
        lines.append("-" * 40)
        for f in results['files_created'][:15]:
            lines.append(f"  {f}")
        if len(results['files_created']) > 15:
            lines.append(f"  ... and {len(results['files_created']) - 15} more")
        lines.append("")

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
        description='Fullstack Scaffolder - Complete application template generator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create a Next.js + Express app
  %(prog)s --output ./my-app --name my-app

  # Create with FastAPI backend and PostgreSQL
  %(prog)s --output ./app --name app --backend fastapi --database postgres

  # Create with all features (Docker, CI, Testing)
  %(prog)s --output ./full-app --name full-app --docker --ci --testing

  # Create Vite React + Fastify + MongoDB
  %(prog)s --output ./vite-app --name vite-app --frontend vite-react --backend fastify --database mongodb

Frontend Frameworks:
  - nextjs: Next.js 14 with App Router
  - vite-react: Vite + React (coming soon: nuxt, sveltekit)

Backend Frameworks:
  - express: Express.js with TypeScript
  - fastapi: FastAPI with Python
  - fastify: Fastify with TypeScript

Databases:
  - postgres: PostgreSQL with Prisma ORM
  - mongodb: MongoDB with Mongoose
  - sqlite: SQLite (development)
  - none: No database configured

Features:
  --docker: Include Dockerfile and docker-compose.yml
  --ci: Include GitHub Actions CI workflow
  --testing: Include testing configuration
        """
    )

    parser.add_argument(
        '--output', '-o',
        required=True,
        help='Output directory for the project'
    )

    parser.add_argument(
        '--name', '-n',
        required=True,
        help='Name of the project'
    )

    parser.add_argument(
        '--frontend', '-fe',
        choices=['nextjs', 'vite-react', 'nuxt', 'sveltekit'],
        default='nextjs',
        help='Frontend framework (default: nextjs)'
    )

    parser.add_argument(
        '--backend', '-be',
        choices=['express', 'fastapi', 'fastify'],
        default='express',
        help='Backend framework (default: express)'
    )

    parser.add_argument(
        '--database', '-db',
        choices=['postgres', 'mongodb', 'sqlite', 'none'],
        default='none',
        help='Database to configure (default: none)'
    )

    parser.add_argument(
        '--docker',
        action='store_true',
        help='Include Docker configuration'
    )

    parser.add_argument(
        '--ci',
        action='store_true',
        help='Include CI/CD configuration (GitHub Actions)'
    )

    parser.add_argument(
        '--testing',
        action='store_true',
        help='Include testing configuration'
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

    # Parse enums
    frontend_map = {
        'nextjs': FrontendFramework.NEXTJS,
        'vite-react': FrontendFramework.VITE_REACT,
        'nuxt': FrontendFramework.NUXT,
        'sveltekit': FrontendFramework.SVELTEKIT,
    }
    backend_map = {
        'express': BackendFramework.EXPRESS,
        'fastapi': BackendFramework.FASTAPI,
        'fastify': BackendFramework.FASTIFY,
    }
    database_map = {
        'postgres': Database.POSTGRES,
        'mongodb': Database.MONGODB,
        'sqlite': Database.SQLITE,
        'none': Database.NONE,
    }

    # Check for unsupported combinations
    if args.frontend in ['nuxt', 'sveltekit']:
        print(f"Warning: {args.frontend} support coming soon, using nextjs", file=sys.stderr)
        args.frontend = 'nextjs'

    output_path = Path(args.output).resolve()

    config = ProjectConfig(
        name=args.name,
        frontend=frontend_map[args.frontend],
        backend=backend_map[args.backend],
        database=database_map[args.database],
        include_docker=args.docker,
        include_ci=args.ci,
        include_testing=args.testing,
        output_path=output_path,
    )

    try:
        scaffolder = FullstackScaffolder(config, verbose=args.verbose)
        results = scaffolder.run()

        formatter = OutputFormatter()
        if args.format == 'json':
            output_text = formatter.format_json(results)
        else:
            output_text = formatter.format_text(results)

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
