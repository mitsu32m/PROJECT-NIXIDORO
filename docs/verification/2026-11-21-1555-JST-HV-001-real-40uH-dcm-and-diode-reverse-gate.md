# HV-001 / Issue #2 — 40uH actual candidate versus DCM power and rectifier reverse stress
Date: 2026-11-21 15:55 JST. Role: Chat A deep-design. Branch: `codex/reva-integrated-prototype-review`.
**PENDING REVIEW — CONDITIONAL model screen; hardware BLOCKED. NO FORMAL CLAIM.**

## Task contract / repository evidence
Question: In the *explicitly hypothetical isolated single-switch DCM flyback* model from Chat A 11:55, can an existing actual 40uH candidate deliver 205V x 16mA at 100kHz and 4.75V, and what diode reverse-voltage bound does this topology imply? Exit: reproducible model comparison against actual manufacturer Lm tolerance, and topology-specific diode rating gate. This is NOT proof of the original MAX668 coupled-inductor circuit.

Read branch SOP, handoff, open-issues, decisions, tech-tree.yaml, tech-tree.md, docs/hv-transformer-screen.md, Chat A 08:00/11:55 and Chat B 09:01 reports, GitHub issue #2 and issue search. Branch HEAD exact SHA and complete latest report enumeration unavailable through the available GitHub connector; **UNKNOWN**, not substituted with blob SHA. Shared indexes reserved for Work integration to avoid concurrent edits.

## Primary component inputs and classifications
- Würth 750315839 manufacturer sheet https://www.we-online.com/components/products/datasheet/750315839.pdf ; repository manufacturer screening: Lp=40uH +/-10% (manufacturer specification), Ns/Np=10, primary DCR 85mOhm +/-10% at 20C, secondary DCR 8.4Ohm +/-10%, saturation 3.2A **TYPICAL** at 20% L decrease, leakage <=0.5uH. Representative application 200V/12mA, NOT 205V/16mA guarantee.
- Sumida 13324-T087 manufacturer source https://media.digikey.com/pdf/Data%20Sheets/Sumida%20PDFs/13324-T087_Spec.pdf ; existing screen lists Lp=40uH +/-10%, Ns/Np=10 +/-3%, primary DCR <=130mOhm, secondary <=19Ohm. No 205V/16mA manufacturer guarantee.
- ADI MAX668/MAX669 datasheet https://www.analog.com/media/en/technical-documentation/data-sheets/MAX668-MAX669.pdf . Its real topology, current-sense and ROSC setting are NOT validated by the model below.
- TARGET Pout=205V*0.016A=3.28W. ASSUMED Vin=4.75V, f=100kHz, eta=0.80, D=0.75, Vdiode=1V, N=10. The existing MAX668 Rosc=200kohm draft gives nominal 250kHz, **not** the assumed 100kHz; component application frequency must be checked.

## Independent DCM calculation
For fully reset isolated flyback with linear triangular magnetizing current:
Ipk=Vin*D/(Lm*f); Pout,idealized=eta*Vin^2*D^2/(2*Lm*f).
At Lm=40uH, D=.75, Vin=4.75V, f=100kHz, eta=.80:
Ipk=0.890625A; Pout=1.26914W; Iout=6.191mA. With Lm 36uH (tolerance low): Pout=1.41016W; at 44uH: 1.15376W.
To achieve 3.28W at same assumptions, Lm_required=15.48uH and Ipk_required=2.302A. This is not an instruction to substitute a 15.48uH transformer: turns ratio, saturation, leakage, core and copper losses, frequency, and real circuit must be requalified.
DCM reset check: Dreset=N*Vin*D/(Vout+Vd)=10*4.75*.75/206=0.17294; idle fraction=0.07706. D=.81262 from the earlier ratio calculation is the BCM boundary and cannot be counted as DCM with idle margin.
The power model assumes eta=.80 independent of L and current; real efficiency will vary. At 250kHz with unchanged 40uH and D=.75, DCM idealized output is only ~0.508W (under fixed duty); this is a scenario, not a MAX668 performance prediction. At fixed 40uH and 100kHz, DCM power increases with D but D cannot exceed reset boundary.

## New diode reverse-voltage gate — *isolated flyback only*
When the primary MOSFET is ON, the secondary diode is reverse biased. For the stated isolated winding polarity, ideal reverse voltage is approximately Vout + N*Vin, NOT merely Vout. With Vout=205V, N=10, Vin=5.25V (ASSUMED high rail), this is **257.5V before ringing**. At N=10.3 (illustrative +3% ratio corner), **259.075V before ringing**. If a candidate diode is rated 250V, it fails this model even before ringing; 300V rating is NOT automatically sufficient without voltage tolerance, recovery, transient and thermal margin. These diode figures must NOT be applied to tapped/coupled-inductor boost or charge-pump architectures without tracing the actual diode node.
For isolated flyback MOSFET OFF, ideal VDS approx Vin+(Vout+Vd)/N, about 25.35V at Vin=4.75V, Vout=205V, Vd=1V, N=10, before leakage spikes. This is also topology-specific; real clamp and drain stress remain UNKNOWN.

## Contradictions and qualification
- Manufacturer 40uH candidates and 100kHz DCM 3.28W are incompatible under the *stated* duty/efficiency model; does not reject CCM/BCM, other frequencies or original coupled MAX668 topology.
- The Würth 3.2A saturation number is TYPICAL and cannot establish a guaranteed safe peak. DCM required 2.302A is not a guaranteed MAX668 drain-current bound.
- Diode voltage rating is a topology identity gate: isolated flyback needs at least the calculated reverse-voltage stress plus margin, but original MAX668 winding/pin/dot and diode paths must be read before selecting any rectifier.
- Continuous 3.28W, MOSFET/diode loss, PCB/enclosure thermal, startup, 220V HV5524 transient envelope, independent OVP/hard-off/discharge remain BLOCKED.

## Disposition and handoff
**CONDITIONAL**: manufacturer 40uH +/-10% candidate at 100kHz, Vin4.75V, D=.75, eta=.80 produces only 1.15–1.41W in the stated idealized DCM model. Isolated flyback diode sees ideal reverse ~257.5–259.1V at the illustrated high-rail/ratio corner, prior to transients.
**NO-GO (limited)**: claiming these 40uH parts prove 205V/16mA at 100kHz in the specified DCM model; claiming a 250V rectifier is adequate for the stated isolated flyback reverse stress.
**BLOCKED**: original MAX668 coupled-inductor topology, actual switching frequency, actual 16mA continuous feasibility and safety protection.
**PENDING REVIEW**: Chat C independently check formula, topology dependence and manufacturer tolerance provenance. Work retain unmodified D-004/D-005 and no BOM adoption.
Next A: trace original Zhang/ehbtj winding dots and actual diode conduction paths, then calculate voltage stress and current for THAT circuit rather than repeating flyback proxies.
No purchases, PCB fabrication, HV energization, main merge, requirements or KiCad changes.
