# Chat B — HV-001 / SYS-001: manufacturer high-voltage flyback reference as a concrete alternative
Date: 2026-11-20 17:01 JST. Role: wide research. Starting branch HEAD: 5921698d8732c2a17ce918f72ee76086f5c4c60c (GitHub branch REST). Branch: codex/reva-integrated-prototype-review.
Claim: NONE, provisional #7/#4 research (atomic claim not verified). Review: **PENDING REVIEW** for Chat C. Decision: **CONDITIONAL** primary-source reference exists; **BLOCKED** for 205V/16mA adoption and order-ready parts.

## Contract and novelty
Question: Is there an actual manufacturer-documented controller+transformer high-voltage pair rather than a generic hypothetical flyback? Exit: identify exact source-controlled schematic MPNs, source operating point, gap to 205V/16mA, supply modes, thermal/fault/procurement holds. No circuit changes, HV testing or part purchases. Read required six documents, latest 2026-11-20 15:00 C-REVIEW-011, 16:00 Chat A HV-003 and issues #2/#4/#7/#9. This report addresses C-REVIEW-011 request for an actual pair, not another NTC/USB sensitivity repetition.

## Manufacturer primary evidence — actual pair
Analog Devices LT3757/LT3757A Rev.H data sheet, **page 32, Typical Applications, High Voltage Flyback Power Supply**:
https://www.analog.com/media/en/technical-documentation/data-sheets/lt3757-3757a.pdf
- Controller **LT3757**, transformer **TDK DCT15EFD-U44S003**, MOSFET **Vishay Si7850DP**, diode **Vishay GSD2004S** (two diodes in series), primary:secondary turns ratio **1:10**, **VIN 5–12V**, **VOUT 350V at 10mA**, fSW **100kHz**, 0.02-ohm sense, 68nF x2 output capacitor, 1.5M+1M+1M+16.2k feedback chain. These are manufacturer *application schematic* values, not guaranteed across-temperature output rating for our altered circuit.
- This is a stronger reference than controller-only listing: it identifies a **specific transformer** and full topology. LT3757 manufacturer product page says production and input 2.9–40V; the *example* itself is 5–12V, so **do not claim 1S battery 2.5–4.2V compatibility**.
- Primary-source reference output 350V*0.010A = **3.50W**, versus target 205V*0.016A=**3.28W**. The reference is **6.7% higher nominal output power** but **not proof** of target feasibility: changed VOUT, output current, secondary RMS, duty, feedback, rectifier and transformer heating need recalculation. 350V example is *not* acceptable to connect to HV5524 (220V recommended maximum).
- At assumed efficiency etaHV=0.75/0.80, 3.28W target would draw 4.373/4.100W at the 5V converter input, or 0.875/0.820A at 5V before 5V-regulator/control losses. These are assumed, not manufacturer efficiency data.
- If feeding from 1S through SYS->5V at eta5=0.90, source demand is 3.28/(0.75*0.90)=4.859W or 3.28/(0.80*0.90)=4.556W, **before other system loads**. A 5V/500mA USB input cannot cover 3.28W even at ideal efficiency. USB+BAT supplement is potentially a **net-discharge** state; USB+BAT net-charge requires independently proven spare power and power-path conditions.

## Alternative pair comparison, source class
A. **ADI LT3757 + TDK DCT15EFD-U44S003**: manufacturer published 5–12V to 350V/10mA schematic (3.50W), full component IDs. Strongest concrete newly identified reference; must redesign and requalify for 205V, verify exact transformer sourcing.
B. **Existing Sumida 13324-T086 or Würth 750315839 with their associated original reference controllers**: previous GitHub B SYS-001 report describes nominal 200V/12mA (2.40W) examples, but controller+transformer association and complete primary source are **not independently reverified in this run**. 205V/16mA requires +36.7% output power versus 2.40W, so neither is a proven pair at target. Do not imply either is rated at 3.28W.
C. **MAX668 coupled-inductor approach**: remains candidate; exact coupled magnetic, polarity, switch stress, leakage clamp and regulation are unqualified. Ordinary uncoupled 5V->205V boost rejection does not reject coupled variant.
D. **Direct 1S/SYS flyback**: potentially removes intermediate 5V losses, but the specific LT3757 published example starts at 5V and cannot serve as a direct 1S reference.

## Fault, temperature, procurement gates
- Independent OVP, stop and discharge mandatory; LT3757 soft-start/UVLO do not independently prove 220V HV5524 protection. Changing feedback to 205V without full tolerance/transient and tail-energy proof is prohibited.
- Transformer: primary/secondary DCR, Lp tolerance, leakage, insulation, Isat/flux, temperature rise, 5V low corner, switch peak, diode reverse voltage, winding temperature and sealed PETG heat all UNKNOWN at 205V/16mA. Verify thermal with actual part and mounting.
- 350V/10mA reference COUT 68nF x2 is NOT an approved Cmin/Cmax for 205V OVP/discharge; coordinate SYS-002 and #6.
- TDK DCT15EFD-U44S003 Japan stock/lead time, lifecycle, actual manufacturer drawing, MOQ, landed JPY price UNKNOWN. LT3757, Si7850DP, GSD2004S Japan stock/JPY also UNKNOWN. The application is a credible technical starting point, not a purchasable BOM.
- Failure modes to assess: load removal/open circuit, failed feedback, shorted rectifier, shorted MOSFET, transformer insulation breakdown, USB disconnect, battery low, thermal runaway and latched restart. No hardware safety release.

## Chat C / Work handoff
Review the exact page 32 primary source and transformer MPN, verify 350V/10mA/5–12V/1:10, distinguish reference from qualified target, challenge current and power-path calculations. Work should ask Chat A to analyze LT3757/TDK as an *alternative* to MAX668, not adopt it. For Chat B next: retrieve TDK transformer original drawing + actual Japan distributor availability, and identify a second manufacturer controller+magnetics reference with >=3.28W nominal output or document why unavailable. For SYS-001, build node-specific USB/VBUS/SYS/BAT budget including auxiliary load and actual BQ power-path.
SOP proposal (do not edit shared SOP): every alternative-topology report must distinguish manufacturer example output power from qualified target and record minimum supported VIN separately from controller's generic VIN range.
No formal Claim; no shared-index edit, purchases, PCB, HV energization, main merge, requirement change or schedule modification.
