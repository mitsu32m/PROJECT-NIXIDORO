# SYS-002 / HV-003 — Passive versus switched discharge: power and fail-safe contract
Date: 2026-11-23 20:00 JST. Role: Chat A deep-design. Related issues #6, #8, #9. **PENDING REVIEW; NO FORMAL CLAIM**.
Branch: `codex/reva-integrated-prototype-review`. Starting branch HEAD: **NOT VERIFIED** (connected GitHub interface did not expose branch-specific HEAD; do not substitute default-branch commit-search result).
Result: **CONDITIONAL** for the ideal power/energy equations; **NO-GO (limited)** for assuming a control-gated discharge circuit is intrinsically fail-safe; **BLOCKED** for component selection and hardware approval.

## Task contract / difference from previous work
Previous A 16:02 report established a lower bound on continuous heat for *two always-connected* passive branches that each survive a single branch-open fault. This run compares the same passive envelope with a switched discharge path, emphasizing the additional energy cut-path and fail-open/fail-closed cases. Exit criterion: consistent load budget and state/fault contract, with explicit testable evidence missing. This is **not** a proposal to adopt any switch or revise 60V/5s as a safety requirement.

## Repository evidence consulted
Requested branch files: `docs/ai-workflow.md`, `docs/verification/handoff.md`, `docs/verification/open-issues.md`, `docs/verification/decisions.md`, `docs/tech-tree.yaml`, `docs/tech-tree.md`, latest known A 16:02 report; GitHub Issues #6 and #9. Branch-wide report enumeration and start HEAD remain unavailable from this connector; recent B/C completeness is **UNKNOWN**. No formal atomic Claim is available. Shared indexes deliberately unchanged for integration/review.

## Numerical assumptions (not guaranteed component ratings)
- Target HV output 205 V at 16 mA = 3.280 W, **TARGET**.
- 220 V initial shutdown, 60 V endpoint, 5 s limit, Cmax=12 uF, +/-5% resistors: **ASSUMED illustrative only**, not safe-touch standard.
- Two always-connected independent 300 kohm branches, worst actual Rmin=285 kohm: **ASSUMED**.
- HV converter efficiency eta=0.60, 0.75, 0.85: **ASSUMED sensitivity**, not a manufacturer guarantee at 205V.
- Switched branch disabled in run state with zero leakage: **IDEALIZED**; actual off leakage, gate drive, standby and switch withstand ratings **UNKNOWN**.
- Ideal isolated capacitor exponential decay after *all* HV energy sources stop; continued energy injection and common-cause failures excluded from numerical RC model.

## New quantitative comparison: low-voltage input penalty
The always-connected dual-branch bleeder dissipates `Pbleed = 2*V^2/Rmin`.
At 205V: `Pbleed = 2*205^2/285000 = 0.29491 W`. At 220V: `0.33965 W`.
For a converter supplying the same useful lamp demand, the **incremental input** due solely to this bleeder is `Delta Pin = Pbleed/eta` (assuming efficiency unchanged; actual operating-point efficiency may change).
At 205V: eta=0.60 -> 0.4915 W; eta=0.75 -> 0.3932 W; eta=0.85 -> 0.3470 W.
At 5V upstream, equivalent incremental current is respectively 98.3mA, 78.6mA, 69.4mA **before** upstream regulator losses.
At 205V the bleeder adds 8.99% to the target 3.28W HV useful output. The percentage is not an estimate of total battery penalty.
At a **hypothetical** upstream 5V efficiency of 0.90, eta=0.75 case adds 0.4369 W drawn from the upstream source, not necessarily the cell (power-path modes differ).

## Shutdown pulse versus run-state heat
For Cmax=12uF and V0=220V, stored energy is `0.5*C*V0^2 = 0.2904 J`; energy dissipated *until 60V* is `0.5*C*(220^2-60^2) = 0.2688 J`.
If discharged once per 25-minute cycle, the long-run average of the entire 0.2904J discharge is only `0.2904/1500 = 0.0001936 W`, excluding leakage, HV charging loss, switch/control losses and any other cycles. A switched architecture could therefore greatly reduce *continuous* heat compared with always-on bleeders, but the safety and component tradeoff dominates; energy savings alone cannot qualify it.
At Rmax=315kohm for one surviving branch, ideal discharge time `t=Rmax*Cmax*ln(220/60)=4.9113 s`; **only if the discharge switch actually connects that branch** and HV source is no longer injecting energy.

## Failure-mode contract: do not conflate shutdown command with discharged output
| Condition | Always-on dual passive | Switched discharge (unqualified) | Required evidence |
|---|---|---|---|
| HV running normally | ~0.295W worst-corner continuous at 205V | nominally off; off-leakage unknown | voltage/temperature derating, leakage |
| MCU reset / firmware hang | branches remain physically connected | command may not turn switch on | independent hardware default-on mechanism |
| USB/battery loss | passive branches remain connected to C if wiring intact | auxiliary gate drive may disappear | no-power switch state proven at residual 220V |
| One resistor branch open | remaining branch discharges within *assumed* 5s if connected | single switched path can become completely open | separate independent physical discharge path |
| Switch stuck OFF/open | not applicable | discharge unavailable | fail-open mitigation or monitored redundancy |
| Switch stuck ON/short | not applicable | becomes permanent bleeder, heat and input budget return | resistor continuous rating and thermal fault response |
| Shared HV/GND trace open | both paths may fail | both paths may fail | placement and common-cause review |
| HV stage fails ON | discharge may be unable to pull voltage down | same; discharge switch cannot substitute for HV hard-off | independent converter energy isolation + OVP |
| Capacitor at 220V, external supply off | passive decay if connected | default-on behavior must work without external supply | real schematic, guaranteed parts, controlled test |

A 'normally-on' device alone is not a proven solution: its actual VDS, VGS, off-state leakage, maximum current, gate drive reference, and behavior with the output voltage collapsing all require a complete topology. Mechanical or solid-state switching and monitoring can introduce additional single points of failure. **No particular active discharge topology is selected.**

## Architecture gate and next experiment (design-only)
1. Identify real Cmax and approved discharge endpoint/time; until then 12uF/60V/5s remains a scenario.
2. Draw HV node, both discharge branches, actual switch/gate bias return, independent hard-off and ground return as a *fault-path schematic*, not merely a block diagram.
3. For MCU off, 5V off, cell removed, USB removed, output still charged, switch stuck open/closed, resistor open, common trace open: prove whether energy can flow to a discharge path and whether a single failure defeats the objective.
4. If switched path remains attractive, source manufacturer-guaranteed switch leakage, voltage withstand, thermal and fail-state behavior; calculate worst Cmax and converter tail energy. Include actual off-state leakage/standby, peak resistor dissipation, pulse energy, voltage rating and HV insulation.
5. Have Chat C independently check fault assumptions and arithmetic; Work decides any shared-index update. Do not promote to schematic/BOM without user approval.

## Disposition
**CONDITIONAL**: ideal power and shutdown-energy comparison.
**NO-GO (limited)**: treating MCU-gated or unpowered switched bleeder as inherently fail-safe or claiming zero run-state heat without leakage data.
**BLOCKED**: actual HV capacitor, independent converter stop, manufacturer-qualified switching topology, worst-case faults, physical common cause and reviewed safe discharge criterion.
**PENDING REVIEW**: Chat C; no formal adoption.

No purchases, PCB manufacture, HV energization, main merge, or unapproved specification changes.
