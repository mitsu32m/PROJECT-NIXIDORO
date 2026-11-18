# Chat B PROTO-001B — protected 21700 traceability and NTC integration screen

- Date: 2026-11-18 JST; task PROTO-001B, Issue #7, related BAT-001/PWR-002/SYS-001.
- Role: wide-research; **PROVISIONAL, NO FORMAL CLAIM**; **PENDING REVIEW** for Chat C.
- Starting HEAD: `562a571f35f7027a62986b51cf525fa94a3ec2f0`.
- Verdict: **CONDITIONAL** as a sourcing shortlist; **BLOCKED** for battery/NTC qualification and procurement. No order, schematic change or HV operation.
- Sources checked: six startup docs, 2026-11-18-1302 Chat B sourcing report, Work handoff, open GitHub Issues #1–#8. This report focuses on the battery/NTC portion of Issue #7 and avoids repeating transformer Issue #2 or SYS-mode Issue #4.

## Manufacturer and retailer evidence (2026-11-18 web observation)

| Candidate | Traceable source | Stated attributes | Open qualification |
|---|---|---|---|
| **Keeppower P2150K** | [manufacturer Japanese product page](https://www.keeppower.com/ja/product/keeppower-21700-5000mah-protected-li-ion-rechargeable-battery-p2150k/) | Protected 21700; 5000mAh nominal, 4900mAh minimum; 3.6V nominal; 4.2V maximum charge; 2.5V discharge cutoff; 21.5mm diameter ×75.0mm length ±0.2mm; charge temperature +10 to +45°C, discharge -20 to +60°C; standard charge 2450mA. **Manufacturer stated**, but product page does not by itself establish the protection-board continuous discharge trip/current, cell-internal resistance or fitted 10k B3435 NTC. | Exact protection trip thresholds/tolerances, continuous discharge limit, holder geometry and contact resistance, terminal style, Japanese-stock and delivered JPY price **UNKNOWN**. The +10°C charging minimum must be considered; a generic 0°C battery charge assumption is unsafe for this candidate. |
| **BLACK WOLF BW21700-50E** | [Japanese brand/store product page](https://www.blackwolf.co.jp/items/134648855) | Protected 21700, nominal 5000mAh / min 4900mAh, nominal 3.63V, 4.2V max charge, 21.5×75±0.5mm, listed ¥1,800. Source lists both “16A discharge current” and “1C maximum discharge performance” with no reconciled conditions. **Seller/brand claim**, not independently validated protection-board datasheet. | Apparent 16A versus 1C (=~5A for 5Ah) inconsistency: **DO NOT select current limit from either line**. Obtain manufacturer's controlled electrical spec, PCM limits and temperature derating; price is displayed, not delivered quotation or confirmed stock. |
| **Generic 21700 protected button-top** | [retailer listing](https://item.rakuten.co.jp/surprise-collection/21700-j-1/) | 5000mAh, 74.5mm length, 21.6mm diameter, protection and PSE claims. **Retailer claim**. | No traceable cell/PCM manufacturer or qualified current/temperature/NTC; cannot use as engineering baseline. |

**Explicit exclusion:** Unprotected 21700 or a listing saying “requires device-side protection” is not equivalent to the specified protected-cell requirement. A PSE claim alone is not evidence of PCM current-trip behavior or a cell-attached temperature sensor.

## Power and thermal consistency checks

Existing model (ASSUMED, not measured): 205V ×16mA =3.28W output, `P_SYS≈6.60W` at assumed HV η70%, 5V η85%, 0.5W logic and 0.5W other SYS loads. At nominal 3.6V, ideal `I_BAT≈6.60/3.6=1.83A` battery-only **before** BATFET, PCM, contact and cell resistance; at 3.0V ideal `I_BAT≈2.20A`. These are power-balance minima, not peak switch current or a guaranteed cell operating point. BQ25185/TPS61023 startup/low-cell stress remains Chat A Issue #8.

Assume (for sensitivity only) `R_total` cell+PCM+holder+contacts of 0.05/0.10/0.20Ω, and 2.2A steady current: `P_loss=I²R=0.242/0.484/0.968W`. **ASSUMED** resistance values are not P2150K/BW21700-50E data and must not be promoted to guaranteed loss. They illustrate why battery/PCM and holder temperatures inside sealed PETG matter. Charge mode is distinct: USB present with BAT supplement means discharge, not simultaneous positive net charging. BQ input 5V ×450–498mA gives only 2.25–2.49W at its configured input-limit corners; USB-only 3.28W HV output is NO-GO even ideally.

A holder sized for bare 21700 length ~70mm may not fit the 75mm protected products. Confirm actual positive/negative terminal shape, compression range, contact heating and reverse-insertion protection before mechanical design.

## NTC requirement and gating

The Rev.A proposal assumes a **cell-attached 10kΩ, B=3435K NTC** into BQ25185 TS network. Neither candidate page establishes an integrated/attached NTC of this exact characteristic. Therefore **BAT-001 is not complete**. A board-mounted ambient thermistor is not automatically a cell-temperature measurement; confirm electrical TS window against the exact charger datasheet and thermistor R(T) tolerance, thermal coupling, insulation and cable open/short behavior. The Keeppower candidate's stated +10 to +45°C charge range must be enforced by a justified TS/firmware/hardware design, not assumed covered by generic charger JEITA defaults.

Do not use an arbitrary “10k NTC” as proof of B3435 fit. Require exact MPN, resistance tolerance at 25°C, beta tolerance or R/T table, physical attachment, insulation, charge-temperature cutoff, fault behavior and supplier.

## Decision matrix

- **P2150K**: best manufacturer-traceable protected candidate among sources checked, but no confirmed Japanese price/stock, PCM discharge specification or attached NTC. **SHORTLIST ONLY**.
- **BW21700-50E**: domestic brand listing with price, but contradictory current wording; **HOLD pending clarification**.
- **Generic protected listings**: insufficient traceability for safety-critical design; **DO NOT ADOPT**.
- **Any battery option**: do not approve charge/discharge current, enclosure, BOM or purchase without verified exact cell/PCM/NTC and thermal limits.

## Chat C / Work handoff and next tasks

1. Chat C: verify product-page claims against full controlled datasheets; challenge P2150K charging minimum +10°C and BW 16A/1C contradiction; independently review resistance/thermal sensitivity without treating assumptions as measurements.
2. Chat B next PROTO-001C: exact Japanese seller stock and delivered JPY pricing for P2150K, exact NTC 10k B3435 with R/T table and connector, and a separate neon lamp MPN; prioritize traceable source over generic listings.
3. Chat A Issue #8: calculate and measure low-cell BQ BATFET, PCM and TPS61023 transients/heat, battery absence and USB assist; obtain cell maximum continuous discharge and cutoff behavior.
4. Work: update shared BOM, BAT-001 and tech tree only after review; retain prototype staging and deadline, no procurement authorization.

**PENDING REVIEW. NOT ORDER-READY.** Shared indexes and scheduler unchanged; no formal Issue Claim. Primary source here is a manufacturer's product page, **not** a complete certified battery pack test report.
