# HV-001 / Issue #2 — leakage-inductance energy and clamp thermal budget
Date: 2026-11-22 20:01 JST
Role: Chat A / deep-design
Review state: **PENDING REVIEW**; **NO FORMAL CLAIM**
Disposition: **CONDITIONAL** sensitivity model; physical implementation **BLOCKED**

## Task contract and provenance
Question: How much loss can even small primary-referred leakage inductance cause at the switching frequency and current reported for the MAX668 autotransformer precedent, and what information is required before a 40 V MOSFET / 400 V diode static-rating pair can be considered?
Scope excludes adopting a snubber, winding or switch, or assuming every leakage joule dissipates in the MOSFET.
Exit: reproducible leakage energy/power relationship, sensitivity grid, worst-case data requirements and explicit thermal/surge qualifications.

Working branch: codex/reva-integrated-prototype-review. **Starting HEAD SHA UNKNOWN**: the available connector provided file blob SHAs and commit search did not resolve the exact branch head. Formal atomic Claim mechanism not confirmed; provisional work only. Required SOP, handoff, open-issues, decisions, YAML tree, Markdown tree, GitHub Issue #2 and preceding 16:03 HV-001 report were read. Latest report directory / concurrent B/C coverage **NOT EXHAUSTIVELY VERIFIED**; avoid shared index edits. This is a distinct loss mechanism rather than repeating the prior static voltage/ratio screen.

## Inputs and evidence classification
- Manufacturer precedent (ADI, 2002-07-04): MAX668 autotransformer example 150 V x 25.5 mA, reported efficiency 77%, 1:9 winding example, 5.6 uH primary and 2.3 A peak reported in prior evidence. Primary source: https://www.analog.com/en/resources/technical-articles/small-highvoltage-boost-converters-guide.html . The 2.3 A value is a **precedent reported value**, NOT guaranteed for the proposed 205 V stage.
- Switching frequency f = 250 kHz: **ASSUMED** design scenario, not guaranteed exact operating frequency.
- Primary-referred leakage Llk = 0.1, 0.25, 0.5, 1.0 uH: **ASSUMED sensitivity values**, NOT measurements or vendor limits.
- Peak leakage current = 2.3 A: **ASSUMED transfer** of the reported precedent peak, not the NIXIDORO current bound.
- Clamp dissipated fraction beta = 0..1: **UNKNOWN**, topology and clamp dependent. No universal equality between leakage energy and FET heat.

## Independent calculation
For a first-order hard turn-off event, leakage energy per cycle is E_lk = 0.5 * Llk * Ipk^2.
If one such event occurs per cycle, energy-processing rate is P_lk = E_lk * f.
At 2.3 A and 250 kHz: **P_lk = 0.66125 W per 1 uH of primary-referred leakage**.

| Assumed Llk (uH) | E_lk (uJ/cycle) | P_lk (W at 250kHz) |
|---:|---:|---:|
| 0.10 | 0.2645 | 0.0661 |
| 0.25 | 0.6613 | 0.1653 |
| 0.50 | 1.3225 | 0.3306 |
| 1.00 | 2.6450 | 0.6613 |

At 3.2 A instead (ASSUMED alternate current corner), P_lk = 1.28 W/uH, or 0.64 W for 0.5 uH. Scaling: P_lk proportional to Llk, f and Ipk squared; 20% higher peak current causes 44% higher leakage energy, other conditions fixed.

For a hypothetical allowable leakage-related heat budget Pbudget = 0.25 W (ASSUMED, NOT a thermal rating), with beta=1, f=250kHz, Ipk=2.3A, required Llk <= 0.378 uH. If beta<1, dissipation location changes; any recovered energy still needs its real path and losses accounted for. This bound does not guarantee safe clamping, because transient VDS, clamp voltage, avalanche and resistor/pulse ratings must also pass.

## Important interpretation
The leakage-energy model is an *energy-processing upper-envelope heuristic* under a defined current waveform and turn-off event. It is NOT a prediction of total converter loss, an absolute bound on real peak ringing voltage, or a substitute for magnetics measurements. Energy can be recovered, distributed among snubber/FET/diode/parasitics, or dissipated over multiple intervals. A nonideal clamp can also create extra circulating loss. The earlier 40 V MOSFET / 400 V diode static voltage screen does not establish transient reliability. For MOSFET 40 V with ideal off voltage 26.725 V at the earlier assumed 220 V / 5.25 V / n=9 corner, the remaining 13.275 V to the absolute rating is **not** an acceptable assumed ringing allowance; it needs measured/simulated worst-case including temperature and tolerances.

## Next actionable manufacturer/bench evidence gates (no bench authorization)
1. Verify the original series-aiding winding dots, pin mapping, exact primary-referred Llk test definition and datasheet guaranteed limits (if unavailable, UNKNOWN). Do not transplant isolated flyback equations.
2. Obtain an actual switch MPN: VDS absolute maximum, avalanche SOA/EAS and repetitive avalanche restrictions, Qg, RDS(on) vs temperature, Coss/Eoss and package thermal impedance.
3. Obtain actual diode MPN: VRRM, reverse recovery/capacitance, thermal limits and worst-case output-current waveform; confirm diode polarity in original circuit.
4. Derive current and switching-frequency maximum for 205V/16mA at lowest input, startup and short/open-load faults; use those maxima rather than 2.3 A/250kHz precedent.
5. Select candidate clamp topology only for analysis, quantify snubber voltage/energy and pulse/average thermal at fault corners; independently check HV OVP and safe discharge. A PCB/layout and supervised test plan require human review before HV energization.

## Outcome
**CONDITIONAL:** exact energy and frequency scaling for assumed Llk/Ipk/f; potentially material loss even below 1uH.
**NO-GO (limited):** treating the prior static 40V/400V rating screen as sufficient for component adoption.
**BLOCKED:** actual winding/part data, guaranteed Llk and Ipk, measured or modelled transient voltage, loss allocation, thermal path, startup, independent OVP and discharge.
**PENDING REVIEW:** Chat C should challenge leakage-energy allocation, reference current provenance, and distinguish worst-case current from precedent. Work integrates only reviewed findings.

No purchase, manufacturing, HV energization, main merge, schematic change or requirements change.