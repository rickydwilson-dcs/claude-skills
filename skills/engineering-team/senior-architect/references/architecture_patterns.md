# System Architecture Patterns

## Overview

Comprehensive guide to modern software architecture patterns for building scalable, maintainable, and resilient systems. Covers microservices, event-driven architectures, domain-driven design, and cloud-native patterns.

## Monolithic Architecture

### Traditional Monolith

**When to Use:**
- Small to medium applications
- Limited team size (< 10 developers)
- Simple deployment requirements
- Rapid prototyping

**Benefits:**
- Simple deployment
- Easy debugging
- Strong consistency
- Lower operational overhead

**Trade-offs:**
- Scalability limitations
- Technology lock-in
- Slower deployment cycles
- All-or-nothing scaling

**Example Structure:**
```
monolith/
├── web/              # Presentation layer
├── services/         # Business logic
├── data/             # Data access
└── shared/           # Utilities
```

### Modular Monolith

**Description:** Monolith organized into well-defined modules with clear boundaries.

**When to Use:**
- Growing applications
- Teams need independence
- Not ready for microservices
- Need monolith benefits with better organization

**Structure:**
```typescript
// Module boundaries
modules/
├── users/
│   ├── api/
│   ├── services/
│   └── data/
├── orders/
│   ├── api/
│   ├── services/
│   └── data/
└── payments/
    ├── api/
    ├── services/
    └── data/

// Each module exports clean interface
export class UsersModule {
  getUserById(id: string): Promise<User>;
  createUser(data: CreateUserDto): Promise<User>;
}
```

**Key Principles:**
- Strong module boundaries
- No cross-module database access
- Clear public APIs
- Independent testing

## Microservices Architecture

### Service Decomposition Strategies

**By Business Capability**
```
Services:
- User Service (identity, profile)
- Order Service (orders, cart)
- Payment Service (transactions)
- Inventory Service (stock management)
- Notification Service (email, SMS)
```

**By Subdomain (DDD)**
```
Core Domain:
- Order Management (competitive advantage)

Supporting Domains:
- User Management
- Payment Processing

Generic Domains:
- Email/SMS (use 3rd party)
```

### Service Communication Patterns

**Synchronous Communication**

**REST APIs**
```typescript
// API Gateway pattern
@Controller('/api/orders')
export class OrdersController {
  constructor(
    private ordersService: OrdersService,
    private usersClient: UsersApiClient,
    private paymentsClient: PaymentsApiClient
  ) {}

  @Post()
  async createOrder(@Body() data: CreateOrderDto) {
    // Validate user
    const user = await this.usersClient.getUser(data.userId);

    // Create order
    const order = await this.ordersService.create(data);

    // Process payment
    const payment = await this.paymentsClient.charge({
      orderId: order.id,
      amount: order.total
    });

    return { order, payment };
  }
}
```

**GraphQL Federation**
```typescript
// User service schema
type User @key(fields: "id") {
  id: ID!
  name: String!
  email: String!
}

// Order service schema
extend type User @key(fields: "id") {
  id: ID! @external
  orders: [Order!]!
}

// Gateway automatically federates
query {
  user(id: "123") {
    name
    email
    orders {
      id
      total
    }
  }
}
```

**Asynchronous Communication**

**Event-Driven Architecture**
```typescript
// Publisher
class OrderService {
  async createOrder(data: CreateOrderDto) {
    const order = await this.repository.save(data);

    // Publish event
    await this.eventBus.publish('order.created', {
      orderId: order.id,
      userId: order.userId,
      total: order.total,
      timestamp: new Date()
    });

    return order;
  }
}

// Subscriber
class NotificationService {
  @EventHandler('order.created')
  async onOrderCreated(event: OrderCreatedEvent) {
    await this.emailService.send({
      to: event.userEmail,
      subject: 'Order Confirmed',
      body: `Your order #${event.orderId} has been confirmed.`
    });
  }
}

// Another subscriber
class InventoryService {
  @EventHandler('order.created')
  async onOrderCreated(event: OrderCreatedEvent) {
    await this.reserveStock(event.items);
  }
}
```

**Message Queues (RabbitMQ/Kafka)**
```typescript
// Producer
await channel.sendToQueue('orders.processing', {
  orderId: order.id,
  items: order.items
});

// Consumer
channel.consume('orders.processing', async (msg) => {
  const order = JSON.parse(msg.content.toString());
  await processOrder(order);
  channel.ack(msg);
});
```

### Service Mesh

**Features:**
- Service discovery
- Load balancing
- Circuit breaking
- Observability
- Security (mTLS)

**Istio Example:**
```yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: orders
spec:
  hosts:
  - orders.default.svc.cluster.local
  http:
  - match:
    - headers:
        version:
          exact: v2
    route:
    - destination:
        host: orders
        subset: v2
  - route:
    - destination:
        host: orders
        subset: v1
      weight: 90
    - destination:
        host: orders
        subset: v2
      weight: 10
```

## Event-Driven Architecture

### Event Sourcing

**Concept:** Store state changes as events rather than current state.

**Implementation:**
```typescript
// Events
interface OrderEvent {
  type: string;
  orderId: string;
  timestamp: Date;
}

interface OrderCreatedEvent extends OrderEvent {
  type: 'ORDER_CREATED';
  userId: string;
  items: OrderItem[];
}

interface OrderShippedEvent extends OrderEvent {
  type: 'ORDER_SHIPPED';
  trackingNumber: string;
}

// Event Store
class EventStore {
  async append(streamId: string, event: OrderEvent): Promise<void> {
    await this.db.events.insert({
      streamId,
      type: event.type,
      data: event,
      version: await this.getNextVersion(streamId),
      timestamp: new Date()
    });
  }

  async getEvents(streamId: string): Promise<OrderEvent[]> {
    return await this.db.events.find({ streamId }).sort({ version: 1 });
  }
}

// Aggregate
class Order {
  private events: OrderEvent[] = [];
  id: string;
  status: OrderStatus;
  items: OrderItem[];

  static fromEvents(events: OrderEvent[]): Order {
    const order = new Order();
    events.forEach(event => order.apply(event));
    return order;
  }

  apply(event: OrderEvent): void {
    switch (event.type) {
      case 'ORDER_CREATED':
        this.id = event.orderId;
        this.items = event.items;
        this.status = 'CREATED';
        break;
      case 'ORDER_SHIPPED':
        this.status = 'SHIPPED';
        break;
    }
    this.events.push(event);
  }
}
```

**Benefits:**
- Complete audit trail
- Temporal queries (state at any point in time)
- Event replay for debugging
- Multiple read models from same events

**Trade-offs:**
- Increased complexity
- Storage requirements
- Eventual consistency
- Schema evolution challenges

### CQRS (Command Query Responsibility Segregation)

**Pattern:** Separate read and write models.

```typescript
// Write Model (Commands)
class CreateOrderCommandHandler {
  async handle(command: CreateOrderCommand): Promise<void> {
    const order = new Order(command.userId, command.items);
    await this.eventStore.append(`order-${order.id}`, [
      { type: 'ORDER_CREATED', ...order }
    ]);
  }
}

// Read Model (Queries)
class OrderQueryService {
  // Optimized for reads
  async getOrderById(id: string): Promise<OrderDto> {
    return await this.readDB.orders.findOne({ id });
  }

  async getUserOrders(userId: string): Promise<OrderDto[]> {
    return await this.readDB.orders.find({ userId });
  }
}

// Projections (Event Handlers that update read model)
class OrderProjection {
  @EventHandler('ORDER_CREATED')
  async onOrderCreated(event: OrderCreatedEvent): Promise<void> {
    await this.readDB.orders.insert({
      id: event.orderId,
      userId: event.userId,
      items: event.items,
      status: 'CREATED',
      createdAt: event.timestamp
    });
  }

  @EventHandler('ORDER_SHIPPED')
  async onOrderShipped(event: OrderShippedEvent): Promise<void> {
    await this.readDB.orders.update(
      { id: event.orderId },
      { status: 'SHIPPED', shippedAt: event.timestamp }
    );
  }
}
```

## Domain-Driven Design (DDD)

### Strategic Design

**Bounded Contexts**
```
E-commerce System:

[Sales Context]
- Order (aggregate)
- Customer (entity)
- Product (entity)

[Inventory Context]
- Stock (aggregate)
- Product (entity - different from Sales)
- Warehouse (entity)

[Shipping Context]
- Shipment (aggregate)
- Order (entity - just ID and items)
- Address (value object)
```

**Context Mapping**
```typescript
// Anti-Corruption Layer
class SalesOrderAdapter {
  toShippingOrder(salesOrder: SalesOrder): ShippingOrder {
    return {
      id: salesOrder.id,
      items: salesOrder.items.map(item => ({
        sku: item.product.sku,
        quantity: item.quantity,
        weight: item.product.weight
      })),
      destination: this.toShippingAddress(salesOrder.deliveryAddress)
    };
  }

  private toShippingAddress(address: CustomerAddress): ShippingAddress {
    // Transform between contexts
  }
}
```

### Tactical Design

**Aggregates**
```typescript
// Order Aggregate Root
class Order {
  private _id: OrderId;
  private _customerId: CustomerId;
  private _items: OrderItem[] = [];
  private _status: OrderStatus;
  private _total: Money;

  // Factory method
  static create(customerId: CustomerId, items: OrderItem[]): Order {
    const order = new Order();
    order._id = OrderId.generate();
    order._customerId = customerId;
    order._status = OrderStatus.Draft;
    items.forEach(item => order.addItem(item));
    return order;
  }

  // Business logic
  addItem(item: OrderItem): void {
    if (this._status !== OrderStatus.Draft) {
      throw new Error('Cannot add items to non-draft order');
    }
    this._items.push(item);
    this.recalculateTotal();
  }

  submit(): void {
    if (this._items.length === 0) {
      throw new Error('Cannot submit order without items');
    }
    this._status = OrderStatus.Submitted;
    // Emit domain event
    this.addDomainEvent(new OrderSubmittedEvent(this._id));
  }

  private recalculateTotal(): void {
    this._total = this._items.reduce(
      (sum, item) => sum.add(item.price.multiply(item.quantity)),
      Money.zero()
    );
  }
}

// Value Object
class Money {
  private constructor(
    private readonly amount: number,
    private readonly currency: string
  ) {}

  static create(amount: number, currency: string): Money {
    if (amount < 0) throw new Error('Amount cannot be negative');
    return new Money(amount, currency);
  }

  add(other: Money): Money {
    if (this.currency !== other.currency) {
      throw new Error('Cannot add different currencies');
    }
    return new Money(this.amount + other.amount, this.currency);
  }

  equals(other: Money): boolean {
    return this.amount === other.amount && this.currency === other.currency;
  }
}
```

## Cloud-Native Patterns

### The Twelve-Factor App

1. **Codebase:** One codebase tracked in version control
2. **Dependencies:** Explicitly declare dependencies
3. **Config:** Store config in environment
4. **Backing Services:** Treat as attached resources
5. **Build, Release, Run:** Strictly separate stages
6. **Processes:** Execute as stateless processes
7. **Port Binding:** Export services via port binding
8. **Concurrency:** Scale out via process model
9. **Disposability:** Fast startup and graceful shutdown
10. **Dev/Prod Parity:** Keep environments similar
11. **Logs:** Treat logs as event streams
12. **Admin Processes:** Run as one-off processes

### Container Orchestration (Kubernetes)

**Deployment Strategy:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: orders-service
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    spec:
      containers:
      - name: orders
        image: orders-service:v2
        ports:
        - containerPort: 3000
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
        livenessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 5
```

### Resilience Patterns

**Circuit Breaker**
```typescript
class CircuitBreaker {
  private state: 'CLOSED' | 'OPEN' | 'HALF_OPEN' = 'CLOSED';
  private failureCount = 0;
  private lastFailureTime?: Date;

  async execute<T>(fn: () => Promise<T>): Promise<T> {
    if (this.state === 'OPEN') {
      if (this.shouldAttemptReset()) {
        this.state = 'HALF_OPEN';
      } else {
        throw new Error('Circuit breaker is OPEN');
      }
    }

    try {
      const result = await fn();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }

  private onSuccess(): void {
    this.failureCount = 0;
    this.state = 'CLOSED';
  }

  private onFailure(): void {
    this.failureCount++;
    this.lastFailureTime = new Date();

    if (this.failureCount >= this.threshold) {
      this.state = 'OPEN';
    }
  }
}
```

**Retry Pattern**
```typescript
async function withRetry<T>(
  fn: () => Promise<T>,
  options: RetryOptions
): Promise<T> {
  let lastError: Error;

  for (let attempt = 1; attempt <= options.maxAttempts; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error;

      if (attempt < options.maxAttempts) {
        const delay = options.backoffMs * Math.pow(2, attempt - 1);
        await sleep(delay);
      }
    }
  }

  throw lastError;
}
```

## Conclusion

Choose architecture patterns based on:
- System complexity
- Team size and structure
- Scalability requirements
- Consistency needs
- Deployment frequency

Start simple (modular monolith), evolve to complexity (microservices) only when needed.

**Key Takeaways:**
- Monoliths aren't bad - modular monoliths are often ideal
- Microservices add operational complexity
- Event-driven architectures enable loose coupling
- DDD helps manage complexity in large systems
- Cloud-native patterns are essential for modern deployments
- Always measure and iterate
