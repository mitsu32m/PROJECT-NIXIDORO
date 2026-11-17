# HV-001 — MAX668 coupled-inductor evidence and quantitative flyback reference screen

Date: 2026-11-17 10:25 JST (analysis time approximate)
Role: Chat A / deep-design, provisional work without claim
Status: **PENDING REVIEW — CONDITIONAL feasibility hypothesis; NOT ORDER-READY**
Branch: `codex/reva-integrated-prototype-review`
Issue: HV-001 (Markdown register); GitHub issue #1 is workflow implementation, **not** a claim.
Starting HEAD SHA: not provided by branch search; no claim of SHA-based conflict exclusion.

## Prior art and overlap
Read SOP, handoff, open issues, decisions, YAML and Mermaid tech trees, 09:30 MAX668 coupled-inductor precedent report, hv-architecture-decision, hv-transformer-screen, hv-voltage-window, and PWR power-thermal review. No new claims of a 205V/16mA tested converter. Existing 09:30 report identifies Zhang 2023 (170–174V class, TTRN-060S-054) and ehbtj 2022 (~200V, TTRN-060S-013-T); neither gives primary magnetic parameters or a qualified 205V/16mA continuous result. Their actual winding schematics have **not** been independently retrieved in this run; topology remains unverified.

## Primary evidence and classification
- ADI MAX668/MAX669 Rev3 (2016), https://www.analog.com/media/en/technical-documentation/data-sheets/MAX668-MAX669.pdf : flyback and isolated output configurations explicitly supported (manufacturer statement); MAX668 non-bootstrapped output unrestricted by its 28V VCC limit; MAX668 VCC 3–28V (specified), 200kΩ ROSC frequency 225/250/275kHz min/typ/max, maximum duty 87/90/93% min/typ/max (at specified conditions), CS threshold 85/100/115mV, shutdown delay 70µs (table figure, not a system OVP bound), FB 1.22–1.28V over -40..85C. Manufacturer's >90% efficiency statements are NOT applicable guarantees for this design.
- Würth 750315839 Rev003.001 (2022-11-10), https://www.we-online.com/components/products/datasheet/750315839.pdf : Np:Ns=1:10; Lp=40µH ±10%; Isat 3.2A TYP at 20% L reduction, not guaranteed; primary DCR 0.085Ω ±10%, secondary DCR 8.4Ω ±10% at 20C; leakage <=0.5µH; 1500VAC insulation test; manufacturer typical application 4–36V, 50–200kHz, 200V/12mA, NOT 205V/16mA guarantee.

## Independent numerical envelope — ordinary flyback only, NOT coupled boost
Design point: Vin=4.75V ASSUMED, Vout=205V TARGET, Iout=16mA TARGET, eta=70% ASSUMED, f=200kHz ASSUMED, Lp=36µH specified minimum, N=Ns/Np=10. Ideal CCM duty D=Vout/(Vout+N*Vin)=0.81188. Pout=3.28W; assumed Pin=4.6857W; Iin=0.9865A. Current-budget proxy Ipri,on=Iin/D=1.215A; triangular ripple ΔI=Vin*D/(Lp*f)=0.5356A; peak=1.483A; valley=0.947A. The ideal duty and lossy input-power assumption are intentionally combined as a conservative sizing proxy, NOT a self-consistent efficiency/CCM solution; actual duty shifts with losses and rectifier drop. The implied ideal secondary current would exceed the specified load and cannot be presented as a physical operating point.

Ideal off-state MOSFET VDS=Vin+Vout/N=25.25V, EXCLUDING leakage spikes, diode drop, ringing, startup and tolerances. A 30V MOSFET would have <4.75V ideal headroom and is NOT qualified. A 60V or higher candidate is a *screening suggestion*, not a selected rating; validate VDS under measured/clamped leakage and derating. Ideal diode reverse voltage for flyback is Vout+N*Vin=252.5V, EXCLUDING transients and tolerances. Thus 200V and 250V diode ratings cannot be accepted; >=400V is only a preliminary candidate class, not a final specification. The **coupled-inductor boost** can have different switch/diode stresses and must be recalculated from its exact winding schematic.

At the assumed current proxy, Ipri,rms=sqrt(D*(Ipri,on²+ΔI²/12))≈1.104A. With primary DCR maximum at 20C =0.0935Ω, Pcu,primary≈0.114W (20C ONLY). A similarly idealized secondary RMS current proxy sqrt((1-D)*(Ipri,on²+ΔI²/12))/N≈0.0531A gives Pcu,secondary≈0.0261W at 20C using secondary DCR max 9.24Ω; this proxy overstates ideal delivered load for assumed eta=70% and is **not** a consistent total-loss model. Copper temperature multiplier at 100C relative to 20C is ~1+0.00393*(100-20)=1.314 (ASSUMED copper coefficient), giving ~0.150W primary and ~0.034W secondary. Core loss and AC winding loss UNKNOWN. Leakage energy per cycle if all dissipated, 0.5*0.5µH*(1.483A)^2*200kHz≈0.110W, a **scenario** not a guaranteed snubber loss or spike bound.

A MOSFET with RDS(on)=0.20Ω ASSUMED would dissipate ~0.244W conduction at this current proxy (temperature and gate drive unknown). A diode with VF=1.0V ASSUMED would dissipate ~0.016W at 16mA average, ignoring reverse recovery/capacitance and waveform-dependent loss. These values are **sensitivity examples, not selected components or worst-case bounds**. Switching loss cannot be calculated without MOSFET Qg/Coss, rise/fall times, snubber, frequency and actual waveforms. 70% efficiency allows 1.406W total HV-stage loss, but summing incomplete proxy component losses does not prove the 70% assumption.

MAX668 CS limit: with 85mV GUARANTEED MIN threshold, RCS <=0.085/1.483≈0.0573Ω would be needed to avoid a nominal proxy peak tripping under these exact assumptions; this is **not** a resistor selection because max threshold 115mV implies higher fault peak, CS noise/filtering and tolerances matter. 3.2A Isat is TYPICAL and not a protected peak limit.

Frequency compatibility: ROSC=200kΩ yields guaranteed 225–275kHz at specified table conditions, beyond the Würth typical application 50–200kHz. Choosing a different ROSC requires rechecking frequency min/max, current limit, losses and control; merely changing ROSC to nominal 200kHz is not qualification.

## Startup, fault, system limits
- MAX668 soft-start is described but does not guarantee 205V startup into full load; HV output capacitance, initial conditions, pulse limit, feedback loop and TPS61023 5V droop are UNKNOWN.
- For C_HV=1µF ASSUMED, E=0.5*C*205²=21.0mJ. At 3.28W useful output, an impossible zero-loss lower-bound charge time is 6.4ms; a real startup may be longer and input power peaks larger. Capacitor value, bleeder and output startup profile are unspecified.
- 205V*16mA=3.28W; 70% HV efficiency -> 4.686W/0.937A from 5V, before logic. At 85% 5V stage -> 5.513W from SYS, before logic; existing PWR review says batteryless USB at 500mA configured input is insufficient.
- Static FB tolerance and independent OVP window remain HV-002 blockers. 70µs controller shutdown delay is not a guarantee that output will stop below 220V. 200V output capacitor ratings cannot be reused for 205V.
- No guaranteed transformer core loss, flux density, winding thermal resistance, ambient enclosure temperature, MOSFET stress, diode stress, startup or thermal margin. **No approval to energize HV**.

## New research increment vs previous report
(1) Ideal ordinary-flyback switch and rectifier voltage stress quantified; (2) MAX668 minimum CS threshold tied to current budget; (3) frequency conflict at guaranteed 225–275kHz made explicit; (4) component copper/leakage/MOS/diode loss sensitivity separated from actual guaranteed loss; (5) identified that mixing assumed eta with ideal duty yields only a conservative sizing proxy, not a solved physical operating point. None of these results qualifies the coupled-inductor design without its winding connection.

## Conclusion and next tasks
**CONDITIONAL** as an investigation path; **PENDING REVIEW** for any engineering adoption. MAX668 is capable of controlling flyback topologies in principle; neither the cited hobbyist coupled-inductor implementations nor Würth typical application proves 205V/16mA continuous. **BLOCKED** for selection of actual coupled-boost transformer/FET/diode until exact source schematic and primary magnetic specification exist.

Follow-up HV-001A: obtain original MAX668 coupled-boost schematics (Zhang / ehbtj), identify winding polarity, switching node and diode orientation, derive topology-specific VDS/VRRM/duty and compare to flyback. Follow-up HV-001B: request manufacturer magnetics core-loss, peak saturation and thermal data at 4.75V, 205V/16mA, 100–200kHz and find qualified parts. Follow-up HV-001C: quantify startup input current with TPS61023 and HV capacitance; maintain hard-off/OVP/discharge as independent safety gate.

No KiCad edits, purchase, fabrication, main merge or high voltage work. This report has not been independently reviewed.
