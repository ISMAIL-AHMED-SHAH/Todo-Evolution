# Phase 3 Authentication UI - Architecture Diagram

## Component Hierarchy

```
RootLayout (app/layout.tsx)
│
├── BetterAuthProvider ✨ NEW
│   │
│   └── Providers (QueryClient + UserProviderWrapper)
│       │
│       ├── Header (existing)
│       │
│       ├── Children (page content)
│       │
│       └── Toaster ✨ NEW
│
└── Authentication Flow

```

## Route Structure

```
App Routes
│
├── (auth) Group ✨ NEW - No navbar, centered layout
│   │
│   ├── /login
│   │   └── LoginForm Component ✨ NEW
│   │       ├── React Hook Form
│   │       ├── Zod Validation (loginSchema)
│   │       ├── Better Auth (authClient.signIn.email)
│   │       └── Framer Motion (pageVariants)
│   │
│   └── /register
│       └── RegisterForm Component ✨ NEW
│           ├── React Hook Form
│           ├── Zod Validation (registerSchema)
│           ├── Better Auth (authClient.signUp.email)
│           └── Framer Motion (pageVariants)
│
└── Protected Routes
    │
    └── /dashboard (example) ✨ NEW
        └── ProtectedRoute Wrapper ✨ NEW
            ├── Auth Check (useAuth hook)
            ├── Redirect to /login if not authenticated
            ├── Loading Skeleton
            └── Render children when authenticated
```

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    User Interaction                         │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   LoginForm / RegisterForm                  │
│  • React Hook Form collects input                          │
│  • Zod validates data (loginSchema / registerSchema)       │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      useAuth Hook                           │
│  • login({ email, password })                              │
│  • register({ email, password })                           │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  Better Auth Client                         │
│  • authClient.signIn.email()                               │
│  • authClient.signUp.email()                               │
│  • Returns JWT token + session                             │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   Backend API                               │
│  • POST /api/auth/sign-in                                  │
│  • POST /api/auth/sign-up                                  │
│  • Validates credentials                                    │
│  • Returns user + JWT token                                │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  Session Storage                            │
│  • localStorage.setItem('auth_token', token)               │
│  • useAuth updates state (user, isAuthenticated)           │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      Redirect                               │
│  • router.push('/dashboard')                               │
│  • User accesses protected content                          │
└─────────────────────────────────────────────────────────────┘
```

## Authentication State Management

```
┌─────────────────────────────────────────────────────────────┐
│                      useAuth Hook                           │
│  (hooks/use-auth.ts)                                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  STATE:                                                     │
│  • user: User | null                                       │
│  • isAuthenticated: boolean                                │
│  • isLoading: boolean                                      │
│  • error: string | null                                    │
│                                                             │
│  ACTIONS:                                                   │
│  • login(credentials)      ──▶ Better Auth signIn         │
│  • register(input)         ──▶ Better Auth signUp         │
│  • logout()                ──▶ Better Auth signOut        │
│  • refreshSession()        ──▶ Reload session data        │
│  • clearError()            ──▶ Clear error state          │
│                                                             │
│  EFFECTS:                                                   │
│  • Load session on mount                                   │
│  • Auto-refresh every 5 minutes                            │
│  • Store JWT in localStorage                               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              Components using useAuth                       │
│                                                             │
│  • LoginForm          ──▶ login()                          │
│  • RegisterForm       ──▶ register()                       │
│  • ProtectedRoute     ──▶ isAuthenticated, isLoading       │
│  • Dashboard          ──▶ user, logout()                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Form Validation Flow

```
┌─────────────────────────────────────────────────────────────┐
│                  User Input (Form)                          │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              React Hook Form (Client-side)                  │
│  • useForm with zodResolver                                │
│  • Real-time validation on blur/change                     │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   Zod Schema Validation                     │
│                                                             │
│  loginSchema:                                              │
│  • email: required, valid format                           │
│  • password: required, min 8 chars                         │
│                                                             │
│  registerSchema:                                           │
│  • email: required, valid format, max 255                  │
│  • password: required, min 8, uppercase, lowercase, number │
│  • confirmPassword: must match password                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                            │
                            ├─── VALID ──────────────────────────┐
                            │                                     │
                            └─── INVALID                          │
                                      │                           │
                                      ▼                           ▼
                            ┌──────────────────┐    ┌──────────────────┐
                            │ Display Errors   │    │ Submit to API    │
                            │ (FormMessage)    │    │ (Better Auth)    │
                            └──────────────────┘    └──────────────────┘
```

## Protected Route Flow

```
┌─────────────────────────────────────────────────────────────┐
│          User Navigates to Protected Route                  │
│          (e.g., /dashboard)                                 │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  ProtectedRoute Component                   │
│  • Wraps page content                                      │
│  • Checks authentication status                             │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    useAuth Hook                             │
│  • isAuthenticated: boolean                                │
│  • isLoading: boolean                                      │
└─────────────────────────────────────────────────────────────┘
                            │
                ┌───────────┴───────────┐
                │                       │
                ▼                       ▼
    ┌────────────────────┐  ┌────────────────────┐
    │   isLoading=true   │  │  isLoading=false   │
    └────────────────────┘  └────────────────────┘
                │                       │
                ▼                       │
    ┌────────────────────┐             │
    │ Show Skeleton      │             │
    │ Loading State      │             │
    └────────────────────┘             │
                                       │
                        ┌──────────────┴──────────────┐
                        │                             │
                        ▼                             ▼
            ┌──────────────────┐        ┌──────────────────┐
            │ isAuthenticated  │        │    Not           │
            │    = true        │        │ Authenticated    │
            └──────────────────┘        └──────────────────┘
                        │                             │
                        ▼                             ▼
            ┌──────────────────┐        ┌──────────────────┐
            │ Render Children  │        │ Redirect to      │
            │ (Page Content)   │        │ /login           │
            └──────────────────┘        └──────────────────┘
```

## UI Component Dependencies

```
┌─────────────────────────────────────────────────────────────┐
│                  Auth Components (NEW)                      │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ LoginForm    │  │ RegisterForm │  │ Protected    │
│              │  │              │  │ Route        │
└──────────────┘  └──────────────┘  └──────────────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              ShadCN UI Components (Existing)                │
├─────────────────────────────────────────────────────────────┤
│  • Button          • Form           • Input                │
│  • Label           • Alert          • Skeleton             │
│  • Card            • Toast/Toaster                         │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ React Hook   │  │ Framer       │  │ Better       │
│ Form         │  │ Motion       │  │ Auth         │
│              │  │              │  │              │
│ • useForm    │  │ • motion.div │  │ • authClient │
│ • zodResolver│  │ • variants   │  │ • signIn     │
│              │  │              │  │ • signUp     │
└──────────────┘  └──────────────┘  └──────────────┘
```

## File Import Relationships

```
LoginForm.tsx
├── @/hooks/use-auth              (Better Auth hook)
├── @/lib/validations             (loginSchema)
├── @/lib/animations              (pageVariants)
├── @/components/ui/button        (ShadCN Button)
├── @/components/ui/form          (ShadCN Form)
├── @/components/ui/input         (ShadCN Input)
├── @/components/ui/alert         (ShadCN Alert)
├── lucide-react                  (Loader2 icon)
├── react-hook-form               (useForm)
├── @hookform/resolvers/zod       (zodResolver)
└── framer-motion                 (motion)

RegisterForm.tsx
├── @/hooks/use-auth              (Better Auth hook)
├── @/lib/validations             (registerSchema)
├── @/lib/animations              (pageVariants)
├── @/components/ui/button
├── @/components/ui/form
├── @/components/ui/input
├── @/components/ui/alert
├── lucide-react
├── react-hook-form
├── @hookform/resolvers/zod
└── framer-motion

ProtectedRoute.tsx
├── @/hooks/use-auth              (useAuth hook)
├── @/components/ui/skeleton      (ShadCN Skeleton)
└── next/navigation               (useRouter)
```

## Color System

```
┌─────────────────────────────────────────────────────────────┐
│                     Color Palette                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Primary (Teal):                                           │
│  • bg-teal-600     #14b8a6  ──▶ Buttons, links            │
│  • hover:bg-teal-700 #0f766e  ──▶ Hover states            │
│                                                             │
│  Background:                                                │
│  • from-teal-50 to-blue-50    ──▶ Auth layout gradient    │
│  • bg-gray-50                 ──▶ Dashboard background     │
│  • bg-white                   ──▶ Card backgrounds         │
│                                                             │
│  Text:                                                      │
│  • text-gray-900              ──▶ Headings                 │
│  • text-gray-600              ──▶ Body text                │
│  • text-gray-500              ──▶ Muted text               │
│                                                             │
│  States:                                                    │
│  • destructive (red)          ──▶ Error alerts             │
│  • opacity-50 disabled        ──▶ Disabled elements        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Animation Timeline

```
┌─────────────────────────────────────────────────────────────┐
│               Form Animation (pageVariants)                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Initial (0ms):                                            │
│  • opacity: 0                                              │
│  • y: 20px (slide from below)                             │
│                                                             │
│           │                                                 │
│           ▼  (300ms ease-out)                              │
│                                                             │
│  Animate (300ms):                                          │
│  • opacity: 1                                              │
│  • y: 0                                                    │
│                                                             │
│           │                                                 │
│           ▼  (on exit, 200ms ease-in)                      │
│                                                             │
│  Exit (200ms):                                             │
│  • opacity: 0                                              │
│  • y: -20px (slide up)                                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Summary

This architecture provides:

✅ **Separation of Concerns**
   - Auth logic (useAuth hook)
   - UI components (LoginForm, RegisterForm)
   - Route protection (ProtectedRoute)
   - Layout structure ((auth) route group)

✅ **Type Safety**
   - TypeScript throughout
   - Zod schema validation
   - Better Auth type definitions

✅ **User Experience**
   - Smooth animations (Framer Motion)
   - Clear loading states
   - User-friendly error messages
   - Responsive design

✅ **Developer Experience**
   - Clean imports with path aliases
   - Reusable components
   - Consistent patterns
   - Well-documented code

✅ **Security**
   - JWT token authentication
   - Password strength validation
   - Protected route enforcement
   - Secure session management
