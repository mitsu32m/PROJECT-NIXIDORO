# MAX668 coupled-inductor Nixie precedent — correction to earlier architecture screening

Date: 2026-11-17 JST.
Status: **RESEARCH FINDING / CONDITIONAL / NOT APPROVED**.
Branch: `codex/reva-integrated-prototype-review`.
Question: Did preceding reports prematurely exclude MAX668 from NIXIDORO due to its insufficient duty cycle in a simple boost?

## Correction

The previously rejected design is **only a non-coupled, conventional single-inductor boost** from 5 V to 205 V: ideal D=1-5/205=97.56%, exceeding the MAX668 maximum-duty datasheet specifications. This argument does **not** reject a MAX668 controller in flyback or **coupled-inductor boost** topologies, where winding ratio affects conversion. Please keep `D-003` precise and do not generalize to all MAX668 topologies.

## Examined precedents — community evidence, NOT manufacturer guarantees

1. Zhang Shuqiao, 2023-04-24, https://zhangshuqiao.org/2023-04/基于MAX668的辉光管升压方案/ . Describes MAX668 + coupled-inductor boost (similar to NCH8200HV), redesigned PCB after high ground impedance contaminated REF and produced only ~70 V; revised board reportedly supplies 174 V and drives six IN-14 tubes. Notes NCH8200HV's identifiable transformer marked **TTRN-060S-054**, not -013-T. Blog references open schematics at oshwhub and 51hei, but 205 V/16 mA, temperature and worst-case are not established. Blog mentions a 200 V output capacitor candidate; **a 200 V rated capacitor is not acceptable for a nominal 205 V rail** without a separate defensible design specification.
2. Another independent builder, 2022-06-25, https://ehbtj.com/electronics/redesign-of-boost-converter-for-nixie-tube/ . MAX668 transformer 5 V to nominally 200 V; specifically describes **TTRN-060S-013-T** as bought from a marketplace. Displays IN-18 lighting after repair of transformer pin mapping, but explicitly has no proper quantified performance characterization. Transformer authenticity, original manufacturer Lp, Isat, leakage, creepage/insulation, temperature and availability **remain unknown**.
3. https://oshwhub.com/stevenjoezhang/nixie-power_copy lists 5 V→170 V coupled inductor boost, at least six IN-14 by author claim.
4. Independent commercial MAX668-*compatible clone* module teardown at https://www.mikrocontroller.net/articles/Nixie-Röhren/Versorgung/Kaufmodule/Nixie_Supply_ae1005005526009791 describes seller claim 170 V /16 mA continuous, and measured voltage-vs-current curves. This is a different IC (not guaranteed MAX668-equivalent at all ratings) and cannot qualify 205 V/16 mA.

## Manufacturer primary document

ADI MAX668/MAX669 Rev3 datasheet: https://www.analog.com/media/en/technical-documentation/data-sheets/MAX668-MAX669.pdf . General description explicitly includes step-up, SEPIC, flyback and isolated output configurations; for MAX668 used non-bootstrapped the IC does not impose a 28 V **output** limit. Check actual max duty, feedback/currents/temperature against exact datasheet table before design.

## NIXIDORO evaluation scope

205 V ×16 mA = 3.28 W HV output. For comparison 170 V×16 mA=2.72 W; the NIXIDORO output power is 20.6% more. At assumed (not measured) HV efficiency 60/70/80%, required 5 V HV input currents are 1.093/0.937/0.820 A respectively; PWR TPS61023 must also supply other logic and inrush. No tested NIXIDORO system efficiency/thermal margin is available.

## Required follow-up before any KiCad HV power-stage design

- Retrieve author **actual schematics** and identify whether both precedents use the same topology, pin mappings, polarity, magnetics, and MOSFET voltage margin; do not infer from prose.
- Find primary specs of TTRN-060S-013-T and TTRN-060S-054; if none obtainable, use only as non-qualified experimental references.
- Model coupled-inductor boost and flyback separately over min 5 V supply, Vout setpoint around 200–205 V, 0–16 mA, startup/no-load, FET/diode stress including leakage spikes, winding currents and saturation, frequency, losses/thermal.
- Revisit the 205 V nominal voltage-tolerance problem: MAX668 FB + resistors static high 214.13 V in prior model; independent OVP and overshoot must stay under HV5524 recommended max 220 V. Community reference has no verified safe OVP for this project.
- Check HV output capacitor rated voltage: do not reuse 200 V-rated caps from 170 V precedent without margin.
- Keep manufacturing, component ordering and HV energization NO-GO until review and validation.

Conclusion: **PROMOTE MAX668 coupled-inductor boost to active comparative candidate; do not claim 205 V/16 mA is established.**
