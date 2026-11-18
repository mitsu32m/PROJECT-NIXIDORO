# Chat B PROTO-001C — 10k B3435 thermistor sourcing vs cell-temperature attachment

- Date: 2026-11-18 JST
- Role: Chat B wide research, **PROVISIONAL / NO FORMAL CLAIM**
- Parent: PROTO-001 (#7), BAT-001, PWR-002, SYS-001
- Starting branch HEAD: `86c69e1c08c8c4fffd1665390ac754822a147dd6`
- Verdict: **CONDITIONAL** for a traceable NTC electrical candidate; **BLOCKED** for actual protected-cell temperature sensing, charger TS network qualification, and purchasing
- Review: **PENDING REVIEW** for Chat C. Not an adopted BOM part or an authorization for cell modification, soldering, purchase, battery tests or HV energization.

## 1. Narrow question and overlap check

Issue #7 calls for a protected 21700 and exact 10k/B3435 cell-attached NTC. The immediately preceding PROTO-001B report already shortlisted Keeppower P2150K and BW21700-50E, found +10..45°C charging for the former, and identified the absent attached NTC. This report investigates the **missing electrical thermistor MPN vs mechanical attachment mismatch**. It does not repeat transformer availability (PROTO-001A), battery product claims (PROTO-001B), charger heat (Chat A #8), SYS power modes (#4), or OVP (#6).

Read six mandatory SOP/handoff/issues/decisions/tree documents, Work INT-002, PROTO-001A/B and SYS-001F, and open Issues #1–#8. `docs/ai-workflow.md` v1.1 already contains the owner-authorized nonblocking fallback, so no duplicate SOP amendment or shared-index write is needed. The GitHub Issues queue has role-named tasks but no demonstrated atomic Claim. Proceed as a nonexclusive, append-only provisional investigation.

## 2. Traceable manufacturer NTC evidence and sourcing

**TDK NTCG103JF103FT1** manufacturer [Rev.3 datasheet, 2023-05-08](https://product.tdk.com/system/files/dam/doc/product/sensor/ntc/chip-ntc-thermistor/data_sheet/datasheet_ntcg103jf103ft1.pdf): 10kΩ at 25°C ±1%; **B25/85=3435K ±1%**, whereas **B25/50=3380K typical**. 0402 / 1005 metric SMT, maximum applied voltage 5V, maximum rated power 100mW at 25°C, permissive operating current 0.31mA at 25°C, thermal dissipation constant 1mW/°C at 25°C, operating -40..125°C. Manufacturer labels this general-grade device. These are datasheet specified limits/typicals as identified, **not** proof of physical cell attachment or BQ25185 TS compatibility.

Japanese distributor [DigiKey Japan NTCG103JF103FT1](https://www.digikey.jp/ja/products/detail/tdk/NTCG103JF103FT1/614628) lists the exact MPN, cut tape, and a 12-week manufacturer standard lead time. This is **not** a confirmed Japan-shipped delivery date, local live stock, or a tax/shipping-inclusive quote; delivered cost and stock **UNKNOWN** in this run.

A related [TDK NTCG103JF103FT1A distributor listing](https://www.digikey.jp/ja/products/detail/tdk-corporation/NTCG103JF103FT1A/23350607) showed a separate active variant, 10k ±1%, B25/85 3435K, a displayed 91 units and ¥17/unit excluding tax (¥18.70 incl. tax) in the retrieved listing. This is a **time-dependent distributor snapshot**, not a reserved quantity, and is **NOT** a substitute without checking its own current manufacturer revision, packaging, footprint and qualification. Do not transfer this variant's price or stock to FT1.

Counterexample: [Murata NCP18XH103F03RB Japanese distributor listing](https://www.digikey.jp/ja/products/detail/murata-electronics/NCP18XH103F03RB/1644665) has 10k and B25/85 3434K but B25/50 3380K and is marked not recommended for new designs; numerical similarity is not proof of an exact required part. The relevant B convention matters.

**Important mechanical mismatch:** TDK FT1 is a **surface-mount chip**, not a prewired, insulated, cell-bonded probe. The product specification does not establish an adhesive, insulating sleeve, lead harness, connector, attachment pressure, vibration/thermal aging, cell surface measurement accuracy or protection against cell-can short. No permission to solder to or modify a Li-ion cell. A chip on the PWR PCB is a **board-temperature sensor**, not necessarily the protected cell's surface temperature. An insulated externally affixed sensor/harness needs separate safety and thermal review; a vendor-integrated temperature-sensor pack is another option, but must retain the protected-cell requirement.

## 3. Reproducible beta-model check — NOT a full tolerance-qualified R/T curve

For an **assumed constant B=3435K** and R25=10kΩ, `R(T)=10000*exp[3435*(1/(T+273.15)-1/298.15)]`, temperatures in °C. The calculated resistance is:

| Temperature | Idealized R(T) |
|---|---:|
| 0°C | 28.70kΩ |
| +10°C | 18.41kΩ |
| +25°C | 10.00kΩ |
| +45°C | 4.847kΩ |
| +50°C | 4.101kΩ |

**Critical distinction:** TDK specifies B25/85=3435K and B25/50=3380K. Therefore a single B3435 exponential does **not** reproduce the manufacturer's entire R/T curve exactly, especially below 25°C; the above is a sensitivity model, **not** a threshold table to program or a guaranteed cutoff. Use the manufacturer's linked 1°C-step R/T table and worst-case R25/B/tolerance/aging before selecting TS resistor thresholds. Check the charger-specific TS voltage and source-current windows, sensor self-heating, and cable open/short detection with TI's actual BQ25185 datasheet. A nominal 10k label alone does not prove charge cutoffs.

## 4. Cell-specific charge-temperature contract

The previous [Keeppower P2150K manufacturer product page](https://www.keeppower.com/ja/product/keeppower-21700-5000mah-protected-li-ion-rechargeable-battery-p2150k/) states charge **+10..+45°C**, discharge -20..+60°C (source claim from PROTO-001B). If this cell is selected, a default charger JEITA profile that permits charging at 0..10°C would be **insufficient** unless a separate hardware-enforced inhibit covers the interval. Firmware-only temperature observation must not be presumed a fail-safe charging inhibit while MCU is off or crashed. Determine exact BQ25185 TS network's guaranteed thresholds and whether it can be configured to enforce this cell's range with worst-case NTC errors, thermal lag, contact quality, sensor open/short and USB insertion during sleep. The protected PCM's current/temperature behavior is still UNKNOWN; a PCM does not replace a charging thermistor automatically.

For a self-heating bound, `DeltaT=P_NTC / D`, where TDK D≈1mW/°C at 25°C is a **typical free-air characterization**, not the actual cell-attached value. For example P_NTC=0.1mW gives a nominal 0.1°C rise in that model; neither P_NTC nor mounted D has been measured. For cell thermal lag use a separate calibrated `tau` and surface-to-core gradient; a chip's electrical precision does not prove cell core-temperature accuracy. In a sealed PETG case, test charger IC, PCM, cell surface, connector, PCB hot spots and ambient with selected parts before asserting a safe thermal margin.

## 5. System power and alternative options

Under the existing **assumed** full display target, `P_HV=205V*16mA=3.28W`; BQ25185's 500mA-configured USB limit is 450/475/498mA at 5V table conditions per [TI BQ25185 datasheet](https://www.ti.com/lit/ds/symlink/bq25185.pdf). Thus USB-only 16mA remains NO-GO even ideally; USB plus BAT supplementation can mean **net battery discharge**, not charging. This NTC sourcing investigation **does not** relax any power contract or select a MAX668/other HV converter. Thermal control must handle both charging mode and battery-assist discharge mode, with separate permitted temperatures.

| Option | Electrical traceability | Physical thermal accuracy | Engineering state |
|---|---|---|---|
| TDK FT1 on PWR PCB | Manufacturer R/B specs traceable | **Cell surface unproven** | Candidate for board sensing only |
| TDK FT1 on separately insulated cell-adjacent flex/harness | R/B traceable | Attachment, electrical isolation, cable faults, lag **UNKNOWN** | Engineering research only |
| Protected 21700 supplied with integrated matched NTC/harness | Depends on exact pack/PCM datasheet | Potentially better mechanical repeatability | No exact protected MPN qualified |
| External packaged 10k B3435 wired probe | Depends on actual manufacturer R/T and insulation | Attachment still requires verification | Exact MPN/stock **UNKNOWN** |

## 6. Chat C review, integrator action and next task

- **Chat C:** verify TDK FT1's B25/85 versus B25/50 definition and full R/T table; confirm whether FT1A is electrically interchangeable and whether any sensor arrangement truly measures the protected cell. Challenge the constant-B values and the proposed +10..45°C charge inhibit; do not accept a threshold without BQ TS worst-case analysis.
- **Chat A (#8):** derive BQ25185 TS thresholds across resistor/NTC tolerances, source current, thermistor open/short and MCU-off states; enforce selected cell's exact charge-temperature range. Separate cell surface lag and BQ junction temperature.
- **Chat B next:** find a traceable **prewired insulated** 10k/B3435 cell sensor or protected 21700 pack with integrated NTC; confirm Japanese supplier's delivered JPY cost, real stock and the cell/PCM ratings. If unavailable, report no qualified pair and maintain the LV-first prototype split.
- **Work:** after Chat C review, reconcile PROTO-001/BAT-001 in shared issue register, BOM and tech tree; retain all procurement and HV gates.

**PENDING REVIEW / NO FORMAL CLAIM / NOT ORDER-READY**. No changes to `docs/ai-workflow.md`, shared indexes, KiCad, main, schedules, purchasing or HV work.
