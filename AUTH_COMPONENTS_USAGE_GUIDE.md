# Authentication Components Usage Guide

Quick reference for using the Phase 3 authentication components.

## Routes

### Public Routes (No Authentication Required)
- `/login` - Login page
- `/register` - Registration page

### Protected Routes (Require Authentication)
- `/dashboard` - Main dashboard (example)
- Any route wrapped with `<ProtectedRoute>`

## Components

### 1. LoginForm
Standalone login form component with validation.

```tsx
import LoginForm from '@/components/auth/LoginForm';

export default function LoginPage() {
  return (
    <div className="container">
      <LoginForm />
    </div>
  );
}
```

**Features**:
- Email and password fields
- Form validation
- Loading state
- Error display
- Auto-redirect to /dashboard on success

---

### 2. RegisterForm
Registration form with password confirmation.

```tsx
import RegisterForm from '@/components/auth/RegisterForm';

export default function RegisterPage() {
  return (
    <div className="container">
      <RegisterForm />
    </div>
  );
}
```

**Features**:
- Email, password, confirm password fields
- Strong password validation
- Duplicate email error handling
- Loading state
- Auto-redirect to /dashboard on success

---

### 3. ProtectedRoute
Wrapper component to protect routes from unauthenticated access.

```tsx
import ProtectedRoute from '@/components/auth/ProtectedRoute';

export default function DashboardPage() {
  return (
    <ProtectedRoute>
      <div>
        {/* Your protected content here */}
        <h1>Dashboard</h1>
      </div>
    </ProtectedRoute>
  );
}
```

**Options**:
```tsx
// Custom redirect path
<ProtectedRoute redirectTo="/custom-login">
  {/* Protected content */}
</ProtectedRoute>
```

**Features**:
- Automatic redirect to /login (or custom path)
- Loading skeleton during auth check
- Seamless user experience

---

### 4. useAuth Hook
Access authentication state and methods.

```tsx
'use client';

import { useAuth } from '../../../hooks/use-auth';

export default function MyComponent() {
  const {
    user,           // Current user object or null
    isAuthenticated, // Boolean
    isLoading,      // Boolean
    error,          // Error message or null
    login,          // (credentials) => Promise<void>
    register,       // (input) => Promise<void>
    logout,         // () => Promise<void>
    refreshSession, // () => Promise<void>
    clearError,     // () => void
  } = useAuth();

  // Example: Logout handler
  const handleLogout = async () => {
    await logout();
    router.push('/login');
  };

  return (
    <div>
      {isLoading && <p>Loading...</p>}
      {user && <p>Welcome, {user.email}!</p>}
    </div>
  );
}
```

**Methods**:

#### `login(credentials)`
```tsx
await login({
  email: 'user@example.com',
  password: 'SecurePass123',
});
```

#### `register(input)`
```tsx
await register({
  email: 'newuser@example.com',
  password: 'SecurePass123',
});
```

#### `logout()`
```tsx
await logout();
```

#### `refreshSession()`
```tsx
await refreshSession(); // Refresh current session
```

---

## Validation Schemas

### Login Schema
```tsx
import { loginSchema, type LoginFormData } from '../../../../lib/validations';

// Schema structure:
{
  email: string;    // Required, valid email
  password: string; // Required, min 8 characters
}
```

### Register Schema
```tsx
import { registerSchema, type RegisterFormData } from '../../../../lib/validations';

// Schema structure:
{
  email: string;          // Required, valid email, max 255 chars
  password: string;       // Required, min 8 chars, must have uppercase, lowercase, number
  confirmPassword: string; // Required, must match password
}
```

---

## Animations

All auth forms use `pageVariants` for smooth fade-in animations.

```tsx
import { pageVariants } from '../../../../lib/animations';
import { motion } from 'framer-motion';

<motion.div
  variants={pageVariants}
  initial="initial"
  animate="animate"
  exit="exit"
>
  {/* Your content */}
</motion.div>
```

**Animation Specs**:
- Initial: opacity 0, y: 20
- Animate: opacity 1, y: 0, duration 300ms
- Exit: opacity 0, y: -20, duration 200ms

---

## Error Handling

### Display Errors in Forms
```tsx
import { Alert, AlertDescription } from '@/components/ui/alert';

{error && (
  <Alert variant="destructive">
    <AlertDescription>{error}</AlertDescription>
  </Alert>
)}
```

### Custom Error Messages
```tsx
try {
  await register(data);
} catch (err) {
  const errorMessage = err instanceof Error
    ? err.message
    : 'An error occurred';

  // Check for specific errors
  if (errorMessage.includes('already exists')) {
    setCustomError('Email already registered');
  }
}
```

---

## Styling

### Primary Colors
```css
/* Teal - Primary action color */
bg-teal-600   /* #14b8a6 */
hover:bg-teal-700 /* #0f766e */

/* Backgrounds */
bg-gradient-to-br from-teal-50 to-blue-50
```

### Button Styling
```tsx
<Button
  className="w-full bg-teal-600 hover:bg-teal-700"
  disabled={isLoading}
>
  {isLoading ? (
    <>
      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
      Loading...
    </>
  ) : (
    'Submit'
  )}
</Button>
```

---

## Complete Example: Custom Protected Page

```tsx
'use client';

import { useRouter } from 'next/navigation';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import { useAuth } from '../../../hooks/use-auth';
import { Button } from '@/components/ui/button';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';

export default function MyProtectedPage() {
  const router = useRouter();
  const { user, logout, isLoading } = useAuth();

  const handleLogout = async () => {
    await logout();
    router.push('/login');
  };

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gray-50 p-8">
        <Card className="max-w-2xl mx-auto">
          <CardHeader>
            <CardTitle>Welcome Back!</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-gray-600 mb-4">
              Logged in as: {user?.email}
            </p>
            <Button
              onClick={handleLogout}
              variant="outline"
              disabled={isLoading}
            >
              Sign Out
            </Button>
          </CardContent>
        </Card>
      </div>
    </ProtectedRoute>
  );
}
```

---

## Common Patterns

### Redirect After Login
```tsx
const router = useRouter();

const onSubmit = async (data) => {
  await login(data);
  router.push('/dashboard'); // or any protected route
};
```

### Conditional Rendering Based on Auth
```tsx
const { isAuthenticated, isLoading } = useAuth();

if (isLoading) {
  return <LoadingSkeleton />;
}

return isAuthenticated ? (
  <AuthenticatedView />
) : (
  <UnauthenticatedView />
);
```

### Check Auth Status
```tsx
const { user, isAuthenticated } = useAuth();

useEffect(() => {
  if (!isAuthenticated) {
    // User is not logged in
    router.push('/login');
  }
}, [isAuthenticated]);
```

---

## Troubleshooting

### Issue: "Module not found" for useAuth
**Solution**: Use relative import path from `frontend/hooks/use-auth.ts`:
```tsx
import { useAuth } from '../../../hooks/use-auth';
```

### Issue: Validation errors not showing
**Solution**: Ensure you're using `FormMessage` component:
```tsx
<FormField>
  {/* ... */}
  <FormMessage /> {/* This displays validation errors */}
</FormField>
```

### Issue: Session not persisting
**Solution**: Check that BetterAuthProvider is wrapping your app in layout.tsx:
```tsx
<BetterAuthProvider>
  <Providers>{children}</Providers>
</BetterAuthProvider>
```

### Issue: Redirect loop
**Solution**: Make sure auth routes (/login, /register) are NOT wrapped with ProtectedRoute.

---

## Best Practices

1. **Always use ProtectedRoute** for pages requiring authentication
2. **Check isLoading** before rendering auth-dependent UI
3. **Clear errors** when user starts typing (use `clearError()`)
4. **Provide user feedback** during async operations (loading states)
5. **Handle errors gracefully** with user-friendly messages
6. **Use TypeScript types** from validation schemas for type safety

---

## Reference Links

- Better Auth Docs: https://better-auth.com
- ShadCN UI: https://ui.shadcn.com
- React Hook Form: https://react-hook-form.com
- Zod Validation: https://zod.dev
- Framer Motion: https://www.framer.com/motion
