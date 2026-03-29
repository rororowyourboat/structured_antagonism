# Software Systems Domain

SA instruments for designing, auditing, and synthesizing software system specifications.

## The Three Instruments

| Instrument | Purpose | Input | Output |
|-----------|---------|-------|--------|
| [Product Spec](product-spec.md) | Generate a structured, implementation-neutral system design | Problem statement + constraints | Behavioral spec with domain model, features, contracts |
| [Spec Audit](spec-audit.md) | Adversarially review a spec and plan next steps | A product spec | Audit summary + prioritized drill-down plan |
| [Spec Synthesize](spec-synthesize.md) | Interrogate, validate, and produce a low-level design | A product spec (+ optional answers) | Questionnaire, clarifications, or final LLD spec |

## The Loop

```
Problem Statement
       │
       ▼
  Product Spec  ──▶  Spec Audit  ──▶  Spec Synthesize
       │                  │                    │
       │            Gaps found?          Complete &
       │                  │              compatible?
       │                  ▼                    │
       │            Fix & re-spec         Yes: Final LLD
       │                                  No:  Clarify & loop
       ▼
  (iterate until stable)
```

## When to Use Each

**Product Spec** — When you have a problem statement and need to define what the system does (not how it's built). Use this to force ontological commitment before anyone starts engineering.

**Spec Audit** — When you have a spec and want to know what's missing, ambiguous, or contradictory. Use this before investing in detailed design or implementation.

**Spec Synthesize** — When you want to go from a high-level spec to a complete low-level design through a structured Q&A process. Use this to close all open questions and validate cross-section compatibility.

## Principles Emphasized

This domain most strongly exercises:
- Ontology First (domain model before features)
- Principled Lossyness (behavioral what, never implementation how)
- Epistemic Sequencing (domain → contracts → flows → quality → lifecycle)
- Cross-Layer Validation (compatibility matrix in the synthesis instrument)
