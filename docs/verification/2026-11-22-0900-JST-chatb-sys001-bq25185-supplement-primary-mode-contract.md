# Chat B — SYS-001: BQ25185 battery supplement mode, primary-source contract
Date: 2026-11-22 09:00 JST (research window; precise execution time not independently verified)
Status: **PENDING REVIEW**; scoped decision **CONDITIONAL** for documented mode semantics, **BLOCKED** for full-load electrical/thermal qualification. **NO FORMAL CLAIM**.
Repository: mitsu32m/PROJECT-NIXIDORO; branch: codex/reva-integrated-prototype-review.
Starting branch HEAD: **UNKNOWN** — connector branch search exposes branch name but not commit SHA; GitHub REST branch API was inaccessible through available web fetch. Do not confuse a file blob SHA with HEAD.
Parent: SYS-001; issue #4, related #7/#8/#9/#10. Chat B research only.

## Startup and duplication check
Read docs/ai-workflow.md, docs/verification/handoff.md, docs/verification/open-issues.md, docs/verification/decisions.md, docs/tech-tree.yaml and docs/tech-tree.md, GitHub open issue search, and prior 2026-11-22 05:00 Chat B SYS-001 report. Existing #4 covers mode semantics; this report adds **TI Rev.B primary text** rather than repeating hypothetical efficiency screens. Issue search lacks reliable labels/assignee/state metadata; safe atomic Claim cannot be demonstrated. No Claim asserted. Shared index files intentionally not modified.

## Manufacturer primary evidence (GUARANTEED descriptive behavior; not current capacity guarantee)
TI **BQ25185**, datasheet **SLUSF65B Rev.B, revised August 2026**, section **6.3.2 DPPM**, **6.3.3 Battery Supplement Mode**, **6.3.4 Sleep**, **6.3.5 SYS Regulation**, **6.3.6 ILIM/VSET** (p.15): https://www.ti.com/lit/ds/symlink/bq25185.pdf

1. DPPM gives SYS load priority over charge current: when input-current budget is reached, charging current is reduced. Only **after charge current reaches zero and SYS falls below the supplement threshold VBSUP1** can the battery supplement system load. Supplement stops at VBSUP2. Thus *battery supplement while USB is present is an explicitly documented mode*, not merely inferred from a marketing label.
2. TI explicitly states **battery supplement current is not regulated**, although BAT OCP remains active. Battery voltage must exceed BAT UVLO. This is not a guarantee of 3.28W HV load, acceptable BATFET dissipation, or transient continuity.
3. TI states **charge termination disabled during supplement**; do not report concurrent net charging as the default when input limit is saturated.
4. The charge-enable pin controls charging, not all SYS loads; TI's charge-process description notes supplement behavior is independent of CE. Consequently an asserted /CE charge inhibit is not an HV power cut.
5. Input current limiting is on **IN**, not a 500mA guaranteed output at SYS. Actual SYS voltage varies with supply, cell voltage, DPPM and mode; power balance must use V_IN*I_IN, BAT/SYS voltage and losses, not assume a lossless 5V SYS.
6. In battery-only mode, prior handoff cites Rev.B §6.4 p19 TS Measurement=NO. Thus battery-only thermal enforcement remains separate (#9); do not infer that a connected NTC protects battery-only load operation.

## Quantitative necessary conditions (ASSUMED efficiencies; no measurements)
Target 205V * 0.016A = **3.280W** (project TARGET, not demonstrated lamp demand).
USB input configured 5V/500mA gives **at most 2.50W** ideal (actual current-limit tolerance and USB supply conditions may reduce this). Since P_HVout > P_USB,in, **USB-only continuous 16mA NO-GO**, even before loss.
For a SYS→5V→HV chain, P_SYS,load = (3.28/eta_HV + P_aux5)/eta_5 + P_auxSYS. Example eta_HV=.75, eta_5=.90, auxiliaries zero => **4.859W SYS load**. Even assuming perfect IN→SYS transfer of full 2.50W, deficit **>=2.359W at SYS**. At a hypothetical 3.0V battery, ideal equivalent current >=0.786A; real BATFET/PCM/contact losses and VSYS droop increase stress. This is a *necessary energy bound*, not a qualified operating point.
In USB+BAT supplement, signed I_BAT > 0 (discharge); charging is already reduced to zero by DPPM in the documented onset sequence. USB+net-charge requires **P_IN sufficient for SYS load plus battery charge and losses**, so it is incompatible with this illustrative full-load 500mA condition.
Battery-only: P_BAT must cover SYS→5V→HV and auxiliaries plus battery-path losses; no guarantee without selected cell, actual SYS minimum, TPS61023 startup/current-limit, temperature and HV capacitor charging.

## Mode/fault matrix (research contract)
| Mode | Source/path | Charge sign | 16mA target | Qualification hold |
|---|---|---|---|---|
| USB only, no usable BAT | IN→SYS | zero | NO-GO at 500mA | enforce reduced demand/hard disable |
| USB + battery supplement | IN and BAT→SYS via BATFET | I_BAT positive/discharge | conditional in principle | VBSUP thresholds, OCP, path/thermal/low-cell transient |
| USB + net charge | IN→SYS and BAT | I_BAT negative/charge | NO-GO at 500mA full load | real current budget, charge temp and CE logic |
| BAT only | BAT→SYS | positive/discharge | unknown | BATFET/PCM/TPS61023 and battery-only thermal |
| USB unplug/PCM open/reset | transient source change | dynamic | unknown | brownout, independent HV hard-stop/discharge |

## Comparison of HV alternatives (not new adoption)
- MAX668 conventional non-coupled 5→205V boost remains rejected by D-003; **coupled** alternative remains open with switch, transformer, diode and temperature unqualified.
- LT3757 flyback manufacturer 350V/10mA example does not prove 205V/16mA; original TDK DCT15EFD-U44S003 sourcing flagged obsolete in earlier B report.
- LT8365 DC2838A charge-pump evaluation 9–30V→250V/10mA cannot establish 5V→205V/16mA; actual peak currents and thermal remain open #10.
- Direct-SYS flyback removes one conversion stage theoretically, but needs a qualified current-production controller + transformer and low-cell/startup/OVP evidence.
No newly confirmed distributor stock/JPY/lead time: **UNKNOWN**. No parts pair is approved.

## New precise decision boundary and Chat C questions
**New evidence versus prior 05:00 report:** Rev.B §6.3.3 explicitly confirms existence of USB-present battery supplement mode, with charge reduced to zero before supplement and supplement current unregulated. This resolves the narrow question 'does the IC support supplement in principle?', **not** 'can NIXIDORO sustain 16mA safely?'. Review TI wording, mode matrix, current sign and arithmetic; challenge whether 2.50W is properly an upper bound under selected input programming and whether any current limit guarantees need temperature/tolerance derating. Check CE-independent supplement and separate battery-only thermal cut path.
Proposed SOP addition for integrator (do not edit docs/ai-workflow.md directly): require each SYS-001 report to cite exact BQ section/revision and separate **feature existence / guaranteed current / thermal and startup proof**, plus USB-only, supplement, net-charge, BAT-only modes and signed battery current.

## Next bounded research
1. Extract Rev.B table min/typ/max of VBSUP1/2, BAT OCP, IN limit, VBUVLO and thermal derating at applicable temperature; compare with selected battery/PCM and actual TPS61023 input demand.
2. Source exact DC lamp current/duty/simultaneous matrix to determine 16mA continuous versus exceptional peak.
3. Identify >=2 currently procurable controller+magnetics pairs, with controlled drawings, current/temperature, single-unit JPY price/lead time and failure behavior.
4. Independent Chat C review then Work integration. No hardware authorization or shared-index edits.
