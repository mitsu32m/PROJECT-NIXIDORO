# HV-002 / Issue #6 — TLV6700 input-current and startup primary-source gate
Date: 2026-11-24 08:01 JST. Chat A deep-design. Branch: `codex/reva-integrated-prototype-review`.
**PENDING REVIEW / NO FORMAL CLAIM / NOT ORDER-READY.**

## Task contract
Question: Does the previous ±0.1%-divider static OVP window survive the manufacturer's input-current and startup specifications? Exit: quantify the bias sensitivity and identify exactly what is guaranteed versus not. No part adoption, schematic changes, purchases or HV operation.

Repository basis: SOP, handoff, open-issues, decisions, tech-tree, Issue #6, 2026-11-24-0400-JST-HV-002-precision-divider-static-margin-energy-screen.md, WORK-INT-004. Existing report's nominal Rtop=5.415 Mohm, Rbottom=10 kohm, 217.05877 V threshold and 0.32467/0.33256 V margins are **ASSUMED** illustrative numbers, not approved specifications.

## Primary manufacturer evidence
TI TLV6700 datasheet **SNVSAV2B, November 2019**, https://www.ti.com/lit/ds/symlink/tlv6700.pdf :
- §7.5 p5: INB− input current **−15 to +15 nA** at **VDD=1.8 and 18 V, VI=0.1 V**; INA+ −25 to +25 nA at **VI=6.5 V**. These are specified at their stated test conditions, **NOT guaranteed at the ~0.4 V proposed OVP sense node**. INB− is the relevant positive-going overvoltage channel (p1, pin functions p3).
- §7.5 p5: positive-going threshold VIT+ **396–404 mV** over −40..125°C and stated supply conditions; hysteresis is a distinct parameter. The prior ±1% comparator threshold proxy roughly matches this but does not include external sense-current effects.
- §7.5 p5 notes: startup delay **450 µs max after VDD exceeds 1.8 V**, and below V(POR) output state is undetermined; falling VDD below UVLO drives OUTA low and **OUTB high impedance** (not an asserted hardware-off).
- §7.6 p6: propagation delays 18/29 µs are **timing requirements at VDD=5 V, 10 mV input overdrive and specified output pull-up**, not a universal bound at arbitrary overdrive, supply or ramp.

## Independent circuit sensitivity
For an ideal resistor divider with input current I_B flowing **into** the sense pin:
V_HV,trip = V_REF*(1+Rtop/Rbottom) + I_B*Rtop.
Thevenin resistance at the sense node = Rtop || Rbottom ≈ 9.982 kohm. Consequently 1 nA changes sense voltage ~9.982 µV, corresponding to **5.415 mV** at HV; 15 nA corresponds to **81.225 mV** (NOT 81 V). Important unit check: 15e-9*5.415e6 = 0.081225 V. A previous intuitive 81V interpretation would be a 1000× unit error and is rejected here.

At 217 V nominal, divider current ≈ 217/(5.425 Mohm)=40.0 µA and dissipation ≈8.68 mW (ASSUMED ideal resistors). ±15 nA is ~0.0375% of divider current and causes ±0.081225 V of HV trip uncertainty *if* that current bound held at 0.4 V. This consumes about 25% of the 0.325 V historical low-side margin, before resistor TC, drift, contamination, normal ripple or tail energy.

The current bound **does not transfer as GUARANTEED** from VI=0.1 V to the proposed VI≈0.4 V. It is a conditional sensitivity scenario only. Manufacturer clarification/bench characterization is needed before claiming a complete worst-case trip bound.

## Fault and supply-state contract
| State | Manufacturer-supported observation | Required design consequence |
|---|---|---|
| VDD nominal and sense over threshold | INB−/OUTB positive-going trip behavior; threshold min/max specified | Must still prove stop-gate and downstream switch disable |
| VDD ramp crossing 1.8 V | up to 450 µs startup to correct output | HV must remain independently inhibited during comparator initialization |
| VDD falls below UVLO | OUTB high impedance; below POR undetermined | OUTB alone cannot be interpreted as a fail-safe hard-off signal |
| HV persists with comparator supply absent | no active comparator guarantee | independent default-off HV drive and residual discharge path required |
| divider top open / bottom short / return open | sense may read falsely low or undefined | common fault/return analysis; no single-divider-only safety claim |

## Decision and next action
**CONDITIONAL:** correct circuit sensitivity is ±81.225 mV for a hypothetical ±15 nA at the OVP input; this is significant relative to the previous ~0.33 V margins, but is not itself a proven failure.
**NO-GO (limited):** using the TLV6700 INB− ±15 nA at VI=0.1 V as a guaranteed input-current bound at VI≈0.4 V; or assuming OUTB high-impedance under UVLO is automatically safe.
**BLOCKED:** guaranteed bias at actual sense conditions, real resistor chain MPN/TC/aging/working voltage, supply-rail sequencing and default-off stop, actual Cmin and bounded tail energy, dynamic normal voltage and independent discharge.
**PENDING REVIEW:** Chat C must verify TI table interpretation and the 5.415 mV/nA sensitivity before Work integration. Do not adopt parts or threshold.
Next: ask manufacturer for full input current over ~0.4V, VDD and temperature, or compare a reference/comparator whose bias is guaranteed at the actual node; then design the fail-off gate with explicit UVLO/startup timing and common-return fault table.
No hardware action, purchasing, manufacturing, HV energization, main merge or requirement changes.
