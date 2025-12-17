<!--
Sync Impact Report
==================
Version Change: 2.0.0 → 2.1.0
Rationale: MINOR version bump - Expanded UI principles to include rich, modern, animated UI requirements with specific component libraries and interaction patterns.

Modified Principles:
  - Principle VII: "Responsive Modern UI" → "Rich Modern Animated UI Architecture"
    - Added: ShadCN UI component library requirement
    - Added: Framer Motion for animations and transitions
    - Added: Next.js App Router emphasis
  - Principle VIII: New principle "UI Layout and Component Standards"
    - Added: Card-based interactive blocks requirement
    - Added: Client-side validation requirement
    - Added: Better Auth client component integration
    - Added: Mobile-first responsive layout rules

Added Sections:
  - New Principle VIII: UI Layout and Component Standards

Removed Sections: None

Renumbered Principles:
  - Old VIII → IX (Monorepo Structure)
  - Old IX → X (Spec-Driven Development)
  - Old X → XI (API Contract Enforcement)
  - Old XI → XII (Task Ownership Enforcement)
  - Old XII → XIII (Documentation Capture)

Templates Requiring Updates:
  ✅ plan-template.md - Already includes constitution check and frontend structure
  ✅ spec-template.md - Already includes user scenarios and requirements sections
  ✅ tasks-template.md - Already includes frontend/backend task organization
  ⚠️  Frontend implementation guidance - Should reference ShadCN UI, Framer Motion, and card-based layouts

Follow-up TODOs:
  - Consider creating UI component library documentation referencing ShadCN usage patterns
  - Consider documenting Framer Motion animation standards and reusable transitions
  - Consider creating card-based layout templates for common task operations
-->

# Hackathon Todo App Phase-2 - Full-Stack Multi-User Web Application Constitution

## Core Principles

### I. Full-Stack Web Application Architecture
The application MUST be implemented as a full-stack web application with separate frontend and backend services. The frontend MUST be built with Next.js 16+ (App Router) using TypeScript and Tailwind CSS. The backend MUST be built with Python FastAPI. Services MUST communicate via REST API with JSON payloads.

**Rationale**: Enables modern web development practices, scalability, and separation of concerns between user interface and business logic while supporting multi-user functionality.

### II. Multi-User Task Management System
The application MUST support full CRUD operations for tasks with multi-user isolation. Each task MUST be owned by a specific user and only accessible to that user. API endpoints MUST enforce user ownership at every operation.

**Rationale**: Core requirement for a multi-user application to ensure data privacy and proper access control between users.

### III. JWT-Based Authentication & Authorization
User authentication MUST be implemented using Better Auth with JWT tokens. The frontend MUST attach JWT tokens to all authenticated API calls. The backend MUST verify JWT tokens using a shared secret (BETTER_AUTH_SECRET) before processing any protected requests.

**Rationale**: Ensures secure user authentication and proper authorization for accessing protected resources while maintaining stateless server architecture.

### IV. Serverless PostgreSQL Database Persistence
All application data MUST be persisted in Neon Serverless PostgreSQL database. No in-memory storage or alternative persistence mechanisms are allowed. Database schema MUST be managed through proper migrations.

**Rationale**: Provides reliable, scalable, and persistent data storage suitable for a multi-user web application with serverless scalability benefits.

### V. SQLModel ORM for Database Operations
All database operations MUST use SQLModel as the Object-Relational Mapping layer. Direct SQL queries are prohibited except for complex operations that cannot be expressed through the ORM.

**Rationale**: Ensures type safety, prevents SQL injection, and provides a consistent interface for database operations across the application.

### VI. RESTful API Design
All backend endpoints MUST follow RESTful design principles with proper HTTP methods (GET, POST, PUT, PATCH, DELETE) and status codes. API endpoints MUST follow the pattern: GET/POST /api/{user_id}/tasks, GET/PUT/DELETE /api/{user_id}/tasks/{id}, PATCH /api/{user_id}/tasks/{id}/complete.

**Rationale**: Provides consistent, predictable, and standardized API interface that follows industry best practices for web services.

### VII. Rich Modern Animated UI Architecture
The frontend interface MUST be built using Next.js App Router with a rich, modern, animated experience. All UI components MUST use ShadCN UI component library for buttons, inputs, forms, dialogs, and modals. Page transitions and element animations MUST use Framer Motion. The UI MUST be responsive and work across different device sizes and browsers using Tailwind CSS for styling.

**Rationale**: Provides a professional, polished user experience with consistent component design, smooth animations, and accessibility while maintaining modern web standards.

### VIII. UI Layout and Component Standards
All UI pages MUST follow responsive layout rules with mobile-first design principles. Interactive elements MUST be organized as card-based blocks (e.g., "Add Task" card, "View Tasks" card, "Update Task" card). All forms MUST implement client-side validation with clear, helpful error messages. Authenticated pages MUST fetch and display user session information from Better Auth client components.

**Rationale**: Ensures consistent user interface patterns, improves usability through clear visual organization, prevents invalid data submission, and maintains secure session management throughout the application.

### IX. Monorepo Structure with Docker-Compose
The project MUST follow a monorepo structure with separate directories for frontend and backend, orchestrated with docker-compose. The repository structure MUST follow: frontend/, backend/, docker-compose.yml, and proper configuration files.

**Rationale**: Simplifies development, testing, and deployment while maintaining clear separation between frontend and backend codebases.

### X. Spec-Driven Development
All implementation MUST follow the specification file strictly. No feature may be added or removed unless updated in the spec first. Development workflow MUST follow: update specs → plan → tasks → implementation.

**Rationale**: Maintains traceability between requirements and implementation, ensures reproducibility, and prevents scope creep while supporting the Spec-Kit-Plus methodology.

### XI. API Contract Enforcement
Frontend and backend development MUST be coordinated through clearly defined API contracts. Changes to API endpoints MUST be documented and agreed upon before implementation.

**Rationale**: Ensures frontend and backend teams can work independently while maintaining compatibility and preventing integration issues.

### XII. Task Ownership Enforcement
Every API operation MUST verify that the authenticated user owns the task being accessed. No user MAY access, modify, or delete tasks owned by other users. Database queries MUST filter by user_id for all operations.

**Rationale**: Critical security requirement to ensure data isolation between users and prevent unauthorized access to tasks.

### XIII. Documentation Capture
Architectural Decision Records (ADRs) and Prompt History Records (PHRs) MUST be automatically generated and maintained by the AI under the `history/` directory for every major workflow command (`/sp.plan`, `/sp.tasks`, `/sp.implement`) to ensure full project transparency and horizontal intelligence accumulation.

**Rationale**: Ensures comprehensive historical context for development decisions and interactions, facilitates knowledge transfer, and provides a traceable audit trail for all significant project changes.

## Development Workflow

### Specification-First Development
1. All features MUST be documented in the specification before implementation
2. Specification changes MUST be reviewed and approved before code changes
3. Implementation MUST reference the specific spec section being implemented
4. All development begins with updating specs, then planning, then tasks, then implementation

### Frontend-Backend Coordination
- API contracts MUST be defined before parallel development
- Frontend and backend teams MUST coordinate through shared specification
- Integration testing SHOULD occur regularly to ensure compatibility

### Code Review Standards
- All changes MUST reference the specification section they implement
- Reviewers MUST verify alignment with constitution principles
- API changes MUST be documented and justified
- Violations of constitution principles MUST be documented and justified

## Quality Standards

### Code Organization
- Frontend and backend code MUST be properly separated
- Business logic MUST be properly distributed between frontend and backend
- Authentication logic MUST be clearly separated from business logic
- Database models MUST be properly defined in SQLModel

### Error Handling
- All API endpoints MUST handle errors gracefully with proper HTTP status codes
- Authentication errors MUST return 401 Unauthorized
- Authorization errors MUST return 403 Forbidden
- Resource not found errors MUST return 404 Not Found
- Server errors MUST return appropriate 5xx status codes

### Security
- All API endpoints MUST verify JWT authentication where required
- User input MUST be validated and sanitized
- SQL queries MUST use parameterized statements through ORM
- Secrets MUST be stored in environment variables, never hardcoded

### Performance
- API responses MUST complete within reasonable timeframes (< 2 seconds for typical operations)
- Database queries MUST be optimized and use appropriate indexing
- Frontend pages MUST load efficiently with proper caching strategies

### Testing
- Backend API endpoints MUST have comprehensive unit and integration tests
- Frontend components MUST have appropriate unit tests
- Authentication flows MUST be thoroughly tested
- Multi-user scenarios MUST be tested for proper isolation

## Governance

### Constitution Authority
This constitution supersedes all other development practices and guidelines. When conflicts arise between this constitution and other documentation, the constitution takes precedence.

### Amendment Process
1. Proposed amendments MUST be documented with rationale and impact analysis
2. Amendments MUST be approved by project stakeholders
3. Amendments MUST include a migration plan for existing code if applicable
4. All template files MUST be updated to reflect constitutional changes

### Compliance
- All pull requests MUST verify compliance with this constitution
- Architecture violations MUST be justified in the implementation plan
- Regular constitution compliance audits SHOULD be conducted

### Version Semantics
Constitution versions follow semantic versioning:
- **MAJOR**: Backward incompatible governance changes or principle removals/redefinitions
- **MINOR**: New principles added or materially expanded guidance
- **PATCH**: Clarifications, wording improvements, non-semantic refinements

**Version**: 2.1.0 | **Ratified**: 2025-12-08 | **Last Amended**: 2025-12-13