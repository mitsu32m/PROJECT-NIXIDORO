# Decision register — proposed vs verified

Updated 2026-11-25 JST. This is a summary of prior project design documents, **not an engineering release approval**.

| ID | Subject | Current state | Rationale / evidence | Reopen condition |
|---|---|---|---|---|
| D-001 | Main MCU: Pico 2 | **PROPOSED baseline** | `docs/reva-integrated-net-spec.md` | Unacceptable size, current, pin count or startup behavior |
| D-002 | Separate TPS63031 3V3 supply | **NOT in Rev.A baseline** | Pico 3V3(OUT) may supply OLED + RTC; `docs/ctrl-power-domains.md` | External load/standby/noise tests fail |
| D-003 | MAX668 single boost 5 V → 205 V | **REJECTED** | Required ideal D≈97.56%, device max duty lower; `docs/hv-architecture-decision.md` | Fundamentally different topology |
| D-004 | HV power architecture | **COMPARATIVE CANDIDATES; NONE ADOPTED** | 5V flyback comparison baseline; MAX668 coupled and direct-SYS alternatives retained; [INT-002](2026-11-18-work-integration-002.md), C-001/002 | Qualified actual topology/magnetics, power/thermal/startup/OVP and procurement evidence |
| D-005 | HV max output 16 mA continuous | **TARGET, NOT VERIFIED** | 205V×16mA=3.28W, high loss and current requirements; `docs/pwr-reva-power-thermal-review.md` | Lamp-current measurements or power/heat evidence |
| D-006 | “200–205V” interpretation | **UNDECIDED** | Nominal-target vs guaranteed-window conflict; `docs/hv-voltage-window.md` | User decision + full tolerance/OVP analysis |
| D-007 | Independent HV OVP, fault stop, bleeder | **MANDATORY SAFETY REQUIREMENTS, NOT DESIGNED** | `docs/reva-integrated-prototype-review.md` | Only marked complete after schematic, faults, tolerances and safe bench test |
| D-008 | Charging /CE tied GND | **PROPOSED BASELINE UNDER THERMAL HOLD** | Actual PWR net CE=GND; direct NTC does not enforce P2150K +10..45C, and BQ TS is inactive battery-only; [INT-003](2026-11-19-work-integration-003.md) | #9 reviewed charge/load thermal enforcement architecture; no schematic change yet |
| D-009 | ADC: MOS-switched 100k/47k | **PROPOSED** | Lower cost than TMUX1101 approach; reverse feed needs validation; `docs/pwr-reva-v3-review.md` | Leak/injection or thermal results fail |
| D-010 | USB supply from dedicated 5V ≥500mA charger | **PROPOSED operating constraint** | USB source advertisement/host behavior not automatically handled; `docs/pwr-reva-v3-review.md` | Need broader host compatibility |
| D-011 | HV outputs rely on HV5524 BL=LOW/POL=HIGH for display OFF | **LOGIC-STATE ONLY; NOT SAFETY ISOLATION** | `docs/ctrl-driver-rtc-schematic.md`; HV logic supply must be valid | HV stop/discharge is separately verified |

## Editing rules

A new result may supersede a prior decision, but it must include original ID, old state, new state, date, supporting calculation/tests, link to dated report and a concise explicit reason. Never silently erase rejected alternatives. The user must approve product requirements changes (e.g. reducing maximum neon current or relaxing nominal target); the engineer/supervisor must verify high-voltage bench safety.

## 2026-11-17 — WORK-INT-001 integration supplement

| ID | Previous state | New state | Adoption conditions / evidence | Reopen trigger |
|---|---|---|---|---|
| D-012 | No mode-specific integrated adoption gate | **PROPOSED / PENDING REVIEW:** define HV–PWR–CTRL power contract before final HV selection | [Work integration](2026-11-17-work-integration-001.md); lamp-current evidence, qualified topology, supply/startup/thermal bounds, independent OVP and power-loss/discharge behavior; explicit approval for requirements changes | Chat C reviewed package or new power/current/protection evidence |

D-003 remains limited to ordinary non-coupled boost. D-004 is unproven; D-005 remains the unmodified 16mA target; D-006 remains undecided. Latest Chat A report has no located Chat C review package at examined SHA. No final topology, component rating or firmware threshold is adopted.

## 2026-11-18 — WORK-INT-002 current dispositions

Historical entries above retain their date/scope. B and C artifacts now exist; the earlier “no review package located” is no longer the current availability assessment.

| ID | Previous state | Current disposition | Grounds and conditions |
|---|---|---|---|
| D-004 | 5V flyback proposed/unproven | Comparative candidates; no final architecture | C-001 blocks hardware adoption; direct-SYS B reports remain pending review; actual parts and minimum SYS required |
| D-012 | PROPOSED / PENDING REVIEW | **CONDITIONAL, C-001 reviewed integration priority** | Mode-specific power contract; no target or user behavior changed |
| D-013 | Not recorded | **ADOPTED analysis requirement; implementation BLOCKED** | Joint HV capacitor/OVP/startup/discharge evidence using Cmin vs Cmax; C-002 algebra plus independent primary/timing and energy checks in [INT-002](2026-11-18-work-integration-002.md). No capacitance/OVP threshold approved |
| D-014 | No explicit staged prototype decision | **PROPOSED: low-voltage PWR/CTRL then independent HV then enclosure integration** | #7/#8 prepare BOM and test evidence; user authorizes purchases/tests separately |

D-003 remains rejected only for conventional non-coupled boost. D-005 16mA target unchanged; D-006 nominal vs guaranteed voltage undecided; D-007 protection not implemented. MAX668 70us=TYP is now directly established; maximum shutdown/tail energy remains UNKNOWN. B 05:03 mixed DCM proxy is **CHANGES_REQUESTED as a simultaneous real operating point**, retained as a hypothetical screen. No unreviewed device proposal is formally selected.

## 2026-11-19 — WORK-INT-003 dispositions

[Integration and direct source/netlist checks](2026-11-19-work-integration-003.md) apply C-003/004/005/006 within their stated scopes. Earlier PENDING REVIEW statements are historical where those later packages cover a claim; no hardware node is promoted.

| ID | Previous state | Current disposition | Grounds / adoption conditions |
|---|---|---|---|
| D-008 | /CE=GND proposed automatic charge | **THERMAL COMPATIBILITY HOLD**; actual net unchanged | U1 pin4 grounded; no separate charge-inhibit interface implemented. Existing pair with P2150K/direct NTC is not accepted for charge safety. #9 must define reviewed alternative and requested change scope |
| D-015 | Charge/discharge thermal responsibilities not separately recorded | **REJECTED claim:** protected cell + direct 10k/B3435 alone completes charge AND battery-only thermal protection | C-005/006, TI §6.4 p19 (not Table 6-2), Keeppower page and nominal TE R/T counterexamples. Actual limits, worst-case errors, enforced charge/load cut paths and MCU-off/fault behavior required |
| D-016 | TE 15mm versus 20mm ambiguity; nominal electrical match | **CONDITIONAL SENSOR CANDIDATES, none selected** | C-006 + primary PDF body supports STM010 20±1mm; PDF/web environmental conflict persists. Insulation, fit, attachment/lag and full cost remain unqualified |

D-012 mode contract remains conditional; D-013 joint HV Cmin/Cmax analysis requirement is supported by C-003; D-014 staged prototype remains proposed. C-003 confirms rejection of the mixed B DCM operating point; C-004 accepts limited mode/direct-SYS algebra, not real controller/lamp selection. C-005 static power/OCP examples remain assumptions, not safe load thresholds.

New Work proof for GND-only Rs+(Rp||NTC) cannot expand TE nominal R10/R45 ratio 3.64837 to BQ entry ratio 8.76087: **PENDING INDEPENDENT REVIEW**, a restricted analytical screen only. It does not reject all compensation circuits or adopt a new charger/NTC. No 16mA, HV voltage, USB current or cell temperature requirement changed.


## 2026-11-23 — WORK-INT-004 current dispositions

[WORK-INT-004](2026-11-23-2201-JST-WORK-INT-004-power-discharge-topology-integration.md) applies C-007〜024 within explicit scopes and independently checks manufacturer tables and the topology/load contradiction. No implementation or requirement adoption.

| ID | Previous state | Current disposition | Evidence / adoption conditions / reason |
|---|---|---|---|
| D-004 | Comparative HV candidates | **CONDITIONAL candidates retained; no qualified pair** | MAX668 coupled, LT3757 controller-only, LT8365 multiplier and direct-SYS retained; Q4434/35 1:1 excluded from 205V-qualified pair count. Real controlled magnetics, currents/loss/thermal/OVP and sourcing required |
| D-005 / D-006 | 16mA target / voltage meaning undecided | **UNCHANGED; current boundary also UNDECIDED** | Lamp-only vs whole-bus must be explicit. No reduced display/current/USB policy adopted |
| D-013 | Joint capacitance requirement | **ADOPTED analysis requirement; implementation BLOCKED** | Same real Cmin/Cmax, guaranteed tail, startup and single/common-fault discharge; 60V/5s and 300k are examples, no safety thresholds/parts |
| D-015 | Direct NTC + protected cell insufficient | **REJECTION retained; three distinct protection contracts** | charge inhibit, battery-only load cut, HV residual discharge. TI TS inactive battery-only; CE only charge. MCU3V3-only pullup/float not fail-inhibit |
| D-017 | Separate reports use inconsistent bleeder load | **ADOPTED load-accounting analysis contract** | HV total=lamp+bleeder+OVP/divider+driver/leakage; voltage nodes, eta boundaries, Paux, signed IBAT. Negative remaining budget→INFEASIBLE, never clip to feasible zero. Actual modes BLOCKED |
| D-018 | Passive/switched discharge not compared consistently | **CONDITIONAL alternatives P1/P2/S1/H1; none adopted** | P2 assumed300k×2 min corner adds0.294912W at205V, one-open4.91129s under assumed12µF/220→60V/5s. Shared-return/continued-drive/cap/thermal/ratings unqualified |
| D-019 | No explicit actual-part false-positive gate | **REJECTED as qualified 205V pairs: Q4434/35; LT8365 ordinary boost** | Manufacturer1:1/5V example and SW150V limit. No universal transformer impossibility; multiplier retained. TDK old reference held for sourcing proof |
| D-020 | Work Rs/Rp proof pending | **ACCEPTED mathematical scope, C-007 reviewed** | Fixed-bias positive Rs+(Rp||NTC) contracts nominal ratio; does not exclude all compensation/active/other charger or adopt values |

Adoption conditions: primary min/max only under stated conditions; typical efficiency, threshold, resistance and manufacturer application examples cannot become guaranteed system performance. No real FET/diode/magnetics/cap/NTC/cell chosen. Budget and staged prototype D-014 remain proposals, not authorization. C-024/B21:03 "0 neon" presentation is refined to "digit2 itself infeasible" at the specified450mA dual-bleeder example; older artifacts retained.


## 2026-11-24 — WORK-INT-005 OVP and magnetics

[WORK-INT-005](2026-11-24-1003-JST-WORK-INT-005-ovp-timing-and-magnetics-gates.md) integrates C-025/026 and partially checks pending B09:03. No hardware or specification adoption.

| ID | Previous state | Current disposition | Reason / conditions |
|---|---|---|---|
| D-021 | Actual OVP candidate not indexed | **TLV6700 alternative; stated ±1% divider proxy REJECTED; precision variant BLOCKED** | TI Rev.B p6 footnote/Figure1: INB rising→OUTB falling=tPLH29µs NOM, not18µs; max delay UNKNOWN.450µs startup max under conditions, UVLO high-Z not fail-off. Real bias/chain/normal dynamic/C/tail/stop required |
| D-022 | Magnetics energy and timing split across reports | **ADOPTED analysis requirement: simultaneous reset/current/frequency/control/thermal proof** | CJ5143 3V/100kHz fully-reset constant15µH/n15 model insufficient even ideal;5V nearly boundary and above1.2A characterization. Do not infer universal part/topology rejection or continuous rating |
| D-023 | Würth actual working-voltage/drawing not freshly verified | **SOURCE-DOCUMENTED partial evidence; hardware BLOCKED** | Controlled003.001 p1 pins/dots confirmed;p2 functional insulation265Vrms/400Vpeak OVCII wording. Not system/basic/reinforced qualification. Isat3.2A TYP;50–200kHz typical application, not universal absolute range |
| D-017 | B21:03 pending C | **Arithmetic reviewed C-025; bookkeeping retained** | Negative residual remains INFEASIBLE; no duplicate new mode decision. B11/24 09:03 still pending C |

C-025/026 delay wording is corrected with primary-source evidence; originals retained.73.107µJ uses assumed1µF and normalized midpoint, not a capacitor/threshold selection. Fixed5.415M/10k plus400mV nominal is217.000V, not217.058766V. All previous release locks,200–205V/16mA target and budget constraints unchanged.


## 2026-11-25 — WORK-INT-007 current dispositions

[WORK-INT-007](2026-11-25-0956-JST-WORK-INT-007-cutoff-energy-and-current-gates.md): C-027 integrated; A04:01 remains PENDING C REVIEW after limited Work source/math check.

| ID | Previous state | Current disposition | Evidence / adoption conditions / reason |
|---|---|---|---|
| D-021/D-023 | Work correction/partial Wurth evidence awaiting C | **C-027 scoped review accepted; hardware BLOCKED** |29us input-rise/output-fall correction and controlled Wurth scope confirmed; typical timing/current and functional insulation do not qualify real stage |
| D-024 | Upstream stop energy contract did not explicitly inventory LV caps | **ADOPTED analysis requirement; implementation BLOCKED** | After upstream opening, downstream LV Ceff/max, magnetic energy, timing supply and alternate feeds remain; source-to-HV transfer unknown.10/22/47uF examples are assumptions, not C selections or actual Etail |
| D-025 | LT8365 low-SYS proxy pending review | **C-027 reviewed necessary-condition arithmetic only** |1.5A steady boost guide is distinct from1.5/2/2.7A table and actual charge-pump peak.3V lamp-only+bleeder proxy fails; actual topology/efficiency/current/temp/startup required |
| D-026 | No upstream switch candidate indexed | **TPS22918 CONDITIONAL research alternative, not adopted** | tOFF2us=TYP, no max; QOD weakens on VIN loss, not HV discharge.79mohmmax test at−200mA not1A. Actual latch/fault/reversefeed/full-load thermal needed |

11/25 evidence checkpoint remains unfulfilled at09:56 snapshot, not a claim about the entire day. Full-HV release and initial40k/reserve10k/total50k remain unproven. No specification/current/capacitance or schematic change.



## 2026-11-25 evening — WORK-INT-008 lamp revision/lifecycle gates

[WORK-INT-008](2026-11-25-2159-JST-WORK-INT-008-neon-revision-and-lifecycle-gate.md): new B21:02 and Work primary checks PENDING C REVIEW. Original sources/reports retained; no hardware adoption.

| ID | Previous state | Current disposition | Evidence / reason / adoption conditions |
|---|---|---|---|
| D-027 | A1A nominal0.5mA/95VDC versus listing90VDC; revision unknown | **ADOPTED evidence requirement; lamp selection HOLD** | S1 actually03/17 Rev2; S2 manufacturer-hosted undated table design0.6mA/maxbreakdown90VDC. Establish applicable lot/revision/DC behavior/life. Distributor generic voltage not established as same electrical quantity; no0.5/0.6mA guaranteed load adopted |
| D-028 | NRND/cached sourcing only | **A1A-T OBS documented; bareA1A lifecycle UNKNOWN / sourcing HOLD** | Manufacturer PCN333 p1/p25 issued/effective2014-01-21 lists A1A-T; no transfer to bareA1A. Require exact suffix state, sourceable alternative and dated landed quote before BOM selection |

D-004 candidates/D-00516mA target/D-006 voltage interpretation and all stop/thermal/energy holds unchanged. New independent C review required for Work008; no claim C-027 reviewed newB. Budget40k+10k/50k remains unproven.



## 2026-11-27 — WORK-INT-012 C-028 and RS source difference

[WORK-INT-012](2026-11-27-2202-JST-WORK-INT-012-cutoff-review-and-rs-source-conflict.md) preserves old reports. No hardware/specification adoption.

| ID | Previous state | Current disposition | Evidence / conditions |
|---|---|---|---|
| D-024/D-026 | A04:01/Work007 pending C | **C-028 scoped review complete; TPS22918 alternative only** | Source/arithmetic and inventory accepted; transfer conditional. Real circuit/timing/default-off/reversefeed/thermal/discharge blocked.2us TYP notmax,79mohm at−200mA not1A guarantee |
| D-029 | Nominal/constant-C energy screen | **ADOPTED analysis requirement; hardware BLOCKED** | Voltage-dependent capacitance needs Cdiff energy integral or conservative bounds; align nodes/trip/cut time, no pre-trip/storage double counting, strict margin. C-028 supports requirement, Work refinements pending independent C; no actual cap selection |
| D-030 | New B655-9413 listing250uA; DC striking unknown | **SOURCE CONFLICT / DC AND PROCUREMENT HOLD; no part adoption** | Linked RS PDF p1 gives maxcurrent0.15mA/DC strikingmax95V; listing250uA, applicable revision/lot unknown. B evidence completeness correction pending C. Price/stock retrieval not landedquote. Need actual DC operating/life/current/lot and source revision |

D-027/028 A1A source/PCN batch still pending C. Existing HV candidates/rejected branches,200–205V/16mA target and all charge/BAT-only/thermal/UI/insulation gates retained. Budget remains unproven.
