# Chat B — SYS-001: USB 500mA, battery assist and charging are distinct power modes

Date: 2026-11-22 05:00 JST (scheduled research window; exact execution clock not independently verified)
Status: **PENDING REVIEW**; **NO FORMAL CLAIM**. Decision: **CONDITIONAL power-balance arithmetic; physical USB/BAT path and 16mA operating mode BLOCKED**.
Branch: `codex/reva-integrated-prototype-review`.
Starting branch HEAD: **UNKNOWN — exact ref SHA could not be obtained using available GitHub connector**. Last verified prior Chat B commit: `4c3948c6ed7d23c6cc50678f0dcaf2f131913c7a` (not asserted to be HEAD).

## Bounded task contract
Parent issues: #7 PROTO-001, #10 HV-001; SYS-001 in open-issues. Determine *necessary* USB-only and USB+battery discharge conditions without silently treating BQ25185 500mA input limit as a guaranteed system-load supply or assuming simultaneous charge. Exit: explicit equations, sensitivity table, measurement/primary-evidence gaps, Chat C questions. Excludes hardware authorization, topology adoption, and real cell specifications.

## Repo review / nonduplication
Read required six canonical documents (ai-workflow, handoff, open-issues, decisions, tech-tree.yaml, tech-tree.md), issue search including #7/#10, and #10 review thread through C-REVIEW-016 and Chat B 01:03 update. This report extends earlier HV-only 0.820–0.875A estimates to the **upstream 5V boost / battery and charging concurrency**. GitHub issue search returns insufficient label/state metadata to prove safe Claim; no Claim asserted.

## Explicit necessary power contract
Assume: 205V, 16mA continuous (project target, not verified lamp demand), so P_HVout=3.280W. Define eta_HV = HV converter efficiency, eta_5 = SYS→5V boost efficiency (only if path uses that converter), P_aux5 = 5V-side controls/OLED/driver load, P_auxSYS = SYS-side controls, P_charge = cell charging power drawn from SYS. All efficiencies below are **ASSUMED**, not measured or guaranteed.

For SYS→5V→HV:
P_5,load = 3.28/eta_HV + P_aux5
P_SYS,load >= P_5,load/eta_5 + P_auxSYS
For USB-only without battery discharge and with charging disabled:
P_SYS,available <= V_USB * I_USB * eta_USBpath, where eta_USBpath <=1 and USB current limit 500mA is an upper bound, not guaranteed delivered load power.
Thus 2.50W theoretical input maximum <3.28W output even with zero other loads and 100% conversion: **USB-only 16mA continuous NO-GO independent of HV topology**.

For a USB+BAT mode (battery discharging, IBAT>0), the necessary lower bound on battery contribution at SYS is:
P_BAT_to_SYS >= max(0, P_SYS,load - P_USB_to_SYS), where P_USB_to_SYS <=2.50W, and BAT terminal power is greater when BATFET/PCM/contact losses exist. This is **not** proof that the BQ25185 power path can sustain the needed current, thermal, or transitions.

### Illustrative no-auxiliary, ideal USB-path scenarios (all ASSUMED)
| eta_HV | eta_5 | P_SYS,load (W) | Battery SYS contribution at least (W) | at 3.0V cell, ideal IBAT at least (A) |
|---|---|---:|---:|---:|
| 0.80 | 0.90 | 4.556 | 2.056 | 0.685 |
| 0.75 | 0.90 | 4.859 | 2.359 | 0.786 |
| 0.70 | 0.85 | 5.513 | 3.013 | 1.004 |
The last column assumes ideal 3.0V→SYS transfer; actual BAT current increases with series losses and depends on SYS voltage. These are **optimistic lower bounds**, not design ratings. If P_aux5=0.30W in the 75%/90% case, extra SYS demand =0.333W and battery minimum rises from 2.359 to 2.692W. Charging simultaneously increases input demand further; a 250mA charge setpoint is not an entitlement to 250mA charge while load consumes the USB budget.

## Mode and failure questions
1. USB-only/no battery: full 16mA must be inhibited or display demand reduced; no software claim that 500mA input can deliver 3.28W.
2. USB+battery: identify BQ25185 input-limit priority, SYS/BATFET supplemental-current behavior and whether discharge while USB present is actually supported at each VIN/SYS/BAT corner. Do not infer from 'power path' marketing wording.
3. USB+charge: charge current must be reduced/inhibited when input-limited; distinguish *net charging*, *net discharging*, and *no charging*. Need signed IBAT and thermal qualification.
4. Battery-only: low-cell 3.0V, PCM trip, connector/contact/BATFET voltage drop, TPS61023 current-limit/startup, HV output-capacitor inrush and sealed PETG temperature must be jointly bounded.
5. Fault: USB unplug/replug, BAT absent/PCM opened, NTC open/short, controller reset, HV open load, OVP hard-off and discharge; no guarantee that disabling charging disables HV.
6. Current-demand baseline: document actual IN-12B/neon lamp DC currents, per-channel ballast dissipation and simultaneous on/off matrix before declaring 16mA normal versus peak.

## Architecture comparison / sourcing gates
- MAX668 coupled-inductor: externally switched, magnetics design and switch/diode loss unqualified; no BOM approval.
- LT3757 flyback: 350V/10mA reference exists, but DCT15EFD-U44S003 sourcing flagged obsolete; substitution requires full magnetics/thermal qualification.
- LT8365 DC2838A charge pump: 9–30V demo is not 5V qualification; Rev.A switch current-limit MIN/TYP/MAX 1.5/2.0/2.7A at stated datasheet conditions does not establish 5V startup or real SW waveforms. Pump capacitor/diode RMS and voltage rating unproven.
- Direct SYS flyback: removes eta_5 penalty in principle but raises low-cell primary current and requires actual sourceable transformer/IC pair.
No newly verified stock/price/lead time in this run; **UNKNOWN**, not assumed available.

## Primary evidence to obtain
TI BQ25185 Rev.B power-path/input-current regulation/TS mode tables and pin-level behavior; TI TPS61023 worst-case current limit and low-VIN startup; ADI LT8365 Rev.A p3 and DC2838A controlled schematic; manufacturer-controlled magnetic component drawings and current distributor stock. Previous reports contain partial references, but this run did not independently re-download all manufacturer PDFs; treat new numerical results here as explicit assumption sensitivity only.

## Chat C independent review request
Verify equations and whether USB current is properly constrained at input versus SYS; challenge any implicit simultaneous battery assist assumption, charger net current, 3.0V cell lower bound, and efficiency multiplication. Require explicit load matrix and physical path evidence before any architecture adoption. Proposed SOP addition (for integrator, **do not directly edit ai-workflow**): every SYS-001 report must label USB-only / USB+BAT discharge / USB+net-charge / BAT-only and carry signed IBAT, path efficiencies, charge state, thermal and fault conditions.

## Next bounded work
Fetch exact TI BQ25185 supplement-mode/current-limit guarantees and actual cell-to-SYS topology; identify two *in-production, single-unit purchasable* controller+magnetics pairs with manufacturer current/thermal data. Compare 205V/16mA and lower-current lamp modes, then obtain Chat C review. No purchase, PCB fabrication, HV energization, main merge, requirements or schedule changes.
