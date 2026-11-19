# PROTO-001H — Protected 21700 P2150R alternative screen
Date: 2026-11-19 17:03 JST
Role: Chat B; Issue #7; **PENDING REVIEW**; **NO FORMAL CLAIM**.
Branch: codex/reva-integrated-prototype-review. Starting HEAD: **UNKNOWN**: connector did not expose a branch-scoped SHA; repository-wide commit search is not a reliable substitute.

## Question and exit criterion
Compare exact primary-source P2150K and P2150R specifications; identify what prevents pack/holder approval. No part selection, schematic change, hardware work or procurement.

## Manufacturer primary sources (checked 2026-11-19)
- P2150K: https://www.keeppower.com/product/keeppower-21700-5000mah-protected-li-ion-rechargeable-battery-p2150k/ — nominal 5000 mAh, max D21.5 x L75.0 mm (±0.2 mm), charging +10..45 C, discharging -20..60 C. PCM lists overcharge, overdischarge, overcurrent and short circuit, not temperature cutoff. Continuous discharge rating UNKNOWN in this primary page.
- P2150R: https://www.keeppower.com/product/p2150r-keeppower-21700-5000mah-protected-li-ion-rechargeable-battery-max-15a/ — nominal 5000 mAh, max D21.6 x L74.5 mm (±0.2 mm), manufacturer states max continuous discharge 15 A; charge +10..45 C, discharge -20..60 C. PCM temperature cutout NOT documented. 15 A rating is not proof of thermal safety in a sealed PETG case.
- P2150R JST SYP-02 lead variant listed by manufacturer: https://www.keeppower.com/nl/product/p2150r-keeppower-21700-5000mah-protected-li-ion-rechargeable-battery-max-15a-discharge/ . Harness polarity, gauge, lead length, terminal resistance, variant availability and price UNKNOWN. Do not assume all P2150R cells ship with this lead.

## Reproducible calculation
205 V * 0.016 A = 3.28 W (ASSUMED worst simultaneous target, not a verified lamp load).
Battery average current I=Pout/(eta*Vbat), excluding controls, transient, wire/PCM losses:
| Vbat | eta=60% | eta=70% | eta=80% |
|---|---:|---:|---:|
| 3.0 V | 1.822 A | 1.562 A | 1.367 A |
| 2.5 V | 2.187 A | 1.874 A | 1.640 A |
These are hypothetical steady-state averages, NOT verified low-cell continuous operation. 5 V * 0.5 A = 2.5 W gross USB input, so USB-only cannot supply 3.28 W HV output even at 100% conversion efficiency. USB+battery supplement may mean net cell discharge, not charging.

P2150R is nominally 0.5 mm shorter and 0.1 mm wider than P2150K. Published maximum upper lengths including stated ±0.2 mm are 74.7 and 75.2 mm respectively. No generic 21700 holder is guaranteed to accommodate either protected cell; require exact manufacturer holder drawing and contact spring travel. NTC needs reliable thermal contact, isolation and strain relief.

## Failure, thermal and procurement holds
PCM trip threshold/time, PCM R, thermal cutoff and pack terminal temperature remain UNKNOWN. +10..45 C is a charging operating range, not an automatically enforced PCM trip. BQ25185 TS does not enforce battery-only temperature limits; THERM-001 requires independent monitoring/load inhibit. MCU-off, NTC open/short and charge-state transitions must be bounded. Exact holder MPN/drawing, P2150R local landed price, tax, shipping, stock, lead time and genuine source are UNKNOWN. Do not solder to the cell or modify PCM.

## Conclusion
P2150R is a CONDITIONAL alternative with a better documented manufacturer continuous-current figure; **pack adoption remains BLOCKED**. P2150K remains CONDITIONAL, with continuous-current rating missing from the cited primary page. No thermal protection, fit, power path or procurement approval follows.

## Chat C review / next
Review P2150R primary rating and harness variant, arithmetic, worst-case geometry and non-claim of PCM temperature cutoff. Next Chat B: source exact holder manufacturer drawing for >=75.2 mm length and >=21.6 mm diameter, connector/contact current rating, Japanese stock/landed price, and P2150R PCM thresholds. Chat A owns thermal interlock design. Work owns shared ledger integration. Existing ai-workflow.md v1.1 nonblocking fallback already covers this run; no direct SOP edits proposed.
