# HV-002A — independent OVP threshold tolerance and residual switching-pulse budget
Date: 2026-11-17 15:57 JST | Role: Chat A deep-design | Technical ID HV-002A / GitHub Issue #3
Status: **PENDING REVIEW** | Outcome: **CONDITIONAL mathematical window / BLOCKED component approval** | **NO FORMAL CLAIM**
Branch: `codex/reva-integrated-prototype-review`. Starting branch SHA **UNKNOWN**: current GitHub connector returned file content but did not expose authoritative HEAD; latest known earlier commit is not asserted as current HEAD.

## Scope and sources
Question: Can a standalone OVP comparator with ±1% aggregate trip uncertainty fit between existing MAX668 normal-static high corner and HV5524 220V recommended ceiling, allowing finite post-trip energy? Exit: derive explicit numerical admissible thresholds and energy/pulse budget, identify missing guaranteed parameters. This is **not** an OVP schematic or safety approval.
Read fresh: docs/ai-workflow.md; docs/verification/handoff.md; docs/verification/open-issues.md; docs/verification/decisions.md; docs/tech-tree.yaml; docs/tech-tree.md; docs/hv-voltage-window.md; docs/verification/2026-11-17-1155-JST-HV-001A-max668-precedent-ovp-energy.md; docs/verification/2026-11-17-work-integration-001.md; docs/verification/2026-11-17-1403-JST-chatb-sys001-supply-mode-alternatives.md; open GitHub Issues #1–#4. No confirmed working atomic claim; no overlap with Chat B SYS-001 supply-mode research. This adds a **threshold-tolerance feasibility test**, not another repetition of 205→220 capacitor energy arithmetic.

Manufacturer primary references:
- [MAX668/MAX669 Rev3 June 2016](https://www.analog.com/media/en/technical-documentation/data-sheets/MAX668-MAX669.pdf): FB 1.22–1.28V over -40..85°C; 222–278kHz at ROSC 200kΩ±1% under stated conditions. Values are **datasheet min/max**, not system behavior.
- [Microchip HV5524 DS20006850A](https://ww1.microchip.com/downloads/aemDocuments/documents/APID/ProductDocuments/DataSheets/HV5524-32-Channel-Serial-to-Parallel-Converter-Data-Sheet-DS20006850.pdf): 220V **recommended maximum**, 230V **absolute maximum not usable as normal limit**.
- Existing normal static max 214.13495V from `docs/hv-voltage-window.md` assumes nominal 205V, MAX668 FB corner and two independent ±1% resistors. This excludes FB bias, VCR/TCR, load/line, transient.

## A. OVP trip tolerance feasible region — NEW calculation
Let normal maximum = Vn=214.13495V (existing **INCOMPLETE STATIC** bound). Let nominal comparator OVP trip Vt, fractional **aggregate** uncertainty ε (ASSUMED, includes reference, comparator offset, resistor tolerances, drift, bias; not individual 1% resistor tolerance), and maximum post-trip rise ΔV (UNKNOWN). Necessary conditions:
1. `Vt*(1-ε) > Vn` (avoid false trip at normal high corner)
2. `Vt*(1+ε)+ΔV < 220V` (protect recommended HV5524 maximum).
Hence `Vn/(1-ε) < Vt < (220-ΔV)/(1+ε)`.
Nonempty window requires `ΔV < 220 - Vn*(1+ε)/(1-ε)`.

At ε=1% ASSUMED and ΔV=0V (impossible ideal shutdown), Vt must be >216.2979V and <217.8218V; total nominal design window **1.524V**. Maximum tolerable post-trip rise is **1.539V**. At ε=0.5% ASSUMED, ΔV=0, Vt >215.2109V and <218.9055V; maximum ΔV≈**3.713V**. At ε=2% ASSUMED, even ΔV=0, `Vn*(1.02/0.98)=222.876V>220V`: **NO-GO** for this entire assumed static envelope with 2% aggregate trip uncertainty, unless normal-control tolerance/target is changed. All strict inequalities need positive design margin, not equality.

These are **necessary, not sufficient**: actual normal dynamic max >214.135V, trip accuracy may be worse, comparator response and switching-tail are unknown. A nominal threshold in the computed band is **not** a recommendation to implement it.

## B. Relating switching tail to ΔV — NEW sensitivity
For minimum effective HV capacitance Cmin, at trip-high voltage Vh=Vt*(1+ε), available post-trip energy is `Ehead=0.5*Cmin*(220²-Vh²)`. Any continuing energy injected after detection (including delay, magnetic stored energy, output rectifier current and load variation) must be less than Ehead. For a hypothetical residual pulse `Ep=0.5*Lp*Ipk²` (ASSUMED that **all** primary magnetic energy transfers to output, not valid as an exact coupled-inductor model), `N*Ep < Ehead` is a *screen*; leakage/clamp and stored energy distribution change real result. This is not an upper bound unless Lp and Ipk are guaranteed maxima and all other injection mechanisms bounded.

Example: Cmin=1µF ASSUMED, Lp=44µH ASSUMED upper corner of a 40µH±10% part, Ipk=3.2A ASSUMED (manufacturer TYPICAL Isat must NOT be treated as guaranteed limit). Ep=0.22528mJ. At Vh=218V, Ehead=0.438mJ; **two** such pulses (0.451mJ) exceed that budget, before any delay energy. At Vh=217V, Ehead=0.6555mJ; **three** pulses (0.676mJ) exceed it. This is a counterexample scenario, not a predicted converter waveform.

At f=278kHz, 2 periods ≈7.19µs; 3 periods ≈10.79µs. Frequency alone does not guarantee the number of pulses after trip; asynchronous disable, gate-driver propagation, current-limit response, flyback secondary conduction and any latched-off behavior must be proven. An OVP architecture that simply asks firmware to stop is not an independent hard-off.

At 1µF, 220V stored energy is 24.2mJ (ASSUMED capacitor), relevant to controlled discharge and touch safety, but 220V is a *driver operating rating*, not a safe-touch threshold.

## C. Worst-case model and failure cases still needed
- Actual comparator/reference datasheets with **guaranteed** Vtrip,min/max across temperature, divider resistor voltage coefficient, tolerance, bias, layout leakage, noise and aging.
- HV output capacitor selected part: guaranteed capacitance MIN after tolerance, DC bias, temperature and aging; actual HV rail capacitance may be less than nominal.
- Controller and switching network: actual Lp MAX, peak-current bound including current sense 115mV MAX / RCS MIN, switch and driver propagation, number of post-trip pulses, secondary energy and clamp.
- Normal dynamic maximum for abrupt load removal and startup; static MAX668 tolerance is not a bound on those.
- Single-fault shutdown path independent of MCU and HV5524 blanking, including reset/power-loss; latched failure and safe discharge verified separately.
- High-voltage wiring insulation and measurement plan reviewed by supervisor before energization.

## Decision and handoff
**CONDITIONAL** for a mathematical comparator design window at **assumed** ε≤1% and sufficiently small ΔV. **NO-GO** for ε=2% within the *existing assumed normal-static bound*, even with zero overshoot. **BLOCKED** for real OVP part selection or approval: guaranteed normal dynamic voltage, post-trip energy, actual OVP error and independent hard-off are absent. **PENDING REVIEW**. Do not edit shared indexes (integrator-owned), select components, change target, order, fabricate, merge main or energize HV.
Next: HV-002B evaluate exact comparator/reference/divider chain with all guaranteed error terms and finite response, plus hardware-latched shutdown. HV-001A topology remains separate; do not transpose this flyback pulse-energy example into coupled-inductor guarantee.
