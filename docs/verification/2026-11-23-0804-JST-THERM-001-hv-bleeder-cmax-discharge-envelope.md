# THERM-001 / HV-003 — Passive bleeder Cmax and thermal-stop residual-HV envelope
Date: 2026-11-23 08:04 JST
Role: Chat A / deep-design; GitHub Issue #9, related #6/#8. **PENDING REVIEW; NO FORMAL CLAIM**.
Branch: `codex/reva-integrated-prototype-review`.
Starting HEAD SHA: **NOT VERIFIED** (GitHub connector branch-specific HEAD unavailable in this run; search_commits returned historical/default-branch results and must not be substituted).
Result: **CONDITIONAL** for ideal RC arithmetic; **BLOCKED** for safety discharge and thermal interlock implementation.

## Bounded task and delta
After the 2026-11-23 04:02 report separated charge inhibit, battery load cutoff and residual HV discharge, quantify how the *unselected* output capacitor Cmax alters residual energy, decay time and continuous bleeder heat. This is **not** a repetition of its 1uF/1Mohm example: here the design question is whether a discharge-time objective can coexist with sealed-enclosure standby dissipation, resistor voltage rating and single-fault requirements. No hardware or threshold selection.

## Sources and evidence class
- Repository `docs/ai-workflow.md`, `docs/verification/handoff.md`, `docs/verification/open-issues.md`, `docs/verification/decisions.md`, `docs/tech-tree.yaml`, Issue #9 and comments, latest known A 04:02 report: reread on this branch during this run.
- C-REVIEW-020 (2026-11-22): BAT-only cutoff remains BLOCKED (Issue #9 comment).
- Output nominal 205V/16mA is a **TARGET**, not a measured operating point. Upper evaluation 220V is an **ASSUMED analysis corner**, NOT an acceptable operating/fault limit; HV5524 limit and OVP dynamics remain independently open.
- C=1, 4.7, 10uF, R=1Mohm or 330kohm, 60V and 5s are all **ASSUMED study values**, not selected, guaranteed, or touch-safe criteria. No part manufacturer rating or tolerances verified in this report.
- Ideal passive bleeder: E=0.5*C*V^2; t=RC*ln(V0/Vtarget); P0=V0^2/R. Ignores converter tail energy, capacitor voltage derating, temperature, resistance tolerance, leakage and resistor failures.

## Reproducible calculations
At 220V, initial stored energy:
| Assumed C | E at 220V | t(220->60V), R=1Mohm |
|---|---:|---:|
| 1uF | 24.20mJ | 1.299s |
| 4.7uF | 113.74mJ | 6.106s |
| 10uF | 242.00mJ | 12.993s |

For the **illustrative** 10uF, 220->60V in <=5s target, the *ideal nominal* maximum bleeder resistance is R <= 5/[10e-6*ln(220/60)] = **384.8kohm**. A hypothetical 330kohm yields **4.288s** and **146.7mW continuous dissipation at 220V** (127.35mW at 205V). The energy at 60V with 10uF remains 18mJ. 330kohm/10uF is **NOT A RECOMMENDED COMPONENT SELECTION**. Worst-case Cmax, Rmax, voltage, time and environmental temperature can invalidate 5s.

## New cross-system result
1. The residual-HV stop requirement creates a *permanent enclosure heat load* if a passive bleeder is used. For 10uF at the assumed 5s objective, the illustrative resistor dissipation is about 0.147W at 220V; this must enter #8 sealed PETG/pack heat accounting rather than being treated as a free safety feature.
2. Battery-only thermal cutoff or PCM opening does not guarantee discharge. If the bleeder opens, the RC decay guarantee disappears even if all upstream switching is disabled. Independent single-fault coverage is still **BLOCKED**.
3. A guaranteed safe-stop claim needs the **selected** capacitor Cmax and resistor network with rated working voltage, pulse/continuous power, temperature drift, tolerances and failure analysis; also guaranteed converter tail energy and supervised discharge tests. Do not define 60V as safe-touch merely because it was used for arithmetic.
4. Charge-inhibit and load-isolation circuits remain separate from HV discharge; this report does not qualify /CE or battery-only monitoring. No MCU-only safety claim.

## Review/decision gates
- **CONDITIONAL**: Ideal RC and power bounds as explicitly assumed.
- **NO-GO (limited)**: Claiming a 1Mohm bleeder always meets a 5s 220->60V objective for 4.7uF or 10uF; ideal times already exceed 5s.
- **BLOCKED**: actual Cmin/Cmax, selected resistor voltage/power and thermal design, fault-open coverage, HV shutdown tail energy, OVP and human-safe voltage/time, thermal sensor/load cutoff, and hardware qualification.
- **PENDING REVIEW**: independent Chat C challenge required; Work may integrate only scoped arithmetic, not adopt values.

## Next bounded work
#6/#8 joint selection must supply actual capacitor Cmin/Cmax, converter stop/tail bound and allowed thermal dissipation. #9 must define monitor power domain, MCU-off default-off load path and independent charge interruption with /CE short-GND. Chat B should obtain exact parts; Chat C review this RC/thermal coupling. Update shared indexes only through designated integrator to avoid concurrent writes.

No purchase, PCB fabrication, HV energization, main merge, KiCad modification or requirement change.
