# C-REVIEW-010 — THERM-001 /CE power-domain and SYS-001 USB/BAT power contract
Date: 2026-11-20 09:02 JST. Reviewer: Chat C, independent first review.
Branch: `codex/reva-integrated-prototype-review`. Starting verified branch HEAD: `d6d73369d28c2927c33101a1a96ee73c1e412b8e` (GitHub fetch_commit of branch ref).
Claim: NONE; provisional review. No hardware approval, component adoption, schematic edits or requirements changes.

## Scope and sources
Reviewed three new PENDING REVIEW reports added after C-REVIEW-009 (commit 1f4b2dbd4357a1a54a960ec6d65271a7307cd383):
- [A 04:03 /CE electrical thresholds](2026-11-20-0403-JST-THERM-001-ce-primary-threshold-and-vbus-clamp.md)
- [B 05:03 SYS/USB/BAT and holder correction](2026-11-20-0503-JST-chatb-sys001-usb-battery-power-contract-and-holder-correction.md)
- [A 08:02 independent power domain](2026-11-20-0802-JST-THERM-001-ce-power-domain-independence.md)

Read required SOP, handoff, open issues, decisions, YAML and Mermaid tech tree; relevant baseline `docs/reva-integrated-net-spec.md`. Compared previous review SHA to branch and found these three changed reports. Manufacturer primary evidence independently fetched: TI BQ25185 datasheet Rev.B, SLUSF65B, revised August 2026, https://www.ti.com/lit/ds/symlink/bq25185.pdf, pp.4–8 (pin, abs max, electrical thresholds, current limit), §6.4 (battery-only TS). No actual hardware measurement or KiCad netlist extraction in this run. Exact latest source branch SHA as above; all numeric efficiency and holder impedance examples are ASSUMED.

## Independent verdict by claim
1. **ACCEPTED (datasheet-only):** /CE pin 4 HIGH inhibits charging and LOW enables it (p4); all pins except IN have -0.3..5.5V ABSOLUTE MAX (p5), not a functional operating range. /CE VIL 0.4V, VIH 1.3V are table specifications at VPULLUP=1.8V, VIN=5V/VBAT=3.6V and stated temperature conditions (p8). These values do not establish behavior during an unpowered ramp. CE leakage and startup guarantee remain UNKNOWN. The A report's 5.7V CE example would exceed 5.5V ABS MAX by 0.2V **if** 5.7V reaches CE; TPS259533 5.7V clamp bound itself was not independently verified, so no assertion that actual CE reaches 5.7V.
2. **ACCEPTED (topology counterexample only):** MCU/Pico-3V3-derived-only pullup cannot guarantee /CE HIGH when USB powers BQ but Pico 3V3=0. At VPU=0, a passive pullup cannot establish 1.3V HIGH. This disproves an *independent fail-inhibit claim*, not proof that battery charging necessarily begins (TS and other charger states matter). Existing baseline /CE=GND is a proposed draft and permits charging under CE logic; no independent thermal interlock implemented.
3. **CONDITIONAL:** A's 10k pullup 1.8V static current budget: (1.8-1.3)/10k=50uA; with ASSUMED extra 0.2V margin: (1.8-1.3-0.2)/10k=30uA. Arithmetic correct; no actual resistor choice or CE leakage guarantee. Input VIN_LOWV charging-start 3.0..3.15V (p6) does not bound CE ramp or guarantee onset at that exact voltage.
4. **ACCEPTED (ideal impossibility):** B's 205V*16mA=3.280W exceeds 5V*500mA=2.500W before any losses; with TI programmed 500mA ILIM table at VIN=5V, measured/guaranteed table range is 450/475/498mA min/typ/max (p6), so 2.500W is an optimistic nominal programmed-limit screen, not a guaranteed deliverable input budget. At 498mA max, the corresponding ceiling is 2.490W. Neither USB-only 16mA continuous nor simultaneous net charging at full HV is feasible under the stated 500mA input contract.
5. **ACCEPTED (arithmetic-only):** 3.28/(.8*.9)=4.5556W=0.9111A at 5V; 3.28/(.7*.85)=5.5126W=1.1025A. 2.5*.8*.9/205=8.7805mA; 2.5*.7*.85/205=7.2561mA. Battery supplement input-side equivalent at 80%*90% is 4.5556-2.5=2.0556W and /3V=0.6852A *if* the sources combine at the modeled input node and the battery path is ideal. **CONDITIONAL** for actual BQ power-path implementation: actual BAT-to-SYS current, conversion topology, USB limit, supplement threshold and thermal dissipation must be modeled; do not assign this input-equivalent current directly to battery without mapping losses and nodes.
6. **ACCEPTED (algebra-only):** B's correction `V_pack_out=V_cell_tab-I*(R_PCM+R_holder+R_wire)`, `V_SYS=V_pack_out-V_powerpath_drop` prevents double subtraction when the starting voltage is already measured at pack output. A lower-bound inequality is valid only with simultaneously guaranteed limits, consistent voltage reference nodes, and cutoff/temperature behavior; actual V_SYS,min is UNKNOWN. 2.2A^2*0.1ohm=0.484W is sensitivity only.
7. **BLOCKED (hardware):** Independent charge inhibit under USB ramp, /CE short-GND, MCU loss, NTC detachment, independent battery-only temperature cutoff, cell/PCM compatibility, HV shutdown/discharge, 5V startup, real lamp current, actual magnetics and safe temperature have not been demonstrated.

## Cross-system and fault implications
- TI §6.4 battery-only TS measurement is inactive: /CE is not a battery discharge/HV isolation control. Distinguish charging stop from SYS load cutoff and stored-HV discharge.
- Even a correctly biased /CE HIGH cannot protect against /CE hard short to GND; any single-fault protection claim requires independent enforceable energy path, fault coverage and system power-path analysis.
- Source-power inequality is an ideal impossibility for full USB-only 16mA, **not** authority to change the 16mA target, USB current contract or user display behavior.
- C-REVIEW-009 correction is addressed at algebra level by B. Keep exact cell/PCM/holder/contact limits, thermal and low-cell minimum open.

## Work decision package — significant, deliver
**Decision:** Is the current BQ25185 + protected 21700 + 500mA USB architecture retained with additional independent thermal charge inhibit and discharge protection, or should charger/pack/input architecture be redesigned?
**A claims:** direct-VBUS CE pullup may violate CE abs max under 5.7V exposure; Pico-powered pullup cannot fail-inhibit when MCU rail absent. **B claims:** USB-only 16mA is energy-impossible; battery supplement needed at full target; pack voltage reference correction.
**Independently checked:** TI Rev.B CE pin behavior, abs-max, thresholds and 500mA programmed ILIM range; ideal power and contact algebra above.
**Not verified:** CE leakage/ramp, 5.7V eFuse bound, actual cell charge limits, real power-path current, thermal/OVP, any proposed independent monitor, component cost.
**Alternatives:** independent adapter-powered supervised charge-inhibit plus separately enforced battery load cutoff; qualified thermally protected cell/pack; charger architecture with validated temperature window; explicit owner-approved lower simultaneous display mode or revised USB contract.
**System effect:** extra PWR power domain/parts/connector/sensing and startup/fault behavior; battery discharge and 5V thermal budget; HV current and capacitor/OVP coupling; 2027-Jan procurement schedule.
**Recommendation:** maintain THERM-001 and SYS-001 BLOCKED for hardware; ask A for actual schematic-independent power-state/short-fault matrix and B for real cell/PCM/controller/holder primary evidence, then Work chooses architecture after C-reviewed proof. No parts or PCB approval.
**Evidence:** three source reports linked above, TI Rev.B link, baseline branch HEAD `d6d73369d28c2927c33101a1a96ee73c1e412b8e`. Handoff to Work via this report and Issues #9, #4, #7.

## Queue and next steps
Changed-since-C009 PENDING REVIEW reports: 3; reviewed in this batch: 3. Remaining important unreviewed count is **UNKNOWN** without exhaustive branch-tree and review-coverage matching. Oldest remaining item **UNKNOWN**; prior handoff identifies older tapped-inductor/magnetics reports still requiring coverage verification. Next: prioritize #2 real magnetics and #6 OVP tail-energy, while continuing #9 actual circuit state/fault table. This review did not resolve any hardware safety gate.
