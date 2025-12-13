# Swift Patterns Reference

Modern Swift patterns for iOS development with Swift 5.9+ and Swift 6.

## Modern Concurrency

### Async/Await Basics

```swift
// Basic async function
func fetchUser(id: String) async throws -> User {
    let url = URL(string: "https://api.example.com/users/\(id)")!
    let (data, response) = try await URLSession.shared.data(from: url)

    guard let httpResponse = response as? HTTPURLResponse,
          httpResponse.statusCode == 200 else {
        throw NetworkError.invalidResponse
    }

    return try JSONDecoder().decode(User.self, from: data)
}

// Calling async code
Task {
    do {
        let user = try await fetchUser(id: "123")
        print("Fetched: \(user.name)")
    } catch {
        print("Error: \(error)")
    }
}
```

### Structured Concurrency

```swift
// Parallel execution with async let
func loadDashboard() async throws -> Dashboard {
    async let user = fetchUser()
    async let notifications = fetchNotifications()
    async let stats = fetchStats()

    return try await Dashboard(
        user: user,
        notifications: notifications,
        stats: stats
    )
}

// Task groups for dynamic parallelism
func fetchAllUsers(ids: [String]) async throws -> [User] {
    try await withThrowingTaskGroup(of: User.self) { group in
        for id in ids {
            group.addTask {
                try await fetchUser(id: id)
            }
        }

        var users: [User] = []
        for try await user in group {
            users.append(user)
        }
        return users
    }
}
```

### Actors

```swift
// Basic actor for thread-safe state
actor ImageCache {
    private var cache: [URL: UIImage] = [:]

    func image(for url: URL) -> UIImage? {
        cache[url]
    }

    func setImage(_ image: UIImage, for url: URL) {
        cache[url] = image
    }

    func clear() {
        cache.removeAll()
    }
}

// Using actors
let cache = ImageCache()
await cache.setImage(image, for: url)
if let cachedImage = await cache.image(for: url) {
    // Use cached image
}

// Global actor for main thread
@MainActor
class ViewModel: ObservableObject {
    @Published var data: [Item] = []

    func loadData() async {
        // Already on main thread due to @MainActor
        let items = try? await service.fetchItems()
        data = items ?? []
    }
}
```

### Task Management

```swift
// Cancellable tasks
class SearchViewModel {
    private var searchTask: Task<Void, Never>?

    func search(_ query: String) {
        // Cancel previous search
        searchTask?.cancel()

        searchTask = Task {
            // Debounce
            try? await Task.sleep(for: .milliseconds(300))

            // Check cancellation
            guard !Task.isCancelled else { return }

            let results = await performSearch(query)

            await MainActor.run {
                self.results = results
            }
        }
    }
}

// Task with timeout
func fetchWithTimeout() async throws -> Data {
    try await withThrowingTaskGroup(of: Data.self) { group in
        group.addTask {
            try await fetchData()
        }
        group.addTask {
            try await Task.sleep(for: .seconds(10))
            throw TimeoutError()
        }

        let result = try await group.next()!
        group.cancelAll()
        return result
    }
}
```

## Protocol-Oriented Design

### Protocol Extensions

```swift
// Protocol with default implementation
protocol Loadable {
    associatedtype Content
    var loadingState: LoadingState<Content> { get set }
    func load() async throws -> Content
}

extension Loadable {
    mutating func performLoad() async {
        loadingState = .loading
        do {
            let content = try await load()
            loadingState = .loaded(content)
        } catch {
            loadingState = .error(error)
        }
    }
}

// Usage
struct UserLoader: Loadable {
    var loadingState: LoadingState<User> = .idle

    func load() async throws -> User {
        try await userService.fetchCurrentUser()
    }
}
```

### Protocol Composition

```swift
// Composable protocols
protocol Identifiable {
    var id: String { get }
}

protocol Timestamped {
    var createdAt: Date { get }
    var updatedAt: Date { get }
}

protocol Archivable {
    var isArchived: Bool { get set }
    mutating func archive()
}

// Composed type
typealias Entity = Identifiable & Timestamped & Codable

struct Document: Entity, Archivable {
    let id: String
    let createdAt: Date
    var updatedAt: Date
    var isArchived: Bool = false
    var content: String

    mutating func archive() {
        isArchived = true
        updatedAt = Date()
    }
}
```

## Result Types and Error Handling

### Typed Throws (Swift 6)

```swift
// Typed error handling
enum NetworkError: Error {
    case invalidURL
    case noData
    case decodingFailed(Error)
    case serverError(Int)
}

func fetchUser(id: String) async throws(NetworkError) -> User {
    guard let url = URL(string: "https://api.example.com/users/\(id)") else {
        throw .invalidURL
    }

    let (data, response) = try await URLSession.shared.data(from: url)

    guard let httpResponse = response as? HTTPURLResponse else {
        throw .noData
    }

    guard httpResponse.statusCode == 200 else {
        throw .serverError(httpResponse.statusCode)
    }

    do {
        return try JSONDecoder().decode(User.self, from: data)
    } catch {
        throw .decodingFailed(error)
    }
}
```

### Result Type Pattern

```swift
// Result-based API
enum Result<Success, Failure: Error> {
    case success(Success)
    case failure(Failure)
}

func fetchUser(id: String) async -> Result<User, NetworkError> {
    do {
        let user = try await performFetch(id)
        return .success(user)
    } catch let error as NetworkError {
        return .failure(error)
    } catch {
        return .failure(.unknown(error))
    }
}

// Usage with switch
let result = await fetchUser(id: "123")
switch result {
case .success(let user):
    print("User: \(user.name)")
case .failure(let error):
    print("Error: \(error)")
}

// Usage with map/flatMap
let userName = result
    .map { $0.name }
    .mapError { _ in "Unknown user" }
```

## Property Wrappers

### Custom Property Wrappers

```swift
// User defaults wrapper
@propertyWrapper
struct UserDefault<T> {
    let key: String
    let defaultValue: T

    var wrappedValue: T {
        get { UserDefaults.standard.object(forKey: key) as? T ?? defaultValue }
        set { UserDefaults.standard.set(newValue, forKey: key) }
    }
}

// Usage
struct Settings {
    @UserDefault(key: "isDarkMode", defaultValue: false)
    var isDarkMode: Bool

    @UserDefault(key: "fontSize", defaultValue: 14)
    var fontSize: Int
}

// Clamped value wrapper
@propertyWrapper
struct Clamped<T: Comparable> {
    var value: T
    let range: ClosedRange<T>

    init(wrappedValue: T, _ range: ClosedRange<T>) {
        self.range = range
        self.value = min(max(wrappedValue, range.lowerBound), range.upperBound)
    }

    var wrappedValue: T {
        get { value }
        set { value = min(max(newValue, range.lowerBound), range.upperBound) }
    }
}

// Usage
struct Volume {
    @Clamped(0...100) var level: Int = 50
}
```

## Generics

### Generic Constraints

```swift
// Multiple constraints
func process<T: Codable & Hashable>(_ item: T) -> Data? {
    try? JSONEncoder().encode(item)
}

// Where clause
func findFirst<C: Collection>(in collection: C, where predicate: (C.Element) -> Bool) -> C.Element?
where C.Element: Equatable {
    collection.first(where: predicate)
}

// Associated type constraints
protocol Repository {
    associatedtype Entity: Identifiable & Codable

    func fetch(id: Entity.ID) async throws -> Entity
    func save(_ entity: Entity) async throws
}
```

### Generic Type Erasure

```swift
// Type-erased wrapper
struct AnyRepository<T: Identifiable & Codable>: Repository {
    typealias Entity = T

    private let _fetch: (Entity.ID) async throws -> Entity
    private let _save: (Entity) async throws -> Void

    init<R: Repository>(_ repository: R) where R.Entity == T {
        _fetch = repository.fetch
        _save = repository.save
    }

    func fetch(id: Entity.ID) async throws -> Entity {
        try await _fetch(id)
    }

    func save(_ entity: Entity) async throws {
        try await _save(entity)
    }
}
```

## Macros (Swift 5.9+)

### Observable Macro

```swift
// Modern observation
@Observable
class UserViewModel {
    var name: String = ""
    var email: String = ""
    var isLoading: Bool = false

    // Private properties are not observed
    private var cache: [String: Any] = [:]
}

// Usage in SwiftUI
struct UserView: View {
    @State private var viewModel = UserViewModel()

    var body: some View {
        VStack {
            Text(viewModel.name)  // Automatically updates
            if viewModel.isLoading {
                ProgressView()
            }
        }
    }
}
```

### Custom Macros

```swift
// Attached macro for logging
@attached(body)
macro Logged() = #externalMacro(module: "MyMacros", type: "LoggedMacro")

// Usage
@Logged
func performAction() {
    // Automatically logs entry/exit
}

// Freestanding macro
@freestanding(expression)
macro stringify<T>(_ value: T) -> (T, String) = #externalMacro(module: "MyMacros", type: "StringifyMacro")

// Usage
let (value, string) = #stringify(1 + 2)
// value = 3, string = "1 + 2"
```

## Memory Management

### Weak and Unowned References

```swift
// Weak references for optional relationships
class Parent {
    var child: Child?
}

class Child {
    weak var parent: Parent?  // Breaks retain cycle

    init(parent: Parent) {
        self.parent = parent
    }
}

// Unowned for guaranteed non-nil
class Customer {
    var card: CreditCard?
}

class CreditCard {
    unowned let customer: Customer  // Always has a customer

    init(customer: Customer) {
        self.customer = customer
    }
}

// Capture lists in closures
class ViewController {
    var data: [String] = []

    func loadData() {
        service.fetch { [weak self] result in
            guard let self else { return }
            self.data = result
        }
    }
}
```

## Best Practices

### Naming Conventions

```swift
// Types: UpperCamelCase
struct UserProfile { }
class NetworkManager { }
enum HTTPMethod { }

// Functions/Properties: lowerCamelCase
func fetchUser() { }
var isEnabled: Bool

// Clear, descriptive names
func fetchUser(withID id: String) -> User  // Good
func get(_ x: String) -> User  // Bad

// Boolean naming
var isEnabled: Bool      // Good
var enabled: Bool        // Less clear
var hasPermission: Bool  // Good
var permission: Bool     // Less clear
```

### Code Organization

```swift
// MARK comments for sections
class ViewController: UIViewController {

    // MARK: - Properties

    private let viewModel: ViewModel

    // MARK: - Lifecycle

    override func viewDidLoad() {
        super.viewDidLoad()
    }

    // MARK: - Private Methods

    private func setupUI() { }
}

// Extension for protocol conformance
extension ViewController: UITableViewDelegate {
    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        // ...
    }
}
```
