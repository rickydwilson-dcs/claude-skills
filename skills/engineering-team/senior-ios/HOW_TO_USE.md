# How to Use Senior iOS Skill

Quick start guide for native iOS development with Swift 5.9+ and SwiftUI.

## Quick Start

### 1. New SwiftUI Project

Create a new SwiftUI app with modern architecture:

```swift
// 1. Set up MVVM structure
// Models/User.swift
struct User: Identifiable, Codable {
    let id: UUID
    var name: String
    var email: String
}

// ViewModels/UserViewModel.swift
@Observable
class UserViewModel {
    var users: [User] = []
    var isLoading = false

    func loadUsers() async {
        isLoading = true
        defer { isLoading = false }
        users = try? await userService.fetchUsers()
    }
}

// Views/UserListView.swift
struct UserListView: View {
    @State private var viewModel = UserViewModel()

    var body: some View {
        NavigationStack {
            List(viewModel.users) { user in
                Text(user.name)
            }
            .task { await viewModel.loadUsers() }
        }
    }
}
```

### 2. Validate for App Store

Use the senior-mobile tools:

```bash
# Validate iOS build
python3 ../../senior-mobile/scripts/app_store_validator.py --store apple --strict

# Check project configuration
python3 ../../senior-mobile/scripts/platform_detector.py --check ios --depth full
```

### 3. Profile Performance

1. Product > Profile (Cmd+I)
2. Choose Time Profiler or Allocations
3. Run through critical flows
4. Analyze bottlenecks
5. Optimize and re-profile

## Common Patterns

### Async Data Loading

```swift
@Observable
class DataViewModel {
    var data: [Item] = []
    var error: Error?

    func load() async {
        do {
            data = try await service.fetchItems()
        } catch {
            self.error = error
        }
    }
}
```

### Navigation

```swift
struct ContentView: View {
    var body: some View {
        NavigationStack {
            List(items) { item in
                NavigationLink(value: item) {
                    ItemRow(item: item)
                }
            }
            .navigationDestination(for: Item.self) { item in
                ItemDetailView(item: item)
            }
        }
    }
}
```

### UIKit Bridge

```swift
struct LegacyViewWrapper: UIViewControllerRepresentable {
    func makeUIViewController(context: Context) -> LegacyViewController {
        LegacyViewController()
    }

    func updateUIViewController(_ uiViewController: LegacyViewController, context: Context) {
        // Update if needed
    }
}
```

## Key References

| Reference | Content |
|-----------|---------|
| `swift-patterns.md` | Modern Swift patterns, async/await |
| `swiftui-guide.md` | SwiftUI state, navigation |
| `xcode-workflows.md` | Signing, Instruments, TestFlight |

## App Store Checklist

- [ ] App icon (1024x1024)
- [ ] Launch screen
- [ ] Privacy descriptions in Info.plist
- [ ] Privacy manifest (PrivacyInfo.xcprivacy)
- [ ] Version/build numbers updated
- [ ] Screenshots for all device sizes

## Related Skills

- **senior-mobile** - Cross-platform tools and scaffolding
- **senior-flutter** - Flutter/Dart development

## Need More?

See `SKILL.md` for complete workflows and detailed documentation.
