# Audit Findings Register

## Audit — 2026-03-29

**Scope:** Phases 1 & 2 (Scaffold + GAN Model)
**Mode:** Formal-stage (GDS encodings present)
**Audited artifacts:** `models/gan/model.py`, `models/gan/artifacts/*`, `docs/research-journal.md`, `docs/philosophy.md`, `docs/manifesto.md`

| ID | Layer | Severity | Status | Summary | Resolution |
|----|-------|----------|--------|---------|------------|
| F-001 | 5 | Critical | **Resolved** | Verification report claims 10/10 but full suite is 22/23 with 1 failure (S-005) | Verification now runs full OGS+GDS suite (27+11 checks). S-005 warning documented as false positive for environment-sourced utility topology. |
| F-002 | 2 | Significant | **Resolved** | Discriminator's Ground Truth Label backward_in port is unwired | Added `PatternInput("Ground Truth Labels")` wiring to Discriminator. S-005 remains as warning (check doesn't inspect PatternInputs). Documented in Known Limitations. |
| F-003 | 3 | Significant | **Resolved** | Failure modes attributed to operator class (Entry 7) but actually depend on observation symmetry (Entry 8) — contradictory causal stories | Entry 7 revised: failure modes now "associated with" operator class, with explicit note that they depend on the full three-axis combination (operator, observation, enforcement). |
| F-004 | 5 | Minor | **Documented** | RDF uses `isTemporal`, IR uses `is_corecursive` — naming mismatch across layers | Documented in Known Limitations section of research journal. Framework-level issue in gds-owl. |
| F-005 | 5 | Minor | **Resolved** | Journal's `.loop()` notation is not valid OGS syntax — actual API is `CorecursiveLoop` | Added notation key at top of research journal mapping shorthand to OGS API names. |
| F-006 | 2 | Significant | **Documented** | Terminal conditions and exit conditions are strings, not computable — convergence claim is external to the formalism | Documented in Known Limitations. Convergence claims are structural preconditions, not formal proofs. Making them computable requires extending GDS with state predicates. |
| F-007 | 2 | Minor | **Resolved** | `noise_source` and `real_data` CovariantFunction objects are declared but never composed | Removed dead objects from model. Removed unused `CovariantFunction` import. |
| F-008 | 0 | Minor | **Resolved** | "symmetric_antagonism" tag on individual players conflates system-level and component-level properties | Tags reduced to role-level only (`"role": "generator"`, `"role": "discriminator"`). System-level classification lives in the comparison report. |
| F-009 | 5 | Significant | **Resolved** | Entry 1's "structurally identical" claim contradicts Entry 7's revised taxonomy | Entry 1 revised with inline correction noting that the shared pattern is information asymmetry failure, not composition topology. Entry 2 table updated to use correct operator names. |

### Convergence status: Reached

All 9 findings addressed:
- 7 Resolved (code/docs fixed)
- 2 Documented (known limitations of the formalism, not modeling errors)

No blocking findings remain. The S-005 warning is an accepted false positive for this topology, documented with justification.
