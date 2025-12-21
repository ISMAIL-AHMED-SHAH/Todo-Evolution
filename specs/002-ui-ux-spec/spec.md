# Feature Specification: ToDoneAI UI/UX - Phase 2

**Feature Branch**: `002-ui-ux-spec`
**Created**: 2025-12-13
**Last Updated**: 2025-12-20
**Status**: Implemented & Production-Ready
**Input**: User description: "Generate a complete UI/UX specification for Phase-2 of the Todo Web App, with design inspired by the provided screenshot"

## Implementation Updates (2025-12-20)

### Critical Bug Fixes

#### Task Persistence Across Navigation (CRITICAL FIX)
**Problem**: Tasks were disappearing when navigating between Dashboard, Tasks, and Profile pages.

**Root Cause**:
- Two authentication systems running simultaneously (UserContext + useAuth hook)
- During navigation, `loadSession()` effect caused `user` to become `null` temporarily
- `useUserId()` returned `null` during auth reload
- React Query cache key changed from `['tasks', 'list', userId, undefined]` to `['tasks', 'list', null, undefined]`
- Different cache key = different cache = tasks appeared to "disappear"

**Solution Implemented**:
1. **Stable userId Hook** (`hooks/use-auth.ts`):
   - Modified `useUserId()` to cache userId in localStorage
   - Returns cached userId during auth reload instead of `null`
   - Prevents React Query cache key changes during navigation
   - Clears cached userId only on explicit logout

2. **Enhanced React Query Configuration** (`providers/Providers.tsx`):
   - Increased `gcTime` from 10 to 30 minutes (prevents premature cache garbage collection)
   - Disabled `refetchOnWindowFocus` (stops unnecessary refetches on tab switch)
   - Disabled `refetchOnMount` (uses cache if data is fresh)
   - Added `placeholderData: (previousData) => previousData` (keeps data during refetch)

**Impact**:
- ✅ Tasks now persist across all page navigation
- ✅ No more "disappearing tasks" when switching pages
- ✅ Completed tasks stay visible (don't get filtered out)
- ✅ Better performance with fewer unnecessary API calls

#### Authentication Form Visibility (CRITICAL FIX)
**Problem**: Input text appeared white on white background in light mode, making it unreadable.

**Root Cause**: Base Input component used `bg-transparent` with default text colors.

**Solution**:
- Added explicit styling to LoginForm and RegisterForm components
- Applied `bg-white dark:bg-gray-700` for proper backgrounds
- Set text colors: `text-gray-900 dark:text-white`
- Fixed placeholder colors: `placeholder:text-gray-500 dark:placeholder:text-gray-400`

**Impact**:
- ✅ All auth form inputs are now readable in both light and dark modes
- ✅ Proper visual hierarchy and accessibility

### Task Form UX Refinements

#### Professional Scrolling with shadcn ScrollArea
**Implementation**:
- Installed `@radix-ui/react-scroll-area` and shadcn `ScrollArea` component
- Replaced basic `overflow-y-auto` with accessible ScrollArea
- Proper scroll indicators and touch-friendly scrolling on mobile

**Modal Improvements**:
- **Height Management**:
  - Mobile: `h-[95vh]` (fixed height for consistent button visibility)
  - Desktop: `sm:h-auto sm:max-h-[90vh]` (adaptive height)
- **Responsive Padding**: `px-5 sm:px-6` and `py-4 sm:py-5`
- **Improved Width**: `w-[calc(100%-1.5rem)]` on mobile for better screen utilization

#### Consistent Form Field Spacing
**All Form Fields Updated**:
- Uniform `space-y-2` spacing within each FormItem
- Consistent height for inputs: `h-11` (44px touch-friendly)
- Improved FormDescription styling with `mt-1.5` for breathing room
- Responsive font sizes: `text-lg sm:text-xl md:text-2xl` for title

**Specific Field Updates**:
- **Title**: `h-11`, concise description
- **Description**: `min-h-[100px]`, cleaner placeholder
- **Priority**: `h-11` for SelectTrigger
- **Categories**: Updated CategoryInput with consistent height and dark mode badges
- **Due Date**: `h-11` for date picker button

#### Smart Action Buttons
**Always Accessible Design**:
- **Sticky Positioning**: `sticky bottom-0` with background to stay visible
- **Mobile-First Ordering**: `flex-col-reverse` puts primary "Create Task" button on top
- **Desktop Layout**: `sm:flex-row` for side-by-side buttons
- **Larger Touch Targets**: `min-h-[48px]` on mobile, `sm:min-h-[44px]` on desktop
- **Visual Hierarchy**: Primary button has `font-semibold`
- **Clear Separation**: `pt-6 mt-2 border-t` creates distinct action area

### Tasks Page Complete Redesign

#### New Tabbed Interface
**Three Views**:
1. **All Tasks** - View all tasks at once
2. **Pending** - Focus on active tasks only
3. **Completed** - Review finished work

**Tab Features**:
- Dynamic counts: `All (15)`, `Pending (8)`, `Completed (7)`
- Active state styling with white/dark backgrounds
- Smooth tab switching animations

#### Rich Task Card Design
**Each Task Card Displays**:
- **Status Icon** - Clickable circle/checkmark to toggle complete/pending
- **Title & Description** - Strikethrough styling for completed tasks
- **Priority Badge** - Color-coded (Red=High, Orange=Medium, Green=Low)
- **Due Date Badge** - Overdue shown in red, upcoming in blue
- **Status Badge** - Completed (green) or Pending (gray)
- **Categories** - Tag icons with first 3 visible + count for more
- **Created Date** - With clock icon showing creation date
- **Action Buttons** - Edit and Delete with hover color changes

**Visual Design**:
- **Hover Effects**: Border changes to teal, shadow appears on hover
- **Completed Styling**: 75% opacity, gray border for completed tasks
- **Overdue Indicator**: Red badge for past-due tasks
- **Responsive Grid**: 1 column mobile → 2 tablet → 3 desktop
- **Staggered Animation**: Cards animate in with progressive delay
- **Empty States**: Beautiful placeholders for each tab ("No tasks yet", "All caught up!", "No completed tasks")

**Dark Mode Support**:
- Full dark mode styling for all card elements
- Background colors: `bg-gray-800`, `bg-gray-700`
- Text colors: `text-white`, `text-gray-300`, `text-gray-400`
- Border colors: `border-gray-600`, `border-gray-700`
- All badges have dark variants with proper contrast
- Button hover states adapted for dark theme

#### Task List Replacement
**Decision**: Replaced the old TaskList component with card-based tabbed interface because:
- Cards display more information per task without scrolling
- More visually appealing and modern
- Better responsive behavior on mobile
- Easier to scan and interact with
- Aligns with modern task management UI patterns

### React Query Cache Improvements

**Configuration Updates** (`providers/Providers.tsx`):
```typescript
{
  staleTime: 5 * 60 * 1000,        // 5 minutes (unchanged)
  gcTime: 30 * 60 * 1000,          // 30 minutes (increased from 10)
  retry: 1,                         // 1 retry (unchanged)
  refetchOnWindowFocus: false,     // Disabled (was production-only)
  refetchOnMount: false,           // Disabled (new)
  placeholderData: (prev) => prev  // Keep previous data (new)
}
```

**Cache Key Consistency** (`hooks/use-task-mutations.ts`):
- All mutations now explicitly use `taskQueryKeys.list(userId, undefined)`
- Prevents cache misses when filters parameter is omitted
- Ensures create, update, delete, and toggle mutations target correct cache entry

### Component Additions

**New shadcn Components**:
- `src/components/ui/scroll-area.tsx` - Accessible scrolling
- `src/components/ui/tabs.tsx` - Tabbed interface
- `src/components/ui/separator.tsx` - Visual separators

**Dependencies Added**:
- `@radix-ui/react-scroll-area` - Scroll area primitive
- `date-fns` - Date formatting (already present, used for overdue detection)

### Technical Debt Addressed

**useState Caching Strategy**:
- Product decision: Use localStorage for userId caching
- Safe because: Only stores numeric ID (not sensitive data)
- Automatically cleared on logout
- Prevents React Query cache misses during auth state transitions
- Standard practice for client-side state persistence

**React Query Best Practices**:
- Prioritized user experience (no disappearing data)
- Balanced performance (fewer network requests)
- Maintained data freshness (5-minute stale time)
- Conservative approach to cache retention

## Implementation Updates (2025-12-19)

### Branding
- **Application Name**: Rebranded from "Todo App" to "ToDoneAI"
- **Navbar Logo**: Updated to display "ToDoneAI" in top-left
- **Page Title**: Changed to "ToDoneAI - Smart Task Management"
- **Description**: Updated to include "AI-powered features" for future expansion

### Theme System
- **Dark Mode**: Full dark mode implementation with theme toggle
- **Theme Toggle**: Sun/Moon icon button in navbar (desktop and mobile)
- **Persistence**: Theme preference saved to localStorage
- **System Preference**: Respects OS dark mode setting as fallback
- **Coverage**: All components support dark mode (dashboard, forms, modals, profile, navbar)
- **Color Scheme**:
  - Dark backgrounds: `bg-gray-900`, `bg-gray-800`, `bg-gray-700`
  - Dark text: `text-white`, `text-gray-200`, `text-gray-300`, `text-gray-400`
  - Dark borders: `border-gray-700`, `border-gray-600`
  - Accent colors adjusted for dark mode: `dark:text-teal-400`, `dark:bg-teal-900`

### Dashboard UX
- **Stats Cards**: Replaced action cards with 5 statistical insight cards:
  1. **Total Tasks**: Blue icon - shows total task count
  2. **Completed**: Green checkmark - shows completed count
  3. **Pending**: Orange circle - shows pending count
  4. **Completion Rate**: Purple trending icon - shows completion percentage
  5. **High Priority**: Red alert icon - shows urgent pending tasks
- **Layout**: Responsive grid (1 column mobile → 2 columns tablet → 5 columns desktop)
- **Animation**: Staggered entrance animations using Framer Motion
- **Add Task Button**: Prominent teal button in header (replaces action card)
- **Progress Bar**: Visual completion progress below stats cards
- **Task List**: Full task list with CRUD controls on same page

### Task Modal UX
- **Modal Structure**: Fixed header with scrollable form content
- **Header**: "Create New Task" or "Edit Task" title with description
- **Sizing**:
  - Mobile: `w-[calc(100%-2rem)]` (comfortable 1rem margins)
  - Desktop: `max-w-[600px]`, `max-h-[90vh]`
- **Scrolling**: Form content scrollable with buttons always accessible
- **Submit Button**: Always visible "Create Task" or "Save Changes" primary action
- **Dark Mode**: Full dark theme support for modal and all form inputs

### Task Creation Flow
- **User Feedback**: Toast notifications for all CRUD operations:
  - Success: "Task '{title}' created successfully!" (green toast, 5s)
  - Update: "Task '{title}' updated successfully!" (green toast, 5s)
  - Delete: "Task deleted successfully!" (green toast, 5s)
  - Error: Descriptive error messages (red toast, 7s)
- **State Management**: Optimistic updates via React Query
- **Form Reset**: Form clears after successful creation
- **Modal Behavior**: Closes automatically on success

### Form Dark Mode Support
All form inputs fully support dark mode:
- Input fields: `dark:bg-gray-700`, `dark:text-white`, `dark:border-gray-600`
- Labels: `dark:text-white`, `dark:text-gray-200`
- Descriptions: `dark:text-gray-400`
- Select dropdowns: Dark background and text
- Date picker: Dark calendar popover
- Buttons: Proper dark mode styling
- Separators: `dark:bg-gray-700`

### Profile Page Dark Mode
- Header icons and text with dark variants
- Card backgrounds: `dark:bg-gray-800`
- All input fields with dark mode support
- Labels and descriptions with proper contrast
- Account information section with dark text colors
- Border separators with dark variants

### Technical Implementation Details
- **State Management**: React Query for caching and optimistic updates
- **Form Validation**: React Hook Form with Zod schemas
- **Animations**: Framer Motion for all page and modal transitions
- **Responsive Design**: Mobile-first approach with Tailwind breakpoints
- **Accessibility**: Proper ARIA labels, keyboard navigation, focus states
- **Performance**: Skeleton loaders, optimistic UI updates, efficient re-renders

## User Scenarios & Testing *(mandatory)*

### User Story 1 - User Authentication Journey (Priority: P1) *(Updated 2025-12-20)*

Users need to securely register and log into the Todo application to access their personal task management dashboard, with clearly visible and accessible form inputs in both light and dark modes.

**Why this priority**: Authentication is the foundation for all user-specific features. Without login/register, users cannot access any task management functionality. The input visibility fix ensures users can actually read what they're typing in both themes, which is critical for successful authentication.

**Independent Test**: Can be fully tested by: (1) viewing the register/login forms in both light and dark modes and verifying input text is readable, (2) creating a new account, (3) logging in with credentials, (4) verifying session persistence across page refreshes and navigation between pages, (5) logging out successfully. Delivers secure, accessible user access to the application.

**Acceptance Scenarios**:

1. **Given** a new user visits the application, **When** they navigate to the register page and submit valid registration details (email, password), **Then** their account is created and they are redirected to the dashboard
2. **Given** an existing user visits the login page, **When** they enter valid credentials and submit, **Then** they are authenticated and redirected to their dashboard with their session active
3. **Given** an authenticated user, **When** they refresh the page or navigate between pages, **Then** their session persists and they remain logged in (userId cached in localStorage during auth reload)
4. **Given** an authenticated user, **When** they click the "Sign Out" button, **Then** their session is terminated, cached userId is cleared, and they are redirected to the login page
5. **Given** a user enters invalid credentials on login, **When** they submit the form, **Then** they see a clear error message and remain on the login page
6. **Given** a user enters an already-registered email on register page, **When** they submit, **Then** they see an error message indicating the email is already in use
7. **Given** a user views the login or register form in light mode, **When** they type in the email or password fields, **Then** the text is clearly visible with dark gray text on white background (not white on white)
8. **Given** a user views the login or register form in dark mode, **When** they type in the email or password fields, **Then** the text is clearly visible with white text on dark gray background
9. **Given** a user focuses on an input field in the auth forms, **When** they observe the field, **Then** it has proper border highlighting and the placeholder text is visible with appropriate contrast

---

### User Story 2 - Dashboard Overview and Task Management (Priority: P2)

Users need a comprehensive dashboard that provides statistical insights about their tasks and enables full task management (view, create, edit, delete, complete) from a single page.

**Why this priority**: The dashboard is the primary work surface where users spend most of their time. Showing statistics at-a-glance and providing immediate access to task management creates an efficient, modern user experience.

**Independent Test**: Can be tested by logging in and verifying all statistics display correctly, the "Add Task" button opens a modal, task list shows all tasks with proper controls, and all CRUD operations work seamlessly. Delivers a complete, unified task management experience.

**Acceptance Scenarios**:

1. **Given** an authenticated user lands on the dashboard, **When** the page loads, **Then** they see the page title "Dashboard", welcome message, and an "Add Task" button in the header
2. **Given** a user views the dashboard, **When** they observe the statistics section, **Then** they see 5 cards displaying: Total Tasks, Completed, Pending, Completion Rate (%), and High Priority count
3. **Given** a user has completed some tasks, **When** they view the statistics, **Then** the completion rate card shows the accurate percentage and all counts are correct
4. **Given** a user clicks the "Add Task" button, **When** the action executes, **Then** a centered modal opens displaying the task creation form with all fields and visible submit button
5. **Given** a user views their task list on the dashboard, **When** they observe the tasks, **Then** each task displays with a checkbox, edit button, delete button, and all task metadata
6. **Given** a user clicks edit on a task, **When** the modal opens, **Then** the form is pre-filled with the task's current data
7. **Given** a user toggles a task's completion checkbox, **When** the action completes, **Then** the statistics cards and progress bar update immediately to reflect the new state
8. **Given** a user deletes a task, **When** they confirm the action, **Then** the task is removed from the list and statistics update accordingly

---

### User Story 3 - Task List Display and Management (Priority: P3) *(Updated 2025-12-20)*

Users need to view all their tasks in a beautiful tabbed card interface with visual indicators for status, priority, categories, and dates, with the ability to filter by status and toggle completion directly from cards.

**Why this priority**: The task list is the core data view where users spend most of their time reviewing and managing tasks. The new tabbed card interface provides superior organization, visual clarity, and quick status updates while being more visually appealing and easier to scan.

**Independent Test**: Can be tested by navigating to the task list page and verifying: (1) three tabs appear (All, Pending, Completed) with dynamic counts, (2) all tasks display as rich cards with complete information, (3) the progress bar accurately reflects completion ratio, (4) clicking status icons toggles task completion, (5) tasks persist across tab switches. Delivers full task visibility, filtering, and quick completion management.

**Acceptance Scenarios**:

1. **Given** a user navigates to the task list page, **When** the page loads, **Then** they see a page title "My Tasks" with subtitle, a progress bar, and three tabs labeled "All (X)", "Pending (X)", "Completed (X)" with accurate counts
2. **Given** a user views the "All" tab, **When** they observe the task cards, **Then** each task displays as a card in a responsive grid (1 col mobile, 2 tablet, 3 desktop) showing: clickable status icon, title, description, priority badge, due date badge (with overdue indicator), status badge, up to 3 category tags with count, created date, and Edit/Delete buttons
3. **Given** a user clicks the "Pending" tab, **When** the tab activates, **Then** only incomplete tasks are shown in the card grid, and if empty, a "All caught up!" empty state is displayed
4. **Given** a user clicks the "Completed" tab, **When** the tab activates, **Then** only completed tasks are shown with 75% opacity and strikethrough titles, and if empty, a "No completed tasks" empty state is displayed
5. **Given** a user has completed some tasks, **When** they view the task list, **Then** a progress bar displays at the top showing "X of Y completed" with visual progress
6. **Given** a user clicks a task's status icon (circle/checkmark), **When** the action completes, **Then** the task's completion status toggles, the card updates styling (opacity, strikethrough), tab counts update, and the progress bar reflects the new count
7. **Given** a user views a completed task card, **When** they observe it, **Then** the title has strikethrough text, the card has 75% opacity, a green "Completed" badge is shown, and a checkmark icon is displayed
8. **Given** a user has no tasks, **When** they view any tab, **Then** they see an appropriate empty state message with an icon encouraging them to create their first task
9. **Given** a user hovers over a pending task card, **When** they move their mouse over it, **Then** the card border changes to teal and a shadow appears
10. **Given** a user views a task with a past due date, **When** the task is not completed, **Then** the due date badge is displayed in red with "overdue" styling
11. **Given** a user clicks the "Edit" button on a task card, **When** the action executes, **Then** the edit modal opens with the form pre-filled with the task's data
12. **Given** a user clicks the "Delete" button on a task card, **When** they confirm the action, **Then** the task is removed from the list, tab counts update, and the progress bar updates
13. **Given** a user navigates between Dashboard and Tasks page, **When** they return to Tasks, **Then** all tasks remain visible and no tasks have disappeared (persistence bug fixed)

---

### User Story 4 - Task Creation (Priority: P4) *(Updated 2025-12-20)*

Users need to create new tasks by filling out a professional, accessible form that captures all task details including title, description, priority, category/tags, and due date, with smooth scrolling and always-visible action buttons.

**Why this priority**: Task creation is the primary data entry point. The improved form UX with shadcn ScrollArea, consistent spacing, and mobile-optimized buttons ensures users can add tasks efficiently on any device without UX frustrations like invisible buttons or awkward scrolling.

**Independent Test**: Can be tested by clicking "Add Task" button on dashboard, filling out the creation form on both mobile and desktop, scrolling through all fields, verifying buttons are always accessible at the bottom, submitting, and confirming the new task appears in the task list with all entered details. Delivers production-ready task creation capability.

**Acceptance Scenarios**:

1. **Given** a user clicks the "Add Task" button on the dashboard, **When** the modal opens, **Then** they see a modal with title "Create New Task", subtitle text, and a form with shadcn ScrollArea containing fields for: task title (required, h-11), description (optional, min-h-100px), priority selector (h-11), category/tags input (h-11), and due date picker (h-11)
2. **Given** a user views the task creation form on a small mobile screen, **When** they scroll through the form, **Then** the form content scrolls smoothly with proper scroll indicators, and the "Create Task" and "Cancel" buttons remain visible and accessible at the bottom via sticky positioning
3. **Given** a user fills out the task creation form with valid data, **When** they submit, **Then** the task is created via optimistic update, the modal closes automatically, the form resets to default values, and they see a green success toast: "Task '{title}' created successfully!"
4. **Given** a user submits the task creation form with an empty title, **When** validation runs, **Then** they see an error message "Title is required" below the title field and the form does not submit
5. **Given** a user fills out the task creation form, **When** they submit successfully, **Then** they can navigate to the task list and see their new task displayed immediately with all entered details (no disappearing due to cache bug)
6. **Given** a user is filling out the task creation form, **When** they click the "Cancel" button, **Then** the modal closes without creating a task and no data is saved
7. **Given** a user views the modal on mobile, **When** they observe the button layout, **Then** the "Create Task" button is positioned at the top (mobile-first ordering with flex-col-reverse) with min-h-48px for easy thumb access
8. **Given** a user adds category tags, **When** they type and press Enter, **Then** category badges appear with full dark mode support (blue background, proper contrast) and show "X/10" count
9. **Given** a user selects a priority, **When** they open the priority dropdown, **Then** they see High (red), Medium (orange), and Low (green) options with color indicators
10. **Given** a user picks a due date, **When** they click the date picker, **Then** a calendar popover opens with dark mode support and allows date selection

---

### User Story 5 - Task Editing (Priority: P5)

Users need to update existing tasks by opening an edit modal pre-filled with current task data and modifying any field.

**Why this priority**: Tasks often need updates as circumstances change. Users must be able to modify task details to keep their task list accurate and relevant.

**Independent Test**: Can be tested by selecting a task from the list, opening the edit modal, modifying fields, saving, and verifying the task list reflects the updated information. Delivers complete task editing capability.

**Acceptance Scenarios**:

1. **Given** a user clicks "Update Task" or clicks on a specific task in the list, **When** the edit modal opens, **Then** the form is pre-filled with the task's current title, description, priority, category/tags, and due date
2. **Given** a user modifies fields in the edit form and submits, **When** the save action completes, **Then** the task is updated, the modal closes, and the task list reflects the new values
3. **Given** a user clears the title field in the edit form, **When** they try to submit, **Then** they see an error message "Title is required" and the form does not submit
4. **Given** a user is editing a task, **When** they click "Cancel", **Then** the modal closes without saving changes and the task retains its original values

---

### User Story 6 - Profile and Settings Management (Priority: P6)

Users need to view and update their profile information and application preferences.

**Why this priority**: While not immediately critical for task management, profile and settings provide important account management functionality and improve long-term user experience.

**Independent Test**: Can be tested by navigating to the profile/settings page, viewing current user information, updating preferences, and verifying changes are saved. Delivers user account management capability.

**Acceptance Scenarios**:

1. **Given** an authenticated user clicks on their profile/settings link in the navbar, **When** the page loads, **Then** they see their current email address and any profile settings
2. **Given** a user updates their profile information, **When** they save changes, **Then** the updates are persisted and they see a success confirmation message
3. **Given** a user wants to change their password, **When** they fill out the password change form with current password and new password, **Then** their password is updated and they remain logged in

---

### Edge Cases

- What happens when a user tries to create a task with a past due date? (Allow but display a warning indicator)
- How does the system handle very long task titles or descriptions? (Truncate display with "..." and show full text on hover or in modal)
- What happens when a user loses internet connection while filling out a form? (Show offline indicator and preserve form data locally)
- How does the system handle special characters or emojis in task titles/descriptions? (Accept and display all valid UTF-8 characters)
- What happens when a user has hundreds of tasks? (Implement pagination or infinite scroll on task list page)
- How does the system handle rapid clicking on toggle completion checkbox? (Debounce requests to prevent duplicate API calls)
- What happens when a user tries to access a protected route without being logged in? (Redirect to login page with return URL preserved)
- How does the system handle expired JWT tokens? (Detect expiration, clear session, redirect to login with message "Session expired, please log in again")

## Requirements *(mandatory)*

### Functional Requirements

#### Authentication & Session Management

- **FR-001**: System MUST provide a registration page with email and password fields and a submit button
- **FR-002**: System MUST validate email format on registration and login forms before submission
- **FR-003**: System MUST validate password strength on registration (minimum 8 characters)
- **FR-004**: System MUST provide a login page with email and password fields and a submit button
- **FR-005**: System MUST authenticate users using Better Auth with JWT token generation
- **FR-006**: System MUST store JWT tokens securely in the browser (httpOnly cookies or secure localStorage)
- **FR-007**: System MUST attach JWT tokens to all authenticated API requests
- **FR-008**: System MUST restore user sessions automatically when returning to the application with valid tokens
- **FR-009**: System MUST provide a "Sign Out" button that terminates the session and clears JWT tokens
- **FR-010**: System MUST redirect unauthenticated users to the login page when accessing protected routes
- **FR-011**: System MUST display clear error messages for invalid credentials on login
- **FR-012**: System MUST display clear error messages for registration failures (e.g., duplicate email)

#### Dashboard & Navigation

- **FR-013**: System MUST display a navigation bar at the top of all authenticated pages showing "ToDoneAI" logo, theme toggle, navigation links, user email, and sign out button
- **FR-014**: System MUST provide a dashboard as the default landing page after login with page title "Dashboard" and welcome message "Welcome back, {email}!"
- **FR-015**: System MUST display five statistical insight cards on the dashboard: Total Tasks (blue), Completed (green), Pending (orange), Completion Rate (purple), High Priority (red)
- **FR-016**: Each statistics card MUST display an icon, label, and calculated value derived from current task data
- **FR-017**: System MUST display an "Add Task" button in the dashboard header (teal background, white text)
- **FR-018**: System MUST arrange statistics cards in a responsive grid (1 col mobile, 2 col tablet, 5 col desktop)
- **FR-019**: System MUST open the task creation modal when user clicks the "Add Task" button
- **FR-020**: System MUST display the complete task list on the dashboard page below statistics
- **FR-021**: System MUST display a progress bar showing "X of Y tasks completed" with visual fill percentage below statistics

#### Task List Display

- **FR-022**: System MUST display all user tasks on the task list page in card format
- **FR-023**: System MUST display a progress section titled "Toggle Completion Status" above the task list
- **FR-024**: System MUST display a progress bar showing "X of Y completed" with visual fill percentage
- **FR-025**: Each task card MUST display: checkbox, title, description, priority tag, category tag, due date, completion status badge, created date, and delete button
- **FR-026**: System MUST display completed tasks with strikethrough text on the title
- **FR-027**: System MUST display priority tags with color coding (e.g., High = red, Medium = orange, Low = green)
- **FR-028**: System MUST display category tags with distinct styling (e.g., work, personal, shopping)
- **FR-029**: System MUST display due dates in readable format (MM/DD/YYYY)
- **FR-030**: System MUST display completion status as a badge with text "Completed" or implied pending state
- **FR-031**: System MUST display created dates in format "Created MM/DD/YYYY"
- **FR-032**: System MUST display an empty state message when user has no tasks: "No tasks yet. Create your first task to get started!"

#### Task Actions

- **FR-033**: System MUST toggle task completion status when user clicks the checkbox on a task card
- **FR-034**: System MUST update the progress bar immediately after toggling task completion
- **FR-035**: System MUST display a confirmation dialog when user clicks the "Delete" button on a task card
- **FR-036**: System MUST remove the task from the list after user confirms deletion
- **FR-037**: System MUST update the progress bar and task count after task deletion
- **FR-038**: System MUST open an edit modal pre-filled with task data when user clicks on a task card or edit action

#### Task Creation Form

- **FR-039**: System MUST display a centered modal dialog for task creation with fixed header and scrollable form content
- **FR-040**: Modal MUST have fixed header showing "Create New Task" title and description
- **FR-041**: Modal content area MUST be scrollable (overflow-y-auto) to ensure submit button is always accessible
- **FR-042**: Form MUST contain: title input (required), description textarea (optional), priority selector, category/tags input, due date picker
- **FR-043**: System MUST validate that title field is not empty before allowing form submission
- **FR-044**: System MUST display inline error message "Title is required" when title validation fails
- **FR-045**: System MUST provide priority options: High, Medium, Low (with visual color indicators)
- **FR-046**: System MUST provide a date picker for selecting due date
- **FR-047**: System MUST allow users to add multiple category tags to a task
- **FR-048**: System MUST display visible "Create Task" primary action button at bottom of form
- **FR-049**: System MUST create the task and close the modal when user submits valid form data
- **FR-050**: System MUST display toast notification after task creation: "Task '{title}' created successfully!"
- **FR-051**: System MUST close the modal without saving when user clicks "Cancel" button or clicks outside modal
- **FR-052**: System MUST clear form fields after successful task creation
- **FR-053**: System MUST show new task immediately in the dashboard task list via optimistic update

#### Task Editing Form

- **FR-049**: System MUST display an edit modal pre-filled with current task data when user initiates edit action
- **FR-050**: System MUST allow users to modify any task field: title, description, priority, category/tags, due date
- **FR-051**: System MUST validate that title field is not empty before allowing update submission
- **FR-052**: System MUST update the task and close the modal when user submits valid changes
- **FR-053**: System MUST display a success message after task update: "Task updated successfully!"
- **FR-054**: System MUST close the modal without saving when user clicks "Cancel" button
- **FR-055**: System MUST preserve original task data when user cancels edit

#### Profile & Settings

- **FR-056**: System MUST provide a profile/settings page accessible from the navigation
- **FR-057**: System MUST display user's email address on the profile page
- **FR-058**: System MUST allow users to update their profile information
- **FR-059**: System MUST provide a password change form with current password and new password fields
- **FR-060**: System MUST validate current password before allowing password change
- **FR-061**: System MUST display success message after profile updates: "Profile updated successfully!"

#### Theme & Dark Mode

- **FR-062**: System MUST provide a theme toggle button in the navbar showing sun icon (dark mode) or moon icon (light mode)
- **FR-063**: System MUST persist theme preference to localStorage with key "theme"
- **FR-064**: System MUST apply theme preference on page load before rendering to prevent flash
- **FR-065**: System MUST fallback to system preference (prefers-color-scheme) when no localStorage value exists
- **FR-066**: Dark mode MUST apply to all components: navbar, dashboard, forms, modals, task cards, profile page
- **FR-067**: All text MUST have sufficient contrast in both light and dark modes (WCAG AA minimum)
- **FR-068**: All interactive elements MUST have visible focus states in both themes

#### UI/UX Interactive Behaviors

- **FR-069**: All page transitions MUST use Framer Motion animations (fade + slide effects, 300ms duration)
- **FR-070**: Modal open/close actions MUST use Framer Motion animations (fade + scale effects)
- **FR-071**: Statistics cards MUST have staggered entrance animations (100ms delay between cards)
- **FR-072**: Dashboard cards MUST have hover effects (subtle shadow enhancement)
- **FR-073**: All buttons MUST use ShadCN UI Button component with appropriate variants
- **FR-074**: All form inputs MUST use ShadCN UI Input component with validation states
- **FR-075**: All forms MUST use ShadCN UI Form components with React Hook Form and Zod validation
- **FR-076**: All modals/dialogs MUST use ShadCN UI Dialog component
- **FR-077**: Task cards MUST have hover effects (border highlight)
- **FR-078**: All loading states MUST display ShadCN UI Skeleton components
- **FR-079**: All error states MUST display clear error messages with ShadCN UI Alert component
- **FR-080**: All success/error feedback MUST use toast notifications (success: 5s, error: 7s)
- **FR-081**: The application MUST be fully responsive and adapt to mobile (320px+), tablet, and desktop screen sizes
- **FR-082**: The navigation bar MUST be responsive with hamburger menu on mobile devices
- **FR-083**: Dashboard statistics cards MUST stack in 1 column on mobile, 2 columns on tablet, 5 columns on desktop

### Key Entities

- **User**: Represents an authenticated user with email, password (hashed), and profile information. Related to multiple tasks through ownership.

- **Task**: Represents a todo item with title (required), description (optional), priority (High/Medium/Low), category tags (array of strings), due date (date), completion status (boolean), created date (timestamp), and user relationship (owner). Related to one user.

- **Session**: Represents an active user session with JWT token, user reference, expiration time, and authentication state. Related to one user.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can complete registration and first login in under 1 minute with 95% success rate
- **SC-002**: Users can create a new task in under 30 seconds with all fields populated
- **SC-003**: Users can toggle task completion status with a single click and see immediate visual feedback within 200ms
- **SC-004**: The application loads the dashboard within 2 seconds on standard broadband connections
- **SC-005**: All page transitions complete smoothly within 300ms with visible animations
- **SC-006**: All form validations display error messages within 100ms of user interaction
- **SC-007**: 90% of users successfully complete their first task creation without errors or confusion
- **SC-008**: The interface is fully usable on mobile devices (320px width) through desktop (1920px width)
- **SC-009**: Users can access any core feature (view, create, edit, delete tasks) within 2 clicks from the dashboard
- **SC-010**: Session restoration works correctly on 100% of page refreshes with valid tokens
- **SC-011**: Empty states, loading states, and error states provide clear guidance with 100% coverage
- **SC-012**: All interactive elements (buttons, cards, checkboxes) respond to user actions within 150ms

### User Experience Quality

- **SC-013**: Task list provides at-a-glance understanding of task status through color-coded priority tags and completion badges
- **SC-014**: Dashboard cards provide intuitive iconography matching their function (plus for add, clipboard for view, pencil for edit, etc.)
- **SC-015**: Form validation errors guide users to corrections without frustration through inline messaging
- **SC-016**: The application maintains visual consistency using the defined color palette across all pages and components

## Assumptions

1. **Color Palette**: Based on the screenshot, we assume the following color scheme:
   - Navbar: Teal/turquoise (#14b8a6 or similar)
   - Add Task card: Mint green (#a7f3d0 or similar)
   - View Tasks card: Light purple (#c4b5fd or similar)
   - Update Task card: Cream/yellow (#fde68a or similar)
   - Complete/Pending card: Light blue (#93c5fd or similar)
   - Delete Task card: Pink (#fbcfe8 or similar)
   - Priority High: Red background
   - Priority Medium: Orange background (assumed)
   - Priority Low: Green background (assumed)
   - Category tags: Purple-ish background

2. **Typography**: We assume using standard sans-serif fonts (e.g., Inter, system fonts) for readability

3. **Icons**: We assume using a standard icon library compatible with ShadCN (e.g., Lucide React icons)

4. **Date Format**: We assume MM/DD/YYYY format based on the screenshot example (12/13/2025)

5. **Task Ordering**: We assume tasks display in reverse chronological order (newest first) unless user applies custom sorting

6. **Mobile Navigation**: We assume a hamburger menu approach for mobile navigation to save space

7. **Pagination**: We assume client-side pagination or infinite scroll for task lists exceeding 50 items

8. **Animation Duration**: We assume standard animation durations (200-300ms) for Framer Motion transitions

9. **Form Auto-save**: We assume no auto-save functionality; users must explicitly submit forms

10. **Offline Support**: We assume basic offline detection but no full offline mode (Progressive Web App features may be added later)

## Technical Constraints *(informational only)*

These constraints are noted for awareness but do not belong in a business specification:

- Next.js App Router structure for file-based routing
- ShadCN UI component library for all UI components
- Tailwind CSS for styling and responsive design
- Framer Motion for animations and transitions
- Better Auth for authentication with JWT tokens
- All authenticated pages must fetch user session from Better Auth client components
- API communication uses RESTful endpoints with JSON payloads
