# HV-001 / Issue #2 — Joint MOSFET/diode voltage-rating feasibility vs winding ratio
Date: 2026-11-22 16:03 JST
Role: Chat A deep-design
Review: PENDING REVIEW; NO FORMAL CLAIM
Disposition: CONDITIONAL mathematical screen; BLOCKED physical qualification

## Task contract
Question: Does a winding ratio exist that simultaneously satisfies an assumed voltage-rating fraction for both the switch and rectifier in the ADI series-aiding autotransformer model? This is a joint constraint, not another isolated rating comparison.
Exit: algebraic feasible interval, counterexamples, and conditions that invalidate the model.
Branch: codex/reva-integrated-prototype-review. Starting HEAD SHA: UNKNOWN (GitHub connector provided file blob SHA but not authoritative branch commit SHA). No Claim mechanism was verified, so no formal Claim asserted.
Sources read: docs/ai-workflow.md, docs/verification/handoff.md, docs/verification/open-issues.md, docs/verification/decisions.md, docs/tech-tree.yaml, docs/tech-tree.md, Issue #2 and 2026-11-22-1155-JST-HV-001-adi-autotransformer-switch-diode-stress-derating.md. Full latest report tree / concurrent Chat B/C coverage NOT VERIFIED.

## Evidence and model
Manufacturer source: Analog Devices, Small, High-Voltage Boost Converters, 2002-07-04, https://www.analog.com/en/resources/technical-articles/small-highvoltage-boost-converters-guide.html . Figure 1c topology and MAX668 example are cited by predecessor. Manufacturer pin-level Figure 9 / magnetics drawing NOT independently recovered in this run. The equations are CONDITIONAL on that topology and rectifier polarity, not guaranteed for a different connection.

Define n=Ns/Np>0, N=1+n, Vin=5.25 V (ASSUMED high input), Vout=220 V (ASSUMED comparison ceiling, NOT fault trip target), alpha=0.8 (ASSUMED fraction of component rating allocated to ideal voltage; NOT a safety standard).
Vds_ideal=Vin+(Vout-Vin)/(1+n).
Vr_ideal=Vout+n*Vin (requires diode polarity verification).
Necessary constraints Vds_ideal <= alpha*Vfet and Vr_ideal <= alpha*Vdiode imply:
n_min=(Vout-Vin)/(alpha*Vfet-Vin)-1, provided alpha*Vfet>Vin.
n_max=(alpha*Vdiode-Vout)/Vin, provided alpha*Vdiode>=Vout.
A simultaneous candidate exists only if max(0,n_min)<=n_max; this is necessary, never sufficient.

## Independent numeric screen (all ASSUMED)
At Vin=5.25 V, Vout=220 V, alpha=0.8:
| FET rating | Diode rating | n_min | n_max | Result |
|---|---|---:|---:|---|
| 30 V | 300 V | 10.453 | 3.810 | NO-GO within model |
| 40 V | 300 V | 7.028 | 3.810 | NO-GO within model |
| 60 V | 300 V | 4.023 | 3.810 | NO-GO within model |
| 30 V | 400 V | 10.453 | 19.048 | CONDITIONAL interval |
| 40 V | 400 V | 7.028 | 19.048 | CONDITIONAL interval |
| 60 V | 400 V | 4.023 | 19.048 | CONDITIONAL interval |

Example n=9: 40V FET/400V diode: Vds=26.725V <=32V and Vr=267.25V <=320V, passing *only* this static assumed screen. 40V/300V cannot be fixed by choosing another n under the same assumptions: reducing n to ease diode stress raises Vds above its budget.
The inequality can also be rewritten as a coupled rating requirement: alpha*Vdiode >= Vout + Vin*[(Vout-Vin)/(alpha*Vfet-Vin)-1]. A higher MOSFET rating may permit a smaller n, easing diode stress, but does not establish physical efficiency.

## Limitations / adversarial review
These numbers do not include switch-node ringing, leakage inductance, diode recovery, Coss/Qg, winding resistance, insulation, controller duty limit, peak current, low-Vin behavior, startup/open-load/OVP transient, aging, tolerance, temperature or PCB parasitics. At low Vin the required duty and current may dominate even if voltage stress decreases. Actual maximum Vin and 220V comparison must be replaced by controlled circuit corners; 20% reservation is arbitrary and NOT a guaranteed safe derating. Voltage ratings are component absolute maxima, not normal operating targets. Manufacturer example 150V/25.5mA at 77% does not qualify 205V/16mA.

## Outcome and next evidence gate
CONDITIONAL: A closed-form necessary joint voltage-rating interval was derived.
NO-GO (limited): 30/300, 40/300, and 60/300 V rating pairs cannot simultaneously meet the assumed 80%-rating static screen at 220V/5.25V in this topology model.
BLOCKED: pin/dot verified actual circuit, qualified magnetics and real component MPNs, transient upper bounds, peak currents, losses/thermal, startup, OVP hard stop and discharge. No design adoption.
PENDING REVIEW: Chat C must independently verify the diode polarity and the joint inequalities. Work should integrate only after review.
No shared index edited. No purchases, PCB manufacturing, HV energization, main merge or requirements changes.
