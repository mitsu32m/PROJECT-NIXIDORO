# Chat B — HV-001 / PROTO-001: LT3757 + Coilcraft Q4434/Q4435 sourcing false-positive screen
Date: 2026-11-23 01:00 JST (scheduled research window; exact wall-clock completion may differ)
Role: wide-research. **PENDING REVIEW — NO FORMAL CLAIM**
Result: **CONDITIONAL** controller research; **NO-GO** for treating the two advertised transformer examples as qualified 205 V magnetics; actual 205 V/16 mA system **BLOCKED**.

## Task contract and baseline
Branch: `codex/reva-integrated-prototype-review`; starting HEAD **e74133db9e1e468cdad6929e97a37ffc9889c6c0** (GitHub branch endpoint, not blob SHA). Related Issues #7 (PROTO-001), #4 (SYS-001A), #10 (LT8365), #2 (MAX668 actual topology). Objective: identify an externally switched flyback controller with a manufacturer source, then test whether two *actually named* commercial magnetics constitute a qualified controller+transformer pair. Exit: classify source claims vs engineering requirements and identify missing winding proof. Excludes adoption, hardware changes and purchasing.

Read SOP, handoff, open-issues, decisions, YAML/Mermaid tech trees; latest A 2026-11-22 23:56, C 21:08, B 21:00, GitHub issue register. These show no qualified HV stage and the 2026-11-22 ADI 1:9 autotransformer Ip=2.3A provenance correction. Formal atomic Claim mechanism not demonstrated; continue provisionally without claim.

## Primary evidence (checked 2026-11-23 JST)
1. Analog Devices LT3757/LT3757A manufacturer product page and Rev.H datasheet listing: https://www.analog.com/en/products/lt3757.html . **MANUFACTURER:** production controller supports boost/flyback/SEPIC/inverting, VIN 2.9–40 V, external N-channel MOSFET, switching frequency 100 kHz–1 MHz, programmable soft-start/UVLO. This establishes *controller topology/input-voltage plausibility only*, NOT 205 V output, switch rating, 5 V gate drive performance, 3.28 W thermal or a specific transformer. ADI's displayed DC1341A/B demonstration is **5 V output**, not 205 V.
2. Coilcraft **Q4434-BL** official https://www.coilcraft.com/ja-jp/products/transformers/power-transformers/power-converter-transformers/q4434/ . **MANUFACTURER:** example use 4–6 V input, **5 V / 1.6 A output** at 100 kHz, LM258X, advertised one-unit price US$6.85 and stock text on fetched product page. This is **NOT** evidence of 205 V winding ratio/diode insulation/continuous HV load; price excludes Japan landed costs and stock is dynamic.
3. Coilcraft **Q4435-BL** official https://www.coilcraft.com/en-us/products/transformers/power-transformers/power-converter-transformers/q4435/ . **MANUFACTURER:** example 4–6 V input, **5 V / 1.6 A output** at 100 kHz, LM258X, advertised one-unit price US$5.83. Its low-voltage application does not establish suitability for 205 V. Stock and Japan landed cost UNKNOWN.
4. Coilcraft **TA7608** official https://www.coilcraft.com/en-us/products/transformers/power-transformers/power-converter-transformers/ta7608/ . Manufacturer calls it Si88xx digital-isolator supply transformer; listed 60 nH leakage and 2500 Vrms one-minute isolation, one-unit price US$3.61. **NOT a qualified 205 V/3.28 W transformer** merely because insulation and low leakage are advertised. No compatible controller/waveform pairing established.

## Numerical qualification gates (ASSUMED efficiency, not measurements)
Target 205 V × 0.016 A = **3.28 W**. A 5 V input at assumed HV efficiency 0.75 requires **4.373 W / 0.875 A** at converter input; at 0.80 -> 4.10 W / 0.820 A. USB 5 V × 0.500 A = 2.50 W ideal upper bound; BQ input-limit 450 mA example gives 2.25 W before loss. Thus USB-only full load NO-GO irrespective of topology; USB+BAT supplement is conditional on actual power path, battery state, heat and protection. For an illustrative flyback n=Ns/Np=10, D=0.50, Vin=5 V, ideal reflected secondary output is n*Vin*D/(1-D)=50 V, **not 205 V**. Achieving 205 V at n=10 requires D=205/(205+50)=0.8039, neglecting diode drop, losses, minimum off-time, leakage and topology details. Conversely at D=0.5, n≈41.0 would be required. These are only ideal flyback algebra and do not transfer to MAX668 series-aiding autotransformer. At low input 3.0 V, n=10 needs D≈205/(205+30)=0.8723. This makes winding ratio, controller duty/min-off and saturation essential before any claim of feasibility.

## Screening table
| Proposed pair | Actual evidence | Status |
|---|---|---|
| LT3757A + Q4434-BL | Controller supports flyback; transformer marketed for 4–6 V→5 V at 8 W, LM258X | **NOT QUALIFIED**: no verified HV secondary topology/ratio/insulation/diode/drive/thermal |
| LT3757A + Q4435-BL | Same controller; transformer marketed for 4–6 V→5 V at 8 W, LM258X | **NOT QUALIFIED**: same missing HV evidence |
| LT3757A + TA7608 | Digital-isolator transformer, insulation rating ≠ 3.28 W conversion qualification | **NOT QUALIFIED** |
| MAX668 series-aiding coupled | Actual ADI 1:9 historical example (2002) at 150V/3.825W; 2.3A Ip meaning not confirmed | **ALTERNATIVE**, exact current magnetic production/sourcing UNKNOWN |
| LT8365 + DC2838A charge pump | ADI demo 9–30 V→250 V/10mA; project 5 V below demo range | **ALTERNATIVE**, 5 V/16mA not qualified |

**Do not count any of the first three as the requested two credible complete controller+magnetics pairs.** This negative result avoids a false-positive procurement shortlist.

## Thermal, failure, procurement and exit requirements
- Request manufacturer-controlled Q4434/Q4435 full winding diagram, turns ratio/dots/pinout, Lp at operating bias, Isat, primary and secondary DCR, leakage, isolation/working voltage, thermal limits; verify *actual* 205 V secondary operation before considering. Example 5 V outputs are not interchangeable with HV winding.
- For LT3757: datasheet current sense limits across temperature, MOSFET gate drive at 3–5 V input, duty/minimum-off/frequency, FET VDS and avalanche, diode VRRM and recovery, clamp energy, no-load/open-secondary startup and thermal fault. All remain UNKNOWN here.
- Independent hardware OVP with 220 V recommended HV5524 ceiling, post-trip energy, output discharge, battery UVLO and MCU-off behavior remain mandatory. No current selection is safe-release ready.
- Manufacturer web pricing is indicative USD only; exact suffix, Japan distributor 1-unit stock, JPY tax/shipping, PCB footprint and lead time UNKNOWN. **Do not purchase.**

## Chat C handoff / SOP improvement proposal
Chat C: check that the three named Coilcraft examples are *low-voltage or isolator-use examples* and cannot be counted as HV-qualified pair; verify LT3757 input range and the ideal D formula; check 3.0 V vs 5 V distinctions. Work: retain HV-001/PROTO-001 BLOCKED, and ask for one **controlled 205 V transformer winding drawing + current/thermal data** before approving a controller pair. SOP proposal (do not edit shared SOP): add a sourcing matrix field `manufacturer_demo_output_voltage` and `actual_secondary_winding_verified`; refuse a pair if demo output voltage differs materially from intended 205 V without a verified winding redesign. Avoid reporting dynamic stock as a guaranteed supply.

No main merge, spec change, procurement, fabrication, HV operation, shared-index edits or automation changes.
