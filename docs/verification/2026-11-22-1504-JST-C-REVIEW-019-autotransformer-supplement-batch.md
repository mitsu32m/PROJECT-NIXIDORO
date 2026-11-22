# C-REVIEW-019 — autotransformer stress and BQ25185 supplement bounds
Date: 2026-11-22 15:04 JST
Role: Chat C independent first review; NO FORMAL CLAIM
Branch: `codex/reva-integrated-prototype-review`
Starting HEAD: `485c9b9e16924e0bf50cb958211c383d38867240` (fetch_commit of branch ref)
Disposition: CONDITIONAL / CHANGES_REQUESTED / BLOCKED; NOT hardware safety approval

## Task and evidence scope
Reviewed required SOP, handoff, open-issues, decisions, tech-tree YAML and MD at working branch, Issue #2/#4/#6/#8/#9 descriptions, and two newly added A/B reports since C-018, identified by GitHub compare C-018 commit `d3d4a2dd2199b2c1d3f54fedbaab62ba946c86dc` to working branch (ahead 2 commits). No shared index edited. No formal claim. Full KiCad pin-level verification, manufacturer figure inspection and manufacturer PDF direct read were NOT performed this run. Issue state/labels across all issues not exhaustively reconciled. Independent checks below are algebraic and explicitly conditional.

Input A: [HV-001 11:55](https://github.com/mitsu32m/PROJECT-NIXIDORO/blob/485c9b9e16924e0bf50cb958211c383d38867240/docs/verification/2026-11-22-1155-JST-HV-001-adi-autotransformer-switch-diode-stress-derating.md).
Input B: [SYS-001 13:00](https://github.com/mitsu32m/PROJECT-NIXIDORO/blob/485c9b9e16924e0bf50cb958211c383d38867240/docs/verification/2026-11-22-1300-JST-chatb-sys001-bq25185-threshold-current-corners.md).
A primary cited: ADI, *Small, High-Voltage Boost Converters*, 2002-07-04, https://www.analog.com/en/resources/technical-articles/small-highvoltage-boost-converters-guide.html (specific Figure 1c/9 not independently inspected here).
B primary cited: TI BQ25185 SLUSF65B Rev.B, https://www.ti.com/lit/ds/symlink/bq25185.pdf (table transcription NOT independently verified against PDF in this run).

## Claim-level review: A, Issue #2
1. **ACCEPTED (algebra only):** with series-aiding topology *as described*, N=10, Vin=5.25V, Vout=205/220V, VDS=Vin+(Vout−Vin)/N gives 25.225/26.725V. Diode reverse model Vout+9Vin gives 252.25/267.25V. These are ideal static equations, NOT verified node voltages without original winding dots.
2. **ACCEPTED (arithmetic only):** 30V MOSFET 20%-reserve screen: 0.8*30=24V; N>= (220−5.25)/(24−5.25)=11.4533, n>=10.4533. 40V screen 32−26.725=5.275V reserve to assumed 80% threshold. 300V diode at 220V has 32.75V absolute margin, but fails assumed 20% reserve; 267.25/0.8=334.0625V. 400V only passes this ideal screen.
3. **CONDITIONAL:** series-aiding circuit's diode anode polarity and n=9 mapping must be independently verified from ADI original Figure 9 and actual Sumida winding drawing; ON/OFF node table required. Ideal switch VDS may be exceeded by leakage spikes and fault transients.
4. **CHANGES_REQUESTED:** phrase '30V FET insufficient for robust design' must remain tied to *assumed* 20% margin, not a guaranteed derating criterion. Ratio changes simultaneously change diode stress, magnetic loss, and drive.
5. **BLOCKED:** real 205V/16mA continuous topology, 30/40/60V FET, 300/400V diode, snubber, thermal, startup and OVP qualification.

## Claim-level review: B, Issue #4
1. **ACCEPTED (arithmetic only):** 205*0.016=3.28W; 3.28/(0.75*0.90)=4.859259W; nominal 5V*0.450=2.25W; deficit 2.609259W; ideal battery contribution at 3.0V=0.869753A, 3.6V=0.724794A. These use ASSUMED converter efficiencies, zero auxiliary demand and lossless IN→SYS.
2. **ACCEPTED (necessary condition):** 5V*0.498=2.49W <3.28W; at nominal 5V, even lossless USB-only full target is impossible under the stated 498mA ceiling. It does not prove a specific supplement current can be delivered.
3. **CHANGES_REQUESTED:** B calls the 2.609W deficit a 'lower bound' for assumed efficiencies. It is only conditional on those efficiencies and a 450mA actual source contribution. The 450mA MIN input current-limit threshold is NOT guaranteed source delivery; actual input could be lower, increasing battery burden. At a source above 450mA the deficit can be smaller. Present a parametric equation: Pbat,needed >= max(0,Pout/(etaHV*eta5)+Paux−Pin_to_SYS), with Pin_to_SYS <= Vin*Iin; do not equate threshold with available supply.
4. **CONDITIONAL:** BQ25185 450/475/498mA, supplement 40/20mV typical, UVLO 3V typical, BATOCP 3.13A typical, BATFET 115/140mOhm values are reported by B from TI Rev.B but **NOT independently transcribed in this run**. Do not combine typical thresholds into guaranteed handoff/brownout bounds.
5. **BLOCKED:** continuous battery supplement, cell PCM current/temperature, battery-only TS, charging inhibit, startup and full 205V/16mA operation. Under stated USB-only load full-output operation cannot net-charge the battery.

## Cross-system counterexamples and Work decision package
- **Decision requested of Work:** keep both ADI autotransformer and USB+BAT supplement as comparison candidates only; do NOT select a MOSFET, diode, transformer, cell, charger thermal cutoff or operating mode. Existing 16mA target unchanged.
- **Counterexamples:** 220V steady output plus switching ringing can exceed 30V VDS/300V VRRM even if ideal static margin is positive. At BAT near typical UVLO, supplement can disappear while HV capacitor is charged; stop, OVP and discharge must be independent of MCU and charge /CE.
- **Alternatives:** 40/60V MOSFET and 400V diode are *voltage-class screens*, not parts; alternate isolated flyback or charge-pump candidates remain unqualified. USB reduced-load mode needs owner approval if it changes required behavior.
- **System impacts:** HV-001/#2, HV-002/#6, SYS-001/#4, PWR-002/#8, THERM-001/#9, BAT-001/#7 and prototype BOM; no release gate opened.
- **Required evidence:** original ADI schematic and Sumida winding dots; selected actual transistor/diode datasheets with voltage/temperature/leakage and recovery, worst-case ringing/thermal; TI Rev.B table direct check; real USB source and BQ power-path tests under supervised low-voltage plan; pack PCM and enclosure heat; independent HV OVP stop/tail energy and discharge.
- **Work handoff:** integration lead / Work; review is NOT adoption, purchase approval or safety signoff.

## Queue accounting and next priority
New A/B reports since C-018: **2**; reviewed this run: **2**; newly discovered remaining from that compare: **0**. Older unreviewed important reports across entire history: **UNKNOWN** (full historical report-to-review/Issue reconciliation not completed). Oldest in this bounded batch: A 2026-11-22 11:55 JST. Oldest project-wide waiting: UNKNOWN.
Next: #6 independent OVP with Cmin, tail energy and fault discharge; #2 actual Figure 9 winding/pin stresses; #9 thermal enforcement and #8 low-cell startup. Preserve shared index ownership. No procurement, PCB release, HV energization, main merge, specification change or scheduler action.
