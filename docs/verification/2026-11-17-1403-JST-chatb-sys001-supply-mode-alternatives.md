# Chat B SYS-001A — display-current and supply-mode architecture screen

- Date: 2026-11-17 14:03 JST (research snapshot)
- Role: Chat B / wide research; **provisional work, NO FORMAL CLAIM**
- Parent: SYS-001; related HV-004, PWR-001, PWR-002, BAT-001, HV-001
- Branch: `codex/reva-integrated-prototype-review`
- Starting HEAD: `41a9eaae6b00131915b523a251952f9678ddc2fe`
- Status: **PENDING REVIEW** for Chat C; conclusion **CONDITIONAL for architecture comparison, NO-GO for 205V/16mA USB-only at configured 500mA, UNKNOWN for battery-assisted/thermal feasibility**
- This is a calculation and primary-source-based *screen*, not measurement, approval, component selection or authorization to energize HV.

## 1. Scope and novelty

The existing WORK-INT-001 already proved the USB-only impossibility and proposed a mode contract. This report does **not** claim that calculation as new. The additional contribution is a decision matrix separating USB current limiting, power-path battery supplementation, net cell charging, and source/topology changes, plus actionable review gates. Issue #2 covers MAX668 coupled topology and Issue #3 covers OVP energy; neither is claimed or duplicated. No open `role:wide-research` task and no atomic Claim were established at snapshot; provisional work is authorized by the project owner.

Read: `docs/ai-workflow.md`, `docs/verification/handoff.md`, `docs/verification/open-issues.md`, `docs/verification/decisions.md`, `docs/tech-tree.yaml`, `docs/tech-tree.md`, `docs/verification/2026-11-17-work-integration-001.md`, `docs/pwr-reva-power-thermal-review.md`; searched open Issues #1–#3.

## 2. Primary sources, source classes, unresolved evidence

1. TI **BQ25185**, SLUSF65B Rev.B Aug 2026, [datasheet](https://www.ti.com/lit/ds/symlink/bq25185.pdf), §5.5 and §6.3.2–6.3.3: 500mA programmed input limit 450mA min / 475mA typ / 498mA max under stated VIN=5V table conditions (**GUARANTEED limits / TYPICAL** as individually tabulated); input dynamic power-path management (DPPM) reduces charging before battery supplementation, and battery may supplement SYS when demand exceeds input capability (**FUNCTIONAL description**, not a guaranteed sustained assist-current capability for this PCB). The proposed RILIM/VSET=18kΩ and ISET=1.2kΩ are design-specific, not verified measurements.
2. TI **TPS61023**, [datasheet](https://www.ti.com/lit/ds/symlink/tps61023.pdf): 2.7A minimum valley switch limit at specified conditions, typical 3.7A; efficiency varies with VIN, output and load. The 1.5A Li-ion design example is **not** guaranteed over the full operating range. Actual L1, effective output capacitance and PCB heat path **UNKNOWN**.
3. Microchip **HV5524**, DS20006850A, [datasheet](https://ww1.microchip.com/downloads/aemDocuments/documents/APID/ProductDocuments/DataSheets/HV5524-32-Channel-Serial-to-Parallel-Converter-Data-Sheet-DS20006850.pdf): 220V recommended HV maximum; 230V absolute maximum is **not** a design target. OVP remains independent and unresolved.
4. IN-12B and the **exact purchased NE-2-class neon part**: manufacturer primary documents confirming strike/maintain voltage, allowable continuous lamp current, life versus current, and resistor derating have **NOT been established in this screen**. `IN-12B 2mA each + neon 1mA each` is **ASSUMED**, not a validated optical/electrical requirement. Do not substitute arbitrary generic NE-2 seller figures for selected-device ratings.
5. Existing project scenario: `docs/verification/2026-11-17-work-integration-001.md` and `docs/pwr-reva-power-thermal-review.md`; efficiencies and miscellaneous loads below are **ASSUMED**, not manufacturer's guaranteed values or measurements.

## 3. Explicit load and mode arithmetic

For assumed simultaneous 2 IN-12B at 2mA each and 12 neon at 1mA each:
`I_HV = 2*2mA + 12*1mA = 16mA` (**ASSUMED**). `P_HV = V_HV I_HV` at 205V is 3.28W. Note that most of this HV output is dissipated in lamp current-limit resistors and driver paths; it is not emitted optical power.

Let `eta_HV=.70`, `eta_5=.85`, `P_5logic=.50W`, `P_SYSother=.50W` (all **ASSUMED**). Then
`P_5V = 205*I_HV/eta_HV + P_5logic`;
`P_SYS = P_5V/eta_5 + P_SYSother`.
At 0/4/8/12/16mA, approximate `P_SYS` = 1.11/2.47/3.85/5.22/6.60W respectively (zero-load uses an assumed 20mW HV standby, as in the existing model). These are steady-state **sensitivity points**, not supported firmware settings or approved lower current.

For USB 5V at programmed input current limit 450/475/498mA, `P_USB,max`=2.250/2.375/2.490W at that VIN (**GUARANTEED minimum/typical/maximum current-limit corners**, not power available at SYS). The 3.28W HV output alone exceeds even 2.49W, therefore **USB-only 16mA is physically impossible** at the present input setting even with ideal conversion. A more realistic `P_SYS,USB` must subtract input protection/charger/path losses and respect actual SYS voltage and input limit. Using 2.25W as a hypothetical *lossless* SYS ceiling and the assumed model, solve
`I_HV,max,ideal = [((2.25 - .50)*.85 - .50)*.70]/205 = 3.37mA`.
This **3.37mA is an optimistic model bound**, not a certified lamp current, and may be lower due to losses, current-limit transients, voltage drop, startup and temperature. With 2.49W the same idealized bound is ~4.05mA. Do not equate a 500mA USB charger rating with 500mA continuously deliverable at the battery or SYS.

For USB plus battery, define `P_SYS,demand` and actual `P_SYS,USB`. An ideal lower bound on required cell power is `P_BAT >= max(0,P_SYS,demand-P_SYS,USB)`, with actual cell power higher due to BATFET, cell protection, contact and PCB losses. At 16mA and the optimistic 2.25W SYS ceiling, the deficit is at least `6.60-2.25=4.35W` under assumed efficiencies. At an *illustrative* 3.6V cell this is ≥1.21A **before** path losses. Real DPPM/VSYS may shift the balance; this is **not** a manufacturer-guaranteed battery assist operating point. For net cell charge, require measured `I_BAT,net < 0` if discharge is defined positive; a USB cable plugged in, charge-enable pin LOW or charger STAT alone is not proof of positive charge current during high load.

### Operating-mode contract (proposed; no firmware adoption)

| Mode | Demand/constraint | Preliminary interpretation | Required evidence |
|---|---|---|---|
| USB present, battery absent | ≤ input current limit; SYS behavior without BAT unverified | **NO-GO** for 16mA; lower-load modes not automatically approved | BQ BAT-absent behavior, 5V rail startup and HV load transient |
| USB present, battery fitted, low display load | Input supports SYS and possibly charge | **CONDITIONAL**; charge current may be reduced by DPPM | Simultaneous I_USB, I_BAT, V_SYS and thermal |
| USB present, battery fitted, full 16mA | Input insufficient; BAT may supplement | **UNKNOWN / likely battery discharge**; do not advertise simultaneous net charging | Minimum cell voltage, BATFET and protection loss, source disconnect, thermal, charger status |
| Battery only, full 16mA | ~6.60W SYS assumed, low cell increases current | **UNKNOWN**; TPS61023, actual L1 and cell must be qualified | Low-cell/aged-cell transient and temperature, minimum effective 5V |
| USB unplug/replug while HV active | Power-path and control transient | **UNKNOWN / safety critical** | HV independent hard-off, supply brownout, discharge, reverse-feed |
| OLED/audio active concurrently | Extra SYS load and heat | **UNKNOWN** | Real UI/audio duty and power, startup overlap |
| Reduced lamp duty/current | Lower average or peak HV demand only if specified | **ALTERNATIVE, NOT REQUIREMENT CHANGE** | Selected lamp life/brightness/strike characteristics, no hidden peak current |

## 4. Broad alternatives and discriminators

A. **Keep 500mA input; battery-supplement full load.** Minimal baseline changes but requires selected protected cell, real BQ BATFET loss, thermal, charge state UX and 5V regulator margin; USB presence cannot be labeled charging. Prove worst-case SOC, low cell and unplug transient.

B. **Keep 500mA input; restrict USB-only display mode.** Could offer a safe low-load mode only after actual lamp current and startup demand are verified. Does not solve 16mA on USB-only. Firmware display patterns alone are not current regulation or HV safety protection.

C. **Redesign USB input current budget/power path** to support a higher advertised 5V source, while retaining 1S charging protections. This requires verifying USB-C source capability/CC policy, eFuse, charger programming, cable and heat; a higher-rated adapter cannot bypass the currently configured BQ limit. Requires owner approval before requirements/PCB changes.

D. **Battery-to-HV conversion with fewer stages**, e.g. a qualified 1S-input flyback instead of SYS→5V→HV, may avoid one conversion stage; compare realistic low-cell 3V-class input, switch peak current, magnetics, OVP, startup and control power. **No proven component candidate or efficiency figure in this report**; do not assume it wins. Keep existing HV-001 research separate.

E. **Manufacturer-qualified HV module / alternative HV controller** may reduce magnetic design risk but still must satisfy 205V/16mA continuous, load/temperature derating, startup, safety, price and physical fit; existing XP F05 module did not satisfy target. Do not conflate 170V hobbyist module evidence with 205V continuous specification.

F. **Revisit load requirement only after HV-004 primary data and measurements.** 16mA remains target until owner explicitly approves change. Multiplexing, current reduction and display duty cycle require minimum strike/maintain current and visibility/lifetime checks, and peak supply/OVP must remain within safe limits.

## 5. Loss, heat and fault boundary

At 16mA the model yields `P_HV-stage-loss=3.28*(1/.70-1)=1.406W`, `P_5-stage-loss=5.186*(1/.85-1)=0.915W`. These are *total converter* losses, **not IC junction losses**; distribute across transformer/inductor, FET, diode, IC, capacitors, resistors and PCB before computing junction temperature. The 205V*16mA load power is largely dissipated locally in lamps/series resistors/driver; evaluate the sealed PETG enclosure and cell thermal separately. `T_J=T_A+theta_JA*P_IC` is a preliminary calculation only, and thetaJA depends on actual board/enclosure. Thermal pass/fail and the 21700 temperature limits remain UNKNOWN.

If USB power disappears under full HV load, battery-assist transition, MCU brownout, HV_EN default-off, independent OVP and discharge must be evaluated together. HV5524 logic blanking is not HV power isolation. Never energize HV or fabricate boards based on this report.

## 6. Proposed next bounded tasks for Chat A / Chat C / Work

1. **HV-004A / Chat B or source researcher:** identify exact IN-12B and NE-2 selected manufacturer datasheets; table minimum maintaining current, recommended current, lifetime and voltage, lamp resistor power/voltage and simultaneous display pattern. If exact part unknown, return UNKNOWN and propose supervised brightness test only.
2. **SYS-001B / Chat A:** derive *actual* BQ25185 SYS power allocation, BATFET conduction and cell supplementation across 3.3/3.6/4.0V and USB 450/475/498mA; do not confuse battery charging with supplementing. Cross-check BQ modes/thermal and real USB source CC constraints.
3. **PWR-001A / Chat A:** qualify TPS61023 L1 Isat, valley-current limit and startup with 0/4/8/12/16mA HV equivalent load; model low-cell and PCB thermal, include effective output capacitance.
4. **HV-001B / wide research:** compare direct 1S→HV flyback against SYS→5V→HV with real component magnetics, full loss/thermal and safe stop; avoid duplicate Issue #2 coupled-inductor topology work.
5. **Chat C:** independently review 3.37mA *optimistic* USB-only model bound, BQ DPPM/supplement semantics, load assumptions and whether the proposed mode contract covers unplug/reset/fault. Preserve PENDING REVIEW until signed off.
6. **Work / integrator:** only after review, update shared issue register, decisions, tech tree and handoff; approve or reject proposed alternatives explicitly. No changes to D-005 or design targets by this worker.

## 7. Handoff and non-actions

**PENDING REVIEW**. No formal GitHub Claim; no existing deep-design issue claimed. The analysis identifies a new potential decision axis: whether the USB-connected full-load behavior should explicitly be called **battery-assisted discharge** rather than **charging while operating**. Existing SYS-001 is the parent; do not create a duplicate issue without integrator triage. Shared indexes, KiCad, requirements, purchase orders, fabrication, main merge and HV operation were not modified. See companion Chat B SOP proposal for non-blocking provisional workflow.
