# C-REVIEW-013 — SYS-002 capacitor/bleeder and HV-001 transformer evidence batch
Date: 2026-11-21 03:00 JST (scheduled review window)
Role: Chat C independent first-pass reviewer. No formal Claim.
Branch: `codex/reva-integrated-prototype-review`
**Starting branch HEAD (resolved by GitHub fetch_commit on branch): `e636652004a34e90bd07d24217e3c1d22f6fe431`.**
Prior C review: C-REVIEW-012 at `69dc021dc3b562f2f51f620091e061dec62f03fd`. GitHub compare returned 3 newly added reports (3 commits ahead), all reviewed here. Required SOP, handoff, open issues, decisions and both tech-tree representations read at pinned starting SHA; issue titles/bodies #2/#6/#7/#4 reviewed. Shared indexes untouched.

## Scope, prioritization and verdict
P0 first: (1) Chat A `2026-11-21-0001-JST-SYS-002-ovp-capacitance-bleeder-fault-feasibility.md`, issue #6: **ACCEPTED (algebra only)**, **CONDITIONAL (joint illustrative infeasibility)**, **BLOCKED (hardware safety/selection)**.
(2) Chat B `2026-11-20-2103-JST-chatb-hv001-tdk-obsolete-sourcing-gate.md`, issues #7/#2: **ACCEPTED (DigiKey obsolete classification and basic arithmetic)**, **CONDITIONAL (historical Marutsu listing/TDK mirrored drawing)**, **BLOCKED (procurement and 205V/16mA design)**.
(3) Chat B `2026-11-21-0100-JST-chatb-hv001-adi-field-failure-alternate-magnetics-gate.md`, issues #7/#2/#4: **ACCEPTED (ADI Rev.H published 350V/10mA 100kHz example and 5V input)**, **CONDITIONAL (manufacturer-forum user anecdote)**, **BLOCKED (drop-in transformer substitution)**.
No hardware approval, no selected BOM, no change to 205V/16mA target.

## Independent numerical reproduction
Given assumed `Etail=0.2253mJ`, `Vlimit=220V`, `Cmin > 2 Etail/(Vlimit^2-Vtrip,max^2)`: at Vtrip 217, 219.17, 219.978 V, thresholds are respectively **0.343707, 1.236176, 46.551914 uF**. Strict inequality and nonzero design margin needed.
For assumed 2.1Mohm surviving one-open bleeder, 220V to *arbitrary* 60V in 3s, `Cmax <=3/[2.1e6 ln(220/60)]=1.099508uF`. Thus 219.17V scenario is algebraically incompatible (1.236176uF lower bound exceeds 1.099508uF upper bound); 217V leaves a mathematical interval, not a part qualification. `0.5*1uF*205^2=21.0125mJ`. If actual capacitor effective Cmax/Cmin ratio exceeds the available 1.099508/0.343707=3.199, even the 217V illustrative scenario fails. The example assumes a single isolated residual pulse and first-order RC discharge; neither is guaranteed.
**Additional challenge:** capacitance is not a substitute for a proven bounded post-trip energy: continued switching, multiple pulses, common-mode trace failures, diode recovery, parasitic inductance and output overshoot are outside the scalar model. Treat 220V as HV5524 recommended design ceiling, not a human-touch safe threshold. 60V and 3s are arbitrary examples, not accepted safety criteria.

205V*0.016A=3.280W vs ADI 350V*0.010A=3.500W (93.714% output power; 160% nominal output current). At hypothetical HV efficiencies 75% and 80%, 5V input currents are 0.874667A and 0.820A, respectively. Ideal 5V*0.5A=2.5W is below 3.28W. At hypothetical equal RMS waveforms only, (16/10)^2=2.56, **not** a measured winding copper loss multiplier. Historical Marutsu 500*JPY851.86=JPY425,930, not a current quotation or proof of universally unavailable stock.

## Independently inspected primary/provenance
- ADI LT3757/LT3757A product page https://www.analog.com/en/products/lt3757.html lists Rev.H and 50kHz–1MHz controller capability; this does not qualify any transformer. Rev.H PDF page 32 https://www.analog.com/media/en/technical-documentation/data-sheets/lt3757-3757a.pdf?isDownload=true contains **5–12V, 350V/10mA, 100kHz (RT 140k), TDK DCT15EFD-U44S003**. This is a 100kHz reference, not a 1MHz design. 
- DigiKey https://www.digikey.com/en/products/detail/tdk-corporation/DCT15EFD-U44S003/1473742 explicitly lists **Obsolete/no longer manufactured**. Manufacturer EOL notice, verified current stock at other suppliers, and controlled TDK drawing remain **UNKNOWN**.
- Marutsu historical stock/MOQ and 2005 TDK drawing mirrored on third-party site were **not independently reopened in this run**; retain as **CONDITIONAL/UNVERIFIED**, not source-confirmed.
- ADI EngineerZone reports https://ez.analog.com/power/f/q-a/116852/lt3757-flyback-converter/347950 and https://ez.analog.com/power/f/q-a/162262/lt3757/367319 were **not independently opened this run**. Their claimed melting and employee advice are **reported anecdotes, not controlled device ratings or verified failure causality**. No categorical rejection of ATB series or 1MHz operation follows.
- No controlled transformer replacement drawing, saturation/current/temperature curves, leakage/clamp, isolation or verified Japan single-unit supply identified; **BLOCKED**.

## Required revisions / counterexamples
A (#6): replace assumed pulse with **guaranteed maximum tail energy** including multi-pulse/fault shutdown latency; identify exact capacitor MPN and worst Cmin/Cmax vs bias/temp/aging; exact resistor voltage/power ratings and one-open/common-trace failures; define discharge endpoint/time through human review. Compare `Vnormal,dynamic,max < Vtrip,min` and `Vtrip,max + posttrip rise <220V` with margin and source cutoff proven independently.
B (#7/#2): provide controlled current-production transformer MPN/drawing and dated single-unit Japan supply, frequency/flux and peak/RMS current thermal calculations, real 205V/16mA load/startup/no-load stresses, rectifier/FET/snubber ratings and low-cell/PWR interactions. Forum anecdote is a risk lead only.
Do not reuse the published 350V design on HV5524.

## Work decision package — handoff to Work
**Decision requested:** reject the *obsolete DCT15EFD-U44S003 as order-ready*, keep LT3757 reference as historical comparison; prioritize sourcing a current-production controller+magnetics pair; do not fix OVP trip/capacitance/bleeder from hypothetical example.
A claim: joint Cmin/Cmax existence inequalities. B claims: transformer obsolete, substitute may overheat. Independently verified: algebra above, DigiKey obsolete listing, ADI Rev.H 100kHz 350V/10mA example. Unverified: guaranteed tail energy, true transformer thermal limit, forum anecdote, current replacement stock and actual capacitor ranges. Alternatives: MAX668 coupled, LT3757 with qualified magnetics, other 5V flyback or low-SYS flyback; all unqualified. System impacts: HV5524 220V, PWR startup and battery heating, discharge safety, sourcing/budget/Jan 2027 deadline. **Recommendation:** BLOCKED for physical selection; conditional research only.
Source report paths are the three above at starting SHA `e636652004a34e90bd07d24217e3c1d22f6fe431`. Follow-up issues #6, #7, #2. No shared indexes or KiCad modified.

## Queue and limits
Three new reports found in compare from C-012 to start SHA; **3/3 reviewed in this bounded delta**, remaining *important historical backlog* not exhaustively enumerated, exact count and oldest overall **UNKNOWN**. The oldest in this batch is Chat B 2026-11-20 21:03 JST. Next priorities: real OVP tail-energy/part evidence (#6), current-production magnetics (#2/#7), thermal charging protection (#9) and PWR startup (#8). Issue comments are follow-up separate from this file. No formal Claim, purchasing, HV energization, PCB fabrication, main merge, requirement change or safety approval.
