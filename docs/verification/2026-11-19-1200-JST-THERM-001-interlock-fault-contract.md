# 2026-11-19 1200 JST — THERM-001 / Issue #9: temperature-interlock fault-state contract

**Role:** Chat A deep-design. **Claim:** provisional; NO FORMAL CLAIM (atomic claim protocol not proven). **Review:** PENDING REVIEW.
**Verdict:** CONDITIONAL for architectural separation and logic requirements; BLOCKED for component-level safety qualification and hardware adoption.
**Starting SHA:** UNKNOWN (connector file reads return blob SHA, not branch HEAD; do not misrepresent blob as commit).
**Baseline:** `docs/ai-workflow.md`, `docs/verification/handoff.md`, `docs/verification/open-issues.md`, `docs/verification/decisions.md`, `docs/tech-tree.yaml`, WORK-INT-003, A PWR-002B 07:56, Issue #9 and open Issues #2/#6/#8 read on the working branch.

## Bounded question and exit
Given actual Rev.A U1 /CE=GND and TS/MR tied to CELL_NTC, how should independent charge inhibition, battery-only temperature detection and energy shutdown interact when MCU is unpowered or NTC fails? Exit: explicit truth table, proposed signal/power boundaries, quantitative sensor-bias constraint, and remaining primary evidence. No schematic edit, purchase, energization or adoption.

## Primary evidence and classifications
- TI BQ25185 Rev.B (Aug 2026), https://www.ti.com/lit/ds/symlink/bq25185.pdf : **manufacturer** /CE is charge enable, not SYS disconnection; §6.4 p19 TS measurement adapter YES, battery-only NO; TS/MR multifunction. The existing /CE=GND is **repository-confirmed** via WORK-INT-003 netlist inspection, not independently reinspected here.
- Keeppower P2150K official candidate page, https://www.keeppower.com/ja/product/keeppower-21700-5000mah-protected-li-ion-rechargeable-battery-p2150k/ : charge +10..45°C, discharge -20..60°C **manufacturer candidate limits, not selected cell**. PCM thermal cutoff not established.
- TE GA10K3435STM010 manufacturer sheet linked in WORK-INT-003: sensor R/T nominal, not guaranteed installed cell surface error or response. Existing ideal direct-NTC TS window near 1.74..59.51°C is **model**, not a pack-safe range.

## Proposed separation of functions (architecture only)
1. **CHARGE_PERMIT_HW:** normally false, enabled only when adapter present, cell sensor valid, and independently evaluated cell temperature is inside selected pack's *derated* charge interval. Drive BQ /CE with hardware-default HIGH/inhibit (requires deliberate change from existing hard GND); MCU may request inhibit but must not override hardware fault. Confirm actual /CE input levels, leakage, startup and power domain from datasheet before component choice. A latch is not sufficient unless power-up state is safe.
2. **LOAD_PERMIT_HW:** normally false, enabled only with cell-temperature monitoring powered in battery-only mode and valid temperature/pack status. It must interrupt the energy source to HV and other nonessential loads using an independently specified load switch/enable path; firmware BL, MAX668 shutdown pin and BQ /CE alone do not isolate stored HV energy. Consider retaining essential alarm/RTC only after standby and reverse-feed verification.
3. **HV_FAULT_STOP:** independent hardware shutdown and defined output-capacitor discharge per HV-002/003 and Issue #6. Temperature fault requires load stop and HV discharge, including MCU reset and adapter removal. Do not equate logical off with HV-safe touch voltage.
4. **Sensor acquisition:** preferred research direction is **separate dedicated temperature-sense network** for the hardware interlock, rather than connecting an MCU ADC directly to the BQ TS/MR pin. Shared single physical NTC is possible only after a full bias and fault-interaction analysis; a second physically cell-coupled sensor provides independence but adds cost, mechanical attachment and common-mode detachment risk.

## Minimum state and fault matrix (requirements, not tested behavior)
| Mode/fault | Charge permit | HV/load permit | Required physical outcome |
|---|---|---|---|
| USB present, valid cell T inside approved charge band | May enable | Only if separate load and power budgets valid | Monitor cell and board |
| USB present, cell too cold/hot for charge but within approved discharge band | OFF | May remain ON if separately proven | Do not conflate charge and discharge windows |
| Battery only, valid discharge-range T | OFF (no adapter) | May enable | Temperature monitor must remain powered |
| Battery only, T outside discharge band | OFF | OFF | Hardware HV stop + discharge |
| NTC open, short, intermittent or detached | OFF | OFF | Latched fault/recovery only after valid requalification; detached sensor may appear electrically valid and needs attachment mitigation |
| MCU off/reset/firmware hung | OFF unless independent hardware explicitly qualifies charge | OFF by default | No reliance on GPIO boot level |
| USB inserted/removed, brownout, monitor supply lost | OFF until requalified | OFF until requalified | No backfeed or transient unintended enable |
| Pack PCM opens or cell absent | OFF | OFF | No SYS→BAT reverse feed; HV discharge independently |

**Important nuance:** A simple high/low temperature comparator does not prove open/short fault detection; use valid-range/window checks with explicit diagnostics. A single sensor detached from the cell can produce an in-range reading, so redundancy or mechanically qualified attachment is necessary for a safety claim. The above OFF defaults are **proposed requirements**, not demonstrated circuit behavior.

## Quantitative shared-NTC loading screen
For the **assumed** ideal BQ TS bias I=38 µA and nominal TE NTC R(10°C)=17.95 kΩ, R(45°C)=4.92 kΩ (WORK-INT-003), a parallel ADC input/bias resistor `R_L` to ground gives:
`R_eff=R_NTC*R_L/(R_NTC+R_L)`, `V_TS=I*R_eff`.
At 10°C with an assumed 100 kΩ loading resistor, R_eff=15.22 kΩ, V_TS=0.578 V vs unloaded 0.682 V (**-104 mV, -15.2%**).
At 45°C, R_eff=4.69 kΩ, V_TS=0.178 V vs 0.187 V (**-8.8 mV, -4.7%**).
This is a **counterexample** to the assumption that a high-impedance-looking additional analog branch is automatically nonintrusive. It is not a proposed resistor value or a complete ADC model. Actual ADC input impedance is dynamic and GPIO protection diodes may inject into an unpowered rail. TS/MR short behavior may also invoke reset/factory semantics; verify exact timing/thresholds before any shared-sensor topology.

## Architecture comparison and explicit schematic-change request (NOT authorization)
- A: Retain BQ25185 and add independent always-on window detector, fail-safe /CE pull-up and qualified load/HV isolation. **Potentially viable;** needs supply/reference, independent thermal limits, sensor topology, quiescent current, pin assignment, physical fail-safe switch, startup/reset and thermal proof.
- B: Pack with **documented** thermal cutoff for both charge and discharge plus independent HV stop/discharge. **Potentially viable only** if exact PCM thresholds, fault modes and charger compatibility are guaranteed; generic 'protected' is insufficient.
- C: Change charger/pack to a documented configurable thermal window and independent battery-only monitor. **Potentially viable**, requires architecture, PCB, budget and procurement re-review.
- Requested future schematic change scope: remove hard /CE-GND only after review; add explicit CHARGE_PERMIT_HW, LOAD_PERMIT_HW, TEMP_FAULT and HV_STOP interface; define independent monitor power and safe default pull states, connector pin count, test points, isolation and output discharge. No KiCad modifications made here.

## Remaining qualification gates
- Select actual cell/PCM and pack charging/discharging limits and exact NTC assembly, including guaranteed R/T, tolerances, attachment and maximum thermal lag (Chat B #7).
- Establish monitor/reference/comparator and load-switch candidates from manufacturer specs, quiescent current and all temperature/brownout/short conditions; quantify fault latency versus cell heating and stored HV energy.
- Demonstrate hardware default states for loss of MCU, adapter, cell, sensor and monitor power, plus hysteresis, startup, recovery and sensor disagreement.
- Include thermal budget in sealed PETG and 50k JPY BOM. Do not adopt comparator thresholds at nominal pack endpoints without sensor and thermal error margin.
- Chat C to review Work's limited positive-Rs/Rp ratio proof and this fault table; Work to integrate shared ledgers only after review.

**Disposition:** CONDITIONAL architecture contract; BLOCKED actual hardware and safety; PENDING REVIEW. Prior PWR-002B established TS gap; this report adds explicit independent interlock truth table, quantitative TS loading counterexample, power-failure defaults and future change boundary. No hardware tests, orders, PCB fabrication, main merge or specification changes.
