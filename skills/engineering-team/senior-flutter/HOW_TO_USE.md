# How to Use Senior Flutter Skill

Quick start guide for Flutter and Dart development with Riverpod, Bloc, and clean architecture.

## Quick Start

### 1. Generate Flutter Project

```bash
# Using senior-mobile scaffolder
python3 ../../senior-mobile/scripts/mobile_scaffolder.py \
  --framework flutter \
  --platforms ios,android \
  --navigation go-router \
  --state riverpod \
  --output ./my-flutter-app
```

### 2. Set Up Clean Architecture

```
lib/
├── core/
│   ├── error/
│   ├── network/
│   └── router/
├── features/
│   └── auth/
│       ├── data/
│       ├── domain/
│       └── presentation/
└── main.dart
```

### 3. Implement State Management

**Riverpod (Recommended):**
```dart
@riverpod
class UsersNotifier extends _$UsersNotifier {
  @override
  Future<List<User>> build() async {
    return ref.read(userRepositoryProvider).getUsers();
  }

  Future<void> refresh() async {
    state = const AsyncValue.loading();
    state = await AsyncValue.guard(() =>
      ref.read(userRepositoryProvider).getUsers()
    );
  }
}

// Usage
class UsersScreen extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final usersAsync = ref.watch(usersNotifierProvider);

    return usersAsync.when(
      data: (users) => UserList(users: users),
      loading: () => const CircularProgressIndicator(),
      error: (e, _) => ErrorWidget(error: e),
    );
  }
}
```

## Common Patterns

### Freezed for Immutable Data

```dart
@freezed
class User with _$User {
  const factory User({
    required String id,
    required String name,
    String? email,
  }) = _User;

  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);
}
```

### GoRouter Navigation

```dart
final router = GoRouter(
  routes: [
    GoRoute(
      path: '/',
      builder: (context, state) => const HomeScreen(),
      routes: [
        GoRoute(
          path: 'profile/:id',
          builder: (context, state) => ProfileScreen(
            userId: state.pathParameters['id']!,
          ),
        ),
      ],
    ),
  ],
);
```

### Platform Channels

```dart
class NativeService {
  static const _channel = MethodChannel('com.example/native');

  static Future<String> getNativeData() async {
    return await _channel.invokeMethod('getData');
  }
}
```

## Validation

```bash
# Check project configuration
python3 ../../senior-mobile/scripts/platform_detector.py --check all

# Validate for Google Play
python3 ../../senior-mobile/scripts/app_store_validator.py --store google --strict
```

## Key References

| Reference | Content |
|-----------|---------|
| `dart-patterns.md` | Dart 3.x, null safety, pattern matching |
| `widget-architecture.md` | Widget lifecycle, keys, render |
| `state-management.md` | Riverpod vs Bloc vs Provider |

## Performance Tips

1. Use `const` constructors everywhere possible
2. Add `RepaintBoundary` around expensive widgets
3. Use `ListView.builder` for long lists
4. Profile with Flutter DevTools before optimizing
5. Use `Isolate.run` for heavy computation

## Related Skills

- **senior-mobile** - Cross-platform tools and scaffolding
- **senior-ios** - iOS-specific patterns

## Need More?

See `SKILL.md` for complete workflows and detailed documentation.
