# Chat B SYS-001E — LT3757A flyback magnetics evidence and feasibility boundary

- Date: 2026-11-18 05:03 JST
- Role: Chat B wide research, **provisional; NO FORMAL CLAIM**
- Parent: SYS-001 / HV-001 / PWR-001 / BAT-001, linked to GitHub Issue #4
- Start HEAD: `86697edb11c874eab5bc1bdd66987cef0ff4d2c4`
- Status: **PENDING REVIEW** for Chat C; **CONDITIONAL** for controller comparison; **BLOCKED** for 205V/16mA hardware qualification, stock/price and safe operation
- Goal: identify a distinct primary-source risk/constraint for the already screened LT3757A low-SYS-input direct flyback, rather than repeat its 2.9V rating or previous 59.5% efficiency comparison.
- Excluded: MAX668 coupled-inductor Issue #2; OVP Issues #3/#5/#6; actual HV work, KiCad, procurement, fabrication, requirement changes, main merge.

## 1. Startup and coordination

Read `docs/ai-workflow.md`, `docs/verification/handoff.md`, `docs/verification/open-issues.md`, `docs/verification/decisions.md`, `docs/tech-tree.yaml`, `docs/tech-tree.md`, and recent Chat B SYS-001C/001D reports. Searched open GitHub Issues #1–#6; no eligible `role:wide-research` labeled issue or verified atomic Claim. Therefore this is a separate provisional, append-only report. Shared registers remain integrator-owned. The owner's non-blocking fallback proposal is in `docs/verification/2026-11-17-1403-JST-chatb-provisional-workflow-sop-proposal.md`; canonical SOP remains unmodified.

## 2. New evidence: matching controller and magnetics matters more than minimum VIN

**Primary manufacturer source:** ADI LT3757/LT3757A datasheet, [ADI PDF Rev.G](https://www.analog.com/media/en/technical-documentation/data-sheets/lt3757-3757a.pdf), *Applications Information — Flyback Converter: Transformer Design for Discontinuous Mode Operation*. ADI explicitly treats `D_MAX`, secondary conduction interval `D2`, and dead interval `D3`; `D2=1-D_MAX-D3`, and recommends `D3MIN≥10%` for a DCM design. Manufacturer formula: `I_LP,avg,on = P_OUT/(D_MAX*V_INMIN*eta)` (ADI labels maximum average primary current; carefully interpret averaging interval before sizing peak). **DESIGN METHOD, not a guaranteed operating point.** ADI also specifies an internal 7.2V gate-drive supply architecture and a 2.9V controller input operating range [ADI product page](https://www.analog.com/en/products/lt3757.html). Neither implies that a particular 205V stage will start and regulate at 2.9V.

**Independent counterexample, NOT a qualified manufacturer design:** [ADI EngineerZone 2019-09-30, verified reply thread](https://ez.analog.com/power/f/q-a/116852/lt3757-flyback-converter): a user attempted LT3757 flyback at **5V→200V, <10mA**, reported that the reference transformer `DCT15EFD-U44S003` was obsolete, and a replacement `ATB322524-0110-T000` overheated or failed when driven at **1MHz**. This is a **USER-REPORTED FAILURE** and does not prove the alternative transformer universally unsuitable; it is a relevant counterexample to inferring that similar turns ratio or an ADI reference circuit automatically qualifies a replacement at 205V/16mA. It also does not prove either part's 2026 availability. Another [ADI EngineerZone 2022-01-20 thread](https://ez.analog.com/power/f/q-a/554272/lt3757a-in-flyback-configuration-oscillation-of-output-voltage) reports flyback feedback oscillation despite an LTspice model; again anecdotal, not a manufacturer performance bound. Review the primary ADI datasheet and actual magnetics datasheet before design adoption.

**TI comparison:** [TI LM5155 product and datasheet](https://www.ti.com/product/LM5155), [LM5155 Rev.E PDF](https://www.ti.com/lit/ds/symlink/lm5155.pdf): 2.97V start under **BIAS=VCC** condition; otherwise 3.5V bias condition; flyback supported, current-mode controller. The published `1.5A` is gate-driver peak capability, not allowable primary current. Its broad advertised 300V output is not a 205V/16mA reference design. No manufacturer-qualified low-SYS transformer+controller+205V/16mA pair was located in this bounded search. The absence is a search result, not a claim none exists.

## 3. DCM envelope and numerical falsification test

**ASSUMED/TARGET:** `V_OUT=205V`, `I_OUT=16mA`, `P_OUT=3.28W`; hypothetical `V_SYS,min=3.0V` and `eta=0.70`; `D_MAX=0.65`, `D3=0.10`, `f=200kHz` chosen only for a transparent sensitivity example. These are **not** selected operating points, a recommended switching frequency, or a proven SYS floor.

For ideal DCM with triangular primary current starting at zero, average input current over the entire period is `I_IN=P_OUT/(eta*V_IN)=1.562A`. On-time average primary current is `I_LP,on,avg=I_IN/D=2.402A`, so triangular peak `I_PK≈2*I_IN/D=4.806A`. Primary inductance for this assumed ramp is `L_P=V_IN*D/(f*I_PK)=2.03µH`. Secondary conduction interval `D2=1-0.65-0.10=0.25`; ideal secondary peak `I_S,PK≈2*I_OUT/D2=0.128A`. A rough ideal turns ratio from volt-second reset is `N_S/N_P≈(V_OUT+V_D)*D2/(V_IN*D)`; neglecting diode drop gives `≈26.3`. This ratio is *not* a selected transformer and ignores leakage, parasitic capacitance, diode recovery, saturation and actual current-limit waveforms. The 4.806A peak is **not** guaranteed or a safe rating; actual current can be higher with loss/line changes and startup. The exercise shows why screening solely for 2.9V controller VIN and 1.56A average current is insufficient.

Cross-check energy: `0.5*L_P*I_PK²*f≈4.69W` delivered to the ideal magnetizing path, matching `P_OUT/eta≈4.69W` only as an **input-energy bookkeeping proxy**. Actual output energy per cycle, core/copper and switch/rectifier loss must be modeled coherently. For real DCM with transformer ratio `n`, require `D2>0`, `D3≥0.10`, `V_DS,peak≈V_IN+(V_OUT+V_D)/n+V_leak,spike`, `V_RRM≈V_OUT+n*V_IN+V_ringing`, and `I_PK<I_sat,min(T)` with derating. These are simplified topology-specific approximations; independent OVP must separately enforce the HV5524 recommended 220V ceiling.

**Critical constraint:** an assumed `L_P≈2µH`, `n≈26`, `I_PK≈4.8A` at 200kHz is materially different from prior screened 40µH / 1:5 or 1:10 magnetics. Do not reuse those transformer candidates by ratio alone; DCM reset and current limits must be recalculated from the actual selected component. Changing `D`, `D3`, `f`, and `eta` can move these values substantially; no specific component is endorsed.

## 4. Mode and heat implications

The existing 500mA-configured BQ25185 input current limit of 450/475/498mA at 5V [TI BQ25185 datasheet](https://www.ti.com/lit/ds/symlink/bq25185.pdf) provides at most 2.49W at the 498mA corner, below the **3.28W HV output alone**. A direct 1S/SYS flyback cannot change USB-only 16mA **NO-GO**. When USB and BAT are connected, BQ DPPM may reduce charging and BAT may supplement SYS; the cell may be discharging. Require signed I_BAT measurement and battery thermal constraints before claiming simultaneous charging. At the hypothetical 3V SYS and 70% direct-HV efficiency, HV stage alone draws 4.686W / 1.562A average, plus logic and charger-path loss; pulse currents and cell current are higher.

The hypothetical stage conversion loss is `3.28*(1/0.7-1)=1.406W` **ASSUMED**, distributed among transformer core/copper, FET, rectifier, snubber, sense, controller and PCB. The 205V output power is itself dissipated in lamp resistors/lamps/driver, largely inside the sealed PETG housing. No IC junction or cell temperature can be calculated from total stage loss without component partition, layout thermal resistance and actual enclosure ambient. A 1MHz magnetic failure report is not a substitute for frequency-dependent core-loss curves and copper AC loss.

## 5. Options and decision gates

| Alternative | Positive | Disqualifier / needed evidence |
|---|---|---|
| LT3757A direct SYS→HV flyback | 2.9V manufacturer input range; ADI detailed DCM design method | Actual low-SYS startup, qualified Lp/ratio/Isat/leakage/DCR/core-loss, peak current, feedback stability, switch/diode stresses, price and 205V/16mA thermal |
| LM5155 direct SYS→HV flyback | 2.97V start condition with BIAS=VCC; manufacturer flyback support | BIAS/VCC configuration, low-SYS gate-drive, magnetics, compensation, peak current and thermal |
| Existing SYS→TPS61023→5V→HV | Existing draft and shared 5V logic | TPS61023 low-cell full load/startup/thermal, HV magnetic qualification and OVP |
| Lower-current/limited-USB display | Could reduce typical demand | Exact IN-12B/neon source part and simultaneous pattern, ignition/maintaining voltage, resistor heat, user approval for requirement changes |
| Higher USB source/input limit | Could reduce battery assist | USB-C CC/source compatibility, BQ charger/eFuse, 21700 cell thermal, explicit owner approval |

No distributor price, stock, lead time or production transformer part number was verified in this run: **UNKNOWN**. The 2019 obsolete-part statement is historical only.

## 6. Next bounded tasks and review request

1. **Chat C:** audit DCM equations, especially interpretation of on-time average current and `D3≥0.10`, and whether the proposed 2µH/26:1/4.8A *hypothetical* point is physically plausible; ensure it is not turned into a BOM.
2. **Chat B next:** search 2026 manufacturer magnetics datasheets for a *concrete* Lp/ratio/Isat/core-loss candidate at 3.0–3.3V and 205V/16mA; include actual supplier stock, JPY price and lead time, or report explicitly that no qualified off-the-shelf part was found. Compare an easier 5V→HV case to determine if SYS-direct cost/time is justified.
3. **Chat A / PWR-002:** obtain minimum SYS under actual BQ battery-assist and low-cell conditions and full power path, plus USB unplug transient and 5V logic load. Without a SYS minimum, 2.9/2.97V controller thresholds are not adoption evidence.
4. **Work/integrator:** review adoption gates and integrate only independently checked findings. No shared index edits by Chat B.

**PENDING REVIEW**, no formal Claim, no new component selected, no HV operation or PCB manufacturing authorized.
