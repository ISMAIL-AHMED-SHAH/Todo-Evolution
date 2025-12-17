# Testing & Validation Guide: Todo App UI/UX - Phase 2

**Feature**: 002-ui-ux-spec
**Created**: 2025-12-16
**Purpose**: Comprehensive testing procedures for validating all functional requirements, success criteria, acceptance scenarios, and edge cases

## Prerequisites for Testing

Before running these tests, ensure:

1. ✅ Frontend server running at `http://localhost:3000`
2. ✅ Backend server running at `http://localhost:8000`
3. ✅ Database migrations applied (Alembic)
4. ✅ Environment variables configured correctly
5. ✅ Test user accounts available or ability to create new accounts

## Test Execution Strategy

**Recommended Order**:
1. **Acceptance Scenarios** (T151) - Validates user stories end-to-end
2. **Functional Requirements** (T152) - Validates specific features systematically
3. **Success Criteria** (T153) - Validates performance and UX quality metrics
4. **Edge Cases** (T154) - Validates boundary conditions and error handling
5. **End-to-End Journeys** (T155) - Validates complete user workflows

---

## T151: Acceptance Scenarios Validation

### User Story 1 - Authentication Journey (6 scenarios)

#### Scenario 1.1: New User Registration
**Given** a new user visits the application
**When** they navigate to the register page and submit valid registration details (email, password)
**Then** their account is created and they are redirected to the dashboard

**Test Steps**:
1. Navigate to `http://localhost:3000/register`
2. Enter email: `test_user_${timestamp}@example.com`
3. Enter password: `SecurePass123!`
4. Click "Register" button
5. Verify redirect to `/dashboard`
6. Verify dashboard displays "My Tasks" title

**✅ PASS** | **❌ FAIL** | **⚠️ BLOCKED**

---

#### Scenario 1.2: Existing User Login
**Given** an existing user visits the login page
**When** they enter valid credentials and submit
**Then** they are authenticated and redirected to their dashboard with their session active

**Test Steps**:
1. Navigate to `http://localhost:3000/login`
2. Enter email from Scenario 1.1
3. Enter password from Scenario 1.1
4. Click "Login" button
5. Verify redirect to `/dashboard`
6. Verify session cookie/token is set (check browser DevTools)

**✅ PASS** | **❌ FAIL** | **⚠️ BLOCKED**

---

#### Scenario 1.3: Session Persistence
**Given** an authenticated user
**When** they refresh the page or navigate between pages
**Then** their session persists and they remain logged in

**Test Steps**:
1. Complete Scenario 1.2 (login)
2. Press F5 to refresh page
3. Verify user remains on dashboard (not redirected to login)
4. Navigate to `/tasks` page
5. Navigate back to `/dashboard`
6. Verify user email still appears in navbar

**✅ PASS** | **❌ FAIL** | **⚠️ BLOCKED**

---

#### Scenario 1.4: User Logout
**Given** an authenticated user
**When** they click the "Sign Out" button
**Then** their session is terminated and they are redirected to the login page

**Test Steps**:
1. Complete Scenario 1.2 (login)
2. Click "Sign Out" button in navbar
3. Verify redirect to `/login`
4. Attempt to navigate to `/dashboard` directly
5. Verify redirect back to `/login` (protected route)

**✅ PASS** | **❌ FAIL** | **⚠️ BLOCKED**

---

#### Scenario 1.5: Invalid Credentials Error
**Given** a user enters invalid credentials on login
**When** they submit the form
**Then** they see a clear error message and remain on the login page

**Test Steps**:
1. Navigate to `http://localhost:3000/login`
2. Enter email: `invalid@example.com`
3. Enter password: `WrongPassword`
4. Click "Login" button
5. Verify error message displays: "Invalid credentials" or similar
6. Verify user remains on `/login` page

**✅ PASS** | **❌ FAIL** | **⚠️ BLOCKED**

---

#### Scenario 1.6: Duplicate Email Registration
**Given** a user enters an already-registered email on register page
**When** they submit
**Then** they see an error message indicating the email is already in use

**Test Steps**:
1. Complete Scenario 1.1 (create account)
2. Navigate to `/register` again
3. Enter same email from Scenario 1.1
4. Enter any password
5. Click "Register" button
6. Verify error message: "Email already in use" or similar

**✅ PASS** | **❌ FAIL** | **⚠️ BLOCKED**

---

### User Story 2 - Dashboard Overview (7 scenarios)

#### Scenario 2.1: Dashboard Loads with Action Cards
**Given** an authenticated user lands on the dashboard
**When** the page loads
**Then** they see a page title "My Tasks" with subtitle "Organize your day, achieve your goals" and five action cards

**Test Steps**:
1. Login and navigate to `/dashboard`
2. Verify page title: "My Tasks"
3. Verify subtitle: "Organize your day, achieve your goals"
4. Count action cards: should be 5
5. Verify card names: Add Task, View Tasks, Update Task, Complete/Pending, Delete Task

**✅ PASS** | **❌ FAIL** | **⚠️ BLOCKED**

---

#### Scenario 2.2: Complete/Pending Card Shows Task Counts
**Given** a user views the dashboard
**When** they observe the Complete/Pending card
**Then** it displays the current count of completed and pending tasks

**Test Steps**:
1. Create 3 tasks (see Scenario 4.1)
2. Mark 1 task as complete (checkbox)
3. Navigate back to dashboard
4. Verify Complete/Pending card shows "1 done, 2 pending" or similar

**✅ PASS** | **❌ FAIL** | **⚠️ BLOCKED**

---

#### Scenario 2.3: Add Task Card Opens Modal
**Given** a user clicks the "Add Task" card
**When** the action executes
**Then** a modal opens displaying the task creation form

**Test Steps**:
1. Navigate to `/dashboard`
2. Click "Add Task" card
3. Verify modal opens with form fields
4. Verify form has: title input, description textarea, priority selector, category input, due date picker

**✅ PASS** | **❌ FAIL** | **⚠️ BLOCKED**

---

#### Scenario 2.4: View Tasks Card Navigates to Task List
**Given** a user clicks the "View Tasks" card
**When** the action executes
**Then** they navigate to the task list page showing all their tasks

**Test Steps**:
1. Navigate to `/dashboard`
2. Click "View Tasks" card
3. Verify navigation to `/tasks` page
4. Verify task list displays (even if empty)

**✅ PASS** | **❌ FAIL** | **⚠️ BLOCKED**

---

#### Scenario 2.5: Update Task Card Navigates to Task List
**Given** a user clicks the "Update Task" card
**When** the action executes
**Then** they navigate to the task list page with editing capabilities enabled

**Test Steps**:
1. Navigate to `/dashboard`
2. Click "Update Task" card
3. Verify navigation to `/tasks` page
4. Verify edit functionality is accessible (click task to edit)

**✅ PASS** | **❌ FAIL** | **⚠️ BLOCKED**

---

#### Scenario 2.6: Complete/Pending Card Action
**Given** a user clicks the "Complete/Pending" card
**When** the action executes
**Then** they navigate to a filtered view or toggle to manage task completion status

**Test Steps**:
1. Navigate to `/dashboard`
2. Click "Complete/Pending" card
3. Verify navigation to task management view (likely `/tasks`)
4. Verify completion toggles are visible

**✅ PASS** | **❌ FAIL** | **⚠️ BLOCKED**

---

#### Scenario 2.7: Delete Task Card Action
**Given** a user clicks the "Delete Task" card
**When** the action executes
**Then** they navigate to the task list page with delete actions enabled

**Test Steps**:
1. Navigate to `/dashboard`
2. Click "Delete Task" card
3. Verify navigation to `/tasks` page
4. Verify delete buttons are visible on task cards

**✅ PASS** | **❌ FAIL** | **⚠️ BLOCKED**

---

### User Story 3 - Task List Display (6 scenarios)

#### Scenario 3.1: Task Cards Display All Metadata
**Given** a user navigates to the task list page
**When** they view their tasks
**Then** each task displays as a card showing all metadata

**Test Steps**:
1. Create a task with all fields populated
2. Navigate to `/tasks`
3. Verify task card shows:
   - Checkbox
   - Title
   - Description
   - Priority tag (colored)
   - Category tag
   - Due date
   - Status badge
   - Created date
   - Delete button

**✅ PASS** | **❌ FAIL** | **⚠️ BLOCKED**

---

#### Scenario 3.2: Progress Bar Displays Completion Ratio
**Given** a user has completed some tasks
**When** they view the task list
**Then** a progress bar displays at the top showing "X of Y completed" with visual progress

**Test Steps**:
1. Create 4 tasks
2. Mark 2 tasks as complete
3. Navigate to `/tasks`
4. Verify progress bar shows "2 of 4 completed"
5. Verify visual progress bar is 50% filled

**✅ PASS** | **❌ FAIL** | **⚠️ BLOCKED**

---

#### Scenario 3.3: Checkbox Toggles Completion Status
**Given** a user clicks a task's checkbox
**When** the action completes
**Then** the task's completion status toggles, badge updates, and progress bar reflects new count

**Test Steps**:
1. Create 1 task (incomplete)
2. Navigate to `/tasks`
3. Note current progress (0 of 1)
4. Click checkbox on task
5. Verify checkbox becomes checked
6. Verify status badge updates to "Completed"
7. Verify progress bar updates to "1 of 1 completed"

**✅ PASS** | **❌ FAIL** | **⚠️ BLOCKED**

---

#### Scenario 3.4: Completed Tasks Show Strikethrough
**Given** a user views a completed task
**When** they observe the task card
**Then** the title is styled with strikethrough text and status badge shows "Completed"

**Test Steps**:
1. Create and complete a task
2. Navigate to `/tasks`
3. Verify task title has strikethrough styling
4. Verify status badge shows "Completed"

**✅ PASS** | **❌ FAIL** | **⚠️ BLOCKED**

---

#### Scenario 3.5: Empty State Message
**Given** a user has no tasks
**When** they view the task list page
**Then** they see an empty state message

**Test Steps**:
1. Delete all tasks
2. Navigate to `/tasks`
3. Verify message: "No tasks yet. Create your first task to get started!" or similar

**✅ PASS** | **❌ FAIL** | **⚠️ BLOCKED**

---

#### Scenario 3.6: Task Deletion with Confirmation
**Given** a user clicks the "Delete" button on a task card
**When** they confirm the action
**Then** the task is removed from the list and progress bar updates

**Test Steps**:
1. Create 2 tasks
2. Navigate to `/tasks`
3. Click delete button on one task
4. Verify confirmation dialog appears
5. Click "Confirm" in dialog
6. Verify task is removed from list
7. Verify progress bar updates (1 task remaining)

**✅ PASS** | **❌ FAIL** | **⚠️ BLOCKED**

---

### User Story 4 - Task Creation (5 scenarios)

#### Scenario 4.1: Task Creation Form Opens
**Given** a user clicks the "Add Task" card on the dashboard
**When** the modal opens
**Then** they see a form with all required fields

**Test Steps**:
1. Navigate to `/dashboard`
2. Click "Add Task" card
3. Verify modal opens
4. Verify fields present:
   - Title input (required indicator)
   - Description textarea
   - Priority selector (High/Medium/Low)
   - Category/tags input
   - Due date picker
   - Submit button
   - Cancel button

**✅ PASS** | **❌ FAIL** | **⚠️ BLOCKED**

---

#### Scenario 4.2: Successful Task Creation
**Given** a user fills out the task creation form with valid data
**When** they submit
**Then** the task is created, modal closes, and success message appears

**Test Steps**:
1. Open task creation modal
2. Fill in:
   - Title: "Test Task"
   - Description: "Test description"
   - Priority: "High"
   - Category: "work"
   - Due date: tomorrow's date
3. Click "Submit"
4. Verify modal closes
5. Verify success toast: "Task created successfully!"
6. Navigate to `/tasks` and verify new task appears

**✅ PASS** | **❌ FAIL** | **⚠️ BLOCKED**

---

#### Scenario 4.3: Title Required Validation
**Given** a user submits the task creation form with an empty title
**When** validation runs
**Then** they see an error message "Title is required" and form does not submit

**Test Steps**:
1. Open task creation modal
2. Leave title field empty
3. Fill in other fields
4. Click "Submit"
5. Verify error message: "Title is required"
6. Verify modal remains open
7. Verify task is not created

**✅ PASS** | **❌ FAIL** | **⚠️ BLOCKED**

---

#### Scenario 4.4: New Task Appears in Task List
**Given** a user fills out and submits the task creation form successfully
**When** they navigate to the task list
**Then** they see their new task with all entered details

**Test Steps**:
1. Complete Scenario 4.2 (create task)
2. Navigate to `/tasks`
3. Verify new task appears with:
   - Correct title: "Test Task"
   - Correct description: "Test description"
   - Correct priority: High (red tag)
   - Correct category: "work"
   - Correct due date: tomorrow's date

**✅ PASS** | **❌ FAIL** | **⚠️ BLOCKED**

---

#### Scenario 4.5: Cancel Does Not Create Task
**Given** a user is filling out the task creation form
**When** they click "Cancel"
**Then** the modal closes without creating a task and no data is saved

**Test Steps**:
1. Open task creation modal
2. Fill in some fields
3. Click "Cancel" button
4. Verify modal closes
5. Navigate to `/tasks`
6. Verify no new task was created

**✅ PASS** | **❌ FAIL** | **⚠️ BLOCKED**

---

### User Story 5 - Task Editing (4 scenarios)

#### Scenario 5.1: Edit Modal Pre-fills with Task Data
**Given** a user clicks on a specific task in the list
**When** the edit modal opens
**Then** the form is pre-filled with the task's current data

**Test Steps**:
1. Create a task with known data
2. Navigate to `/tasks`
3. Click on the task card
4. Verify edit modal opens
5. Verify all fields are pre-filled with current task data:
   - Title matches
   - Description matches
   - Priority matches
   - Categories match
   - Due date matches

**✅ PASS** | **❌ FAIL** | **⚠️ BLOCKED**

---

#### Scenario 5.2: Successful Task Update
**Given** a user modifies fields in the edit form and submits
**When** the save action completes
**Then** the task is updated, modal closes, and task list reflects new values

**Test Steps**:
1. Open edit modal for a task
2. Change title to "Updated Title"
3. Change priority to "Low"
4. Click "Save" button
5. Verify modal closes
6. Verify success toast: "Task updated successfully!"
7. Verify task list shows updated values

**✅ PASS** | **❌ FAIL** | **⚠️ BLOCKED**

---

#### Scenario 5.3: Title Required Validation in Edit
**Given** a user clears the title field in the edit form
**When** they try to submit
**Then** they see an error message and form does not submit

**Test Steps**:
1. Open edit modal for a task
2. Clear the title field (delete all text)
3. Click "Save" button
4. Verify error message: "Title is required"
5. Verify modal remains open
6. Verify task is not updated

**✅ PASS** | **❌ FAIL** | **⚠️ BLOCKED**

---

#### Scenario 5.4: Cancel Preserves Original Data
**Given** a user is editing a task
**When** they click "Cancel"
**Then** the modal closes without saving changes and task retains original values

**Test Steps**:
1. Note original task data
2. Open edit modal
3. Change multiple fields
4. Click "Cancel" button
5. Verify modal closes
6. Verify task list shows original values (unchanged)

**✅ PASS** | **❌ FAIL** | **⚠️ BLOCKED**

---

### User Story 6 - Profile & Settings (3 scenarios)

#### Scenario 6.1: Profile Page Displays User Info
**Given** an authenticated user clicks on their profile/settings link
**When** the page loads
**Then** they see their current email address and profile settings

**Test Steps**:
1. Login with known email
2. Click profile/settings link in navbar
3. Verify navigation to `/profile` or similar
4. Verify email address displays correctly

**✅ PASS** | **❌ FAIL** | **⚠️ BLOCKED**

---

#### Scenario 6.2: Successful Profile Update
**Given** a user updates their profile information
**When** they save changes
**Then** the updates are persisted and success message appears

**Test Steps**:
1. Navigate to profile page
2. Update email to new value
3. Click "Save" button
4. Verify success toast: "Profile updated successfully!"
5. Refresh page
6. Verify new email persists

**✅ PASS** | **❌ FAIL** | **⚠️ BLOCKED**

---

#### Scenario 6.3: Password Change
**Given** a user wants to change their password
**When** they fill out the password change form
**Then** their password is updated and they remain logged in

**Test Steps**:
1. Navigate to profile page
2. Enter current password
3. Enter new password (meeting validation rules)
4. Click "Change Password" button
5. Verify success message
6. Verify user remains logged in (not logged out)
7. Logout and login with new password
8. Verify new password works

**✅ PASS** | **❌ FAIL** | **⚠️ BLOCKED**

---

## T152: Functional Requirements Verification

### FR-001 to FR-012: Authentication & Session Management

| FR | Requirement | Verified | Notes |
|----|-------------|----------|-------|
| FR-001 | Registration page with email/password fields | ☐ | Check `/register` page |
| FR-002 | Email format validation | ☐ | Enter invalid email format |
| FR-003 | Password strength validation (min 8 chars) | ☐ | Enter short password |
| FR-004 | Login page with email/password fields | ☐ | Check `/login` page |
| FR-005 | Better Auth JWT token generation | ☐ | Check DevTools after login |
| FR-006 | JWT tokens stored securely | ☐ | Check cookies/localStorage |
| FR-007 | JWT tokens attached to API requests | ☐ | Check Network tab |
| FR-008 | Session restoration on return | ☐ | Close browser, reopen |
| FR-009 | Sign Out button terminates session | ☐ | Click sign out |
| FR-010 | Protected routes redirect unauthenticated users | ☐ | Access `/dashboard` without login |
| FR-011 | Clear error messages for invalid credentials | ☐ | Login with wrong password |
| FR-012 | Clear error messages for registration failures | ☐ | Register with duplicate email |

### FR-013 to FR-021: Dashboard & Navigation

| FR | Requirement | Verified | Notes |
|----|-------------|----------|-------|
| FR-013 | Navigation bar on all authenticated pages | ☐ | Check all pages |
| FR-014 | Dashboard title "My Tasks" + subtitle | ☐ | Check `/dashboard` |
| FR-015 | Five interactive action cards | ☐ | Count cards |
| FR-016 | Distinct pastel colors for each card | ☐ | Visual inspection |
| FR-017 | Icons on each dashboard card | ☐ | Visual inspection |
| FR-018 | Badge on Complete/Pending card | ☐ | Check task counts |
| FR-019 | Add Task card opens modal | ☐ | Click card |
| FR-020 | View Tasks card navigates to list | ☐ | Click card |
| FR-021 | Other cards navigate to task management | ☐ | Click each card |

### FR-022 to FR-032: Task List Display

| FR | Requirement | Verified | Notes |
|----|-------------|----------|-------|
| FR-022 | All tasks displayed in card format | ☐ | Check `/tasks` page |
| FR-023 | Progress section titled "Toggle Completion Status" | ☐ | Visual inspection |
| FR-024 | Progress bar with "X of Y completed" | ☐ | Check calculation |
| FR-025 | Task card displays all metadata | ☐ | Check each field |
| FR-026 | Completed tasks have strikethrough | ☐ | Mark task complete |
| FR-027 | Priority tags color-coded | ☐ | Check High/Medium/Low colors |
| FR-028 | Category tags distinctly styled | ☐ | Visual inspection |
| FR-029 | Due dates in MM/DD/YYYY format | ☐ | Check format |
| FR-030 | Status badge shows "Completed" | ☐ | Check completed task |
| FR-031 | Created dates in "Created MM/DD/YYYY" format | ☐ | Check format |
| FR-032 | Empty state message when no tasks | ☐ | Delete all tasks |

### FR-033 to FR-038: Task Actions

| FR | Requirement | Verified | Notes |
|----|-------------|----------|-------|
| FR-033 | Checkbox toggles completion status | ☐ | Click checkbox |
| FR-034 | Progress bar updates immediately | ☐ | Check after toggle |
| FR-035 | Confirmation dialog for delete | ☐ | Click delete button |
| FR-036 | Task removed after delete confirmation | ☐ | Confirm deletion |
| FR-037 | Progress bar updates after deletion | ☐ | Check after delete |
| FR-038 | Edit modal opens pre-filled | ☐ | Click task card |

### FR-039 to FR-048: Task Creation Form

| FR | Requirement | Verified | Notes |
|----|-------------|----------|-------|
| FR-039 | Modal dialog with all form fields | ☐ | Open Add Task modal |
| FR-040 | Title field validation (not empty) | ☐ | Submit empty title |
| FR-041 | Inline error "Title is required" | ☐ | Check error message |
| FR-042 | Priority options with color indicators | ☐ | Check dropdown |
| FR-043 | Date picker for due date | ☐ | Check date picker |
| FR-044 | Multiple category tags | ☐ | Add multiple tags |
| FR-045 | Task created, modal closes on submit | ☐ | Submit valid form |
| FR-046 | Success message "Task created successfully!" | ☐ | Check toast |
| FR-047 | Cancel closes without saving | ☐ | Click cancel |
| FR-048 | Form fields cleared after creation | ☐ | Create task, reopen modal |

### FR-049 to FR-055: Task Editing Form

| FR | Requirement | Verified | Notes |
|----|-------------|----------|-------|
| FR-049 | Edit modal pre-filled with current data | ☐ | Open edit for task |
| FR-050 | All fields modifiable | ☐ | Try changing each field |
| FR-051 | Title validation on update | ☐ | Clear title, submit |
| FR-052 | Task updated, modal closes | ☐ | Submit valid changes |
| FR-053 | Success message "Task updated successfully!" | ☐ | Check toast |
| FR-054 | Cancel closes without saving | ☐ | Click cancel |
| FR-055 | Original data preserved on cancel | ☐ | Verify unchanged |

### FR-056 to FR-061: Profile & Settings

| FR | Requirement | Verified | Notes |
|----|-------------|----------|-------|
| FR-056 | Profile/settings page accessible | ☐ | Check navigation link |
| FR-057 | Email address displayed | ☐ | Check profile page |
| FR-058 | Profile information updatable | ☐ | Try updating |
| FR-059 | Password change form | ☐ | Check form fields |
| FR-060 | Current password validation | ☐ | Enter wrong current password |
| FR-061 | Success message after profile update | ☐ | Update and check toast |

### FR-062 to FR-075: UI/UX Interactive Behaviors

| FR | Requirement | Verified | Notes |
|----|-------------|----------|-------|
| FR-062 | Framer Motion page transitions | ☐ | Navigate between pages |
| FR-063 | Modal animations (fade + scale) | ☐ | Open/close modals |
| FR-064 | Dashboard card hover effects | ☐ | Hover over cards |
| FR-065 | ShadCN Button components | ☐ | Inspect button elements |
| FR-066 | ShadCN Input components | ☐ | Inspect form inputs |
| FR-067 | ShadCN Form components | ☐ | Inspect form structure |
| FR-068 | ShadCN Dialog components | ☐ | Inspect modals |
| FR-069 | Task card hover effects | ☐ | Hover over task cards |
| FR-070 | Loading states with Spinner/Skeleton | ☐ | Slow down network |
| FR-071 | Error states with Alert component | ☐ | Trigger errors |
| FR-072 | Success toasts | ☐ | Complete actions |
| FR-073 | Fully responsive | ☐ | Test all screen sizes |
| FR-074 | Responsive navbar (hamburger on mobile) | ☐ | Check mobile view |
| FR-075 | Dashboard cards stack on mobile | ☐ | Check mobile layout |

---

## T153: Success Criteria Validation

### Measurable Outcomes (SC-001 to SC-012)

| SC | Criteria | Target | Actual | Pass/Fail | Notes |
|----|----------|--------|--------|-----------|-------|
| SC-001 | Registration + first login time | < 1 min, 95% success | | ☐ | Time 5 users |
| SC-002 | Task creation time (all fields) | < 30 sec | | ☐ | Time task creation |
| SC-003 | Completion toggle feedback | < 200ms | | ☐ | Use DevTools Performance tab |
| SC-004 | Dashboard load time | < 2 sec (broadband) | | ☐ | Use DevTools Network tab |
| SC-005 | Page transition duration | < 300ms | | ☐ | Measure with DevTools |
| SC-006 | Form validation display time | < 100ms | | ☐ | Measure with DevTools |
| SC-007 | First task creation success rate | 90% | | ☐ | Test with 10 users |
| SC-008 | Responsive range | 320px - 1920px | | ☐ | Test all breakpoints |
| SC-009 | Feature access from dashboard | ≤ 2 clicks | | ☐ | Count clicks for each feature |
| SC-010 | Session restoration success | 100% | | ☐ | Test 10 refreshes |
| SC-011 | State coverage (empty/loading/error) | 100% | | ☐ | Verify all states present |
| SC-012 | Interactive element response time | < 150ms | | ☐ | Test all buttons/cards/checkboxes |

### User Experience Quality (SC-013 to SC-016)

| SC | Criteria | Method | Result | Notes |
|----|----------|--------|--------|-------|
| SC-013 | At-a-glance task understanding | Visual inspection | ☐ | Check color-coded priority/status |
| SC-014 | Intuitive dashboard iconography | User feedback | ☐ | Ask 5 users to identify actions |
| SC-015 | Form validation guides corrections | User observation | ☐ | Watch users correct errors |
| SC-016 | Visual consistency (color palette) | Visual inspection | ☐ | Check all pages match spec colors |

---

## T154: Edge Cases Testing

### Edge Case 1: Past Due Date on Task Creation
**Scenario**: User creates a task with due date in the past
**Expected**: System allows creation but displays warning indicator

**Test Steps**:
1. Open task creation modal
2. Fill in title: "Overdue Test"
3. Select due date: yesterday
4. Submit task
5. Verify task is created
6. Check if warning indicator shows (overdue badge, red color, etc.)

**✅ PASS** | **❌ FAIL** | **⚠️ BLOCKED**

---

### Edge Case 2: Very Long Task Titles/Descriptions
**Scenario**: User enters extremely long text in title or description
**Expected**: System truncates display with "..." and shows full text on hover/modal

**Test Steps**:
1. Create task with title: 500 character string
2. Create task with description: 2000 character string
3. View task list
4. Verify title truncates with "..."
5. Hover over truncated title
6. Verify full text appears (tooltip or modal)

**✅ PASS** | **❌ FAIL** | **⚠️ BLOCKED**

---

### Edge Case 3: Offline Connection During Form Submission
**Scenario**: User loses internet connection while filling form
**Expected**: System shows offline indicator and preserves form data locally

**Test Steps**:
1. Open task creation modal
2. Fill in all fields
3. Disconnect internet (DevTools → Network → Offline)
4. Try to submit
5. Verify offline indicator appears
6. Reconnect internet
7. Verify form data is still present
8. Submit successfully

**✅ PASS** | **❌ FAIL** | **⚠️ BLOCKED**

---

### Edge Case 4: Special Characters and Emojis
**Scenario**: User enters special characters/emojis in task data
**Expected**: System accepts and displays all valid UTF-8 characters

**Test Steps**:
1. Create task with title: "Test 📝 @#$% ñ 中文"
2. Create task with description: "Emoji test 🚀 ✅ 💡"
3. View task list
4. Verify all characters display correctly
5. Edit task
6. Verify characters preserved in edit modal

**✅ PASS** | **❌ FAIL** | **⚠️ BLOCKED**

---

### Edge Case 5: Hundreds of Tasks Performance
**Scenario**: User has hundreds of tasks
**Expected**: System implements pagination or infinite scroll

**Test Steps**:
1. Create 100+ tasks (use script or API)
2. Navigate to `/tasks` page
3. Verify pagination controls OR infinite scroll
4. Scroll through tasks
5. Check load time remains reasonable
6. Verify performance does not degrade

**✅ PASS** | **❌ FAIL** | **⚠️ BLOCKED**

---

### Edge Case 6: Rapid Clicking on Completion Toggle
**Scenario**: User rapidly clicks checkbox multiple times
**Expected**: System debounces requests to prevent duplicate API calls

**Test Steps**:
1. Create 1 task
2. Navigate to task list
3. Open DevTools Network tab
4. Rapidly click checkbox 10 times
5. Verify only 1 or 2 API requests sent (debounced)
6. Verify final state is correct (either completed or pending)

**✅ PASS** | **❌ FAIL** | **⚠️ BLOCKED**

---

### Edge Case 7: Accessing Protected Route Without Login
**Scenario**: User tries to access protected route while not authenticated
**Expected**: System redirects to login with return URL preserved

**Test Steps**:
1. Logout completely
2. Clear cookies/localStorage
3. Try to navigate directly to `/dashboard`
4. Verify redirect to `/login`
5. Optionally: verify return URL preserved (e.g., `/login?returnUrl=/dashboard`)

**✅ PASS** | **❌ FAIL** | **⚠️ BLOCKED**

---

### Edge Case 8: Expired JWT Token Handling
**Scenario**: User's JWT token expires during session
**Expected**: System detects expiration, clears session, redirects to login with message

**Test Steps**:
1. Login successfully
2. Manually expire JWT token (modify expiration in DevTools or wait for expiration)
3. Try to perform action (create task, toggle completion)
4. Verify session cleared
5. Verify redirect to login
6. Verify message: "Session expired, please log in again"

**✅ PASS** | **❌ FAIL** | **⚠️ BLOCKED**

---

## T155: End-to-End User Journeys

### Journey 1: Complete New User Onboarding to First Task
**Flow**: Registration → Login → Dashboard → Create Task → View Task

**Test Steps**:
1. Register new account
2. Verify redirect to dashboard
3. Click "Add Task" card
4. Fill out task creation form completely
5. Submit task
6. Click "View Tasks" card
7. Verify task appears in list with all details correct

**Duration**: ___ minutes
**Success**: ☐ Yes | ☐ No
**Blockers**: _______________

---

### Journey 2: Task Management Lifecycle
**Flow**: Create Task → View → Edit → Complete → Delete

**Test Steps**:
1. Login as existing user
2. Create new task from dashboard
3. Navigate to task list
4. Click task to open edit modal
5. Modify task fields
6. Save changes
7. Toggle completion checkbox
8. Verify strikethrough and status change
9. Click delete button
10. Confirm deletion
11. Verify task removed

**Duration**: ___ minutes
**Success**: ☐ Yes | ☐ No
**Blockers**: _______________

---

### Journey 3: Multi-Task Management
**Flow**: Create Multiple Tasks → Organize → Bulk Complete

**Test Steps**:
1. Login as existing user
2. Create 5 tasks with different priorities
3. Create 3 tasks with different categories
4. Navigate to task list
5. Verify all 8 tasks display
6. Mark 4 tasks as complete
7. Verify progress bar shows "4 of 8 completed"
8. Delete 2 pending tasks
9. Verify progress bar shows "4 of 6 completed"

**Duration**: ___ minutes
**Success**: ☐ Yes | ☐ No
**Blockers**: _______________

---

### Journey 4: Profile Management Workflow
**Flow**: Login → Profile → Update Email → Change Password → Logout → Login with New Credentials

**Test Steps**:
1. Login with known credentials
2. Navigate to profile page
3. Update email address
4. Save changes
5. Change password
6. Save changes
7. Logout
8. Login with new email and new password
9. Verify successful authentication

**Duration**: ___ minutes
**Success**: ☐ Yes | ☐ No
**Blockers**: _______________

---

### Journey 5: Mobile User Experience
**Flow**: Complete workflow on mobile device (or mobile viewport)

**Test Steps**:
1. Set browser to mobile viewport (375px width)
2. Login on mobile view
3. Verify hamburger menu appears
4. Navigate dashboard cards (should stack)
5. Create task on mobile
6. View task list on mobile
7. Toggle task completion on mobile
8. Edit task on mobile
9. Verify all interactions work smoothly

**Duration**: ___ minutes
**Success**: ☐ Yes | ☐ No
**Blockers**: _______________

---

## Testing Summary Report

### Overall Status

| Category | Total | Passed | Failed | Blocked | Pass Rate |
|----------|-------|--------|--------|---------|-----------|
| Acceptance Scenarios | 35 | | | | % |
| Functional Requirements | 75 | | | | % |
| Success Criteria | 16 | | | | % |
| Edge Cases | 8 | | | | % |
| E2E Journeys | 5 | | | | % |
| **TOTAL** | **139** | | | | **%** |

### Critical Issues

_List any critical blocking issues discovered during testing_

1.
2.
3.

### Minor Issues

_List any non-blocking issues or improvements_

1.
2.
3.

### Recommendations

_List recommendations for improvements or fixes_

1.
2.
3.

---

## Test Environment Details

- **Frontend URL**: http://localhost:3000
- **Backend URL**: http://localhost:8000
- **Database**: _________________
- **Test Date**: _________________
- **Tester**: _________________
- **Browser(s)**: _________________
- **Screen Resolutions Tested**: _________________

---

## Sign-off

- [ ] All acceptance scenarios validated
- [ ] All functional requirements verified
- [ ] All success criteria met
- [ ] All edge cases tested
- [ ] All E2E journeys completed
- [ ] Issues documented and prioritized
- [ ] Ready for deployment

**Validated by**: _________________ **Date**: _________________
