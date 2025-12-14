#!/usr/bin/env python3
"""
Pipeline Generator
CI/CD pipeline configuration generator for GitHub Actions, GitLab CI, Jenkins, and CircleCI.

Features:
- Multi-platform support (GitHub Actions, GitLab CI, Jenkins, CircleCI)
- Language-specific templates (Node.js, Python, Go, Java)
- Multi-stage pipelines (build, test, scan, deploy)
- Deployment target configurations (Kubernetes, ECS, Docker Compose)
- Environment-specific workflows (dev, staging, prod)
- Security scanning and artifact publishing

Standard library only - no external dependencies required.
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
from typing import Any, Dict, List, Optional, Set

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class Platform(Enum):
    """Supported CI/CD platforms"""
    GITHUB = "github"
    GITLAB = "gitlab"
    JENKINS = "jenkins"
    CIRCLECI = "circleci"


class Language(Enum):
    """Supported programming languages"""
    NODEJS = "nodejs"
    PYTHON = "python"
    GO = "go"
    JAVA = "java"
    DOCKER = "docker"


class DeployTarget(Enum):
    """Supported deployment targets"""
    KUBERNETES = "kubernetes"
    ECS = "ecs"
    DOCKER_COMPOSE = "docker-compose"
    SERVERLESS = "serverless"
    NONE = "none"


class Stage(Enum):
    """Pipeline stages"""
    BUILD = "build"
    TEST = "test"
    SCAN = "scan"
    PUBLISH = "publish"
    DEPLOY = "deploy"


@dataclass
class PipelineStage:
    """Configuration for a pipeline stage"""
    name: str
    stage_type: Stage
    commands: List[str]
    dependencies: List[str] = field(default_factory=list)
    environment: Optional[str] = None
    artifacts: List[str] = field(default_factory=list)
    cache_paths: List[str] = field(default_factory=list)
    services: List[str] = field(default_factory=list)
    condition: Optional[str] = None


@dataclass
class PipelineConfig:
    """Complete pipeline configuration"""
    name: str
    platform: Platform
    language: Language
    stages: List[PipelineStage]
    environments: List[str]
    deploy_target: DeployTarget
    docker_registry: str = "ghcr.io"
    node_version: str = "20"
    python_version: str = "3.11"
    go_version: str = "1.21"
    java_version: str = "17"
    use_cache: bool = True
    parallel_tests: bool = True


@dataclass
class ProjectInfo:
    """Detected project information"""
    name: str
    language: Language
    has_docker: bool
    has_tests: bool
    package_manager: str
    test_command: str
    build_command: str
    existing_ci: List[str]


class PipelineGenerator:
    """
    CI/CD pipeline generator supporting multiple platforms and languages.
    """

    LANGUAGE_CONFIGS = {
        Language.NODEJS: {
            "package_files": ["package.json", "package-lock.json", "yarn.lock", "pnpm-lock.yaml"],
            "test_commands": {
                "npm": "npm test",
                "yarn": "yarn test",
                "pnpm": "pnpm test"
            },
            "build_commands": {
                "npm": "npm run build",
                "yarn": "yarn build",
                "pnpm": "pnpm build"
            },
            "cache_paths": ["node_modules", ".npm", ".yarn/cache"],
            "docker_base": "node:20-alpine"
        },
        Language.PYTHON: {
            "package_files": ["requirements.txt", "pyproject.toml", "setup.py", "Pipfile"],
            "test_commands": {
                "pip": "pytest",
                "poetry": "poetry run pytest",
                "pipenv": "pipenv run pytest"
            },
            "build_commands": {
                "pip": "pip install -e .",
                "poetry": "poetry build",
                "pipenv": "pipenv install"
            },
            "cache_paths": [".venv", "__pycache__", ".pytest_cache"],
            "docker_base": "python:3.11-slim"
        },
        Language.GO: {
            "package_files": ["go.mod", "go.sum"],
            "test_commands": {"go": "go test ./..."},
            "build_commands": {"go": "go build -o bin/app ./..."},
            "cache_paths": ["~/go/pkg/mod"],
            "docker_base": "golang:1.21-alpine"
        },
        Language.JAVA: {
            "package_files": ["pom.xml", "build.gradle", "build.gradle.kts"],
            "test_commands": {
                "maven": "mvn test",
                "gradle": "./gradlew test"
            },
            "build_commands": {
                "maven": "mvn package -DskipTests",
                "gradle": "./gradlew build -x test"
            },
            "cache_paths": ["~/.m2/repository", "~/.gradle/caches"],
            "docker_base": "eclipse-temurin:17-jdk-alpine"
        }
    }

    def __init__(
        self,
        target_path: str,
        platform: str,
        language: Optional[str] = None,
        stages: Optional[List[str]] = None,
        environments: Optional[List[str]] = None,
        deploy_target: str = "none",
        verbose: bool = False
    ):
        self.target_path = Path(target_path)
        self.platform = Platform(platform)
        self.requested_language = Language(language) if language else None
        self.requested_stages = [Stage(s) for s in (stages or ["build", "test"])]
        self.environments = environments or ["dev", "staging", "prod"]
        self.deploy_target = DeployTarget(deploy_target)
        self.verbose = verbose
        self.project_info: Optional[ProjectInfo] = None
        self.config: Optional[PipelineConfig] = None
        self.generated_files: Dict[str, str] = {}

    def run(self) -> Dict[str, Any]:
        """Execute the pipeline generation"""
        if self.verbose:
            print(f"Analyzing project: {self.target_path}", file=sys.stderr)

        # Analyze project
        self.project_info = self._analyze_project()

        if self.verbose:
            print(f"Detected language: {self.project_info.language.value}", file=sys.stderr)
            print(f"Package manager: {self.project_info.package_manager}", file=sys.stderr)

        # Build configuration
        self.config = self._build_config()

        # Generate pipeline
        if self.platform == Platform.GITHUB:
            self._generate_github_actions()
        elif self.platform == Platform.GITLAB:
            self._generate_gitlab_ci()
        elif self.platform == Platform.JENKINS:
            self._generate_jenkinsfile()
        elif self.platform == Platform.CIRCLECI:
            self._generate_circleci()

        return {
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "project": {
                "name": self.project_info.name,
                "language": self.project_info.language.value,
                "package_manager": self.project_info.package_manager,
                "has_docker": self.project_info.has_docker,
                "has_tests": self.project_info.has_tests
            },
            "pipeline": {
                "platform": self.platform.value,
                "stages": [s.value for s in self.requested_stages],
                "environments": self.environments,
                "deploy_target": self.deploy_target.value
            },
            "files": list(self.generated_files.keys()),
            "content": self.generated_files
        }

    def _analyze_project(self) -> ProjectInfo:
        """Analyze the project to detect language and configuration"""
        name = self.target_path.name
        language = self.requested_language
        has_docker = False
        has_tests = False
        package_manager = "unknown"
        test_command = ""
        build_command = ""
        existing_ci: List[str] = []

        # Check for existing CI configurations
        ci_paths = [
            (".github/workflows", "github"),
            (".gitlab-ci.yml", "gitlab"),
            ("Jenkinsfile", "jenkins"),
            (".circleci/config.yml", "circleci")
        ]
        for ci_path, ci_name in ci_paths:
            if (self.target_path / ci_path).exists():
                existing_ci.append(ci_name)

        # Check for Dockerfile
        if (self.target_path / "Dockerfile").exists():
            has_docker = True

        # Detect language if not specified
        if not language:
            language = self._detect_language()

        # Get package manager and commands
        lang_config = self.LANGUAGE_CONFIGS.get(language, {})

        if language == Language.NODEJS:
            if (self.target_path / "yarn.lock").exists():
                package_manager = "yarn"
            elif (self.target_path / "pnpm-lock.yaml").exists():
                package_manager = "pnpm"
            else:
                package_manager = "npm"
        elif language == Language.PYTHON:
            if (self.target_path / "pyproject.toml").exists():
                package_manager = "poetry"
            elif (self.target_path / "Pipfile").exists():
                package_manager = "pipenv"
            else:
                package_manager = "pip"
        elif language == Language.GO:
            package_manager = "go"
        elif language == Language.JAVA:
            if (self.target_path / "build.gradle").exists() or (self.target_path / "build.gradle.kts").exists():
                package_manager = "gradle"
            else:
                package_manager = "maven"
        else:
            package_manager = "docker"

        # Get commands from config
        test_commands = lang_config.get("test_commands", {})
        build_commands = lang_config.get("build_commands", {})
        test_command = test_commands.get(package_manager, "echo 'No tests configured'")
        build_command = build_commands.get(package_manager, "echo 'No build configured'")

        # Check for tests
        test_dirs = ["test", "tests", "spec", "__tests__", "src/test"]
        for test_dir in test_dirs:
            if (self.target_path / test_dir).exists():
                has_tests = True
                break

        return ProjectInfo(
            name=name,
            language=language,
            has_docker=has_docker,
            has_tests=has_tests,
            package_manager=package_manager,
            test_command=test_command,
            build_command=build_command,
            existing_ci=existing_ci
        )

    def _detect_language(self) -> Language:
        """Detect the primary language of the project"""
        # Check for language-specific files
        if (self.target_path / "package.json").exists():
            return Language.NODEJS
        elif (self.target_path / "go.mod").exists():
            return Language.GO
        elif (self.target_path / "pom.xml").exists() or \
             (self.target_path / "build.gradle").exists() or \
             (self.target_path / "build.gradle.kts").exists():
            return Language.JAVA
        elif (self.target_path / "requirements.txt").exists() or \
             (self.target_path / "pyproject.toml").exists() or \
             (self.target_path / "setup.py").exists():
            return Language.PYTHON
        elif (self.target_path / "Dockerfile").exists():
            return Language.DOCKER
        else:
            return Language.NODEJS  # Default

    def _build_config(self) -> PipelineConfig:
        """Build the pipeline configuration"""
        stages: List[PipelineStage] = []
        lang_config = self.LANGUAGE_CONFIGS.get(self.project_info.language, {})
        cache_paths = lang_config.get("cache_paths", [])

        # Build stage
        if Stage.BUILD in self.requested_stages:
            stages.append(PipelineStage(
                name="build",
                stage_type=Stage.BUILD,
                commands=self._get_build_commands(),
                cache_paths=cache_paths,
                artifacts=self._get_build_artifacts()
            ))

        # Test stage
        if Stage.TEST in self.requested_stages:
            stages.append(PipelineStage(
                name="test",
                stage_type=Stage.TEST,
                commands=self._get_test_commands(),
                dependencies=["build"] if Stage.BUILD in self.requested_stages else [],
                cache_paths=cache_paths
            ))

        # Scan stage
        if Stage.SCAN in self.requested_stages:
            stages.append(PipelineStage(
                name="security-scan",
                stage_type=Stage.SCAN,
                commands=self._get_scan_commands(),
                dependencies=["build"] if Stage.BUILD in self.requested_stages else []
            ))

        # Publish stage
        if Stage.PUBLISH in self.requested_stages or (Stage.DEPLOY in self.requested_stages and self.project_info.has_docker):
            stages.append(PipelineStage(
                name="publish",
                stage_type=Stage.PUBLISH,
                commands=self._get_publish_commands(),
                dependencies=["test"] if Stage.TEST in self.requested_stages else ["build"]
            ))

        # Deploy stages per environment
        if Stage.DEPLOY in self.requested_stages:
            for i, env in enumerate(self.environments):
                deps = ["publish"] if Stage.PUBLISH in [s.stage_type for s in stages] else ["test", "build"]
                if i > 0:
                    deps.append(f"deploy-{self.environments[i-1]}")

                stages.append(PipelineStage(
                    name=f"deploy-{env}",
                    stage_type=Stage.DEPLOY,
                    commands=self._get_deploy_commands(env),
                    dependencies=deps,
                    environment=env,
                    condition=self._get_deploy_condition(env)
                ))

        return PipelineConfig(
            name=f"{self.project_info.name}-pipeline",
            platform=self.platform,
            language=self.project_info.language,
            stages=stages,
            environments=self.environments,
            deploy_target=self.deploy_target
        )

    def _get_build_commands(self) -> List[str]:
        """Get build commands for the detected language"""
        commands = []

        if self.project_info.language == Language.NODEJS:
            pm = self.project_info.package_manager
            if pm == "yarn":
                commands = ["yarn install --frozen-lockfile", "yarn build"]
            elif pm == "pnpm":
                commands = ["pnpm install --frozen-lockfile", "pnpm build"]
            else:
                commands = ["npm ci", "npm run build"]

        elif self.project_info.language == Language.PYTHON:
            pm = self.project_info.package_manager
            if pm == "poetry":
                commands = ["poetry install", "poetry build"]
            elif pm == "pipenv":
                commands = ["pipenv install --deploy"]
            else:
                commands = ["pip install -r requirements.txt"]

        elif self.project_info.language == Language.GO:
            commands = ["go mod download", "go build -o bin/app ./..."]

        elif self.project_info.language == Language.JAVA:
            pm = self.project_info.package_manager
            if pm == "gradle":
                commands = ["./gradlew build -x test"]
            else:
                commands = ["mvn package -DskipTests"]

        elif self.project_info.language == Language.DOCKER:
            commands = ["docker build -t $IMAGE_NAME:$VERSION ."]

        return commands

    def _get_test_commands(self) -> List[str]:
        """Get test commands for the detected language"""
        commands = []

        if self.project_info.language == Language.NODEJS:
            pm = self.project_info.package_manager
            if pm == "yarn":
                commands = ["yarn test", "yarn test:coverage"]
            elif pm == "pnpm":
                commands = ["pnpm test", "pnpm test:coverage"]
            else:
                commands = ["npm test", "npm run test:coverage"]

        elif self.project_info.language == Language.PYTHON:
            commands = ["pytest --cov=. --cov-report=xml"]

        elif self.project_info.language == Language.GO:
            commands = ["go test -v -race -coverprofile=coverage.out ./..."]

        elif self.project_info.language == Language.JAVA:
            pm = self.project_info.package_manager
            if pm == "gradle":
                commands = ["./gradlew test"]
            else:
                commands = ["mvn test"]

        return commands

    def _get_scan_commands(self) -> List[str]:
        """Get security scanning commands"""
        commands = []

        if self.project_info.language == Language.NODEJS:
            commands = ["npm audit --audit-level=high", "npx eslint . --ext .js,.ts"]
        elif self.project_info.language == Language.PYTHON:
            commands = ["pip-audit", "bandit -r . -ll"]
        elif self.project_info.language == Language.GO:
            commands = ["go vet ./...", "gosec ./..."]
        elif self.project_info.language == Language.JAVA:
            commands = ["mvn org.owasp:dependency-check-maven:check"]

        # Add secret scanning for all
        commands.append("git secrets --scan || true")

        return commands

    def _get_publish_commands(self) -> List[str]:
        """Get artifact/Docker publish commands"""
        if self.project_info.has_docker:
            return [
                "docker build -t $REGISTRY/$IMAGE_NAME:$VERSION .",
                "docker push $REGISTRY/$IMAGE_NAME:$VERSION",
                "docker tag $REGISTRY/$IMAGE_NAME:$VERSION $REGISTRY/$IMAGE_NAME:latest",
                "docker push $REGISTRY/$IMAGE_NAME:latest"
            ]
        return ["echo 'No publish step configured'"]

    def _get_deploy_commands(self, environment: str) -> List[str]:
        """Get deployment commands for an environment"""
        if self.deploy_target == DeployTarget.KUBERNETES:
            return [
                f"kubectl config use-context {environment}",
                "kubectl apply -f k8s/",
                f"kubectl set image deployment/$APP_NAME $APP_NAME=$REGISTRY/$IMAGE_NAME:$VERSION",
                "kubectl rollout status deployment/$APP_NAME"
            ]
        elif self.deploy_target == DeployTarget.ECS:
            return [
                f"aws ecs update-service --cluster {environment}-cluster --service $APP_NAME --force-new-deployment",
                "aws ecs wait services-stable --cluster {environment}-cluster --services $APP_NAME"
            ]
        elif self.deploy_target == DeployTarget.DOCKER_COMPOSE:
            return [
                f"docker-compose -f docker-compose.{environment}.yml pull",
                f"docker-compose -f docker-compose.{environment}.yml up -d"
            ]
        elif self.deploy_target == DeployTarget.SERVERLESS:
            return [f"serverless deploy --stage {environment}"]
        return [f"echo 'Deploy to {environment}'"]

    def _get_deploy_condition(self, environment: str) -> str:
        """Get deployment condition based on environment"""
        if environment == "prod":
            return "main"
        elif environment == "staging":
            return "main,staging"
        else:
            return "develop,feature/*"

    def _get_build_artifacts(self) -> List[str]:
        """Get build artifacts paths"""
        if self.project_info.language == Language.NODEJS:
            return ["dist/", "build/", ".next/"]
        elif self.project_info.language == Language.PYTHON:
            return ["dist/", "*.whl"]
        elif self.project_info.language == Language.GO:
            return ["bin/"]
        elif self.project_info.language == Language.JAVA:
            return ["target/*.jar", "build/libs/*.jar"]
        return []

    def _generate_github_actions(self):
        """Generate GitHub Actions workflow"""
        workflow = {
            "name": self.config.name,
            "on": {
                "push": {"branches": ["main", "develop"]},
                "pull_request": {"branches": ["main", "develop"]}
            },
            "env": {
                "REGISTRY": "ghcr.io",
                "IMAGE_NAME": "${{ github.repository }}",
                "VERSION": "${{ github.sha }}"
            },
            "jobs": {}
        }

        for stage in self.config.stages:
            job = self._create_github_job(stage)
            workflow["jobs"][stage.name] = job

        # Convert to YAML manually (no PyYAML dependency)
        yaml_content = self._dict_to_yaml(workflow)
        self.generated_files[".github/workflows/ci-cd.yml"] = yaml_content

    def _create_github_job(self, stage: PipelineStage) -> Dict:
        """Create a GitHub Actions job from a stage"""
        job: Dict[str, Any] = {
            "runs-on": "ubuntu-latest"
        }

        # Add dependencies
        if stage.dependencies:
            job["needs"] = stage.dependencies

        # Add environment for deploy stages
        if stage.environment:
            job["environment"] = stage.environment

        # Add condition for deploy stages
        if stage.condition and stage.stage_type == Stage.DEPLOY:
            branches = stage.condition.split(",")
            if len(branches) == 1:
                job["if"] = f"github.ref == 'refs/heads/{branches[0]}'"
            else:
                conditions = [f"github.ref == 'refs/heads/{b.strip()}'" for b in branches if not b.strip().endswith("/*")]
                job["if"] = " || ".join(conditions) if conditions else "true"

        # Build steps
        steps = [{"uses": "actions/checkout@v4"}]

        # Language-specific setup
        if self.config.language == Language.NODEJS:
            steps.append({
                "uses": "actions/setup-node@v4",
                "with": {"node-version": self.config.node_version, "cache": "npm"}
            })
        elif self.config.language == Language.PYTHON:
            steps.append({
                "uses": "actions/setup-python@v5",
                "with": {"python-version": self.config.python_version}
            })
        elif self.config.language == Language.GO:
            steps.append({
                "uses": "actions/setup-go@v5",
                "with": {"go-version": self.config.go_version}
            })
        elif self.config.language == Language.JAVA:
            steps.append({
                "uses": "actions/setup-java@v4",
                "with": {"java-version": self.config.java_version, "distribution": "temurin"}
            })

        # Docker login for publish/deploy
        if stage.stage_type in [Stage.PUBLISH, Stage.DEPLOY] and self.project_info.has_docker:
            steps.append({
                "uses": "docker/login-action@v3",
                "with": {
                    "registry": "ghcr.io",
                    "username": "${{ github.actor }}",
                    "password": "${{ secrets.GITHUB_TOKEN }}"
                }
            })

        # Add commands as run steps
        for i, cmd in enumerate(stage.commands):
            steps.append({
                "name": f"Step {i+1}: {cmd[:50]}...",
                "run": cmd
            })

        # Upload artifacts for build stage
        if stage.stage_type == Stage.BUILD and stage.artifacts:
            steps.append({
                "uses": "actions/upload-artifact@v4",
                "with": {
                    "name": "build-artifacts",
                    "path": "\n".join(stage.artifacts)
                }
            })

        # Upload coverage for test stage
        if stage.stage_type == Stage.TEST:
            steps.append({
                "uses": "codecov/codecov-action@v4",
                "with": {"fail_ci_if_error": False},
                "continue-on-error": True
            })

        job["steps"] = steps
        return job

    def _generate_gitlab_ci(self):
        """Generate GitLab CI configuration"""
        config: Dict[str, Any] = {
            "stages": [s.name for s in self.config.stages],
            "variables": {
                "DOCKER_TLS_CERTDIR": "/certs",
                "IMAGE_NAME": "$CI_REGISTRY_IMAGE",
                "VERSION": "$CI_COMMIT_SHORT_SHA"
            },
            "default": {
                "image": self._get_docker_image()
            }
        }

        # Add cache configuration
        if self.config.use_cache:
            lang_config = self.LANGUAGE_CONFIGS.get(self.config.language, {})
            cache_paths = lang_config.get("cache_paths", [])
            if cache_paths:
                config["cache"] = {
                    "key": "$CI_COMMIT_REF_SLUG",
                    "paths": cache_paths
                }

        # Add jobs for each stage
        for stage in self.config.stages:
            job_config = self._create_gitlab_job(stage)
            config[stage.name] = job_config

        yaml_content = self._dict_to_yaml(config)
        self.generated_files[".gitlab-ci.yml"] = yaml_content

    def _create_gitlab_job(self, stage: PipelineStage) -> Dict:
        """Create a GitLab CI job from a stage"""
        job: Dict[str, Any] = {
            "stage": stage.name,
            "script": stage.commands
        }

        # Add dependencies
        if stage.dependencies:
            job["needs"] = stage.dependencies

        # Add environment
        if stage.environment:
            job["environment"] = {
                "name": stage.environment,
                "url": f"https://{stage.environment}.example.com"
            }

        # Add rules for deploy stages
        if stage.stage_type == Stage.DEPLOY and stage.condition:
            rules = []
            for branch in stage.condition.split(","):
                branch = branch.strip()
                if branch.endswith("/*"):
                    rules.append({"if": f'$CI_COMMIT_BRANCH =~ /^{branch[:-2]}/'})
                else:
                    rules.append({"if": f'$CI_COMMIT_BRANCH == "{branch}"'})
            job["rules"] = rules

        # Add artifacts
        if stage.artifacts:
            job["artifacts"] = {
                "paths": stage.artifacts,
                "expire_in": "1 week"
            }

        # Add services for Docker
        if stage.stage_type in [Stage.PUBLISH] and self.project_info.has_docker:
            job["image"] = "docker:24.0.5"
            job["services"] = ["docker:24.0.5-dind"]
            job["before_script"] = [
                "docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY"
            ]

        return job

    def _generate_jenkinsfile(self):
        """Generate Jenkinsfile"""
        lines = [
            "pipeline {",
            "    agent any",
            "",
            "    environment {",
            "        REGISTRY = 'ghcr.io'",
            f"        IMAGE_NAME = '{self.project_info.name}'",
            "        VERSION = \"${env.BUILD_NUMBER}\"",
            "    }",
            "",
            "    options {",
            "        buildDiscarder(logRotator(numToKeepStr: '10'))",
            "        disableConcurrentBuilds()",
            "        timeout(time: 30, unit: 'MINUTES')",
            "    }",
            ""
        ]

        # Add tool configurations
        tools = []
        if self.config.language == Language.NODEJS:
            tools.append(f"        nodejs '{self.config.node_version}'")
        elif self.config.language == Language.JAVA:
            tools.append(f"        jdk 'JDK{self.config.java_version}'")
            tools.append("        maven 'Maven3'")
        elif self.config.language == Language.GO:
            tools.append(f"        go 'Go{self.config.go_version}'")

        if tools:
            lines.append("    tools {")
            lines.extend(tools)
            lines.append("    }")
            lines.append("")

        # Add stages
        lines.append("    stages {")

        for stage in self.config.stages:
            stage_lines = self._create_jenkins_stage(stage)
            lines.extend(stage_lines)

        lines.append("    }")
        lines.append("")

        # Add post actions
        lines.extend([
            "    post {",
            "        always {",
            "            cleanWs()",
            "        }",
            "        success {",
            "            echo 'Pipeline completed successfully!'",
            "        }",
            "        failure {",
            "            echo 'Pipeline failed!'",
            "        }",
            "    }",
            "}"
        ])

        self.generated_files["Jenkinsfile"] = "\n".join(lines)

    def _create_jenkins_stage(self, stage: PipelineStage) -> List[str]:
        """Create a Jenkins stage"""
        lines = [
            f"        stage('{stage.name.title()}') {{"
        ]

        # Add condition for deploy stages
        if stage.stage_type == Stage.DEPLOY and stage.condition:
            branches = stage.condition.split(",")
            branch_conditions = []
            for b in branches:
                b = b.strip()
                if b.endswith("/*"):
                    branch_conditions.append(f"env.BRANCH_NAME.startsWith('{b[:-2]}')")
                else:
                    branch_conditions.append(f"env.BRANCH_NAME == '{b}'")
            condition = " || ".join(branch_conditions)
            lines.append(f"            when {{ expression {{ {condition} }} }}")

        # Add environment
        if stage.environment:
            lines.extend([
                f"            environment {{",
                f"                DEPLOY_ENV = '{stage.environment}'",
                "            }"
            ])

        # Add steps
        lines.append("            steps {")
        for cmd in stage.commands:
            # Escape quotes for shell
            cmd_escaped = cmd.replace("'", "'\"'\"'")
            lines.append(f"                sh '{cmd_escaped}'")
        lines.append("            }")
        lines.append("        }")
        lines.append("")

        return lines

    def _generate_circleci(self):
        """Generate CircleCI configuration"""
        config: Dict[str, Any] = {
            "version": 2.1,
            "orbs": {},
            "jobs": {},
            "workflows": {
                "build-test-deploy": {
                    "jobs": []
                }
            }
        }

        # Add orbs based on language
        if self.config.language == Language.NODEJS:
            config["orbs"]["node"] = "circleci/node@5.1"
        elif self.config.language == Language.PYTHON:
            config["orbs"]["python"] = "circleci/python@2.1"
        elif self.config.language == Language.GO:
            config["orbs"]["go"] = "circleci/go@1.7"

        # Add Docker orb if needed
        if self.project_info.has_docker:
            config["orbs"]["docker"] = "circleci/docker@2.4"

        # Create jobs
        for stage in self.config.stages:
            job = self._create_circleci_job(stage)
            config["jobs"][stage.name] = job

            # Add to workflow
            workflow_job: Dict[str, Any] = {stage.name: {}}
            if stage.dependencies:
                workflow_job[stage.name]["requires"] = stage.dependencies

            # Add filters for deploy stages
            if stage.stage_type == Stage.DEPLOY and stage.condition:
                branches = stage.condition.split(",")
                branch_filters = []
                for b in branches:
                    b = b.strip()
                    if b.endswith("/*"):
                        branch_filters.append(f"/^{b[:-2]}.*$/")
                    else:
                        branch_filters.append(b)
                workflow_job[stage.name]["filters"] = {
                    "branches": {"only": branch_filters}
                }

            config["workflows"]["build-test-deploy"]["jobs"].append(workflow_job)

        yaml_content = self._dict_to_yaml(config)
        self.generated_files[".circleci/config.yml"] = yaml_content

    def _create_circleci_job(self, stage: PipelineStage) -> Dict:
        """Create a CircleCI job from a stage"""
        job: Dict[str, Any] = {
            "docker": [{"image": self._get_docker_image()}],
            "steps": ["checkout"]
        }

        # Add language-specific setup
        if self.config.language == Language.NODEJS:
            job["steps"].append({"node/install-packages": {}})
        elif self.config.language == Language.PYTHON:
            job["steps"].append({
                "python/install-packages": {
                    "pkg-manager": self.project_info.package_manager
                }
            })

        # Add commands
        for cmd in stage.commands:
            job["steps"].append({"run": cmd})

        # Add artifacts
        if stage.artifacts:
            job["steps"].append({
                "store_artifacts": {
                    "path": stage.artifacts[0] if stage.artifacts else "dist"
                }
            })

        return job

    def _get_docker_image(self) -> str:
        """Get the Docker image for the language"""
        lang_config = self.LANGUAGE_CONFIGS.get(self.config.language, {})
        return lang_config.get("docker_base", "ubuntu:22.04")

    def _dict_to_yaml(self, data: Dict, indent: int = 0) -> str:
        """Convert a dictionary to YAML string (simple implementation)"""
        lines = []
        prefix = "  " * indent

        for key, value in data.items():
            if isinstance(value, dict):
                lines.append(f"{prefix}{key}:")
                lines.append(self._dict_to_yaml(value, indent + 1))
            elif isinstance(value, list):
                lines.append(f"{prefix}{key}:")
                for item in value:
                    if isinstance(item, dict):
                        # Check if single-key dict (common in workflows)
                        if len(item) == 1:
                            item_key = list(item.keys())[0]
                            item_value = item[item_key]
                            if isinstance(item_value, dict) and item_value:
                                lines.append(f"{prefix}  - {item_key}:")
                                for k, v in item_value.items():
                                    if isinstance(v, list):
                                        lines.append(f"{prefix}      {k}:")
                                        for vi in v:
                                            lines.append(f"{prefix}        - {self._format_value(vi)}")
                                    elif isinstance(v, dict):
                                        lines.append(f"{prefix}      {k}:")
                                        for vk, vv in v.items():
                                            if isinstance(vv, list):
                                                lines.append(f"{prefix}        {vk}:")
                                                for vvi in vv:
                                                    lines.append(f"{prefix}          - {self._format_value(vvi)}")
                                            else:
                                                lines.append(f"{prefix}        {vk}: {self._format_value(vv)}")
                                    else:
                                        lines.append(f"{prefix}      {k}: {self._format_value(v)}")
                            else:
                                lines.append(f"{prefix}  - {item_key}")
                        else:
                            lines.append(f"{prefix}  -")
                            for k, v in item.items():
                                if isinstance(v, dict):
                                    lines.append(f"{prefix}    {k}:")
                                    for kk, vv in v.items():
                                        lines.append(f"{prefix}      {kk}: {self._format_value(vv)}")
                                else:
                                    lines.append(f"{prefix}    {k}: {self._format_value(v)}")
                    else:
                        lines.append(f"{prefix}  - {self._format_value(item)}")
            else:
                lines.append(f"{prefix}{key}: {self._format_value(value)}")

        return "\n".join(lines)

    def _format_value(self, value: Any) -> str:
        """Format a value for YAML output"""
        if value is None:
            return "null"
        elif isinstance(value, bool):
            return "true" if value else "false"
        elif isinstance(value, (int, float)):
            return str(value)
        elif isinstance(value, str):
            # Quote strings with special characters
            if any(c in value for c in [":", "#", "[", "]", "{", "}", ",", "&", "*", "?", "|", "-", "<", ">", "=", "!", "%", "@", "`", "'", '"', "\n"]):
                return f'"{value}"'
            elif value.startswith("$"):
                return f'"{value}"'
            return value
        return str(value)


class OutputFormatter:
    """Format output in different formats"""

    @staticmethod
    def format_text(results: Dict, verbose: bool = False) -> str:
        """Format results as human-readable text"""
        lines = []
        lines.append("=" * 80)
        lines.append("PIPELINE GENERATOR REPORT")
        lines.append("=" * 80)
        lines.append("")

        # Project info
        project = results.get("project", {})
        lines.append("PROJECT INFORMATION")
        lines.append("-" * 40)
        lines.append(f"Name:            {project.get('name', 'N/A')}")
        lines.append(f"Language:        {project.get('language', 'N/A')}")
        lines.append(f"Package Manager: {project.get('package_manager', 'N/A')}")
        lines.append(f"Has Docker:      {project.get('has_docker', False)}")
        lines.append(f"Has Tests:       {project.get('has_tests', False)}")
        lines.append("")

        # Pipeline info
        pipeline = results.get("pipeline", {})
        lines.append("PIPELINE CONFIGURATION")
        lines.append("-" * 40)
        lines.append(f"Platform:        {pipeline.get('platform', 'N/A')}")
        lines.append(f"Stages:          {', '.join(pipeline.get('stages', []))}")
        lines.append(f"Environments:    {', '.join(pipeline.get('environments', []))}")
        lines.append(f"Deploy Target:   {pipeline.get('deploy_target', 'N/A')}")
        lines.append("")

        # Generated files
        files = results.get("files", [])
        lines.append("GENERATED FILES")
        lines.append("-" * 40)
        for f in files:
            lines.append(f"  - {f}")
        lines.append("")

        # Show content if verbose
        if verbose:
            content = results.get("content", {})
            for filename, file_content in content.items():
                lines.append(f"FILE: {filename}")
                lines.append("-" * 40)
                lines.append(file_content)
                lines.append("")

        lines.append("=" * 80)
        return "\n".join(lines)

    @staticmethod
    def format_json(results: Dict) -> str:
        """Format results as JSON"""
        return json.dumps(results, indent=2, default=str)

    @staticmethod
    def format_yaml_only(results: Dict) -> str:
        """Return only the generated YAML content"""
        content = results.get("content", {})
        if content:
            return list(content.values())[0]
        return ""


def main():
    """Main entry point with standardized CLI interface"""
    parser = argparse.ArgumentParser(
        description="Pipeline Generator - Generate CI/CD pipeline configurations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --input ./my-project --platform github
  %(prog)s --input ./project --platform gitlab --language python --stages build,test,deploy
  %(prog)s --input . --platform github --deploy-target kubernetes --environments dev,staging,prod
  %(prog)s --input ./app -p github -l nodejs -s build,test,scan,deploy -d ecs -o yaml -f ci.yml

Platforms:
  github      GitHub Actions (.github/workflows/ci-cd.yml)
  gitlab      GitLab CI (.gitlab-ci.yml)
  jenkins     Jenkinsfile
  circleci    CircleCI (.circleci/config.yml)

Languages:
  nodejs      Node.js / TypeScript (auto-detects npm/yarn/pnpm)
  python      Python (auto-detects pip/poetry/pipenv)
  go          Go
  java        Java (auto-detects Maven/Gradle)
  docker      Docker-only (no language runtime)

Stages:
  build       Compile/build the application
  test        Run unit and integration tests
  scan        Security scanning and linting
  publish     Build and push Docker images
  deploy      Deploy to target environment

Deploy Targets:
  kubernetes    Kubernetes (kubectl)
  ecs           AWS ECS
  docker-compose Docker Compose
  serverless    Serverless Framework / AWS Lambda
  none          No deployment (CI only)
        """
    )

    parser.add_argument(
        "--input", "-i",
        required=True,
        dest="target",
        help="Project directory to analyze"
    )

    parser.add_argument(
        "--platform", "-p",
        required=True,
        choices=["github", "gitlab", "jenkins", "circleci"],
        help="Target CI/CD platform"
    )

    parser.add_argument(
        "--language", "-l",
        choices=["nodejs", "python", "go", "java", "docker"],
        help="Primary language (auto-detected if not specified)"
    )

    parser.add_argument(
        "--stages", "-s",
        default="build,test",
        help="Comma-separated pipeline stages (default: build,test)"
    )

    parser.add_argument(
        "--environments", "-e",
        default="dev,staging,prod",
        help="Comma-separated environments for deployment (default: dev,staging,prod)"
    )

    parser.add_argument(
        "--deploy-target", "-d",
        choices=["kubernetes", "ecs", "docker-compose", "serverless", "none"],
        default="none",
        help="Deployment target (default: none)"
    )

    parser.add_argument(
        "--output", "-o",
        choices=["text", "json", "yaml"],
        default="text",
        help="Output format (default: text)"
    )

    parser.add_argument(
        "--file", "-f",
        help="Write output to file instead of stdout"
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )

    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 1.0.0"
    )

    args = parser.parse_args()

    # Parse stages and environments
    stages = [s.strip() for s in args.stages.split(",")]
    environments = [e.strip() for e in args.environments.split(",")]

    try:
        generator = PipelineGenerator(
            target_path=args.target,
            platform=args.platform,
            language=args.language,
            stages=stages,
            environments=environments,
            deploy_target=args.deploy_target,
            verbose=args.verbose
        )

        results = generator.run()

        # Format output
        if args.output == "json":
            output = OutputFormatter.format_json(results)
        elif args.output == "yaml":
            output = OutputFormatter.format_yaml_only(results)
        else:
            output = OutputFormatter.format_text(results, verbose=args.verbose)

        # Write output
        if args.file:
            with open(args.file, "w") as f:
                f.write(output)
            print(f"Results written to {args.file}", file=sys.stderr)
        else:
            print(output)

        sys.exit(0)

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
