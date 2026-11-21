# HV-001 / Issue #2 — DCM magnetizing inductance and peak-current coupled constraint
Date: 2026-11-21 11:55 JST. Role: Chat A deep-design. Branch: `codex/reva-integrated-prototype-review`.
**PENDING REVIEW — CONDITIONAL analytical screen; BLOCKED hardware feasibility. NO FORMAL CLAIM.**

## Bounded task contract
Question: Assuming the 1:10 example from Chat A 08:00 is *actually* a single-switch flyback-like discontinuous-magnetizing-current stage, what primary magnetizing inductance and switch peak-current combination can transfer 205V x 16mA continuously at 4.75V? This explicitly does NOT identify the Zhang/ehbtj coupled-inductor topology or qualify MAX668.
Issue #2: https://github.com/mitsu32m/PROJECT-NIXIDORO/issues/2
Read: docs/ai-workflow.md, docs/verification/handoff.md, docs/verification/open-issues.md, docs/verification/decisions.md, docs/tech-tree.yaml, docs/tech-tree.md, 2026-11-21-0800-JST-HV-001-max668-duty-turns-ratio-screen.md and Chat B 09:01 LT8365 report, Issue #2 and open issue register. Latest entire verification tree and exact starting branch HEAD not independently enumerated: **UNKNOWN**. GitHub search_commits yielded older default-branch commits, which are not branch HEAD. Shared indexes not edited to avoid concurrent writers.

## Primary evidence and input provenance
- ADI MAX668/MAX669 manufacturer datasheet https://www.analog.com/media/en/technical-documentation/data-sheets/MAX668-MAX669.pdf ; controller current limit, maximum duty at chosen ROSC, frequency and MOSFET/sense implementation need part-specific guarantee verification. **No guaranteed controller peak current asserted here.**
- Existing actual magnetics screening: docs/hv-transformer-screen.md; Würth 750315839 https://www.we-online.com/components/products/datasheet/750315839.pdf ; Sumida T086/T087 manufacturer sheets cited in prior 08:00 report. **No actual Lm, Isat, DCR, leakage or pinout confirmed in this calculation.**
- Pout=205V x 0.016A=3.280W (TARGET); Vin=4.75V, D=0.81262 (ASSUMED illustrative ideal 1:10 flyback ratio); efficiency eta=0.70/0.80/0.85 (ASSUMED, not measured); switching frequency f=100kHz (ASSUMED, not MAX668 guarantee at a selected ROSC).
- Chat B 09:01 LT8365 work is a different topology and was not duplicated.

## Reproducible derivation
For **single-switch DCM flyback with complete reset each cycle**, linear current rise and negligible residual magnetizing current:
Ipk = Vin D/(Lm f).
Pout = eta (1/2) Lm Ipk^2 f = eta Vin^2 D^2/(2 Lm f).
Thus Lm_required = eta Vin^2 D^2/(2 Pout f), and Ipk_required = 2 Pout/(eta Vin D). These are simultaneous necessary values for a fully DCM design at the assumed fixed duty; neither may be selected independently. For operation with D <= Dlim, Lm must not exceed the value computed at Dlim if this DCM power transfer model is applicable.
At Vin=4.75V, D=0.81262, f=100kHz:
| eta assumed | Lm for 3.28W (uH) | Ipk (A) | Pin (W) | input average (A) |
|---|---:|---:|---:|---:|
| 0.70 | 15.91 | 2.435 | 4.686 | 0.986 |
| 0.80 | 18.18 | 2.131 | 4.100 | 0.863 |
| 0.85 | 19.32 | 2.006 | 3.859 | 0.812 |

Example at eta=0.80, Lm=47uH and 100kHz, maximum idealized DCM output power at D=.81262 is **1.269W**, not 3.28W. At Lm=22uH it is **2.711W**. This is a *conditional DCM exclusion* of these inductances at that frequency/duty/efficiency, NOT a universal exclusion of those magnetics or of CCM.

Important adversarial check: DCM complete reset imposes a secondary demagnetization time. For an ideal flyback, Dreset = Vin D N/(Vout+Vd). At N=10, Vout+Vd=206V, Vin=4.75V and D=.81262, Dreset≈.18738, giving D+Dreset≈1: **the earlier duty equality is the CCM/BCM volt-second boundary**, not a DCM point with margin! A physically DCM solution must use **D smaller than .81262** at the same ratio and voltage, which reduces the maximum allowable Lm and increases Ipk. For example D=.75, eta=.80, 100kHz: Lm=15.48uH, Ipk=2.302A, Dreset≈.17294, leaving ~.077 cycle idle. Thus using the prior .81262 as a practical DCM operating point is invalid; the 18.18uH entry is an optimistic boundary, not a qualified component selection.

## Faults and qualification gates
- Coupled-inductor boost vs flyback identity is still UNKNOWN. If primary winding remains electrically tied to output/diode differently, the above transfer and reset equations can be **wrong**. Obtain original schematic, dot orientation and switching conduction states before adopting any number.
- Peak MOSFET current needs **actual MAX668 sense/current limit guaranteed bounds** and startup/saturation/temperature; Ipk here is ideal triangular primary magnetizing current, not guaranteed drain current under leakage, faults or CCM.
- VDS and diode reverse voltage require winding connections, leakage L, clamp, overshoot and parasitics. Cannot infer from ideal ratio alone.
- 4.75V input is not necessarily the worst low-cell SYS/5V startup corner. Frequency, actual Lm tolerance, core loss, DCR, flux swing, core thermal and thermal enclosure must be bounded.
- 220V HV5524 recommended limit is not an OVP trip target. Independent hardware shutdown, capacitor tail energy and discharge remain unqualified.
- Pout 3.28W already exceeds 5V x 0.5A USB budget before loss, so battery assist or altered operating mode is mandatory for that scenario; no target changed.

## Disposition and handoff
**CONDITIONAL**: For a *verified flyback-like DCM circuit* at eta=.80, 4.75V and 100kHz, D=.75 requires approximately Lm=15.48uH and Ipk=2.30A, before tolerance/fault margin.
**NO-GO limited**: Treating the earlier D=.81262 equality as a DCM operating point with idle-time margin; or claiming 47uH/100kHz/.81262 can supply 3.28W in the stated DCM model.
**BLOCKED**: MAX668 original coupled-inductor schematic identification, selected magnetics, full-temperature current limit, actual losses/thermal/startup and independent OVP.
**PENDING REVIEW**: Chat C should independently challenge topology and DCM/BCM boundary. Work should not promote this screen to a BOM.
Next: retrieve exact original circuit switching states and candidate magnetics Lm/leakage/Isat, then evaluate current/voltage/thermal at verified switching frequency and low-Vin.
No purchase, PCB manufacturing, HV energization, main merge, important spec or KiCad modification.
