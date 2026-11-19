# Chat B — PROTO-001J: protected-21700 holder contact and fit screening
Date: 2026-11-20 01:00 JST
Status: PENDING REVIEW; engineering disposition: BLOCKED for holder adoption
Role: Chat B wide research; parent: #7 PROTO-001; linked #8 PWR-002A, #9 THERM-001, SYS-001
Branch: codex/reva-integrated-prototype-review
Starting HEAD: UNKNOWN — available branch-search returns name only, commit-search does not reliably return branch HEAD. Do not confuse blob SHA with HEAD.
Claim: NONE (provisional work, #7 explicitly says NO FORMAL CLAIM).

## Question / scope
What quantitative holder/contact qualification evidence is required before adopting a protected 21700 pack, without repeating the earlier NTC material? No purchase, design change, PCB, HV test or cell selection.

## Evidence baseline
Read docs/ai-workflow.md v1.1, docs/verification/handoff.md (WORK-INT-003 baseline 6ac0d8c...), docs/verification/open-issues.md, docs/verification/decisions.md, docs/tech-tree.yaml, docs/tech-tree.md, and GitHub Issues including #7/#8/#9. Prior Chat B PROTO-001G/H/I cover geometry and generic contact sensitivity. This report adds a *joint voltage-drop, thermal and minimum-SYS qualification envelope*, not an invented holder part number.
Known candidate envelope from earlier manufacturer-grounded research (reconfirm with original manufacturer drawings before procurement): P2150K length 74.8–75.2mm, diameter up to 21.5mm; P2150R length 74.3–74.7mm, diameter up to 21.6mm. Exact holder MPN, terminal travel and current rating UNKNOWN.

## Reproducible bounded calculation (ASSUMED; not measured)
At constant pack current I, total positive+negative contact resistance R_contact:
V_drop=I*R_contact; P_contact=I²*R_contact.
At I=2.2 A (ASSUMED sensitivity, not certified maximum), for combined contact R:
- 0.020 ohm: Vdrop 0.044V, P 0.0968W
- 0.050 ohm: Vdrop 0.110V, P 0.242W
- 0.100 ohm: Vdrop 0.220V, P 0.484W
- 0.200 ohm: Vdrop 0.440V, P 0.968W
At I=3.0 A (ASSUMED transient), R=0.100 ohm yields 0.300V and 0.900W. This is *total contact* dissipation; one bad contact can carry most heat. In addition to cell internal resistance, PCM and cable drop, the available minimum SYS voltage must be bounded as:
V_SYS,min <= V_cell,terminal - I*(R_PCM+R_contacts+R_wire) - V_path,drop
(with actual charger/BATFET topology and directional current validated by Chat A). This is a screening inequality, not a solved SYS rating. USB 5V/500mA nominal 2.5W is input, not guaranteed output; 205V*0.016A=3.28W is already greater, even at ideal efficiency. Battery assist may therefore be net discharge while USB is present.

## Qualification matrix (candidate MPNs not yet sourced)
1. Holder geometry: controlled maker drawing must explicitly accommodate 74.3–75.2mm protected-cell length, <=21.6mm diameter, terminal stack and insulation. Spring travel and tolerances UNKNOWN. Generic '21700' listing insufficient.
2. Continuous current: published rating at actual ambient and connector termination; include inrush and derating. UNKNOWN.
3. Contact resistance: supplier maximum at end-of-life/contamination/low-force, or a supervised 4-wire test plan at realistic compression. UNKNOWN; do not equate nominal spring metal resistance with installed contact resistance.
4. Thermal: per-contact hot spot in sealed PETG and cell surface under charge and discharge; use actual cell + PCM limits, not a generic ambient threshold. UNKNOWN.
5. NTC: protected cell surface contact must remain under vibration, insertion/removal and harness strain; no exposed conductor to cell can. UNKNOWN.
6. Faults: reversed cell, spring collapse, intermittent contact/brownout, PCM trip and recovery, sensor detached, thermal runaway path. No firmware-only safety assertion.
7. Procurement: maker MPN, drawing revision, distributor SKU, stock timestamp, JPY tax/shipping, lead time, footprint/harness and replacements all UNKNOWN until verified.

## Decision / alternative
A spring holder is NOT qualified by form-factor alone. Compare (A) a manufacturer-dimensioned protected-21700 holder with documented continuous current and thermal data; (B) a professionally assembled protected-cell pack with welded leads, rated connector and cell-attached qualified NTC, eliminating user-accessible spring contacts but introducing pack qualification, replacement and shipping constraints. Neither is adopted. Do not spot-weld a bare lithium cell as an ad hoc workaround.

## Exit and handoff
Chat B next: obtain >=2 exact maker holder MPNs and drawings or document why none fit; compare with a complete preassembled protected pack; add dated domestic price/stock and assembly BOM. Chat A #8/#9: use resistance and thermal bounds in signed BAT/USB mode and actual cutoff path. Chat C: independently check equations, distinguish terminal and cell voltage, and challenge contact thermal concentration. Work: retain BLOCKED holder/cell selection.
SOP proposal (do not edit shared SOP without owner): every sourcing report must include exact MPN + drawing revision + explicit UNKNOWN for contact maximum/ambient rating and a date-stamped price; a generic compatibility listing cannot clear a safety gate.
No release authorization. No requirements, schematic, main, schedule or hardware changes.
