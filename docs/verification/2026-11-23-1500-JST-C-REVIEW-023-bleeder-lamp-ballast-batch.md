# C-REVIEW-023 — SYS-002 bleeder and HV-004 ballast batch

Date: 2026-11-23 15:00 JST. Role: Chat C independent first review. **No formal Claim; no hardware safety approval.**
Branch: codex/reva-integrated-prototype-review. Starting HEAD: `62539b00fd863281ebdbc8c99e83e2dcfb590cca`.

## Scope and evidence
Reviewed required docs/ai-workflow.md, docs/verification/{handoff,open-issues,decisions}.md, docs/tech-tree.{yaml,md}, current tree and open Issues; A 2026-11-23 11:55 SYS-002 and B 09:00/13:03 HV-004. Related #6, #4, #7, #8, #9. Previous C-REVIEW-022 is the baseline. Existing PWR/HV KiCad paths were located; **no complete electrical netlist or component cross-check was performed**, so real design fit remains UNKNOWN. GitHub Issue labels are empty; PENDING REVIEW is in report text, not a verified formal queue claim. No independent manufacturer PDF body retrieved in this run: B's primary AC-only and secondary tube citations remain unverified directly.

## Independent calculations and rulings

1. **A SYS-002:** ACCEPTED (assumed ideal RC arithmetic only): ln(220/60)=1.299282984; at Cmax=12uF and Rmax=346.5kohm, t=5.402419s; max actual R for 5s=320.690kohm; maximum nominal R at +5%=305.419kohm. Two parallel 680kohm paths yield R=340kohm, t=5.301075s; one open gives 10.602149s. At Rmin=313.5kohm, P(220V)=154.386mW. E(220V,Cmax)=290.400mJ. **CHANGES_REQUESTED** for any assertion nominal 330kohm/10uF guarantees <=5s; **BLOCKED** for physical discharge safety. The 5s/60V thresholds are assumed, not accepted safe-touch criteria. Converter tail, capacitor bias/tolerance, working voltage, resistor single-open and enclosure heat unknown.

2. **B HV-004 09:00:** ACCEPTED (arithmetic only) for I=2Id+12In, and 205V * 12mA=2.46W, and 2.46/(0.75*0.9)=3.64444W. **CONDITIONAL** source-classification: 110VAC/68kohm NE-2 test cannot certify 205V DC; IN-12B figures are secondary supplier figures. 16mA remains target, not an adopted 12mA requirement. Actual DC lamp lots and simultaneous-mode truth table UNKNOWN.

3. **B HV-004 13:03:** ACCEPTED (assumed ideal ballast arithmetic only): each digit (205-145)*.003=0.180W; each neon (205-60)*.0005=0.0725W; total ballast 2*.180+12*.0725=1.230W. Lamp dissipation 2*.435+12*.030=1.230W, and Pbus=2.460W. HV converter loss 2.46*(1/.75-1)=0.820W, SYS→5V loss (2.46/.75)*(1/.9-1)=0.36444W. SYS input=3.64444W, **not 3.644W additional heat beyond bus output**. **CONDITIONAL** for physical distribution; sealed PETG thermal resistance, selected resistor derating, voltage rating and thermal coupling UNKNOWN.

4. **B shorted digit:** ACCEPTED (ideal steady resistor model) I=205/20000=10.25mA and P=2.10125W. **BLOCKED** as fault qualification: upstream current limiting, actual resistor tolerance and thermal-fuse response, sustained fault duration, switch behavior and HV capacitor transient not verified. Do not adopt 0.25W or 0.5W parts from nominal power alone.

## Cross-check and adversarial cases
- A's bleeder heat is **additional to** the B lamp/ballast load if the bleeder is connected during operation; B's 12mA scenario excludes I_aux and therefore cannot represent full 205V bus current. For example at 205V/330kohm, ideal bleeder draws 0.6212mA and 0.12735W, making a 12mA lamp-only example at least 12.6212mA before driver/divider loads. At 220V/Rmin, thermal worst corner is higher. **CHANGES_REQUESTED** for any SYS budget treating lamp-only bus current as total current.
- If the digit shorts, the resistor's ~2.10W steady dissipation greatly exceeds nominal 0.18W; time-to-failure, high-voltage cut and energy-release path are unresolved. PWM lowers average heating only if mode timing and fault behavior are bounded, not instantaneous fault stress.
- An active discharge network reduces steady bleeder heat only conditionally and introduces switch-open, supply-loss and sensing faults. No architecture approved.
- Voltage at 60V is not independently qualified as safe to touch. No new requirements, thresholds, parts or schematics adopted.

## Work decision package (handoff to Work)
**Decision:** Keep 205V/16mA requirement and no-release status. Require a joint, mode-specific bus power and heat worksheet covering lamp ballast, bleeder, divider, driver, conversion losses and startup, with Cmin/Cmax and single-open/fault discharge. A: conditional RC corner arithmetic; B: conditional AC-vs-DC source classification and ballast/fault arithmetic. Independent evidence is the calculations above; manufacturer-controlled lamp and passive component limits and actual KiCad connectivity are NOT independently checked. Alternatives: continuous passive bleeder (steady heat), two individually sized redundant branches (higher steady heat), or supervised active discharge (fault and supply dependencies). System effects: HV output demand, PWR/BAT heat, 21700 temperature, resistor PCB area, discharge safety, initial BOM. Recommendation: Work should maintain BLOCKED hardware adoption, ask A for bounded single-fault discharge and B for exact DC lamp MPN/lot and resistor derating, then revisit architecture with traceable parts. No duplicate issue; #6 and #4/#7 already cover.

Source reports:
- https://github.com/mitsu32m/PROJECT-NIXIDORO/blob/62539b00fd863281ebdbc8c99e83e2dcfb590cca/docs/verification/2026-11-23-1155-JST-SYS-002-bleeder-tolerance-single-open-envelope.md
- https://github.com/mitsu32m/PROJECT-NIXIDORO/blob/62539b00fd863281ebdbc8c99e83e2dcfb590cca/docs/verification/2026-11-23-0900-JST-chatb-hv004-lamp-current-primary-vs-16ma-target.md
- https://github.com/mitsu32m/PROJECT-NIXIDORO/blob/62539b00fd863281ebdbc8c99e83e2dcfb590cca/docs/verification/2026-11-23-1303-JST-chatb-hv004-ballast-heat-and-mode-envelope.md
- https://www.taydaelectronics.com/datasheets/files/1039.PDF (manufacturer AC-only PDF cited by B, not independently opened)
- https://www.tube-tester.com/sites/nixie/data/in-12b.htm (secondary cited by B, not independently opened)

## Next review and exclusions
Next P0: OVP stop-tail+Cmin/Cmax and single-fault discharge; battery-only temperature enforcement/charger inhibit; real HV magnetic/controller pairing; PWR startup and enclosure heat. Historical backlog complete count remains UNKNOWN; oldest unreviewed issue must be established by full report-to-review audit. No purchasing, PCB fabrication, HV energization, main merge, safety approval, requirements change, or scheduler change.
