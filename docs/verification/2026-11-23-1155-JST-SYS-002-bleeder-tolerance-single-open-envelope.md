# SYS-002 / HV-003 — Bleeder tolerance and single-open counterexample
Date: 2026-11-23 11:55 JST. Role: Chat A deep-design. GitHub issues #6 and #9. **PENDING REVIEW; NO FORMAL CLAIM.**
Branch: `codex/reva-integrated-prototype-review`. Starting HEAD: `cd3c83bdaa88521f2445c681e905d6600c53c949`.
Result: **CONDITIONAL** for ideal RC sensitivity; **NO-GO (limited)** for treating nominal 330k/10uF as guaranteed <=5s; **BLOCKED** for physical safety architecture.

## Contract and new question
Previous A 08:04 and C-REVIEW-022 validated nominal 10uF/330kohm, 220->60V in 4.288s. This run checks whether illustrative capacitor and resistor tolerances invalidate that margin, and whether two parallel bleeder paths establish single-open coverage. Exit: independently reproducible worst-corner arithmetic and a precise design gate, not a component selection. No changes to schematic, requirements, shared indexes or hardware.

## Inputs and provenance
- 205V/16mA: **TARGET**, not measured. 220V initial and 60V endpoint, 5s objective: **ASSUMED**, not approved safe-touch limits.
- Cnom=10uF; Cmax=12uF (+20%): **ASSUMED** illustrative capacitance tolerance, NOT a manufacturer-rated capacitor. Rnom=330kohm, Rmax=346.5kohm (+5%), Rmin=313.5kohm (-5%): **ASSUMED** illustrative resistor tolerance, NOT a selected part.
- Ideal disconnected RC: `t=RC ln(Vinitial/Vend)`, `E=CV²/2`, `P=V²/R`. Ignore leakage, tail energy, bias, ageing, temperature, ESR and physical failure modes. No manufacturer-rated component or measurements.
- Baselines: [A 08:04](2026-11-23-0804-JST-THERM-001-hv-bleeder-cmax-discharge-envelope.md), [C-REVIEW-022](2026-11-23-0900-JST-C-REVIEW-022-thermal-bleeder-sys-efficiency-batch.md), D-013 and open issues SYS-002/HV-003.

## Independent sensitivity and counterexamples
At 220->60V, ln(220/60)=1.299282984:
| Illustrative configuration | Time | Other consequence |
|---|---:|---|
| 10uF, 330kohm nominal | 4.288s | Previously independently reviewed nominal |
| 12uF Cmax, 346.5kohm Rmax | 5.402s | **Exceeds assumed 5s**, even with zero converter tail |
| 12uF Cmax, R <= 320.69kohm | <=5.000s ideal | Maximum *actual* resistance; nominal 5%-tolerance choice <= 305.42kohm |
| 330kohm nominal, Rmin 313.5kohm, 220V | — | continuous dissipation 154.39mW, plus unknown switching/thermal losses |
| Two independent parallel 680kohm paths, both intact | 5.301s | Assumes exact resistors and Cmax |
| Same two paths, one open | 10.602s | Single open **defeats 5s objective** |

At Cmax=12uF, E(220V)=290.40mJ, E(60V)=21.60mJ. The endpoint is not a validated safe voltage.

## Engineering implications
1. **Nominal 4.288s does not guarantee 5s.** Any actual capacitor selection must use guaranteed Cmax (including tolerance, operating conditions and ageing) and resistor Rmax, and bound converter tail charge. Initial 220V itself is a hypothetical corner, not an accepted maximum.
2. A redundant-looking parallel bleeder network may still fail the discharge-time objective on a single-open fault. Two parallel branches must each individually meet the required single-fault discharge criterion (or an independently proven alternate discharge path must act); a parallel resistor pair alone is not evidence of fault detection.
3. Continuous bleeder power is worst at Rmin and high voltage; resistor working-voltage rating, voltage coefficient, pulse/continuous dissipation, ambient derating and series-element voltage sharing require manufacturer evidence. Parallel branch power must be added, not assumed zero.
4. A monitored active discharge might reduce continuous heat but creates supply-dependence, switch failure, detection, default-state and HV isolation questions. No architecture adopted.
5. Actual converter shutdown tail energy, Cmin for OVP and Cmax for discharge/startup, physical discharge path after PCM/USB loss, and cell-temperature exposure remain unknown. Firmware or /CE alone cannot qualify a discharge path.

## Status / handoff
**CONDITIONAL:** math and corner counterexamples under stated assumptions. **NO-GO (limited):** treating nominal 330kohm/10uF as guaranteed <=5s under illustrative +20%/+5% tolerances, or two 680kohm branches as a single-open 5s guarantee. **BLOCKED:** physical discharge safety and selected part ratings, tail energy and fail-safe test plan. **PENDING REVIEW** for Chat C; no formal adoption.
Next #6/#8: source actual capacitor Cmin/Cmax and resistor working-voltage/thermal specs, choose user/supervisor-approved endpoint/time, derive max allowable total resistance under worst-case tail, then run single-fault and low-cell/startup budget. Share with Work for index integration. No new issue: #6 already covers this gap.
No purchase, PCB manufacture, HV energization, main merge or important specification change.
