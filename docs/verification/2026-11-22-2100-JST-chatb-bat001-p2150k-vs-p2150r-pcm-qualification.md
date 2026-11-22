# Chat B — BAT-001 / SYS-001: P2150K vs P2150R protected-cell discharge qualification
Date: 2026-11-22 21:00 JST
Status: **PENDING REVIEW**; scoped result **CONDITIONAL** (manufacturer model differentiation), **BLOCKED** (exact P2150K PCM and assembly approval). **NO FORMAL CLAIM**.
Branch: `codex/reva-integrated-prototype-review`. Starting branch HEAD: **UNKNOWN** — GitHub connector fetch_file exposes blob SHA, search_commits returned stale default-branch results, branch lookup did not expose commit SHA. Do not misidentify a blob SHA as branch HEAD.
Issues: #7 PROTO-001, #4 SYS-001A, #9 THERM-001. Prior B 2026-11-22 17:03 battery-current screen, C review pending.

## Bounded task
Question: Does the proposed P2150K protected 21700 cell have a *manufacturer-published, unambiguous* continuous-discharge and PCM protection threshold sufficient to qualify SYS-001? Compare closely named P2150R without silently substituting its 15A rating. Exit: manufacturer evidence and exact unresolved fields, then review handoff. Scope excludes actual purchase, qualification, HV energization or adoption.

## Required startup / overlap
Read `docs/ai-workflow.md`, `docs/verification/handoff.md`, `docs/verification/open-issues.md`, `docs/verification/decisions.md`, `docs/tech-tree.yaml`, `docs/tech-tree.md`, `hardware/integration/thermal-qualification-holds.csv` and prior B 17:03 report. Inspected GitHub Issues search (role:wide-research label returned zero) and repository issue register; no atomic Claim proven. Provisional independent report; no shared-index edits.

## New primary-source distinction (checked 2026-11-22 JST)
1. Keeppower **P2150K** official product page: https://www.keeppower.com/product/keeppower-21700-5000mah-protected-li-ion-rechargeable-battery-p2150k/ — 5000mAh typical, 4900mAh min, 21.5 x 75.0mm (±0.2mm), charge +10..45°C, discharge -20..60°C, 2.5V cutoff, protective PCM advertised. **No explicit numeric maximum continuous discharge current, PCM overcurrent threshold or trip delay in the retrieved current manufacturer product page**. Its text explicitly lists "Max. discharge current" as a customization option. These fields are **UNKNOWN for the exact purchasable variant**.
2. Keeppower **P2150R** official page: https://www.keeppower.com/product/p2150r-keeppower-21700-5000mah-protected-li-ion-rechargeable-battery-max-15a/ — **15A continuous discharge** claimed for *P2150R*, 21.6 x 74.5mm (±0.2mm), charge +10..45°C, discharge -20..60°C, 2.5V cutoff. It is **not P2150K**, so 15A must NOT be copied into the P2150K BOM or safety claim. Actual P2150R PCM trip thresholds, timing, and Japan sourcing remain UNKNOWN.
3. Independent historical P2150K 2019 teardown/review https://lygte-info.dk/review/batteries2012/Keeppower%2021700%205000mAh%20P2150K%20%28Black%29%202019%20UK.html reports an older claimed 10A maximum and observed protection trips after some time at 10A. **SECONDARY HISTORICAL**, not controlled evidence for the 2026 P2150K lot; 2019 stated capacity differs from current manufacturer's 4900mAh min. Do not promote 10A to a current guarantee.

## Power-mode implications
Prior B 17:03 idealized scenario: P_HV=205V*16mA=3.28W; assumed eta_HV=.75 and eta_5=.90 -> P_SYS=4.859W (auxiliary loads excluded). At V_BAT=3.6V, ideal battery-only current=1.350A; at 3.0V, 1.620A; USB actual 450mA ideal-delivered at 5V gives 3.0V battery supplement 0.870A. These are **ASSUMED lower bounds** before BATFET/PCM/contact losses, startup peaks, thermal and source sag. Neither P2150R's 15A nor historical P2150K's 10A proves that the BQ25185/TPS61023 power path can supply these loads. Likewise 2.5V PCM cutoff is NOT a suitable asserted regulated operating voltage: BQ battery UVLO ~3.0V typical and TPS61023 low-VIN behavior need independent bounds.

## Variant decision matrix
| Candidate | Primary continuous-discharge claim | PCM trip / delay | Physical size | Thermal window | Disposition |
|---|---|---|---|---|---|
| P2150K | UNKNOWN on retrieved official page; customizable | UNKNOWN | 21.5 x 75.0mm ±0.2mm | charge +10..45°C, discharge -20..60°C | HOLD, retain original candidate |
| P2150R | 15A manufacturer product-page claim, not necessarily across-temp guaranteed | UNKNOWN | 21.6 x 74.5mm ±0.2mm | charge +10..45°C, discharge -20..60°C | ALTERNATIVE only, no substitution |
| Historical 2019 P2150K | 10A in independent older review, trip observed at 10A | time/lot UNKNOWN | not used as current drawing | not qualified | SECONDARY counterexample only |

## Qualification requests / fault behavior
- Obtain controlled current-revision PDF/spec from Keeppower or distributor for exact **P2150K orderable variant**, including cell manufacturer, PCM board revision, rated continuous and pulse discharge over temperature, overcurrent threshold MIN/MAX, delay, short-circuit, UV/OV reset and cell internal resistance.
- Verify actual cell-holder compatibility for >75mm protected button-top pack, mechanical compression, contact resistance, NTC attachment/insulation and full Japan landed cost and stock timestamp. P2150R is a separate part and may require different holder fit.
- Characterize PCM opening under HV startup or USB unplug: independent HV hardware disable/discharge must remain fail-safe with MCU unpowered. Battery-only temperature enforcement remains open per #9; PCM presence is not proof of temperature cutoff.
- Cross-check BQ25185 BATFET and TPS61023 worst-case input-current, startup and enclosure heat; do not use 15A as a system safe-current limit.
- **HV alternative work still open**: no actual 205V/16mA controller+magnetics pair qualified. MAX668 coupled, LT3757 flyback, LT8365 charge-pump and direct SYS remain comparison candidates. No stock/price claims from this run.

## Chat C review / SOP proposal
Chat C: verify that current P2150K official page does not give numeric continuous discharge, contrast P2150R 15A with exact MPN, and challenge 2019 review as non-current lot evidence; reject any implicit 10A/15A P2150K guarantee. Work: preserve BAT-001/PROTO-001/SYS-001 BLOCKED; do not edit shared decision/tree until reviewed.
SOP proposal (not direct SOP edit): Require a controlled **cell+PCM revision** and evidence-class field for every protected-cell current rating; forbid borrowing a rating from a similar Keeppower suffix. Log current stock and landed cost separately from manufacturer capability.

No purchases, PCB manufacturing, HV energization, main merge, specification or schedule changes.
