# ADR-003: Configuration over Customization

Date: 2026-06-20

Decision:
TexFlow AI ERP shall prioritize configuration over source-code customization. Workflows, approvals, production processes, TNA stages, document templates, dashboards, reports, email templates, roles, permissions, and business rules should be configurable through the application wherever practical.

Rationale:
- One codebase for all customers.
- Faster onboarding.
- Easier upgrades.
- Reduced maintenance.
- Greater flexibility for different factories and brands.

Consequences:
- Build a powerful configuration model and admin UI to manage business rules and workflows.
- Favor feature flags, templating, and metadata-driven schemas over hard-coded logic.
- Ensure configurations are versioned and auditable.

Status: Accepted
