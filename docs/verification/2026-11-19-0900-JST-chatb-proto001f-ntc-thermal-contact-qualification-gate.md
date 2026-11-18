# Chat B PROTO-001F — NTC thermal-contact qualification and enclosure fit gate

- Date: 2026-11-19 09:00 JST
- Parent: PROTO-001 / Issue #7; linked BAT-001, SYS-001, PWR-002A / Issue #8
- Role: Chat B wide research, PROVISIONAL; NO FORMAL CLAIM
- Review: **PENDING REVIEW** for Chat C; **BLOCKED** for actual cell-temperature qualification and mechanical fit; **NOT ORDER-READY**
- Branch: `codex/reva-integrated-prototype-review`
- Starting HEAD: **UNKNOWN**. GitHub connector read branch files, but available branch/commit discovery did not return an authoritative branch-tip SHA. Last independently documented earlier Chat B commit `5fcc7fb7d427` is NOT asserted to be current HEAD.
- Read: docs/ai-workflow.md v1.1, docs/verification/handoff.md, docs/verification/open-issues.md, docs/verification/decisions.md, docs/tech-tree.yaml, docs/tech-tree.md, latest PROTO-001E and PROTO-001D reports, Issue #7 and #8 and issue register. Formal atomic Claim not verified.
- Scope: mechanically/thermally qualifying an insulated NTC on a protected 21700; **not** charger TS resistor design (Chat A #8), not repetition of Japan prices or 5V/HV controller screens.

## 1. Exact bounded question

Can an existing 10k/B3435 insulated probe be qualified as a **cell-temperature** sensor in the compact PETG assembly, rather than merely an electrically compatible thermistor? Exit: identify measured dimensions, thermal-contact evidence, fail-safe checks and a falsifiable acceptance contract. No candidate may be called mechanically qualified until real holder/cell/probe drawings and approved measurements exist.

## 2. Evidence carried forward, not independently reverified this run

- TE manufacturer product records: [GA10K3435STM010](https://www.te.com/ja/product-GA10K3435STM010.html) and [GA10K3435DM010](https://www.te.com/en/product-GA10K3435DM010.html). Both nominal 10k/B25/85 3435; prior report records STM010 datasheet-title **5×15mm** versus DigiKey **5×20mm**. Treat this as an unresolved exact drawing/revision discrepancy. DM010 distributor B tolerance ±2% versus STM010 ±1%.
- [SEMITEC AT series](https://www.semitec-global.com/products/thermistor_at/) 103AT-2: electrically plausible small bead but not an insulated ready-made harness.
- Prior PROTO-001E dated Japan listings: STM010 ¥2,830.30, DM010 ¥1,808.40, 103AT-2 ¥123.20 including assumed 10% JCT. These are historical **distributor snapshots**, not current stock or delivered cost.
- Protected Keeppower P2150K prior manufacturer-derived +10..45°C charging interval; **cell adoption not approved**. Exact protected cell diameter/length including wrapper and button/protector, actual holder internal clearance and mechanical tolerances are UNKNOWN.

## 3. Thermal coupling: measurable model, not assumed safety

Let T_cell be cell surface temperature at the hottest relevant spot, T_NTC sensed probe temperature, R_th,contact the effective thermal resistance from cell surface to probe and C_th,probe the effective probe heat capacity. A first-order model gives tau=R_th,contact*C_th,probe; for a cell ramp dT_cell/dt approximately r, a first-order probe can lag by approximately r*tau after transients. This is an **ASSUMED sensitivity model**, not a manufacturer guarantee and not a bound during fast fault heating. Example only: r=1°C/min and tau=30s produces about 0.5°C steady ramp lag. If r=3°C/min and tau=60s, lag is about 3°C. Neither tau nor r is measured. In air, probe time constants cannot be used as guaranteed cell-contact time constants.

If cell max charge temperature is 45°C, a sensor reporting 45°C while lagging by 3°C may correspond to 48°C cell temperature. Similarly, a cold cell at 8°C with a warmer probe at 11°C may be charged below a +10°C minimum. Therefore qualifying only a static 10k/B3435 curve is insufficient; both hot and cold transition directions matter.

Thermistor constant-B *sensitivity*, not a guaranteed manufacturer R/T table: R(T)=10000*exp(3435*(1/(T+273.15)-1/298.15)) ohms. At 10°C ~18.4kΩ; at 45°C ~4.85kΩ. Need exact manufacturer table and worst-case tolerance/cable/connector error before Chat A defines charger thresholds.

## 4. Mechanical/electrical qualification matrix

| Evidence required | TE STM010 / DM010 | SEMITEC 103AT-2 assembly |
|---|---|---|
| Exact drawing and revision, width/height/tolerance | UNKNOWN; 5×15 vs 5×20 conflict for STM010 | Bead dimensions known by series, finished assembly dimensions UNKNOWN |
| Actual protected 21700 outer diameter/length, holder clearance | UNKNOWN | UNKNOWN |
| Contact location and retained pressure without cell-wrap damage | UNKNOWN | UNKNOWN |
| Insulation integrity and routing/strain relief in PETG | Overmold exists; installed assembly unqualified | Must be designed and qualified |
| Cell-vs-probe hot/cold lag under realistic charge/operation | UNKNOWN | UNKNOWN |
| Open/short/loose-probe response with MCU off | UNKNOWN; Chat A #8 hardware TS owner | UNKNOWN; Chat A #8 hardware TS owner |
| Full Japan landed cost including cable/connector/mount | UNKNOWN | UNKNOWN |

Mechanical fit requires `clearance_min = holder_free_space_min - probe_envelope_max - wire_bend_and_strain_relief_allowance_max > 0` under real CAD and manufacturing tolerances. Neither dimension is known; do not declare fit from a nominal 21700 diameter or a 5mm catalog width. Any adhesive or band must not compromise the protected cell's wrap, vent or protection circuit.

## 5. Proposed approval-gated qualification contract (not permission to test)

- Record exact cell MPN and manufacturer charge temperature interval, complete cell+holder CAD, exact sensor drawing revision, full wiring/connector and assembly photos.
- Under approved low-voltage/temperature-controlled supervised characterization only, compare reference cell-surface sensors at likely hot spots against NTC readout during charge, discharge, cold-to-warm and warm-to-cold transitions. Log worst signed delta and time lag. Include sensor displacement and wiring faults.
- Chat A #8 must allocate a **quantitative temperature error budget**: NTC R/T tolerance, divider/TS thresholds, cable resistance, contact error, thermal lag, placement and reference-sensor uncertainty. Require conservative hardware charging inhibition throughout actual cell prohibited temperature intervals including MCU off and single sensor faults.
- If verified hardware TS cutoffs cannot enforce the selected cell interval with error margin, escalate a **cell/charger/sensor architecture alternative** to Work and owner. Do not relax cell rating or silently rely on firmware.
- Explicit independent Chat C review of evidence, followed by Work integration; no hardware acceptance before owner approval.

## 6. Decision and next task

**CONDITIONAL**: retain STM010/DM010 as nominal electrically matched insulated probe options; retain 103AT-2 as lower-cost custom-harness candidate. **BLOCKED**: no sensor/holder combination is mechanically or thermally qualified, and no procurement authorization exists.

Chat B next: obtain actual 21700 holder drawing and protected-cell mechanical envelope; check TE exact dimensional PDF and identify connector/strain-relief and costed assembly. Chat A #8 owns charger TS hardware threshold and fault behavior. Chat C reviews this thermal-lag distinction. SYS-001 target 205V*16mA=3.28W unchanged; USB 5V/500mA alone cannot sustain this even ideally; USB+BAT assist may discharge the cell.

No shared-index/SOP edits, KiCad changes, purchases, PCB manufacturing, HV application, main merge, or schedule changes.
