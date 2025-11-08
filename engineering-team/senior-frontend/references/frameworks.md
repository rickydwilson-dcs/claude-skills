# Frontend Architecture Frameworks & Design Patterns

Comprehensive guide to React/Next.js architecture patterns, component design, state management, and performance optimization for building modern, scalable frontend applications.

## Component Architecture Patterns

### Atomic Design Pattern

**Hierarchy:**
```
Atoms       → Button, Input, Label, Icon
Molecules   → SearchBar, FormField, Card
Organisms   → Navigation, ProductCard, LoginForm
Templates   → PageLayout, DashboardLayout
Pages       → HomePage, ProductDetailPage
```

**Implementation:**
```typescript
// atoms/Button.tsx
export interface ButtonProps {
  variant: 'primary' | 'secondary' | 'ghost';
  size: 'sm' | 'md' | 'lg';
  onClick?: () => void;
  children: React.ReactNode;
}

export const Button: React.FC<ButtonProps> = ({
  variant,
  size,
  onClick,
  children
}) => {
  const classes = cn(
    'btn',
    `btn-${variant}`,
    `btn-${size}`
  );

  return (
    <button className={classes} onClick={onClick}>
      {children}
    </button>
  );
};

// molecules/FormField.tsx
export const FormField: React.FC<{
  label: string;
  error?: string;
  children: React.ReactNode;
}> = ({ label, error, children }) => {
  return (
    <div className="form-field">
      <Label>{label}</Label>
      {children}
      {error && <ErrorText>{error}</ErrorText>}
    </div>
  );
};

// organisms/LoginForm.tsx
export const LoginForm: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  return (
    <form onSubmit={handleSubmit}>
      <FormField label="Email" error={emailError}>
        <Input value={email} onChange={setEmail} />
      </FormField>
      <FormField label="Password" error={passwordError}>
        <Input type="password" value={password} onChange={setPassword} />
      </FormField>
      <Button variant="primary" type="submit">
        Login
      </Button>
    </form>
  );
};
```

### Compound Component Pattern

**Usage:**
```typescript
// components/Select/index.tsx
interface SelectContextValue {
  selected: string;
  onChange: (value: string) => void;
}

const SelectContext = createContext<SelectContextValue | null>(null);

export const Select: React.FC<{
  value: string;
  onChange: (value: string) => void;
  children: React.ReactNode;
}> = ({ value, onChange, children }) => {
  return (
    <SelectContext.Provider value={{ selected: value, onChange }}>
      <div className="select">{children}</div>
    </SelectContext.Provider>
  );
};

Select.Trigger = function SelectTrigger({ children }) {
  const context = useContext(SelectContext);
  return (
    <button className="select-trigger">
      {children}
    </button>
  );
};

Select.Options = function SelectOptions({ children }) {
  return <div className="select-options">{children}</div>;
};

Select.Option = function SelectOption({ value, children }) {
  const context = useContext(SelectContext);
  return (
    <div
      className={cn('select-option', {
        'select-option-active': context?.selected === value
      })}
      onClick={() => context?.onChange(value)}
    >
      {children}
    </div>
  );
};

// Usage
<Select value={value} onChange={setValue}>
  <Select.Trigger>
    <span>{value}</span>
  </Select.Trigger>
  <Select.Options>
    <Select.Option value="red">Red</Select.Option>
    <Select.Option value="blue">Blue</Select.Option>
  </Select.Options>
</Select>
```

### Render Props Pattern

```typescript
interface DataLoaderProps<T> {
  url: string;
  render: (data: T | null, loading: boolean, error: Error | null) => React.ReactNode;
}

function DataLoader<T>({ url, render }: DataLoaderProps<T>) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    fetch(url)
      .then(res => res.json())
      .then(setData)
      .catch(setError)
      .finally(() => setLoading(false));
  }, [url]);

  return <>{render(data, loading, error)}</>;
}

// Usage
<DataLoader<User>
  url="/api/users/123"
  render={(user, loading, error) => {
    if (loading) return <Spinner />;
    if (error) return <ErrorMessage error={error} />;
    return <UserProfile user={user} />;
  }}
/>
```

## State Management Patterns

### Zustand (Lightweight)

```typescript
// stores/userStore.ts
import create from 'zustand';
import { persist } from 'zustand/middleware';

interface UserState {
  user: User | null;
  token: string | null;
  login: (user: User, token: string) => void;
  logout: () => void;
  updateUser: (user: Partial<User>) => void;
}

export const useUserStore = create<UserState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      login: (user, token) => set({ user, token }),
      logout: () => set({ user: null, token: null }),
      updateUser: (updates) =>
        set((state) => ({
          user: state.user ? { ...state.user, ...updates } : null
        }))
    }),
    { name: 'user-storage' }
  )
);

// Usage in components
const Component = () => {
  const { user, login, logout } = useUserStore();

  return (
    <div>
      {user ? (
        <>
          <p>Welcome {user.name}</p>
          <button onClick={logout}>Logout</button>
        </>
      ) : (
        <LoginForm onLogin={login} />
      )}
    </div>
  );
};
```

### Context + useReducer (Complex State)

```typescript
// contexts/CartContext.tsx
interface CartState {
  items: CartItem[];
  total: number;
}

type CartAction =
  | { type: 'ADD_ITEM'; payload: CartItem }
  | { type: 'REMOVE_ITEM'; payload: string }
  | { type: 'UPDATE_QUANTITY'; payload: { id: string; quantity: number } }
  | { type: 'CLEAR_CART' };

function cartReducer(state: CartState, action: CartAction): CartState {
  switch (action.type) {
    case 'ADD_ITEM':
      return {
        ...state,
        items: [...state.items, action.payload],
        total: state.total + action.payload.price * action.payload.quantity
      };
    case 'REMOVE_ITEM':
      const item = state.items.find(i => i.id === action.payload);
      return {
        ...state,
        items: state.items.filter(i => i.id !== action.payload),
        total: state.total - (item ? item.price * item.quantity : 0)
      };
    // ... other cases
    default:
      return state;
  }
}

export const CartProvider: React.FC = ({ children }) => {
  const [state, dispatch] = useReducer(cartReducer, { items: [], total: 0 });

  return (
    <CartContext.Provider value={{ state, dispatch }}>
      {children}
    </CartContext.Provider>
  );
};

export const useCart = () => {
  const context = useContext(CartContext);
  if (!context) throw new Error('useCart must be used within CartProvider');
  return context;
};
```

## Performance Optimization Patterns

### Code Splitting & Lazy Loading

```typescript
// Dynamic imports
const DashboardModule = lazy(() => import('./Dashboard'));
const ProfileModule = lazy(() => import('./Profile'));

// Route-based code splitting
function App() {
  return (
    <Suspense fallback={<PageLoader />}>
      <Routes>
        <Route path="/dashboard" element={<DashboardModule />} />
        <Route path="/profile" element={<ProfileModule />} />
      </Routes>
    </Suspense>
  );
}

// Component-level lazy loading
const HeavyChart = lazy(() => import('./HeavyChart'));

function Analytics() {
  const [showChart, setShowChart] = useState(false);

  return (
    <div>
      <button onClick={() => setShowChart(true)}>Show Chart</button>
      {showChart && (
        <Suspense fallback={<ChartSkeleton />}>
          <HeavyChart />
        </Suspense>
      )}
    </div>
  );
}
```

### Memoization Patterns

```typescript
// useMemo for expensive calculations
function ProductList({ products, filters }) {
  const filteredProducts = useMemo(() => {
    return products
      .filter(p => p.category === filters.category)
      .filter(p => p.price >= filters.minPrice && p.price <= filters.maxPrice)
      .sort((a, b) => a.price - b.price);
  }, [products, filters]); // Only recalculate when these change

  return <div>{filteredProducts.map(renderProduct)}</div>;
}

// useCallback for event handlers
function SearchBar({ onSearch }) {
  const [query, setQuery] = useState('');

  const handleSearch = useCallback(() => {
    onSearch(query);
  }, [query, onSearch]); // Stable reference

  return (
    <div>
      <input value={query} onChange={(e) => setQuery(e.target.value)} />
      <button onClick={handleSearch}>Search</button>
    </div>
  );
}

// React.memo for component memoization
export const ProductCard = React.memo<ProductCardProps>(
  ({ product }) => {
    return (
      <div className="product-card">
        <img src={product.image} alt={product.name} />
        <h3>{product.name}</h3>
        <p>${product.price}</p>
      </div>
    );
  },
  (prevProps, nextProps) => {
    // Custom comparison
    return prevProps.product.id === nextProps.product.id &&
           prevProps.product.price === nextProps.product.price;
  }
);
```

### Virtual Scrolling

```typescript
// Using react-window
import { FixedSizeList } from 'react-window';

function VirtualizedList({ items }) {
  const Row = ({ index, style }) => (
    <div style={style}>
      {items[index].name}
    </div>
  );

  return (
    <FixedSizeList
      height={600}
      itemCount={items.length}
      itemSize={50}
      width="100%"
    >
      {Row}
    </FixedSizeList>
  );
}
```

## Next.js Specific Patterns

### Server Components

```typescript
// app/dashboard/page.tsx (Server Component)
async function DashboardPage() {
  // Fetch data on server
  const user = await getUser();
  const stats = await getStats(user.id);

  return (
    <div>
      <h1>Dashboard</h1>
      <UserProfile user={user} />
      <Stats data={stats} />
    </div>
  );
}

// Client component for interactivity
'use client';

function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(count + 1)}>{count}</button>;
}
```

### Data Fetching Patterns

```typescript
// Server-side rendering (SSR)
export async function getServerSideProps(context) {
  const { id } = context.params;
  const product = await fetchProduct(id);

  return {
    props: { product }
  };
}

// Static generation (SSG)
export async function getStaticProps() {
  const products = await fetchProducts();

  return {
    props: { products },
    revalidate: 3600 // Revalidate every hour
  };
}

// Incremental static regeneration (ISR)
export async function getStaticPaths() {
  const products = await fetchProducts();

  return {
    paths: products.map(p => ({ params: { id: p.id } })),
    fallback: 'blocking'
  };
}
```

### API Routes

```typescript
// pages/api/users/[id].ts
import type { NextApiRequest, NextApiResponse } from 'next';

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  const { id } = req.query;

  if (req.method === 'GET') {
    const user = await getUserById(id as string);
    return res.status(200).json(user);
  }

  if (req.method === 'PUT') {
    const updated = await updateUser(id as string, req.body);
    return res.status(200).json(updated);
  }

  res.setHeader('Allow', ['GET', 'PUT']);
  res.status(405).end(`Method ${req.method} Not Allowed`);
}
```

## Testing Patterns

### Component Testing

```typescript
// ProductCard.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { ProductCard } from './ProductCard';

describe('ProductCard', () => {
  const mockProduct = {
    id: '1',
    name: 'Test Product',
    price: 99.99,
    image: '/test.jpg'
  };

  it('renders product information', () => {
    render(<ProductCard product={mockProduct} />);

    expect(screen.getByText('Test Product')).toBeInTheDocument();
    expect(screen.getByText('$99.99')).toBeInTheDocument();
  });

  it('calls onAddToCart when button clicked', () => {
    const onAddToCart = jest.fn();
    render(<ProductCard product={mockProduct} onAddToCart={onAddToCart} />);

    fireEvent.click(screen.getByText('Add to Cart'));
    expect(onAddToCart).toHaveBeenCalledWith(mockProduct);
  });
});
```

### Custom Hook Testing

```typescript
// useDebounce.test.ts
import { renderHook, act } from '@testing-library/react';
import { useDebounce } from './useDebounce';

describe('useDebounce', () => {
  jest.useFakeTimers();

  it('debounces value changes', () => {
    const { result, rerender } = renderHook(
      ({ value }) => useDebounce(value, 500),
      { initialProps: { value: 'initial' } }
    );

    expect(result.current).toBe('initial');

    rerender({ value: 'changed' });
    expect(result.current).toBe('initial'); // Still old value

    act(() => {
      jest.advanceTimersByTime(500);
    });

    expect(result.current).toBe('changed'); // Now updated
  });
});
```

## Styling Patterns

### CSS Modules

```typescript
// Button.module.css
.button {
  padding: 0.5rem 1rem;
  border-radius: 0.25rem;
  font-weight: 500;
}

.primary {
  background-color: var(--color-primary);
  color: white;
}

.secondary {
  background-color: var(--color-secondary);
  color: white;
}

// Button.tsx
import styles from './Button.module.css';

export const Button = ({ variant = 'primary', children }) => {
  return (
    <button className={`${styles.button} ${styles[variant]}`}>
      {children}
    </button>
  );
};
```

### Tailwind CSS with CVA

```typescript
import { cva, type VariantProps } from 'class-variance-authority';

const buttonVariants = cva(
  'inline-flex items-center justify-center rounded-md font-medium transition-colors',
  {
    variants: {
      variant: {
        primary: 'bg-blue-600 text-white hover:bg-blue-700',
        secondary: 'bg-gray-200 text-gray-900 hover:bg-gray-300',
        ghost: 'hover:bg-gray-100'
      },
      size: {
        sm: 'h-8 px-3 text-sm',
        md: 'h-10 px-4',
        lg: 'h-12 px-6 text-lg'
      }
    },
    defaultVariants: {
      variant: 'primary',
      size: 'md'
    }
  }
);

interface ButtonProps extends VariantProps<typeof buttonVariants> {
  children: React.ReactNode;
}

export const Button: React.FC<ButtonProps> = ({ variant, size, children }) => {
  return (
    <button className={buttonVariants({ variant, size })}>
      {children}
    </button>
  );
};
```

## Error Handling Patterns

### Error Boundaries

```typescript
class ErrorBoundary extends React.Component<
  { children: React.ReactNode; fallback?: React.ReactNode },
  { hasError: boolean; error?: Error }
> {
  state = { hasError: false, error: undefined };

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('Error caught by boundary:', error, errorInfo);
    // Log to error tracking service
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback || (
        <div>
          <h2>Something went wrong</h2>
          <p>{this.state.error?.message}</p>
        </div>
      );
    }

    return this.props.children;
  }
}

// Usage
<ErrorBoundary fallback={<ErrorFallback />}>
  <App />
</ErrorBoundary>
```

This comprehensive framework guide provides the foundation for building modern, performant React and Next.js applications.
