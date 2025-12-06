<!--
Sync Impact Report:
- Version change: 1.0.0 -> 1.0.1
- Added Sections: None.
- Removed Sections: None.
- Templates requiring updates:
  - ✅ .specify/memory/constitution.md (updated)
  - ✅ my-books/docusaurus.config.ts (updated)
  - ⬜ .specify/templates/plan-template.md (no update needed)
  - ⬜ .specify/templates/spec-template.md (no update needed)
  - ⬜ .specify/templates/tasks-template.md (no update needed)
  - ⬜ .specify/templates/adr-template.md (no update needed)
  - ⬜ .specify/templates/phr-template.prompt.md (no update needed)
- Follow-up TODOs: None.
-->
# Docusaurus Textbook Constitution

## Core Principles

### I. Spec-Driven Development
All development MUST begin with a specification (`spec.md`). The spec defines the problem, scope, and acceptance criteria before any code is written. This ensures clarity and alignment.

### II. Test-Driven Development
TDD is mandatory. A failing test (`red` state) MUST be written to demonstrate the bug or new feature's absence before implementation (`green` state) begins. The Red-Green-Refactor cycle is strictly enforced.

### III. Clear and Auditable History
Every significant action, prompt, and decision MUST be recorded. Prompt History Records (PHRs) and Architectural Decision Records (ADRs) are non-negotiable artifacts. This creates a transparent and traceable project history.

### IV. Modular and Reusable Code
Strive for small, single-responsibility functions and modules. Code should be written with reusability in mind, preferring generic helpers over specific, one-off solutions.

### V. Consistent Tooling and Automation
The project MUST rely on a consistent set of tools and scripts for common tasks like creating records, running tests, and managing features. Automation is preferred over manual processes to reduce errors.

## Development Workflow

The standard workflow follows the Spec-Driven Development model: `Spec -> Plan -> Tasks -> Red -> Green -> Refactor`. All work should be done on a dedicated feature branch.

## Quality Gates

Before merging, all new code must pass automated tests, linting, and a peer review. The associated spec and tasks must be successfully fulfilled.

## Governance

This constitution is the authoritative guide for project development. Any proposed amendments must be documented in an ADR and approved by the project owner. All contributions must adhere to these principles. Compliance is verified during code review. Use `GEMINI.md` for agent-specific runtime guidance.

**Version**: 1.0.1 | **Ratified**: 2025-12-04 | **Last Amended**: 2025-12-05