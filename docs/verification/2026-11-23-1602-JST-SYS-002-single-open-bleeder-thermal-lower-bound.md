# SYS-002 / HV-003 — Single-open passive bleeder: irreducible heat and supply penalty
Date: 2026-11-23 16:02 JST. Role: Chat A deep-design. Issue #6, related #8/#9. **PENDING REVIEW; NO FORMAL CLAIM**.
Branch: `codex/reva-integrated-prototype-review`. Starting branch HEAD: **NOT VERIFIED** (GitHub connector lacks branch HEAD retrieval; repository commit search is default-branch-biased, so no fabricated SHA).
Result: **CONDITIONAL** for ideal passive circuit bounds; **NO-GO (limited)** for claiming redundant passive discharge without accounting for approximately 0.34 W continuous heat in the illustrative case; **BLOCKED** for physical safety approval.

## Task contract and delta
Previous A 11:55 showed 330kohm nominal fails an illustrative 5-second single-path worst-corner and 2x680kohm fails one-open. This report derives the **minimum continuous dissipation** required by any two always-connected, independent passive resistor branches where *either branch alone* must satisfy the same ideal single-open discharge time. This is not a selection or revision to specifications. Exit: analytic bound, numerical example, power impact and failure limits.

## Read baseline
Fetched from the requested branch: `docs/ai-workflow.md`, `docs/verification/handoff.md`, `docs/verification/open-issues.md`, `docs/verification/decisions.md`, `docs/tech-tree.yaml`, `docs/tech-tree.md`, A 11:55 and A 08:04 dated reports; issue #6 and #9. Existing B/C coverage not exhaustively enumerated because recursive branch tree/HEAD unavailable. Shared indexes intentionally untouched to avoid collision. Issue Claim is not proven atomic; provisional task only.

## Inputs and evidence class
- 205V/16mA **TARGET**, not demonstrated.
- V0=220V, Vend=60V, tmax=5s, Cmax=12uF, branch resistor tolerance ±5%: **ASSUMED illustrative analysis corners**, NOT approved safety voltage/time or real component guarantees.
- Ideal isolated capacitor discharge, two physically independent always-connected resistors, either one may open, no tail current, no leakage/ESR, no short-circuit fault: **ASSUMED**.
- Real resistor working-voltage/power ratings, high-voltage transient, temperature, derating, layout and insulation: **UNKNOWN**.

## Derivation
Let L=ln(V0/Vend)=ln(220/60)=1.299282984. After any one branch opens, the surviving branch must satisfy
`R_survivor,max * Cmax * L <= tmax`.
Thus `R_survivor,max <= 5/(12e-6*L)=320689.2 ohm`.
For a ±5% nominal resistor, `R_nom <= 320689.2/1.05 = 305418.3 ohm`.
For two independent identical branches, their minimum actual resistance is `Rmin=0.95*Rnom`; continuous power at V0 is
`P_total,max = 2*V0^2/(0.95*Rnom)`.
Therefore, **even at the largest allowed nominal resistance**, `P_total,max >= 2*(220)^2/(0.95*305418.3) = 0.3336 W` (approx). At nominal 205V, same resistance corner gives >=0.2897W.
This is a lower bound within the stated model, not a guarantee of safe discharge. Any additional always-connected paths increase heat; switched/active designs can avoid the bound only by adding fault and power-domain risks.

Illustrative standard nominal 300kohm each, ±5%:
- single surviving branch at Rmax=315kohm: `t=315e3*12e-6*L = 4.9113s`.
- both branches at Rmax=315kohm each: `t=2.4556s`.
- at Rmin=285kohm each: `P_total(220V)=2*48400/285000=0.33965W`; `P_total(205V)=0.29491W`.
- 220V/16mA output target power is 3.52W **only as a comparison at 220V**, not the actual 205V target. At 205V, bleeder 0.29491W is 8.99% of the 3.28W target output, before converter losses. Output stage must supply this additional continuous load.
- Cmax 12uF at 220V stores 290.4mJ; passive resistors dissipate this energy on shutdown, but physical thermal and pulse ratings remain unqualified.

## Failure and architecture challenge
- A branch-open fault is only one failure mode; common solder/node break, capacitor disconnect, shorted bleeder, open ground, incorrect resistor voltage rating, HV converter still injecting energy, and output physically accessible during a fault are not covered.
- A pair of branches cannot be called independent if they share a single vulnerable PCB connection, connector or fuse.
- Single-open compliance is mathematically possible in this ideal model, but imposes continuous load and sealed-PETG thermal penalty. This is a meaningful SYS-001/PWR-001/HV-001 design input, not a recommendation to use two 300kohm parts.
- A normally-on discharge switch that removes steady heat may fail open on loss of auxiliary supply or MCU reset; any proposed active solution must demonstrate power-loss default behavior, isolation, fault detection and discharge from the actual Cmax.
- At 220V, a nominal 300kohm branch dissipates 161.3mW and must withstand full output voltage if single-part, including transients. Do not infer a 0.25W resistor is qualified from this arithmetic; manufacturer working voltage and temperature derating are independent constraints.
- The 60V/5s illustration is **not** a safe-touch certification or an adopted target.

## Verdict and next gate
**CONDITIONAL**: ideal RC one-open inequality and continuous-power lower bound.
**NO-GO (limited)**: any proposal treating two continuously connected passive branches as thermal-free redundancy.
**BLOCKED**: actual capacitor Cmin/Cmax, tail injection, OVP coordination, actual manufacturer-rated resistor network, thermal resistance, fail-safe path and approved endpoint/time.
**PENDING REVIEW**: Chat C must independently verify math and evaluate common-cause failures before Work integration.
Next: #6/#8 quantify whether >=0.29W additional continuous output loss is acceptable at low cell and sealed enclosure, then compare real rated passive networks against supervised active discharge architecture. Do not change requirements or schematic without approval.

No purchase, PCB fabrication, HV energization, main merge or important specification change.
