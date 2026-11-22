# C-REVIEW-022 — THERM-001 / HV-003 discharge and SYS-001 efficiency batch
Date: 2026-11-23 09:00 JST. Role: Chat C independent first review. **NO FORMAL CLAIM; NO HARDWARE SAFETY APPROVAL**.
Repository: https://github.com/mitsu32m/PROJECT-NIXIDORO
Branch: `codex/reva-integrated-prototype-review`
Verified starting branch HEAD via GitHub fetch_commit(branch): `3e8b5e194d6cc8dcffd6e13ee88f7f7721fa8f14`.
Previous review C-021: `29043fe8c3705c338e5403c236b85098cfeac117`.
Changed since C-021: exactly 3 added research files per compare_commits (no other changed files in that comparison).
Scope: GitHub #9, #6, #8, #4. Review three PENDING REVIEW reports (A 04:02, B 05:00, A 08:04 JST) as one related power/safety batch. No index edits, KiCad edits, purchase, energization, fabrication or requirements change.

## Evidence and provenance
- A 04:02: [THERM-001 cutoff and residual energy](2026-11-23-0402-JST-THERM-001-independent-cutoff-residual-hv-energy-contract.md), commit `29043fe8c3705c338e5403c236b85098cfeac117` parent of new commits.
- B 05:00: [SYS direct-vs-cascade](2026-11-23-0500-JST-chatb-sys001-direct-sys-vs-5v-flyback-power-contract.md), commit `e2f605d419bcbfd22ae74c1d9e9d9d8a142390e9`.
- A 08:04: [bleeder Cmax](2026-11-23-0804-JST-THERM-001-hv-bleeder-cmax-discharge-envelope.md), starting branch HEAD not verified by author; reviewed content exists at current branch HEAD.
- Read SOP, handoff, open-issues, decisions, YAML and Mermaid tech-tree from branch. GitHub Issues #4/#6/#8/#9 and recent comments read. Shared handoff remains an older 2026-11-19 snapshot; not silently assumed current.
- TI BQ25185 Rev.B https://www.ti.com/lit/ds/symlink/bq25185.pdf and ADI LT3757A https://www.analog.com/en/products/lt3757.html are cited in A/B, **not independently freshly retrieved in this C run**. Manufacturer-specific feature statements are therefore not newly ACCEPTED as primary-source checks.
- Numeric inputs C=1/4.7/10uF, R=1Mohm/330kohm, 220V/60V, 5s, eta5=.90, etaHV=.75, etaDirect=.70/.75 are **ASSUMED**. 205V/16mA is a TARGET. Physical measurements: NONE.

## Independent numerical verification (recomputed, not copied)
Ideal passive RC: `E=.5*C*V^2; t=R*C*ln(V0/Vf); P=V^2/R`.
- At 220V: 1uF -> 24.200mJ, 1Mohm -> 1.299283s; 4.7uF -> 113.740mJ, 6.106630s; 10uF -> 242.000mJ, 12.992830s.
- 10uF, 220->60V within assumed 5s requires ideal R<=384827.64ohm; 330kohm gives 4.287634s, 146.667mW at 220V, 127.348mW at 205V. At 60V, 10uF retains 18.000mJ.
- A 04:02 example 1uF at 205V -> 21.0125mJ, 1Mohm -> t=ln(205/60)=1.228665s, P=42.025mW. Numerically correct within rounding.
- B 05:00: 205*.016=3.280W; cascade 3.28/(.90*.75)=4.859259W; direct at .75=4.373333W; direct at .70=4.685714W. Equal-.75 direct saves .485926W; break-even etaDirect=.675, **strictly > .675** for improvement assuming same other losses. Ideal USB 5V*.5A=2.50W <3.28W even before losses. With optimistic full 2.50W delivered to SYS, battery deficits are 2.359259/1.873333/2.185714W; divided by 3V: .786420/.624444/.728571A. BAT-only at ideal 3V: 1.619753/1.457778/1.561905A. All arithmetic agrees within rounding.
- Counterexample to unconditional direct superiority: etaDirect=.65 -> 3.28/.65=5.046154W, **worse** than 4.859259W cascade.

## Claim-by-claim review
| Claim | Judgment | Boundary / correction |
|---|---|---|
| Charge inhibit, BAT-only load isolation and residual HV discharge are distinct safety functions | **ACCEPTED** as functional decomposition | /CE-only is not an HV isolation or capacitor discharge proof. No specific physical architecture adopted. |
| A 04:02 ideal residual energy/RC values | **ACCEPTED** arithmetic only | 60V and 5s are not user-safe thresholds; bleeder-open and tail-energy invalidate a safety claim. |
| A 08:04 Cmax/RC/power numerical table | **ACCEPTED** ideal arithmetic | 4.7/10uF with 1Mohm exceed assumed 5s. Continuous dissipation must enter thermal budget. |
| 330kohm/10uF as actual discharge solution | **BLOCKED** | Rmax/Cmax/temp, rated working voltage, series resistors, creepage, single fault, HV tail energy and stored energy after 60V UNKNOWN. |
| B 05:00 direct-SYS efficiency crossover | **ACCEPTED** ideal algebra | efficiency and auxiliary losses ASSUMED; direct topology not automatically better. |
| USB-only full 205V/16mA with 5V/500mA source | **ACCEPTED** impossibility under that power cap | Even ideal source power below HV output; not a claim about reduced display modes. |
| Actual USB+BAT current and cell/charger thermal qualification | **BLOCKED** | Delivered USB current, battery path efficiency, BATFET, PCM, low-cell, startup, transients and charge state UNKNOWN. |
| TI/ADI part-specific electrical feature assertions | **CONDITIONAL** | Not freshly independently cross-checked against manufacturer controlled documents in this review. |

## Adversarial faults and system effects
1. /CE stuck low: cannot inhibit charge by /CE; sensor fault/MCU-off/monitor power loss require independent default-inhibit path. BQ TS in BAT-only was previously reviewed as inactive, but not reverified in primary PDF this run.
2. PCM disconnect / battery-only thermal cutoff: load switch-off is not removal of stored HV. Bleeder-open leaves an uncontrolled discharge time; single-fault discharge coverage unresolved.
3. 10uF capacitor with 330kohm dissipates 0.147W at 220V continuously, **if held at 220V**. This is an enclosure thermal load in addition to controller, transformer, diode, HV5524 and BATFET. Cannot infer cell temperature without thermal resistance and geometry.
4. Larger Cmax improves some post-trip energy headroom but increases stored energy, startup charge and discharge time; Cmin and Cmax must be evaluated together, not chosen separately.
5. No actual resistor working-voltage ratings, capacitor effective Cmin/Cmax at bias/temp/age, independent OVP trip tolerance, guaranteed stop delay, magnetic tail energy, low-cell power path, thermal trip path or actual KiCad trace were established. No physical tests.

## Work decision package (only consequential items)
**Decision A — mandatory protection-function separation** (#9/#6): Chat A argues /CE cannot perform charge inhibit, BAT-only HV cutoff and residual discharge simultaneously. Independent review accepts this logical decomposition, not a component selection. Recommend Work preserve three separate verifiable safety contracts and request a power-state/single-fault path matrix with actual schematic/pack evidence. Alternative qualified pack/independent cutoff circuits remain open. Impacts PWR, CTRL, HV, BOM and PETG enclosure.
**Decision B — passive bleeder heat versus Cmax** (#6/#8): A reports 10uF, 330kohm ~4.288s and 0.147W at 220V; independently reproduced. Recommend Work explicitly include Cmax discharge energy and bleeder continuous loss in thermal budget, and do not adopt 330kohm. Alternative dual redundant paths or supervised discharge require engineering proof; no part qualified.
**Decision C — direct-SYS architecture comparison** (#4/#2): B claims ideal break-even direct eta >67.5%, independently reproduced; direct .65 is a counterexample. Recommend Work add measured/guaranteed efficiency and input/startup/thermal conditions to topology comparison rather than selecting direct-SYS. No qualified controller+magnetics pair.

Source URLs: above report paths, https://github.com/mitsu32m/PROJECT-NIXIDORO/issues/9 , /issues/6 , /issues/8 , /issues/4 and manufacturer links above. Baseline HEAD `3e8b5e194d6cc8dcffd6e13ee88f7f7721fa8f14`; this review's resulting commit SHA is the GitHub commit containing this file.

## Queue and next priorities
New research reports since C-021: **3**; independently reviewed this run: **3**; unreviewed among these three after review: **0**. Historical outstanding review total **UNKNOWN** (no exhaustive provenance/status reconciliation); oldest historical pending issue/report **UNKNOWN**. Oldest in this bounded batch: 2026-11-23 04:02 JST (A THERM-001).
Priority next: (1) actual OVP Cmin/Cmax and guaranteed tail energy plus bleeder single-fault discharge; (2) independent charge/BAT-only thermal cutoff under /CE-short and MCU-off; (3) actual cell/PCM/BATFET/low-cell and 5V startup thermal; (4) sourceable HV magnetics/controller and direct-SYS comparative efficiency.
Status: research arithmetic reviewed; **actual protection/HV/pack design BLOCKED**. Hand off this report to Work. Shared indexes unchanged by Chat C.
