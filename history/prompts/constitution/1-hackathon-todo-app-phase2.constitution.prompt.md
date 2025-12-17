---
id: 1
title: "Hackathon Todo App Phase2 Constitution"
stage: constitution
date: "2025-12-08"
surface: "agent"
model: "Claude Sonnet 4.5"
feature: "none"
branch: "main"
user: "user"
command: "/sp.constitution"
labels: ["constitution", "spec-driven", "full-stack", "web-application"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - ".specify/memory/constitution.md"
tests: []
---

# Constitution Update: Hackathon Todo App Phase-2

## Prompt Text

Draft a complete Spec‑Kit‑Plus constitution for Phase‑2 of the Hackathon Todo App.

The project is now evolving from a console‑based todo app (Phase‑1) into a full‑stack multi‑user web application.

The constitution should define:

Project Vision

Transform Phase‑1 console todo app into a modern full‑stack, multi‑user todo web platform.

Built using Claude Code + Spec‑Kit‑Plus in a monorepo.

Spec‑driven workflow across frontend, backend, database, auth, and deployment.

Required Tech Stack

Frontend: Next.js 16+ (App Router), TypeScript, Tailwind CSS

Backend: Python FastAPI

Database: Neon Serverless PostgreSQL

ORM: SQLModel

Authentication: Better Auth (JWT enabled)

Spec‑Driven: Claude Code + GitHub Spec‑Kit‑Plus

Infrastructure: Docker‑compose monorepo structure

Core Requirements (Phase‑2)

Include all required capabilities:

Full CRUD task management (multi‑user)

REST API endpoints for:

GET/POST /api/{user_id}/tasks

GET/PUT/DELETE /api/{user_id}/tasks/{id}

PATCH /api/{user_id}/tasks/{id}/complete

User signup/signin with Better Auth (frontend-owned)

Frontend must attach JWT token to API calls

Backend must verify JWT with shared secret (BETTER_AUTH_SECRET)

Task ownership enforcement at every API call

Responsive modern UI

Persistent database storage in Neon PostgreSQL

Monorepo & Spec‑Kit Structure

Specify the repo structure below, and require adherence to Spec‑Kit conventions:

hackathon-todo/

.spec-kit/config.yaml

specs/

overview.md

architecture.md

features/

api/

database/

ui/

frontend/ (Next.js)

backend/ (FastAPI)

docker-compose.yml

CLAUDE.md

Constitution must enforce that all development begins with updating specs, then planning, then tasks, then implementation.

Constitution should support future phases (e.g., chatbot in Phase 3).

Governance Rules

Specs are the single source of truth

Every change requires updating specs before coding

Claude Code must reference specs with @specs/...

Sub‑agents & skills may be created for:

backend development

frontend UI

database modeling

authentication

API contract enforcement

Generate a polished,

## Response Text

Successfully transformed the constitution from a console-based todo app to a full-stack multi-user web application. The new constitution (v2.0.0) includes principles for:

- Full-stack web application architecture with Next.js 16+ frontend and Python FastAPI backend
- Multi-user task management with ownership enforcement
- JWT-based authentication using Better Auth
- Serverless PostgreSQL database with Neon
- SQLModel ORM for database operations
- RESTful API design with specific endpoint patterns
- Responsive UI with Tailwind CSS
- Monorepo structure with Docker-Compose
- Spec-driven development workflow
- API contract enforcement

The constitution enforces spec-first development and includes quality standards for code organization, error handling, security, performance, and testing.

## Outcome

The constitution was successfully updated from v1.2.0 to v2.0.0, completely transforming the project's direction from a console app to a full-stack web application with multi-user support, authentication, and proper architecture separation.