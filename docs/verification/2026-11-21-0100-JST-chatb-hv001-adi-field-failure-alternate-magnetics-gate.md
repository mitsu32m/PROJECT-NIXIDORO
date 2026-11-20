# Chat B HV-001 / SYS-001 — ADI field failure and replacement-magnetics qualification gate
Date: 2026-11-21 01:00 JST
Status: **PENDING REVIEW** (Chat C); technical disposition **BLOCKED** for parts adoption
Role: Chat B, provisional research; **NO FORMAL CLAIM**
Starting branch HEAD: `355a2585081f77d0acfde79cd59979aba556c3cc`
Issues: #7 PROTO-001, #4 SYS-001A, #2 HV-001A (Chat A owns circuit deep-design)

## Task contract
Question: Is a pin/ratio-similar replacement transformer for LT3757's obsolete TDK DCT15EFD-U44S003 an acceptable direct substitute for a 205V/16mA continuous NIXIDORO HV stage?
Exit: identify manufacturer-origin evidence of substitution risk and formulate a testable qualification contract, including power, switching frequency, temperature, fault behavior and supply modes. No actual topology or BOM adoption.

## Newly located manufacturer-hosted engineering evidence
1. ADI EngineerZone 2019-09-30, *LT3757 Flyback Converter*: engineer reports using alternative **TDK ATB322524-0110-T000** after original DCT15EFD-U44S003 obsolescence, for 5V -> 200V (<10mA), at **1MHz**. Transformer reportedly became very hot and in some cases melted. **Source class: user field report hosted on manufacturer forum; NOT independently measured/verified and NOT a guarantee of this part's behavior in other circuits.** https://ez.analog.com/power/f/q-a/116852/lt3757-flyback-converter/347950
2. ADI EngineerZone 2020-03-06/17, *LT3757*: another user reports original transformer obsolete. ADI employee response suggests three alternatives in an **image** and points to **LT8365** as another IC. Image alternative MPNs not recoverable from text, so do not invent them. **Source class: manufacturer employee informal recommendation, not qualified NIXIDORO circuit.** https://ez.analog.com/power/f/q-a/162262/lt3757/367319
3. ADI LT3757/LT3757A Rev.H datasheet, p.32: 5–12V -> 350V/10mA example, TDK DCT15EFD-U44S003; 100kHz example (RT=140k), not a 1MHz direct substitution design. https://www.analog.com/media/en/technical-documentation/data-sheets/LT3757-3757A.pdf
4. ADI product page lists LT3757/A production and programmable switching frequency 50kHz–1MHz; IC production status does not qualify transformer supply. https://www.analog.com/en/products/lt3757.html

## Calculated scope and limits
- Current requirement **ASSUMED target**: 205V x 0.016A = **3.280W**. ADI example: 350V x 0.010A = **3.500W**. Output power is 93.7% of example, but required output current is 160%; power similarity is NOT a secondary winding RMS/thermal guarantee.
- At HV efficiency `eta_HV` 0.75/0.80 (both **ASSUMED**), 5V-stage draw is 3.28/(5*eta) = **0.875/0.820 A**. USB 5V x 0.5A = **2.50W theoretical maximum** (before charger limit, 5V boost and auxiliary load). Thus 16mA USB-only remains impossible. Battery supplement must be distinguished from positive net battery charging.
- Under idealized equal-current and same-wire comparison only, DC winding copper loss scales with I^2: (16/10)^2 = **2.56x**; actual RMS currents, turns, duty, waveform and temperature differ, so **not** a predicted real loss multiplier.
- Switching frequency 1MHz vs 100kHz is 10x, but switching loss cannot be assumed exactly 10x without actual waveforms; core loss depends on flux swing, frequency, material and temperature. ADI field report is a concrete warning against ratio-only drop-in substitutions.
- The original reference output 350V is above the HV5524 220V recommended limit; feedback and independent OVP require redesign and separate review. **Never energize original 350V reference into HV5524.**

## Comparison — status, not a qualified BOM
| Architecture | Primary evidence | Magnetics supply | Thermal / faults | Disposition |
|---|---|---|---|---|
| LT3757 + DCT15EFD-U44S003 | ADI Rev.H p32 350V/10mA | Reported obsolete; current stock not verified this run | 205V/16mA and 220V OVP unproven | BLOCKED |
| LT3757 + ATB322524-0110-T000 | ADI-hosted 2019 user report 5V/200V <10mA | Current stock and controlled drawing UNKNOWN | Reported overheat/melting at 1MHz; not quantified | NOT a qualified drop-in |
| LT8365 + suitable magnetics | ADI employee 2020 alternative IC suggestion | Pair not identified; stock UNKNOWN | No 205V/16mA primary reference verified | RESEARCH CANDIDATE |
| MAX668 coupled-inductor | Prior #2 investigation | Actual qualified magnetics UNKNOWN | Winding polarity, leakage, peak switch/diode stress open | RESEARCH CANDIDATE |

## Required replacement-transformer gate
Obtain controlled manufacturer MPN and datasheet: primary inductance and tolerance; turns ratio/polarity; magnetizing and leakage inductance; Isat vs temperature, winding DCR at operating temperature, core material/core loss vs flux/frequency, isolation/creepage and package, mounting/footprint. Derive peak/RMS primary/secondary currents for 205V/16mA continuous at low VIN, startup and no load; verify diode reverse voltage, FET VDS and clamp. Estimate worst-case losses and sealed PETG temperature with defensible thermal resistance; verify open-load, short, MCU-off, OVP and discharge behavior. Obtain dated Japan single-unit stock, total JPY cost, lead time and second-source before order approval. UNKNOWN is not a passing gate.

## Chat C / Work review request
Independently check the provenance of the 2019 user failure and 2020 ADI employee reply; verify whether Rev.H 100kHz example applies to the exact shown schematic and whether any newer controlled magnetic part can be identified. Do not generalize one field failure into a ban on the ATB series or 1MHz operation. Keep LT3757/other controller approaches open until concrete magnetics and thermal evidence exists.

## Workflow proposal (do not edit shared SOP)
For every candidate controller+magnetics pair require a **frequency/flux/thermal cross-check** and manufacturer-controlled magnetic part evidence, not just turns ratio and nominal output watts. Attach provenance labels to community failures and manufacturer forum responses. A Chat B worker should write unique reports; Work alone integrates shared registers.

## Unchanged restrictions
No parts purchasing, PCB manufacturing, HV application, main merge, shared-index overwrite, or requirements change. Hardware remains NOT ORDER-READY.
