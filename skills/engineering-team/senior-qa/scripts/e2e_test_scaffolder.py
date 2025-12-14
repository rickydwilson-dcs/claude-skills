#!/usr/bin/env python3
"""
E2E Test Scaffolder
Scaffold complete end-to-end testing infrastructure with Playwright or Cypress
including page objects, fixtures, test data, and CI/CD integration.

Features:
- Framework detection and setup (Playwright, Cypress)
- Page Object Model generation
- Test structure scaffolding
- Fixture and test data management
- CI/CD integration templates (GitHub Actions, GitLab CI, CircleCI)
- Configuration file generation
"""

import argparse
import csv
import json
import logging
import os
import sys
from dataclasses import dataclass, field, asdict
from datetime import datetime
from io import StringIO
from pathlib import Path
from typing import Dict, List, Optional, Any, Set

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class GeneratedFile:
    """Represents a generated file"""
    path: str
    content: str
    description: str
    category: str  # config, page, test, fixture, ci, util

    def to_dict(self) -> Dict:
        return {
            'path': self.path,
            'description': self.description,
            'category': self.category,
            'size': len(self.content),
        }


@dataclass
class ScaffoldResult:
    """Result of scaffolding operation"""
    framework: str
    output_dir: str
    files_generated: List[GeneratedFile] = field(default_factory=list)
    directories_created: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return {
            'framework': self.framework,
            'output_dir': self.output_dir,
            'files_generated': [f.to_dict() for f in self.files_generated],
            'directories_created': self.directories_created,
            'recommendations': self.recommendations,
            'total_files': len(self.files_generated),
        }


class E2ETestScaffolder:
    """Generate E2E testing infrastructure"""

    # Framework configurations
    FRAMEWORKS = {
        'playwright': {
            'config_file': 'playwright.config.ts',
            'test_dir': 'tests',
            'test_suffix': '.spec.ts',
            'package_deps': ['@playwright/test'],
        },
        'cypress': {
            'config_file': 'cypress.config.ts',
            'test_dir': 'cypress/e2e',
            'test_suffix': '.cy.ts',
            'package_deps': ['cypress'],
        },
    }

    # CI/CD providers
    CI_PROVIDERS = {
        'github-actions': '.github/workflows/e2e.yml',
        'gitlab-ci': '.gitlab-ci.yml',
        'circleci': '.circleci/config.yml',
    }

    def __init__(self, target_path: str, verbose: bool = False,
                 framework: str = 'playwright', output_dir: Optional[str] = None,
                 ci_provider: Optional[str] = None, base_url: str = 'http://localhost:3000',
                 pages_only: bool = False):
        if verbose:
            logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("E2ETestScaffolder initialized")

        self.target_path = Path(target_path)
        self.verbose = verbose
        self.framework = framework
        self.output_dir = Path(output_dir) if output_dir else self.target_path / 'e2e'
        self.ci_provider = ci_provider
        self.base_url = base_url
        self.pages_only = pages_only

        self.result = ScaffoldResult(
            framework=framework,
            output_dir=str(self.output_dir),
        )

        self.results = {
            'status': 'success',
            'target': str(target_path),
            'framework': framework,
            'output_dir': str(self.output_dir),
            'files_generated': [],
            'directories_created': [],
            'recommendations': [],
            'scaffold_result': {},
        }

    def run(self) -> Dict:
        """Execute E2E test scaffolding"""
        logger.debug("Starting E2E test scaffolding run")
        print(f"Running E2ETestScaffolder...")
        print(f"Target: {self.target_path}")
        print(f"Framework: {self.framework}")
        print(f"Output: {self.output_dir}")

        try:
            # Detect existing setup
            existing = self._detect_existing_setup()
            if existing:
                logger.debug(f"Detected existing setup: {existing}")
                if self.verbose:
                    print(f"Detected existing setup: {existing}")

            # Create directory structure
            self._create_directories()

            # Generate files
            if not self.pages_only:
                self._generate_config()
                self._generate_utils()

            self._generate_pages()

            if not self.pages_only:
                self._generate_tests()
                self._generate_fixtures()

                if self.ci_provider:
                    self._generate_ci_config()

            # Write files if output directory specified
            self._write_files()

            # Generate recommendations
            self._generate_recommendations()

            # Build results
            self.results['files_generated'] = [f.to_dict() for f in self.result.files_generated]
            self.results['directories_created'] = self.result.directories_created
            self.results['recommendations'] = self.result.recommendations
            self.results['scaffold_result'] = self.result.to_dict()

            self._generate_report()

            print("Completed successfully!")
            return self.results

        except Exception as e:
            logger.error(f"Error during E2E scaffolding: {e}")
            print(f"Error: {e}")
            self.results['status'] = 'error'
            self.results['error'] = str(e)
            if self.verbose:
                import traceback
                traceback.print_exc()
            return self.results

    def _detect_existing_setup(self) -> Optional[str]:
        """Detect existing E2E testing setup"""
        for fw, config in self.FRAMEWORKS.items():
            config_path = self.target_path / config['config_file']
            if config_path.exists():
                return fw

        # Check package.json for dependencies
        package_json = self.target_path / 'package.json'
        if package_json.exists():
            try:
                pkg = json.loads(package_json.read_text())
                deps = {**pkg.get('dependencies', {}), **pkg.get('devDependencies', {})}

                for fw, config in self.FRAMEWORKS.items():
                    for dep in config['package_deps']:
                        if dep in deps:
                            return fw
            except json.JSONDecodeError:
                pass

        return None

    def _create_directories(self):
        """Create directory structure"""
        dirs = [
            self.output_dir,
            self.output_dir / 'pages',
            self.output_dir / 'fixtures',
            self.output_dir / 'utils',
        ]

        if self.framework == 'playwright':
            dirs.append(self.output_dir / 'tests')
        elif self.framework == 'cypress':
            dirs.extend([
                self.output_dir / 'e2e',
                self.output_dir / 'support',
            ])

        for dir_path in dirs:
            self.result.directories_created.append(str(dir_path))

    def _generate_config(self):
        """Generate framework configuration file"""
        if self.framework == 'playwright':
            content = self._generate_playwright_config()
            filename = 'playwright.config.ts'
        else:
            content = self._generate_cypress_config()
            filename = 'cypress.config.ts'

        self.result.files_generated.append(GeneratedFile(
            path=str(self.output_dir / filename),
            content=content,
            description=f'{self.framework.title()} configuration',
            category='config',
        ))

    def _generate_playwright_config(self) -> str:
        """Generate Playwright configuration"""
        return f'''import {{ defineConfig, devices }} from '@playwright/test';

/**
 * Playwright configuration
 * @see https://playwright.dev/docs/test-configuration
 */
export default defineConfig({{
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [
    ['html'],
    ['json', {{ outputFile: 'test-results/results.json' }}],
  ],

  use: {{
    baseURL: process.env.BASE_URL || '{self.base_url}',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  }},

  projects: [
    {{
      name: 'chromium',
      use: {{ ...devices['Desktop Chrome'] }},
    }},
    {{
      name: 'firefox',
      use: {{ ...devices['Desktop Firefox'] }},
    }},
    {{
      name: 'webkit',
      use: {{ ...devices['Desktop Safari'] }},
    }},
    {{
      name: 'mobile-chrome',
      use: {{ ...devices['Pixel 5'] }},
    }},
    {{
      name: 'mobile-safari',
      use: {{ ...devices['iPhone 12'] }},
    }},
  ],

  webServer: {{
    command: 'npm run dev',
    url: '{self.base_url}',
    reuseExistingServer: !process.env.CI,
    timeout: 120 * 1000,
  }},
}});
'''

    def _generate_cypress_config(self) -> str:
        """Generate Cypress configuration"""
        return f'''import {{ defineConfig }} from 'cypress';

export default defineConfig({{
  e2e: {{
    baseUrl: '{self.base_url}',
    specPattern: 'cypress/e2e/**/*.cy.{{js,jsx,ts,tsx}}',
    supportFile: 'cypress/support/e2e.ts',
    viewportWidth: 1280,
    viewportHeight: 720,
    video: true,
    screenshotOnRunFailure: true,
    retries: {{
      runMode: 2,
      openMode: 0,
    }},
    setupNodeEvents(on, config) {{
      // implement node event listeners here
    }},
  }},
  component: {{
    devServer: {{
      framework: 'react',
      bundler: 'vite',
    }},
  }},
}});
'''

    def _generate_utils(self):
        """Generate utility files"""
        if self.framework == 'playwright':
            self._generate_playwright_utils()
        else:
            self._generate_cypress_utils()

    def _generate_playwright_utils(self):
        """Generate Playwright utility files"""
        # helpers.ts
        helpers = '''import { Page, expect } from '@playwright/test';

/**
 * Wait for network to be idle
 */
export async function waitForNetworkIdle(page: Page, timeout = 5000): Promise<void> {
  await page.waitForLoadState('networkidle', { timeout });
}

/**
 * Wait for element to be visible and stable
 */
export async function waitForElement(
  page: Page,
  selector: string,
  options = { timeout: 10000 }
): Promise<void> {
  await page.waitForSelector(selector, { state: 'visible', ...options });
}

/**
 * Take screenshot with timestamp
 */
export async function takeScreenshot(
  page: Page,
  name: string
): Promise<string> {
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const path = `screenshots/${name}-${timestamp}.png`;
  await page.screenshot({ path, fullPage: true });
  return path;
}

/**
 * Fill form field with validation
 */
export async function fillField(
  page: Page,
  selector: string,
  value: string
): Promise<void> {
  await page.fill(selector, '');
  await page.fill(selector, value);
  await expect(page.locator(selector)).toHaveValue(value);
}

/**
 * Click with retry on failure
 */
export async function clickWithRetry(
  page: Page,
  selector: string,
  retries = 3
): Promise<void> {
  for (let i = 0; i < retries; i++) {
    try {
      await page.click(selector, { timeout: 5000 });
      return;
    } catch (e) {
      if (i === retries - 1) throw e;
      await page.waitForTimeout(1000);
    }
  }
}

/**
 * Assert page title
 */
export async function assertTitle(
  page: Page,
  expected: string | RegExp
): Promise<void> {
  await expect(page).toHaveTitle(expected);
}

/**
 * Assert URL contains
 */
export async function assertUrlContains(
  page: Page,
  substring: string
): Promise<void> {
  await expect(page).toHaveURL(new RegExp(substring));
}
'''

        self.result.files_generated.append(GeneratedFile(
            path=str(self.output_dir / 'utils' / 'helpers.ts'),
            content=helpers,
            description='Test helper functions',
            category='util',
        ))

        # constants.ts
        constants = f'''/**
 * Test constants and configuration
 */

export const BASE_URL = process.env.BASE_URL || '{self.base_url}';

export const TIMEOUTS = {{
  short: 5000,
  medium: 10000,
  long: 30000,
  navigation: 60000,
}};

export const SELECTORS = {{
  // Navigation
  nav: {{
    home: '[data-testid="nav-home"]',
    about: '[data-testid="nav-about"]',
    login: '[data-testid="nav-login"]',
    logout: '[data-testid="nav-logout"]',
  }},
  // Auth
  auth: {{
    emailInput: '[data-testid="email-input"]',
    passwordInput: '[data-testid="password-input"]',
    submitButton: '[data-testid="submit-button"]',
    errorMessage: '[data-testid="error-message"]',
  }},
  // Common
  common: {{
    loading: '[data-testid="loading"]',
    toast: '[data-testid="toast"]',
    modal: '[data-testid="modal"]',
    closeButton: '[data-testid="close-button"]',
  }},
}};

export const TEST_USERS = {{
  standard: {{
    email: 'test@example.com',
    password: 'password123',
  }},
  admin: {{
    email: 'admin@example.com',
    password: 'admin123',
  }},
}};
'''

        self.result.files_generated.append(GeneratedFile(
            path=str(self.output_dir / 'utils' / 'constants.ts'),
            content=constants,
            description='Test constants and selectors',
            category='util',
        ))

    def _generate_cypress_utils(self):
        """Generate Cypress utility files"""
        # commands.ts
        commands = '''/// <reference types="cypress" />

/**
 * Custom Cypress commands
 */

declare global {
  namespace Cypress {
    interface Chainable {
      login(email: string, password: string): Chainable<void>;
      logout(): Chainable<void>;
      getByTestId(testId: string): Chainable<JQuery<HTMLElement>>;
      waitForApi(alias: string): Chainable<void>;
    }
  }
}

/**
 * Login command
 */
Cypress.Commands.add('login', (email: string, password: string) => {
  cy.session([email, password], () => {
    cy.visit('/login');
    cy.getByTestId('email-input').type(email);
    cy.getByTestId('password-input').type(password);
    cy.getByTestId('submit-button').click();
    cy.url().should('not.include', '/login');
  });
});

/**
 * Logout command
 */
Cypress.Commands.add('logout', () => {
  cy.getByTestId('nav-logout').click();
  cy.url().should('include', '/login');
});

/**
 * Get element by data-testid
 */
Cypress.Commands.add('getByTestId', (testId: string) => {
  return cy.get(`[data-testid="${testId}"]`);
});

/**
 * Wait for API call
 */
Cypress.Commands.add('waitForApi', (alias: string) => {
  cy.wait(`@${alias}`).its('response.statusCode').should('be.oneOf', [200, 201]);
});

export {};
'''

        self.result.files_generated.append(GeneratedFile(
            path=str(self.output_dir / 'support' / 'commands.ts'),
            content=commands,
            description='Custom Cypress commands',
            category='util',
        ))

        # e2e.ts
        e2e_support = '''/// <reference types="cypress" />

import './commands';

/**
 * Global before/after hooks
 */

beforeEach(() => {
  // Clear local storage and cookies before each test
  cy.clearLocalStorage();
  cy.clearCookies();
});

afterEach(function() {
  // Take screenshot on failure
  if (this.currentTest?.state === 'failed') {
    const testName = this.currentTest.title.replace(/\\s+/g, '-');
    cy.screenshot(`failure-${testName}`);
  }
});

/**
 * Prevent uncaught exceptions from failing tests
 */
Cypress.on('uncaught:exception', (err, runnable) => {
  // Log the error for debugging
  console.error('Uncaught exception:', err.message);
  // Return false to prevent Cypress from failing the test
  return false;
});
'''

        self.result.files_generated.append(GeneratedFile(
            path=str(self.output_dir / 'support' / 'e2e.ts'),
            content=e2e_support,
            description='Cypress E2E support file',
            category='util',
        ))

    def _generate_pages(self):
        """Generate Page Object Model files"""
        if self.framework == 'playwright':
            self._generate_playwright_pages()
        else:
            self._generate_cypress_pages()

    def _generate_playwright_pages(self):
        """Generate Playwright page objects"""
        # base.page.ts
        base_page = '''import { Page, Locator, expect } from '@playwright/test';

/**
 * Base page class for common functionality
 */
export abstract class BasePage {
  readonly page: Page;

  constructor(page: Page) {
    this.page = page;
  }

  /**
   * Navigate to page
   */
  abstract goto(): Promise<void>;

  /**
   * Wait for page to load
   */
  async waitForLoad(): Promise<void> {
    await this.page.waitForLoadState('networkidle');
  }

  /**
   * Get element by test ID
   */
  getByTestId(testId: string): Locator {
    return this.page.getByTestId(testId);
  }

  /**
   * Get element by role
   */
  getByRole(role: Parameters<Page['getByRole']>[0], options?: Parameters<Page['getByRole']>[1]): Locator {
    return this.page.getByRole(role, options);
  }

  /**
   * Click navigation link
   */
  async clickNavLink(name: string): Promise<void> {
    await this.page.getByRole('link', { name }).click();
  }

  /**
   * Assert page URL
   */
  async assertUrl(pattern: string | RegExp): Promise<void> {
    await expect(this.page).toHaveURL(pattern);
  }

  /**
   * Assert element visible
   */
  async assertVisible(locator: Locator): Promise<void> {
    await expect(locator).toBeVisible();
  }

  /**
   * Assert element hidden
   */
  async assertHidden(locator: Locator): Promise<void> {
    await expect(locator).toBeHidden();
  }

  /**
   * Wait for navigation
   */
  async waitForNavigation(url: string | RegExp): Promise<void> {
    await this.page.waitForURL(url);
  }

  /**
   * Take screenshot
   */
  async screenshot(name: string): Promise<void> {
    await this.page.screenshot({ path: `screenshots/${name}.png`, fullPage: true });
  }
}
'''

        self.result.files_generated.append(GeneratedFile(
            path=str(self.output_dir / 'pages' / 'base.page.ts'),
            content=base_page,
            description='Base page object class',
            category='page',
        ))

        # login.page.ts
        login_page = f'''import {{ Page, Locator, expect }} from '@playwright/test';
import {{ BasePage }} from './base.page';

/**
 * Login page object
 */
export class LoginPage extends BasePage {{
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly submitButton: Locator;
  readonly errorMessage: Locator;
  readonly forgotPasswordLink: Locator;
  readonly signUpLink: Locator;

  constructor(page: Page) {{
    super(page);
    this.emailInput = page.getByTestId('email-input');
    this.passwordInput = page.getByTestId('password-input');
    this.submitButton = page.getByTestId('submit-button');
    this.errorMessage = page.getByTestId('error-message');
    this.forgotPasswordLink = page.getByRole('link', {{ name: 'Forgot password' }});
    this.signUpLink = page.getByRole('link', {{ name: 'Sign up' }});
  }}

  async goto(): Promise<void> {{
    await this.page.goto('/login');
    await this.waitForLoad();
  }}

  /**
   * Fill login form
   */
  async fillForm(email: string, password: string): Promise<void> {{
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
  }}

  /**
   * Submit login form
   */
  async submit(): Promise<void> {{
    await this.submitButton.click();
  }}

  /**
   * Perform login
   */
  async login(email: string, password: string): Promise<void> {{
    await this.fillForm(email, password);
    await this.submit();
  }}

  /**
   * Assert error message
   */
  async assertError(message: string | RegExp): Promise<void> {{
    await expect(this.errorMessage).toBeVisible();
    await expect(this.errorMessage).toHaveText(message);
  }}

  /**
   * Assert successful login
   */
  async assertLoginSuccess(): Promise<void> {{
    await expect(this.page).not.toHaveURL(/login/);
  }}

  /**
   * Assert form validation error
   */
  async assertValidationError(field: 'email' | 'password'): Promise<void> {{
    const input = field === 'email' ? this.emailInput : this.passwordInput;
    await expect(input).toHaveAttribute('aria-invalid', 'true');
  }}
}}
'''

        self.result.files_generated.append(GeneratedFile(
            path=str(self.output_dir / 'pages' / 'login.page.ts'),
            content=login_page,
            description='Login page object',
            category='page',
        ))

        # home.page.ts
        home_page = f'''import {{ Page, Locator, expect }} from '@playwright/test';
import {{ BasePage }} from './base.page';

/**
 * Home page object
 */
export class HomePage extends BasePage {{
  readonly heading: Locator;
  readonly navigation: Locator;
  readonly content: Locator;
  readonly footer: Locator;

  constructor(page: Page) {{
    super(page);
    this.heading = page.getByRole('heading', {{ level: 1 }});
    this.navigation = page.getByRole('navigation');
    this.content = page.getByRole('main');
    this.footer = page.getByRole('contentinfo');
  }}

  async goto(): Promise<void> {{
    await this.page.goto('/');
    await this.waitForLoad();
  }}

  /**
   * Assert home page loaded
   */
  async assertLoaded(): Promise<void> {{
    await this.assertUrl('/');
    await expect(this.heading).toBeVisible();
    await expect(this.navigation).toBeVisible();
  }}

  /**
   * Get navigation links
   */
  async getNavLinks(): Promise<string[]> {{
    const links = await this.navigation.getByRole('link').all();
    return Promise.all(links.map(link => link.textContent() as Promise<string>));
  }}

  /**
   * Navigate to page
   */
  async navigateTo(pageName: string): Promise<void> {{
    await this.navigation.getByRole('link', {{ name: pageName }}).click();
  }}

  /**
   * Assert user logged in
   */
  async assertLoggedIn(username?: string): Promise<void> {{
    await expect(this.getByTestId('user-menu')).toBeVisible();
    if (username) {{
      await expect(this.getByTestId('user-name')).toHaveText(username);
    }}
  }}

  /**
   * Assert user logged out
   */
  async assertLoggedOut(): Promise<void> {{
    await expect(this.getByTestId('login-button')).toBeVisible();
  }}
}}
'''

        self.result.files_generated.append(GeneratedFile(
            path=str(self.output_dir / 'pages' / 'home.page.ts'),
            content=home_page,
            description='Home page object',
            category='page',
        ))

        # index.ts - export all pages
        index = '''export { BasePage } from './base.page';
export { LoginPage } from './login.page';
export { HomePage } from './home.page';
'''

        self.result.files_generated.append(GeneratedFile(
            path=str(self.output_dir / 'pages' / 'index.ts'),
            content=index,
            description='Page objects index',
            category='page',
        ))

    def _generate_cypress_pages(self):
        """Generate Cypress page objects"""
        # login.page.ts
        login_page = '''/**
 * Login page object for Cypress
 */
export class LoginPage {
  // Selectors
  readonly selectors = {
    emailInput: '[data-testid="email-input"]',
    passwordInput: '[data-testid="password-input"]',
    submitButton: '[data-testid="submit-button"]',
    errorMessage: '[data-testid="error-message"]',
    forgotPasswordLink: 'a:contains("Forgot password")',
    signUpLink: 'a:contains("Sign up")',
  };

  /**
   * Visit login page
   */
  visit(): this {
    cy.visit('/login');
    return this;
  }

  /**
   * Fill email field
   */
  fillEmail(email: string): this {
    cy.get(this.selectors.emailInput).clear().type(email);
    return this;
  }

  /**
   * Fill password field
   */
  fillPassword(password: string): this {
    cy.get(this.selectors.passwordInput).clear().type(password);
    return this;
  }

  /**
   * Submit form
   */
  submit(): this {
    cy.get(this.selectors.submitButton).click();
    return this;
  }

  /**
   * Perform login
   */
  login(email: string, password: string): this {
    this.fillEmail(email);
    this.fillPassword(password);
    this.submit();
    return this;
  }

  /**
   * Assert error message
   */
  assertError(message: string | RegExp): this {
    cy.get(this.selectors.errorMessage)
      .should('be.visible')
      .and('contain', message);
    return this;
  }

  /**
   * Assert successful login
   */
  assertLoginSuccess(): this {
    cy.url().should('not.include', '/login');
    return this;
  }
}

export const loginPage = new LoginPage();
'''

        self.result.files_generated.append(GeneratedFile(
            path=str(self.output_dir / 'pages' / 'login.page.ts'),
            content=login_page,
            description='Login page object',
            category='page',
        ))

        # home.page.ts
        home_page = '''/**
 * Home page object for Cypress
 */
export class HomePage {
  // Selectors
  readonly selectors = {
    heading: 'h1',
    navigation: 'nav',
    userMenu: '[data-testid="user-menu"]',
    loginButton: '[data-testid="login-button"]',
    logoutButton: '[data-testid="logout-button"]',
  };

  /**
   * Visit home page
   */
  visit(): this {
    cy.visit('/');
    return this;
  }

  /**
   * Assert page loaded
   */
  assertLoaded(): this {
    cy.url().should('eq', Cypress.config().baseUrl + '/');
    cy.get(this.selectors.heading).should('be.visible');
    cy.get(this.selectors.navigation).should('be.visible');
    return this;
  }

  /**
   * Click navigation link
   */
  clickNavLink(name: string): this {
    cy.get(this.selectors.navigation)
      .contains('a', name)
      .click();
    return this;
  }

  /**
   * Assert user logged in
   */
  assertLoggedIn(): this {
    cy.get(this.selectors.userMenu).should('be.visible');
    return this;
  }

  /**
   * Assert user logged out
   */
  assertLoggedOut(): this {
    cy.get(this.selectors.loginButton).should('be.visible');
    return this;
  }
}

export const homePage = new HomePage();
'''

        self.result.files_generated.append(GeneratedFile(
            path=str(self.output_dir / 'pages' / 'home.page.ts'),
            content=home_page,
            description='Home page object',
            category='page',
        ))

    def _generate_tests(self):
        """Generate test files"""
        if self.framework == 'playwright':
            self._generate_playwright_tests()
        else:
            self._generate_cypress_tests()

    def _generate_playwright_tests(self):
        """Generate Playwright test files"""
        # auth.spec.ts
        auth_spec = '''import { test, expect } from '@playwright/test';
import { LoginPage, HomePage } from '../pages';
import { TEST_USERS } from '../utils/constants';

test.describe('Authentication', () => {
  let loginPage: LoginPage;
  let homePage: HomePage;

  test.beforeEach(async ({ page }) => {
    loginPage = new LoginPage(page);
    homePage = new HomePage(page);
  });

  test('should display login page correctly', async () => {
    await loginPage.goto();

    await expect(loginPage.emailInput).toBeVisible();
    await expect(loginPage.passwordInput).toBeVisible();
    await expect(loginPage.submitButton).toBeVisible();
  });

  test('should login with valid credentials', async () => {
    await loginPage.goto();
    await loginPage.login(TEST_USERS.standard.email, TEST_USERS.standard.password);

    await loginPage.assertLoginSuccess();
    await homePage.assertLoggedIn();
  });

  test('should show error with invalid credentials', async () => {
    await loginPage.goto();
    await loginPage.login('invalid@example.com', 'wrongpassword');

    await loginPage.assertError(/invalid credentials/i);
  });

  test('should validate required fields', async () => {
    await loginPage.goto();
    await loginPage.submit();

    await loginPage.assertValidationError('email');
    await loginPage.assertValidationError('password');
  });

  test('should logout successfully', async ({ page }) => {
    // Login first
    await loginPage.goto();
    await loginPage.login(TEST_USERS.standard.email, TEST_USERS.standard.password);
    await loginPage.assertLoginSuccess();

    // Logout
    await page.getByTestId('nav-logout').click();

    // Verify logged out
    await homePage.assertLoggedOut();
  });
});
'''

        self.result.files_generated.append(GeneratedFile(
            path=str(self.output_dir / 'tests' / 'auth.spec.ts'),
            content=auth_spec,
            description='Authentication tests',
            category='test',
        ))

        # navigation.spec.ts
        nav_spec = '''import { test, expect } from '@playwright/test';
import { HomePage } from '../pages';

test.describe('Navigation', () => {
  let homePage: HomePage;

  test.beforeEach(async ({ page }) => {
    homePage = new HomePage(page);
    await homePage.goto();
  });

  test('should load home page', async () => {
    await homePage.assertLoaded();
  });

  test('should display navigation links', async () => {
    const links = await homePage.getNavLinks();

    expect(links.length).toBeGreaterThan(0);
  });

  test('should navigate between pages', async ({ page }) => {
    // Test navigation to about page
    await homePage.navigateTo('About');
    await expect(page).toHaveURL(/about/);

    // Navigate back to home
    await homePage.navigateTo('Home');
    await homePage.assertLoaded();
  });

  test('should be responsive on mobile', async ({ page }) => {
    // Set mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });

    // Verify mobile menu toggle exists
    const menuToggle = page.getByTestId('mobile-menu-toggle');
    await expect(menuToggle).toBeVisible();
  });
});
'''

        self.result.files_generated.append(GeneratedFile(
            path=str(self.output_dir / 'tests' / 'navigation.spec.ts'),
            content=nav_spec,
            description='Navigation tests',
            category='test',
        ))

    def _generate_cypress_tests(self):
        """Generate Cypress test files"""
        # auth.cy.ts
        auth_spec = '''import { loginPage } from '../pages/login.page';
import { homePage } from '../pages/home.page';

describe('Authentication', () => {
  beforeEach(() => {
    cy.clearCookies();
    cy.clearLocalStorage();
  });

  it('should display login page correctly', () => {
    loginPage.visit();

    cy.get(loginPage.selectors.emailInput).should('be.visible');
    cy.get(loginPage.selectors.passwordInput).should('be.visible');
    cy.get(loginPage.selectors.submitButton).should('be.visible');
  });

  it('should login with valid credentials', () => {
    loginPage
      .visit()
      .login('test@example.com', 'password123')
      .assertLoginSuccess();

    homePage.assertLoggedIn();
  });

  it('should show error with invalid credentials', () => {
    loginPage
      .visit()
      .login('invalid@example.com', 'wrongpassword')
      .assertError('Invalid credentials');
  });

  it('should validate required fields', () => {
    loginPage.visit().submit();

    cy.get(loginPage.selectors.emailInput).should('have.attr', 'aria-invalid', 'true');
    cy.get(loginPage.selectors.passwordInput).should('have.attr', 'aria-invalid', 'true');
  });

  it('should logout successfully', () => {
    // Login
    cy.login('test@example.com', 'password123');
    homePage.visit().assertLoggedIn();

    // Logout
    cy.logout();
    homePage.assertLoggedOut();
  });
});
'''

        self.result.files_generated.append(GeneratedFile(
            path=str(self.output_dir / 'e2e' / 'auth.cy.ts'),
            content=auth_spec,
            description='Authentication tests',
            category='test',
        ))

        # navigation.cy.ts
        nav_spec = '''import { homePage } from '../pages/home.page';

describe('Navigation', () => {
  beforeEach(() => {
    homePage.visit();
  });

  it('should load home page', () => {
    homePage.assertLoaded();
  });

  it('should display navigation links', () => {
    cy.get(homePage.selectors.navigation)
      .find('a')
      .should('have.length.greaterThan', 0);
  });

  it('should navigate between pages', () => {
    // Navigate to about
    homePage.clickNavLink('About');
    cy.url().should('include', '/about');

    // Navigate back home
    homePage.clickNavLink('Home');
    homePage.assertLoaded();
  });

  it('should be responsive on mobile', () => {
    cy.viewport('iphone-x');

    cy.getByTestId('mobile-menu-toggle').should('be.visible');
  });
});
'''

        self.result.files_generated.append(GeneratedFile(
            path=str(self.output_dir / 'e2e' / 'navigation.cy.ts'),
            content=nav_spec,
            description='Navigation tests',
            category='test',
        ))

    def _generate_fixtures(self):
        """Generate fixture files"""
        # users.json
        users_json = '''{
  "standard": {
    "id": "user-1",
    "email": "test@example.com",
    "password": "password123",
    "name": "Test User",
    "role": "user"
  },
  "admin": {
    "id": "admin-1",
    "email": "admin@example.com",
    "password": "admin123",
    "name": "Admin User",
    "role": "admin"
  },
  "newUser": {
    "email": "new@example.com",
    "password": "newuser123",
    "name": "New User"
  }
}
'''

        self.result.files_generated.append(GeneratedFile(
            path=str(self.output_dir / 'fixtures' / 'users.json'),
            content=users_json,
            description='User fixture data',
            category='fixture',
        ))

        # test-data.json
        test_data = '''{
  "validInputs": {
    "email": "valid@example.com",
    "password": "ValidP@ssw0rd",
    "name": "Valid Name",
    "phone": "+1234567890"
  },
  "invalidInputs": {
    "email": "invalid-email",
    "password": "123",
    "name": "",
    "phone": "not-a-phone"
  },
  "edgeCases": {
    "longEmail": "verylongemailaddressthatisover100characterslong@example.verylongdomainname.com",
    "specialChars": "test+special@example.com",
    "unicode": "user@domain.com",
    "xss": "<script>alert('xss')</script>",
    "sqlInjection": "'; DROP TABLE users; --"
  }
}
'''

        self.result.files_generated.append(GeneratedFile(
            path=str(self.output_dir / 'fixtures' / 'test-data.json'),
            content=test_data,
            description='Test data fixtures',
            category='fixture',
        ))

    def _generate_ci_config(self):
        """Generate CI/CD configuration"""
        if self.ci_provider == 'github-actions':
            self._generate_github_actions()
        elif self.ci_provider == 'gitlab-ci':
            self._generate_gitlab_ci()
        elif self.ci_provider == 'circleci':
            self._generate_circleci()

    def _generate_github_actions(self):
        """Generate GitHub Actions workflow"""
        if self.framework == 'playwright':
            workflow = '''name: E2E Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  e2e-tests:
    runs-on: ubuntu-latest
    timeout-minutes: 30

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Install Playwright browsers
        run: npx playwright install --with-deps

      - name: Build application
        run: npm run build

      - name: Run E2E tests
        run: npx playwright test
        env:
          BASE_URL: http://localhost:3000

      - name: Upload test results
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 30

      - name: Upload test artifacts
        uses: actions/upload-artifact@v4
        if: failure()
        with:
          name: test-artifacts
          path: |
            test-results/
            screenshots/
          retention-days: 7
'''
        else:
            workflow = '''name: E2E Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  e2e-tests:
    runs-on: ubuntu-latest
    timeout-minutes: 30

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Build application
        run: npm run build

      - name: Run Cypress tests
        uses: cypress-io/github-action@v6
        with:
          start: npm run start
          wait-on: 'http://localhost:3000'
          wait-on-timeout: 120

      - name: Upload screenshots
        uses: actions/upload-artifact@v4
        if: failure()
        with:
          name: cypress-screenshots
          path: cypress/screenshots
          retention-days: 7

      - name: Upload videos
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: cypress-videos
          path: cypress/videos
          retention-days: 7
'''

        self.result.files_generated.append(GeneratedFile(
            path=str(self.target_path / '.github' / 'workflows' / 'e2e.yml'),
            content=workflow,
            description='GitHub Actions E2E workflow',
            category='ci',
        ))

    def _generate_gitlab_ci(self):
        """Generate GitLab CI configuration"""
        if self.framework == 'playwright':
            config = '''stages:
  - test

e2e-tests:
  stage: test
  image: mcr.microsoft.com/playwright:v1.40.0-jammy
  script:
    - npm ci
    - npm run build
    - npx playwright test
  artifacts:
    when: always
    paths:
      - playwright-report/
      - test-results/
    expire_in: 1 week
  only:
    - main
    - develop
    - merge_requests
'''
        else:
            config = '''stages:
  - test

e2e-tests:
  stage: test
  image: cypress/browsers:node-20.9.0-chrome-118.0.5993.88-1-ff-118.0.2-edge-118.0.2088.46-1
  script:
    - npm ci
    - npm run build &
    - npx cypress run
  artifacts:
    when: always
    paths:
      - cypress/screenshots/
      - cypress/videos/
    expire_in: 1 week
  only:
    - main
    - develop
    - merge_requests
'''

        self.result.files_generated.append(GeneratedFile(
            path=str(self.target_path / '.gitlab-ci.yml'),
            content=config,
            description='GitLab CI E2E configuration',
            category='ci',
        ))

    def _generate_circleci(self):
        """Generate CircleCI configuration"""
        if self.framework == 'playwright':
            config = '''version: 2.1

orbs:
  node: circleci/node@5

jobs:
  e2e-tests:
    docker:
      - image: mcr.microsoft.com/playwright:v1.40.0-jammy
    steps:
      - checkout
      - node/install-packages
      - run:
          name: Build application
          command: npm run build
      - run:
          name: Run E2E tests
          command: npx playwright test
      - store_artifacts:
          path: playwright-report
          destination: playwright-report
      - store_artifacts:
          path: test-results
          destination: test-results

workflows:
  test:
    jobs:
      - e2e-tests:
          filters:
            branches:
              only:
                - main
                - develop
'''
        else:
            config = '''version: 2.1

orbs:
  node: circleci/node@5
  cypress: cypress-io/cypress@3

jobs:
  e2e-tests:
    executor: cypress/default
    steps:
      - checkout
      - node/install-packages
      - run:
          name: Build application
          command: npm run build
      - cypress/run-tests:
          start-command: npm run start
          wait-on: 'http://localhost:3000'
      - store_artifacts:
          path: cypress/screenshots
      - store_artifacts:
          path: cypress/videos

workflows:
  test:
    jobs:
      - e2e-tests:
          filters:
            branches:
              only:
                - main
                - develop
'''

        self.result.files_generated.append(GeneratedFile(
            path=str(self.target_path / '.circleci' / 'config.yml'),
            content=config,
            description='CircleCI E2E configuration',
            category='ci',
        ))

    def _write_files(self):
        """Write generated files to disk"""
        for gen_file in self.result.files_generated:
            file_path = Path(gen_file.path)

            # Create parent directories
            file_path.parent.mkdir(parents=True, exist_ok=True)

            # Write file
            file_path.write_text(gen_file.content)

            if self.verbose:
                print(f"  Created: {file_path}")

    def _generate_recommendations(self):
        """Generate setup recommendations"""
        recs = []

        # Framework-specific recommendations
        if self.framework == 'playwright':
            recs.extend([
                'Install Playwright: npm init playwright@latest',
                'Install browsers: npx playwright install',
                'Run tests: npx playwright test',
                'View report: npx playwright show-report',
            ])
        else:
            recs.extend([
                'Install Cypress: npm install cypress --save-dev',
                'Open Cypress: npx cypress open',
                'Run tests: npx cypress run',
            ])

        # General recommendations
        recs.extend([
            'Add data-testid attributes to your components for reliable selectors',
            'Use page objects for maintainable tests',
            'Run tests in CI/CD pipeline on every PR',
            'Keep tests isolated - each test should be independent',
        ])

        self.result.recommendations = recs

    def _generate_report(self):
        """Generate and display the scaffolding report"""
        print("\n" + "=" * 60)
        print("E2E TEST SCAFFOLDER REPORT")
        print("=" * 60)

        print(f"\nFramework: {self.framework}")
        print(f"Output directory: {self.output_dir}")

        # Files by category
        categories = {}
        for f in self.result.files_generated:
            if f.category not in categories:
                categories[f.category] = []
            categories[f.category].append(f)

        print(f"\nFiles Generated ({len(self.result.files_generated)} total):")
        for cat, files in sorted(categories.items()):
            print(f"\n  {cat.upper()} ({len(files)}):")
            for f in files:
                print(f"    - {f.path}")

        print(f"\nDirectories Created ({len(self.result.directories_created)}):")
        for d in self.result.directories_created[:5]:
            print(f"  - {d}")

        if self.result.recommendations:
            print(f"\nSetup Instructions:")
            for i, rec in enumerate(self.result.recommendations[:5], 1):
                print(f"  {i}. {rec}")

        print("\n" + "=" * 60)


def format_csv_output(results: Dict) -> str:
    """Format results as CSV"""
    output = StringIO()
    writer = csv.writer(output)

    writer.writerow(['path', 'category', 'description', 'size'])

    for f in results.get('files_generated', []):
        writer.writerow([
            f.get('path', ''),
            f.get('category', ''),
            f.get('description', ''),
            f.get('size', 0),
        ])

    return output.getvalue()


def main():
    """Main entry point with standardized CLI interface"""
    parser = argparse.ArgumentParser(
        description="E2ETestScaffolder - Generate E2E testing infrastructure",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --input . --framework playwright
  %(prog)s --input . --framework cypress --output ./e2e
  %(prog)s --input . --framework playwright --ci github-actions
  %(prog)s --input . --framework cypress --base-url http://localhost:8080
  %(prog)s --input . --framework playwright --pages-only

Supported Frameworks:
  playwright - Playwright (recommended for cross-browser)
  cypress    - Cypress (great for debugging)

CI/CD Providers:
  github-actions - GitHub Actions workflow
  gitlab-ci      - GitLab CI configuration
  circleci       - CircleCI configuration

For more information, see the skill documentation.
        """
    )

    parser.add_argument(
        '--input', '-i',
        required=True,
        dest='target',
        help='Project directory'
    )

    parser.add_argument(
        '--framework', '-F',
        choices=['playwright', 'cypress'],
        default='playwright',
        help='E2E testing framework (default: playwright)'
    )

    parser.add_argument(
        '--output', '-O',
        dest='output_dir',
        help='Output directory for E2E tests (default: ./e2e)'
    )

    parser.add_argument(
        '--ci',
        choices=['github-actions', 'gitlab-ci', 'circleci'],
        help='Generate CI/CD configuration'
    )

    parser.add_argument(
        '--base-url', '-b',
        default='http://localhost:3000',
        help='Base URL for tests (default: http://localhost:3000)'
    )

    parser.add_argument(
        '--pages-only',
        action='store_true',
        help='Generate only page objects (no tests or config)'
    )

    parser.add_argument(
        '--format', '-o',
        choices=['text', 'json', 'csv'],
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

    scaffolder = E2ETestScaffolder(
        args.target,
        verbose=args.verbose,
        framework=args.framework,
        output_dir=args.output_dir,
        ci_provider=args.ci,
        base_url=args.base_url,
        pages_only=args.pages_only,
    )

    results = scaffolder.run()

    # Format output
    if args.format == 'csv':
        output = format_csv_output(results)
    elif args.format == 'json':
        output = json.dumps(results, indent=2, default=str)
    else:
        output = json.dumps(results, indent=2, default=str)

    if args.file:
        with open(args.file, 'w') as f:
            f.write(output)
        print(f"Results written to {args.file}")
    elif args.format != 'text':
        print(output)

    # Exit code
    sys.exit(0 if results.get('status') == 'success' else 1)


if __name__ == '__main__':
    main()
