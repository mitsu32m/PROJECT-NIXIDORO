# Chat B SYS-001C — Direct SYS→HV versus SYS→5V→HV conversion-chain screen

- Date: 2026-11-17 21:00 JST (scheduled research)
- Role: Chat B, wide research, **provisional/no formal Claim**
- Parent: SYS-001 / HV-001 / PWR-001 / PWR-002; GitHub Issue #4 for handoff
- Starting working branch HEAD: `22ebaafd1ca079ed864e73d37c842b4456c734e5`
- Status: **PENDING REVIEW** for Chat C; **CONDITIONAL** architecture sensitivity only; **BLOCKED** for implementation and part adoption
- Question: Does bypassing the intermediate 5V conversion improve *system* power enough to justify a new 1S/SYS-input HV stage, without conflating USB-only supply with battery assistance?
- Exit: correct break-even equation and current/thermal sensitivity, independent of MAX668 coupled-boost Issue #2 and OVP Issue #6; explicit primary-source qualification gates.
- Forbidden: requirements changes, KiCad edits, purchasing, PCB fabrication, HV operation, main merge.

## Startup and overlap

Read the six mandatory SOP/handoff/issues/decisions/tech-tree documents; 2026-11-17 20:03 Chat A OVP tail-energy report and open Issues #1–#6; 17:02 Chat B lamp-current report, 14:03 SYS-001 report, `docs/hv-transformer-screen.md` and `docs/requirements.md`. Existing Chat A investigates MAX668 coupled-inductor and OVP, so **this report does not re-derive their switch stress or propose OVP thresholds**. No concurrency-safe Claim was verified, no exclusive ownership claimed. This report extends the earlier list of alternatives with a *system-level* efficiency threshold and low-cell supply implications.

## Source and input classification

- **TI BQ25185**, datasheet Rev.B Aug 2026, https://www.ti.com/lit/ds/symlink/bq25185.pdf : configured USB input limit 450mA min / 475mA typical / 498mA max at specified 5V conditions; DPPM and battery supplementation. **GUARANTEED / TYPICAL** per individual table entries. Actual SYS voltage and net BAT current under load **UNKNOWN**.
- **TI TPS61023**, https://www.ti.com/lit/ds/symlink/tps61023.pdf : low-input boost with specified startup and valley current limit under datasheet conditions. The previously used 85% conversion efficiency is **ASSUMED**, not guaranteed at this load and PCB.
- **ADI LT8304**, https://www.analog.com/media/en/technical-documentation/data-sheets/lt8304.pdf : primary-side-regulated flyback family, illustrative 4V→200V application in repository transformer screen. This is a **manufacturer application example**, not a guarantee of 3.3V→205V/16mA or an endorsement of direct SYS use. Its operating range, current-limit corners, minimum supply/startup, and exact variant must be checked before any circuit adoption.
- **Würth 750315839** https://www.we-online.com/components/products/datasheet/750315839.pdf and **Sumida 13324-T086** https://media.digikey.com/pdf/Data%20Sheets/Sumida%20PDFs/13324-T086_Spec.pdf : magnetics previously screened for 5V input; none proven for 205V/16mA at minimum SYS. A 4V manufacturer example cannot be extrapolated to a 3.0–3.3V low-cell input without primary peak, frequency, loss and temperature checks.
- **Microchip HV5524** https://ww1.microchip.com/downloads/aemDocuments/documents/APID/ProductDocuments/DataSheets/HV5524-32-Channel-Serial-to-Parallel-Converter-Data-Sheet-DS20006850.pdf : recommended HV maximum 220V; direct conversion does **not** remove independent OVP/hard-off/discharge requirements.
- 205V, 16mA continuous **TARGET, UNVERIFIED**; `eta_HV=.70`, `eta_5=.85`, `P_5logic=.50W`, `P_SYSother=.50W`, direct-HV `eta_direct=.60/.70/.80`: **ASSUMED** scenario parameters. Actual 5V-only loads, HV idle power, battery cell/NTC and thermal resistance **UNKNOWN**. No new prices/availability checked this run; BOM comparison **UNKNOWN**.

## 1. Correct topology comparison: 5V logic cannot disappear

The proposed baseline uses BQ SYS→TPS61023 5V→HV plus some 5V logic. A direct SYS→HV stage **does not eliminate the 5V rail** while 5V logic still needs it. Hence compare:

`P_SYS,baseline = (P_HV/eta_HV + P_5logic)/eta_5 + P_SYSother`.

`P_SYS,direct = P_HV/eta_direct + P_5logic/eta_5 + P_SYSother`.

`Delta P_SYS = P_SYS,baseline - P_SYS,direct = P_HV*(1/(eta_HV*eta_5) - 1/eta_direct)`.

Thus the direct path only lowers SYS consumption when `eta_direct > eta_HV*eta_5`. For assumed .70*.85, **break-even = 59.5%**. This is an algebraic result conditional on equal HV output and identical logic load; it does not include different control power, converter quiescent load, battery path efficiency, start-up, magnetic and thermal changes. A direct stage with worse than 59.5% efficiency would **increase** SYS power despite deleting a conversion stage.

| HV load | P_HV | Baseline SYS (70% HV,85% 5V) | Direct SYS 60% | Direct SYS 70% | Direct SYS 80% |
|---|---:|---:|---:|---:|---:|
| 4mA | 0.820W | 2.466W | 2.455W | 2.260W | 2.113W |
| 8mA | 1.640W | 3.845W | 3.822W | 3.432W | 3.139W |
| 16mA | 3.280W | 6.601W | 6.555W | 5.775W | 5.189W |

Table is **ASSUMED sensitivity**, not guaranteed efficiency, runtime or temperature. At 16mA, 70% direct would save ~0.826W SYS; 80% direct ~1.412W; 60% direct saves only ~0.046W. At 4mA, savings are smaller and could be erased by higher quiescent draw or new hardware.

**IMPORTANT: system heat.** The saved power is principally reduced conversion loss, not reduced 205V×I load dissipation. For 16mA at 70% direct, direct HV-stage loss = `3.28*(1/.70-1)=1.406W`; 5V logic conversion loss = `.50*(1/.85-1)=.088W`. Baseline HV loss 1.406W plus TPS61023 loss `(3.28/.70+.50)*(1/.85-1)=.915W`; the 0.826W reduction matches the comparison. Direct stage may shift loss to magnetics near the protected cell and **does not prove** improved cell temperature in sealed PETG.

## 2. Low-cell / battery assistance and USB modes

For a first-pass 3.3V **ASSUMED SYS voltage** (not a guarantee or cell voltage), 16mA baseline `I_SYS≈6.601/3.3=2.00A`, direct at 70% `≈5.775/3.3=1.75A`, direct at 80% `≈5.189/3.3=1.57A`. These are SYS currents **before** charger BATFET/cell protection/contact losses. A real direct HV stage draws pulsed input current; peak magnetizing current can greatly exceed the average and needs current-limit/saturation analysis.

For a 5V USB input with the existing 500mA BQ configuration, even the **best-case** 498mA limit gives 2.49W before losses. Since 205V×16mA=3.28W, **both baseline and direct topologies are NO-GO for USB-only 16mA**. Eliminating the intermediate 5V converter does not change conservation of energy. A larger adapter alone does not bypass BQ's configured input limit.

When USB and battery are both connected, actual SYS input may be split between USB and BAT. Battery supplementation is not charging; define cell discharge positive and require actual signed battery-current measurement to prove charge/discharge. At a *hypothetical lossless* 2.25W USB contribution to SYS, 16mA baseline needs ≥4.351W from battery/path and 70%-direct needs ≥3.525W. At illustrative 3.6V this means ≥1.21A and ≥0.98A respectively **before losses**. These are **optimistic lower-bound arithmetic**, not actual BQ25185 SYS operating points. Do not assume DPPM enables any particular continuous assist current or net charging.

## 3. Hidden architecture costs and failure modes

1. **Input range and startup:** BQ SYS is not an ideal cell source; under DPPM, battery assist and brownout it varies. A direct SYS→HV controller must start and regulate at the *measured worst SYS*, not merely a 4V typical application point. Verify manufacturer guaranteed UVLO/startup, minimum load, peak switch current, transformer saturation, diode recovery and regulation at low cell.
2. **Retained 5V rail:** logic and level shifters still need 5V. Retaining TPS61023 at reduced load may change its efficiency and light-load behavior; the constant 85% scenario is not a true low-load model. A separate 3V3-only control redesign is a different scope and needs pin-level verification.
3. **Power-path location:** sourcing direct HV from **BQ SYS** retains input/battery power-path management. Sourcing directly from **BAT** instead bypasses the SYS path and may drain the cell while the system reports USB operation; requires independent cell undervoltage, protection, reverse feed, shipping/off-state and charging-mode controls. **Do not silently treat SYS→HV and BAT→HV as interchangeable.**
4. **USB source disconnect:** test modeled transitions USB→BAT, BAT→USB, battery absent, BAT protector trip and charger DPPM; guarantee HV hard-off on undervoltage or control reset. A controller EN GPIO or HV5524 BL is not an independent safety cut.
5. **Voltage safety:** existing OVP Issue #6 shows very narrow 220V margin. Direct topology does not change the HV5524 recommended limit, stored charge, or need for independent OVP, fault latch, physical isolation and discharge.
6. **Thermal and procurement:** qualification requires MOSFET conduction/switching loss, transformer core/copper/leakage clamp loss, diode loss, PCB heat, PETG cell temperature, actual footprint, cost and stock. No verified full 205V/16mA direct design exists in repository.

## 4. Alternatives and decision matrix

| Architecture | Potential benefit | Disqualifying uncertainty / review gate |
|---|---|---|
| **Baseline SYS→5V→HV** | Existing PWR draft and shared 5V supply | TPS61023 5V full-load startup/thermal and HV magnetics unproven |
| **SYS→HV direct + SYS→5V logic** | Save conversion loss if eta_direct > eta_HV*eta_5 | Qualified minimum-SYS controller, magnetics, startup, peak current, new HV fault-stop and BOM |
| **BAT→HV direct + SYS→5V logic** | May reduce one power-path drop | Bypasses BQ SYS control; cell cutoff, charging semantics and reverse-feed fault require new architecture review |
| **Higher USB input budget** | May permit more USB-only load | Requires USB-C CC/source agreement, BQ/eFuse reprogramming and heat review; human approval |
| **Mode-limited USB-only display** | May preserve existing power path and BOM | Needs exact lamp current/strike/brightness and mode overlap evidence; full 16mA USB-only still impossible |
| **Prequalified HV module** | Potentially reduce design time | No manufacturer-confirmed 205V/16mA 1S/5V module and cost/thermal fit established |

**Comparative recommendation (not design approval):** Keep the baseline as the control architecture while requesting a *bounded* manufacturer-documented direct-SYS flyback candidate. Do not switch architectures based on a theoretical 0.8W gain; the 1S low-voltage current and unproven magnetic/OVP may outweigh it before January procurement. First settle selected lamp current and UI modes, then evaluate whether direct conversion remains materially beneficial at actual average/peak load.

## 5. Independent review / next tasks

- **Chat C:** independently verify the 59.5% break-even and tables, ensure direct-SYS and direct-BAT distinctions, and flag missing converter idle power and variable 5V efficiency. Validate no unearned claim of 205V/16mA.
- **HV-001B / wide research:** identify a genuine manufacturer-qualified SYS-input HV flyback control IC + available transformer with guaranteed minimum VIN/startup, current-limit corner and 205V/16mA continuous proof or explicitly reject as unqualified. Compare price/availability including OVP/bleeder, not merely controller cost.
- **SYS-001 / Work:** decide whether low-power gauge-only USB mode should be an optional product requirement after HV-004 evidence. Maintain current 16mA stress target pending owner approval.
- **PWR-002 / Chat A:** obtain mode-specific BQ25185 input/SYS/BAT currents and junction loss, especially low-cell and USB unplug transition. Do not infer net charging from USB presence.
- **BAT-001:** choose actual protected cell and thermistor before interpreting battery current or enclosure heat.
- **HV-002C:** remain with existing Issue #6; direct HV requires same independent OVP/tail-energy constraints.

## 6. Handoff

**PENDING REVIEW**, no formal Claim, no accepted architecture, no component purchase/PCB/HV operation. Report is an append-only independent file. Integrator owns edits to `docs/ai-workflow.md`, shared issue/decision registers, handoff and tech-tree indexes. The earlier [Chat B SOP proposal](2026-11-17-1403-JST-chatb-provisional-workflow-sop-proposal.md) remains available for adoption; do not overwrite the shared SOP during concurrent research.
