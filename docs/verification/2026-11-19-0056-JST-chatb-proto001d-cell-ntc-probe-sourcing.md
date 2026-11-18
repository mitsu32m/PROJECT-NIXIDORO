# Chat B PROTO-001D — wired 10k/B3435 NTC sourcing and protected-cell attachment gate

- Date: 2026-11-19 00:56 JST
- Role: Chat B wide research; **PROVISIONAL, NO FORMAL CLAIM**
- Parent: PROTO-001 / GitHub Issue #7; related BAT-001, PWR-002, SYS-001
- Starting branch HEAD: `1499945cba5ff32ae46bdf43a47808eb32a94474`
- Review: **PENDING REVIEW** (Chat C); conclusion: **CONDITIONAL** for electrically matching wired sensor options, **BLOCKED** for cell-contact thermal qualification, BQ25185 TS thresholds, and procurement
- Exclusions: do not claim hardware adoption, attach sensors to live cells, modify cell wraps, order, energize HV, edit shared indexes or change charging thresholds.

## 1. Novel question and overlap

PROTO-001B covered protected-cell options and PROTO-001C covered TDK's board-mount NTCG103JF103FT1. This run seeks **non-SMT wired/insulated 10k/B3435 products** for a protected 21700's surface, with current Japan-facing price/stock where found. Chat A Issue #8 owns charger TS and thermal implementation; do not duplicate it. SOP v1.1 already contains the owner's nonblocking fallback; no new SOP patch is justified.

Read at run start: docs/ai-workflow.md, docs/verification/handoff.md, docs/verification/open-issues.md, docs/verification/decisions.md, docs/tech-tree.yaml, docs/tech-tree.md, PROTO-001C, and open GitHub Issues (including #7 and #8). No verified atomic Claim; research is nonexclusive.

## 2. Candidate matrix (stock/prices are unreserved distributor snapshots)

| Exact MPN | Manufacturer evidence / source classification | Mechanical form | Sourcing snapshot | Qualification hold |
|---|---|---|---|---|
| SEMITEC **103AT-2** | [SEMITEC AT series official page](https://www.semitec-global.com/products/thermistor_at/): **SPECIFIED** R25=10kΩ ±1%, B25/85=3435K ±1%, operating -50..110°C, rated power 10mW, ~15s still-air time constant | Bead with ~12.5mm leads; **not pre-insulated cable** | [DigiKey Japan listing](https://www.digikey.jp/ja/products/detail/semitec-usa-corp/103AT-2/16579059) retrieved 2026-11-19: 3,228 units shown; ¥112 each excluding tax, ¥123.20 incl. 10% tax; manufacturer standard lead time 12 weeks. Shipping and Japan delivery date **UNKNOWN** | Requires separately qualified electrical insulation, strain relief, sensor-to-cell coupling, and connector; do not solder to cell |
| TE Connectivity **GA10K3435STM010** | [Farnell listing](https://de.farnell.com/en-DE/te-connectivity/ga10k3435stm010/ntc-thermistor-probe-10k/dp/2990332): **DISTRIBUTOR REPORTED** 10kΩ ±1%, B3435 ±1%, -35..105°C, 15s in-air thermal time constant | TPE-overmolded insulated probe, ~5×20mm, ~980mm cable, IP67 reported; physically bulky for compact 21700 housing | Distributor standard lead time 14 weeks, no confirmed Japan stock, landed JPY **UNKNOWN** | Manufacturer primary datasheet/thermal-contact suitability, cable shortening/connector treatment and enclosure fit unresolved |
| TE Connectivity **GA10K3435DM010** | [DigiKey listing](https://www.digikey.at/en/products/detail/te-connectivity-measurement-specialties/GA10K3435DM010/9842005): **DISTRIBUTOR REPORTED** 10kΩ ±1%, B25/85=3435K ±2%, -40..125°C | Insulated TPE probe ~5×20mm, ~980mm cable | European listing 170 units, €8.91 ex-VAT; Japan landed price/stock **UNKNOWN**; regional stock not interchangeable | ±2% B differs from ±1% target; BQ TS window and enclosure fit must be recalculated |
| TDK **NTCG103JF103FT1** (prior work) | [TDK manufacturer datasheet](https://product.tdk.com/system/files/dam/doc/product/sensor/ntc/chip-ntc-thermistor/data_sheet/datasheet_ntcg103jf103ft1.pdf): 10kΩ ±1%, B25/85 3435K ±1% | 0402 SMT, no lead insulation | Prior PROTO-001C; **not** a direct cell-attached probe | Board-temperature measurement is not cell surface temperature |

**Evidence caution:** TE values above are distributor-reported, not independently verified against the exact manufacturer datasheet revision this run. The SEMITEC official page explicitly defines B using R25 and R85; do not treat B25/50 as identical. DigiKey stock and pricing are transient and do not reserve parts. Standard manufacturer lead time is not a promised dispatch time.

## 3. Quantitative design implications and safety boundaries

At constant-B *sensitivity only*, `R(T)=10000 exp[3435(1/(T+273.15)-1/298.15)]` Ω. At 10°C ≈18.41kΩ; at 45°C ≈4.85kΩ. These are **ASSUMED model values**, not guaranteed BQ25185 charge-disable thresholds; use the actual SEMITEC resistance/temperature table and worst-case R25, B and cable resistance. For a 100µA assumed excitation current, at 25°C `P=I²R=0.1mW`; the 103AT-2 manufacturer dissipation factor ~2mW/°C implies ~0.05°C free-air self-heating at that illustrative condition. Actual charger TS excitation, cell contact and enclosure airflow are UNKNOWN.

For the candidate Keeppower P2150K, prior PROTO-001B reports charging +10..45°C. A 0..45°C generic JEITA policy would be inadequate at 0..10°C **if this exact cell is adopted**. This is a conditional safety observation, not proof of BQ25185 programmable hardware thresholds. Sensor lag and imperfect contact can leave the cell hotter or colder than the probe. The probe must be insulated from the cell can, mechanically restrained without damaging the protective wrap, and electrically fail-safe on open/short with MCU off. No assumption that a PCM automatically provides temperature qualification.

For SYS-001, the 205V×16mA=3.28W HV target remains unchanged; at 5V input and configured 500mA input limit, USB-only cannot sustain that target even at ideal efficiency. USB+BAT supplementation may discharge the cell; USB presence is not evidence of net charging. This is prior WORK-INT-001 evidence, **not a novel finding here**.

## 4. Selection gate and next bounded tasks

1. **Chat B / PROTO-001E:** obtain TE manufacturer's exact probe drawing/datasheet and **Japan** landed price/availability for STM010 or compact alternative; identify physically smaller *pre-insulated* 10k/B3435 probe, not just a bare bead. Explicitly check cell holder clearance, connector, cable length, IP rating relevance and whether source is stock vs standard lead time.
2. **Chat A / Issue #8:** calculate BQ25185 TS network across actual R/T and ±tolerances at +10/+45°C, charge-disable fail-safe on open/short, and 21700 thermal time lag. If hardware cannot enforce the exact cell charging window, propose a charger/cell combination change for owner approval rather than relying on firmware.
3. **Chat C:** verify the SEMITEC manufacturer table, distinguish distributor claims from manufacturer guarantees, and challenge mechanical attachment assumptions and misleading stock interpretations.
4. **Work:** decide whether to use an insulated bead assembly or integrated cell thermistor pack; only integrator updates shared issues/decisions/tech tree after review. No purchase approval.

## 5. Handoff

**PENDING REVIEW**. This is a bounded sourcing screen, not an approved BOM, cell attachment procedure, charge-temperature setting, or safety test. Exact cell, probe, attachment, TS threshold and procurement source remain UNKNOWN. No shared indexes, KiCad, main branch or automation settings changed.
