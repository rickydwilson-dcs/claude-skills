# State Management Comparison

Comprehensive comparison of Flutter state management solutions: Riverpod, Bloc, and Provider.

## Quick Decision Guide

| Factor | Riverpod | Bloc | Provider |
|--------|----------|------|----------|
| Learning Curve | Medium | Medium-High | Low |
| Boilerplate | Low | Medium-High | Low |
| Testability | Excellent | Excellent | Good |
| DevTools Support | Good | Excellent | Good |
| Compile-time Safety | Excellent | Good | Good |
| Best For | Most apps | Large teams, strict patterns | Simple apps |

## Riverpod

### Setup

```yaml
# pubspec.yaml
dependencies:
  flutter_riverpod: ^2.4.0
  riverpod_annotation: ^2.3.0

dev_dependencies:
  riverpod_generator: ^2.3.0
  build_runner: ^2.4.0
```

### Basic Providers

```dart
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:riverpod_annotation/riverpod_annotation.dart';

part 'providers.g.dart';

// Simple state provider
@riverpod
int counter(CounterRef ref) => 0;

// Computed provider
@riverpod
int doubleCounter(DoubleCounterRef ref) {
  final count = ref.watch(counterProvider);
  return count * 2;
}

// Async provider
@riverpod
Future<User> user(UserRef ref) async {
  return await userRepository.fetchCurrentUser();
}

// Family provider (with parameter)
@riverpod
Future<User> userById(UserByIdRef ref, String id) async {
  return await userRepository.fetchUser(id);
}
```

### Notifier Providers

```dart
@riverpod
class Counter extends _$Counter {
  @override
  int build() => 0;

  void increment() => state++;
  void decrement() => state--;
  void reset() => state = 0;
}

// Async Notifier
@riverpod
class Users extends _$Users {
  @override
  Future<List<User>> build() async {
    return await ref.read(userRepositoryProvider).fetchUsers();
  }

  Future<void> addUser(User user) async {
    state = const AsyncValue.loading();
    state = await AsyncValue.guard(() async {
      await ref.read(userRepositoryProvider).createUser(user);
      return ref.read(userRepositoryProvider).fetchUsers();
    });
  }

  Future<void> refresh() async {
    state = const AsyncValue.loading();
    state = await AsyncValue.guard(() =>
      ref.read(userRepositoryProvider).fetchUsers()
    );
  }
}
```

### Usage in Widgets

```dart
// Wrap app with ProviderScope
void main() {
  runApp(
    const ProviderScope(
      child: MyApp(),
    ),
  );
}

// ConsumerWidget
class CounterScreen extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final count = ref.watch(counterProvider);
    final users = ref.watch(usersProvider);

    return Column(
      children: [
        Text('Count: $count'),
        ElevatedButton(
          onPressed: () => ref.read(counterProvider.notifier).increment(),
          child: const Text('Increment'),
        ),
        users.when(
          data: (users) => ListView.builder(
            itemCount: users.length,
            itemBuilder: (context, index) => UserTile(user: users[index]),
          ),
          loading: () => const CircularProgressIndicator(),
          error: (error, stack) => Text('Error: $error'),
        ),
      ],
    );
  }
}

// Consumer (for partial rebuilds)
class OptimizedWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        const Text('Static content'),  // Never rebuilds
        Consumer(
          builder: (context, ref, child) {
            final count = ref.watch(counterProvider);
            return Text('Count: $count');  // Only this rebuilds
          },
        ),
      ],
    );
  }
}
```

### Testing with Riverpod

```dart
void main() {
  test('Counter increments', () {
    final container = ProviderContainer();
    addTearDown(container.dispose);

    expect(container.read(counterProvider), 0);

    container.read(counterProvider.notifier).increment();

    expect(container.read(counterProvider), 1);
  });

  test('Users loads successfully', () async {
    final container = ProviderContainer(
      overrides: [
        userRepositoryProvider.overrideWithValue(MockUserRepository()),
      ],
    );
    addTearDown(container.dispose);

    // Wait for async provider
    await container.read(usersProvider.future);

    final users = container.read(usersProvider);
    expect(users.valueOrNull, isNotEmpty);
  });
}
```

## Bloc

### Setup

```yaml
# pubspec.yaml
dependencies:
  flutter_bloc: ^8.1.0
  bloc: ^8.1.0
  equatable: ^2.0.5

dev_dependencies:
  bloc_test: ^9.1.0
```

### Defining Events and States

```dart
import 'package:equatable/equatable.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

// Events
abstract class CounterEvent extends Equatable {
  const CounterEvent();

  @override
  List<Object> get props => [];
}

class CounterIncremented extends CounterEvent {}
class CounterDecremented extends CounterEvent {}
class CounterReset extends CounterEvent {}

// State
class CounterState extends Equatable {
  final int count;

  const CounterState({this.count = 0});

  CounterState copyWith({int? count}) {
    return CounterState(count: count ?? this.count);
  }

  @override
  List<Object> get props => [count];
}

// Bloc
class CounterBloc extends Bloc<CounterEvent, CounterState> {
  CounterBloc() : super(const CounterState()) {
    on<CounterIncremented>(_onIncrement);
    on<CounterDecremented>(_onDecrement);
    on<CounterReset>(_onReset);
  }

  void _onIncrement(CounterIncremented event, Emitter<CounterState> emit) {
    emit(state.copyWith(count: state.count + 1));
  }

  void _onDecrement(CounterDecremented event, Emitter<CounterState> emit) {
    emit(state.copyWith(count: state.count - 1));
  }

  void _onReset(CounterReset event, Emitter<CounterState> emit) {
    emit(const CounterState());
  }
}
```

### Async Bloc with Freezed

```dart
import 'package:freezed_annotation/freezed_annotation.dart';

part 'user_bloc.freezed.dart';

// Events
@freezed
class UserEvent with _$UserEvent {
  const factory UserEvent.loadUsers() = LoadUsers;
  const factory UserEvent.addUser(User user) = AddUser;
  const factory UserEvent.deleteUser(String id) = DeleteUser;
  const factory UserEvent.refresh() = RefreshUsers;
}

// State
@freezed
class UserState with _$UserState {
  const factory UserState.initial() = _Initial;
  const factory UserState.loading() = _Loading;
  const factory UserState.loaded(List<User> users) = _Loaded;
  const factory UserState.error(String message) = _Error;
}

// Bloc
class UserBloc extends Bloc<UserEvent, UserState> {
  final UserRepository _repository;

  UserBloc(this._repository) : super(const UserState.initial()) {
    on<LoadUsers>(_onLoadUsers);
    on<AddUser>(_onAddUser);
    on<DeleteUser>(_onDeleteUser);
    on<RefreshUsers>(_onRefresh);
  }

  Future<void> _onLoadUsers(LoadUsers event, Emitter<UserState> emit) async {
    emit(const UserState.loading());
    try {
      final users = await _repository.fetchUsers();
      emit(UserState.loaded(users));
    } catch (e) {
      emit(UserState.error(e.toString()));
    }
  }

  Future<void> _onAddUser(AddUser event, Emitter<UserState> emit) async {
    final currentState = state;
    if (currentState is _Loaded) {
      try {
        await _repository.createUser(event.user);
        final users = await _repository.fetchUsers();
        emit(UserState.loaded(users));
      } catch (e) {
        emit(UserState.error(e.toString()));
      }
    }
  }

  Future<void> _onDeleteUser(DeleteUser event, Emitter<UserState> emit) async {
    // Implementation
  }

  Future<void> _onRefresh(RefreshUsers event, Emitter<UserState> emit) async {
    try {
      final users = await _repository.fetchUsers();
      emit(UserState.loaded(users));
    } catch (e) {
      emit(UserState.error(e.toString()));
    }
  }
}
```

### Usage in Widgets

```dart
// Provide bloc
void main() {
  runApp(
    MultiBlocProvider(
      providers: [
        BlocProvider(create: (_) => CounterBloc()),
        BlocProvider(create: (context) => UserBloc(
          context.read<UserRepository>(),
        )),
      ],
      child: const MyApp(),
    ),
  );
}

// BlocBuilder
class CounterScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return BlocBuilder<CounterBloc, CounterState>(
      builder: (context, state) {
        return Column(
          children: [
            Text('Count: ${state.count}'),
            Row(
              children: [
                IconButton(
                  icon: const Icon(Icons.remove),
                  onPressed: () =>
                      context.read<CounterBloc>().add(CounterDecremented()),
                ),
                IconButton(
                  icon: const Icon(Icons.add),
                  onPressed: () =>
                      context.read<CounterBloc>().add(CounterIncremented()),
                ),
              ],
            ),
          ],
        );
      },
    );
  }
}

// BlocConsumer (listener + builder)
class UserScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return BlocConsumer<UserBloc, UserState>(
      listener: (context, state) {
        state.maybeWhen(
          error: (message) {
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(content: Text(message)),
            );
          },
          orElse: () {},
        );
      },
      builder: (context, state) {
        return state.when(
          initial: () => const SizedBox.shrink(),
          loading: () => const Center(child: CircularProgressIndicator()),
          loaded: (users) => UserList(users: users),
          error: (message) => ErrorWidget(message: message),
        );
      },
    );
  }
}

// BlocListener (listener only)
BlocListener<AuthBloc, AuthState>(
  listener: (context, state) {
    if (state is Unauthenticated) {
      Navigator.of(context).pushReplacementNamed('/login');
    }
  },
  child: const HomeScreen(),
)
```

### Testing with Bloc

```dart
import 'package:bloc_test/bloc_test.dart';

void main() {
  group('CounterBloc', () {
    blocTest<CounterBloc, CounterState>(
      'emits [CounterState(1)] when CounterIncremented is added',
      build: () => CounterBloc(),
      act: (bloc) => bloc.add(CounterIncremented()),
      expect: () => [const CounterState(count: 1)],
    );

    blocTest<CounterBloc, CounterState>(
      'emits [CounterState(2)] after two increments',
      build: () => CounterBloc(),
      act: (bloc) => bloc
        ..add(CounterIncremented())
        ..add(CounterIncremented()),
      expect: () => [
        const CounterState(count: 1),
        const CounterState(count: 2),
      ],
    );
  });

  group('UserBloc', () {
    late MockUserRepository mockRepository;

    setUp(() {
      mockRepository = MockUserRepository();
    });

    blocTest<UserBloc, UserState>(
      'emits [loading, loaded] when LoadUsers succeeds',
      build: () {
        when(() => mockRepository.fetchUsers())
            .thenAnswer((_) async => [User(id: '1', name: 'Test')]);
        return UserBloc(mockRepository);
      },
      act: (bloc) => bloc.add(const LoadUsers()),
      expect: () => [
        const UserState.loading(),
        isA<_Loaded>(),
      ],
    );
  });
}
```

## Provider (Legacy)

### Setup

```yaml
# pubspec.yaml
dependencies:
  provider: ^6.1.0
```

### ChangeNotifier

```dart
import 'package:flutter/foundation.dart';

class CounterProvider extends ChangeNotifier {
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
}

// Async provider
class UserProvider extends ChangeNotifier {
  List<User> _users = [];
  bool _isLoading = false;
  String? _error;

  List<User> get users => _users;
  bool get isLoading => _isLoading;
  String? get error => _error;

  final UserRepository _repository;

  UserProvider(this._repository);

  Future<void> loadUsers() async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      _users = await _repository.fetchUsers();
    } catch (e) {
      _error = e.toString();
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<void> addUser(User user) async {
    await _repository.createUser(user);
    await loadUsers();
  }
}
```

### Usage in Widgets

```dart
// Provide at root
void main() {
  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => CounterProvider()),
        ChangeNotifierProvider(
          create: (context) => UserProvider(context.read<UserRepository>()),
        ),
      ],
      child: const MyApp(),
    ),
  );
}

// Consumer widget
class CounterScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Consumer<CounterProvider>(
      builder: (context, counter, child) {
        return Column(
          children: [
            Text('Count: ${counter.count}'),
            child!,  // Static parts
          ],
        );
      },
      child: const Text('This never rebuilds'),
    );
  }
}

// context.watch/read
class AnotherScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    // watch rebuilds when value changes
    final count = context.watch<CounterProvider>().count;

    return Column(
      children: [
        Text('Count: $count'),
        ElevatedButton(
          onPressed: () {
            // read doesn't rebuild
            context.read<CounterProvider>().increment();
          },
          child: const Text('Increment'),
        ),
      ],
    );
  }
}

// Selector (selective rebuilds)
class OptimizedWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Selector<UserProvider, int>(
      selector: (_, provider) => provider.users.length,
      builder: (context, userCount, child) {
        return Text('$userCount users');  // Only rebuilds when count changes
      },
    );
  }
}
```

## Comparison Summary

### When to Use Riverpod

- **New projects** - Modern, well-designed API
- **Type safety matters** - Compile-time provider checking
- **Need flexibility** - Provider overriding, family providers
- **Testing focus** - Easy to override dependencies
- **Code generation OK** - Uses build_runner

### When to Use Bloc

- **Large teams** - Enforced patterns, clear structure
- **Complex business logic** - Event-driven architecture
- **Need replay/undo** - Event history available
- **DevTools important** - Best debugging tools
- **Strict separation** - UI completely decoupled from logic

### When to Use Provider

- **Simple apps** - Minimal learning curve
- **Quick prototypes** - Fast to implement
- **Legacy projects** - Already in use
- **Minimal dependencies** - Just one package

### Migration Path

```
Provider → Riverpod: Recommended
Provider → Bloc: Possible but significant rewrite
Bloc → Riverpod: Some effort, different mental model
Riverpod → Bloc: Significant rewrite
```

### Performance Comparison

| Aspect | Riverpod | Bloc | Provider |
|--------|----------|------|----------|
| Initial Load | Fast | Fast | Fast |
| State Updates | Very Fast | Fast | Fast |
| Memory Usage | Low | Medium | Low |
| Bundle Size | Medium | Medium | Small |
| Rebuild Optimization | Excellent | Good | Good |
