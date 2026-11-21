# HV-001 / Issue #2 — ADI/MAXIM primary-source autotransformer benchmark
Date: 2026-11-22 08:01 JST
Role: Chat A deep-design; NO FORMAL CLAIM
Status: PENDING REVIEW (Chat C)
Decision: CONDITIONAL for topology precedent; BLOCKED for NIXIDORO qualification

## Task contract and provenance
Question: Does a manufacturer-origin MAX668 autotransformer circuit offer an actual measured power benchmark beyond community tube-lighting anecdotes, and what stress boundaries follow?
Exit: identify primary-source topology, demonstrated load/power, and distinguish assumptions from guaranteed 205V/16mA qualification.
Branch: codex/reva-integrated-prototype-review. Starting HEAD SHA NOT VERIFIED (connector provided file blob SHAs, not branch commit SHA). Required SOP, handoff, open-issues, decisions, tech-tree.yaml and tech-tree.md read; latest known Chat A 2026-11-22-0400 report and transformer screen checked. Concurrent reports beyond the known dated artifact cannot be certified exhaustively. Issue #2 checked. Claim mechanism not used; provisional scope. No shared-index writes.

## New primary-source finding
Analog Devices/Maxim original technical article dated 2002-07-04:
https://www.analog.com/jp/resources/technical-articles/small-highvoltage-boost-converters-guide.html
Sections '動作理論' and '実験的な比較' / Figures 1c, 9, 11.
It explicitly distinguishes the **non-isolated autotransformer/hybrid boost-flyback** topology from ordinary isolated flyback. The secondary flyback voltage is stacked on input and primary flyback voltage. Therefore earlier isolated-flyback DCM screens are **not a transferable NO-GO** for this circuit.
Manufacturer-origin example: MAX668, Sumida CMD-8LN 6313-T036, Lp=5.6uH, primary peak 2.3A, winding ratio Np:Ns=1:9, Rp=0.5ohm. Reported transformer-based output **150V at 25.5mA = 3.825W**, efficiency **77% at that load**. Peak efficiency **88% at 15mA**. The comparison ordinary-inductor converter delivers 150V at 18mA = 2.7W and peak efficiency 65%. These are **REPORTED EXPERIMENTAL** values for the specified example, NOT guaranteed datasheet operating limits.
This is a materially stronger power precedent than the Zhang 174V tube-lighting report, but the manufacturer example still does not demonstrate 205V/16mA or selected sourceable transformer.

## Independent quantitative screening
REQUIREMENT: 205V * 0.016A = 3.280W continuous.
Manufacturer experiment: 150V * 0.0255A = 3.825W; target power / experimental power = 0.8575. **Lower power demand does not prove higher voltage operation**, because output voltage stress and regulation differ.
ASSUMED same 77% efficiency at 205V: Pin=3.28/0.77=4.260W; at 5V, Iin=0.852A; at 4.75V, Iin=0.897A. Efficiency is not extrapolatable as a guaranteed value.
ASSUMED ideal autotransformer of the same 1:9 turns (total ratio Nt/Np=10), correctly dotted in Figure 1c, negligible leakage and diode drop:
MOSFET OFF-state ideal Vds ~ Vin + (Vout-Vin)/10. At 5V,205V -> 25V; at 5.25V,220V -> 26.725V. This is a **topology-specific approximate steady voltage**, not a MOSFET rating; leakage spikes, ringing and fault states must be added.
Rectifier reverse stress in the presumed series-aiding configuration on MOSFET ON is approximately Vout + 9*Vin (depending on exact dot orientation/diode node), i.e. 205+9*5.25=252.25V. This **must be checked against Figure 9 actual pin-level connections** before part selection. 200V diode from the 150V ordinary boost example cannot simply be transplanted to 205V. Output capacitor 200V is NO-GO at 205V nominal regardless of topology.
A source's 30V MOSFET for 150V output is NOT automatically acceptable at 205V or at 220V OVP; even ideal 26.725V leaves only 3.275V to 30V before ringing, tolerance, startup or fault transients.

## Evidence classes and unresolved conditions
- GUARANTEED: none for 205V/16mA with a sourceable MAX668/transformer pair.
- REPORTED EXPERIMENTAL: 150V 25.5mA 77% and 150V 15mA 88% in ADI/Maxim 2002 article.
- MANUFACTURER EXAMPLE, NOT QUALIFIED PURCHASE PART: Sumida CMD-8LN 6313-T036, Lp=5.6uH, 1:9, Rp=0.5ohm, primary current 2.3A; supply and pinout need fresh confirmation.
- ASSUMED: 77% extrapolation, ideal Vds and diode reverse expressions.
- UNKNOWN: exact current supplier part, pin/dot mapping and coupling/leakage; guaranteed maximum switch current and MAX668 CS limit corners, frequency, core/copper loss vs temperature, gate driver startup, diode trr/VRRM, snubber energy, voltage loop stability, open load, OVP hard-off and capacitor Cmin/Cmax.

## Adversarial checks
At 4.75V input and worst load, losses may rise. A nominal 30V switch is particularly risky when the ideal steady Vds is already ~26.7V at a 220V event. The source's 150V/25.5mA observation does not bound 205V fault overshoot, shutdown tail energy or sealed-PETG thermal behavior. The topology is non-isolated and cannot be described as touch-safe. Need hardware-independent OVP and discharge; firmware/BL are not substitutes.

## Decision and handoff
**CONDITIONAL**: A MAX668 non-isolated autotransformer hybrid has manufacturer-origin experimental evidence of 3.825W at 150V, showing power capability at a different operating point. It corrects any overbroad conclusion that 40uH isolated DCM failures eliminate all MAX668 transformer circuits.
**NO-GO (limited)**: Treating the 150V demonstration as a qualified 205V/16mA design, using 200V HV capacitor, or adopting a 30V MOSFET from ideal Vds alone.
**BLOCKED**: 205V/16mA sustained and protected operation, sourceable transformer, stress/thermal/startup/OVP.
**PENDING REVIEW**: Chat C independent source, topology and equation review; Work only may integrate into shared decisions/tree.
Next: inspect actual Figure 9 image and source manufacturer's winding drawing, create pin-level ON/OFF current-path table, then calculate leakage spikes, MOSFET/diode stress and 4.75V 3.28W thermal envelope. If exact magnetic unavailable, compare a sourceable manufacturer-qualified equivalent, do not assert direct substitution.
No procurement, fabrication, HV energization, main merge or requirement change.
