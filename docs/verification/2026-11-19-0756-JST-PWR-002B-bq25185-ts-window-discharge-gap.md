# 2026-11-19 07:56 JST — PWR-002B / Issue #8: BQ25185 TS temperature window and battery-only monitoring gap

**Role:** Chat A deep-design. **Claim:** provisional, NO FORMAL CLAIM. **Review:** PENDING REVIEW. **Verdict:** CONDITIONAL for the explicitly assumed ideal-NTC threshold arithmetic; BLOCKED for actual protected-cell charging/discharge thermal qualification.

## Task contract and baseline
- Repository `mitsu32m/PROJECT-NIXIDORO`, branch `codex/reva-integrated-prototype-review`; start HEAD **5fcc7fb7d4271444d24a1371cbb6407049bfa7a5**.
- Parent GitHub Issue **#8** (PWR-002A, charger/cell/5V/startup/thermal). Scope: one new bounded subquestion PWR-002B. No formal claim: Issue #1's atomic claim protocol is not established.
- Read `docs/ai-workflow.md`, `docs/verification/handoff.md`, `docs/verification/open-issues.md`, `docs/verification/decisions.md`, `docs/tech-tree.yaml`, `docs/tech-tree.md`, C-REVIEW-005 (03:02), A 04:00, Work INT-002, and #8. B #7 owns exact cell/probe sourcing, C owns independent review, Work owns shared ledgers.
- **Question:** With the baseline direct 10kΩ/B3435 NTC and BQ25185 TS/MR current source, what *nominal* and preliminary electrical-corner charging inhibit temperatures follow from the manufacturer's TS voltage/current ranges, and does this protect battery-only discharge?
- **Exit:** independently reproducible resistance/temperature bounds, manufacturer-vs-assumed classifications, explicit fault/safety gap and next physical evidence. No part adoption, firmware threshold change, hardware change or tests.

## Primary manufacturer evidence
- Texas Instruments **BQ25185 Rev.B SLUSF65B (Aug 2026)**, https://www.ti.com/lit/ds/symlink/bq25185.pdf , electrical characteristics and §TS monitoring: ITSMR **36.5–39.5 µA** (typ 38 µA) when adapter present; VHOT_ENTRY **0.105–0.125 V** (typ 0.115 V); VCOLD_ENTRY **0.9575–1.0575 V** (typ 1.0075 V). These are **SPECIFIED under datasheet test conditions**, not an all-environment battery-temperature guarantee. Datasheet Table 6-2: TS measurement **YES adapter / NO battery-only**. BQ uses TS/MR also for pushbutton/factory functions; do not assume short-to-GND is only a thermal event.
- TI §TS describes 10kΩ at 25°C, B25/85=3435K NTC; direct connection assumed here. **Actual Rev.A TS pin wiring, NTC part suffix and pack attachment not yet requalified**. Series/parallel resistor or leakage changes the model.
- C-REVIEW-005 (2026-11-19 03:02) independently identified the adapter-only TS and the need for a separate battery-only thermal strategy; this report adds an explicit threshold-envelope computation, not a duplicate of that observation.

## Model: nominal and preliminary electrical corners
**ASSUMED:** ideal `R(T)=10000*exp(3435*(1/(T_C+273.15)-1/298.15))` Ω, direct NTC to TS/MR/GND, no parallel/series compensation, no leakage/self-heating/thermal lag. The single B25/85 parameter is not a guaranteed full-temperature R/T curve. **SPECIFIED:** BQ voltage and bias-current limits as above. `Rtrip=Vthreshold/Ibias`; `Ttrip_C=[1/298.15+ln(Rtrip/10000)/3435]^-1-273.15`.

| Entry condition | Typical V / I | Nominal equivalent R | Nominal ideal-beta temperature | Electrical-corner ideal-beta range* |
|---|---:|---:|---:|---:|
| Cold entry (charging inhibit as temperature falls) | 1.0075 V / 38 µA | 26.513 kΩ | **+1.74 °C** | **−0.20 to +3.72 °C** |
| Hot entry (charging inhibit as temperature rises) | 0.115 V / 38 µA | 3.026 kΩ | **+59.51 °C** | **+55.58 to +63.74 °C** |

*Electrical corners: cold low-temperature end uses 1.0575V/36.5µA, high-temperature end 0.9575V/39.5µA. Hot low-temperature end uses 0.125V/36.5µA, high-temperature end 0.105V/39.5µA. These combine independently extreme published electrical limits as a screening envelope, **not** a TI-guaranteed temperature interval. Correlation, actual device conditions, R25/B tolerances, R/T curve, TS/MR wiring, wiring faults, contact lag, board and cell gradients are excluded.

For the same assumed ideal NTC, `R(10°C)=18.410kΩ`, `VTS(10°C,typ)=0.700V` (below typical cold-entry 1.0075V, so charging would still be permitted in the simple model); `R(45°C)=4.847kΩ`, `VTS(45°C,typ)=0.184V` (above typical hot-entry 0.115V, also permitted). These are **counterexamples** to treating a bare 10k/B3435 connection as a 10–45°C charging inhibit. **No cell-specific charge temperature range has been approved**; 10/45°C are illustrative boundaries, not newly imposed requirements.

**Important:** The temperature values are *entry* thresholds only. Cold/hot exit hysteresis is different and must be separately bounded for restart; do not implement a software state machine from the entry numbers alone.

## Independent reproduction (Python 3, no packages)
```python
from math import exp,log
B=3435.; T25=298.15
def R(tc): return 10000*exp(B*(1/(tc+273.15)-1/T25))
def T(v,i_microamp):
    r=v/(i_microamp*1e-6)
    return 1/(1/T25+log(r/10000)/B)-273.15
for name,low,typ,high in [('cold',.9575,1.0075,1.0575),('hot',.105,.115,.125)]:
    corners=sorted([T(v,i) for v in (low,high) for i in (36.5,39.5)])
    print(name,round(T(typ,38),3),round(corners[0],3),round(corners[-1],3))
for tc in (10,45): print(tc,round(R(tc),2),round(R(tc)*38e-6,4))
```

## Safety and design impact
1. **BLOCKED — charging temperature:** A pack whose permitted charging range is narrower than this TS window cannot be protected by the unmodified direct NTC alone. Establish the *selected pack manufacturer's* charge limits and all electrical/thermal corners before deciding whether an independent hardware inhibit or a different charger/NTC network is required. Do not rely on MCU firmware alone without proving MCU-off and reset behavior.
2. **BLOCKED — discharge temperature:** TI Table 6-2 says BQ TS is not measured in battery-only mode. It cannot by itself prove cell-temperature protection for the battery-powered 205V/16mA display. Qualify pack PCM/BMS temperature cutoff (if any) and/or an independent cell-attached sensor plus an enforceable fail-safe HV/load shutdown path; validate that any monitor actually runs in battery-only and during MCU reset.
3. **Faults:** Open NTC, shorted NTC (also TS/MR button), intermittent contact, wiring to chassis, detached sensor, charging while MCU off, hot cell with cold PCB and USB removal all require separate tests. An NTC on the PCB is not a cell temperature sensor.
4. **Thermal coupling:** BQ TS is charging-oriented; BQ junction, BATFET, TPS61023/L1, cell case and PETG enclosure each require their own measured acceptance limits. The BQ reference thetaJA cannot be used as the enclosed-system guarantee.
5. **Dependencies:** B #7 must provide actual protected 21700 PCM temperature and charging specification, exact NTC/probe drawing and R/T tolerances. Chat C independently check Rev.B threshold table/assumptions. Work integrate only reviewed evidence into BAT-001/PWR-002 and decisions.

## Comparison with previous work and disposition
Previous A 04:00 analyzed a hypothetical SYS transient charge deficit; C-REVIEW-005 already highlighted TS adapter-only measurement. **New contribution:** quantitative BQ electrical-corner *entry* window and explicit 10/45°C counterexamples, which identify a charger-cell compatibility decision gate rather than another arbitrary SYS capacitance screen.

**CONDITIONAL:** nominal/electrical-corner ideal-beta math only. **BLOCKED:** real charge inhibit temperature, discharge protection, exact cell/NTC and thermal safety. **PENDING REVIEW:** not a hardware design decision. No purchase, fabrication, HV energization, main merge, autonomous specification changes or tests.
