# Chat B — SYS-001 / HV-004: low-current neon USB-only margin corner
Date: 2026-11-20 12:57 JST
Branch: codex/reva-integrated-prototype-review
Starting HEAD: c9cb002dbf6c9be640ea97a5acd886b3e51bb885 (resolved via GitHub fetch_commit with branch ref).
Role: wide research. Claim: NONE; provisional task from #7 and #4. Review: **PENDING REVIEW** for Chat C.
Technical result: **NO-GO** for 205V/16mA from 5V/500mA USB alone; **BLOCKED** for proposed low-current 2ML USB-only mode (insufficient verified power budget and primary lamp data). No design adoption.

## Task contract
Question: Does the distributor-listed 300uA 2ML scenario provide a robust USB-only power budget after the proposed BQ25185 input-limit tolerance? Exit: reproducible sensitivity and evidence classification. Excludes changes to target, component adoption, physical tests, KiCad, purchases.
Sources: docs/verification/2026-11-20-0904-JST-chatb-hv004-cml-2ml-dc-neon-current-screen.md; docs/verification/handoff.md; docs/verification/open-issues.md; docs/tech-tree.yaml and .md; TI BQ25185 https://www.ti.com/lit/ds/symlink/bq25185.pdf ; distributor 2ML https://uk.farnell.com/cml-innovative-technologies/2ml/neon-lamp-wire-ended-t1-1-4/dp/1139240 . Manufacturer-controlled 2ML PDF not obtained. No stock/price guarantee.

## Evidence and power boundaries
- **ASSUMED** 12 neon simultaneously on at 0.300mA each (distributor listing, not qualified at 205V DC), plus two IN-12B at **ASSUMED** 2mA each: 7.6mA total; 205V rail output = 1.558W. HV divider, bleeder and driver omitted.
- **ASSUMED** 5V conversion efficiency 90%, HV efficiency 80%: 1.558/(0.9*0.8)=2.1639W required at upstream 5V input, before all other loads.
- **Previously documented TI electrical table** for nominal 500mA input setting: 450/475/498mA minimum/typical/maximum; verify exact test conditions and revision before treating 450mA as guaranteed across the actual design envelope. At 5.0V, 450mA gives 2.250W; 475mA gives 2.375W; 500mA ideal nominal gives 2.500W.
- Source-side leftover before MCU/OLED/RTC/charger bias/eFuse/thermal: 0.0861W at 450mA; 0.2111W at 475mA; 0.3361W at 500mA. 0.0861W/5V=17.2mA remaining input current in 450mA scenario. These are conditional arithmetic, not a guarantee that BQ25185 passes that energy to SYS.
- If HV conversion is 75% rather than 80% with 90% 5V stage, source need =1.558/0.675=2.308W, **exceeding** the 2.250W 450mA scenario before control loads. At 70% HV efficiency, source need=2.473W.
- The **unchanged full target** 205V*0.016A=3.280W exceeds 5V*0.500A=2.500W even at ideal 100% efficiency. No choice of MAX668/flyback/direct-SYS removes this energy constraint.

## Mode contracts (signed IBAT positive when discharging)
1. USB-only, battery absent or not supplementing: P_USB,usable >= P_HV/eta_path + P_CTRL + P_losses + P_charge(if any); require min USB input power and worst-case efficiencies. For the 2ML hypothetical mode, currently BLOCKED.
2. USB+BAT supplement: if total demand > USB available and path allows supplement, IBAT>0, battery net discharges. **Do not call this charging.** Must verify actual BQ power-path transition, battery voltage, BATFET and thermal losses.
3. BAT-only: input from battery must cover HV, CTRL and power-path losses; separate cell thermal cutoff and HV hard-off/discharge needed.
4. USB+BAT true net charge: IBAT<0 while loads run, requiring spare input capacity and permitted charge temperature; a programmed 250mA charge setting does not imply this state.

## Alternative topology screening — no qualified pair
- MAX668 conventional uncoupled boost: prior scope rejected for required 5V-to-205V practical conversion. Coupled MAX668 is a research candidate, but requires exact transformer, switching peak/temperature, output regulation and fault-stop evidence.
- 5V-to-HV flyback with controller plus matched transformer: candidate; two-stage efficiency compounds and 5V startup/thermal must be shown, not inferred from a 200V/12mA reference.
- Direct battery/SYS-to-HV coupled flyback: candidate potentially removes 5V stage loss, but demands qualified variable-input start-up, battery brownout, peak switch current, thermal and fault behavior.
- Existing Sumida 13324-T086 and Würth 750315839 reference applications are around 200V/12mA, **not** proven at 205V/16mA. 3.28W vs 2.40W is +36.7%. Japan stock, tax/shipping and exact controller+magnetics qualified pair remain UNKNOWN.
- No manufacturer-qualified 2ML DC lamp current, strike voltage, luminosity or life evidence; no verified Japanese landed cost. Thus the 7.6mA mode cannot be adopted or used to weaken 16mA requirements.

## Thermal and failure implications
At the 450mA assumed source corner, a 0.086W nominal margin is insufficient to claim startup or steady-state thermal robustness: no bounded CTRL load, charger losses, voltage droop, capacitor charging, output load transients, high temperature efficiency, lamp ignition, open load or output overvoltage. Independent HV OVP/hard-stop/discharge still mandatory. Even a lower lamp average current does not imply safe open-circuit HV.

## New actionable gap and Chat C request
1. Obtain manufacturer-controlled 2ML PDF and DC-current/ignition/lifetime/ballast details, or replace candidate; explicitly cross-check 300uA distributor spec.
2. Obtain guaranteed input-current minimum **at actual configured ILIM and VBUS/temperature** and bound power delivered to SYS after eFuse and charger. Distinguish USB 5V nominal from minimum delivered VBUS.
3. Establish bounded CTRL + auxiliary draw and efficiency map at 7.6mA/16mA, cold/hot, startup and battery transition.
4. Source two actual HV controller+magnetics pairs and Japan landed costs; identify reference-only vs rated designs.
5. Chat C: independently check arithmetic, table provenance and failure of nominal USB-only margin. Work: do not change requirements without owner decision.
6. SOP proposal (not direct edit): require source-side *minimum* input-limit corner and auxiliary-load reserve whenever low-current mode is proposed, rather than reporting only 500mA nominal.
Status: **PENDING REVIEW**. No formal Claim, purchase, PCB, HV operation, main merge, shared index edits or automation modifications.
