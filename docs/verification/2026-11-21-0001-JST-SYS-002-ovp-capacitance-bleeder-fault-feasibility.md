# SYS-002 / Issue #6 — OVP Cmin vs redundant bleeder Cmax feasibility inequalities
Date: 2026-11-21 00:01 JST. Chat A deep-design. Branch: codex/reva-integrated-prototype-review.
Status: **PENDING REVIEW**. Formal Claim: NONE; provisional P0 task from open-issues.md. Verdict: **CONDITIONAL** mathematical feasibility screen, **BLOCKED** hardware qualification.

## Evidence and novelty
Read required ai-workflow, handoff, open-issues, decisions, tech-tree, Issue #6 and the two latest A HV-003 reports (2026-11-20 16:00 and 20:00). Shared indexes left unchanged. This report connects the previously separate hypothetical post-trip energy and one-open redundant bleeder time into a **single Cmin/Cmax existence test**; it does not repeat resistor working-voltage screening. Other concurrent branch reports could not be exhaustively enumerated; overlap remains UNKNOWN. Exact starting branch HEAD unavailable from fetch-file API (blob SHA is not branch commit SHA).

Primary reference for device-limit context: ADI MAX668/MAX669 datasheet Rev3 https://www.analog.com/media/en/technical-documentation/data-sheets/MAX668-MAX669.pdf . Its typical shutdown timing is not a guaranteed worst-case residual energy bound. HV5524 recommended 220 V limit is treated as a design ceiling, NOT as a safe discharge voltage.

## Equations
With trip voltage Vt,max, absolute design ceiling Vlim, and guaranteed post-trip residual energy Etail,max, minimum effective capacitance must satisfy:
Cmin > 2 Etail,max / (Vlim² - Vt,max²).
This is a strict inequality, requiring a nonzero margin; valid only if Vt,max < Vlim and all other overshoot/ESR/ESL effects are separately bounded.

For a discharge target Vs and maximum time T, one surviving resistor branch Rremain,max (e.g., after one of two parallel branches opens) requires:
Cmax <= T / [Rremain,max ln(V0,max/Vs)].
These two inequalities must be simultaneously satisfiable using a **single actual capacitor part's minimum and maximum effective capacitances**, with temperature, DC bias, tolerance, aging, wiring and relevant fault modes.

Illustrative hypothetical pulse Etail=0.2253 mJ (44uH/3.2A energy only, NOT a verified bound), Vlim=220V:
| Assumed Vt,max | Required Cmin (no safety margin) |
|---|---:|
| 217.000 V | >0.344 uF |
| 219.170 V | >1.236 uF |
| 219.978 V | >46.55 uF |
This extreme sensitivity near 220V makes nominal OVP setpoint selection inseparable from capacitance and startup. Values are illustrative, not approved capacitor requirements. They neglect all additional tail energy and transient terms.

Illustrative one-open case: two parallel 2MΩ branches (1MΩ nominal intact); surviving R=2MΩ nominal, Rmax=2.1MΩ at +5%; V0,max=220V; Vs=60V (arbitrary mathematical endpoint, NOT a safety-approved touch threshold); T=3.0s hypothetical. Then Cmax <= 3/[2.1e6 ln(220/60)] = 1.100 uF. With Vt,max=219.17V, illustrative Cmin >1.236uF, so **no capacitor** satisfies both bounds, even before capacitor tolerance, if these scenario assumptions are jointly imposed. At Vt,max=217V, the interval 0.344uF < Cmin <= Cmax <= 1.100uF is mathematically nonempty, but no real part or safety margin has been demonstrated. T=3s and Vs=60V are analysis parameters, not project safety specifications.

A normal capacitor with Cmax/Cmin >1 makes the feasible nominal interval narrower. If a candidate's ratio k=Cmax/Cmin, existence requires Cmin,OVP * k < Cmax,discharge; at 217V the illustrative upper ratio bound is 1.100/0.344≈3.20 (zero margin), whereas at 219.17V the ratio bound is 0.89, impossible even for an ideal k>=1 capacitor.

## Limitations and fault paths
- The pulse energy 0.2253mJ is a **hypothetical** example; real controller/magnetics/current-limit, multiple switching pulses, leakage, comparator latency and independent hard-off must provide a defensible guaranteed Etail,max. 220V is a recommended operating limit, not a failure-safe ceiling.
- Discharge model requires independent source hard-off. If converter continues switching, no exponential guarantee. A resistor short can demand uncontrolled source current; a common pad/trace open defeats two branches.
- One-open tolerance calculation assumes a *surviving fully rated branch* and ignores dielectric absorption, capacitor voltage rebound, parasitic wiring capacitance, temperature derating and surface contamination.
- A higher capacitor increases startup energy (E=0.5CV²); at 205V, 1uF requires 21.0mJ before losses, and a low-cell supply's startup power margin remains unverified.
- Real HV capacitor manufacturer MPN, guaranteed effective Cmin/Cmax, voltage/ripple/ESR, actual resistor MPN, accepted discharge endpoint/time, physical isolation and safety validation are UNKNOWN.

## Review request and next experiment design (no energization)
Chat C: independently verify numerical inequalities and reject any inference that assumed 0.2253mJ or 3s/60V are specifications. Work: require an actual capacitor's worst-case C range, bounded controller tail-energy and explicit discharge criteria before part adoption. Chat A/B: prioritize exact HV stage/magnetics and capacitor sourcing, rather than further nominal RC tables. No shared ledger, KiCad, BOM, target, purchase, fabrication, main merge or HV test changed.

**CONDITIONAL**: joint mathematical constraints under declared assumptions.
**NO-GO (scenario only)**: Vt,max=219.17V, assumed tail=0.2253mJ, 3s/60V one-open 2MΩ branch scenario cannot share any capacitor.
**BLOCKED**: guaranteed real Cmin/Cmax, actual tail energy, independent OVP stop, safe discharge requirements.
**PENDING REVIEW**: not formally adopted.
