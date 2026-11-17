# Chat B SYS-001D — direct-SYS HV controller primary-source screen (LM5155 vs LT3757A)

- Date: 2026-11-18 01:00 JST
- Role: Chat B wide research; **provisional, NO FORMAL CLAIM**
- Starting branch HEAD: `099243a18bcb02359dec782d17356e89c6f13713`
- Parent SYS-001 / HV-001B; related HV-004, PWR-001/002, BAT-001, HV-002C
- Review state: **PENDING REVIEW** for Chat C
- Result: **CONDITIONAL as controller candidates only; BLOCKED for 205V/16mA design adoption** (magnetics, loss, stress, temperature, OVP and pricing unqualified)
- Exclusions: Issue #2 MAX668 coupled-inductor topology and Issues #3/#5/#6 OVP timing/energy are separate research; no claimed ownership, no design-target or shared-index changes.

## 1. Startup and novelty

Read `docs/ai-workflow.md`, `docs/verification/handoff.md`, `docs/verification/open-issues.md`, `docs/verification/decisions.md`, `docs/tech-tree.yaml`, `docs/tech-tree.md`, and recent Chat B 17:02 lamp-envelope and 21:00 direct-SYS comparison reports; checked open GitHub Issues #1–#6 and zero open issues matching `label:role:wide-research`. No concurrency-safe formal Claim. This report adds *manufacturer-grounded specific controllers* and low-SYS screening, not a repeat of the 59.5% efficiency break-even already derived.

## 2. Manufacturer sources and claims

| Controller | Manufacturer evidence | Classification | Unproven applicability |
|---|---|---|---|
| **TI LM5155 / LM51551** | [TI LM5155 product](https://www.ti.com/product/LM5155), [TI SNVSB75E datasheet Rev.E Aug 2023](https://www.ti.com/lit/ds/symlink/lm5155.pdf), §8.3 recommended operating: VBIAS/VVCC minimum 2.97V when BIAS=VCC; TI states 3.5–45V conventional bias operation, 2.97–16V BIAS=VCC, and 1.5V power-stage input only when BIAS≥3.5V; boost/SEPIC/flyback supported; current-sense threshold 100mV ±7% and 1.5A MOSFET driver (product claims). | **GUARANTEED/RECOMMENDED operating bound** 2.97V only under BIAS=VCC topology; 100mV ±7% as product specification, not a guaranteed 205V converter output. | Actual BQ SYS minimum, BIAS=VCC wiring, external FET gate drive at low VCC, transformer, peak current, UVLO, FB/OVP and 205V output performance UNKNOWN. 1.5A is **gate driver peak**, not output or primary power current. Product table `Vout(max)=300V` does **not** qualify a 205V/16mA assembled flyback. |
| **ADI LT3757A** | [ADI product](https://www.analog.com/en/products/lt3757.html), [ADI LT3757/LT3757A datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/LT3757-3757A.pdf), 2.9–40V input, boost/flyback/SEPIC/inverting, external MOSFET, adjustable UVLO/soft-start and switching frequency; shutdown current <1µA stated. | **Manufacturer stated operating input range**; shutdown-current feature is an upper bound under its stated conditions, not the HV system's standby current. | Minimum *usable* MOSFET gate drive at 2.9–3.3V, FB accuracy/compensation, magnetics, switching stress and 205V/16mA continuous efficiency UNKNOWN. ADI demo DC1547B is 3.1–9V to 12V/1.5A boost, **not** a 205V flyback validation. |
| **Existing MAX668, LT8304-1** | Project `docs/hv-transformer-screen.md`, `docs/hv-architecture-decision.md`; MAX668 ordinary noncoupled boost rejected only for duty. | Existing *screen*, not repeated or superseded. | No selected 205V/16mA transformer or complete safety design. |

**Do not confuse a controller's low VIN spec with a demonstrated low-VIN high-voltage converter.** The two proposed controllers both have external MOSFET drive and no guaranteed end-to-end efficiency at this application point. Neither supplies independent HV safety isolation.

## 3. SYS-input lower-bound screening

Use `V_HV=205V`, `I_HV=16mA` (**ASSUMED design target**), `P_HV=3.28W`. Assume `eta_direct=0.60,0.70,0.80` (**ASSUMED, not measured**).

`P_direct_in=P_HV/eta_direct` = 5.467 / 4.686 / 4.100W. For a hypothetical `V_SYS=3.3V` (**ASSUMED**), corresponding *HV-stage-only average* input currents are 1.657 / 1.420 / 1.242A. At 3.0V: 1.822 / 1.562 / 1.367A. This excludes 5V logic, MCU, charger/BATFET losses and input ripple; the cell current may be higher. Controller operation at a quoted minimum VIN says nothing about those currents or thermal margin.

**Conditional headroom:** If actual SYS dips below 2.97V during load-step/USB-unplug/aged-cell conditions, the TI BIAS=VCC 2.97V recommended bound is violated; if below 2.9V, the ADI quoted input range is violated. The exact SYS floor is **UNKNOWN**. A programmable UVLO above those thresholds may force controlled HV shutdown rather than regulation; user-visible full-load availability at low battery must be specified. No arbitrary 3.0V operating cutoff is adopted.

**Peak-current counterexample (illustrative, not sizing):** For an ideal DCM flyback with triangular input magnetizing current, `P_in ≈ V_SYS*(I_pk/2)*D`, so `I_pk≈2*P_in/(V_SYS*D)`. At 3.3V, 70% direct efficiency and assumed D=.80, `I_pk≈3.55A`. At 3.0V, D=.80, `I_pk≈3.90A`. These are **conditional idealized DCM proxies**, not valid for arbitrary CCM operation, transformer reset, leakage or real controller waveforms. A transformer or FET rated from the ~1.4A average alone could fail. For the same illustrative 3.3V, 3.55A peak, 100kHz and D=.8, `L_p≈V_SYS*D/(I_pk*f)≈7.4µH` if current ramps from zero; check energy per cycle, core saturation and transformer ratio separately. These are not adopted magnetic values.

## 4. Alternative architectures and constraints

| Path | Distinct benefit | Primary gating risk |
|---|---|---|
| **BQ SYS → LM5155 flyback** plus SYS→5V logic | 2.97V conditional low-voltage controller option; current-mode, external FET | BIAS=VCC operating condition, MOS gate drive, qualified magnetics and minimum SYS, 205V feedback/OVP, WSON PCB thermal and procurement |
| **BQ SYS → LT3757A flyback** plus SYS→5V logic | 2.9V manufacturer input range, soft-start/UVLO, external MOSFET | Actual low-input gate drive, magnetics and efficiency, 205V regulation, cost/footprint and safety |
| **Existing SYS→TPS61023→5V→HV** | Existing draft, shared 5V logic, reduced HV controller input range | Two conversion stages, 5V boost thermal/startup and HV magnetics unproven |
| **BAT→HV direct** | Potential path-loss reduction | Bypasses BQ SYS management; additional battery cutoff, protection, reverse-feed and charging UX required; NOT equivalent to SYS→HV |
| **Higher USB input allowance / reduced USB display mode** | Could reduce need for cell supplementation | New USB-C/charger/eFuse validation or exact lamp/UI-current evidence and owner approval |

For both direct candidates, the unchanged USB-only constraint is decisive: BQ 500mA input limit at 5V is ≤2.49W at its 498mA upper corner, less than the **3.28W HV output alone**. Direct conversion cannot create the missing power. With battery assist, USB presence does not imply charging; signed `I_BAT` and DPPM state must be measured.

## 5. Thermal, failure and sourcing gates

- At assumed 70% direct efficiency, stage loss `P_loss=3.28*(1/.70-1)=1.406W` distributed among MOSFET, transformer copper/core, rectifier, snubber/clamp, sense, controller and PCB. It is **not** 1.406W entirely in the IC. At 60% it is 2.187W. No defensible junction temperature without per-part loss, layout, enclosure and ambient; protected cell thermal remains independent.
- MOSFET VDS and diode VRRM must be calculated from **actual turns ratio, leakage overshoot and topology**, not guessed from output voltage. Independently bound HV normal excursion, OVP comparator trip spread, shutdown tail energy, discharge and power-loss state (existing Issue #6). Do not use LM5155 integrated OVP as proof of independent protection.
- Check minimum cell and BQ SYS voltage in all USB/charge/BAT assist states, including charger DPPM, protector trip and battery absent. Ensure HV_EN defaults off and independent hardware stop remains effective when MCU/5V disappears.
- **Procurement UNKNOWN:** no live distributor stock, JPY price, transformer lead time or actual board-space/thermal fit verified. A low-VIN controller is not a purchasable qualified HV stage; check distributor stock, WSON vs MSOP assembly, MOS/transformer/diode/OVP costs before selection. Short January purchasing window favors a qualified transformer + controller *pair* over controller-only attractiveness.

## 6. Independent review and bounded next tasks

1. **Chat C:** verify TI §8.3 BIAS=VCC condition, ADI 2.9V operating claims, distinguish driver 1.5A from primary load current, audit DCM illustrative equation and no inference of 205V feasibility.
2. **HV-001B / Chat B next:** search manufacturer reference designs for a *matched* low-VIN (≤3.0V conditional) controller + stocked transformer, with Lp, ratio, Isat, DCR, leakage, frequency, diode/FET stress and continuous 205V/16mA loss; reject or mark UNKNOWN if no primary proof. No repetition of MAX668 coupled topology Issue #2.
3. **SYS-001 / Work:** set the required minimum SYS input under battery-assisted, low-cell and unplug conditions before choosing a direct controller. Distinguish low-battery graceful HV shutdown from guaranteed full-load operation.
4. **PWR-002 / Chat A:** characterize BQ SYS and BATFET losses and net battery current in USB 450–498mA mode, at actual protected-cell voltage and NTC conditions.
5. **HV-004 / Chat B:** verify exact lamp part numbers and actual gauge simultaneous-lighting policy before relaxing any load design target.
6. **BOM-001 / Work:** check actual sourcing and prices of both controller/transformer pairs and complete safety circuitry; no pricing or stock conclusion in this screen.

## 7. SOP note and handoff

Existing [Chat B provisional workflow proposal](2026-11-17-1403-JST-chatb-provisional-workflow-sop-proposal.md) remains **PENDING REVIEW**. Canonical `docs/ai-workflow.md` still lacks the owner's non-blocking fallback; integrator should merge the proposal with concurrent changes. Do not edit shared indexes from this worker.

**PENDING REVIEW**. No formal Claim, no design adoption, no hardware tests, no purchases, no PCB manufacturing, no main merge. New candidate discovery should be tracked under SYS-001 / HV-001B, not treated as completed power-stage design.
