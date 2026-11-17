# HV-001A — ideal tapped-inductor boost topology discriminant (NOT a circuit identification)

Date: 2026-11-17 23:59 JST. Role: Chat A deep-design. Issue: [#2](https://github.com/mitsu32m/PROJECT-NIXIDORO/issues/2), parent HV-001. Branch: `codex/reva-integrated-prototype-review`. **NO FORMAL CLAIM**; atomic claim protocol not verified. **PENDING REVIEW**. Scoped conclusion: **CONDITIONAL mathematical screening / BLOCKED actual topology and part selection**.

## Contract and startup
Question: How does an ideal tapped-inductor boost (one possible coupled-inductor topology) differ from the already calculated ordinary flyback in duty and ideal MOSFET stress, and what winding ratios are even compatible with MAX668's duty limit? Exit: explicit derivation, numeric low-input screen, exact exclusions, no transposition to unverified builder circuit. No hardware changes or HV energization.

Re-read `docs/ai-workflow.md`, `docs/verification/handoff.md`, `docs/verification/open-issues.md`, `docs/verification/decisions.md`, `docs/tech-tree.yaml`, `docs/tech-tree.md`, `docs/hv-architecture-decision.md`, `docs/pwr-reva-power-thermal-review.md`, 09:30 precedent, 11:55 precedent, 15:57 and 20:03 OVP reports, and open GitHub Issues #1–#6. The working-branch HEAD SHA is **UNKNOWN** because this connector's branch search supplies branch name but no commit SHA; do not confuse blob SHA or earlier report commit with HEAD. This is an independent uniquely named report, not a shared-index edit. No Chat C acceptance was identified in the checked canonical handoff; a newly added report elsewhere in the directory cannot be ruled out by the connector's file-only discovery capability.

## Evidence provenance
- ADI [MAX668/MAX669 Rev3 (June 2016)](https://www.analog.com/media/en/technical-documentation/data-sheets/MAX668-MAX669.pdf): 87/90/93% minimum/typical/maximum maximum-duty table under its stated conditions; 222–278kHz full-temperature oscillator for ROSC=200kΩ±1%. **MANUFACTURER SPEC** for the IC, not a coupled power-stage guarantee.
- [Zhang 2023-04-24](https://zhangshuqiao.org/2023-04/%E5%9F%BA%E4%BA%8EMAX668%E7%9A%84%E8%BE%89%E5%85%89%E7%AE%A1%E5%8D%87%E5%8E%8B%E6%96%B9%E6%A1%88/) calls the approach coupled-inductor boost; [ehbtj 2022-06-25](https://ehbtj.com/electronics/redesign-of-boost-converter-for-nixie-tube/) calls theirs non-isolated flyback. **COMMUNITY DESCRIPTIONS**, actual original netlists/dot polarity still not inspected. Neither is assumed to match the ideal circuit below.
- Voltage target 205V, Iout 16mA: **PROJECT TARGET**. Vin=5V nominal, Vin=4.75V illustrative minimum: **ASSUMED**, not a guaranteed TPS61023 output minimum. n=Nsecondary/Nprimary: **ASSUMED IDEAL** and positive.

## Conditional derivation: a specific ideal tapped-inductor boost
**Only if** the circuit has these exact connections: primary between Vin and MOSFET drain, secondary series-aiding from the primary/switching node to the output rectifier, with the diode reverse-biased while the MOSFET is ON; perfect coupling, continuous magnetizing current, ideal switch/diode and negligible winding resistance.

During ON: Vprimary=Vin. During OFF: volt-second balance gives |Vprimary,off|=Vin*D/(1-D). The output diode sees Vin+(1+n)*|Vprimary,off|, hence:

`M=Vout/Vin=(1+n*D)/(1-D)` and `D=(M-1)/(M+n)`.

MOSFET ideal OFF stress is `VDS,off=Vin+|Vprimary,off|=Vin/(1-D)=(Vout+n*Vin)/(1+n)`. This is **not** the ordinary flyback relation `VDS≈Vin+Vout/n`, and it excludes leakage, clamp and parasitic ringing. Rectifier VRRM cannot be assigned from this generic model without confirming winding/diode reference nodes and polarity; no component voltage rating is approved.

| n assumed | Ideal D @5.00V | Ideal D @4.75V | Ideal VDS @5V | Ideal VDS @4.75V |
|---:|---:|---:|---:|---:|
| 4 | 88.889% | 89.397% | 45.00V | 44.80V |
| 5 | 86.957% | 87.541% | 38.33V | 38.13V |
| 6 | 85.106% | 85.760% | 33.57V | 33.36V |
| 10 | 78.431% | 79.307% | 23.18V | 22.95V |
| 15 | 71.429% | 72.489% | 17.50V | 17.27V |

At the **assumed** 4.75V minimum, n=5 exceeds the 87% minimum specified MAX668 maximum-duty value before any nonidealities. n=6 is below 87% by only ~1.24 percentage points; nonideal losses/rectifier drops can erase it. This is a **necessary ideal duty screen**, not a sufficient feasibility criterion. The 87% table figure must not be interpreted as guaranteed at every oscillator choice without verifying test conditions.

A general necessary condition `D<=Dmax` gives `n >= (M-1)/Dmax - M`. For M=205/4.75=43.1579 and Dmax=0.87, n >=5.299 (ideal). Thus integer n>=6 is needed in this model for the **assumed** Vin corner; a real engineering margin is required beyond that.

## Independent power and stress constraints
205V*16mA=3.28W. At assumed efficiency 70%, input power 4.686W; if 4.75V is the *HV converter input* rather than the upstream 5V rail, average input current =0.986A. At 5V and same assumed efficiency it is 0.937A. This input-current bound is **topology independent** and says nothing about switch peak, saturation, core loss or thermal. Actual tapped-inductor winding RMS and current sense peak require the true netlist, Lmag, coupling, operating mode and switch current waveform. An ideal VDS of 23V for n=10 does **not** qualify a 30V MOSFET: leakage spike, clamp tolerance, switch rise time and layout must be bounded; a rating cannot be selected from this table.

A tapped-inductor boost also retains a conductive input-to-output path through windings and rectifier in some states, unlike an isolated flyback. **Do not infer galvanic isolation or output discharge when switching is disabled**. Exact path and off-state voltage require netlist inspection. Firmware blanking of HV5524 is not a hardware safety disconnect.

## Critical counterchecks
- A manufacturer datasheet that supports MAX668 flyback does **not** prove the ideal tapped-inductor configuration is the topology used in either builder example.
- A community-reported 170–200V output does not establish 205V/16mA continuous, thermal stability, ripple, line/load regulation, startup or OVP.
- At D near the MAX668 duty limit, losses may require a larger duty; n=6 is a weak nominal candidate even before verifying actual magnetic ratio.
- Increasing n reduces ideal MOS stress in this conditional model but may increase leakage, secondary copper resistance, winding capacitance, diode reverse voltage and transformer difficulty; no monotonic optimum can be inferred.
- 220V HV5524 recommended maximum, independent OVP, post-trip energy and discharge are separate safety gates. The narrow 216–218V assumed trip region from previous reports is not an adopted setpoint.

## Result and handoff
**CONDITIONAL**: ideal tapped-inductor boost can meet ideal conversion ratio below the MAX668's 87% lower maximum-duty specification for illustrative n>=6 at Vin=4.75V. **BLOCKED**: this does not establish that the actual Zhang/ehbtj circuits are tapped-inductor boost, or qualify any MOSFET, diode, magnetic component, startup, thermal or 205V/16mA continuous operation. **PENDING REVIEW**; request Chat C to verify the topology equations and source classification before Work adoption.

Next for Issue #2: obtain source schematic/netlist and transformer dot/pin map, derive ON/OFF switch and diode stresses using *that* circuit, then model DCM/CCM boundary and saturation with a manufacturer-qualified magnetic. No duplicate issue created because #2 already captures this task. Do not update shared index files (integrator-owned). No purchasing, fabrication, HV energization, main merge or unilateral specification change.
