# HV-001 / Issue #2 — MAX668 specified oscillator range closes the 40uH DCM frequency escape route
Date: 2026-11-22 00:00 JST. Role: Chat A deep-design. Branch: `codex/reva-integrated-prototype-review`.
**PENDING REVIEW — NO-GO only for the stated fixed-frequency fully-reset isolated DCM combination; actual coupled topology BLOCKED. NO FORMAL CLAIM.**

## Bounded contract
Question: Can the previous 40uH isolated DCM flyback model be rescued by reducing MAX668 frequency to its calculated <=45.42kHz boundary? Exit: compare required frequency against manufacturer MAX668 operating range, including Lm tolerance and optimistic boundary duty; keep original coupled-inductor circuit unresolved.

Repository inputs re-read: docs/ai-workflow.md, docs/verification/handoff.md, docs/verification/open-issues.md, docs/verification/decisions.md, docs/tech-tree.yaml, docs/tech-tree.md, docs/reva-integrated-net-spec.md, docs/hv-transformer-screen.md, 2026-11-21 11:55/15:55/20:00 Chat A reports, GitHub Issue #2 and open issue list. GitHub connector could not enumerate the verification directory or identify the exact branch HEAD: starting SHA UNKNOWN; no blob SHA substituted. Formal atomic Claim not verified; provisional task only. Shared indexes left for Work integration.

## Primary sources and provenance
- ADI MAX668 manufacturer product page: https://www.analog.com/en/products/MAX668.html — adjustable oscillator **100kHz to 500kHz** (manufacturer published operating feature; verify detailed electrical tolerance/conditions in Rev3 datasheet before selecting ROSC). Datasheet: https://www.analog.com/media/en/technical-documentation/data-sheets/MAX668-MAX669.pdf .
- Würth 750315839: https://www.we-online.com/components/products/datasheet/750315839.pdf — Lp=40uH +/-10%, ratio 1:10; example 200V/12mA, not 205V/16mA guarantee (as recorded in docs/hv-transformer-screen.md).
- Sumida 13324-T087: https://media.digikey.com/pdf/Data%20Sheets/Sumida%20PDFs/13324-T087_Spec.pdf — 40uH +/-10%, ratio 1:10 +/-3%; no 5V/205V/16mA guarantee.
- ADI independent MAX668 flyback precedent: https://www.analog.com/en/resources/design-notes/15v-input-converter-generates-185v-at-50ma.html — +15V to -185V/50mA, custom magnetics, NOT proof at 5V/205V/16mA.

## Independent calculations (ASSUMED isolated DCM flyback, not original tapped boost)
TARGET Pout=205V*0.016A=3.280W. ASSUMED Vin=4.75V, eta=0.80 (NOT guaranteed), Vd=1V, N=10, Lm=36/40/44uH. In complete-reset DCM:
Dreset = N Vin D/(Vout+Vd);
D <= D_BCM=(Vout+Vd)/(Vout+Vd+N Vin)=206/253.5=0.812623 (equality is BCM, not DCM idle margin);
Pout=eta Vin^2 D^2/(2 Lm f).
At the lowest manufacturer-advertised MAX668 oscillator f=100kHz and *optimistic* D=D_BCM:
- Lm=36uH: Pout <= 1.656W (~8.08mA at 205V).
- Lm=40uH: Pout <= 1.490W (~7.27mA).
- Lm=44uH: Pout <= 1.355W (~6.61mA).
All are below 3.280W, even at the optimistic BCM edge. For genuine DCM with idle margin, power is lower. At 250kHz the nominal 40uH optimistic bound is ~0.596W. These are model limits under stated efficiency, not measured or universally valid power ratings.

To reach 3.28W at f=100kHz and D_BCM, Lm <=18.18uH for eta=.80, less than even 36uH tolerance minimum. At 40uH and D_BCM, f <=45.42kHz, **outside** MAX668's advertised 100–500kHz oscillator range. Lowering ROSC-derived frequency from 250kHz to 45kHz is therefore not a qualified MAX668 operating fix. Even eta=1.00 raises the 40uH, 100kHz optimistic bound only to 1.863W, still below 3.28W.

## Adversarial checks and limitations
1. This is an **isolated fully-reset DCM flyback** power envelope. A coupled/tapped boost, CCM, or different controller topology may deliver more; do NOT reject MAX668, Würth or Sumida universally. The exact Zhang/ehbtj winding dots, pin connections, switch/diode paths remain UNKNOWN. The Zhang source claims 5V→170V for a coupled-inductor boost (https://zhangshuqiao.org/2023-04/%E5%9F%BA%E4%BA%8EMAX668%E7%9A%84%E8%BE%89%E5%85%89%E7%AE%A1%E5%8D%87%E5%8E%8B%E6%96%B9%E6%A1%88/); ehbtj explicitly describes a non-isolated transformer example (https://ehbtj.com/electronics/redesign-of-boost-converter-for-nixie-tube/). Neither is a manufacturer guarantee of 205V/16mA.
2. f=100kHz is the published minimum adjustment range, NOT an assertion that every unit has an exactly guaranteed 100kHz minimum; detailed electrical limits/ROSC corners still need extraction. This distinction cannot rescue the nominal 40uH fully reset model within the specified range.
3. D_BCM depends on N, Vin, Vout, Vd. Above computations are optimistic at one Vin, efficiency and winding ratio; low rail, winding tolerance, leakage, Isat, current sense, diode recovery, switching loss and thermal only worsen or change actual margins.
4. In CCM, energy transfer includes nonzero valley current and these DCM limits do not apply. Existing repo fixed-frequency CCM screen is also assumption-dependent and requires the original circuit identity.
5. Manufacturer application examples are not evidence of output current qualification at project operating point. Independent OVP/hard-off/discharge and startup/thermal remain P0 blockers.

## Disposition
**NO-GO (narrow):** 40uH +/-10% with MAX668 operating in its advertised 100–500kHz range delivering 3.28W at 4.75V by the assumed fully-reset isolated DCM flyback mechanism, even at ideal BCM boundary and 100% efficiency.
**CONDITIONAL:** algebraic oscillator-range contradiction under the explicit DCM model.
**BLOCKED:** actual MAX668 tapped/coupled-inductor schematic identification, CCM/other mode stresses and 205V/16mA feasibility, guaranteed losses/thermal, startup, OVP and discharge.
**PENDING REVIEW:** Chat C independent challenge; Work may integrate after review, no part/architecture adoption.

## Next bounded action
Trace original Zhang and ehbtj circuit images into an explicit connection table (primary/secondary dots, switch, diode, HV output, ground). Draw ON/OFF current paths and calculate topology-specific VDS, diode VRRM, peak/valley and loss envelope at the actual ROSC. If images cannot be unambiguously read, mark BLOCKED rather than recycle isolated DCM equations. Do not alter shared indices, schematic, requirements, buy/fabricate, energize HV, or merge main.
