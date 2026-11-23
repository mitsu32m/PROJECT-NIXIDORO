# Chat B — HV-001 / SYS-001: CJ5143 DCM reset-time feasibility bound
Date: 2026-11-24 05:02 JST
Role: Chat B wide research; NO FORMAL CLAIM; PENDING REVIEW for Chat C
Starting branch HEAD: UNKNOWN — connector exposes branch file content and branch name, but not verified branch commit SHA. Do not substitute blob SHA or previous report commit.
Issues: #7 PROTO-001; #4 SYS-001A; #2 HV-001A
Scope: independent ideal DCM timing bound for prior CJ5143 candidate. No hardware adoption or schematic edit.

## Sources and traceability
- Coilcraft CJ5143-ALC manufacturer product: https://www.coilcraft.com/en-us/products/transformers/power-transformers/capacitor-charging/cj5143/ (prior Chat B report 2026-11-24-0100, PENDING REVIEW). Lp=15 uH ±10% at 25C, winding ratio Ns/Np=15, L at 1.2A >=13.5 uH, primary DCR <=1ohm, secondary DCR <=25ohm, leakage <=0.3uH. These are CONDITIONAL manufacturer data; no continuous power/Isat guarantee.
- Prior work: docs/verification/2026-11-24-0100-JST-chatb-hv001-coilcraft-cj5143-current-energy-screen.md
- Integration: docs/verification/handoff.md and docs/verification/2026-11-23-2201-JST-WORK-INT-004-power-discharge-topology-integration.md
- BQ25185 manufacturer data and mode assumptions from prior SYS-001 reports; no new current-limit guarantee inferred.

## New calculation: timing is a separate constraint from energy/cycle
ASSUMED ideal fully demagnetized DCM flyback, Vin at primary, Vout=205V, n=Ns/Np=15, constant Lp=15uH, no switch/rectifier drop, no dead time, and one pulse/cycle:
- ton = Lp*Ipk/Vin
- toff = Lp*Ipk*n/Vout
- DCM requires ton+toff <= 1/fs
- Ipk,max,ideal = (1/fs)/(Lp*(1/Vin+n/Vout))
- Pmag,max,ideal = 0.5*Lp*Ipk,max^2*fs
These are upper bounds within this simplified single-pulse model, NOT actual converter guaranteed capabilities; any loss, dead time, saturation or timing limitation reduces feasibility.

At fs=100kHz:
Vin=5V: Ipk,max=2.440A; Pmag,max=4.465W; ton=7.320us; toff=2.678us.
Vin=3V: Ipk,max=1.640A; Pmag,max=2.017W; ton=8.197us; toff=1.800us.
At fs=200kHz:
Vin=5V: Ipk,max=1.220A; Pmag,max=2.232W.
Vin=3V: Ipk,max=0.820A; Pmag,max=1.008W.
For 205V*16mA=3.28W, assumed eta=75% requires Pmag=4.373W. Therefore at 100kHz, 5V has only ~0.092W ideal margin (before losses), while 3V is impossible under the stated ideal DCM model. At 200kHz both 5V and 3V are impossible under the same model. The prior energy-only 200kHz/1.708A scenario omitted ton+toff and is not DCM feasible at 5V.

At 100kHz, 3V and 4.373W ideal target would require Ipk=2.415A; ton=12.075us already exceeds 10us period even before demagnetization. This is a **scoped topology+frequency+voltage exclusion**, not a universal rejection of CJ5143, LT3757A, MAX668, CCM or alternative winding ratios.

## Load/power mode reconciliation
- HV lamp/bus boundary remains unresolved: 16mA may mean lamps only or whole bus. 3.28W is the current target output power at 205V, not proof of actual mode load.
- USB 5V*500mA=2.5W input cannot continuously sustain 3.28W output alone, even ideally. BQ current-limit minimum threshold 450mA is not guaranteed SYS delivery.
- USB+BAT supplementary and BAT-only require separate signed IBAT and actual SYS voltage, converter efficiencies, bleeder/OVP/aux losses, and charging mode; never claim net charging from USB presence.
- A direct SYS→HV candidate must qualify at low SYS; 3V calculation is a stress scenario, not a guaranteed minimum SYS.

## Thermal and failure implications
- At L=15uH, fs=100kHz, 5V, 4.373W target implies Ipk≈2.415A, well above 1.2A characterization point. At Vin=5V ton≈7.245us and toff≈2.651us, leaving ≈0.104us ideal period margin, too small to assert a practical design.
- Primary DCR max 1ohm is not actual copper resistance. DCM triangular RMS primary squared = Ipk²*(ton/T)/3. At target: ≈1.406 A², hence Pcu,pri≈1.406W if Rpri=1ohm at 25C; not a lower bound and not a hot winding guarantee. Core, secondary, clamp, switch and diode losses add heat.
- Missing controlled dot/pin map, L(I) saturation/thermal, actual controller duty/current limits, startup, fault stop, open-load OVP, residual discharge, insulation working voltage, and Japanese stock/landed JPY. No order-ready controller+magnetics pair.

## Comparison and disposition
- CJ5143 + ideal DCM at 100kHz, 3V: NO-GO for 3.28W output at assumed 75% efficiency within ideal model.
- CJ5143 + ideal DCM at 100kHz, 5V: near boundary, BLOCKED in practice; no efficiency/thermal/continuous rating proof.
- MAX668 coupled, LT3757 flyback with alternative magnetics, LT8365 charge-pump: still unqualified research alternatives; no universal topology rejection.
- Physical HV design and 16mA requirement unchanged; no hardware or procurement authorization.

## Chat C independent review requested
1. Recompute timing/energy formulas and check all rounding, explicitly flag ideal DCM assumptions and use of eta.
2. Check whether the source's turns ratio and winding polarity/pins agree with the assumed n=15, and whether any manufacturer continuous-current rating exists.
3. Compare controlled DA2033-AL drawing and a credible 3–5V continuous 3.28W transformer; require Isat/core/thermal and real landed price, else UNKNOWN.
4. Integrator SOP proposal (do not edit docs/ai-workflow.md directly): any DCM energy-per-cycle screening must ALSO include full reset-time constraint and worst-case low-SYS; track current-source delivery separately from programmed input-current limit.

No shared indices, schedule, requirements, schematics, purchases, PCB fabrication, HV energization, or main merge changed.
