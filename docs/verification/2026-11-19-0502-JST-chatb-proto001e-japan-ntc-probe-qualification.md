# Chat B PROTO-001E — Japanese sourcing and manufacturer-document conflict for insulated 10k/B3435 probes

- Date: 2026-11-19 05:02 JST
- Role: Chat B / wide research, **PROVISIONAL; NO FORMAL CLAIM**
- Parent: PROTO-001 / GitHub Issue #7; dependencies BAT-001, PWR-002, SYS-001
- Starting HEAD: `04c7936e5f592ca5fa2c3117b31e4590a979e335`
- Result: **CONDITIONAL** for electrically matched commercially listed probes, **BLOCKED** for mechanical fit and TS safety qualification. **PENDING REVIEW** for Chat C. **NOT ORDER-READY**.
- Scope: Japanese distributor pricing and original TE manufacturer records; avoid duplicating Chat A's BQ25185 TS design (#8) or Chat A's HV topology/OVP work (#2, #6).
- Read on branch: docs/ai-workflow.md v1.1, docs/verification/handoff.md, docs/verification/open-issues.md, docs/verification/decisions.md, docs/tech-tree.yaml, docs/tech-tree.md, prior PROTO-001D report, open GitHub Issues (#4, #7, #8 and HV deep-design issues). No verified atomic Claim.

## 1. Primary-source verification (2026-11-19)

**TE manufacturer:** [GA10K3435STM010](https://www.te.com/ja/product-GA10K3435STM010.html), active, 10kΩ at 25°C, B25/85=3435K, R25 tolerance ±1%, TPE overmold, 24AWG insulated stranded leads, 1000mm, open ends; the manufacturer page shows operation -40..125°C. **Important discrepancy:** TE's linked manufacturer datasheet is titled **Single Insulated TPE OM Probe 5x15mm**, while the DigiKey catalog describes **TEMP PROBE 5X20MM 1 METER LEAD** and -35..105°C. Until the exact drawing revision and dimensional tolerance are inspected, **do not treat 5×15mm or 5×20mm as a qualified mechanical envelope**, nor conflate manufacturer-page and distributor environmental ratings. Manufacturer page says product not currently available direct; this does not imply distributor zero stock.

**TE manufacturer:** [GA10K3435DM010](https://www.te.com/en/product-GA10K3435DM010.html), active, 10kΩ, B25/85=3435K, R25 ±1%, TPE overmold, 24AWG 1000mm open leads, manufacturer page -40..125°C; manufacturer linked datasheet titled **TPE OM NTC Probe 5x20mm**. Distributor lists B tolerance ±2%, so it is **not interchangeable** with STM010 for worst-case TS thresholds without recalculation.

**Distributor / Japan-facing snapshots:** [DigiKey Japan STM010](https://www.digikey.jp/en/products/detail/te-connectivity-measurement-specialties/GA10K3435STM010/9842004) showed 880 in stock, ¥2,573 before Japan consumption tax, **¥2,830.30 including 10% tax**, manufacturer standard lead time 17 weeks; [DigiKey Japan DM010](https://www.digikey.jp/ja/products/detail/te-connectivity-measurement-specialties/GA10K3435DM010/9842005) showed 170 in stock, ¥1,644 ex-tax, **¥1,808.40 incl tax**, manufacturer standard lead time 15 weeks. These are unreserved snapshots, not confirmed delivery to the project's address; shipping and checkout total **UNKNOWN**. In-stock quantities and standard lead times are different concepts, and stock can change before purchase.

**Existing inexpensive fallback:** [SEMITEC 103AT-2 official AT series](https://www.semitec-global.com/products/thermistor_at/) and [DigiKey Japan](https://www.digikey.jp/ja/products/detail/semitec-usa-corp/103AT-2/16579059) were reviewed in PROTO-001D: 10kΩ ±1%, B25/85=3435K ±1%, bare bead with leads, no finished cable/insulated cell mount, prior distributor snapshot ¥123.20 incl tax. **Do not** count it as a ready-to-mount insulated probe. Cable, insulating sleeve, connector, strain relief and attachment must be costed/qualified separately.

**Compact alternatives search:** TE Micro BetaCHIP (MCD) family [manufacturer](https://www.te.com/fr/product-CAT-NTC0065.html) describes polyimide-encapsulated miniature probes, but catalog beta options 3499/3976/4261K, not 3435K; **REJECT as drop-in B3435 replacement** without charger network redesign and approval. No newly verified, compact, pre-insulated 10k/B3435 part with a cell-safe attachment drawing and Japan landed price was established in this run.

## 2. Cost and enclosure implications

| MPN | 10k/B3435 match | Insulated assembly | Snapshot Japan 1pc incl JCT | Unqualified interface |
|---|---|---|---:|---|
| TE GA10K3435STM010 | YES; ±1% R, distributor ±1% B | TPE overmold, 1m 24AWG leads, open ends | ¥2,830.30 | **5×15 vs 5×20mm discrepancy**, 1m cable, cell holder clearance, thermal coupling, connector |
| TE GA10K3435DM010 | YES nominal; distributor ±2% B | TPE overmold, 1m leads, open ends | ¥1,808.40 | 5×20mm, B spread, cell holder clearance, thermal coupling, connector |
| SEMITEC 103AT-2 | YES; ±1% R/B | **NO**; short bare leads | ¥123.20 (prior snapshot) | Insulation, contact and strain relief, harness, thermal lag |

Difference STM010 versus DM010 = ¥1,021.90 per unit including JCT (assuming unchanged 1pc listings). Against the tentative first-order target ≤¥40,000, STM010 costs ~7.1% and DM010 ~4.5% **before** connector/shipping; these are budgeting comparisons, not a complete BOM. A 1m lead inside a small PETG enclosure requires documented routing and secure strain relief; shortening or reterminating an assembled probe is not manufacturer-qualified by default. Need 21700 holder CAD envelope and exact protected-cell dimensions, not only nominal Ø21×70mm.

## 3. Temperature, failure and electrical caveats

A selected protected cell's charging temperature window (P2150K previously reported +10..45°C) is not automatically enforced by BQ25185 TS; Chat A Issue #8 must derive real TS resistor thresholds using the selected manufacturer's R(T) table and worst-case B/R tolerances. For constant-B sensitivity only, `R(T)=10k*exp(3435*(1/T_K-1/298.15))`: ~18.4kΩ at 10°C, ~4.85kΩ at 45°C; not guaranteed cutoffs. Need sensor-to-cell thermal impedance, temperature lag, sensor self-heating, open/short fault default, MCU-off charging and independent charge-disable behavior. If fixed hardware thresholds cannot enforce the cell's charge window, **change cell/charger combination for owner approval**, not firmware-only safety assumptions.

Cell can/wrap must not be punctured, soldered or compromised. TPE insulation alone does not prove correct cell attachment or electrical isolation under wear. Do not adopt probe before physical fit and thermal contact qualification. No bench operation or battery modification authorized by this report.

## 4. SYS-001 linkage and alternatives

These sensor options do not change the existing **205V×16mA=3.28W** HV design target or prove USB-only 500mA operation. At USB 5V and BQ25185's configured 500mA input current limit, USB-only full target remains **NO-GO** even with ideal conversion. USB+BAT may supply full load with **net battery discharge**, not net charging; record signed IBAT. Direct SYS→HV (LM5155/LT3757A) remains a comparison only, with actual magnetics and thermal feasibility unresolved. No power-path topology selected.

## 5. Next bounded tasks and handoff

1. **Chat C:** independently resolve TE STM010 manufacturer's 5×15mm datasheet title vs distributor 5×20mm description, environmental ranges, and verify Japanese landed cost interpretation. Correct earlier PROTO-001D's ambiguous physical dimension; do not silently assume a 20mm probe fits.
2. **Chat B / PROTO-001F:** obtain exact mechanical drawing and contact/adhesive recommendations from TE, protected 21700 holder + wrap geometry and compact pre-insulated B3435 alternative with Japanese stock. If none exists, cost the 103AT-2 harness and document engineering qualification steps instead of claiming a ready-made solution.
3. **Chat A / Issue #8:** quantify BQ TS 10/45°C hardware thresholds, ±1/2% B impact, fail-safe fault behavior, low-cell and USB transition heating; keep its ownership separate.
4. **Work:** decide prototype staging (LV-first vs standalone HV) and procurement holds; integrate only C-reviewed parts and exact source citations into shared BOM/tech-tree.

**PENDING REVIEW.** No Claim, no shared index/SOP edits (v1.1 already includes provisional fallback), no KiCad, order, PCB, HV operation, main merge, or schedule changes.
