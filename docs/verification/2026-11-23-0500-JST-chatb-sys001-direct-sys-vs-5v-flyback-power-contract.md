# Chat B — SYS-001 / HV-001 direct-SYS vs 5V flyback power contract
Date: 2026-11-23 05:00 JST
Status: **PENDING REVIEW**; scoped outcome **CONDITIONAL (architecture comparison only)**; physical feasibility **BLOCKED**
Role: Chat B wide research; formal Claim: **NONE**
Branch: `codex/reva-integrated-prototype-review`
Starting HEAD SHA: **UNKNOWN** — GitHub branch-search connector returned branch name without commit SHA; repository-wide recent-commit search does not establish branch HEAD. Do not confuse file blob SHA with commit SHA.
Related Issues: #4 SYS-001A, #7 PROTO-001, #2 HV-001A, #10 LT8365.
Scope: novel direct-SYS versus cascaded 5V power-path contract; not a repeat of LT8365 current-limit or cell PCM screening.
Exit: algebraically bound the benefit and specify proof gates, not adopt any hardware.

## Repository state and prior work
Read live branch `docs/ai-workflow.md`, `docs/verification/handoff.md`, `docs/verification/open-issues.md`, `docs/verification/decisions.md`, `docs/tech-tree.yaml`, `docs/tech-tree.md`. Recent report context from prior Chat B run 2026-11-23 01:00 JST: LT3757A + Coilcraft Q4434/Q4435/TA7608 not yet qualified. GitHub issue search returned #4, #7, #10 and other tasks; formal atomic Claim protocol unverified. Continue provisionally, no Claim.

## Evidence classification
- TARGET/ASSUMED: HV 205V, 16mA simultaneous continuous; Pout=3.280W. Display-current and simultaneous-lamp requirements remain unverified, not measured.
- ASSUMED: eta_5V=0.90; eta_HV_from_5V=0.75; eta_HV_direct=0.75 or 0.70. These are scenario parameters, not manufacturer guarantees.
- GUARANTEED manufacturer product-feature scope: ADI LT3757A 2.9–40V controller supply, supports flyback, frequency adjustable 50kHz–1MHz; **not** proof of 3V/205V/16mA with any transformer. Source: https://www.analog.com/en/products/lt3757.html (Rev.H product page, accessed 2026-11-23).
- Manufacturer product features: TI BQ25185 input-limit options 100/500/1100mA, power path and battery supplementation; 3.125A *device feature* not an unconditional pack/system safe current. Source: https://www.ti.com/product/BQ25185 (Rev.B product page, accessed 2026-11-23).
- UNKNOWN: actual 1S cell low-voltage at BAT/SYS under load, switch current and duty at low input, transformer part and leakage, independent OVP, full-system temperature, distributor stock/prices.

## Calculation: steady-state mode contract
For Pout=205*0.016=3.28W:
A: SYS->5V->HV: P_SYS = Pout/(eta_5V*eta_HV) = 3.28/(0.9*0.75) = **4.859W**.
B: SYS->HV direct at 75%: P_SYS = 3.28/0.75 = **4.373W**.
C: SYS->HV direct at 70%: P_SYS = 3.28/0.70 = **4.686W**.
At equal 75% HV efficiency direct route saves 0.486W (10.0% of cascaded SYS power), but direct topology may be less efficient. C still saves 0.173W. Direct is beneficial **iff** eta_direct > eta_5V*eta_HV_from_5V = **0.675** (for identical loads and no extra path overhead). At 67.5% the two routes tie; below it direct is worse. Thus direct-SYS is a measurable tradeoff, not automatically preferred.

USB-only: 5V*0.500A=2.50W ideal; BQ25185 programmed 500mA is not guaranteed 500mA available. 3.28W output violates energy conservation even before loss; USB-only full display NO-GO.
USB+BAT: optimistic USB 2.50W delivered without loss to SYS yields minimum battery supplement at SYS of A 2.359W, B 1.873W, C 2.186W. At BAT 3.0V and ideal BAT path, A 0.786A, B 0.624A, C 0.729A. These are *optimistic lower bounds*, not rated continuous currents; actual VIN input-limit min, BQ path, BATFET, protection, control power, and voltage sag increase requirements.
BAT-only at ideal BAT 3.0V: A 1.620A, B 1.458A, C 1.562A; actual currents larger.
Net USB charging while continuous 16mA full display: impossible at 500mA even with perfect conversion. Reduced simultaneous lamp current and dimming are *proposals only*.

## Practical qualification gates
1. Verify actual lamp DC I-V/current per lamp and worst simultaneous count including neon, IN-12B, ballast losses, HV5524. 16mA remains TARGET, not demonstrated requirement.
2. Two separate controller+magnetics BOM pairs: LT3757A external-switch direct-SYS flyback, and MAX668 coupled-inductor or isolated/nonisolated 5V flyback. Exact transformer primary inductance, turns ratio, Isat, leakage, insulation, temperature, price and lead-time mandatory; no current pair qualifies. The prior Q4434/Q4435/TA7608 are not approved HV transformer substitutes.
3. Sweep VIN/SYS low battery to 4.5V/5V, full 3.28W, no load, startup, abrupt off; include MOSFET VDS including leakage overshoot, diode reverse stress, winding insulation, output-capacitance startup energy, efficiency and junction/cell temperatures.
4. Independent HV OVP below HV5524 recommended 220V including tolerances and transient energy, hard-off and safe discharge. No HV energization.
5. Model BQ25185 DPPM/supplement and 500mA USB input separately; charge and discharge thermal enforcement independent, not implied by BAT OCP.

## New decision and handoff
**CONDITIONAL**: Direct-SYS can save 0.486W at equal 75% HV efficiency, but requires >67.5% direct efficiency to outperform a 90%*75% cascade. **BLOCKED**: no selected magnetic/controller pair, no proof of temperature, fault or sourcing; not order-ready.
Chat C: independently audit inequality and whether BQ current limits permit claimed lower-bound scenarios; do not promote ASSUMED efficiency to guaranteed.
Work: consider adding explicit mode-dependent efficiency crossover and battery supplement to SYS-001 acceptance criteria; update shared indices only through designated integrator. Do not directly edit `docs/ai-workflow.md`.
Next Chat B: source exact DC neon/IN-12B current and simultaneous count, then a real transformer pair with manufacturer leakage/Isat and domestic single-unit availability.
Forbidden actions not performed: purchase, PCB manufacturing, HV energization, main merge, spec change, scheduler change.
