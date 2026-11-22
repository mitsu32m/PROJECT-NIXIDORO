# HV-001 / Issue #2 — ADI autotransformer switch/diode voltage stress and derating gate
Date: 2026-11-22 11:55 JST
Role: Chat A deep-design; NO FORMAL CLAIM
Status: PENDING REVIEW (Chat C)
Decision: CONDITIONAL for ideal topology screening; BLOCKED for component qualification

## Task contract
Question: For the ADI MAX668 non-isolated series-aiding autotransformer Figure 1c / Figure 9 / Figure 11 example, how much nominal MOSFET VDS margin and diode VRRM margin exist when extrapolated to NIXIDORO 205V/16mA and 220V ceiling?
Exit: independently calculate ideal stress, explicit assumed derating and the minimum ratio; reject unjustified transfer of 150V component ratings.
Scope excludes pin-level board reconstruction, switching waveform measurements, leakage transient and final parts approval.
Repository: codex/reva-integrated-prototype-review; branch starting commit SHA NOT VERIFIED (connector can fetch branch files but commit-list search returned default-branch results, not a reliable working HEAD). Issue #2 and required SOP/handoff/open-issues/decisions/tech-tree YAML+MD read; latest known Chat A 08:01 report read. Full current branch tree and all concurrent B/C reports NOT VERIFIED. No formal Claim; no shared index modification.

## Primary evidence
ADI/Maxim, *Small, High-Voltage Boost Converters*, 2002-07-04, https://www.analog.com/en/resources/technical-articles/small-highvoltage-boost-converters-guide.html
- Figure 1c explicitly connects the secondary in series with the primary switch node; the article states ideal switch voltage Vin+(Vout-Vin)/N, with N=(Np+Ns)/Np.
- Figure 9 / Figure 11 MAX668 benchmark: Sumida CMD-8LN 6313-T036, Np:Ns=1:9, Lp=5.6uH, Ipk=2.3A, 150V/25.5mA, reported 77% efficiency. Experimental at 150V, NOT a guarantee at 205V.
- Manufacturer article notes leakage spikes and potential snubber, and diode reverse recovery as a performance issue.
Predecessor: docs/verification/2026-11-22-0801-JST-HV-001-adi-max668-autotransformer-primary-benchmark.md.

## Independent calculation (all ideal stress numbers ASSUMED, not guaranteed)
Let n=Ns/Np=9, N=1+n=10, Vin=5.25V maximum assumed, Vout=205V nominal or 220V comparison ceiling. Series-aiding Figure 1c:
- OFF switch: VDS,ideal = Vin + (Vout - Vin)/N.
- ON diode reverse: VR,ideal ≈ Vout + n Vin, with rectifier anode near -n Vin during ON. This expression depends on actual winding dots and connection and must be independently pin-checked against Figure 9.
- At Vout=205V: VDS=25.225V; VR=252.25V.
- At Vout=220V: VDS=26.725V; VR=267.25V.
- Ideal 30V FET headroom at 220V = 3.275V (10.9% of rating). 30V is NOT qualified: ringing, tolerance, switching overshoot and abnormal conditions unknown.
- A 250V diode fails even ideal 205V at Vin=5.25V; a 300V diode has 32.75V ideal margin at 220V (10.9% of rating), without ringing.
- As an explicitly ASSUMED design screen, reserve 20% of MOSFET VDS rating for unmodeled transient/derating (ideal VDS <= 0.8*rating). This is not a manufacturer requirement or verified adequate margin.
  * 30V rated: allowed ideal <=24V, 1:9 FAILS at 220V. Required N >= (220-5.25)/(24-5.25)=11.4533, or n >=10.4533.
  * 40V rated: allowed ideal <=32V, 1:9 PASSES ideal screen (26.725V), but 5.275V remains to 80%-rating budget; actual transients unbounded.
  * 60V rated: allowed ideal <=48V, ideal screen passes; selection still depends on Qg/Rds(on)/gate drive and switching loss.
- A diode with assumed 20% voltage margin would need rated VRRM >=267.25/0.8=334.06V at 220V, so 300V FAILS this assumed screen; 400V PASSES ideal static screen only.
- Changing n to reduce MOSFET voltage raises diode reverse voltage, so ratio and component ratings are coupled. At 220V, Vin=5.25V, n=11: VDS=23.146V and diode VR=277.75V. Higher n also changes leakage/coupling, magnetics loss and attainable duty.

## Failure and thermal checks
- At 205V/16mA, output 3.28W. 77% efficiency extrapolation implies 4.26W input, 0.98W converter dissipation, but 77% is REPORTED at 150V/25.5mA only. At 4.75V, nominal input 0.897A under this ASSUMPTION, not a guaranteed current.
- At startup/open load, Vout and control behavior can depart from steady-state assumptions. An independent OVP and hard stop must bound voltage and tail energy; 220V is NOT an acceptable fault setpoint merely because HV5524 recommends a 220V ceiling.
- VDS and diode reverse-recovery transient require controlled schematic/pinout, leakage L, diode Qrr/trr, MOSFET Coss and layout parasitics; absent these, no MOSFET/diode selection or thermal approval.
- Non-isolated output and stored HV energy remain hazardous even after controller shutdown.

## Conclusions
CONDITIONAL: ADI Figure 1c gives a topology-specific ideal stress model; 30V FET and 250V diode have insufficient ideal/static margin for a robust 205V design at the stated corner. 40V FET/400V diode classes are only *screening categories*, not chosen parts.
NO-GO (limited): 250V diode under 205V/5.25V/n=9 ideal conditions; 30V FET under the explicitly ASSUMED 20% derating screen at 220V.
BLOCKED: exact schematic/dots, sourceable transformer, rated FET/diode with measured/estimated switching stress, guaranteed current limit, thermal, startup, independent OVP and discharge, 205V/16mA proof.
PENDING REVIEW: Chat C must independently check rectifier polarity/equation and source figure before Work adopts any finding.
Next: recover Figure 9 and winding manufacturer drawing, build pin-level ON/OFF node table, then obtain actual FET and diode manufacturer MPNs and transient/thermal bounds. Do not repeat ideal DCM screens.
No purchasing, PCB fabrication, HV energization, main merge, or requirements changes.
