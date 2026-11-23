# Chat B — SYS-001 cross-topology USB-only bound after C-REVIEW-024
Date: 2026-11-23 21:03 JST. Role: Chat B wide research. **PENDING REVIEW**; scoped result **CONDITIONAL arithmetic / BLOCKED hardware**. **NO FORMAL CLAIM** (atomic claim ownership not verified).
Branch: `codex/reva-integrated-prototype-review`. Starting HEAD: `dfda7402691a359a264dcfce528c0faa89e0e30f`.
Issues: #4 SYS-001A, #7 PROTO-001, #6 HV-002C. This is a *correction and cross-topology comparison*, not a repeated lamp-current study.

## Task contract
Question: How does the independently reviewed two-branch passive bleeder model change USB-only display bounds and battery-assist deficits compared with Chat B's earlier single-330k equivalent model? Exit: explicit formulas, integer mode limits, architecture-independent conclusions and handoff. No adoption of a bleeder, UI mode, current target or component.

## Repository and source provenance
Read six required documents (ai-workflow, handoff, open-issues, decisions, tech-tree.yaml, tech-tree.md), latest A 20:00 and C 21:00 reviews, B 17:00 and Issues search. C-REVIEW-024 independently recomputed the original 17:00 algebra and flagged the topology inconsistency. Primary manufacturer document for charger input-current limits: TI BQ25185 datasheet https://www.ti.com/lit/ds/symlink/bq25185.pdf ; 450mA minimum limit threshold is **not** guaranteed delivered SYS current. This report does not independently validate its revision or temperature corner. All lamp currents, efficiency, bleeder resistance and 60V/5s endpoint are **ASSUMED**, not qualified datasheet guarantees.

## Explicit competing topologies
Common assumptions: VHV=205V, digits 3mA each (0..2), neon 0.5mA each (0..12), eta_SYS_to_5V=0.90, eta_5V_to_HV=0.75, eta_total=0.675. USB 5V * 450mA=2.25W is an **optimistic available input upper budget** for illustration, not a guaranteed lower bound. 500mA=2.50W is a nominal source ceiling, not assured through BQ. Control, charger, divider, driver, BQ, thermal and start-up losses excluded.

A) Prior B single-equivalent 330k: Ibleed=205/330000*1000=0.621212mA; Pbleed=0.12735W.
B) A's *proposed but not adopted* two independent 300k ±5% always-on resistors: worst running-current corner both at 285k; Ibleed=2*205/285000*1000=1.438596mA; Pbleed=0.294912W. Nominal both 300k: 1.366667mA, 0.280167W. Worst single-open discharge uses surviving Rmax=315k, not Rmin; the 60V/5s/Cmax=12uF exercise is illustrative and does not prove safety.

Let Ibus(mA)=3Nd+0.5Nn+Ibleed, P_HV=205*Ibus/1000, P_SYS=P_HV/0.675. USB-only **necessary** condition P_SYS<=P_USB; remaining margin is not proof of feasibility.

At 450mA optimistic: Ibus,max=7.408537mA. At 500mA optimistic: 8.231707mA.

| Bleeder topology | Digits on | Neon max at 450mA | Neon max at 500mA |
|---|---:|---:|---:|
| single 330k equivalent | 0 | 12 | 12 |
| single 330k equivalent | 1 | 7 | 9 |
| single 330k equivalent | 2 | 1 | 3 |
| dual 300k ±5%, both Rmin | 0 | 11 | 12 |
| dual 300k ±5%, both Rmin | 1 | 5 | 7 |
| dual 300k ±5%, both Rmin | 2 | 0 (even two digits alone exceed by 0.03006mA) | 1 |

Integer floors clipped to 0..12; 0 is **not** a guarantee even with all neon off. At 450mA with dual Rmin, two digits alone need Ibus=7.438596mA and P_SYS=2.25913W >2.25W. At 500mA two digits + one neon need 7.938596mA, P_SYS=2.411 W before overhead.

All-on (2 digits +12 neon):
- single 330k: Ibus=12.621212mA; P_SYS=3.83311W; optimistic USB450 deficit=1.58311W.
- dual Rmin: Ibus=13.438596mA; P_SYS=4.08135W; optimistic USB450 deficit=1.83135W.
- incremental dual-vs-single input at same assumed efficiency: (0.294912-0.127348)/0.675=0.24824W. At BAT 3.0V with **zero battery-path loss** this is an extra 82.75mA; actual current higher and conditional on power-path dynamics.

If 16mA refers to *lamps alone*, total HV current is 16mA + Ibleed + dividers/drivers/leakage, so 205V*16mA=3.28W **understates** total HV demand. If 16mA is a whole-HV-bus limit, then available lamp current is less. Both definitions remain unapproved and must not be silently merged.

## Fault, heat, procurement and qualification
Dual passive branches raise continuous heat (0.295W at 205V worst Rmin) and can improve a narrowly assumed single-open discharge case, but common HV/return node failure, resistor derating, resistor short, converter stuck-on, enclosure thermal, and single-fault independence are UNKNOWN. Switched/hybrid discharge can reduce run-state loss but must prove default-on operation without MCU/auxiliary power and independent converter hard-off; no actual MOSFET/driver chosen. 205V DC lamp ratings, actual magnetics, controller+transformer pair, part stock and cost remain UNKNOWN. **No qualified HV topology+magnetics pair** is claimed.

## Review request / Work integration proposal
C: independently review the 450mA two-digit zero-neon infeasibility and the topology-dependent 0/1 count, especially rounding, power-path interpretation and source class. Work: create canonical mode-load ledger with Nd,Nn, bleeder candidate ID, divider, driver, leakage, USB input-to-SYS loss, signed BAT current (positive discharge), thermal corners, startup and fault state; preserve single 330k and dual passive as separate alternatives, not combined assumptions. Proposed SOP clarification: every report using a hypothetical resistor network must include its topology ID and whether the 16mA target is lamp-only or whole-bus; submit as proposal only, do not edit shared ai-workflow.md.

**Safety**: No procurement, PCB manufacturing, HV energization, main merge, requirement change or safety signoff. Pending C review and Work integration.
