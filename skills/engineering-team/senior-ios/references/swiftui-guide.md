# SwiftUI Development Guide

Comprehensive guide for building modern iOS applications with SwiftUI.

## State Management

### @State

For simple, view-local state:

```swift
struct CounterView: View {
    @State private var count = 0

    var body: some View {
        VStack {
            Text("Count: \(count)")
            Button("Increment") {
                count += 1
            }
        }
    }
}
```

### @Binding

For passing state down to child views:

```swift
struct ParentView: View {
    @State private var isOn = false

    var body: some View {
        ToggleView(isOn: $isOn)
    }
}

struct ToggleView: View {
    @Binding var isOn: Bool

    var body: some View {
        Toggle("Enable", isOn: $isOn)
    }
}
```

### @Observable (iOS 17+)

Modern observation for view models:

```swift
@Observable
class UserViewModel {
    var name: String = ""
    var email: String = ""
    var isLoading: Bool = false
    var error: Error?

    func load() async {
        isLoading = true
        defer { isLoading = false }

        do {
            let user = try await userService.fetchCurrentUser()
            name = user.name
            email = user.email
        } catch {
            self.error = error
        }
    }
}

struct UserView: View {
    @State private var viewModel = UserViewModel()

    var body: some View {
        Form {
            TextField("Name", text: $viewModel.name)
            TextField("Email", text: $viewModel.email)
        }
        .task {
            await viewModel.load()
        }
        .overlay {
            if viewModel.isLoading {
                ProgressView()
            }
        }
    }
}
```

### @Environment

For app-wide values:

```swift
// Define environment key
struct ThemeKey: EnvironmentKey {
    static let defaultValue: Theme = .light
}

extension EnvironmentValues {
    var theme: Theme {
        get { self[ThemeKey.self] }
        set { self[ThemeKey.self] = newValue }
    }
}

// Set in parent
ContentView()
    .environment(\.theme, .dark)

// Access in child
struct ThemedButton: View {
    @Environment(\.theme) var theme

    var body: some View {
        Button("Tap me") { }
            .foregroundColor(theme.primaryColor)
    }
}
```

### @EnvironmentObject

For shared observable objects:

```swift
class AppState: ObservableObject {
    @Published var user: User?
    @Published var isAuthenticated = false
}

// Inject at root
@main
struct MyApp: App {
    @StateObject private var appState = AppState()

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environmentObject(appState)
        }
    }
}

// Access anywhere
struct ProfileView: View {
    @EnvironmentObject var appState: AppState

    var body: some View {
        if let user = appState.user {
            Text("Hello, \(user.name)")
        }
    }
}
```

## Navigation

### NavigationStack (iOS 16+)

```swift
struct ContentView: View {
    @State private var path = NavigationPath()

    var body: some View {
        NavigationStack(path: $path) {
            List(items) { item in
                NavigationLink(value: item) {
                    ItemRow(item: item)
                }
            }
            .navigationDestination(for: Item.self) { item in
                ItemDetailView(item: item)
            }
            .navigationDestination(for: User.self) { user in
                UserProfileView(user: user)
            }
            .navigationTitle("Items")
        }
    }

    // Programmatic navigation
    func navigateToItem(_ item: Item) {
        path.append(item)
    }

    func popToRoot() {
        path.removeLast(path.count)
    }
}
```

### TabView

```swift
struct MainTabView: View {
    @State private var selectedTab = 0

    var body: some View {
        TabView(selection: $selectedTab) {
            HomeView()
                .tabItem {
                    Label("Home", systemImage: "house")
                }
                .tag(0)

            SearchView()
                .tabItem {
                    Label("Search", systemImage: "magnifyingglass")
                }
                .tag(1)

            ProfileView()
                .tabItem {
                    Label("Profile", systemImage: "person")
                }
                .tag(2)
        }
    }
}
```

### Sheets and Modals

```swift
struct ContentView: View {
    @State private var showSettings = false
    @State private var selectedItem: Item?

    var body: some View {
        List(items) { item in
            Button(item.name) {
                selectedItem = item
            }
        }
        .toolbar {
            Button("Settings") {
                showSettings = true
            }
        }
        // Boolean-based sheet
        .sheet(isPresented: $showSettings) {
            SettingsView()
        }
        // Item-based sheet
        .sheet(item: $selectedItem) { item in
            ItemDetailView(item: item)
        }
        // Full screen cover
        .fullScreenCover(isPresented: $showOnboarding) {
            OnboardingView()
        }
    }
}
```

## Layouts

### VStack, HStack, ZStack

```swift
struct ProfileCard: View {
    var body: some View {
        ZStack(alignment: .bottomTrailing) {
            VStack(alignment: .leading, spacing: 8) {
                HStack {
                    Image(systemName: "person.circle.fill")
                        .font(.largeTitle)

                    VStack(alignment: .leading) {
                        Text("John Doe")
                            .font(.headline)
                        Text("iOS Developer")
                            .font(.subheadline)
                            .foregroundStyle(.secondary)
                    }
                }

                Text("Building amazing apps with SwiftUI")
                    .font(.body)
            }
            .padding()
            .background(.ultraThinMaterial)
            .cornerRadius(12)

            // Badge overlay
            Circle()
                .fill(.green)
                .frame(width: 20, height: 20)
                .offset(x: -10, y: -10)
        }
    }
}
```

### LazyVStack and LazyHStack

```swift
struct LongListView: View {
    var body: some View {
        ScrollView {
            LazyVStack(spacing: 16, pinnedViews: [.sectionHeaders]) {
                Section {
                    ForEach(items) { item in
                        ItemRow(item: item)
                    }
                } header: {
                    Text("Items")
                        .font(.headline)
                        .frame(maxWidth: .infinity, alignment: .leading)
                        .padding()
                        .background(.bar)
                }
            }
        }
    }
}
```

### Grid Layouts

```swift
struct PhotoGrid: View {
    let columns = [
        GridItem(.flexible()),
        GridItem(.flexible()),
        GridItem(.flexible())
    ]

    var body: some View {
        ScrollView {
            LazyVGrid(columns: columns, spacing: 2) {
                ForEach(photos) { photo in
                    AsyncImage(url: photo.url) { image in
                        image
                            .resizable()
                            .aspectRatio(1, contentMode: .fill)
                    } placeholder: {
                        Color.gray
                    }
                    .clipped()
                }
            }
        }
    }
}
```

## Lists and Forms

### List

```swift
struct SettingsView: View {
    @State private var notifications = true
    @State private var soundEnabled = true

    var body: some View {
        List {
            Section("General") {
                NavigationLink("Account") {
                    AccountView()
                }
                NavigationLink("Privacy") {
                    PrivacyView()
                }
            }

            Section("Preferences") {
                Toggle("Notifications", isOn: $notifications)
                Toggle("Sound", isOn: $soundEnabled)
            }

            Section {
                Button("Sign Out", role: .destructive) {
                    signOut()
                }
            }
        }
        .navigationTitle("Settings")
    }
}
```

### Swipe Actions

```swift
struct TaskListView: View {
    @State private var tasks: [Task] = []

    var body: some View {
        List {
            ForEach(tasks) { task in
                TaskRow(task: task)
                    .swipeActions(edge: .trailing) {
                        Button(role: .destructive) {
                            delete(task)
                        } label: {
                            Label("Delete", systemImage: "trash")
                        }

                        Button {
                            archive(task)
                        } label: {
                            Label("Archive", systemImage: "archivebox")
                        }
                        .tint(.orange)
                    }
                    .swipeActions(edge: .leading) {
                        Button {
                            toggleComplete(task)
                        } label: {
                            Label("Complete", systemImage: "checkmark")
                        }
                        .tint(.green)
                    }
            }
        }
    }
}
```

## Async Operations

### Task Modifier

```swift
struct UserProfileView: View {
    @State private var user: User?
    @State private var isLoading = true

    var body: some View {
        Group {
            if isLoading {
                ProgressView()
            } else if let user {
                ProfileContent(user: user)
            } else {
                Text("User not found")
            }
        }
        .task {
            isLoading = true
            user = try? await userService.fetchUser()
            isLoading = false
        }
    }
}
```

### Refreshable

```swift
struct FeedView: View {
    @State private var posts: [Post] = []

    var body: some View {
        List(posts) { post in
            PostRow(post: post)
        }
        .refreshable {
            posts = try? await feedService.fetchPosts() ?? []
        }
    }
}
```

### AsyncImage

```swift
struct UserAvatar: View {
    let url: URL?

    var body: some View {
        AsyncImage(url: url) { phase in
            switch phase {
            case .empty:
                ProgressView()
            case .success(let image):
                image
                    .resizable()
                    .aspectRatio(contentMode: .fill)
            case .failure:
                Image(systemName: "person.circle.fill")
                    .foregroundStyle(.secondary)
            @unknown default:
                EmptyView()
            }
        }
        .frame(width: 50, height: 50)
        .clipShape(Circle())
    }
}
```

## Animations

### Implicit Animations

```swift
struct AnimatedButton: View {
    @State private var isPressed = false

    var body: some View {
        Button("Tap Me") {
            isPressed.toggle()
        }
        .scaleEffect(isPressed ? 0.9 : 1.0)
        .animation(.spring(duration: 0.3), value: isPressed)
    }
}
```

### Explicit Animations

```swift
struct LoadingView: View {
    @State private var rotation = 0.0

    var body: some View {
        Image(systemName: "arrow.clockwise")
            .rotationEffect(.degrees(rotation))
            .onAppear {
                withAnimation(.linear(duration: 1).repeatForever(autoreverses: false)) {
                    rotation = 360
                }
            }
    }
}
```

### Transitions

```swift
struct ToastView: View {
    @State private var showToast = false

    var body: some View {
        ZStack {
            Button("Show Toast") {
                withAnimation(.easeInOut) {
                    showToast = true
                }

                DispatchQueue.main.asyncAfter(deadline: .now() + 2) {
                    withAnimation(.easeInOut) {
                        showToast = false
                    }
                }
            }

            if showToast {
                Text("Operation completed!")
                    .padding()
                    .background(.green)
                    .foregroundColor(.white)
                    .cornerRadius(8)
                    .transition(.move(edge: .top).combined(with: .opacity))
            }
        }
    }
}
```

## Gestures

### Tap and Long Press

```swift
struct GestureDemo: View {
    @State private var taps = 0

    var body: some View {
        Circle()
            .fill(.blue)
            .frame(width: 100, height: 100)
            .onTapGesture(count: 2) {
                print("Double tapped!")
            }
            .onLongPressGesture(minimumDuration: 1) {
                print("Long pressed!")
            }
    }
}
```

### Drag Gesture

```swift
struct DraggableCard: View {
    @State private var offset = CGSize.zero
    @State private var isDragging = false

    var body: some View {
        RoundedRectangle(cornerRadius: 12)
            .fill(.blue)
            .frame(width: 200, height: 150)
            .offset(offset)
            .scaleEffect(isDragging ? 1.1 : 1.0)
            .gesture(
                DragGesture()
                    .onChanged { value in
                        offset = value.translation
                        isDragging = true
                    }
                    .onEnded { _ in
                        withAnimation(.spring()) {
                            offset = .zero
                            isDragging = false
                        }
                    }
            )
    }
}
```

## Custom Modifiers

```swift
struct CardModifier: ViewModifier {
    func body(content: Content) -> some View {
        content
            .padding()
            .background(.white)
            .cornerRadius(12)
            .shadow(color: .black.opacity(0.1), radius: 8, x: 0, y: 4)
    }
}

extension View {
    func cardStyle() -> some View {
        modifier(CardModifier())
    }
}

// Usage
Text("Hello")
    .cardStyle()
```

## Performance Tips

### Use Identifiable for Lists

```swift
// Good - stable identity
struct Item: Identifiable {
    let id: UUID
    var name: String
}

ForEach(items) { item in
    ItemRow(item: item)
}

// Avoid - index-based identity causes issues
ForEach(items.indices, id: \.self) { index in
    ItemRow(item: items[index])  // Bad for animations
}
```

### Extract Subviews

```swift
// Before - large body
var body: some View {
    VStack {
        // 100 lines of header code
        // 100 lines of content code
        // 100 lines of footer code
    }
}

// After - extracted components
var body: some View {
    VStack {
        HeaderView()
        ContentView()
        FooterView()
    }
}
```

### Use @ViewBuilder

```swift
@ViewBuilder
func statusView(for status: Status) -> some View {
    switch status {
    case .loading:
        ProgressView()
    case .success(let data):
        ContentView(data: data)
    case .error(let error):
        ErrorView(error: error)
    }
}
```
