# Chat B — HV-004 / SYS-001 lamp-current evidence and 16mA target sensitivity
Date: 2026-11-23 09:00 JST
Status: **PENDING REVIEW**; scoped finding **CONDITIONAL**, hardware qualification **BLOCKED**
Role: Chat B wide research. Formal Claim: **NONE** (atomic Claim protocol unverified).
Branch: `codex/reva-integrated-prototype-review`
Starting HEAD commit SHA: **UNKNOWN** (GitHub connector can read files but did not expose exact branch HEAD; repository-wide commit search is not branch HEAD).
Related issues: #4 SYS-001A, #7 PROTO-001, #2 HV-001A.
Question: Is 16mA simultaneous HV current backed by actual selected lamp specifications? What does changing the lamp current assumption do to USB and HV power requirements?
Exclusions: no target change, no lamp adoption, no energization or production.

## Repo baseline
Read branch SOP, handoff, open-issues, decisions, tech-tree YAML/MD and prior Chat B 2026-11-23 05:00 report. Requirements document says twelve generic two-terminal neon lamps and two candidate IN-12B; simultaneous-on behavior not fixed. D-005 labels 16mA a TARGET, not verified. Earlier 16mA scenario used two digits at 2mA each plus twelve neon at 1mA each, both ASSUMED.

## Evidence / provenance
- **Manufacturer primary, product-specific but AC test:** San Guang Electronics NE-2 6x16x50 PDF, hosted Tayda: https://www.taydaelectronics.com/datasheets/files/1039.PDF . 110VAC, 68kΩ series, approximately 0.7mA. This is **NOT** a specified 205V DC current, nor proof that a generic sourced NE-2 has same characteristics.
- **Supplier, secondary IN-12B:** https://www.tube-tester.com/sites/nixie/data/in-12b.htm reports typical cathode current 2.5–3.5mA and operating cathode voltage about 145V. Original Soviet factory sheet / exact lot still required.
- **Supplier, secondary cross-check:** https://www.swissnixie.com/tubes/IN12B/ reports 3mA/segment, 145V sustaining and 170V ignition typical. It does not qualify a specific NOS tube.
- **Supplier, part-specific counterexample:** https://www.jameco.com/z/NE-2-Jameco-ValuePro-Neon-Lamp-NE-2-1A1-65-120VAC-0-3mA-Wire-Leads_27351.html displays 0.3mA in specifications, 0.5mA in overview; inconsistent page and AC context, so do not assert a guaranteed DC design current.
- **UNKNOWN:** selected lamp manufacturer/MPN/lot, DC sustaining voltage/current distribution, lifetime at DC, series resistor tolerances, whether 12 neons and both digits ever remain on continuously, decimal point duty, startup/restrike and driver losses.

## Reproducible scenario math
For two IN-12B digit cathodes simultaneously lit and 12 neon bulbs lit:
I_HV = 2 I_digit + 12 I_neon + I_aux. Here I_aux is unknown driver/divider/bleeder load, excluded from table; HV bus current equals branch currents including ballast, while each lamp dissipates only its own sustaining voltage times current.

| Scenario (all ASSUMED, not qualified) | I_digit | I_neon | I_HV excl aux | P_HV at 205V |
|---|---:|---:|---:|---:|
| Legacy 16mA target decomposition | 2mA | 1mA | 16mA | 3.280W |
| Lower NE-2 scenario | 2.5mA | 0.3mA | 8.6mA | 1.763W |
| 0.5mA neon scenario | 3mA | 0.5mA | 12mA | 2.460W |
| 0.7mA neon scenario | 3.5mA | 0.7mA | 15.4mA | 3.157W |
| Conservative comparison (not a rating) | 3.5mA | 1mA | 19mA | 3.895W |

At η_HV=75% and η_SYS5V=90% (both ASSUMED), 12mA requires 2.46/(.75*.9)=3.644W SYS; 16mA requires 4.859W SYS. Even 8.6mA requires 2.612W SYS, exceeding USB 5V*0.5A=2.50W before any control load or BQ path loss. This does **not** imply a lower-current design is approved or that USB-only can sustain it. With the 450mA input-limit minimum previously recorded in the project, ideal USB input may be 2.25W; actual available SYS power is less.
At 205V, nominal 145V IN-12B sustaining voltage and 3mA implies (205-145)/.003 = 20kΩ ballast and resistor power 60*.003=0.18W per digit, **only a typical illustrative operating point**. DC neon resistor at nominal sustaining 60V and 0.5mA would be 290kΩ and dissipate 72.5mW each; no guarantee for selected NE-2 or striking behavior. Check rated resistor voltage, pulse, creepage, power derating.

## Important distinction
A supplier's 110VAC lamp current with a series resistor is not a manufacturer's guaranteed continuous DC current. 16mA must remain an unchanged design target pending user approval; evidence may justify an optional reduced-current mode only after visibility/lifetime tests and explicit owner decision. For power budgeting include HV5524 leakage/quiescent, bleeder and divider current, OLED/audio/control, and startup charge energy separately.

## Exit gates / next action
1. Select exact purchasable NE-2-equivalent MPN with manufacturer DC breakdown/sustain/current/lifetime specs, and exact IN-12B original datasheet provenance or characterize under approved safe bench plan.
2. Define simultaneous-on truth table for 12-step ring, two digits, decimal point and modes (clock, pomodoro, transitions, faults); count continuous and transient currents separately.
3. Calculate actual 205V series resistors incl tolerance, dissipation, HV5524 voltage/current and PCB creepage, and re-run USB-only/BAT supplement/charge budgets with minimum input and auxiliary loads.
4. Seek qualified HV controller+magnetics pairs; no controller-only listing counts as a valid 205V/16mA supply.
5. Chat C independently review source-classification, arithmetic and why AC NE-2 data cannot certify DC. Work integrates shared indices only after review.
6. SOP proposal: require source-specific AC-vs-DC applicability and an explicit simultaneous-on truth table in lamp power contracts; do not directly edit docs/ai-workflow.md.

No purchase, PCB fabrication, HV application, main merge, spec or scheduler change.