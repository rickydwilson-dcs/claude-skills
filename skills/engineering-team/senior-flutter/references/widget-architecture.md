# Widget Architecture Guide

Deep dive into Flutter widget architecture, lifecycle, and performance optimization.

## Widget Fundamentals

### Widget Types

```dart
// StatelessWidget - Immutable, no internal state
class GreetingWidget extends StatelessWidget {
  final String name;

  const GreetingWidget({super.key, required this.name});

  @override
  Widget build(BuildContext context) {
    return Text('Hello, $name!');
  }
}

// StatefulWidget - Mutable state
class CounterWidget extends StatefulWidget {
  const CounterWidget({super.key});

  @override
  State<CounterWidget> createState() => _CounterWidgetState();
}

class _CounterWidgetState extends State<CounterWidget> {
  int _count = 0;

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text('Count: $_count'),
        ElevatedButton(
          onPressed: () => setState(() => _count++),
          child: const Text('Increment'),
        ),
      ],
    );
  }
}
```

### Widget Lifecycle

```dart
class LifecycleWidget extends StatefulWidget {
  const LifecycleWidget({super.key});

  @override
  State<LifecycleWidget> createState() => _LifecycleWidgetState();
}

class _LifecycleWidgetState extends State<LifecycleWidget> {
  @override
  void initState() {
    super.initState();
    // Called once when widget is inserted into tree
    // Initialize state, start animations, subscribe to streams
  }

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    // Called after initState and when dependencies change
    // Good for InheritedWidget lookups
  }

  @override
  void didUpdateWidget(LifecycleWidget oldWidget) {
    super.didUpdateWidget(oldWidget);
    // Called when parent rebuilds with new widget
    // Compare oldWidget with widget to handle changes
  }

  @override
  void deactivate() {
    super.deactivate();
    // Called when widget is removed from tree (temporarily)
  }

  @override
  void dispose() {
    super.dispose();
    // Called when widget is permanently removed
    // Clean up: cancel subscriptions, dispose controllers
  }

  @override
  Widget build(BuildContext context) {
    return Container();
  }
}
```

## Keys

### When to Use Keys

```dart
// ALWAYS use keys for lists of widgets that can be reordered
class TodoList extends StatelessWidget {
  final List<Todo> todos;

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      itemCount: todos.length,
      itemBuilder: (context, index) {
        final todo = todos[index];
        return TodoItem(
          key: ValueKey(todo.id),  // Essential for correct updates
          todo: todo,
        );
      },
    );
  }
}

// Use GlobalKey for accessing state from outside
class FormScreen extends StatefulWidget {
  @override
  State<FormScreen> createState() => _FormScreenState();
}

class _FormScreenState extends State<FormScreen> {
  final _formKey = GlobalKey<FormState>();

  void _submit() {
    if (_formKey.currentState!.validate()) {
      _formKey.currentState!.save();
      // Process form
    }
  }

  @override
  Widget build(BuildContext context) {
    return Form(
      key: _formKey,
      child: Column(/* ... */),
    );
  }
}
```

### Key Types

```dart
// ValueKey - Based on value equality
ValueKey('unique_string')
ValueKey(item.id)

// ObjectKey - Based on object identity
ObjectKey(itemInstance)

// UniqueKey - Always unique (creates new key each time)
UniqueKey()  // Use sparingly, forces rebuild

// GlobalKey - Access state and context across tree
final key = GlobalKey<ScaffoldState>();
key.currentState?.openDrawer();

// PageStorageKey - Preserve scroll position
ListView(
  key: PageStorageKey('my_list'),
  children: [...],
)
```

## BuildContext

### Understanding BuildContext

```dart
class ContextExample extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    // Context represents this widget's location in the tree

    // Access theme
    final theme = Theme.of(context);

    // Access media query
    final size = MediaQuery.of(context).size;

    // Navigate
    Navigator.of(context).push(...);

    // Show snackbar
    ScaffoldMessenger.of(context).showSnackBar(...);

    // Find ancestor widget
    final scaffold = context.findAncestorWidgetOfExactType<Scaffold>();

    return Container();
  }
}
```

### Context Gotchas

```dart
// BAD: Using context after async gap
void _loadData() async {
  final data = await fetchData();
  // Context might be invalid here!
  Navigator.of(context).pop();  // Can crash
}

// GOOD: Check mounted or capture early
void _loadData() async {
  final navigator = Navigator.of(context);
  final data = await fetchData();

  if (!mounted) return;  // Check if still in tree
  navigator.pop();
}

// BAD: Using context in initState
@override
void initState() {
  super.initState();
  final theme = Theme.of(context);  // Error! Context not ready
}

// GOOD: Use didChangeDependencies
@override
void didChangeDependencies() {
  super.didChangeDependencies();
  final theme = Theme.of(context);  // Works here
}
```

## InheritedWidget

### Creating InheritedWidget

```dart
// Define the inherited widget
class ThemeProvider extends InheritedWidget {
  final AppTheme theme;

  const ThemeProvider({
    super.key,
    required this.theme,
    required super.child,
  });

  static AppTheme of(BuildContext context) {
    final provider = context.dependOnInheritedWidgetOfExactType<ThemeProvider>();
    assert(provider != null, 'No ThemeProvider found in context');
    return provider!.theme;
  }

  static AppTheme? maybeOf(BuildContext context) {
    return context.dependOnInheritedWidgetOfExactType<ThemeProvider>()?.theme;
  }

  @override
  bool updateShouldNotify(ThemeProvider oldWidget) {
    return theme != oldWidget.theme;
  }
}

// Usage
class ThemedButton extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final theme = ThemeProvider.of(context);
    return ElevatedButton(
      style: ElevatedButton.styleFrom(
        backgroundColor: theme.primaryColor,
      ),
      onPressed: () {},
      child: Text('Themed'),
    );
  }
}
```

### InheritedNotifier

```dart
// For ChangeNotifier integration
class CounterNotifier extends ChangeNotifier {
  int _count = 0;
  int get count => _count;

  void increment() {
    _count++;
    notifyListeners();
  }
}

class CounterProvider extends InheritedNotifier<CounterNotifier> {
  const CounterProvider({
    super.key,
    required CounterNotifier super.notifier,
    required super.child,
  });

  static CounterNotifier of(BuildContext context) {
    return context
        .dependOnInheritedWidgetOfExactType<CounterProvider>()!
        .notifier!;
  }
}
```

## Render Objects

### CustomPaint

```dart
class CustomCircle extends StatelessWidget {
  final Color color;
  final double radius;

  const CustomCircle({
    super.key,
    required this.color,
    required this.radius,
  });

  @override
  Widget build(BuildContext context) {
    return CustomPaint(
      size: Size(radius * 2, radius * 2),
      painter: CirclePainter(color: color, radius: radius),
    );
  }
}

class CirclePainter extends CustomPainter {
  final Color color;
  final double radius;

  CirclePainter({required this.color, required this.radius});

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = color
      ..style = PaintingStyle.fill;

    canvas.drawCircle(
      Offset(size.width / 2, size.height / 2),
      radius,
      paint,
    );
  }

  @override
  bool shouldRepaint(CirclePainter oldDelegate) {
    return color != oldDelegate.color || radius != oldDelegate.radius;
  }
}
```

### RenderObject Widget

```dart
// For complex custom layouts
class CustomLayout extends MultiChildRenderObjectWidget {
  const CustomLayout({super.key, super.children});

  @override
  RenderObject createRenderObject(BuildContext context) {
    return RenderCustomLayout();
  }
}

class CustomLayoutParentData extends ContainerBoxParentData<RenderBox> {}

class RenderCustomLayout extends RenderBox
    with
        ContainerRenderObjectMixin<RenderBox, CustomLayoutParentData>,
        RenderBoxContainerDefaultsMixin<RenderBox, CustomLayoutParentData> {

  @override
  void setupParentData(RenderBox child) {
    if (child.parentData is! CustomLayoutParentData) {
      child.parentData = CustomLayoutParentData();
    }
  }

  @override
  void performLayout() {
    // Custom layout logic
    size = constraints.biggest;

    RenderBox? child = firstChild;
    while (child != null) {
      child.layout(constraints.loosen(), parentUsesSize: true);
      final childParentData = child.parentData as CustomLayoutParentData;
      // Position child...
      child = childParentData.nextSibling;
    }
  }

  @override
  void paint(PaintingContext context, Offset offset) {
    defaultPaint(context, offset);
  }
}
```

## Performance Optimization

### Const Constructors

```dart
// GOOD: Use const for static content
class MyWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Column(
      children: const [
        Text('Static text'),  // const
        Icon(Icons.star),     // const
        SizedBox(height: 8),  // const
      ],
    );
  }
}

// Define const widgets
class AppConstants {
  static const divider = Divider(height: 1);
  static const spacer = SizedBox(height: 16);
  static const loadingIndicator = Center(child: CircularProgressIndicator());
}
```

### RepaintBoundary

```dart
// Isolate expensive repaints
class ExpensiveAnimationWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return RepaintBoundary(
      child: CustomPaint(
        painter: ExpensivePainter(),
        size: const Size(200, 200),
      ),
    );
  }
}

// Use for static parts that don't need repainting
class ComplexScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        // Static header - won't repaint when list scrolls
        const RepaintBoundary(
          child: Header(),
        ),
        // Scrolling list
        Expanded(
          child: ListView.builder(
            itemCount: 1000,
            itemBuilder: (context, index) => ListItem(index: index),
          ),
        ),
      ],
    );
  }
}
```

### Avoiding Rebuilds

```dart
// BAD: Creates new callback every build
class BadExample extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      itemCount: 100,
      itemBuilder: (context, index) {
        return ListTile(
          onTap: () => handleTap(index),  // New closure each build
        );
      },
    );
  }
}

// GOOD: Use a separate widget with stable callback
class GoodExample extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      itemCount: 100,
      itemBuilder: (context, index) {
        return ItemTile(
          index: index,
          onTap: handleTap,
        );
      },
    );
  }
}

class ItemTile extends StatelessWidget {
  final int index;
  final void Function(int) onTap;

  const ItemTile({super.key, required this.index, required this.onTap});

  @override
  Widget build(BuildContext context) {
    return ListTile(
      onTap: () => onTap(index),
    );
  }
}
```

### Widget Extraction

```dart
// BAD: Large build method
class LargeBuildMethod extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        // 50 lines of header code
        // 50 lines of content code
        // 50 lines of footer code
      ],
    );
  }
}

// GOOD: Extract to separate widgets
class WellStructured extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return const Column(
      children: [
        _Header(),
        _Content(),
        _Footer(),
      ],
    );
  }
}

class _Header extends StatelessWidget {
  const _Header();

  @override
  Widget build(BuildContext context) {
    // Header implementation
    return Container();
  }
}
```

## Slivers

### Basic Sliver Usage

```dart
class SliverExample extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return CustomScrollView(
      slivers: [
        // App bar that collapses
        SliverAppBar(
          expandedHeight: 200,
          pinned: true,
          flexibleSpace: FlexibleSpaceBar(
            title: const Text('Title'),
            background: Image.network('url', fit: BoxFit.cover),
          ),
        ),

        // Fixed height header
        const SliverToBoxAdapter(
          child: Padding(
            padding: EdgeInsets.all(16),
            child: Text('Section Header'),
          ),
        ),

        // Grid of items
        SliverGrid(
          gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
            crossAxisCount: 2,
            crossAxisSpacing: 8,
            mainAxisSpacing: 8,
          ),
          delegate: SliverChildBuilderDelegate(
            (context, index) => GridItem(index: index),
            childCount: 20,
          ),
        ),

        // List of items
        SliverList(
          delegate: SliverChildBuilderDelegate(
            (context, index) => ListItem(index: index),
            childCount: 50,
          ),
        ),

        // Fill remaining space
        SliverFillRemaining(
          hasScrollBody: false,
          child: const Center(child: Text('End of list')),
        ),
      ],
    );
  }
}
```

### SliverPersistentHeader

```dart
class StickyHeader extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return CustomScrollView(
      slivers: [
        SliverPersistentHeader(
          pinned: true,
          delegate: _StickyHeaderDelegate(
            minHeight: 60,
            maxHeight: 150,
            child: Container(
              color: Colors.blue,
              child: const Center(child: Text('Sticky Header')),
            ),
          ),
        ),
        // ... other slivers
      ],
    );
  }
}

class _StickyHeaderDelegate extends SliverPersistentHeaderDelegate {
  final double minHeight;
  final double maxHeight;
  final Widget child;

  _StickyHeaderDelegate({
    required this.minHeight,
    required this.maxHeight,
    required this.child,
  });

  @override
  Widget build(context, double shrinkOffset, bool overlapsContent) {
    return SizedBox.expand(child: child);
  }

  @override
  double get maxExtent => maxHeight;

  @override
  double get minExtent => minHeight;

  @override
  bool shouldRebuild(_StickyHeaderDelegate oldDelegate) {
    return maxHeight != oldDelegate.maxHeight ||
        minHeight != oldDelegate.minHeight ||
        child != oldDelegate.child;
  }
}
```

## Testing Widgets

### Widget Tests

```dart
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets('Counter increments', (WidgetTester tester) async {
    // Build widget
    await tester.pumpWidget(const MaterialApp(home: CounterWidget()));

    // Verify initial state
    expect(find.text('0'), findsOneWidget);

    // Tap button
    await tester.tap(find.byIcon(Icons.add));
    await tester.pump();  // Rebuild

    // Verify new state
    expect(find.text('1'), findsOneWidget);
  });

  testWidgets('Shows loading then content', (WidgetTester tester) async {
    await tester.pumpWidget(MaterialApp(home: AsyncWidget()));

    // Initially shows loading
    expect(find.byType(CircularProgressIndicator), findsOneWidget);

    // Wait for async operation
    await tester.pumpAndSettle();

    // Shows content
    expect(find.byType(CircularProgressIndicator), findsNothing);
    expect(find.text('Content'), findsOneWidget);
  });
}
```

### Golden Tests

```dart
void main() {
  testWidgets('MyWidget matches golden', (WidgetTester tester) async {
    await tester.pumpWidget(
      MaterialApp(
        home: MyWidget(),
      ),
    );

    await expectLater(
      find.byType(MyWidget),
      matchesGoldenFile('goldens/my_widget.png'),
    );
  });
}
```
