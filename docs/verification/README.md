# Verification ledger — PROJECT-NIXIDORO

Status: **research and design review only; not approved for PCB manufacture, purchasing, or high-voltage energization.**
Created: 2026-11-17 JST. Current working branch: `codex/reva-integrated-prototype-review`.

## Read first (for any AI or human contributor)

1. [handoff.md](handoff.md) — current system state, source-of-truth hierarchy, critical blockers, next steps.
2. [open-issues.md](open-issues.md) — live issues, priority, exit criteria and evidence.
3. [decisions.md](decisions.md) — decisions/proposals/rejections and supersession.
4. Chronological verification reports in this directory: `YYYY-MM-DD-HHMM-JST-<topic>.md`.
5. Original technical records: [integrated review](../reva-integrated-prototype-review.md), [HV architecture](../hv-architecture-decision.md), [HV voltage tolerance window](../hv-voltage-window.md), [transformer screening](../hv-transformer-screen.md), [integrated net spec](../reva-integrated-net-spec.md).

## Required report format for every scheduled verification

- **Record ID, JST timestamp, author/AI, repository branch and examined commit SHA**. Never guess a SHA.
- **Question and scope**: exact unresolved issue, what is and is not being evaluated.
- **Starting evidence**: exact GitHub file paths, manufacturer's primary references including document revision, table/figure/page where accessible, access date.
- **Inputs**: part numbers, circuit conditions, temperature, tolerances, units; tag each input `[GUARANTEED]`, `[TYPICAL]`, `[ASSUMED]`, `[MEASURED]`, `[UNKNOWN]`.
- **Analysis**: formula derivation, intermediate values, worst cases, physical limitations and model validity.
- **Alternatives**: evaluated and rejected approaches with actual reasons; don't simply omit discarded ideas.
- **Decision**: `GO` (only scope verified), `CONDITIONAL`, or `NO-GO` plus criteria for change.
- **Open questions**: test/measurement or document required to close each.
- **Delta vs previous review**: what changed, whether the older conclusion is superseded.
- **Next action**: one concrete bounded follow-up that an unbriefed AI could execute.
- **Evidence integrity**: identify unverified quotations, failed tools and missing primary data. Never claim simulation, ERC or hardware verification that was not performed.
- **Commit and artifacts**: all modified paths, calculation code/CSV where relevant, commit hash and permalink. If no commit, explicitly say `NOT COMMITTED`.

## History and governance

- Retain past verification reports. Do not erase historical counterexamples; mark superseded with link to newer record.
- `decisions.md` is a register, not an authorization to purchase or energize. Keep conceptual proposal and approved design clearly separate.
- Use a **documentation-only** commit on working branch for scheduled reviews. Do **not** alter KiCad designs, main branch, BOM purchase instructions, manufacturing output, cell charging limits or electrical safety circuits automatically.
- If GitHub tools are unavailable, return a complete review in ChatGPT with `NOT COMMITTED`; do not claim progress was saved.
- Scheduled reviews must check the newest index and previous report to avoid repeating the same investigation.
- Note elapsed time and source freshness. Inability to obtain a manufacturer's actual transformer electrical datasheet is a blocker, not evidence of compatibility.

## Current schedule (as of 2026-11-17)

ChatGPT verification runs three times daily at approximately 08:00, 14:00, 21:00 JST; system-level review is weekly Wednesday ~19:00 JST. **Schedule may be changed independently; this file is a snapshot, not scheduler configuration.**

## Repository limitations

The files in `hardware/hv/RevA-draft` intentionally contain a non-functional placeholder, not a usable 200 V converter. ERC alone does not establish feasibility, safety or fit for fabrication. The project has no approved design for HV generation, independent OVP, reliable discharge or touch protection.
