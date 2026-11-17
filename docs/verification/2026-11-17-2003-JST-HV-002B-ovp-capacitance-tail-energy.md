# HV-002B — OVP nominal threshold vs effective capacitance and residual energy

- Timestamp: 2026-11-17 20:03 JST
- Role: Chat A / deep-design; GitHub Issue #5; parent HV-002/HV-003
- Status: **PENDING REVIEW**; **CONDITIONAL** mathematical feasibility / **BLOCKED** hardware release
- Claim: **NONE**; atomic Claim mechanism not verified. Work is provisional.
- Working branch: `codex/reva-integrated-prototype-review`; starting HEAD SHA **UNKNOWN** (connector file reads expose blob SHA, not branch commit HEAD). Do not infer a commit HEAD from a file blob.

## Startup and overlap
Re-read `docs/ai-workflow.md`, `docs/verification/handoff.md`, `docs/verification/open-issues.md`, `docs/verification/decisions.md`, `docs/tech-tree.yaml`, GitHub Issues #1–#5 and prior `2026-11-17-1557-JST-HV-002A-ovp-tolerance-pulse-budget.md`. Work owns shared indexes; this run does **not** edit them. This report extends the prior window calculation by deriving a **capacitance-versus-tail-energy design boundary** and showing why choosing the upper nominal trip threshold is fragile. No new manufacturer guarantee is asserted.

## Inputs, provenance and limits
- Normal static maximum Vn=214.13495 V: **ASSUMED / incomplete static bound**, taken from `docs/hv-voltage-window.md` as summarized in HV-002A; excludes dynamic peaks, feedback bias and some drift.
- HV5524 recommended maximum Vlim=220 V: **MANUFACTURER RECOMMENDED OPERATING LIMIT**, Microchip HV5524 DS20006850A, https://ww1.microchip.com/downloads/aemDocuments/documents/APID/ProductDocuments/DataSheets/HV5524-32-Channel-Serial-to-Parallel-Converter-Data-Sheet-DS20006850.pdf . Not a touch-safe voltage; 230V absolute maximum is not a design target.
- Aggregate OVP threshold uncertainty epsilon=±1%: **ASSUMED**, not qualified by a selected comparator, reference or resistors.
- Residual pulse illustration L=44µH, I=3.2A, E=0.5 L I²=0.22528mJ: **ASSUMED COUNTEREXAMPLE**. 3.2A from a transformer typical saturation rating is NOT a guaranteed controller peak-current bound; transfer fraction, polarity and leakage are UNKNOWN.
- Output effective C=1µF: **ASSUMED**; selected part, voltage rating, derating, temperature, ageing and actual effective Cmin UNKNOWN.
- MAX668 MAX669 Rev3 June 2016 https://www.analog.com/media/en/technical-documentation/data-sheets/MAX668-MAX669.pdf : controller is not an independent overvoltage stop and its dynamic behavior is not proven by these calculations.

## Derivation
For a nominal trip Vt, true trip interval [Vt(1-epsilon), Vt(1+epsilon)]. Avoid nuisance trip in normal high static corner:

`Vt > Vn/(1-epsilon) = 216.297929...V`.

Maximum possible true trip `Vh=Vt(1+epsilon)`. For an output capacitor with guaranteed **effective** minimum Cmin and maximum net energy E_tail delivered **after** trip (including continuing switching, secondary stored energy, leakage-dependent transfer, delays, and load removal), the necessary conservative energy inequality is:

`E_tail < 0.5*Cmin*(Vlim²-Vh²)` with Vh<Vlim.

Therefore `Cmin > 2*E_tail/(Vlim²-Vh²)`, or equivalently `Vt < sqrt(Vlim²-2*E_tail/Cmin)/(1+epsilon)`. This assumes a lumped capacitor model and zero helpful dissipation, so it is a conservative capacitor-energy screen **only if E_tail is a proven upper bound**; no such bound exists yet. No claim of guaranteed safe Vpeak.

## Sensitivity at epsilon=1% and hypothetical 0.22528mJ per residual pulse

| Nominal Vt | True high trip Vh | Headroom E for Cmin=1µF | Cmin needed for 1 pulse | Cmin needed for 2 pulses |
|---|---:|---:|---:|---:|
| 216.3V | 218.463V | 0.33696mJ | >0.669µF | >1.337µF |
| 217.0V | 219.170V | 0.18226mJ | >1.236µF | >2.472µF |
| 217.8V | 219.978V | 0.00484mJ | >46.55µF | >93.10µF |

Strict inequalities and real engineering margin required. A nominal 217.8V OVP setting leaves only **22mV** from its worst-case high trip to the 220V recommended maximum under assumed ±1% error, before any energy tail. The earlier mathematical static window 216.298–217.822V is **not** a practically usable window without transient evidence.

The threshold 216.3V is itself only ~0.0021V above the assumed no-false-trip bound, so it has essentially zero margin to model error, normal dynamic overshoot or noise. Thus the lower end of the band also cannot be adopted.

At Vt=217V, the hypothetical 1µF headroom 0.182mJ is **less than one** hypothetical 0.225mJ residual pulse. This is not a predicted real switching pulse; it is a demonstration that threshold, tail energy and Cmin must be co-designed.

## Adversarial cases
- Normal transient above 214.13495V may erase all false-trip margin; load dump and startup must be bounded separately.
- Open load maximizes retained charge; counting on lamp load to absorb energy is invalid for a fault guarantee.
- OVP comparator and reference must work independently of MCU reset, display blanking and the rail being protected. A MOSFET stuck ON or an open feedback divider may defeat single-channel protection; define a safe independent cut path and fault response.
- Effective HV capacitance may fall below nominal; increasing C improves per-pulse voltage headroom but increases stored touch hazard and discharge time/energy, requiring bleeder and controlled discharge sizing.
- HV5524 220V is a recommended limit, not an acceptable transient overshoot limit. Capacitor, diode and driver ratings require separate selection.

## Decision
**CONDITIONAL** only as an algebraic design screen; **BLOCKED** for actual OVP architecture or threshold selection, **PENDING REVIEW**. This does not prove any 205V/16mA hardware design.

## New bounded task proposal HV-002C
Obtain real selected capacitor Cmin across bias/temp/aging, comparator/reference guaranteed trip and delay, switch turnoff path and MAX668 current limit with tolerances. Bound E_tail for at least startup, full-load removal, open load, MCU reset, comparator loss of supply, and single fault. Solve joint feasibility with `Vnormal,dynamic,max < Vtrip,min` and `E_tail,max < 0.5*Cmin*(220²-Vtrip,max²)` with explicit nonzero margin. If impossible, propose architecture change for human decision rather than silently changing HV target. Request Chat C independent review and Work integration.

No changes to schematic, BOM, main or shared registers. No procurement, manufacturing or HV energization.
