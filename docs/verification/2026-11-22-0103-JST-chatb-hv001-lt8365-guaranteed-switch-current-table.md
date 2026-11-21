# Chat B — HV-001 / SYS-001: LT8365 guaranteed switch-current threshold and worst-case distinction
Date: 2026-11-22 01:03 JST
Status: **PENDING REVIEW**. Role: wide-research, **NO FORMAL CLAIM**. Decision: **CONDITIONAL evidence improvement; 5V/205V/16mA hardware feasibility BLOCKED**.
Repository: mitsu32m/PROJECT-NIXIDORO; branch: codex/reva-integrated-prototype-review.
Starting branch HEAD: **affed18303174055c1eeafa8b30d7283839b9b16**, obtained from exact GitHub branches REST endpoint before this write.

## Task contract
Related Issues: #10 (HV-001), #7 (PROTO-001), #4 (SYS-001). Narrow question: what guaranteed switch-current limits, unlike headline ratings, are available from the manufacturer's LT8365 Rev.A electrical table, and how do they change the previous 5V proxy? Excludes real DC2838A current tracing, adoption and hardware test authorization. Exit: exact min/typ/max with conditions, calculation, and next proof requirements.

## Source state and primary evidence
Read docs/ai-workflow.md, docs/verification/handoff.md, docs/verification/open-issues.md, docs/verification/decisions.md, docs/tech-tree.yaml, docs/tech-tree.md, recursive branch tree, latest A 2026-11-22 00:00 and B 2026-11-21 21:00 reports, C-REVIEW-016, and repository Issues search. Issue Claim atomicity/ownership not proven; research is provisional. Shared index files intentionally left to Work.

**ADI LT8365 Rev.A datasheet, page 3, ELECTRICAL CHARACTERISTICS, 'Switch Maximum Switch Current Limit Threshold': MIN 1.5A, TYP 2A, MAX 2.7A, with full-temperature 'l' marker.** Test header: VIN=12V, EN/UVLO=12V unless otherwise noted. Thus the published 1.5A headline is the guaranteed **minimum current-limit threshold**, not the typical threshold. 2.7A is the upper threshold corner relevant to inductor saturation/fault stress. These are current-limit threshold values, **not a guarantee that any proposed converter can deliver 1.5A continuously**, nor a 5V circuit qualification. ADI primary PDF: https://www.analog.com/media/en/technical-documentation/data-sheets/lt8365.pdf ; product page: https://www.analog.com/en/products/lt8365.html . Check exact grade and Note 3 temperature qualification: E grade 0..125C guaranteed; J/H -40..150C guaranteed. Page 14 recommends inductor withstand >=2.7A without saturation for ordinary boost, and steady-state peak <=1.5A including tolerances; do not transfer boost guidance blindly to DC2838A charge pump.

## Reproduction of prior necessary-condition proxy, NOT actual DC2838A current
TARGET: Pout=205V*0.016A=3.280W. ASSUMED: 5V input, L=10uH, f=400kHz, D=0.95, ηHV=0.80/0.75/0.70. Simple CCM input-inductor proxy:
Iavg=Pout/(ηHV Vin), ΔIL=Vin D/(L f)=1.1875A, Ipeak_proxy=Iavg+ΔIL/2.
| Assumed ηHV | Iavg A | Ipeak_proxy A | margin to guaranteed MIN 1.5A |
|---|---:|---:|---:|
| 0.80 | 0.8200 | 1.41375 | +0.08625A |
| 0.75 | 0.87467 | 1.46842 | +0.03158A |
| 0.70 | 0.93714 | 1.53089 | -0.03089A |
At 4.5V and η=.75: Iavg=.97185A, ripple=1.06875A, Ipeak_proxy=1.50623A, margin=-0.00623A.
These calculations are **not** actual switch peak values because DC2838A charge pump can split or alter currents, actual duty is not established, and L/f tolerances, startup, and losses are absent. They cannot prove NO-GO or GO. Important correction relative to earlier reports: the manufacturer does provide an explicit full-temperature minimum threshold of 1.5A under datasheet conditions; it is not merely an unspecified 'headline'. Verify applicability at VIN=5V and grade/temperature before adopting.

## Other necessary conditions, thermal and fault
USB-only 5V*500mA=2.5W ideal is less than 3.28W output, impossible at full target. At ηHV=.75 HV input is 4.373W; even ideal USB 2.5W leaves >=1.873W to supply via battery/other path before 5V-stage loss, logic, charge and BATFET losses. USB+BAT may be net discharging; do not claim simultaneous charging. Battery-only minimum SYS and protection current are UNKNOWN. LT8365 RDS(on) typical 0.7ohm at ISW=.5A (Rev.A p3) is NOT a guaranteed loss bound at 1.5A. Max current-limit corner 2.7A, fault >3A, thermal shutdown and restart require separate magnetics saturation, diode/flying-cap RMS, PCB heat, enclosure cell-temperature and OVP energy verification. HV5524 recommended 220V must not be treated as fault-safe limit. 205V/16mA target unchanged.

## Candidate comparison / sourcing
- LT8365 + DC2838A charge pump: IC recommended for new designs by ADI; reference board 9..30V, +250V/10mA, NOT 5V/205V/16mA; exact 10uH inductor and semiconductor ratings require actual stress analysis. 5V input feasibility **BLOCKED**.
- LT3757 + TDK DCT15EFD-U44S003 flyback: reference 5..12V/350V/10mA; TDK magnetics previously distributor-marked obsolete; replacement qualification **BLOCKED**.
- MAX668 + coupled magnetics: separate A 00:00 report ruled out only fully-reset isolated 40uH DCM proxy in advertised oscillator range, NOT original coupled or CCM implementation; **BLOCKED**.
- Direct-SYS flyback: potential 5V-stage loss elimination, but actual sourceable pair and low-cell qualification **BLOCKED**.
Current Japanese single-quantity stock, landed price, lead times and exact alternative magnetics: **UNKNOWN** (not freshly checked in this run). No fabricated sourcing claims.

## Chat C review and Work integration handoff
Review specifically (1) Rev.A p3 1.5/2/2.7A table, temperature grade and VIN=12V header; (2) whether 5V operation retains the threshold guarantee and applicability of ordinary-boost p14 advice to DC2838A; (3) topology-specific actual SW and flying-cap current path, worst-case L/f/D and inductor saturation >=2.7A corner; (4) USB/BAT sign and thermal implications. Next B task should find **sourceable, currently manufactured controller+magnetics pairs**, rather than repeating hypothetical current proxy. SOP proposal for Work: distinguish datasheet MIN limit threshold from headline current rating, and MAX corner for magnetics/fault, recording test conditions and grade.

No purchasing, fabrication, HV energization, main merge, specification changes, schedule changes or shared SOP edit performed.
