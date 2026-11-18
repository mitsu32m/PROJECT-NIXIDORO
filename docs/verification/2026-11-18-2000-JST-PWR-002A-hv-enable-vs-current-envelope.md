# PWR-002A / #8 — HV enable threshold versus battery-current feasibility (cross-gate correction)

Date: 2026-11-18 20:00 JST scheduled slot (actual runtime time not independently verified). Role: Chat A, deep-design. **PENDING REVIEW; NO FORMAL CLAIM.**

## Task contract
Question: Can the earlier battery-only constant-power/OCP pass at 3.3 V actually permit full-HV operation while the project provisional SYS>=3.4 V HV-enable gate remains in force? Exit: derive the joint inequality and identify which earlier table rows are not operationally permitted. Excludes real component adoption, firmware change, temperature guarantee, or tests.

Working branch: `codex/reva-integrated-prototype-review`. Starting HEAD SHA **UNKNOWN**: connected fetch_file read the named branch but did not expose commit HEAD. Read SOP v1.1, handoff, open-issues, decisions, tech-tree.yaml/md, #8, WORK-INT-002, and preceding 16:00 PWR-002A report. GitHub #1 shows formal atomic Claim remains unverified. No claim asserted. Chat B owns physical sourcing #7; C reviews; Work owns shared indexes.

## Inputs and classifications
- **ASSUMED**: battery-only constant SYS demand P=6.60084 W (prior Work screen), cell terminal voltage Vb, constant total series R=R_BQ+R_EXT, R_BQ=0.140 ohm extrapolated beyond specified BQ25185 test conditions.
- **PROVISIONAL PROJECT POLICY**, not a manufacturer electrical limit: HV enable only if SYS >= 3.4 V (referenced in prior #8 report). It is not yet a validated hysteretic implementation.
- **ILLUSTRATIVE 27 C OCP SCREEN**, not full-temperature guaranteed continuous rating: Icap=3.13*(1-0.18)=2.5666 A from TI BQ25185 Rev.B https://www.ti.com/lit/ds/symlink/bq25185.pdf. Actual OCP response/temperature corners UNKNOWN.
- **UNKNOWN**: real protected 21700 terminal sag, 5V converter efficiency/current limit, startup transients, battery heat and thermal impedance.

## Joint condition and important correction
On battery-only discharge with I>=0 and R>=0:
Vsys=Vb-I*R, P=I*Vsys, so for nonzero load Vsys<=Vb. Consequently **Vb<3.4 V necessarily disables HV** under the provisional enable policy, regardless of whether the constant-power quadratic has a real root and whether OCP screen passes. This is a stronger operational gate than the prior 3.3 V OCP-only pass. At Vb=3.4 V and nonzero R, any positive current gives Vsys<3.4 V, so a strictly positive margin is needed.

For fixed battery terminal Vb and demand P, both OCP and HV-enable require some operating I such that:
- I <= Icap (illustrative only)
- I*(Vb-I*R) >= P
- Vb-I*R >= Vgate=3.4 V.
On the lower-current stable branch the feasible I is (Vb-sqrt(Vb^2-4RP))/(2R), provided discriminant >=0. For R=0, I=P/Vb. Do not treat this model as converter regulation proof.

The HV-enable inequality implies R <= (Vb-Vgate)*Vgate/P **only if** operating Vsys can be at least Vgate and the load power equation holds, with equality at Vsys=Vgate and I=P/Vgate; this boundary is on the lower-current branch when Vb<=2*Vgate. For Vb>2*Vgate the branch selection requires separate evaluation. For the illustrative 3.4–4.0 V region, the boundary applies.

Illustrative maximum R_total from HV gate for P=6.60084 W:
| Vb (V) | R_total max (ohm) | R_EXT max after assumed 0.14 ohm BQ | Verdict |
|---:|---:|---:|---|
| 3.0 | none | none | HV disabled even at R=0 |
| 3.3 | none | none | HV disabled even though 27C OCP-only screen could pass |
| 3.6 | 0.1030 | negative | No feasible R_EXT>=0 under assumed BQ resistance |
| 4.0 | 0.3090 | 0.1690 | Conditional on OCP and all other gates |

At Vb=3.6 V, even R_EXT=0 and assumed R_BQ=0.14 ohm yields Vsys below 3.4 V for 6.60084 W demand; the prior 3.6V OCP-only pass does NOT imply HV enabled. At 4.0V with R_EXT=0.1 ohm (total 0.24 ohm), quadratic low-current solution ~1.857 A and Vsys~3.554 V; passes both illustrative static gates. This is not startup proof.

For 4.0 V the illustrative OCP bound R_total <=0.5564 ohm is weaker than the HV gate R_total <=0.3090 ohm; a current-limit-only assessment materially overstates feasible external resistance.

## Independent reproducibility
Python 3:
```python
P=6.60084; gate=3.4; rbq=0.14
for vb in [3.0,3.3,3.6,4.0]:
    if vb<=gate: print(vb, 'NO positive-power gate margin')
    else:
        rt=(vb-gate)*gate/P
        print(vb,round(rt,6),round(rt-rbq,6))
```
This is a **necessary screen**, not a sufficient design envelope. The constant-R BATFET approximation at multiamp current is not guaranteed. Also the 3.4V threshold is provisional: a user/Work-reviewed threshold and hysteresis/UVLO strategy could alter the allowed operating region; no change made here.

## Result and handoff
**CONDITIONAL**: algebraic joint-gate correction under stated assumptions. **BLOCKED**: real battery-only 205V/16mA operation, selected protected cell, BQ/TPS current/temperature limits, startup, USB transitions, thermal and measured voltage margin. **PENDING REVIEW** for Chat C; Work should annotate #8's previous OCP-only table as non-operational below 3.4 V SYS and require mode-consistent startup/UVLO/hysteresis evidence. No shared indexes or KiCad edited to avoid concurrent integrator writes.

No purchasing, PCB fabrication, main merge, HV energization or important requirement/firmware change authorized.
