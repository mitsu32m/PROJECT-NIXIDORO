# Chat B — SYS-001 USB-only simultaneous-display upper bound (no specification change)

Date: 2026-11-23 17:00 JST. Role: Chat B wide research. **PENDING REVIEW**; scoped verdict **CONDITIONAL arithmetic / BLOCKED hardware**. Formal Claim: **NONE** (no atomic Claim protocol verified; issue labels not established).
Branch: `codex/reva-integrated-prototype-review`. Starting HEAD **03d7ef5206d5d55edbb43d5a9fd70f431b81f4db**. Related issues #4 SYS-001A, #7 PROTO-001, #6 HV-002C.

## Task contract and novelty
Question: Given existing candidate two IN-12B digits, twelve neon ring lamps and proposed continuous bleeder, what simultaneous display envelope can **USB 5V/500mA without battery supplement** possibly sustain? Distinguish necessary upper bounds from actual feasibility. Exit: reproducible optimistic mode limits and a battery supplement sign convention, with exact assumptions. Exclude circuit changes, reduced target adoption, HV testing, purchasing and production. Avoid repeating prior ballast or battery current tables.

Read required six SOP/ledger/tree files, requirements, 2026-11-23 09:00/13:03 B reports, C-REVIEW-023 (15:00), A 16:02 single-open bleeder headline and Issues. Current requirements: twelve generic two-terminal neons and two optional IN-12B digits; digits normally only on demand, so **all-on is a worst-case scenario, not a confirmed normal UI mode**.

## Inputs and evidence classes
- USB source: 5V × 0.5A = 2.50W **ASSUMED nominal ceiling**; BQ25185 500mA-programmed input-limit 450mA minimum, 475mA typical, 498mA maximum from prior TI Rev.B review; use 450mA for conservative available-source comparison, not a guarantee of delivered power. Source: https://www.ti.com/lit/ds/symlink/bq25185.pdf .
- SYS→5V efficiency 90%, HV stage efficiency 75% **ASSUMED**. Both efficiencies, startup, real magnetics and low-SYS operating points remain unverified. BQ input-to-SYS loss and MCU/OLED/driver consumption are initially set to zero (**optimistic**).
- 205V bus **ASSUMED nominal**; digit 3mA and neon 0.5mA **ASSUMED**, sourced only from supplier/AC-context figures, not guaranteed DC characteristics. Prior provenance: https://www.tube-tester.com/sites/nixie/data/in-12b.htm and https://www.taydaelectronics.com/datasheets/files/1039.PDF . Do not treat 110VAC neon test as 205V DC qualification.
- 330kΩ equivalent continuous bleeder **ASSUMED**, from A/C SYS-002 study; no adopted resistor network or discharge safety claim. I_bleed=205/330000=0.6212mA, P_bleed=0.12735W. Actual single-open/temperature corners and HV divider current unknown.

## Necessary power inequality, not sufficiency
Let N_d in [0,2] be illuminated digits and N_n in [0,12] illuminated neons. Excluding all other loads, at 205V:

I_bus(mA) = 3 N_d + 0.5 N_n + 0.6212.
P_SYS(W) = 205 * I_bus(mA)/1000 / (0.75*0.90).
For USB-only without battery discharge, **necessary** condition P_SYS <= 5 * I_USB; this unrealistically assumes zero USB/BQ path loss, zero other loads, no transient or thermal constraints.

At I_USB=450mA, I_bus,max=2.25*.675/205*1000=7.4085mA.
At I_USB=500mA, I_bus,max=2.50*.675/205*1000=8.2317mA.

| Digits on | Maximum neon count at 450mA ideal | Maximum neon count at 500mA ideal | Interpretation |
|---:|---:|---:|---|
| 0 | 12 (capped by physical count) | 12 | No allowance guaranteed for control/charger loss |
| 1 | 7 | 9 | Optimistic upper bounds |
| 2 | **1** | **3** | Full 12-neon display impossible even ideally |

For N_d=2,N_n=12: I_bus=12.6212mA; P_HV=2.58735W; P_SYS=3.8331W. Minimum missing power vs ideal 450mA USB is **1.5831W**. At BAT=3.6V and zero BATFET/PCM/contact losses this would imply >=0.4398A discharge; real requirement is higher. This example is **not** the separate 16mA target case. At 16mA lamps plus 0.6212mA bleeder, P_SYS=5.048W and missing power >=2.798W, ideal 3.6V battery discharge >=0.777A. Distinguish whether the 16mA requirement already includes auxiliary loads; until defined, do not silently add the bleeder to a formally adopted total-current requirement.

USB-only at zero digit and all 12 neons: I_bus=6.6212mA, P_SYS=2.011W. At 450mA nominal input, remaining ideal 0.239W for USB path/control and losses. This is only a mathematical possibility; actual control, BQ path and conversion efficiency corners may eliminate it.

## Charge vs supplement and thermal contract
Define I_BAT>0 for **discharge**. Battery supplement is present only if I_BAT>0; I_BAT<0 is net charging. With USB connected, the BQ25185 may first reduce charging then supplement; never infer simultaneous net charging from USB insertion. Approximate power balance P_SYS <= P_USB_to_SYS + V_BAT*I_BAT minus battery-path losses; the latter are unknown and positive. When I_BAT=0 the USB-only inequality above applies. When I_BAT<0, charger loss and charge power increase USB demand. If 330kΩ bleeder is continuously connected, its 0.127W at 205V also contributes enclosure heat, in addition to ballast, lamp, converter and battery-path heat. A 2-digit short or bleeder single-open is a distinct fault and not bounded by these steady-mode equations.

## Alternative architectures and failure/temperature/sourcing implications
- **Keep SYS→5V→HV:** existing proposal; 0.675 assumed combined efficiency; requires verified TPS61023 startup, magnetics, HV OVP and SYS thermal budget. USB-only full display NO-GO even at ideal 100% efficiency for 16mA lamps.
- **Direct SYS→flyback HV (e.g., LT3757A):** removes intermediate conversion loss; but low-SYS primary current, duty, winding insulation/creepage, transformer saturation, MOSFET/clamp losses and parts availability remain UNKNOWN. For 450mA USB and 75% direct efficiency, optimistic I_bus,max=8.2317mA, still <12.6212mA all-on example.
- **MAX668 coupled magnetic/auto-transformer:** not rejected by ordinary boost duty argument; requires actual turns ratio, primary-current peak, MOSFET stress, losses, fault stop and obtainable magnetic part. No qualified pair exists.
- **Display-mode power limiting:** software may limit nominal simultaneous current but is **not** an independent OVP, battery thermal cutoff or fault-safe shutdown. A verified truth table and user approval required before lowering 16mA target.
- **USB+BAT supplement:** may meet energy balance, but is not net charging and needs pack PCM/BATFET/charger/connector/thermal qualifications. USB source compliance and startup transients unproven.

No new verified distributor stock or transformer MPN in this run; do not call any controller+magnetics pair qualified.

## Independent review questions / next steps
1. Chat C verify floor-count inequalities, whether 16mA is lamp-only or total bus and the 330kΩ continuous-bleeder assumption; check if all-on UI mode is required.
2. Work/owner choose **proposed** operating-mode truth table (12-ring only, digits-on-demand, clock, fault) without changing requirements yet; measure/qualify actual DC lamp current and auxiliary loads.
3. Chat B next: source a specific DC-rated neon and actual transformer/controller pair with manufacturer winding and availability evidence; no repeated theoretical efficiency-only screens.
4. Chat A: coordinate BQ SYS minimum and OVP/Cmin/Cmax, thermal and shutdown.
5. Proposed SOP addition for Work review: every power table must declare whether 16mA includes bleeder/divider/driver, display truth table, BAT sign, USB path loss and source classes. Do **not** directly edit shared SOP.

No manufacturing, purchase, HV energization, main merge, requirement or schedule change.