# Xcode Workflows Guide

Essential Xcode workflows for iOS development, from project setup to App Store submission.

## Project Configuration

### Creating a New Project

1. File > New > Project
2. Select iOS > App
3. Configure:
   - Product Name: Your app name
   - Team: Select your development team
   - Organization Identifier: com.yourcompany
   - Bundle Identifier: Auto-generated (com.yourcompany.appname)
   - Interface: SwiftUI
   - Language: Swift
   - Storage: SwiftData (or Core Data)

### Build Settings

Key settings to configure:

| Setting | Location | Recommended |
|---------|----------|-------------|
| Deployment Target | General > Minimum Deployments | iOS 15.0+ |
| Swift Version | Build Settings > Swift Language Version | Swift 5 |
| Optimization | Build Settings > Optimization Level | -O for Release |
| Bitcode | Build Settings > Enable Bitcode | No (deprecated) |

### Info.plist Configuration

Essential keys:

```xml
<!-- Privacy descriptions -->
<key>NSCameraUsageDescription</key>
<string>We need camera access to take photos</string>

<key>NSPhotoLibraryUsageDescription</key>
<string>We need access to your photo library</string>

<key>NSLocationWhenInUseUsageDescription</key>
<string>We need your location to show nearby places</string>

<!-- App Transport Security -->
<key>NSAppTransportSecurity</key>
<dict>
    <key>NSAllowsArbitraryLoads</key>
    <false/>
</dict>

<!-- Background modes -->
<key>UIBackgroundModes</key>
<array>
    <string>fetch</string>
    <string>remote-notification</string>
</array>
```

## Code Signing

### Automatic Signing

1. Select project in navigator
2. Select target > Signing & Capabilities
3. Check "Automatically manage signing"
4. Select Team

### Manual Signing

For CI/CD or advanced scenarios:

1. Create certificates in Apple Developer Portal
2. Create provisioning profiles
3. Download and install in Xcode
4. Select specific profiles in Build Settings

### Exporting Certificates for CI

```bash
# Export certificate from Keychain
security find-identity -v -p codesigning

# Create .p12 file (GUI: Keychain Access > Export)
# Base64 encode for CI secrets
base64 -i Certificates.p12 | pbcopy
```

## Capabilities

Adding capabilities:

1. Select target > Signing & Capabilities
2. Click "+ Capability"
3. Select capability (Push Notifications, Sign in with Apple, etc.)

Common capabilities:

| Capability | Use Case |
|------------|----------|
| Push Notifications | Remote notifications |
| Sign in with Apple | Apple authentication |
| Background Modes | Background tasks |
| Associated Domains | Universal links |
| App Groups | Share data between apps/extensions |
| HealthKit | Health data access |
| HomeKit | Smart home control |

## Debugging

### Breakpoints

```swift
// Conditional breakpoint (right-click breakpoint > Edit)
// Condition: user.id == "12345"

// Symbolic breakpoint
// Debug > Breakpoints > Create Symbolic Breakpoint
// Symbol: -[UIViewController viewDidLoad]

// Exception breakpoint (catch all exceptions)
// Debug > Breakpoints > Create Exception Breakpoint
```

### LLDB Commands

```bash
# Print variable
(lldb) po myVariable

# Print with format
(lldb) p/x myInt  # Hex
(lldb) p/t myInt  # Binary

# Expression evaluation
(lldb) expr myVariable = newValue

# View hierarchy
(lldb) po UIApplication.shared.keyWindow

# Memory read
(lldb) memory read --size 4 --format x --count 10 0x12345678
```

### View Debugging

1. Debug > View Debugging > Capture View Hierarchy
2. Or click "Debug View Hierarchy" button
3. Inspect 3D view of UI layers
4. Check constraints and frame issues

### Memory Graph

1. Debug > Debug Workflow > View Memory Graph
2. Identify retain cycles
3. Filter by class name
4. Check reference counts

## Instruments

### Time Profiler

Profile CPU usage:

1. Product > Profile (Cmd+I)
2. Select "Time Profiler"
3. Click Record
4. Perform actions in app
5. Stop and analyze

Focus on:
- Heavy functions (high "Weight")
- Call tree depth
- Main thread blocking

### Allocations

Track memory usage:

1. Product > Profile
2. Select "Allocations"
3. Record and perform actions
4. Look for:
   - Memory growth over time
   - Large allocations
   - Persistent memory

### Leaks

Find memory leaks:

1. Product > Profile
2. Select "Leaks"
3. Record and perform actions
4. Check for red leak indicators
5. Expand leak to see retain cycle

### Network

Profile network calls:

1. Product > Profile
2. Select "Network"
3. Record and perform actions
4. Analyze:
   - Request/response times
   - Payload sizes
   - Failed requests

## Testing

### Unit Tests

```swift
import XCTest
@testable import MyApp

final class UserServiceTests: XCTestCase {
    var sut: UserService!

    override func setUp() {
        super.setUp()
        sut = UserService()
    }

    override func tearDown() {
        sut = nil
        super.tearDown()
    }

    func testFetchUser_ValidID_ReturnsUser() async throws {
        let user = try await sut.fetchUser(id: "123")
        XCTAssertEqual(user.id, "123")
    }

    func testFetchUser_InvalidID_ThrowsError() async {
        do {
            _ = try await sut.fetchUser(id: "invalid")
            XCTFail("Expected error")
        } catch {
            XCTAssertTrue(error is UserError)
        }
    }
}
```

### UI Tests

```swift
import XCTest

final class LoginUITests: XCTestCase {
    let app = XCUIApplication()

    override func setUp() {
        super.setUp()
        continueAfterFailure = false
        app.launch()
    }

    func testLogin_ValidCredentials_NavigatesToHome() {
        let emailField = app.textFields["email"]
        let passwordField = app.secureTextFields["password"]
        let loginButton = app.buttons["login"]

        emailField.tap()
        emailField.typeText("test@example.com")

        passwordField.tap()
        passwordField.typeText("password123")

        loginButton.tap()

        XCTAssertTrue(app.staticTexts["Welcome"].waitForExistence(timeout: 5))
    }
}
```

### Running Tests

```bash
# Command line
xcodebuild test -project MyApp.xcodeproj -scheme MyApp -destination 'platform=iOS Simulator,name=iPhone 15'

# With code coverage
xcodebuild test -enableCodeCoverage YES -project MyApp.xcodeproj -scheme MyApp
```

## TestFlight

### Preparing a Build

1. Update version and build numbers
2. Archive: Product > Archive
3. Wait for archive to complete
4. Organizer window opens

### Uploading

1. In Organizer, select archive
2. Click "Distribute App"
3. Select "App Store Connect"
4. Follow wizard (signing, etc.)
5. Upload

### Managing TestFlight

In App Store Connect:

1. Select app > TestFlight tab
2. Add internal testers (up to 100)
3. Create external test groups (up to 10,000)
4. Manage builds and test notes

## App Store Submission

### Pre-Submission Checklist

- [ ] Update version number
- [ ] Update build number
- [ ] Test on multiple device sizes
- [ ] Test on oldest supported iOS version
- [ ] Create screenshots for all required sizes
- [ ] Write App Store description
- [ ] Prepare privacy policy URL
- [ ] Configure In-App Purchases (if any)
- [ ] Test with production environment
- [ ] Archive with Release configuration

### Required Screenshots

| Device | Size | Required |
|--------|------|----------|
| iPhone 6.7" | 1290 x 2796 | Yes |
| iPhone 6.5" | 1284 x 2778 | Yes |
| iPhone 5.5" | 1242 x 2208 | Yes |
| iPad Pro 12.9" | 2048 x 2732 | If iPad supported |
| iPad Pro 11" | 1668 x 2388 | If iPad supported |

### Submission Process

1. Create archive: Product > Archive
2. Upload to App Store Connect
3. In App Store Connect:
   - Fill in app information
   - Upload screenshots
   - Select build
   - Answer export compliance questions
   - Submit for review

### Common Rejection Reasons

| Reason | Solution |
|--------|----------|
| Crashes | Fix all crashes, test thoroughly |
| Incomplete metadata | Fill all required fields |
| Broken links | Verify all URLs work |
| Privacy policy missing | Add privacy policy |
| Missing permissions descriptions | Add all NSUsageDescription keys |
| Guideline 4.3 - Spam | Make app significantly different |

## Keyboard Shortcuts

### Essential Shortcuts

| Shortcut | Action |
|----------|--------|
| Cmd+B | Build |
| Cmd+R | Run |
| Cmd+U | Test |
| Cmd+I | Profile |
| Cmd+Shift+K | Clean Build Folder |
| Cmd+. | Stop |
| Cmd+/ | Comment/Uncomment |
| Cmd+[ / ] | Indent/Outdent |
| Cmd+Shift+O | Open Quickly |
| Cmd+0 | Toggle Navigator |
| Cmd+Option+0 | Toggle Inspector |

### Navigation

| Shortcut | Action |
|----------|--------|
| Cmd+Shift+J | Reveal in Navigator |
| Cmd+Ctrl+↑/↓ | Switch .h/.m or extension |
| Cmd+Shift+L | Library (add views) |
| Cmd+Click | Jump to Definition |
| Cmd+Option+Click | Open in Assistant |

### Debugging

| Shortcut | Action |
|----------|--------|
| F6 | Step Over |
| F7 | Step Into |
| F8 | Step Out |
| Cmd+\ | Toggle Breakpoint |
| Cmd+Y | Activate/Deactivate Breakpoints |

## CI/CD Integration

### xcodebuild Commands

```bash
# List schemes
xcodebuild -list -project MyApp.xcodeproj

# Build
xcodebuild -project MyApp.xcodeproj -scheme MyApp -configuration Release

# Test
xcodebuild test -project MyApp.xcodeproj -scheme MyApp -destination 'platform=iOS Simulator,name=iPhone 15'

# Archive
xcodebuild archive -project MyApp.xcodeproj -scheme MyApp -archivePath ./build/MyApp.xcarchive

# Export IPA
xcodebuild -exportArchive -archivePath ./build/MyApp.xcarchive -exportPath ./build -exportOptionsPlist ExportOptions.plist
```

### ExportOptions.plist

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>method</key>
    <string>app-store</string>
    <key>teamID</key>
    <string>YOUR_TEAM_ID</string>
    <key>uploadSymbols</key>
    <true/>
</dict>
</plist>
```

### Fastlane Integration

```ruby
# Fastfile
default_platform(:ios)

platform :ios do
  desc "Run tests"
  lane :test do
    run_tests(scheme: "MyApp")
  end

  desc "Build and upload to TestFlight"
  lane :beta do
    increment_build_number
    build_app(scheme: "MyApp")
    upload_to_testflight
  end

  desc "Deploy to App Store"
  lane :release do
    build_app(scheme: "MyApp")
    upload_to_app_store(
      skip_screenshots: true,
      skip_metadata: true
    )
  end
end
```
