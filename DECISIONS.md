# Architectural Decisions

This file records Architecture Decision Records (ADRs) for the repository.

## ADR-001: Modular Monolith (Domain-Driven Design)

Date: 2026-06-20

Decision: TexFlow AI ERP will initially be built as a Modular Monolith using Domain-Driven Design (DDD). Microservices will be introduced only when justified by scale or operational needs.

Context:
- Rapid development and iteration are critical for an MVP.
- A modular monolith simplifies deployment, debugging, and local development.
- DDD boundaries allow clean separation of modules and an easier migration path to microservices if needed.

Consequences:
- Codebase will be organized by domain modules (authentication, merchandising, production, inventory, etc.)
- Each module will have clear APIs and data ownership.
- Shared infrastructure (database) initially; module boundaries enforced in code.
- Future migration to microservices will require extracting modules and defining inter-module APIs.

Status: Accepted
