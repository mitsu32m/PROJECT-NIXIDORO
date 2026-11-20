# HV-001 / Issue #2 — MAX668 coupled-winding turns-ratio minimum and duty headroom screen
Date: 2026-11-21 08:00 JST. Role: Chat A deep-design. Branch: codex/reva-integrated-prototype-review.
**PENDING REVIEW**. Claim: NONE; atomic Claim not established. **CONDITIONAL** analytical rejection screen, **BLOCKED** actual stage qualification.

## Contract and source baseline
Question: At minimum 5V-rail input and the MAX668 guaranteed maximum duty limit, which turns ratios are even *ideally* feasible at 205V/16mA? Scope: static ideal volt-second balance only, not magnetics or product approval.
Read current branch ai-workflow, handoff, open-issues, decisions, tech-tree.yaml, prior SYS-002 report, docs/hv-transformer-screen.md and GitHub issue search. GitHub search_commits returns older default-branch commits, NOT branch HEAD. Starting branch HEAD UNKNOWN; no false SHA asserted. Complete tree enumeration/concurrent-write exclusion not established. Unique file only; shared indexes left to Work.

## Sources and classifications
- ADI MAX668/MAX669 primary datasheet: https://www.analog.com/media/en/technical-documentation/data-sheets/MAX668-MAX669.pdf . Prior transformer-screen records MAX668 duty max **minimum 87%** at ROSC=200kohm (GUARANTEED at stated test conditions; verify full operating conditions and switching-mode applicability before circuit adoption).
- Existing repository primary-screen: docs/hv-transformer-screen.md, Würth 750315839 https://www.we-online.com/components/products/datasheet/750315839.pdf (10:1), Sumida T086 https://media.digikey.com/pdf/Data%20Sheets/Sumida%20PDFs/13324-T086_Spec.pdf (5:1), T087 https://media.digikey.com/pdf/Data%20Sheets/Sumida%20PDFs/13324-T087_Spec.pdf (10:1). These parts are not approved.
- Vin=4.75V, Vout=205V: ASSUMED design corners; diode forward drop 0V and 1V: ASSUMED illustrative; duty design ceiling 0.82: ASSUMED margin, not manufacturer guaranteed; 16mA target, Pout=3.28W.

## Independent derivation
For an ideal coupled-inductor / flyback-like energy transfer with primary-to-secondary ratio 1:N, neglecting leakage and losses, volt-second balance gives
Vin D = (Vout+Vd)(1-D)/N.
Thus D=(Vout+Vd)/[(Vout+Vd)+N Vin], and the *minimum* turns ratio to satisfy a duty ceiling Dlim is
N >= ((Vout+Vd)/Vin)*((1-Dlim)/Dlim).
This is a necessary condition ONLY, not sufficient for a MAX668 implementation.

| Vin | Vout+Vd | Dlim | Nmin | 1:5 result | 1:10 result |
|---:|---:|---:|---:|---|---|
| 4.75V | 205V | 0.87 | 6.449 | FAIL | ideal pass |
| 4.75V | 206V | 0.87 | 6.480 | FAIL | ideal pass |
| 4.75V | 206V | 0.82 | 9.518 | FAIL | ideal pass with tiny margin |

For 4.75V, 206V effective output, N=10: D=206/(206+47.5)=0.81262 (81.26%). N=5: D=206/(206+23.75)=0.89663 (89.66%), exceeding 87% guaranteed minimum maximum duty. If N=10 has -3% ratio variation (ASSUMED; actual manufacturer tolerance per exact part), D=206/(206+9.7*4.75)=0.81729, leaving only ~0.27 percentage points below the **assumed** 82% design ceiling. Diode loss, finite winding resistance, switching dead time, leakage, core losses and controller dynamic limits can eliminate this margin.

## Challenge and limitations
A minimum duty-ratio pass is not a proof of continuous 3.28W. Need real coupled-inductor winding configuration (not automatically equivalent to isolated flyback), controller peak current / current-sense, switch voltage stress Vin+(Vout+Vd)/N plus leakage spike, rectifier reverse stress, transformer core loss/saturation and 50–200kHz operating applicability. At N=10, ideal switch off-state ~4.75+20.6=25.35V before leakage spike; this is not a MOSFET voltage rating recommendation. Actual 16mA power capability, startup at low SYS, post-trip energy and independent OVP remain UNKNOWN. MAX668 duty limits at a revised ROSC/frequency cannot be carried over without primary datasheet re-check.

## Result and handoff
**NO-GO (limited)**: 1:5 ratio under the stated 4.75V/205V and 87% guaranteed-duty corner, even before losses.
**CONDITIONAL (limited)**: 1:10 ratio passes ideal duty; near 82% margin and physical power/thermal feasibility unproven.
**BLOCKED**: actual MAX668 205V/16mA continuous and independent OVP, hardware qualification.
**PENDING REVIEW**: Chat C independently verify datasheet duty guarantee, model topology and calculations; Work retain unchanged requirements and adoption hold. Next Chat A should obtain exact 1:10 magnetics and controller full-temperature duty/current-limit behavior, then calculate switching/current/thermal with a real schematic, not repeat arbitrary capacitance examples.
No purchase, PCB manufacturing, HV energization, main merge, specification or KiCad change.
