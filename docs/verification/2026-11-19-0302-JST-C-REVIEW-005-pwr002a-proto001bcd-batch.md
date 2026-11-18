# C-REVIEW-005 — PWR-002A and PROTO-001B/C/D independent batch review

Date: 2026-11-19 03:02 JST. Role: Chat C, independent reviewer. **NO FORMAL CLAIM.** Starting working-branch HEAD: `4d29082e26ee67005cda484dfe3eef1aec0093b4`. Scope: 4 Chat A PWR-002A reports (#8) and 3 Chat B protected-21700/NTC reports (#7); seven reports reviewed by claim group, not a full manufacturer qualification. Shared indices are Work-owned and unchanged. Exit: verify key algebra and manufacturer distinctions, identify corrective actions, give Work a decision package.

## Source reports (all PENDING REVIEW when read)

- A 12:03: [low-cell BATFET/path thermal](2026-11-18-1203-JST-PWR-002A-lowcell-batfet-path-thermal.md)
- A 16:00: [OCP-constrained envelope](2026-11-18-1600-JST-PWR-002A-current-limit-power-envelope.md)
- A 20:00: [HV-enable vs current gate](2026-11-18-2000-JST-PWR-002A-hv-enable-vs-current-envelope.md)
- A 23:40: [load-step headroom](2026-11-18-2340-JST-PWR-002A-hv-enable-load-step-headroom.md)
- B 17:00: [protected-cell sourcing](2026-11-18-1700-JST-chatb-proto001b-protected-21700-source-screen.md)
- B 20:00: [NTC attachment](2026-11-18-2000-JST-chatb-proto001c-ntc-attachment-qualification.md)
- B 00:56: [wired probe sourcing](2026-11-19-0056-JST-chatb-proto001d-cell-ntc-probe-sourcing.md)

## Independent primary checks and classifications

**TI BQ25185 Rev.B, SLUSF65B, revised Aug 2026**: https://www.ti.com/lit/ds/symlink/bq25185.pdf , pp. 5–8, 18–19. **SPECIFIED under test conditions** RON_BAT 115mOhm TYP / 140mOhm MAX at VBAT=4.5V and IBAT=400mA. The 140mOhm at multiamp is an **ASSUMED extrapolation**, not a guaranteed high-current or hot-cell bound. BATOCP 3.13A is **TYP** at VBAT=4V; OCP accuracy ±18% specified at 27°C; 2.5666A is an **illustrative calculation**, not a guaranteed continuous safe current. JEDEC thetaJA 68.3°C/W is a reference thermal metric, not sealed-PETG board thermal resistance. BQ TS/MR with 10k B25/85=3435K is supported; VHOT_ENTRY 0.105–0.125V, VCOLD_ENTRY 0.9575–1.0575V, ITSMR 36.5–39.5uA adapter present. **Crucial**: Table 6-2 states TS measurement **YES in adapter mode, NO in battery-only mode**. Thus BQ TS does not continuously monitor cell temperature while running from battery alone; any battery-only discharge thermal safety contract requires separate mechanism/qualification. TS charging inhibit is not a substitute for discharge temperature monitoring. Also the TS/MR multifunction pushbutton/factory-mode interaction must be considered.

**SEMITEC 103AT-2 official AT-series page**: https://www.semitec-global.com/products/thermistor_at/ , rating table: 10kOhm R25 ±1%, B25/85=3435K ±1%, ~2mW/°C dissipation, ~15s **still-air** thermal time constant, 10mW rated at 25°C, -50..+110°C. **SPECIFIED** electrical candidate; not pre-insulated, not proven to measure protected-cell surface. Its official R/T table requires contact details and was not retrieved. TE probe values and regional stock/prices in B's report are **DISTRIBUTOR-REPORTED / NOT INDEPENDENTLY VERIFIED** this review. Exact P2150K/BW21700-50E pack manufacturer limits and seller stock were **NOT independently reverified**; all remain sourcing candidates only.

## Independent numerical review

Assumptions common to A: battery-only P_SYS=6.60084W constant, R_BQ=0.14Ohm, R_EXT variable, Vgate=3.4V **provisional project policy**, not TI guaranteed threshold. Equations: Vsys=Vb-I R, P=I(Vb-I R), low-current root I=(Vb-sqrt(Vb²-4RP))/(2R). For Vb=4.0V, R=0.24Ohm: I=1.85715047A, Vsys=3.55428389V. Pgate=3.4*(4.0-3.4)/0.24=8.500W; headroom=1.89916W; local dVsys/dP=-0.07720597V/W; minimum assumed Vb at baseline gate=3.86594165V. **ACCEPTED (static algebra only)** for these results. A's 3.3V / 0.34Ohm example: I_low~2.819A exceeds the 2.5666A *27°C-only* OCP proxy. The OCP-based maximum power Icap*(3.3-Icap*0.34) ~6.230W <6.60084W. **ACCEPTED (illustrative necessary screen only)**.

The maximum-power/discriminant root is not a stable operating guarantee. The assumed 3.4V SYS enable gate, constant cell-terminal V, fixed resistance, constant conversion efficiencies, no capacitor transient, and static equilibrium exclude startup/load-step undershoot, UVLO hysteresis, protection FET dynamics, cell polarization and heat. The 1.89916W figure is **not** an allowable instantaneous pulse. At 3.6V with assumed R_BQ=0.14Ohm, static Pgate=4.857W <6.60084W, so OCP-only passing is operationally irrelevant while the provisional gate is enforced. **CONDITIONAL** for analytical screening; **BLOCKED** for hardware operation.

For NTC constant-B sensitivity: 10k*exp(3435*(1/283.15-1/298.15))=18.4104kOhm at 10°C, and at 45°C 4.84687kOhm. **ACCEPTED (idealized exponential arithmetic)**, but a B25/85 value does not prove exact R(T) below 25°C or guaranteed TS cutoff. Actual full R/T table, NTC R25/B tolerances, BQ TS source current/threshold corners, contact thermal lag, cable open/short, MCU-off charging and selected pack charge range must be combined. **CHANGES_REQUESTED** if any 10..45°C inhibit or charge approval is inferred merely from the B3435 label. BQ's built-in thresholds are not established as matching a +10°C cell cutoff; a cell with such minimum charging temperature must be protected by a verified hardware charging inhibit.

## Per-claim verdicts

| Claim | Verdict | Scope |
|---|---|---|
| A constant-power quadratic and R/current tables | ACCEPTED | Illustrative algebra only; not actual component curve |
| A 27°C OCP proxy and 3.4V SYS gate conjunction | CONDITIONAL | Correct necessary static comparison, not a safe current limit |
| A 4.0V/0.24Ohm 1.89916W headroom | ACCEPTED | Steady-state algebra only; transient permission BLOCKED |
| A BATFET junction and external-cell-path thermal qualification | BLOCKED | Real high-current R, PCB/cell temperatures and 5V inductor absent |
| B protected 21700 candidates | CONDITIONAL | Shortlist only; pack PCM/temperature/NTC provenance not independently verified |
| B TDK chip vs cell-attached sensor distinction | ACCEPTED | Mechanical/electrical category distinction only |
| B SEMITEC 103AT-2 electrical R25/B candidate | ACCEPTED | Manufacturer page rating only; assembly qualification BLOCKED |
| B TE probe and Japan sourcing | CONDITIONAL | Distributor claims, live availability and drawing not verified |
| B BQ25185 TS matching a selected cell's charge window | BLOCKED | Worst-case thresholds, cell temperature and faults not proven |

## Work decision package — P0 BAT-001/PWR-002A/PROTO-001

**Decision:** whether to adopt any cell/NTC and permit full-load HV from 1S battery. **A/B claim:** illustrative 6.60084W SYS load may pass mathematical battery-only gate only in limited high-cell-voltage corners; traceable 10k B3435 sensors and protected-cell candidates exist. **Independently verified:** static equations and numerical examples; TI BQ RON/OCP/TS test conditions and adapter-only TS measurement; SEMITEC 103AT-2 manufacturer R25/B rating. **Unverified:** actual pack PCM and NTC attachment, cell resistance, charge range and cold-charge inhibit, TS corner thresholds, 5V TPS61023/L1 load-step behavior, thermals and procurement. **Alternatives:** reduce normal HV load through owner-approved mode contract, defer full HV to independent staged prototype, use manufacturer-qualified integrated pack NTC or a proven insulated wired probe, or change cell/charger combination only after owner approval. **System impact:** high BATFET/external I²R and low-SYS margin may prevent 16mA battery operation; charger TS does not independently protect battery-only discharge temperature; sealed PETG heat and prototype layout remain safety gates. **Recommendation:** do not adopt battery/NTC or full-HV enable; require Chat A #8 to supply guaranteed charger TS cold/hot boundaries and separate discharge thermal strategy; Chat B #7 to supply exact pack/PCM/insulated probe drawing and Japanese availability; Work to keep BAT-001/PWR-002A and procurement gates locked. **Provenance:** starting HEAD `4d29082e26ee67005cda484dfe3eef1aec0093b4`; all source report paths above; current review commit is the GitHub commit that creates this file.

## Queue and next steps

At this start HEAD, 7 PENDING REVIEW reports were reviewed in this bounded batch. Other unreviewed high-impact candidates include A 2026-11-17 23:59 tapped-boost ideal model, A 2026-11-18 03:55 tapped CCM stress, A 07:56 rectifier/capacitance, B 13:02 magnetics sourcing; **at least 4** remaining, exact global count not established because status may live in reports and issues and prior reviews cover some claims. Oldest confirmed outstanding from that set: A 2026-11-17 23:59. Next priority: #2 coupled/tapped topology and B actual magnetics sourcing, then #6 OVP joint Cmin/Cmax and #8 charger TS cutoff/discharge thermal proof.

No physical tests, purchases, HV energization, PCB fabrication, main merge, requirement changes or safety approval. This is a documentation-only review, not a release.
