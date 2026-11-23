# Chat B — HV-001 / PROTO-001: Coilcraft CJ5143-ALC primary magnetics screen
Date: 2026-11-24 01:00 JST
Role: Chat B wide research; NO FORMAL CLAIM; PENDING REVIEW (Chat C)
Branch: codex/reva-integrated-prototype-review
Starting branch HEAD: UNKNOWN (connector exposes file-at-branch and repository-wide commit search, not a verified exact branch ref; repository-wide commits must not be substituted for branch HEAD).
Issues: #7 PROTO-001, #2 HV-001A, #4 SYS-001, #10 HV alternative.
Scope: single new physical transformer candidate; not a topology selection, parts adoption or HV test.

## New primary evidence (checked 2026-11-24)
Coilcraft CJ5143 official controlled product specification:
https://www.coilcraft.com/en-us/products/transformers/power-transformers/capacitor-charging/cj5143/
- CJ5143-ALC; 2.7–5.5 V input, 350 V output **typical application with ON NCP5080 capacitor charger**, NOT a 205 V continuous 16 mA power rating.
- 25°C: primary L0 = 15.0 uH ±10%, L at 1.2 A >=13.5 uH, primary DCR <=1.0 ohm, secondary DCR <=25 ohm, primary-referred leakage <=0.3 uH, turns 1:15, 1000 Vrms one-minute interwinding hipot. Winding pin/dot schematic image on manufacturer page; numeric pin mapping not extracted/qualified here.
- Package 6.2x6.8 mm footprint, 4.6 mm height; -40..+125°C ambient component specification. These are **manufacturer-listed** conditional values, not continuous power/thermal proof.
- Website shows USD 3.46 at quantity one, but the selected configuration also displays “not available for purchase”; actual Japanese landed price, tax, shipping, lead time and selected SKU inventory UNKNOWN.

## Reproducible bounded energy and copper screen
For a **fully reset discontinuous flyback** with at most one energy-transfer event per cycle:
E_cycle = 0.5 * Lp * Ipk^2; Pmag,ideal <= E_cycle * fs.
At Lp=15 uH, Ipk=1.2 A: E=10.8 uJ; 100 kHz -> 1.08 W; 200 kHz -> 2.16 W. Using Lmin=13.5 uH: 9.72 uJ, 0.972/1.944 W. These are scenario calculations; 1.2 A is the **specified inductance test current**, not a guaranteed hard saturation ceiling or current-limit trip.
To transfer Pout=205*0.016=3.28 W with efficiency assumed 75% (Pmag=4.373 W) and L=15 uH, required Ipk=sqrt(2*Pmag/(L*fs)) = 2.415 A at 100 kHz or 1.708 A at 200 kHz. Both exceed the 1.2 A characterization point; the L(I) curve and safe core temperature above 1.2 A are UNKNOWN. Thus **NOT QUALIFIED**, not a proof that the component physically cannot work.
Ideal copper loss with triangular primary pulse and duty D: Pcu,p ~= Ipk^2*D*Rpri/3; using D=0.5, Ipk=2.415 A, Rpri=1 ohm gives 0.972 W (at 25°C, max listed DCR); secondary copper, core, diode, clamp and switching losses additional. D=0.5 is ASSUMED, not a demonstrated timing solution. Primary copper example alone makes assumed 75% overall efficiency implausible without further evidence, but is not a guaranteed lower bound because 1 ohm is a maximum DCR, not minimum.
At n=15, Vin=5 V, Vout=205 V, ideal flyback duty D=Vout/(Vout+n*Vin)=0.732; Vin=3 V gives D=0.820; controller actual duty, reset, switch voltage, and peak current must be separately qualified. Note this ideal relation is not valid for a different coupled-inductor boost topology.
Output voltage and turns ratio do not establish continuous power rating. 1000Vrms 1-minute hipot is not a 205V continuous working voltage guarantee.

## Comparison and decisions
- Previous Q4434/Q4435: 1:1 5V output reference, excluded as 205V qualified pair.
- New CJ5143: **actual manufacturer-listed 1:15 and low-voltage input, with L/DCR/leakage data**; remains CONDITIONAL / NOT QUALIFIED because continuous 3.28W output, current above 1.2A, heat, dot/pin, controller compatibility and procurement unproven.
- MAX668 coupled and LT3757 flyback: both remain research candidates; this report does not establish either controller+CJ5143 as a working pair. NCP5080 photoflash capacitor-charging behavior is not evidence of continuous regulation at 16mA.
- USB-only full 205V*16mA remains NO-GO since 3.28W > 5V*0.5A ideal input. USB+BAT supplementation is a separate mode; net charging not implied.

## Failure and temperature gates
Open-load overshoot, secondary rectifier failure, transformer insulation, shorted load, primary switch stuck-on, loss of MCU/OVP and battery cutoff are unqualified. Independent hardware stop and safe discharge remain mandatory. 25°C DCR cannot be used unchanged at PETG internal hot conditions. No measured thermal impedance or sealed enclosure test.

## Chat C review request / next evidence
1. Independently check energy arithmetic and clarify that the 1.2A inductance test point is not Isat.
2. Retrieve CJ5143 winding dot/pin controlled drawing, L(I) and permissible RMS/temperature, and ask manufacturer whether continuous 3.28W at low input is supported.
3. Compare DA2033-AL and CJ5143 on primary-source continuous thermal/current data and Japanese distributor landed price; if unavailable, explicitly screen out instead of guessing.
4. Verify controller-compatible timing, actual primary and secondary currents, FET/diode stresses, Cmin/Cmax, OVP stop energy, USB/BAT modes.
5. SOP improvement proposal for integrator (do not directly edit docs/ai-workflow.md): distinguish manufacturer-listed low-voltage capacitor charger magnetics from continuous HV load qualification; record branch HEAD as UNKNOWN unless exact ref is verified; don't substitute repository-wide commit search.

No shared indices or schematics edited. No purchases, fabrication, HV energization, main merge, requirements or automation changes.
