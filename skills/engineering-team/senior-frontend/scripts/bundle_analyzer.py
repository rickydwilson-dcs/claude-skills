#!/usr/bin/env python3
"""
Bundle Analyzer - Frontend bundle size analysis and optimization recommendations.

Analyzes frontend projects to identify:
- Heavy dependencies with lighter alternatives
- Bundle size estimation and breakdown
- Code splitting opportunities
- Tree-shaking recommendations

Works with Next.js, Vite, Create React App, Nuxt, and Angular projects.
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
from typing import Any, Dict, List, Optional, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SeverityLevel(Enum):
    """Issue severity levels."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


@dataclass
class DependencyInfo:
    """Information about a package dependency."""
    name: str
    version: str
    size_kb: float
    is_dev: bool = False
    has_lighter_alternative: bool = False
    alternative_name: Optional[str] = None
    alternative_size_kb: Optional[float] = None
    potential_savings_kb: float = 0.0
    tree_shakeable: bool = True
    notes: str = ""


@dataclass
class BundleIssue:
    """Identified issue with the bundle."""
    severity: SeverityLevel
    category: str  # "size", "duplicate", "tree-shaking", "code-splitting", "heavy-dep"
    title: str
    description: str
    file_path: Optional[str] = None
    potential_savings_kb: float = 0.0
    recommendation: str = ""


@dataclass
class ChunkInfo:
    """Information about a bundle chunk/file."""
    name: str
    path: str
    size_bytes: int
    size_kb: float
    file_type: str  # "js", "css", "map", "other"
    is_vendor: bool = False
    is_entry: bool = False


@dataclass
class AnalyzerConfig:
    """Configuration for bundle analysis."""
    target_path: Path
    size_threshold_kb: int = 500
    include_sourcemaps: bool = False
    analyze_node_modules: bool = True
    verbose: bool = False


@dataclass
class BundleAnalysisResult:
    """Complete analysis results."""
    target_path: str
    framework_detected: Optional[str]
    total_size_bytes: int
    total_size_kb: float
    total_size_mb: float
    js_size_kb: float
    css_size_kb: float
    other_size_kb: float
    chunks: List[ChunkInfo]
    dependencies: List[DependencyInfo]
    issues: List[BundleIssue]
    recommendations: List[str]
    optimization_potential_kb: float
    analysis_timestamp: str
    score: int  # 0-100
    dependency_count: int = 0
    dev_dependency_count: int = 0


class BundleAnalyzer:
    """
    Frontend bundle analysis tool for identifying size optimization opportunities.

    Analyzes:
    - package.json for dependency sizes and alternatives
    - Build directories (.next/, dist/, build/) for chunk sizes
    - Source files for code-splitting opportunities
    - node_modules for actual installed sizes
    """

    # Known heavy dependencies with lighter alternatives
    HEAVY_DEPENDENCIES: Dict[str, Dict[str, Any]] = {
        "moment": {
            "alternative": "date-fns",
            "typical_size_kb": 68,
            "alt_size_kb": 12,
            "tree_shakeable": False,
            "notes": "date-fns is modular and tree-shakeable"
        },
        "moment-timezone": {
            "alternative": "date-fns-tz",
            "typical_size_kb": 183,
            "alt_size_kb": 15,
            "tree_shakeable": False,
            "notes": "date-fns-tz with date-fns is much smaller"
        },
        "lodash": {
            "alternative": "lodash-es",
            "typical_size_kb": 72,
            "alt_size_kb": 8,
            "tree_shakeable": False,
            "notes": "Use lodash-es and import specific functions"
        },
        "underscore": {
            "alternative": "lodash-es or native JS",
            "typical_size_kb": 24,
            "alt_size_kb": 0,
            "tree_shakeable": False,
            "notes": "Most underscore methods have native equivalents"
        },
        "jquery": {
            "alternative": "Native DOM APIs",
            "typical_size_kb": 87,
            "alt_size_kb": 0,
            "tree_shakeable": False,
            "notes": "Modern browsers have excellent DOM APIs"
        },
        "rxjs": {
            "alternative": "Consider smaller reactive lib",
            "typical_size_kb": 95,
            "alt_size_kb": 20,
            "tree_shakeable": True,
            "notes": "Import operators individually from rxjs/operators"
        },
        "chart.js": {
            "alternative": "Dynamic import",
            "typical_size_kb": 166,
            "alt_size_kb": 0,
            "tree_shakeable": False,
            "notes": "Lazy load charts only when needed"
        },
        "three": {
            "alternative": "Dynamic import",
            "typical_size_kb": 500,
            "alt_size_kb": 0,
            "tree_shakeable": True,
            "notes": "Always dynamically import Three.js"
        },
        "antd": {
            "alternative": "Import individual components",
            "typical_size_kb": 1200,
            "alt_size_kb": 100,
            "tree_shakeable": True,
            "notes": "Use babel-plugin-import for automatic tree-shaking"
        },
        "@ant-design/icons": {
            "alternative": "Import individual icons",
            "typical_size_kb": 500,
            "alt_size_kb": 10,
            "tree_shakeable": True,
            "notes": "Import only needed icons"
        },
        "@material-ui/core": {
            "alternative": "@mui/material with tree-shaking",
            "typical_size_kb": 800,
            "alt_size_kb": 80,
            "tree_shakeable": True,
            "notes": "Upgrade to @mui and use path imports"
        },
        "@mui/material": {
            "alternative": "Use path imports",
            "typical_size_kb": 400,
            "alt_size_kb": 60,
            "tree_shakeable": True,
            "notes": "Import from @mui/material/Button instead of @mui/material"
        },
        "aws-sdk": {
            "alternative": "@aws-sdk/* v3 modules",
            "typical_size_kb": 3000,
            "alt_size_kb": 50,
            "tree_shakeable": False,
            "notes": "AWS SDK v3 is modular - import only needed services"
        },
        "firebase": {
            "alternative": "firebase/* modular imports",
            "typical_size_kb": 500,
            "alt_size_kb": 50,
            "tree_shakeable": True,
            "notes": "Use modular Firebase v9+ imports"
        },
        "dayjs": {
            "alternative": None,
            "typical_size_kb": 2,
            "alt_size_kb": 0,
            "tree_shakeable": True,
            "notes": "Already lightweight - good choice!"
        },
        "date-fns": {
            "alternative": None,
            "typical_size_kb": 12,
            "alt_size_kb": 0,
            "tree_shakeable": True,
            "notes": "Already modular - good choice!"
        },
    }

    # Framework detection patterns
    FRAMEWORK_PATTERNS: Dict[str, List[str]] = {
        "nextjs": [".next", "next.config.js", "next.config.mjs", "next.config.ts"],
        "vite": ["vite.config.js", "vite.config.ts", "vite.config.mjs"],
        "cra": ["react-scripts"],  # Detected from package.json
        "nuxt": [".nuxt", "nuxt.config.js", "nuxt.config.ts"],
        "angular": ["angular.json", ".angular"],
        "remix": ["remix.config.js"],
        "gatsby": ["gatsby-config.js", "gatsby-config.ts"],
    }

    # Build output directories by framework
    BUILD_DIRS: Dict[str, List[str]] = {
        "nextjs": [".next/static", ".next/server"],
        "vite": ["dist", "dist/assets"],
        "cra": ["build/static"],
        "nuxt": [".nuxt/dist", ".output"],
        "angular": ["dist/browser", "dist"],
        "remix": ["build", "public/build"],
        "gatsby": ["public", ".cache"],
    }

    def __init__(self, config: AnalyzerConfig):
        self.config = config
        self.results: Optional[BundleAnalysisResult] = None

    def analyze(self) -> BundleAnalysisResult:
        """Execute complete bundle analysis."""
        if self.config.verbose:
            print(f"Analyzing: {self.config.target_path}")

        # Detect framework
        framework = self._detect_framework()
        if self.config.verbose:
            print(f"Framework detected: {framework or 'Unknown'}")

        # Parse package.json
        package_data = self._parse_package_json()

        # Analyze dependencies
        dependencies = self._analyze_dependencies(package_data)

        # Scan build directory for chunks
        chunks = self._scan_build_directory(framework)

        # Identify issues
        issues = self._identify_issues(dependencies, chunks, package_data)

        # Generate recommendations
        recommendations = self._generate_recommendations(issues)

        # Calculate totals
        total_bytes = sum(c.size_bytes for c in chunks)
        js_bytes = sum(c.size_bytes for c in chunks if c.file_type == "js")
        css_bytes = sum(c.size_bytes for c in chunks if c.file_type == "css")
        other_bytes = total_bytes - js_bytes - css_bytes

        # Calculate optimization potential
        optimization_potential = sum(i.potential_savings_kb for i in issues)

        # Calculate score
        score = self._calculate_score(issues, total_bytes)

        # Count dependencies
        dep_count = len(package_data.get("dependencies", {}))
        dev_dep_count = len(package_data.get("devDependencies", {}))

        self.results = BundleAnalysisResult(
            target_path=str(self.config.target_path),
            framework_detected=framework,
            total_size_bytes=total_bytes,
            total_size_kb=round(total_bytes / 1024, 2),
            total_size_mb=round(total_bytes / (1024 * 1024), 2),
            js_size_kb=round(js_bytes / 1024, 2),
            css_size_kb=round(css_bytes / 1024, 2),
            other_size_kb=round(other_bytes / 1024, 2),
            chunks=chunks,
            dependencies=dependencies,
            issues=issues,
            recommendations=recommendations,
            optimization_potential_kb=round(optimization_potential, 2),
            analysis_timestamp=datetime.now().isoformat(),
            score=score,
            dependency_count=dep_count,
            dev_dependency_count=dev_dep_count,
        )

        return self.results

    def _detect_framework(self) -> Optional[str]:
        """Detect frontend framework from project structure."""
        target = self.config.target_path

        # Check for marker files/directories
        for framework, patterns in self.FRAMEWORK_PATTERNS.items():
            for pattern in patterns:
                check_path = target / pattern
                if check_path.exists():
                    return framework

        # Check package.json for framework hints
        package_json = target / "package.json"
        if package_json.exists():
            try:
                with open(package_json, 'r') as f:
                    data = json.load(f)
                deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}

                if "next" in deps:
                    return "nextjs"
                elif "nuxt" in deps:
                    return "nuxt"
                elif "react-scripts" in deps:
                    return "cra"
                elif "@angular/core" in deps:
                    return "angular"
                elif "vite" in deps:
                    return "vite"
                elif "@remix-run/react" in deps:
                    return "remix"
                elif "gatsby" in deps:
                    return "gatsby"
            except (json.JSONDecodeError, IOError):
                pass

        return None

    def _parse_package_json(self) -> Dict[str, Any]:
        """Parse and extract dependency information from package.json."""
        package_json = self.config.target_path / "package.json"

        if not package_json.exists():
            if self.config.verbose:
                print("Warning: package.json not found")
            return {}

        try:
            with open(package_json, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            if self.config.verbose:
                print(f"Warning: Could not parse package.json: {e}")
            return {}

    def _analyze_dependencies(self, package_data: Dict[str, Any]) -> List[DependencyInfo]:
        """Analyze dependencies for size and alternatives."""
        dependencies: List[DependencyInfo] = []

        # Process production dependencies
        for name, version in package_data.get("dependencies", {}).items():
            dep_info = self._analyze_single_dependency(name, version, is_dev=False)
            dependencies.append(dep_info)

        # Process dev dependencies (lower priority for size concerns)
        for name, version in package_data.get("devDependencies", {}).items():
            dep_info = self._analyze_single_dependency(name, version, is_dev=True)
            dependencies.append(dep_info)

        # Sort by size (largest first)
        dependencies.sort(key=lambda d: d.size_kb, reverse=True)

        return dependencies

    def _analyze_single_dependency(self, name: str, version: str, is_dev: bool) -> DependencyInfo:
        """Analyze a single dependency."""
        # Check if it's a known heavy dependency
        heavy_info = self.HEAVY_DEPENDENCIES.get(name)

        # Estimate size
        if heavy_info:
            size_kb = heavy_info["typical_size_kb"]
            has_alternative = heavy_info["alternative"] is not None
            alt_name = heavy_info["alternative"]
            alt_size = heavy_info["alt_size_kb"]
            savings = size_kb - alt_size if has_alternative else 0
            tree_shakeable = heavy_info["tree_shakeable"]
            notes = heavy_info["notes"]
        else:
            # Try to estimate from node_modules
            size_kb = self._estimate_dependency_size(name)
            has_alternative = False
            alt_name = None
            alt_size = None
            savings = 0.0
            tree_shakeable = True
            notes = ""

        return DependencyInfo(
            name=name,
            version=version,
            size_kb=size_kb,
            is_dev=is_dev,
            has_lighter_alternative=has_alternative,
            alternative_name=alt_name,
            alternative_size_kb=alt_size,
            potential_savings_kb=savings,
            tree_shakeable=tree_shakeable,
            notes=notes,
        )

    def _estimate_dependency_size(self, name: str) -> float:
        """Estimate size of a dependency from node_modules or heuristics."""
        if not self.config.analyze_node_modules:
            return 0.0

        node_modules = self.config.target_path / "node_modules" / name
        if not node_modules.exists():
            # Try scoped package
            if name.startswith("@"):
                parts = name.split("/")
                if len(parts) == 2:
                    node_modules = self.config.target_path / "node_modules" / parts[0] / parts[1]

        if node_modules.exists():
            total_size = 0
            try:
                for root, dirs, files in os.walk(node_modules):
                    # Skip nested node_modules
                    if "node_modules" in dirs:
                        dirs.remove("node_modules")
                    for file in files:
                        if file.endswith(('.js', '.mjs', '.cjs')):
                            file_path = Path(root) / file
                            try:
                                total_size += file_path.stat().st_size
                            except OSError:
                                pass
                return round(total_size / 1024, 2)
            except OSError:
                pass

        return 0.0

    def _scan_build_directory(self, framework: Optional[str]) -> List[ChunkInfo]:
        """Scan build output for chunk information."""
        chunks: List[ChunkInfo] = []

        # Determine which directories to scan
        if framework and framework in self.BUILD_DIRS:
            build_dirs = self.BUILD_DIRS[framework]
        else:
            # Try common build directories
            build_dirs = ["dist", "build", ".next/static", ".nuxt/dist", "public"]

        for build_dir in build_dirs:
            dir_path = self.config.target_path / build_dir
            if dir_path.exists():
                chunks.extend(self._scan_directory(dir_path))

        # Sort by size (largest first)
        chunks.sort(key=lambda c: c.size_bytes, reverse=True)

        return chunks

    def _scan_directory(self, directory: Path) -> List[ChunkInfo]:
        """Recursively scan a directory for bundle files."""
        chunks: List[ChunkInfo] = []

        try:
            for item in directory.rglob("*"):
                if item.is_file():
                    # Skip sourcemaps unless requested
                    if item.suffix == ".map" and not self.config.include_sourcemaps:
                        continue

                    # Determine file type
                    if item.suffix in (".js", ".mjs", ".cjs"):
                        file_type = "js"
                    elif item.suffix == ".css":
                        file_type = "css"
                    elif item.suffix == ".map":
                        file_type = "map"
                    else:
                        file_type = "other"

                    # Skip non-bundle files
                    if file_type == "other" and item.suffix not in (".woff", ".woff2", ".ttf", ".png", ".jpg", ".svg"):
                        continue

                    try:
                        size_bytes = item.stat().st_size
                    except OSError:
                        continue

                    # Detect vendor chunks
                    is_vendor = any(v in item.name.lower() for v in ["vendor", "node_modules", "chunk-"])

                    # Detect entry points
                    is_entry = any(e in item.name.lower() for e in ["main", "index", "app", "entry", "_app"])

                    chunks.append(ChunkInfo(
                        name=item.name,
                        path=str(item.relative_to(self.config.target_path)),
                        size_bytes=size_bytes,
                        size_kb=round(size_bytes / 1024, 2),
                        file_type=file_type,
                        is_vendor=is_vendor,
                        is_entry=is_entry,
                    ))
        except OSError as e:
            if self.config.verbose:
                print(f"Warning: Could not scan {directory}: {e}")

        return chunks

    def _identify_issues(
        self,
        dependencies: List[DependencyInfo],
        chunks: List[ChunkInfo],
        package_data: Dict[str, Any]
    ) -> List[BundleIssue]:
        """Identify optimization issues."""
        issues: List[BundleIssue] = []

        # Check for heavy dependencies with alternatives
        for dep in dependencies:
            if dep.has_lighter_alternative and not dep.is_dev and dep.potential_savings_kb > 10:
                severity = SeverityLevel.ERROR if dep.potential_savings_kb > 50 else SeverityLevel.WARNING
                issues.append(BundleIssue(
                    severity=severity,
                    category="heavy-dep",
                    title=f"Heavy dependency: {dep.name}",
                    description=f"{dep.name} ({dep.size_kb}KB) has a lighter alternative",
                    potential_savings_kb=dep.potential_savings_kb,
                    recommendation=f"Replace with {dep.alternative_name} ({dep.alternative_size_kb}KB). {dep.notes}",
                ))

        # Check for non-tree-shakeable imports
        for dep in dependencies:
            if not dep.tree_shakeable and not dep.is_dev and dep.size_kb > 20:
                issues.append(BundleIssue(
                    severity=SeverityLevel.WARNING,
                    category="tree-shaking",
                    title=f"Non-tree-shakeable: {dep.name}",
                    description=f"{dep.name} cannot be tree-shaken, entire package is bundled",
                    potential_savings_kb=dep.size_kb * 0.5,  # Estimate 50% could be saved
                    recommendation=dep.notes or "Consider using a modular alternative",
                ))

        # Check for large chunks that could be split
        for chunk in chunks:
            if chunk.file_type == "js" and chunk.size_kb > self.config.size_threshold_kb and not chunk.is_vendor:
                issues.append(BundleIssue(
                    severity=SeverityLevel.WARNING,
                    category="code-splitting",
                    title=f"Large chunk: {chunk.name}",
                    description=f"Chunk is {chunk.size_kb}KB, exceeds threshold of {self.config.size_threshold_kb}KB",
                    file_path=chunk.path,
                    potential_savings_kb=chunk.size_kb * 0.3,  # Estimate 30% could be deferred
                    recommendation="Consider lazy loading with dynamic imports",
                ))

        # Check for duplicate React
        deps = package_data.get("dependencies", {})
        if "react" in deps and "preact" in deps:
            issues.append(BundleIssue(
                severity=SeverityLevel.ERROR,
                category="duplicate",
                title="Multiple React-like libraries",
                description="Both react and preact are installed",
                potential_savings_kb=40,
                recommendation="Use only one React-like library",
            ))

        # Check for both moment and date-fns
        if "moment" in deps and "date-fns" in deps:
            issues.append(BundleIssue(
                severity=SeverityLevel.WARNING,
                category="duplicate",
                title="Duplicate date libraries",
                description="Both moment and date-fns are installed",
                potential_savings_kb=68,
                recommendation="Migrate fully to date-fns and remove moment",
            ))

        # Check for deprecated packages
        deprecated = ["request", "node-sass", "node-uuid", "colors"]
        for pkg in deprecated:
            if pkg in deps:
                issues.append(BundleIssue(
                    severity=SeverityLevel.INFO,
                    category="deprecated",
                    title=f"Deprecated package: {pkg}",
                    description=f"{pkg} is deprecated and should be replaced",
                    recommendation="See npm page for recommended alternatives",
                ))

        # Sort by potential savings
        issues.sort(key=lambda i: i.potential_savings_kb, reverse=True)

        return issues

    def _generate_recommendations(self, issues: List[BundleIssue]) -> List[str]:
        """Generate actionable recommendations from issues."""
        recommendations: List[str] = []

        # Group by category
        heavy_deps = [i for i in issues if i.category == "heavy-dep"]
        tree_shake = [i for i in issues if i.category == "tree-shaking"]
        code_split = [i for i in issues if i.category == "code-splitting"]

        if heavy_deps:
            total_savings = sum(i.potential_savings_kb for i in heavy_deps)
            recommendations.append(
                f"Replace {len(heavy_deps)} heavy dependencies for ~{total_savings:.0f}KB savings"
            )
            # Add top 3 specific recommendations
            for issue in heavy_deps[:3]:
                recommendations.append(f"  - {issue.recommendation}")

        if tree_shake:
            total_savings = sum(i.potential_savings_kb for i in tree_shake)
            recommendations.append(
                f"Enable tree-shaking for {len(tree_shake)} packages (~{total_savings:.0f}KB potential savings)"
            )

        if code_split:
            total_savings = sum(i.potential_savings_kb for i in code_split)
            recommendations.append(
                f"Split {len(code_split)} large chunks with dynamic imports (~{total_savings:.0f}KB deferrable)"
            )

        # General recommendations
        if not recommendations:
            recommendations.append("Bundle looks well-optimized! No major issues found.")

        return recommendations

    def _calculate_score(self, issues: List[BundleIssue], total_bytes: int) -> int:
        """Calculate bundle health score 0-100."""
        score = 100

        # Deduct points based on issue severity
        for issue in issues:
            if issue.severity == SeverityLevel.ERROR:
                score -= 15
            elif issue.severity == SeverityLevel.WARNING:
                score -= 8
            elif issue.severity == SeverityLevel.INFO:
                score -= 2

        # Penalize very large bundles
        total_kb = total_bytes / 1024
        if total_kb > 5000:  # > 5MB
            score -= 20
        elif total_kb > 2000:  # > 2MB
            score -= 10
        elif total_kb > 1000:  # > 1MB
            score -= 5

        return max(0, min(100, score))


def format_text_output(result: BundleAnalysisResult, verbose: bool = False) -> str:
    """Format results as human-readable text."""
    lines = []

    lines.append("=" * 80)
    lines.append("BUNDLE ANALYSIS REPORT")
    lines.append("=" * 80)
    lines.append("")
    lines.append(f"Project: {result.target_path}")
    lines.append(f"Framework: {result.framework_detected or 'Unknown'}")
    lines.append(f"Analyzed: {result.analysis_timestamp}")
    lines.append("")

    # Size summary
    lines.append("BUNDLE SIZE SUMMARY")
    lines.append("-" * 80)
    if result.total_size_bytes > 0:
        lines.append(f"  Total Size:       {result.total_size_mb:.2f} MB ({result.total_size_kb:.0f} KB)")
        lines.append(f"  JavaScript:       {result.js_size_kb:.0f} KB")
        lines.append(f"  CSS:              {result.css_size_kb:.0f} KB")
        lines.append(f"  Other:            {result.other_size_kb:.0f} KB")
    else:
        lines.append("  No build output found. Run your build command first.")
    lines.append("")

    # Largest chunks
    if result.chunks:
        lines.append("LARGEST CHUNKS")
        lines.append("-" * 80)
        for i, chunk in enumerate(result.chunks[:10], 1):
            flags = []
            if chunk.is_entry:
                flags.append("entry")
            if chunk.is_vendor:
                flags.append("vendor")
            flag_str = f" [{', '.join(flags)}]" if flags else ""
            lines.append(f"  {i:2}. {chunk.name:<40} {chunk.size_kb:>8.1f} KB{flag_str}")
        if len(result.chunks) > 10:
            lines.append(f"      ... and {len(result.chunks) - 10} more")
        lines.append("")

    # Dependencies
    if result.dependencies:
        prod_deps = [d for d in result.dependencies if not d.is_dev and d.size_kb > 0]
        if prod_deps:
            lines.append("TOP DEPENDENCIES BY SIZE (Production)")
            lines.append("-" * 80)
            for i, dep in enumerate(prod_deps[:10], 1):
                warning = ""
                if dep.has_lighter_alternative:
                    warning = f" [Use {dep.alternative_name} instead]"
                elif not dep.tree_shakeable:
                    warning = " [Not tree-shakeable]"
                lines.append(f"  {i:2}. {dep.name:<35} {dep.size_kb:>8.1f} KB{warning}")
            lines.append("")

    # Issues
    if result.issues:
        error_count = len([i for i in result.issues if i.severity == SeverityLevel.ERROR])
        warn_count = len([i for i in result.issues if i.severity == SeverityLevel.WARNING])
        info_count = len([i for i in result.issues if i.severity == SeverityLevel.INFO])

        lines.append(f"ISSUES FOUND ({error_count} errors, {warn_count} warnings, {info_count} info)")
        lines.append("-" * 80)

        for issue in result.issues[:15]:
            severity_icon = {
                SeverityLevel.ERROR: "ERROR",
                SeverityLevel.WARNING: "WARN ",
                SeverityLevel.INFO: "INFO ",
            }[issue.severity]

            lines.append(f"  [{severity_icon}] {issue.title}")
            if verbose:
                lines.append(f"          {issue.description}")
            if issue.potential_savings_kb > 0:
                lines.append(f"          Potential savings: {issue.potential_savings_kb:.0f} KB")
            lines.append(f"          Recommendation: {issue.recommendation}")
            lines.append("")

        if len(result.issues) > 15:
            lines.append(f"  ... and {len(result.issues) - 15} more issues")
            lines.append("")

    # Recommendations
    if result.recommendations:
        lines.append("OPTIMIZATION RECOMMENDATIONS")
        lines.append("-" * 80)
        for rec in result.recommendations:
            lines.append(f"  {rec}")
        lines.append("")

    # Summary
    lines.append("SUMMARY")
    lines.append("-" * 80)
    lines.append(f"  Dependencies: {result.dependency_count} production, {result.dev_dependency_count} dev")
    lines.append(f"  Optimization Potential: {result.optimization_potential_kb:.0f} KB")
    lines.append(f"  Bundle Health Score: {result.score}/100")
    lines.append("")
    lines.append("=" * 80)

    return "\n".join(lines)


def format_json_output(result: BundleAnalysisResult) -> str:
    """Format results as JSON."""
    data = {
        "metadata": {
            "tool": "bundle_analyzer",
            "version": "1.0.0",
            "timestamp": result.analysis_timestamp,
            "target": result.target_path,
            "framework": result.framework_detected,
        },
        "summary": {
            "total_size_bytes": result.total_size_bytes,
            "total_size_kb": result.total_size_kb,
            "total_size_mb": result.total_size_mb,
            "js_size_kb": result.js_size_kb,
            "css_size_kb": result.css_size_kb,
            "other_size_kb": result.other_size_kb,
            "dependency_count": result.dependency_count,
            "dev_dependency_count": result.dev_dependency_count,
            "score": result.score,
            "optimization_potential_kb": result.optimization_potential_kb,
        },
        "chunks": [
            {
                "name": c.name,
                "path": c.path,
                "size_bytes": c.size_bytes,
                "size_kb": c.size_kb,
                "type": c.file_type,
                "is_vendor": c.is_vendor,
                "is_entry": c.is_entry,
            }
            for c in result.chunks
        ],
        "dependencies": [
            {
                "name": d.name,
                "version": d.version,
                "size_kb": d.size_kb,
                "is_dev": d.is_dev,
                "has_alternative": d.has_lighter_alternative,
                "alternative": d.alternative_name,
                "alternative_size_kb": d.alternative_size_kb,
                "potential_savings_kb": d.potential_savings_kb,
                "tree_shakeable": d.tree_shakeable,
            }
            for d in result.dependencies
        ],
        "issues": [
            {
                "severity": i.severity.value,
                "category": i.category,
                "title": i.title,
                "description": i.description,
                "file_path": i.file_path,
                "potential_savings_kb": i.potential_savings_kb,
                "recommendation": i.recommendation,
            }
            for i in result.issues
        ],
        "recommendations": result.recommendations,
    }

    return json.dumps(data, indent=2)


def format_html_output(result: BundleAnalysisResult) -> str:
    """Format results as HTML report."""
    # Calculate color for score
    if result.score >= 80:
        score_color = "#22c55e"  # green
    elif result.score >= 60:
        score_color = "#f59e0b"  # amber
    else:
        score_color = "#ef4444"  # red

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bundle Analysis Report</title>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #1f2937;
            background: #f3f4f6;
            padding: 2rem;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{
            background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
            color: white;
            padding: 2rem;
            border-radius: 12px;
            margin-bottom: 2rem;
        }}
        .header h1 {{ font-size: 1.75rem; margin-bottom: 0.5rem; }}
        .header p {{ opacity: 0.9; }}
        .score-card {{
            background: white;
            border-radius: 12px;
            padding: 2rem;
            margin-bottom: 2rem;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        .score-item {{ text-align: center; }}
        .score-item .value {{
            font-size: 2.5rem;
            font-weight: 700;
            color: {score_color};
        }}
        .score-item .label {{ color: #6b7280; font-size: 0.875rem; }}
        .card {{
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        .card h2 {{
            font-size: 1.125rem;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #e5e7eb;
        }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ text-align: left; padding: 0.75rem; border-bottom: 1px solid #e5e7eb; }}
        th {{ font-weight: 600; color: #374151; background: #f9fafb; }}
        .size {{ text-align: right; font-family: monospace; }}
        .tag {{
            display: inline-block;
            padding: 0.125rem 0.5rem;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 500;
        }}
        .tag-error {{ background: #fef2f2; color: #dc2626; }}
        .tag-warning {{ background: #fffbeb; color: #d97706; }}
        .tag-info {{ background: #eff6ff; color: #2563eb; }}
        .tag-vendor {{ background: #f3e8ff; color: #7c3aed; }}
        .tag-entry {{ background: #ecfdf5; color: #059669; }}
        .issue {{
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 0.75rem;
        }}
        .issue-error {{ background: #fef2f2; border-left: 4px solid #ef4444; }}
        .issue-warning {{ background: #fffbeb; border-left: 4px solid #f59e0b; }}
        .issue-info {{ background: #eff6ff; border-left: 4px solid #3b82f6; }}
        .issue-title {{ font-weight: 600; margin-bottom: 0.25rem; }}
        .issue-rec {{ font-size: 0.875rem; color: #4b5563; margin-top: 0.5rem; }}
        .rec-list {{ list-style: none; }}
        .rec-list li {{
            padding: 0.75rem;
            background: #f0fdf4;
            border-radius: 6px;
            margin-bottom: 0.5rem;
            border-left: 3px solid #22c55e;
        }}
        .footer {{ text-align: center; color: #6b7280; margin-top: 2rem; font-size: 0.875rem; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Bundle Analysis Report</h1>
            <p>{result.target_path}</p>
            <p>Framework: {result.framework_detected or 'Unknown'} | Analyzed: {result.analysis_timestamp}</p>
        </div>

        <div class="score-card">
            <div class="score-item">
                <div class="value">{result.score}</div>
                <div class="label">Health Score</div>
            </div>
            <div class="score-item">
                <div class="value">{result.total_size_mb:.1f}MB</div>
                <div class="label">Total Size</div>
            </div>
            <div class="score-item">
                <div class="value">{result.js_size_kb:.0f}KB</div>
                <div class="label">JavaScript</div>
            </div>
            <div class="score-item">
                <div class="value">{result.optimization_potential_kb:.0f}KB</div>
                <div class="label">Potential Savings</div>
            </div>
        </div>
'''

    # Chunks section
    if result.chunks:
        html += '''
        <div class="card">
            <h2>Largest Chunks</h2>
            <table>
                <thead>
                    <tr>
                        <th>File</th>
                        <th>Type</th>
                        <th class="size">Size</th>
                    </tr>
                </thead>
                <tbody>
'''
        for chunk in result.chunks[:15]:
            tags = ""
            if chunk.is_entry:
                tags += '<span class="tag tag-entry">entry</span> '
            if chunk.is_vendor:
                tags += '<span class="tag tag-vendor">vendor</span>'
            html += f'''
                    <tr>
                        <td>{chunk.name} {tags}</td>
                        <td>{chunk.file_type.upper()}</td>
                        <td class="size">{chunk.size_kb:.1f} KB</td>
                    </tr>
'''
        html += '''
                </tbody>
            </table>
        </div>
'''

    # Issues section
    if result.issues:
        html += '''
        <div class="card">
            <h2>Issues Found</h2>
'''
        for issue in result.issues[:10]:
            issue_class = f"issue-{issue.severity.value}"
            tag_class = f"tag-{issue.severity.value}"
            html += f'''
            <div class="issue {issue_class}">
                <div class="issue-title">
                    <span class="tag {tag_class}">{issue.severity.value.upper()}</span>
                    {issue.title}
                </div>
                <div>{issue.description}</div>
                <div class="issue-rec">{issue.recommendation}</div>
            </div>
'''
        html += '''
        </div>
'''

    # Recommendations section
    if result.recommendations:
        html += '''
        <div class="card">
            <h2>Recommendations</h2>
            <ul class="rec-list">
'''
        for rec in result.recommendations:
            html += f'''
                <li>{rec}</li>
'''
        html += '''
            </ul>
        </div>
'''

    html += f'''
        <div class="footer">
            Generated by Bundle Analyzer v1.0.0 | {result.analysis_timestamp}
        </div>
    </div>
</body>
</html>
'''

    return html


def main():
    """Main entry point with standardized CLI interface."""
    parser = argparse.ArgumentParser(
        description="Bundle Analyzer - Analyze frontend bundles for optimization opportunities",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s ./my-app
  %(prog)s ./my-app --threshold 300
  %(prog)s ./my-app --format json
  %(prog)s ./my-app --format html --output report.html
  %(prog)s ./my-app --verbose

Supported Frameworks:
  - Next.js (.next/ directory)
  - Vite (dist/ directory)
  - Create React App (build/ directory)
  - Nuxt (.nuxt/ directory)
  - Angular (dist/browser/)
  - Remix (build/ directory)
  - Gatsby (public/ directory)

The tool analyzes:
  - package.json dependencies for size and alternatives
  - Build output directories for chunk sizes
  - node_modules for actual installed sizes
  - Code splitting opportunities based on chunk sizes

Exit codes:
  0 - Success
  1 - Error (missing path, parse failure)
        """
    )

    parser.add_argument(
        'path',
        nargs='?',
        help='Path to project directory'
    )

    parser.add_argument(
        '--threshold', '-t',
        type=int,
        default=500,
        help='Size threshold in KB for chunk warnings (default: 500)'
    )

    parser.add_argument(
        '--format', '-f',
        choices=['text', 'json', 'html'],
        default='text',
        help='Output format (default: text)'
    )

    parser.add_argument(
        '--output', '-o',
        help='Output file path (stdout if not specified)'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )

    parser.add_argument(
        '--include-sourcemaps',
        action='store_true',
        help='Include sourcemap files in analysis'
    )

    parser.add_argument(
        '--skip-node-modules',
        action='store_true',
        help='Skip node_modules size analysis (faster)'
    )

    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )

    args = parser.parse_args()

    # Validate path
    if not args.path:
        parser.print_help()
        print("\nError: Project path is required")
        sys.exit(1)

    target_path = Path(args.path).resolve()
    if not target_path.exists():
        print(f"Error: Path does not exist: {target_path}", file=sys.stderr)
        sys.exit(1)

    if not target_path.is_dir():
        print(f"Error: Path is not a directory: {target_path}", file=sys.stderr)
        sys.exit(1)

    # Create config
    config = AnalyzerConfig(
        target_path=target_path,
        size_threshold_kb=args.threshold,
        include_sourcemaps=args.include_sourcemaps,
        analyze_node_modules=not args.skip_node_modules,
        verbose=args.verbose,
    )

    # Run analysis
    try:
        analyzer = BundleAnalyzer(config)
        result = analyzer.analyze()
    except Exception as e:
        print(f"Error during analysis: {e}", file=sys.stderr)
        sys.exit(1)

    # Format output
    if args.format == 'json':
        output = format_json_output(result)
    elif args.format == 'html':
        output = format_html_output(result)
    else:
        output = format_text_output(result, verbose=args.verbose)

    # Write output
    if args.output:
        try:
            with open(args.output, 'w') as f:
                f.write(output)
            if args.verbose:
                print(f"Report written to: {args.output}")
        except IOError as e:
            print(f"Error writing output: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(output)

    sys.exit(0)


if __name__ == '__main__':
    main()
