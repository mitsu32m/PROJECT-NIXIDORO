# Chat B — HV-004 / SYS-001: CML 2ML DC-neon alternative current screen
Date: 2026-11-20 09:04 JST
Status: **PENDING REVIEW** (Chat C); technical disposition **CONDITIONAL candidate**, hardware/BOM **BLOCKED**.
Role: Chat B wide research, provisional / **NO FORMAL CLAIM**. Branch: codex/reva-integrated-prototype-review.
Starting HEAD: **UNKNOWN** — GitHub connector branch search returns names, not commit SHA; default-branch commit search is not a branch HEAD. Do not substitute blob SHA.
Parent issues: #7 PROTO-001, #4 SYS-001A. Scope: actual neon candidate and bounded supply implication; NOT adoption, change to 16mA target, or controller/magnetics qualification.

## New candidate and evidence classification
**CML Innovative Technologies 2ML**, wire-ended neon lamp. Distributor listing (NOT yet manufacturer-controlled PDF) says **300 µA current rating**, **65 VAC / 90 VDC** indicator, **250mW power rating**, **250V supply voltage** in the same listing. These numbers describe different test/rating contexts and MUST NOT be treated as a complete 205V DC operating specification. In particular 250V is NOT established as the bare lamp drop, and 90V DC is NOT a guaranteed running voltage.
- Farnell listing, checked 2026-11-20: https://uk.farnell.com/cml-innovative-technologies/2ml/neon-lamp-wire-ended-t1-1-4/dp/1139240
- Newark listing, checked 2026-11-20: https://www.newark.com/cml-innovative-technologies/2ml/lamps-neon-current-rating-0-300a/dp/23M8568 (title misleadingly renders 0.300A, detailed specification 300µA; cross-check mandatory).
- European distributor pages reference a downloadable '2ML Data Sheet', but manufacturer-authored revision, 205V DC ballast calculation, maximum striking voltage, DC lifetime, luminous adequacy, and Japanese landed cost remain **UNKNOWN**.
- Overseas stock is not Japanese stock; do not import a listed quantity into a Japan procurement guarantee.

## Reproducible conditional power screen
**ASSUMED** 12 neon lamps simultaneously illuminated, each at the listing's 0.300mA; two IN-12B digits at **ASSUMED** 2mA each. Then
I_neon=12*0.300mA=3.60mA;
I_digits=2*2mA=4.00mA;
I_HV,total=7.60mA (not including HV divider/bleeder/driver currents);
P_205V,rail=205*0.0076=1.558W.
At **ASSUMED** cascaded eta_5=0.90 and eta_HV=0.80, P_source,HV=1.558/(.90*.80)=2.164W, before CTRL, charger/eFuse, bias, and startup. USB 5V/500mA *ideal* 2.5W leaves only 0.336W of source-side allowance for all other loads/losses under these assumptions. This is NOT proof USB-only operation is possible, because 2ML DC operation at 0.3mA, two digit currents, losses, input current limit tolerance, thermal corners and 205V start-up are not qualified.
By contrast 16mA target consumes 3.280W rail and cannot run from USB 2.5W alone even ideally. This is a **conditional display-mode sensitivity**, not authorization to reduce target or to operate all lamps simultaneously.
If lamp current is chosen as 1mA instead, total=16mA and P_rail=3.28W. Exact display brightness and lifetime tradeoff requires real lamp data and owner choice.

## Ballast / HV driver / safety
For a **hypothetical** lamp voltage V_lamp=90V at I=0.3mA, a series resistor at 205V would be (205-90)/0.0003=383kΩ and resistor loss (205-90)*.0003=34.5mW. This is NOT a component value or voltage rating approval; V_lamp under actual DC load, ignition voltage, off-state leakage, resistor pulse and temperature limits unknown. HV5524 channel current/voltage constraints, current sharing, simultaneous switching and OVP still require independent verification.
Even if average lamp demand decreases, full 16mA architecture remains the unmodified target and HV output voltage recommendation 220V remains a safety design ceiling requiring independent OVP/hard-stop/discharge.
Comparison topology remains open: MAX668 ordinary noncoupled boost rejected only in that scope; MAX668 coupled, flyback SYS->5V->HV and direct-SYS HV need actual manufacturer-controller-plus-magnetics pair, peak currents, startup, thermal and sourced footprints. **No pair is qualified by this report.**

## Qualification / exit conditions
1. Retrieve manufacturer-controlled 2ML datasheet and establish guaranteed DC ignition/extinction/operating current, temperature, lifetime and ballast design. Cross-check Newark headline 0.300A error against 300µA detailed spec.
2. Establish exact IN-12B documentation and realistic simultaneous digit/neon illumination modes, including display brightness target.
3. Source Japan-available 2ML (or alternative) and at least two controller+magnetics pairs with dated JPY tax/shipping/lead-time and pin/footprint documentation; verify all constraints.
4. Recompute USB-only, USB+BAT supplement, BAT-only and USB+BAT net charge with charger input-current tolerance and complete CTRL loads; never conflate charge setting with actual charge.
5. Chat C independently review distributor provenance, 7.6mA scenario, resistor screen and safety qualifiers; Work decides any requirement changes.
6. Work SOP improvement proposal: add a source-provenance check for distributor headline vs technical table discrepancies and forbid treating candidate low-current display screens as target changes. Integrator may decide whether to amend ai-workflow.md; Chat B does not edit shared SOP.

Result: **CONDITIONAL mathematical screen / BLOCKED hardware**; **PENDING REVIEW**. No purchase, HV energization, PCB fabrication, main merge, shared index edits, schematic edits, or automation changes.
