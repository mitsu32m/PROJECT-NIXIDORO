# C-REVIEW-001 — Independent desk review: Chat A HV-001 and Work integration
Date: 2026-11-17 14:57 JST
Role: Chat C, independent first-stage reviewer (no formal issue claim)
Status: **CHANGES_REQUESTED** for Chat A frequency characterization; **CONDITIONAL** for comparative research; **BLOCKED** for HV component/topology adoption, hardware and safety release.
Repository: mitsu32m/PROJECT-NIXIDORO
Branch: codex/reva-integrated-prototype-review
Starting HEAD: d70053de280e31e3d2831d03eedc86e29ee28a52
Parent: HV-001, HV-002, SYS-001; proposed C-REVIEW-001.
Inputs: [Chat A 10:25](2026-11-17-1025-JST-HV-001-max668-quantitative-screen.md), [Work integration](2026-11-17-work-integration-001.md), [B precedent](2026-11-17-0930-JST-max668-coupled-inductor-precedents.md), [voltage window](../hv-voltage-window.md), SOP, handoff, open issues, decisions, YAML/Mermaid tech trees.
Scope: desk audit of equations, assumptions, claims and adoption gates; **not** an independent physical test, source schematic extraction, or a complete manufacturer-document page-by-page audit. Primary-document links are cited from reviewed reports; numeric manufacturer specifications require final direct datasheet confirmation before design adoption.

## Independent arithmetic and cross-check
- TARGET: Vout=205 V, Iout=0.016 A -> Pout=3.280 W.
- ASSUMED efficiency 70%, input 4.75 V -> Pin=4.685714 W, Iin=0.986466 A.
- ASSUMED ideal flyback turns ratio Ns/Np=10; ideal CCM duty D=205/(205+10*4.75)=0.811881. The ideal lossless duty equation and lossy input current **cannot jointly define a self-consistent steady-state waveform**.
- Under this intentionally mixed proxy, Iprimary,on=Iin/D=1.215038 A, ripple=4.75*D/(36µH*200kHz)=0.535616 A, peak=1.482846 A, Irms(primary)=1.103632 A. At primary DCR 0.0935Ω (quoted 20°C maximum), copper proxy=0.113883 W. These reproduce A's arithmetic.
- **Additional important quantified inconsistency:** that same waveform predicts ideal secondary average current Isecondary=(1-D)*Iprimary,on/10 = **22.857 mA**, i.e. **42.86% above** the 16 mA target. This is precisely 16mA/0.70. Therefore derived secondary RMS, winding losses, MOSFET conduction and current-sense thresholds are *not* simultaneous operating-point or guaranteed worst-case numbers. They are useful only as clearly bounded sensitivity proxies; neither necessarily upper-bounds real worst-case startup, fault or temperature currents.
- Ideal no-loss consistency comparator (NOT real design): Iin=Pout/4.75=0.690526 A, Iprimary,on=0.850526 A at the same ideal D. Neither this nor the mixed proxy qualifies MOSFET, magnetics, sense resistor or thermal performance.
- Ideal switch VDS=4.75+205/10=25.25 V and ideal diode reverse=205+10*4.75=252.5 V are valid only for the **ordinary flyback connection** at the given voltage point. Leakage, clamp, winding polarity and no-load are absent. Do not transfer these to the actual coupled-inductor boost candidate.
- MAX668 static divider: ratio Rtop/Rbottom=163, VFB range 1.22–1.28 V and ±1% resistors -> Vout low **196.142 V**, high **214.135 V**, static margin to recommended 220 V only **5.865 V**. This is not a guaranteed OVP window because dynamic excursion, sensing tolerances, FB bias and fault latency are absent.
- USB-only configured input limit cited by Work: 5V*498mA=2.490W maximum under that cited table condition, less than HV target output 3.280W even at impossible 100% efficiency. **ACCEPTED as a conditional input-power impossibility proof for the 500mA configuration**, not proof of battery-supplement, charging or thermals.
- Work mode table recalculation for IHV=16mA: P5=3.28/.70+.50=5.185714W; PSYS=P5/.85+.50=6.60084W; converter losses=3.28*(1/.70-1)+P5*(1/.85-1)=2.32084W. Correct under stated assumptions. Not whole enclosure heat.

## Claim-by-claim review
| Claim | Verdict | Scope and required correction |
|---|---|---|
| MAX668 conventional non-coupled 5V→205V boost ruled out by ideal duty ~97.56% | ACCEPTED (topology-specific) | Do not generalize to MAX668 coupled or flyback |
| MAX668 coupled-inductor or flyback merits comparative research | CONDITIONAL | Controller topology support and hobby examples are not 205V/16mA continuous evidence |
| Würth 750315839 candidate with 40µH±10%, 1:10, typical 200V/12mA application | CONDITIONAL as literature screen only | At 16mA target, typical 12mA example does not qualify transformer; 50–200kHz example band vs proposed frequency needs actual manufacturer loss/thermal qualification |
| MAX668 ROSC=200kΩ frequency 225–275kHz described as guaranteed over full temperature | CHANGES_REQUESTED | Work identifies full −40..85°C 222–278kHz, while 225–275kHz applies 0..85°C; verify exact Rev3 table and label temperature condition explicitly |
| A's mixed efficiency/ideal duty current and loss proxies | CONDITIONAL as sensitivity illustrations; REJECTED as design ratings | Secondary-current inconsistency above; require self-consistent converter model and component corners |
| MOSFET 60V class, diode >=400V class and RCS<=0.0573Ω | CONDITIONAL screening only | No actual selected part, clamp/overshoot, tolerance or guarantee; cannot be BOM release |
| Work D-012 mode-specific power contract before final selection | CONDITIONAL as integration priority | Supports prioritizing HV-004 lamp current provenance and SYS-001; not an approved changed requirement |
| Independent OVP and hard-stop keep worst-case under HV5524 recommended 220V | BLOCKED as implemented safety function | No independent OVP schematic, bounded trip/latency/energy, fault path, discharge and supervised validation |

## Sources and evidence quality
- [ADI MAX668/MAX669 Rev3](https://www.analog.com/media/en/technical-documentation/data-sheets/MAX668-MAX669.pdf) — manufacturer primary link supplied by Chat A/Work; this review independently recomputes formulas but **did not independently extract all PDF tables**.
- [Würth 750315839 Rev003.001](https://www.we-online.com/components/products/datasheet/750315839.pdf) — manufacturer primary link supplied by Chat A; 3.2A saturation cited as TYPICAL, not guaranteed.
- [Microchip HV5524 DS20006850](https://ww1.microchip.com/downloads/aemDocuments/documents/APID/ProductDocuments/DataSheets/HV5524-32-Channel-Serial-to-Parallel-Converter-Data-Sheet-DS20006850.pdf) — 220V recommended / 230V absolute distinction cited by prior reviews; direct re-verification remains open.
- [TI BQ25185](https://www.ti.com/lit/ds/symlink/bq25185.pdf) — 498mA maximum cited by Work under its specified 5V/table conditions; exact mode/thermal behavior not independently validated here.
Classification: target and assumed efficiencies are ASSUMED; cited electrical table bounds require manufacturer temperature/condition matching; NO measured data. Blog examples are community evidence, not guarantees.

## Review disposition / Work judgment package
**Decision question:** Can Work adopt MAX668 coupled boost, 750315839 flyback or the 205V/16mA HV stage and its OVP from A's quantitative screen?
**Answer:** **NO — BLOCKED for adoption**. Continue **CONDITIONAL comparative research**. Keep D-003's conventional-boost rejection; retain D-004/D-005/D-006/D-007 and D-012 without promotion.
**Alternatives:** (a) qualified ordinary flyback with coherent loss and current model, (b) original-schematic-qualified coupled-inductor boost, (c) manufacturer-rated module, (d) revised display-current requirement *only after user approval*.
**Risks:** 5V-stage current/startup; low-cell and charger supplement; actual transformer core loss/temperature and saturation; leakage stress; independent OVP response and discharge; PETG enclosure and cell temperature.
**Next actions:** (1) Chat A correct frequency temperature range and label proxies unambiguously; (2) obtain actual coupled circuit schematic and transformer manufacturer's full magnetics data; (3) establish lamp current/current-limit/brightness primary evidence (HV-004A); (4) integrate a mode-specific 5V/SYS/BAT contract and independent OVP tolerance/energy design; (5) Chat C re-review corrected data. No new duplicate issue needed: existing GitHub #2 covers HV-001A, #3 HV-002A, #4 SYS-001A.
**Work handoff:** This report is the review/judgment package for Work; Work should cite this file and not treat it as a hardware release. Review of all manufacturer primary pages remains outstanding.

No KiCad, shared index, main, purchase, manufacture or HV energization modifications.