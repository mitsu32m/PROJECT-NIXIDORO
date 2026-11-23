# HV-002 / Issue #6 — Precision-divider static window and post-trip energy impossibility screen
Date: 2026-11-24 04:00 JST. Role: Chat A deep-design. Branch: `codex/reva-integrated-prototype-review`.
**PENDING REVIEW / NO FORMAL CLAIM / NOT ORDER-READY.**

## Task contract and evidence
Question: Does tightening the *illustrative* TLV6700 HV divider from ±1% to ±0.1% create enough independent-OVP margin to justify a real design? Exit: exact static interval and available residual-energy ceiling; explicitly distinguish necessary from sufficient conditions.
Inputs: prior [2026-11-24-0000 TLV6700 screen](2026-11-24-0000-JST-HV-002-tlv6700-ovp-divider-static-window-screen.md), [WORK-INT-004](2026-11-23-2201-JST-WORK-INT-004-power-discharge-topology-integration.md), Issue #6, handoff/open-issues/decisions/tech-tree, SOP. Manufacturer context: TI TLV6700 https://www.ti.com/product/TLV6700 ; Microchip HV5524 https://ww1.microchip.com/downloads/aemDocuments/documents/APID/ProductDocuments/DataSheets/HV5524-32-Channel-Serial-to-Parallel-Converter-Data-Sheet-DS20006850.pdf (recommended HV max 220V). **No new datasheet min/max guarantee is claimed in this report**; 1% threshold is an ASSUMED proxy for TI product-page accuracy, not a verified independent transfer function. No measurement.

## Exact independent corner arithmetic (reproducible)
ASSUMED nominal divider Rtop/Rbottom=541.5 (e.g. 5.415Mohm/10kohm), threshold error ±1%, each resistor independently ±r, ideal input bias=0. Normalize nominal trip Vn. Factors:
a=(1-0.01)*(1+(1-r)*541.5/(1+r))/(1+541.5)
b=(1+0.01)*(1+(1+r)*541.5/(1-r))/(1+541.5)
Vtrip,min=a*Vn, Vtrip,max=b*Vn.
Use historical **incomplete ASSUMED** Vnormal,static,max=214.13495V and manufacturer recommended 220V ceiling; strict inequalities demand Vn>214.13495/a and Vn<220/b. No dynamic margin is included.

| R tolerance | a | b | admissible nominal Vn (V) | static finding |
|---|---:|---:|---|---|
| ±1% | 0.97043218 | 1.03036643 | >220.6594 AND <213.5163 | NO-GO even static |
| ±0.1% | 0.98802562 | 1.01201829 | >216.7302 AND <217.3874 | CONDITIONAL nonempty 0.6572V interval |
| ±0.05% | 0.98901232 | 1.01100864 | >216.5139 AND <217.6045 | CONDITIONAL nonempty 1.0905V interval |

For ±0.1% choosing the **midpoint of the nominal feasible interval** Vn=217.05877V yields Vtrip,min=214.45962V (only 0.32467V above historical static normal maximum) and Vtrip,max=219.66744V (only 0.33256V below 220V). Even with ASSUMED Cmin=1µF and no other faults, allowable **total** post-trip injection energy before 220V is only:
Ehead=0.5*Cmin*(220²-219.66744²)=0.07311mJ (73.11µJ).
For ASSUMED Cmin=0.1µF it is 7.31µJ. These are *remaining energy budgets*, not guaranteed tail energies. For comparison, one purely hypothetical 44µH/3.2A magnetic energy packet is 0.22528mJ, already >73.11µJ; that packet is **not** proven to reach the HV capacitor in the actual topology and cannot be used as a real-system NO-GO proof.

## Adversarial limitations
- Precision resistors alone do not solve the problem. Dynamic normal ripple/overshoot consumes the 0.32467V low-side headroom; post-trip drive, capacitor Cmin, delay and comparator startup consume the 73.11µJ high-side budget. Strict nonzero margins are required; interval endpoints are not acceptable operating points.
- The TI 1% figure may incorporate bias, hysteresis or other test conditions. Do **not** blindly sum it with input bias as an independent guarantee. Need Rev.B electrical-characteristics definition and guaranteed comparator trip, output logic, supply and timing conditions.
- Real top chain working voltage, resistance TC/aging, HV surge, leakage/contamination and resistor open/short fault are UNKNOWN. A nominal 5.415Mohm may require multiple series-rated parts; no MPN is qualified.
- A comparator with open-drain output is not a hard-off path by itself: unpowered/brownout, FET stuck-on, shared return open, and residual capacitor discharge need separate proof.
- The historical normal high 214.13495V is **not** a dynamic guarantee; the 220V recommended maximum is a design ceiling, not a trip setpoint. Owner has not decided whether 200–205V is a nominal target or guaranteed operating window.

## Scoped decision / next action
**CONDITIONAL**: ±0.1% ideal resistor tolerances can make the *static mathematical* window nonempty, but leave only ~0.33V on each side at a nominal midpoint and ~73µJ per assumed 1µF of post-trip energy.
**NO-GO (limited)**: claiming that tightening resistors alone qualifies independent OVP or allows selecting 217.06V threshold.
**BLOCKED**: actual full-temperature/aging comparator transfer, exact resistor MPN and voltage ratings, dynamic normal max, real Cmin, topology-specific worst tail energy, guaranteed hardware stop path and common-fault behavior.
**PENDING REVIEW**: independent Chat C review and Work integration before adoption.
Next bounded research: obtain manufacturer min/max for an actual reference/comparator + HV resistor chain, then derive worst-case tail from selected topology and stop circuit. If no feasible nonzero margins, escalate normal voltage window/architecture as **owner decision**, never change requirement automatically.
No purchases, manufacturing, HV energization, main merge or schematic/requirements modifications.
