# Chat B — HV-001 / SYS-001: DC2838A controlled schematic and 5V input current gate
Date: 2026-11-21 13:04 JST
Review: **PENDING REVIEW** (Chat C); hardware adoption **BLOCKED**
Role: Chat B, provisional wide research, **NO FORMAL CLAIM**
Branch: `codex/reva-integrated-prototype-review`
Starting branch HEAD: **UNKNOWN**. GitHub branch search confirmed branch exists, but connector search returns only branch name, not commit SHA. Repository-wide commit search is NOT a substitute for branch HEAD.
Related issues: #10 (primary), #7, #4. Deep topology design remains Chat A #2.

## Bounded question and outcome
Trace the **actual manufacturer-controlled schematic** of LT8365 demo DC2838A, identify its two-stage pump and actual component references, then calculate an explicitly conditional 5V/205V/16mA input-current screen. No parts adoption or electrical safety conclusion.

**Result: CONDITIONAL research.** This is not a generic two-boost cascade: the drawing has a single 10uH switch inductor, D1 and pump D3/D4, flying capacitor C2, storage capacitors C14/C15, and an optional third stage. It does not demonstrate 5V input or 16mA output.

## Manufacturer primary evidence, retrieved 2026-11-21
1. ADI DC2838A evaluation page: 9–30V input, +250V/10mA, 400kHz, optional third charge-pump stage. https://www.analog.com/en/resources/evaluation-hardware-and-software/evaluation-boards-kits/dc2838a.html
2. ADI DC2838A controlled schematic (download link on above page; schematic number 710-DC2838A_REV02, drawing footer dated 2019-07-15; website lists publication 2020-06-18): https://www.analog.com/media/en/technical-documentation/eval-board-schematic/710-dc2838a_rev02_pca_schematic.pdf
3. ADI LT8365 datasheet: https://www.analog.com/media/en/technical-documentation/data-sheets/LT8365.pdf

Schematic visual tracing (not merely text extraction):
- U1 LT8365-MSE, SW1/SW2 common switch node, L1 = 10uH Würth 74437324100; input EMI L2=0.47uH Würth 74479876147; nominal 400kHz R7=107k.
- Main rectifier D1 DFLS1150 feeds NET2/C14 (0.22uF 200V) to GND.
- C2 0.1uF 200V couples SW node to NET1; D3 DFLS1150 + R10 20ohm connects NET1 to NET2; D4 DFLS1150 connects NET1 to NET2/NET3 output chain. C15 0.22uF 200V sits from NET2 to NET3. R14=0ohm and R12=47ohm connect NET3 to output, C17=1000pF 500V to GND.
- Optional C3/D5/D6/C16 third-stage network is marked OPT; not installed by default.
- Schematic notes all ordinary resistors/capacitors have default package size unless specified. Exact current/temperature/ripple ratings and alternate 205V divider are not qualified.

**Important topology distinction:** The base circuit is a boost plus charge-pump multiplier, not conventional single diode SW→205V boost. Thus 150V internal switch rating does not alone rule it out. However actual SW, NET1, NET2 and NET3 worst-case waveforms, cap charging imbalance, diode reverse stresses, switching ringing and open-load overshoot remain UNKNOWN. The manufacturer demonstration is for 9–30V and 2.5W, not the requested 5V and 3.28W.

## SYS-001 arithmetic: guaranteed identities vs assumptions
Target Pout = 205V × 0.016A = **3.28W**. USB 5V × 0.500A = **2.50W ideal upper bound**, insufficient before losses. At assumed HV efficiency eta=0.80, 0.75, required 5V input current = Pout/(5 eta) = **0.820A, 0.8747A**. At assumed 4.5V stage input = **0.9111A, 0.9719A**. At assumed 3V direct input = **1.3667A, 1.4578A**. These are average source currents, **not** verified LT8365 switch currents; BQ charger path/USB input limit and 5V-stage loss further reduce supply margin.

For a *hypothetical* CCM boost base node Vbase=102.5V (equal-voltage-share illustration ONLY; not actual DC2838A NET2 voltage), ideal D=1−Vin/Vbase. Using L1=10uH, f=400kHz, triangular ripple ΔIL=Vin·D/(L·f):
- Vin=5V: D=0.95122, ΔIL=1.189A. With eta=80%/75%, Iavg=0.820/0.8747A, illustrative Ipeak≈1.4146/1.4693A.
- Vin=4.5V: D=0.95610, ΔIL=1.0756A. Iavg=0.9111/0.9719A; illustrative Ipeak≈1.449/1.510A.
- Vin=3V: D=0.97073, ΔIL=0.7280A. Iavg=1.3667/1.4578A; illustrative Ipeak≈1.731/1.822A.

**DO NOT interpret this as a working LT8365 model.** DC2838A charge-pump currents are pulsed; D and Vbase are not measured, CCM may fail, switching current may differ from input current, 1.5A headline switch value is not established as guaranteed cycle-by-cycle minimum or safe continuous value, and actual current limit/duty/thermal behavior requires datasheet corners and circuit simulation. These numbers are a sensitivity screen exposing potential narrow/negative peak-current headroom, not a device pass/fail proof.

## Thermal, fault, sourcing and decisions
At eta=75% or 80%, HV-stage losses are 1.093W or 0.820W **ASSUMED**, not a temperature guarantee. Need partition into U1 switch, L1 DCR/core, D1/D3/D4, C2/C14/C15 ESR, R10 and R12. R12 47ohm carries load current on average, yielding a **lower-bound DC conduction** Iout²R≈0.0120W; pulsed RMS and actual capacitor ripple can raise losses. R10 pulse loss not bounded. C14/C15 are 200V parts; cannot infer safe voltage from 205V output alone without NET2/NET3 and transients. C17=1nF/500V is not evidence that total HV output capacitance meets SYS-002 OVP/startup/discharge requirements.

Failure review needed: open load, C2 short/open, D3/D4 short/open, C14/C15 loss, output short, low VIN startup, EN brownout, independent OVP trip and residual energy, hard-stop/discharge, HV5524 below 220V recommended ceiling under static and dynamic worst cases. An ordinary 150V diode rating must be checked against each actual reverse waveform, not total output voltage.

The schematic identifies L1 74437324100 and L2 74479876147 as **specific manufacturer part numbers**, but live manufacturer current/Isat/DCR/thermal curves, domestic 1-piece availability, tax-inclusive JPY price, shipping and lead time are **UNKNOWN** this run. LT8365 controller alone does not constitute a qualified controller+magnetics pair. No order readiness.

## Chat C independent-review contract
1. Independently trace the ADI controlled schematic and NET1/NET2/NET3, including optional third stage, SW node, diode reverse and flying-cap voltage.
2. Challenge the hypothetical CCM/equal-stage assumptions and replace them with a topology-correct averaged or switching model, including guaranteed current-limit minimum, maximum duty and 5V startup.
3. Validate actual L1 Isat/DCR and pulse thermal loss, diode/ESR/capacitor worst-case stress and distributor availability.
4. Evaluate 205V/16mA vs 220V HV5524 maximum including independent OVP and cap Cmin/Cmax; do not promote hardware adoption.

## SOP proposal (no shared-file edit)
For each controller+magnetics candidate require a screenshot/primary schematic identity, installed vs optional population, exact BOM MPNs, node-voltage stress table (nominal, startup, fault, tolerance), guaranteed current-limit corners and thermal/delivery evidence. Tag every extrapolation beyond a demo-board input/output envelope as ASSUMED; avoid treating peak switch marketing rating as a qualified safe operating bound.

**Restrictions honored:** no procurement, PCB manufacture, HV energization, main merge, requirements changes, shared index edits or schedule modifications.
