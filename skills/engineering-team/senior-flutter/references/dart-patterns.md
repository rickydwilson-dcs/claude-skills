# Dart Patterns Reference

Modern Dart patterns for Flutter development with Dart 3.x.

## Null Safety

### Non-Nullable by Default

```dart
// Non-nullable (must have value)
String name = 'John';
int count = 0;

// Nullable (can be null)
String? optionalName;
int? optionalCount;

// Late initialization
late String lazyName;
late final String immutableLazy;

void initialize() {
  lazyName = 'Initialized later';
  immutableLazy = 'Set once';
}
```

### Null-Aware Operators

```dart
// Null-aware access
String? name;
int? length = name?.length;  // null if name is null

// Null-coalescing
String displayName = name ?? 'Unknown';

// Null-coalescing assignment
String? value;
value ??= 'Default';  // Only assigns if null

// Null assertion (use sparingly)
String definitelyNotNull = name!;  // Throws if null

// Cascade with null check
object
  ?..method1()
  ..method2();
```

### Flow Analysis

```dart
void process(String? input) {
  if (input == null) {
    return;
  }
  // input is promoted to String (non-nullable) here
  print(input.length);
}

// Pattern matching with null
String describe(Object? value) {
  return switch (value) {
    null => 'null',
    String s => 'String: $s',
    int n => 'Int: $n',
    _ => 'Unknown',
  };
}
```

## Pattern Matching (Dart 3.0+)

### Switch Expressions

```dart
// Expression syntax
String describe(Shape shape) => switch (shape) {
  Circle(radius: var r) => 'Circle with radius $r',
  Rectangle(width: var w, height: var h) => 'Rectangle ${w}x$h',
  Square(side: var s) => 'Square with side $s',
};

// With guards
String categorize(int value) => switch (value) {
  < 0 => 'negative',
  0 => 'zero',
  > 0 && < 100 => 'small positive',
  >= 100 => 'large positive',
  _ => 'impossible',
};
```

### Destructuring

```dart
// Record destructuring
(String, int) getNameAndAge() => ('John', 30);

void main() {
  var (name, age) = getNameAndAge();
  print('$name is $age');
}

// Object destructuring
class Point {
  final int x, y;
  Point(this.x, this.y);
}

void processPoint(Point p) {
  var Point(:x, :y) = p;
  print('x: $x, y: $y');
}

// List patterns
var [first, second, ...rest] = [1, 2, 3, 4, 5];
// first = 1, second = 2, rest = [3, 4, 5]

// Map patterns
var {'name': name, 'age': age} = {'name': 'John', 'age': 30};
```

### If-Case

```dart
// Pattern matching in if
void process(Object value) {
  if (value case String s when s.isNotEmpty) {
    print('Non-empty string: $s');
  }

  if (value case [int first, int second, ...]) {
    print('List starting with $first, $second');
  }
}

// Guard clauses
void validate(User? user) {
  if (user case User(:var email) when email.contains('@')) {
    print('Valid email: $email');
  }
}
```

## Records (Dart 3.0+)

### Basic Records

```dart
// Positional record
(String, int) person = ('John', 30);
print(person.$1);  // John
print(person.$2);  // 30

// Named record
({String name, int age}) namedPerson = (name: 'John', age: 30);
print(namedPerson.name);  // John

// Mixed
(String, {int age}) mixed = ('John', age: 30);

// Type aliases
typedef Person = ({String name, int age, String email});

Person createPerson() => (
  name: 'John',
  age: 30,
  email: 'john@example.com',
);
```

### Multiple Return Values

```dart
// Return multiple values without creating a class
(int, int) divide(int dividend, int divisor) {
  return (dividend ~/ divisor, dividend % divisor);
}

void main() {
  var (quotient, remainder) = divide(17, 5);
  print('$quotient with remainder $remainder');  // 3 with remainder 2
}

// Named fields for clarity
({double min, double max, double average}) stats(List<double> values) {
  final sorted = [...values]..sort();
  return (
    min: sorted.first,
    max: sorted.last,
    average: values.reduce((a, b) => a + b) / values.length,
  );
}
```

## Async Patterns

### Futures

```dart
// Basic async/await
Future<User> fetchUser(String id) async {
  final response = await http.get('/users/$id');
  return User.fromJson(response.body);
}

// Error handling
Future<User> fetchUserSafe(String id) async {
  try {
    return await fetchUser(id);
  } on SocketException {
    throw NetworkError('No internet connection');
  } on FormatException {
    throw DataError('Invalid response format');
  }
}

// Parallel execution
Future<Dashboard> loadDashboard() async {
  final results = await Future.wait([
    fetchUser(),
    fetchNotifications(),
    fetchStats(),
  ]);

  return Dashboard(
    user: results[0] as User,
    notifications: results[1] as List<Notification>,
    stats: results[2] as Stats,
  );
}
```

### Streams

```dart
// Creating streams
Stream<int> countStream(int max) async* {
  for (int i = 0; i < max; i++) {
    await Future.delayed(Duration(seconds: 1));
    yield i;
  }
}

// Stream transformations
Stream<String> processNumbers(Stream<int> numbers) {
  return numbers
      .where((n) => n.isEven)
      .map((n) => 'Number: $n')
      .handleError((e) => print('Error: $e'));
}

// StreamController for custom streams
class MessageService {
  final _controller = StreamController<Message>.broadcast();

  Stream<Message> get messages => _controller.stream;

  void addMessage(Message message) {
    _controller.add(message);
  }

  void dispose() {
    _controller.close();
  }
}
```

### Isolates

```dart
// Simple isolate for heavy computation
Future<int> heavyComputation(int input) async {
  return await Isolate.run(() {
    // Heavy work here runs on separate isolate
    int result = 0;
    for (int i = 0; i < input; i++) {
      result += i * i;
    }
    return result;
  });
}

// Compute function (simpler API)
Future<List<ProcessedItem>> processItems(List<RawItem> items) async {
  return await compute(_processItems, items);
}

List<ProcessedItem> _processItems(List<RawItem> items) {
  return items.map((item) => ProcessedItem.from(item)).toList();
}
```

## Classes and Mixins

### Class Modifiers (Dart 3.0+)

```dart
// Final class - cannot be extended
final class ImmutableConfig {
  final String key;
  final String value;
  const ImmutableConfig(this.key, this.value);
}

// Sealed class - known subtypes only
sealed class Result<T> {
  const Result();
}

class Success<T> extends Result<T> {
  final T value;
  const Success(this.value);
}

class Failure<T> extends Result<T> {
  final Exception error;
  const Failure(this.error);
}

// Interface class - implement only
interface class Printable {
  void print();
}

// Base class - extend only
base class BaseWidget {
  void render() {}
}

// Mixin class
mixin class Logger {
  void log(String message) {
    print('[LOG] $message');
  }
}
```

### Mixins

```dart
// Define mixin
mixin Flyable {
  void fly() {
    print('Flying!');
  }
}

mixin Swimmable {
  void swim() {
    print('Swimming!');
  }
}

// Use mixins
class Duck extends Bird with Flyable, Swimmable {}

// Mixin with constraints
mixin CanJump on Animal {
  void jump() {
    print('${name} is jumping!');  // Can access Animal.name
  }
}
```

### Extension Methods

```dart
// Extend existing types
extension StringExtensions on String {
  String get capitalized =>
      isEmpty ? this : '${this[0].toUpperCase()}${substring(1)}';

  bool get isValidEmail =>
      RegExp(r'^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$').hasMatch(this);

  String truncate(int maxLength) =>
      length <= maxLength ? this : '${substring(0, maxLength)}...';
}

// Extension with generics
extension IterableExtensions<T> on Iterable<T> {
  T? firstWhereOrNull(bool Function(T) test) {
    for (final element in this) {
      if (test(element)) return element;
    }
    return null;
  }

  Map<K, List<T>> groupBy<K>(K Function(T) keyFunction) {
    final map = <K, List<T>>{};
    for (final element in this) {
      final key = keyFunction(element);
      map.putIfAbsent(key, () => []).add(element);
    }
    return map;
  }
}

// Usage
'hello'.capitalized;  // 'Hello'
'test@email.com'.isValidEmail;  // true
users.firstWhereOrNull((u) => u.isAdmin);
```

## Generics

### Generic Classes

```dart
// Generic repository
abstract class Repository<T, ID> {
  Future<T?> findById(ID id);
  Future<List<T>> findAll();
  Future<void> save(T entity);
  Future<void> delete(ID id);
}

// Implementation
class UserRepository implements Repository<User, String> {
  @override
  Future<User?> findById(String id) async {
    // Implementation
  }

  // ... other methods
}
```

### Generic Functions

```dart
// Generic function with constraints
T clamp<T extends num>(T value, T min, T max) {
  if (value < min) return min;
  if (value > max) return max;
  return value;
}

// Multiple type parameters
Map<K, V> zipToMap<K, V>(List<K> keys, List<V> values) {
  assert(keys.length == values.length);
  return Map.fromIterables(keys, values);
}

// Covariant type parameter
class Container<out T> {
  final T value;
  Container(this.value);
}
```

## Error Handling

### Custom Exceptions

```dart
// Define exception hierarchy
sealed class AppException implements Exception {
  final String message;
  final StackTrace? stackTrace;

  const AppException(this.message, [this.stackTrace]);

  @override
  String toString() => message;
}

class NetworkException extends AppException {
  final int? statusCode;
  const NetworkException(super.message, {this.statusCode, super.stackTrace});
}

class ValidationException extends AppException {
  final Map<String, String> errors;
  const ValidationException(super.message, this.errors);
}
```

### Result Type Pattern

```dart
// Functional error handling
sealed class Result<T, E extends Exception> {
  const Result();

  T? get valueOrNull;
  E? get errorOrNull;

  R when<R>({
    required R Function(T value) success,
    required R Function(E error) failure,
  });
}

class Success<T, E extends Exception> extends Result<T, E> {
  final T value;
  const Success(this.value);

  @override
  T? get valueOrNull => value;

  @override
  E? get errorOrNull => null;

  @override
  R when<R>({
    required R Function(T value) success,
    required R Function(E error) failure,
  }) => success(value);
}

class Failure<T, E extends Exception> extends Result<T, E> {
  final E error;
  const Failure(this.error);

  @override
  T? get valueOrNull => null;

  @override
  E? get errorOrNull => error;

  @override
  R when<R>({
    required R Function(T value) success,
    required R Function(E error) failure,
  }) => failure(error);
}

// Usage
Future<Result<User, NetworkException>> fetchUser(String id) async {
  try {
    final user = await api.getUser(id);
    return Success(user);
  } on NetworkException catch (e) {
    return Failure(e);
  }
}

final result = await fetchUser('123');
result.when(
  success: (user) => print('User: ${user.name}'),
  failure: (error) => print('Error: ${error.message}'),
);
```

## Code Generation

### Freezed

```dart
// Define immutable data class
import 'package:freezed_annotation/freezed_annotation.dart';

part 'user.freezed.dart';
part 'user.g.dart';

@freezed
class User with _$User {
  const factory User({
    required String id,
    required String name,
    String? email,
    @Default(false) bool isAdmin,
  }) = _User;

  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);
}

// Union types with Freezed
@freezed
sealed class AuthState with _$AuthState {
  const factory AuthState.initial() = _Initial;
  const factory AuthState.loading() = _Loading;
  const factory AuthState.authenticated(User user) = _Authenticated;
  const factory AuthState.unauthenticated() = _Unauthenticated;
  const factory AuthState.error(String message) = _Error;
}

// Usage
authState.when(
  initial: () => SplashScreen(),
  loading: () => LoadingScreen(),
  authenticated: (user) => HomeScreen(user: user),
  unauthenticated: () => LoginScreen(),
  error: (message) => ErrorScreen(message: message),
);
```

### JSON Serialization

```dart
import 'package:json_annotation/json_annotation.dart';

part 'user.g.dart';

@JsonSerializable()
class User {
  final String id;
  final String name;

  @JsonKey(name: 'email_address')
  final String? email;

  @JsonKey(includeIfNull: false)
  final DateTime? lastLogin;

  User({
    required this.id,
    required this.name,
    this.email,
    this.lastLogin,
  });

  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);
  Map<String, dynamic> toJson() => _$UserToJson(this);
}
```

## Best Practices

### Naming Conventions

```dart
// Classes, enums, typedefs: UpperCamelCase
class HttpClient {}
enum Status { active, inactive }
typedef Callback = void Function(String);

// Variables, functions, parameters: lowerCamelCase
var itemCount = 0;
void fetchData() {}
void process(String inputValue) {}

// Constants: lowerCamelCase (not SCREAMING_CAPS)
const defaultTimeout = Duration(seconds: 30);

// Private: underscore prefix
class MyClass {
  String _privateField = '';
  void _privateMethod() {}
}

// Libraries, packages, files: lowercase_with_underscores
import 'package:my_package/src/my_file.dart';
```

### Effective Dart

```dart
// DO use adjacent strings for concatenation
var message = 'This is a very long message '
    'that spans multiple lines '
    'for better readability.';

// DO use collection literals
var points = <Point>[];  // Not: List<Point>()
var addresses = <String, Address>{};  // Not: Map<String, Address>()

// DO use cascade notation
var button = Button()
  ..text = 'OK'
  ..color = Colors.blue
  ..onPressed = handlePress;

// DO use ?? to convert null to bool
bool isEnabled = config.enabled ?? false;

// DON'T use .length to check if collection is empty
if (items.isEmpty) {}  // Good
if (items.length == 0) {}  // Bad
```
