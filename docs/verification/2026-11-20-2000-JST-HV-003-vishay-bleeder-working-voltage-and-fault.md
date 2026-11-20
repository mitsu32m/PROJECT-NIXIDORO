# HV-003 / Issue #6 — Vishay resistor working-voltage qualification screen
Date: 2026-11-20 20:00 JST. Role: Chat A deep-design.
Branch: codex/reva-integrated-prototype-review. Starting branch HEAD: UNKNOWN (branch-specific SHA not exposed by available GitHub connector). Formal Claim: NONE; provisional selection from open-issues.md.
Review: **PENDING REVIEW**. Verdict: **CONDITIONAL** for rated-series screen; **BLOCKED** for a qualified single-fault-safe discharge.

## Task contract and evidence baseline
Question: Can an actual manufacturer's thick-film resistor family plausibly carry a 205 V continuous bleeder, and what limits the selection beyond wattage? Exit: primary-manufacturer working-voltage reference, quantitative stress and explicit fault hold. No actual resistor MPN, PCB, or HV test approved.
Read required SOP, handoff, open issues, decisions, tech-tree.yaml and tech-tree.md, Issue #6, and immediately prior A report 2026-11-20-1600-JST-HV-003-bleeder-discharge-power-fault-screen.md. This is a new **manufacturer rating screen**, not another nominal RC sweep. Full branch tree/latest reports could not be enumerated, so possible concurrent overlap remains UNKNOWN.

## Manufacturer primary source
Vishay D/CRCW e3 thick film chip resistor datasheet, Document 20035, Rev 27-Oct-2020, accessible manufacturer-authored PDF mirror:
https://datasheet.lcsc.com/datasheet/pdf/a9f22213fc8218de4ecd48fda18a6ac0.pdf?productCode=C2091802
The CRCW2512 series working-voltage rating is 500 V (manufacturer family characteristic; verify exact selected ordering code, resistance range, thermal derating, PCB conditions and latest datasheet before adoption). The family power rating is 1 W under specified reference conditions, **not** a blanket permission to apply sqrt(P*R) volts. Distributor corroboration: https://www.digikey.com/en/products/detail/vishay-dale/CRCW251212R0JNEG/1178535 (12 ohm example, not a proposed 1 MΩ part).
Manufacturer rating is a **series screen** only. No exact 1 MΩ part has been qualified or ordered.

## Independent equations and numerical cases
For an ideal bleeder, continuous voltage V, resistance R: I=V/R, P=V²/R. Maximum permissible voltage is limited by min(V_working,max, sqrt(P_rated,derated*R)), plus pulse, pollution/clearance, thermal and assembly limits.
ASSUMED comparison: 1.00 MΩ total, 205 V nominal and 220 V hypothetical corner, 1.0 µF capacitor; no recharging. At 205 V: I=205 µA, P=42.025 mW. At 220 V: I=220 µA, P=48.4 mW. A nominal 1 MΩ, 1 W resistor would yield sqrt(P*R)=1000 V if considering power alone, but a 500 V working-voltage cap would bind before 1000 V. **This is why power-only screening is invalid**; neither 500 V nor 1 W by itself proves the complete assembly safe.
For two equal 500 kΩ series parts: nominal per-part stress at 220 V is 110 V and 24.2 mW. With independent ±5% resistances, worst single-part share is 1.05/(1.05+0.95)=52.5%, hence 115.5 V at 220 V; 205 V gives 107.625 V. The 500 kΩ parts here are hypothetical values, not verified available manufacturer ordering codes. Series division assumes only resistive DC steady state; transient parasitics and humidity/contamination may alter stress.
At 220 V and 1.0 µF, stored energy is 24.2 mJ. Nominal time to 60 V for 1 MΩ is 1.2993 s (60 V is a calculation endpoint, NOT an approved touch-safe threshold). With R +5%, C +20%, V0=220 V, t=1.637 s.
If one **series** resistor opens, the whole discharge path opens: no single-fault discharge guarantee. If one shorts, the other sees full HV; at 220 V, a surviving 500 kΩ element dissipates 96.8 mW (nominal) and carries 440 µA, subject to its own working-voltage and fault temperature rating. Two equal **parallel** 2 MΩ paths nominally yield 1 MΩ; one open doubles R and nominal time, but the other continues to discharge, assuming no common-mode damage and each individual resistor is fully rated for 220 V. Parallel branches offer one-open fault tolerance in the simple model but do NOT protect against both-open, PCB crack common mode, short, ongoing HV generation, or fault access.

## What this changes from previous report
Prior 16:00 report established nominal RC and noted working-voltage as UNKNOWN. This report supplies a real manufacturer family rating and shows (1) power-only voltage qualification is invalid, (2) series chains solve voltage distribution but NOT single-open discharge, (3) independently rated parallel branches can preserve a discharge path after one open, at a quantifiable time penalty. No hardware safety proof is implied.

## Unresolved before any design selection
- Select exact resistance/voltage/power/temperature-rated MPN(s) with latest manufacturer revision, pulse rating, and distributor sourcing; verify 1 MΩ and 2 MΩ ordering codes actually exist.
- Define approved discharge endpoint and maximum time; obtain real HV capacitor Cmax (including tolerance, aging, temperature and parallel wiring), and bound dielectric absorption/rebound.
- Prove independent HV generation hard-off including open-load, power loss, MCU reset and single faults; bleeder alone cannot force V(t) decay while supply is active.
- PCB creepage/clearance, assembly contamination, resistor thermal derating in sealed PETG, and common-mode branch failure require review.
- Coordinate Cmin OVP tail-energy and Cmax startup/discharge with #6/#8. C-review then Work integration required.

**CONDITIONAL:** manufacturer-family voltage screen and transparent equations.
**NO-GO (limited):** assuming a series resistor chain alone is single-open-fault-safe.
**BLOCKED:** actual rated and redundant discharge solution and independent source isolation.
**PENDING REVIEW:** no adoption, no BOM change, no manufacturing or HV operation authorization.
No purchases, PCB fabrication, main merge, HV energization or requirement changes.