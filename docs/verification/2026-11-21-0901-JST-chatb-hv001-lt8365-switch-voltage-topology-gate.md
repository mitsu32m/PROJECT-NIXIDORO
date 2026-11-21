# Chat B — HV-001 / SYS-001: LT8365 150V switch topology gate
Date: 2026-11-21 09:01 JST
Status: **PENDING REVIEW** (Chat C); adoption **BLOCKED**
Role: Chat B provisional wide research; **NO FORMAL CLAIM**
Branch: `codex/reva-integrated-prototype-review`
Starting HEAD SHA: **UNKNOWN** — this connector exposes branch file content but no exact branch commit SHA; never substitute a blob SHA or unrelated repository commit.
Related: #7 PROTO-001; #4 SYS-001A; Chat A #2 owns deep HV topology.

## Bounded question
Does LT8365's 150V integrated switch permit a conventional one-inductor, one-diode direct 5V→205V boost? If not, what extra proof is required for the ADI DC2838A charge-pump reference?

**Result: NO-GO for direct single-stage conventional boost with LT8365; charge-pump variant CONDITIONAL for further research only, not adoption.**

## Manufacturer evidence (retrieved 2026-11-21)
- ADI LT8365 product and datasheet Rev.A (2019-07-30): 2.8–60V VIN, integrated 150V / 1.5A switch, 100–500kHz, recommended for new designs. https://www.analog.com/en/products/lt8365.html ; https://www.analog.com/media/en/technical-documentation/data-sheets/LT8365.pdf
- ADI DC2838A controlled reference (schematic dated 2020-06-18, demo manual Rev.0 2020-03-02): 9–30V VIN, +250V/10mA, 400kHz; optional third charge-pump stage. https://www.analog.com/en/resources/evaluation-hardware-and-software/evaluation-boards-kits/dc2838a.html
- ADI DC2840A: 9–30V, **negative** -250V/10mA, not a positive rail substitute. https://www.analog.com/en/resources/evaluation-hardware-and-software/evaluation-boards-kits/dc2840a.html

## Circuit identity and voltage-stress derivation
For a **conventional nonisolated single-inductor boost** with output diode from SW to VOUT and low-side switch to ground, ideal steady off-state `V_SW≈V_OUT+V_D`. With NIXIDORO `V_OUT=205V`, even `V_D=0` gives `V_SW≥205V >150V`. Nominal excess `205−150=55V`, or 36.7% above 150V. Switching ringing worsens the stress. Therefore this direct topology cannot use LT8365's integrated 150V switch for 205V. This does **not** reject the ADI charge-pump/multiplier reference: its switch node may be lower than output, depending on actual topology. A 150V switch rating is not a 150V output ceiling for all circuits.

The **ideal** duty for an ordinary 5→205V boost would be `D=1−5/205=0.97561`, or 97.56%; for 3→205V, `D=98.54%`. These figures are ideal and are NOT proof of an LT8365 duty-cycle limit. The switch voltage violation alone excludes the direct conventional topology.

For a two-stage charge pump, approximate equal sharing `Vstage≈205/2=102.5V` is **only a hypothetical illustration**, not a verified DC2838A switch-node voltage, nor a safe capacitor/diode rating. Actual switch stress includes topology-specific clamp and ringing, diode forward/recovery, capacitor bias and startup/unbalanced voltages. The controlled schematic must be traced before any rating claim.

## SYS-001 power contract
Full target `205V×0.016A=3.28W`. DC2838A `250V×0.010A=2.50W`; target demands 31.2% more power and 60% more output current. At **ASSUMED** 75%/80% HV efficiency from 5V, input averages `3.28/(5×0.75)=0.8747A` / `0.8200A`. At **ASSUMED** 3.0V direct SYS, `1.4578A` / `1.3667A`. Neither is a measured IC peak switch current. USB 5V×0.5A=2.5W cannot supply 3.28W even at 100% efficiency; battery supplement and true net charging must be distinguished. Charging at a programmed rate cannot be presumed while the HV load operates.

With **ASSUMED** HV efficiencies, total HV-stage loss is 1.093W (75%) or 0.820W (80%). In the charge-pump variant, losses must be apportioned among internal switch, inductor, each diode, each flying capacitor ESR, control IC and PCB. Junction and enclosed-cell temperature remain **UNKNOWN**. For any 150V-rated SW, the worst-case switch voltage plus overshoot must remain below the **actual manufacturer absolute maximum/operating limit**, with explicit margin; a marketing rating is not a design margin.

## Comparative disposition and next evidence
| Candidate | Status | Blocking evidence |
|---|---|---|
| LT8365 direct conventional boost to 205V | **NO-GO** for this circuit | 205V off-state >150V switch |
| LT8365 DC2838A positive charge-pump architecture | **CONDITIONAL research** | Need actual schematic traced, 5V and 16mA redesign, inductor/diode/capacitor current and voltage stress, loss, startup, 220V independent OVP |
| LT3757 + original TDK DCT15EFD-U44S003 | **SOURCING BLOCKED** | Original magnetics obsolete in prior supplier evidence; alternate requires thermal/electrical qualification |
| MAX668 coupled-inductor or direct-SYS flyback | **OPEN** | Real magnetics, winding, saturation, startup, switch stresses and procurement unqualified |

**Procurement**: LT8365 marked recommended for new designs by ADI, but exact domestic 1-piece stock, unit price, shipping and candidate inductor/flying capacitors are **UNKNOWN** in this run. No invented availability claims.

**Faults**: DC2838A open-load, no-load, load removal, VIN brownout, battery cut, MCU reset, pump-capacitor imbalance, short, diode fault, independent hard-stop and discharge must be checked. HV5524 recommended 220V is not a permissible fault target; independent OVP plus tail-energy budget remain required.

## Independent-review request to Chat C
1. Verify the conventional boost SW=VOUT+VD argument and that it does **not** misclassify the ADI charge-pump topology.
2. Inspect DC2838A actual schematic, count charge-pump stages and calculate worst SW, diode, flying capacitor and inductor currents at 5V/205V/16mA; report unsupported bounds as UNKNOWN.
3. Verify mode-specific 500mA USB versus BAT supplement and whether any 5V low-VIN operating proof exists.
4. Do not promote any part/topology to adoption without Work integration.

**Workflow proposal** (do not edit shared SOP): Add a topology-identity gate to high-voltage candidate research: explicitly distinguish SW-node rating from VOUT, draw switch-off conduction path and multiplier stages, record guaranteed VIN/output operating range, and require stage-specific fault stresses before sourcing claims.

No purchase, PCB fabrication, HV energization, main merge, requirements change, shared index edit or schedule change.
