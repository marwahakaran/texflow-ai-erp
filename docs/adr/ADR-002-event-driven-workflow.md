# ADR-002: Event-Driven Business Workflow

Date: 2026-06-20

Decision:
All core business transactions (Purchase Order approval, Fabric Receipt, Cutting Completion, Stitching Completion, Shipment Confirmation, etc.) shall publish domain events through an internal event bus. Modules should react to these events rather than relying on tightly coupled synchronous calls wherever practical.

Context:
- Loose coupling between modules improves extensibility and scalability.
- Event-driven design supports auditability and tracing of domain events.
- Prepares the architecture for future microservice decomposition or external integrations.

Consequences:
- Implement an internal event bus (in-process) with a pluggable adapter to move to a message broker (e.g., Kafka/RabbitMQ) later.
- Domain actions publish events; interested modules subscribe and react.
- Events stored in append-only audit/event store for traceability and replay.
- Design for idempotency, event versioning, and error handling.

Status: Accepted
