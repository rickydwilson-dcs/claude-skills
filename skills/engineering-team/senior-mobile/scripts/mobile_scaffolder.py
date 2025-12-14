#!/usr/bin/env python3
"""
Module: mobile_scaffolder.py
Description: Generate cross-platform mobile project structures for React Native, Flutter, and Expo

This tool scaffolds production-ready mobile applications with complete infrastructure including:
- React Native with TypeScript and modern navigation
- Flutter with Dart null safety and state management
- Expo managed workflow with EAS Build
- Testing infrastructure (unit, integration, E2E)
- CI/CD pipelines (GitHub Actions, Bitrise, Codemagic)

Usage:
    python mobile_scaffolder.py MyApp
    python mobile_scaffolder.py MyApp --framework react-native --platforms both --auth
    python mobile_scaffolder.py MyApp -f flutter --state riverpod --testing all
    python mobile_scaffolder.py MyApp -f expo --ci github-actions -o json

Author: Claude Skills - Senior Mobile Engineer
Version: 1.0.0
Last Updated: 2025-12-13
"""

import argparse
import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MobileScaffolder:
    """Generate cross-platform mobile project structures"""

    FRAMEWORKS = ['react-native', 'flutter', 'expo']
    PLATFORMS = ['ios', 'android', 'both']
    NAVIGATION = {
        'react-native': ['react-navigation', 'none'],
        'expo': ['react-navigation', 'none'],
        'flutter': ['go_router', 'auto_route', 'none']
    }
    STATE_MANAGEMENT = {
        'react-native': ['redux', 'zustand', 'none'],
        'expo': ['redux', 'zustand', 'none'],
        'flutter': ['provider', 'riverpod', 'bloc', 'none']
    }
    TESTING_TYPES = ['unit', 'integration', 'e2e', 'all', 'none']
    CI_PLATFORMS = ['github-actions', 'bitrise', 'codemagic', 'none']

    def __init__(self, project_name: str, **options):
        verbose = options.get('verbose', False)
        if verbose:
            logging.getLogger().setLevel(logging.DEBUG)

        self.project_name = project_name
        self.framework = options.get('framework', 'react-native')
        self.platforms = options.get('platforms', 'both')
        self.navigation = options.get('navigation') or self._default_navigation()
        self.state = options.get('state') or self._default_state()
        self.testing = options.get('testing', 'all')
        self.ci = options.get('ci', 'github-actions')
        self.output_dir = Path(options.get('output_dir', '.'))
        self.dry_run = options.get('dry_run', False)
        self.verbose = verbose

        self.project_path = self.output_dir / self.project_name
        self.files_created = []
        self.dirs_created = []

        logger.debug("MobileScaffolder initialized")

    def _default_navigation(self):
        """Get default navigation for framework"""
        nav_map = {
            'react-native': 'react-navigation',
            'expo': 'react-navigation',
            'flutter': 'go_router'
        }
        return nav_map.get(self.framework, 'none')

    def _default_state(self):
        """Get default state management for framework"""
        state_map = {
            'react-native': 'zustand',
            'expo': 'zustand',
            'flutter': 'riverpod'
        }
        return state_map.get(self.framework, 'none')

    def validate(self) -> List[str]:
        """Validate configuration and return list of errors"""
        logger.debug("Validating configuration")
        errors = []

        # Validate project name
        if not self.project_name:
            logger.warning("Project name is missing")
            errors.append("Project name is required")
        elif not self.project_name.replace('-', '').replace('_', '').isalnum():
            errors.append(f"Invalid project name: {self.project_name} (use alphanumeric, hyphens, underscores)")

        # Validate framework
        if self.framework not in self.FRAMEWORKS:
            errors.append(f"Invalid framework: {self.framework}. Choose from: {', '.join(self.FRAMEWORKS)}")

        # Validate platforms
        if self.platforms not in self.PLATFORMS:
            errors.append(f"Invalid platforms: {self.platforms}. Choose from: {', '.join(self.PLATFORMS)}")

        # Validate navigation
        valid_nav = self.NAVIGATION.get(self.framework, [])
        if self.navigation not in valid_nav:
            errors.append(f"Invalid navigation for {self.framework}: {self.navigation}. Choose from: {', '.join(valid_nav)}")

        # Validate state management
        valid_state = self.STATE_MANAGEMENT.get(self.framework, [])
        if self.state not in valid_state:
            errors.append(f"Invalid state management for {self.framework}: {self.state}. Choose from: {', '.join(valid_state)}")

        # Validate testing
        if self.testing not in self.TESTING_TYPES:
            errors.append(f"Invalid testing: {self.testing}. Choose from: {', '.join(self.TESTING_TYPES)}")

        # Validate CI
        if self.ci not in self.CI_PLATFORMS:
            errors.append(f"Invalid CI platform: {self.ci}. Choose from: {', '.join(self.CI_PLATFORMS)}")

        # Check if project directory exists
        if self.project_path.exists() and not self.dry_run:
            errors.append(f"Project directory already exists: {self.project_path}")

        return errors

    def scaffold(self) -> Dict[str, Any]:
        """Generate the project structure"""
        logger.debug("Starting scaffold generation")
        start_time = datetime.now()

        if self.verbose:
            print(f"Scaffolding {self.framework} project: {self.project_name}")
            print(f"Platform(s): {self.platforms}")
            print(f"Navigation: {self.navigation}")
            print(f"State: {self.state}")
            print(f"Testing: {self.testing}")
            print(f"CI/CD: {self.ci}")
            print(f"Dry run: {self.dry_run}\n")

        # Create directory structure
        if self.framework in ['react-native', 'expo']:
            self._scaffold_react_native()
        elif self.framework == 'flutter':
            self._scaffold_flutter()

        end_time = datetime.now()
        duration_ms = int((end_time - start_time).total_seconds() * 1000)

        return {
            "status": "success",
            "project_name": self.project_name,
            "framework": self.framework,
            "project_path": str(self.project_path),
            "files_created": len(self.files_created),
            "directories_created": len(self.dirs_created),
            "duration_ms": duration_ms,
            "configuration": {
                "platforms": self.platforms,
                "navigation": self.navigation,
                "state_management": self.state,
                "testing": self.testing,
                "ci_cd": self.ci
            }
        }

    def _scaffold_react_native(self):
        """Scaffold React Native or Expo project"""
        logger.debug(f"Scaffolding {self.framework} project")
        # Create directory structure
        self._create_dir('')
        self._create_dir('src')
        self._create_dir('src/components')
        self._create_dir('src/screens')
        self._create_dir('src/navigation')
        self._create_dir('src/store')
        self._create_dir('src/hooks')
        self._create_dir('src/services')
        self._create_dir('src/utils')
        self._create_dir('src/types')
        self._create_dir('src/assets')
        self._create_dir('src/assets/images')
        self._create_dir('src/assets/fonts')

        # Testing directories
        if self.testing in ['unit', 'all']:
            self._create_dir('__tests__')
            self._create_dir('__tests__/components')
            self._create_dir('__tests__/screens')
            self._create_dir('__tests__/utils')

        if self.testing in ['e2e', 'all']:
            self._create_dir('e2e')
            self._create_dir('e2e/tests')

        # CI/CD
        if self.ci == 'github-actions':
            self._create_dir('.github')
            self._create_dir('.github/workflows')

        # Create core files
        self._create_file('package.json', self._get_package_json())
        self._create_file('tsconfig.json', self._get_tsconfig())
        self._create_file('babel.config.js', self._get_babel_config())
        self._create_file('.eslintrc.js', self._get_eslint_config())
        self._create_file('.prettierrc', self._get_prettier_config())
        self._create_file('.env.example', self._get_env_example())
        self._create_file('.gitignore', self._get_gitignore())
        self._create_file('README.md', self._get_readme_react_native())

        # App entry point
        if self.framework == 'expo':
            self._create_file('App.tsx', self._get_expo_app())
            self._create_file('app.json', self._get_expo_app_json())
        else:
            self._create_file('index.js', self._get_rn_index())
            self._create_file('App.tsx', self._get_rn_app())
            self._create_file('metro.config.js', self._get_metro_config())

        # Navigation
        if self.navigation == 'react-navigation':
            self._create_file('src/navigation/RootNavigator.tsx', self._get_root_navigator())
            self._create_file('src/navigation/types.ts', self._get_navigation_types())

        # State management
        if self.state == 'redux':
            self._create_file('src/store/index.ts', self._get_redux_store())
            self._create_file('src/store/slices/exampleSlice.ts', self._get_redux_slice())
        elif self.state == 'zustand':
            self._create_file('src/store/useExampleStore.ts', self._get_zustand_store())

        # Sample components and screens
        self._create_file('src/screens/HomeScreen.tsx', self._get_home_screen())
        self._create_file('src/components/Button.tsx', self._get_button_component())

        # Testing setup
        if self.testing in ['unit', 'all']:
            self._create_file('jest.config.js', self._get_jest_config())
            self._create_file('__tests__/App.test.tsx', self._get_app_test())

        if self.testing in ['e2e', 'all']:
            self._create_file('e2e/.detoxrc.js', self._get_detox_config())
            self._create_file('e2e/tests/app.e2e.ts', self._get_e2e_test())

        # CI/CD
        if self.ci == 'github-actions':
            self._create_file('.github/workflows/ci.yml', self._get_github_actions_rn())

    def _scaffold_flutter(self):
        """Scaffold Flutter project"""
        logger.debug("Scaffolding Flutter project")
        # Create directory structure
        self._create_dir('')
        self._create_dir('lib')
        self._create_dir('lib/core')
        self._create_dir('lib/core/constants')
        self._create_dir('lib/core/theme')
        self._create_dir('lib/core/utils')
        self._create_dir('lib/features')
        self._create_dir('lib/features/home')
        self._create_dir('lib/features/home/presentation')
        self._create_dir('lib/features/home/presentation/screens')
        self._create_dir('lib/features/home/presentation/widgets')
        self._create_dir('lib/shared')
        self._create_dir('lib/shared/widgets')

        # Testing directories
        if self.testing in ['unit', 'integration', 'all']:
            self._create_dir('test')
            self._create_dir('test/features')
            self._create_dir('test/features/home')

        if self.testing in ['integration', 'all']:
            self._create_dir('integration_test')

        # Assets
        self._create_dir('assets')
        self._create_dir('assets/images')
        self._create_dir('assets/fonts')

        # CI/CD
        if self.ci == 'github-actions':
            self._create_dir('.github')
            self._create_dir('.github/workflows')

        # Create core files
        self._create_file('pubspec.yaml', self._get_pubspec_yaml())
        self._create_file('analysis_options.yaml', self._get_analysis_options())
        self._create_file('.env.example', self._get_env_example())
        self._create_file('.gitignore', self._get_gitignore_flutter())
        self._create_file('README.md', self._get_readme_flutter())

        # App entry point
        self._create_file('lib/main.dart', self._get_flutter_main())

        # Core files
        self._create_file('lib/core/constants/app_constants.dart', self._get_app_constants())
        self._create_file('lib/core/theme/app_theme.dart', self._get_app_theme())

        # Navigation
        if self.navigation == 'go_router':
            self._create_file('lib/core/router/app_router.dart', self._get_go_router())

        # State management
        if self.state == 'provider':
            self._create_file('lib/core/providers/example_provider.dart', self._get_provider_example())
        elif self.state == 'riverpod':
            self._create_file('lib/core/providers/example_provider.dart', self._get_riverpod_example())
        elif self.state == 'bloc':
            self._create_file('lib/features/home/presentation/bloc/home_bloc.dart', self._get_bloc_example())
            self._create_file('lib/features/home/presentation/bloc/home_event.dart', self._get_bloc_event())
            self._create_file('lib/features/home/presentation/bloc/home_state.dart', self._get_bloc_state())

        # Sample screens and widgets
        self._create_file('lib/features/home/presentation/screens/home_screen.dart', self._get_flutter_home_screen())
        self._create_file('lib/shared/widgets/custom_button.dart', self._get_flutter_button())

        # Testing setup
        if self.testing in ['unit', 'all']:
            self._create_file('test/features/home/home_screen_test.dart', self._get_flutter_test())

        if self.testing in ['integration', 'all']:
            self._create_file('integration_test/app_test.dart', self._get_flutter_integration_test())

        # CI/CD
        if self.ci == 'github-actions':
            self._create_file('.github/workflows/ci.yml', self._get_github_actions_flutter())

    def _create_dir(self, path: str):
        """Create directory if not in dry run mode"""
        dir_path = self.project_path / path if path else self.project_path

        if self.verbose:
            print(f"{'[DRY RUN] ' if self.dry_run else ''}Creating directory: {dir_path}")

        if not self.dry_run:
            dir_path.mkdir(parents=True, exist_ok=True)

        self.dirs_created.append(str(dir_path))

    def _create_file(self, path: str, content: str):
        """Create file with content if not in dry run mode"""
        file_path = self.project_path / path

        if self.verbose:
            print(f"{'[DRY RUN] ' if self.dry_run else ''}Creating file: {file_path}")

        if not self.dry_run:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

        self.files_created.append(str(file_path))

    # ============================================================================
    # React Native / Expo File Content Templates
    # ============================================================================

    def _get_package_json(self) -> str:
        """Generate package.json for React Native/Expo"""
        is_expo = self.framework == 'expo'

        base_deps = {
            "react": "18.2.0",
            "react-native": "0.72.6" if not is_expo else None
        }

        if is_expo:
            base_deps["expo"] = "~49.0.0"
            base_deps["expo-status-bar"] = "~1.6.0"

        if self.navigation == 'react-navigation':
            base_deps["@react-navigation/native"] = "^6.1.9"
            base_deps["@react-navigation/native-stack"] = "^6.9.17"
            base_deps["react-native-screens"] = "^3.27.0"
            base_deps["react-native-safe-area-context"] = "^4.7.4"

        if self.state == 'redux':
            base_deps["@reduxjs/toolkit"] = "^1.9.7"
            base_deps["react-redux"] = "^8.1.3"
        elif self.state == 'zustand':
            base_deps["zustand"] = "^4.4.7"

        # Remove None values
        base_deps = {k: v for k, v in base_deps.items() if v is not None}

        dev_deps = {
            "@types/react": "~18.2.14",
            "@types/react-native": "0.72.5" if not is_expo else None,
            "typescript": "^5.1.3",
            "@typescript-eslint/eslint-plugin": "^6.10.0",
            "@typescript-eslint/parser": "^6.10.0",
            "eslint": "^8.53.0",
            "prettier": "^3.1.0"
        }

        if self.testing in ['unit', 'all']:
            dev_deps["jest"] = "^29.7.0"
            dev_deps["@testing-library/react-native"] = "^12.4.0"
            dev_deps["@testing-library/jest-native"] = "^5.4.3"

        if self.testing in ['e2e', 'all']:
            dev_deps["detox"] = "^20.13.5"

        # Remove None values
        dev_deps = {k: v for k, v in dev_deps.items() if v is not None}

        package = {
            "name": self.project_name.lower(),
            "version": "1.0.0",
            "description": f"Mobile application built with {self.framework}",
            "main": "index.js" if not is_expo else "node_modules/expo/AppEntry.js",
            "scripts": {
                "start": "expo start" if is_expo else "react-native start",
                "android": "expo run:android" if is_expo else "react-native run-android",
                "ios": "expo run:ios" if is_expo else "react-native run-ios",
                "test": "jest",
                "lint": "eslint . --ext .js,.jsx,.ts,.tsx",
                "format": "prettier --write \"src/**/*.{js,jsx,ts,tsx,json}\""
            },
            "dependencies": base_deps,
            "devDependencies": dev_deps
        }

        return json.dumps(package, indent=2)

    def _get_tsconfig(self) -> str:
        """Generate TypeScript configuration"""
        return '''{
  "compilerOptions": {
    "target": "esnext",
    "module": "commonjs",
    "lib": ["esnext"],
    "jsx": "react-native",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "resolveJsonModule": true,
    "moduleResolution": "node",
    "allowSyntheticDefaultImports": true,
    "forceConsistentCasingInFileNames": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"]
    }
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "**/*.spec.ts"]
}'''

    def _get_babel_config(self) -> str:
        """Generate Babel configuration"""
        preset = "babel-preset-expo" if self.framework == 'expo' else "module:metro-react-native-babel-preset"
        return f'''module.exports = {{
  presets: ['{preset}'],
  plugins: [
    [
      'module-resolver',
      {{
        root: ['./src'],
        extensions: ['.ios.js', '.android.js', '.js', '.ts', '.tsx', '.json'],
        alias: {{
          '@': './src',
        }},
      }},
    ],
  ],
}};'''

    def _get_eslint_config(self) -> str:
        """Generate ESLint configuration"""
        return '''module.exports = {
  root: true,
  extends: [
    '@react-native-community',
    'plugin:@typescript-eslint/recommended',
  ],
  parser: '@typescript-eslint/parser',
  plugins: ['@typescript-eslint'],
  rules: {
    'react-native/no-inline-styles': 'warn',
    '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
  },
};'''

    def _get_prettier_config(self) -> str:
        """Generate Prettier configuration"""
        return '''{
  "semi": true,
  "singleQuote": true,
  "trailingComma": "es5",
  "tabWidth": 2,
  "printWidth": 100
}'''

    def _get_expo_app(self) -> str:
        """Generate Expo App.tsx entry point"""
        nav_import = "import RootNavigator from './src/navigation/RootNavigator';" if self.navigation == 'react-navigation' else ""
        nav_component = "<RootNavigator />" if self.navigation == 'react-navigation' else "<HomeScreen />"

        return f'''import React from 'react';
import {{ StatusBar }} from 'expo-status-bar';
{nav_import}
{'' if nav_import else "import HomeScreen from './src/screens/HomeScreen';"}

export default function App() {{
  return (
    <>
      <StatusBar style="auto" />
      {nav_component}
    </>
  );
}}'''

    def _get_expo_app_json(self) -> str:
        """Generate Expo app.json"""
        app_config = {
            "expo": {
                "name": self.project_name,
                "slug": self.project_name.lower(),
                "version": "1.0.0",
                "orientation": "portrait",
                "icon": "./assets/icon.png",
                "userInterfaceStyle": "light",
                "splash": {
                    "image": "./assets/splash.png",
                    "resizeMode": "contain",
                    "backgroundColor": "#ffffff"
                },
                "assetBundlePatterns": ["**/*"],
                "ios": {
                    "supportsTablet": True,
                    "bundleIdentifier": f"com.{self.project_name.lower()}.app"
                },
                "android": {
                    "adaptiveIcon": {
                        "foregroundImage": "./assets/adaptive-icon.png",
                        "backgroundColor": "#ffffff"
                    },
                    "package": f"com.{self.project_name.lower()}.app"
                },
                "web": {
                    "favicon": "./assets/favicon.png"
                }
            }
        }
        return json.dumps(app_config, indent=2)

    def _get_rn_index(self) -> str:
        """Generate React Native index.js"""
        return '''import { AppRegistry } from 'react-native';
import App from './App';
import { name as appName } from './app.json';

AppRegistry.registerComponent(appName, () => App);'''

    def _get_rn_app(self) -> str:
        """Generate React Native App.tsx"""
        nav_import = "import RootNavigator from './src/navigation/RootNavigator';" if self.navigation == 'react-navigation' else ""
        nav_component = "<RootNavigator />" if self.navigation == 'react-navigation' else "<HomeScreen />"

        return f'''import React from 'react';
import {{ SafeAreaProvider }} from 'react-native-safe-area-context';
{nav_import}
{'' if nav_import else "import HomeScreen from './src/screens/HomeScreen';"}

const App = () => {{
  return (
    <SafeAreaProvider>
      {nav_component}
    </SafeAreaProvider>
  );
}};

export default App;'''

    def _get_metro_config(self) -> str:
        """Generate Metro bundler configuration"""
        return '''const { getDefaultConfig, mergeConfig } = require('@react-native/metro-config');

/**
 * Metro configuration
 * https://facebook.github.io/metro/docs/configuration
 */
const config = {};

module.exports = mergeConfig(getDefaultConfig(__dirname), config);'''

    def _get_root_navigator(self) -> str:
        """Generate React Navigation root navigator"""
        return '''import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import HomeScreen from '../screens/HomeScreen';
import type { RootStackParamList } from './types';

const Stack = createNativeStackNavigator<RootStackParamList>();

const RootNavigator = () => {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen
          name="Home"
          component={HomeScreen}
          options={{ title: 'Home' }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
};

export default RootNavigator;'''

    def _get_navigation_types(self) -> str:
        """Generate navigation TypeScript types"""
        return '''import type { NativeStackScreenProps } from '@react-navigation/native-stack';

export type RootStackParamList = {
  Home: undefined;
};

export type RootStackScreenProps<T extends keyof RootStackParamList> =
  NativeStackScreenProps<RootStackParamList, T>;'''

    def _get_redux_store(self) -> str:
        """Generate Redux store configuration"""
        return '''import { configureStore } from '@reduxjs/toolkit';
import exampleReducer from './slices/exampleSlice';

export const store = configureStore({
  reducer: {
    example: exampleReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;'''

    def _get_redux_slice(self) -> str:
        """Generate Redux slice example"""
        return '''import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface ExampleState {
  value: number;
  status: 'idle' | 'loading' | 'succeeded' | 'failed';
}

const initialState: ExampleState = {
  value: 0,
  status: 'idle',
};

export const exampleSlice = createSlice({
  name: 'example',
  initialState,
  reducers: {
    increment: (state) => {
      state.value += 1;
    },
    decrement: (state) => {
      state.value -= 1;
    },
    incrementByAmount: (state, action: PayloadAction<number>) => {
      state.value += action.payload;
    },
  },
});

export const { increment, decrement, incrementByAmount } = exampleSlice.actions;
export default exampleSlice.reducer;'''

    def _get_zustand_store(self) -> str:
        """Generate Zustand store example"""
        return '''import { create } from 'zustand';

interface ExampleStore {
  count: number;
  increment: () => void;
  decrement: () => void;
  reset: () => void;
}

export const useExampleStore = create<ExampleStore>((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
  decrement: () => set((state) => ({ count: state.count - 1 })),
  reset: () => set({ count: 0 }),
}));'''

    def _get_home_screen(self) -> str:
        """Generate HomeScreen component"""
        # Using double curly braces to escape them in f-string
        return f'''import React from 'react';
import {{ View, Text, StyleSheet }} from 'react-native';
import Button from '../components/Button';

const HomeScreen = () => {{
  const handlePress = () => {{
    console.log('Button pressed!');
  }};

  return (
    <View style={{styles.container}}>
      <Text style={{styles.title}}>Welcome to {self.project_name}</Text>
      <Text style={{styles.subtitle}}>Start building your mobile app</Text>
      <Button title="Get Started" onPress={{handlePress}} />
    </View>
  );
}};

const styles = StyleSheet.create({{
  container: {{
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#fff',
    padding: 20,
  }},
  title: {{
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 10,
  }},
  subtitle: {{
    fontSize: 16,
    color: '#666',
    marginBottom: 30,
    textAlign: 'center',
  }},
}});

export default HomeScreen;'''

    def _get_button_component(self) -> str:
        """Generate Button component"""
        return '''import React from 'react';
import { TouchableOpacity, Text, StyleSheet, TouchableOpacityProps } from 'react-native';

interface ButtonProps extends TouchableOpacityProps {
  title: string;
  variant?: 'primary' | 'secondary';
}

const Button: React.FC<ButtonProps> = ({ title, variant = 'primary', ...props }) => {
  return (
    <TouchableOpacity
      style={[styles.button, styles[variant]]}
      activeOpacity={0.8}
      {...props}
    >
      <Text style={styles.text}>{title}</Text>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  button: {
    paddingVertical: 12,
    paddingHorizontal: 24,
    borderRadius: 8,
    alignItems: 'center',
    justifyContent: 'center',
  },
  primary: {
    backgroundColor: '#007AFF',
  },
  secondary: {
    backgroundColor: '#5856D6',
  },
  text: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
});

export default Button;'''

    def _get_jest_config(self) -> str:
        """Generate Jest configuration"""
        return '''module.exports = {
  preset: 'react-native',
  setupFilesAfterEnv: ['@testing-library/jest-native/extend-expect'],
  transformIgnorePatterns: [
    'node_modules/(?!(react-native|@react-native|@react-navigation)/)',
  ],
  collectCoverageFrom: [
    'src/**/*.{js,jsx,ts,tsx}',
    '!src/**/*.d.ts',
    '!src/**/*.stories.{js,jsx,ts,tsx}',
  ],
};'''

    def _get_app_test(self) -> str:
        """Generate App test"""
        return '''import React from 'react';
import { render } from '@testing-library/react-native';
import App from '../App';

describe('App', () => {
  it('renders correctly', () => {
    const { getByText } = render(<App />);
    expect(getByText(/Welcome/i)).toBeTruthy();
  });
});'''

    def _get_detox_config(self) -> str:
        """Generate Detox configuration"""
        return '''module.exports = {
  testRunner: 'jest',
  runnerConfig: 'e2e/config.json',
  apps: {
    'ios.release': {
      type: 'ios.app',
      build: 'xcodebuild -workspace ios/App.xcworkspace -scheme App -configuration Release -sdk iphonesimulator -derivedDataPath ios/build',
      binaryPath: 'ios/build/Build/Products/Release-iphonesimulator/App.app',
    },
    'android.release': {
      type: 'android.apk',
      build: 'cd android && ./gradlew assembleRelease assembleAndroidTest -DtestBuildType=release',
      binaryPath: 'android/app/build/outputs/apk/release/app-release.apk',
    },
  },
  devices: {
    simulator: {
      type: 'ios.simulator',
      device: { type: 'iPhone 14' },
    },
    emulator: {
      type: 'android.emulator',
      device: { avdName: 'Pixel_5_API_31' },
    },
  },
  configurations: {
    'ios.sim.release': {
      device: 'simulator',
      app: 'ios.release',
    },
    'android.emu.release': {
      device: 'emulator',
      app: 'android.release',
    },
  },
};'''

    def _get_e2e_test(self) -> str:
        """Generate E2E test"""
        return '''describe('App', () => {
  beforeAll(async () => {
    await device.launchApp();
  });

  beforeEach(async () => {
    await device.reloadReactNative();
  });

  it('should display welcome message', async () => {
    await expect(element(by.text('Welcome'))).toBeVisible();
  });

  it('should navigate after button press', async () => {
    await element(by.id('get-started-button')).tap();
    await expect(element(by.text('Next Screen'))).toBeVisible();
  });
});'''

    def _get_github_actions_rn(self) -> str:
        """Generate GitHub Actions workflow for React Native"""
        return f'''name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run linter
        run: npm run lint

      - name: Run type check
        run: npx tsc --noEmit

      - name: Run tests
        run: npm test -- --coverage

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/coverage-final.json

  build-android:
    needs: test
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'

      - name: Setup Java
        uses: actions/setup-java@v3
        with:
          distribution: 'temurin'
          java-version: '11'

      - name: Install dependencies
        run: npm ci

      - name: Build Android
        run: |
          cd android
          ./gradlew assembleRelease

  build-ios:
    needs: test
    runs-on: macos-latest

    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Install CocoaPods
        run: |
          cd ios
          pod install

      - name: Build iOS
        run: |
          cd ios
          xcodebuild -workspace {self.project_name}.xcworkspace \\
            -scheme {self.project_name} \\
            -configuration Release \\
            -sdk iphonesimulator \\
            -derivedDataPath build
'''

    # ============================================================================
    # Flutter File Content Templates
    # ============================================================================

    def _get_pubspec_yaml(self) -> str:
        """Generate pubspec.yaml for Flutter"""
        deps = {
            "flutter": {"sdk": "flutter"},
            "cupertino_icons": "^1.0.2"
        }

        if self.navigation == 'go_router':
            deps["go_router"] = "^12.1.1"
        elif self.navigation == 'auto_route':
            deps["auto_route"] = "^7.8.4"

        if self.state == 'provider':
            deps["provider"] = "^6.1.1"
        elif self.state == 'riverpod':
            deps["flutter_riverpod"] = "^2.4.9"
            deps["riverpod_annotation"] = "^2.3.3"
        elif self.state == 'bloc':
            deps["flutter_bloc"] = "^8.1.3"
            deps["bloc"] = "^8.1.2"

        dev_deps = {
            "flutter_test": {"sdk": "flutter"},
            "flutter_lints": "^3.0.0"
        }

        if self.testing in ['integration', 'all']:
            dev_deps["integration_test"] = {"sdk": "flutter"}

        yaml = f'''name: {self.project_name.lower()}
description: Mobile application built with Flutter
version: 1.0.0+1

environment:
  sdk: '>=3.0.0 <4.0.0'

dependencies:
'''
        for key, value in deps.items():
            if isinstance(value, dict):
                yaml += f'  {key}:\n    sdk: {value["sdk"]}\n'
            else:
                yaml += f'  {key}: {value}\n'

        yaml += '\ndev_dependencies:\n'
        for key, value in dev_deps.items():
            if isinstance(value, dict):
                yaml += f'  {key}:\n    sdk: {value["sdk"]}\n'
            else:
                yaml += f'  {key}: {value}\n'

        yaml += '''
flutter:
  uses-material-design: true

  # assets:
  #   - assets/images/
  #   - assets/fonts/
'''
        return yaml

    def _get_analysis_options(self) -> str:
        """Generate analysis_options.yaml"""
        return '''include: package:flutter_lints/flutter.yaml

linter:
  rules:
    - always_declare_return_types
    - always_require_non_null_named_parameters
    - avoid_print
    - avoid_empty_else
    - prefer_const_constructors
    - prefer_const_literals_to_create_immutables
    - prefer_single_quotes
    - sort_child_properties_last

analyzer:
  errors:
    missing_required_param: error
    missing_return: error
'''

    def _get_flutter_main(self) -> str:
        """Generate Flutter main.dart"""
        if self.state == 'provider':
            wrapper = '''  runApp(
    MultiProvider(
      providers: [],
      child: const MyApp(),
    ),
  );'''
        elif self.state == 'riverpod':
            wrapper = '''  runApp(
    const ProviderScope(
      child: MyApp(),
    ),
  );'''
        else:
            wrapper = '  runApp(const MyApp());'

        router_setup = ''
        if self.navigation == 'go_router':
            router_setup = f'''  final router = AppRouter.router;

  @override
  Widget build(BuildContext context) {{
    return MaterialApp.router(
      title: '{self.project_name}',
      theme: AppTheme.lightTheme,
      routerConfig: router,
    );
  }}'''
        else:
            router_setup = f'''  @override
  Widget build(BuildContext context) {{
    return MaterialApp(
      title: '{self.project_name}',
      theme: AppTheme.lightTheme,
      home: const HomeScreen(),
    );
  }}'''

        return f'''import 'package:flutter/material.dart';
{("import 'package:flutter_riverpod/flutter_riverpod.dart';" if self.state == 'riverpod' else "")}
{("import 'package:provider/provider.dart';" if self.state == 'provider' else "")}
import 'core/theme/app_theme.dart';
{("import 'core/router/app_router.dart';" if self.navigation == 'go_router' else "")}
{("import 'features/home/presentation/screens/home_screen.dart';" if self.navigation != 'go_router' else "")}

void main() {{
{wrapper}
}}

class MyApp extends StatelessWidget {{
  const MyApp({{super.key}});

{router_setup}
}}'''

    def _get_app_constants(self) -> str:
        """Generate app_constants.dart"""
        return f'''class AppConstants {{
  // App Information
  static const String appName = '{self.project_name}';
  static const String appVersion = '1.0.0';

  // API Configuration
  static const String apiBaseUrl = 'https://api.example.com';
  static const Duration apiTimeout = Duration(seconds: 30);

  // UI Constants
  static const double defaultPadding = 16.0;
  static const double defaultBorderRadius = 8.0;

  // Animation Durations
  static const Duration shortAnimation = Duration(milliseconds: 200);
  static const Duration mediumAnimation = Duration(milliseconds: 400);
  static const Duration longAnimation = Duration(milliseconds: 600);
}}'''

    def _get_app_theme(self) -> str:
        """Generate app_theme.dart"""
        return '''import 'package:flutter/material.dart';

class AppTheme {
  static ThemeData get lightTheme {
    return ThemeData(
      useMaterial3: true,
      colorScheme: ColorScheme.fromSeed(
        seedColor: Colors.blue,
        brightness: Brightness.light,
      ),
      appBarTheme: const AppBarTheme(
        centerTitle: true,
        elevation: 0,
      ),
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(8),
          ),
        ),
      ),
    );
  }

  static ThemeData get darkTheme {
    return ThemeData(
      useMaterial3: true,
      colorScheme: ColorScheme.fromSeed(
        seedColor: Colors.blue,
        brightness: Brightness.dark,
      ),
      appBarTheme: const AppBarTheme(
        centerTitle: true,
        elevation: 0,
      ),
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(8),
          ),
        ),
      ),
    );
  }
}'''

    def _get_go_router(self) -> str:
        """Generate GoRouter configuration"""
        return '''import 'package:go_router/go_router.dart';
import '../../features/home/presentation/screens/home_screen.dart';

class AppRouter {
  static final router = GoRouter(
    initialLocation: '/',
    routes: [
      GoRoute(
        path: '/',
        name: 'home',
        builder: (context, state) => const HomeScreen(),
      ),
    ],
  );
}'''

    def _get_provider_example(self) -> str:
        """Generate Provider example"""
        return '''import 'package:flutter/foundation.dart';

class ExampleProvider with ChangeNotifier {
  int _count = 0;

  int get count => _count;

  void increment() {
    _count++;
    notifyListeners();
  }

  void decrement() {
    _count--;
    notifyListeners();
  }

  void reset() {
    _count = 0;
    notifyListeners();
  }
}'''

    def _get_riverpod_example(self) -> str:
        """Generate Riverpod example"""
        return '''import 'package:flutter_riverpod/flutter_riverpod.dart';

class Counter {
  const Counter(this.value);
  final int value;
}

class CounterNotifier extends StateNotifier<Counter> {
  CounterNotifier() : super(const Counter(0));

  void increment() {
    state = Counter(state.value + 1);
  }

  void decrement() {
    state = Counter(state.value - 1);
  }

  void reset() {
    state = const Counter(0);
  }
}

final counterProvider = StateNotifierProvider<CounterNotifier, Counter>((ref) {
  return CounterNotifier();
});'''

    def _get_bloc_example(self) -> str:
        """Generate BLoC example"""
        return '''import 'package:flutter_bloc/flutter_bloc.dart';
import 'home_event.dart';
import 'home_state.dart';

class HomeBloc extends Bloc<HomeEvent, HomeState> {
  HomeBloc() : super(HomeInitial()) {
    on<LoadHomeData>(_onLoadHomeData);
  }

  Future<void> _onLoadHomeData(
    LoadHomeData event,
    Emitter<HomeState> emit,
  ) async {
    emit(HomeLoading());
    try {
      // Simulate API call
      await Future.delayed(const Duration(seconds: 1));
      emit(HomeLoaded(data: 'Home data loaded successfully'));
    } catch (e) {
      emit(HomeError(message: e.toString()));
    }
  }
}'''

    def _get_bloc_event(self) -> str:
        """Generate BLoC event"""
        return '''abstract class HomeEvent {}

class LoadHomeData extends HomeEvent {}'''

    def _get_bloc_state(self) -> str:
        """Generate BLoC state"""
        return '''abstract class HomeState {}

class HomeInitial extends HomeState {}

class HomeLoading extends HomeState {}

class HomeLoaded extends HomeState {
  HomeLoaded({required this.data});
  final String data;
}

class HomeError extends HomeState {
  HomeError({required this.message});
  final String message;
}'''

    def _get_flutter_home_screen(self) -> str:
        """Generate Flutter home screen"""
        return f'''import 'package:flutter/material.dart';
import '../../../../shared/widgets/custom_button.dart';

class HomeScreen extends StatelessWidget {{
  const HomeScreen({{super.key}});

  @override
  Widget build(BuildContext context) {{
    return Scaffold(
      appBar: AppBar(
        title: const Text('{self.project_name}'),
      ),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text(
                'Welcome to {self.project_name}',
                style: Theme.of(context).textTheme.headlineMedium,
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 16),
              Text(
                'Start building your mobile app',
                style: Theme.of(context).textTheme.bodyLarge,
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 32),
              CustomButton(
                text: 'Get Started',
                onPressed: () {{
                  // Navigate to next screen
                }},
              ),
            ],
          ),
        ),
      ),
    );
  }}
}}'''

    def _get_flutter_button(self) -> str:
        """Generate Flutter custom button"""
        return '''import 'package:flutter/material.dart';

class CustomButton extends StatelessWidget {
  const CustomButton({
    super.key,
    required this.text,
    required this.onPressed,
    this.variant = ButtonVariant.primary,
  });

  final String text;
  final VoidCallback onPressed;
  final ButtonVariant variant;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return ElevatedButton(
      onPressed: onPressed,
      style: ElevatedButton.styleFrom(
        backgroundColor: variant == ButtonVariant.primary
            ? theme.colorScheme.primary
            : theme.colorScheme.secondary,
        foregroundColor: Colors.white,
      ),
      child: Text(text),
    );
  }
}

enum ButtonVariant { primary, secondary }'''

    def _get_flutter_test(self) -> str:
        """Generate Flutter widget test"""
        return f'''import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:{self.project_name.lower()}/features/home/presentation/screens/home_screen.dart';

void main() {{
  testWidgets('HomeScreen displays welcome message', (WidgetTester tester) async {{
    await tester.pumpWidget(
      const MaterialApp(
        home: HomeScreen(),
      ),
    );

    expect(find.text('Welcome'), findsOneWidget);
    expect(find.text('Get Started'), findsOneWidget);
  }});

  testWidgets('Button tap triggers callback', (WidgetTester tester) async {{
    await tester.pumpWidget(
      const MaterialApp(
        home: HomeScreen(),
      ),
    );

    await tester.tap(find.text('Get Started'));
    await tester.pump();

    // Add assertions for navigation or state changes
  }});
}}'''

    def _get_flutter_integration_test(self) -> str:
        """Generate Flutter integration test"""
        return f'''import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:{self.project_name.lower()}/main.dart' as app;

void main() {{
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('end-to-end test', () {{
    testWidgets('app launches and displays home screen', (tester) async {{
      app.main();
      await tester.pumpAndSettle();

      expect(find.text('Welcome'), findsOneWidget);
    }});

    testWidgets('navigation flow works correctly', (tester) async {{
      app.main();
      await tester.pumpAndSettle();

      await tester.tap(find.text('Get Started'));
      await tester.pumpAndSettle();

      // Add navigation assertions
    }});
  }});
}}'''

    def _get_github_actions_flutter(self) -> str:
        """Generate GitHub Actions workflow for Flutter"""
        return '''name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Setup Flutter
        uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.16.0'
          channel: 'stable'

      - name: Get dependencies
        run: flutter pub get

      - name: Analyze
        run: flutter analyze

      - name: Run tests
        run: flutter test --coverage

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/lcov.info

  build-android:
    needs: test
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Setup Flutter
        uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.16.0'
          channel: 'stable'

      - name: Setup Java
        uses: actions/setup-java@v3
        with:
          distribution: 'temurin'
          java-version: '11'

      - name: Get dependencies
        run: flutter pub get

      - name: Build APK
        run: flutter build apk --release

  build-ios:
    needs: test
    runs-on: macos-latest

    steps:
      - uses: actions/checkout@v3

      - name: Setup Flutter
        uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.16.0'
          channel: 'stable'

      - name: Get dependencies
        run: flutter pub get

      - name: Build iOS (no codesign)
        run: flutter build ios --release --no-codesign
'''

    # ============================================================================
    # Common Files
    # ============================================================================

    def _get_env_example(self) -> str:
        """Generate .env.example"""
        return '''# API Configuration
API_BASE_URL=https://api.example.com
API_KEY=your_api_key_here
API_TIMEOUT=30000

# Environment
ENVIRONMENT=development

# Features
ENABLE_ANALYTICS=false
ENABLE_CRASH_REPORTING=false'''

    def _get_gitignore(self) -> str:
        """Generate .gitignore for React Native/Expo"""
        return '''# OSX
.DS_Store

# Node
node_modules/
npm-debug.log
yarn-error.log

# Expo
.expo/
.expo-shared/
dist/
web-build/

# React Native
*.jks
*.p8
*.p12
*.key
*.mobileprovision
*.orig.*

# Android
*.apk
*.ap_
*.aab
/android/app/debug
/android/app/release
/android/.gradle
/android/captures/
/android/build/

# iOS
*.pbxuser
!default.pbxuser
*.mode1v3
!default.mode1v3
*.mode2v3
!default.mode2v3
*.perspectivev3
!default.perspectivev3
xcuserdata
*.xccheckout
*.moved-aside
DerivedData
*.hmap
*.ipa
*.xcuserstate
ios/Pods/
ios/build/

# Fastlane
fastlane/report.xml
fastlane/Preview.html
fastlane/screenshots
fastlane/test_output

# Environment
.env
.env.local
.env.*.local

# Testing
coverage/
.nyc_output/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Misc
.cache/'''

    def _get_gitignore_flutter(self) -> str:
        """Generate .gitignore for Flutter"""
        return '''# Miscellaneous
*.class
*.log
*.pyc
*.swp
.DS_Store
.atom/
.buildlog/
.history
.svn/
migrate_working_dir/

# IntelliJ related
*.iml
*.ipr
*.iws
.idea/

# VS Code
.vscode/

# Flutter/Dart/Pub related
**/doc/api/
**/ios/Flutter/.last_build_id
.dart_tool/
.flutter-plugins
.flutter-plugins-dependencies
.packages
.pub-cache/
.pub/
/build/

# Symbolication related
app.*.symbols

# Obfuscation related
app.*.map.json

# Android Studio
*.iml
.gradle
/local.properties
/.idea/caches
/.idea/libraries
/.idea/modules.xml
/.idea/workspace.xml
/.idea/navEditor.xml
/.idea/assetWizardSettings.xml
.DS_Store
/build
/captures
.externalNativeBuild
.cxx
local.properties

# iOS
**/ios/**/*.mode1v3
**/ios/**/*.mode2v3
**/ios/**/*.moved-aside
**/ios/**/*.pbxuser
**/ios/**/*.perspectivev3
**/ios/**/*sync/
**/ios/**/.sconsign.dblite
**/ios/**/.tags*
**/ios/**/.vagrant/
**/ios/**/DerivedData/
**/ios/**/Icon?
**/ios/**/Pods/
**/ios/**/.symlinks/
**/ios/**/profile
**/ios/**/xcuserdata
**/ios/.generated/
**/ios/Flutter/.last_build_id
**/ios/Flutter/App.framework
**/ios/Flutter/Flutter.framework
**/ios/Flutter/Flutter.podspec
**/ios/Flutter/Generated.xcconfig
**/ios/Flutter/ephemeral
**/ios/Flutter/app.flx
**/ios/Flutter/app.zip
**/ios/Flutter/flutter_assets/
**/ios/Flutter/flutter_export_environment.sh
**/ios/ServiceDefinitions.json
**/ios/Runner/GeneratedPluginRegistrant.*

# Environment
.env
.env.local
.env.*.local

# Coverage
coverage/

# Exceptions to above rules.
!**/ios/**/default.mode1v3
!**/ios/**/default.mode2v3
!**/ios/**/default.pbxuser
!**/ios/**/default.perspectivev3'''

    def _get_readme_react_native(self) -> str:
        """Generate README for React Native"""
        install_cmd = "npm install"
        run_cmd = "npm start" if self.framework == 'expo' else "npm run ios # or npm run android"

        return f'''# {self.project_name}

Mobile application built with {self.framework.replace('-', ' ').title()}

## Features

- **Framework:** {self.framework}
- **Platforms:** {self.platforms}
- **Navigation:** {self.navigation}
- **State Management:** {self.state}
- **Testing:** {self.testing}
- **CI/CD:** {self.ci}

## Getting Started

### Prerequisites

- Node.js 18+
- npm or yarn
{"- Xcode (for iOS development)" if self.platforms in ['ios', 'both'] else ""}
{"- Android Studio (for Android development)" if self.platforms in ['android', 'both'] else ""}
{"- Expo CLI: `npm install -g expo-cli`" if self.framework == 'expo' else ""}

### Installation

1. Install dependencies:
```bash
{install_cmd}
```

2. Copy environment variables:
```bash
cp .env.example .env
```

3. Edit `.env` with your configuration

### Running the App

```bash
{run_cmd}
```

### Testing

```bash
# Run unit tests
npm test

# Run with coverage
npm test -- --coverage

# Run E2E tests
npm run test:e2e
```

### Building

#### iOS
```bash
npm run ios:build
```

#### Android
```bash
npm run android:build
```

## Project Structure

```
src/
├── components/     # Reusable UI components
├── screens/        # Screen components
├── navigation/     # Navigation configuration
├── store/          # State management
├── hooks/          # Custom React hooks
├── services/       # API and external services
├── utils/          # Utility functions
└── types/          # TypeScript type definitions
```

## Scripts

- `npm start` - Start development server
- `npm run ios` - Run on iOS simulator
- `npm run android` - Run on Android emulator
- `npm test` - Run tests
- `npm run lint` - Run linter
- `npm run format` - Format code with Prettier

## Tech Stack

- **Language:** TypeScript
- **Framework:** {self.framework}
- **Navigation:** {self.navigation}
- **State:** {self.state}
- **Testing:** Jest, React Native Testing Library
- **Linting:** ESLint + Prettier

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## License

MIT License - see LICENSE file for details

---

Generated with mobile_scaffolder.py
'''

    def _get_readme_flutter(self) -> str:
        """Generate README for Flutter"""
        return f'''# {self.project_name}

Mobile application built with Flutter

## Features

- **Framework:** Flutter
- **Platforms:** {self.platforms}
- **Navigation:** {self.navigation}
- **State Management:** {self.state}
- **Testing:** {self.testing}
- **CI/CD:** {self.ci}

## Getting Started

### Prerequisites

- Flutter SDK 3.16.0+
- Dart 3.0.0+
{"- Xcode (for iOS development)" if self.platforms in ['ios', 'both'] else ""}
{"- Android Studio (for Android development)" if self.platforms in ['android', 'both'] else ""}

### Installation

1. Get dependencies:
```bash
flutter pub get
```

2. Copy environment variables:
```bash
cp .env.example .env
```

3. Edit `.env` with your configuration

### Running the App

```bash
# Debug mode
flutter run

# Release mode
flutter run --release
```

### Testing

```bash
# Run unit tests
flutter test

# Run with coverage
flutter test --coverage

# Run integration tests
flutter test integration_test/
```

### Building

#### Android APK
```bash
flutter build apk --release
```

#### Android App Bundle
```bash
flutter build appbundle --release
```

#### iOS
```bash
flutter build ios --release
```

## Project Structure

```
lib/
├── core/
│   ├── constants/    # App constants
│   ├── theme/        # Theme configuration
│   ├── router/       # Navigation setup
│   └── utils/        # Utility functions
├── features/
│   └── home/         # Feature modules
│       ├── data/
│       ├── domain/
│       └── presentation/
└── shared/
    └── widgets/      # Reusable widgets
```

## Scripts

- `flutter run` - Run in debug mode
- `flutter test` - Run tests
- `flutter analyze` - Analyze code
- `flutter pub get` - Get dependencies

## Tech Stack

- **Language:** Dart
- **Framework:** Flutter
- **Navigation:** {self.navigation}
- **State:** {self.state}
- **Testing:** flutter_test
- **Architecture:** Clean Architecture

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## License

MIT License - see LICENSE file for details

---

Generated with mobile_scaffolder.py
'''


def format_text_output(results: Dict[str, Any], verbose: bool = False) -> str:
    """Format results as human-readable text"""
    output = "=" * 60 + "\n"
    output += "Mobile Project Scaffolding Complete\n"
    output += "=" * 60 + "\n\n"

    output += f"Status: {results['status']}\n"
    output += f"Project: {results['project_name']}\n"
    output += f"Framework: {results['framework']}\n"
    output += f"Location: {results['project_path']}\n\n"

    output += "Configuration:\n"
    config = results['configuration']
    output += f"  Platforms: {config['platforms']}\n"
    output += f"  Navigation: {config['navigation']}\n"
    output += f"  State Management: {config['state_management']}\n"
    output += f"  Testing: {config['testing']}\n"
    output += f"  CI/CD: {config['ci_cd']}\n\n"

    output += f"Created:\n"
    output += f"  {results['directories_created']} directories\n"
    output += f"  {results['files_created']} files\n"
    output += f"  Duration: {results['duration_ms']}ms\n\n"

    output += "Next Steps:\n"
    output += f"  cd {results['project_name']}\n"

    if results['framework'] in ['react-native', 'expo']:
        output += "  npm install\n"
        output += "  cp .env.example .env\n"
        if results['framework'] == 'expo':
            output += "  npm start\n"
        else:
            output += "  npm run ios  # or npm run android\n"
    else:
        output += "  flutter pub get\n"
        output += "  cp .env.example .env\n"
        output += "  flutter run\n"

    output += "\n" + "=" * 60 + "\n"

    return output


def format_json_output(results: Dict[str, Any]) -> str:
    """Format results as JSON with metadata"""
    output = {
        "metadata": {
            "tool": "mobile_scaffolder.py",
            "version": "1.0.0",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        },
        "results": results
    }
    return json.dumps(output, indent=2)


def main():
    """Main entry point with CLI argument parsing"""
    parser = argparse.ArgumentParser(
        description='Generate cross-platform mobile project structures',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s MyApp
  %(prog)s MyApp --framework react-native --platforms both
  %(prog)s MyApp -f flutter --state riverpod --testing all
  %(prog)s MyApp -f expo --ci github-actions --dry-run
  %(prog)s MyApp -f react-native -p ios --navigation react-navigation -v

Frameworks:
  react-native   React Native with TypeScript
  flutter        Flutter with Dart
  expo           Expo managed workflow

Navigation:
  React Native:  react-navigation, none
  Flutter:       go_router, auto_route, none

State Management:
  React Native:  redux, zustand, none
  Flutter:       provider, riverpod, bloc, none

For more information, see:
skills/engineering-team/senior-mobile/SKILL.md
        """
    )

    # Positional argument
    parser.add_argument(
        'project_name',
        help='Name of the project to create'
    )

    # Optional arguments
    parser.add_argument(
        '--framework', '-f',
        choices=MobileScaffolder.FRAMEWORKS,
        default='react-native',
        help='Mobile framework (default: react-native)'
    )

    parser.add_argument(
        '--platforms', '-p',
        choices=MobileScaffolder.PLATFORMS,
        default='both',
        help='Target platforms (default: both)'
    )

    parser.add_argument(
        '--navigation',
        help='Navigation library (auto-detected based on framework)'
    )

    parser.add_argument(
        '--state',
        help='State management (auto-detected based on framework)'
    )

    parser.add_argument(
        '--testing',
        choices=MobileScaffolder.TESTING_TYPES,
        default='all',
        help='Testing setup (default: all)'
    )

    parser.add_argument(
        '--ci',
        choices=MobileScaffolder.CI_PLATFORMS,
        default='github-actions',
        help='CI/CD platform (default: github-actions)'
    )

    parser.add_argument(
        '--output-dir', '-d',
        default='.',
        help='Output directory (default: current directory)'
    )

    parser.add_argument(
        '--output', '-o',
        choices=['text', 'json'],
        default='text',
        help='Output format (default: text)'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be created without creating'
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

    try:
        # Create scaffolder instance
        scaffolder = MobileScaffolder(
            project_name=args.project_name,
            framework=args.framework,
            platforms=args.platforms,
            navigation=args.navigation,
            state=args.state,
            testing=args.testing,
            ci=args.ci,
            output_dir=args.output_dir,
            dry_run=args.dry_run,
            verbose=args.verbose
        )

        # Validate configuration
        errors = scaffolder.validate()
        if errors:
            print("Validation errors:", file=sys.stderr)
            for error in errors:
                print(f"  - {error}", file=sys.stderr)
            sys.exit(1)

        # Scaffold project
        results = scaffolder.scaffold()

        # Format and output results
        if args.output == 'json':
            output = format_json_output(results)
        else:
            output = format_text_output(results, verbose=args.verbose)

        print(output)
        sys.exit(0)

    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        sys.exit(130)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
