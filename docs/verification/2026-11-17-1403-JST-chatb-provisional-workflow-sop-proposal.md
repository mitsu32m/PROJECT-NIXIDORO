# Chat B proposal — non-blocking provisional research workflow (SOP amendment request)

- Date: 2026-11-17 JST
- Status: **PENDING REVIEW** (human owner has explicitly directed provisional work; this is a proposed amendment to `docs/ai-workflow.md`, not an unreviewed shared-index overwrite)
- Scope: Chat B and, if adopted by the integrator, all scheduled research workers
- Source: owner instruction of 2026-11-17; related [Chat B SYS-001 report](2026-11-17-1403-JST-chatb-sys001-supply-mode-alternatives.md)
- Branch: `codex/reva-integrated-prototype-review`
- Starting SHA: `41a9eaae6b00131915b523a251952f9678ddc2fe`
- Formal GitHub Claim: **NONE**; this file is an append-only, uniquely named worker proposal.

## Proposed text for docs/ai-workflow.md

Add the following section under §7, after existing single-writer coordination rules:

> ### Non-blocking research when GitHub Issues/Claim is unavailable
>
> 1. When a concurrency-safe GitHub Issues Claim mechanism is functional, a worker must acquire an eligible role-specific task using that mechanism.
> 2. If Claim is unfinished, the issue queue is empty, or GitHub Issues is impaired, **do not stop technical research solely for that reason**. Read `docs/verification/open-issues.md`, `docs/tech-tree.yaml`, `docs/tech-tree.md`, recent verification logs and relevant existing GitHub Issues. Select one bounded, non-duplicative research question within the worker's assigned role and give it a stable provisional task ID.
> 3. Provisional research is **not** a formal Claim. Do not imply exclusive ownership or override an existing claimed task. Avoid collisions by checking latest commits/reports immediately before writing; write a uniquely named dated Markdown report instead of editing shared indexes.
> 4. Record primary-source links, exact assumptions, equations, conditions, alternatives, unresolved risks and next deep-dive tasks. Label new findings **PENDING REVIEW** and explicitly hand off to Chat C for independent review. The integrator alone adopts decisions or updates shared handoff/issues/decisions/tech-tree indexes, unless an explicitly coordinated exception is approved.
> 5. If a new issue or alternative is found, record it in the dated report and, where safe and non-duplicative, link or create a GitHub Issue. Do not treat an Issue write as an atomic Claim.
> 6. If GitHub write access fails, report **NOT COMMITTED** and the exact attempted file; never claim a save that did not occur.
> 7. A worker must **not** stop, delete, or change its own scheduled task due to Claim/Issue failures, nor change scheduling without explicit owner instruction. Never resume other stopped tasks.
> 8. Hardware purchasing, PCB manufacturing, HV energization, merging to main, design requirement changes and safety approval remain prohibited without explicit authorization.

Update §9 only to replace the potentially misleading fixed `08:00, 14:00, 21:00` sentence with:

> Each worker's actual recurrence and enabled state are defined by the task scheduler, **not** by this SOP. Chat B currently has an owner-requested schedule of 01:00, 05:00, 09:00, 13:00, 17:00 and 21:00 Asia/Tokyo, but schedules may differ per role. The worker must not autonomously pause or change its schedule due to research or GitHub coordination blockers.

## Why the amendment matters

Current §1(5) requires an issue ID and §5 asks for a parent issue. Under incomplete Claim infrastructure, that wording can be interpreted as a stop condition even though technical IDs such as SYS-001 already exist in the Markdown ledger. Clarify that a **technical issue ID plus explicit provisional label** satisfies a bounded research contract until GitHub Issue mapping and atomic Claim are implemented. This is not a waiver of concurrent-write safety, independent review or HV safety gates.

## Review / adoption request

Chat C: check that the fallback cannot be misrepresented as an exclusive Claim and that the review state is explicit. Work/integrator: reconcile this proposal into `docs/ai-workflow.md` with current HEAD and latest changes; do not silently overwrite other concurrent SOP edits. Owner's instruction to continue technical research is already operative for Chat B, independently of whether this proposal has been merged into the canonical SOP.
