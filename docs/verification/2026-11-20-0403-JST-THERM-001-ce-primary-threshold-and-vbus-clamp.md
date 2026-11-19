# THERM-001 / Issue #9 — BQ25185 /CE primary electrical limits and unsafe VBUS pullup
Date: 2026-11-20 04:03 JST. Chat A deep-design. Branch: codex/reva-integrated-prototype-review.
Starting HEAD: UNKNOWN: GitHub connector exposes file blob SHA and repository-wide commit search returned default-branch history, not a verified working-branch HEAD. Formal Claim: NONE (provisional from open-issues). Status: PENDING REVIEW.
Verdict: CONDITIONAL for datasheet-grounded static constraints; BLOCKED for complete charge thermal safety and startup.

## Task contract
Question: Which actual /CE logic thresholds and absolute ratings constrain the proposed adapter-derived default-inhibit pullup, and can a VBUS-direct pullup be accepted? Exit: manufacturer electrical table values, worst-case inequalities, and a falsifiable counterexample. No schematic edits or component adoption.

## Sources and existing evidence
- TI BQ25185 Rev.B (revised Aug 2026), https://www.ti.com/lit/ds/symlink/bq25185.pdf, Table 4-1 p4, §5.1 p5, §5.5 LOGIC PINS p8, §5.5 input thresholds p6, §5.6 p8.
- Repository docs/ai-workflow.md, docs/verification/handoff.md, docs/verification/open-issues.md, docs/verification/decisions.md, docs/tech-tree.yaml, docs/tech-tree.md; 2026-11-20-0004 THERM-001 previous report; GitHub Issue #9 and #2. Work INT-003 identifies Rev.A /CE=GND. These were read on target branch; exhaustive latest-report tree enumeration and branch HEAD resolution unavailable.
- Prior A report establishes abstract timing race; this report replaces UNKNOWN threshold and pin-voltage values with primary specifications, not a repetition of the timing argument.

## Primary manufacturer limits and classification
GUARANTEED table-bound electrical characteristics under datasheet test conditions (VIN=5V, VBAT=3.6V, -40<TJ<125C unless noted): CE VIL = 0.4V, VIH = 1.3V; table explicitly gives VPULLUP=1.8V for these CE thresholds (§5.5 p8). These numbers must not be claimed guaranteed for arbitrary pullup voltages, unpowered input, or ramp.
GUARANTEED stress rating, NOT operational permission: voltage on all pins other than IN is -0.3..5.5V (§5.1 p5). CE is among these pins. VIN itself is allowed a higher voltage, but that does not transfer to CE.
GUARANTEED functional description: CE HIGH inhibits charge, LOW permits charge (Table 4-1 p4). No explicit CE input leakage maximum or internal pull-up/down guarantee was located in the cited LOGIC PINS table; label UNKNOWN, do not misapply STAT1/STAT2 ILKG=1uA to CE.
GUARANTEED specified VIN rising charging-start threshold VIN_LOWV 3..3.15V (§5.5 p6), subject to other charger conditions. This does not supply a guaranteed latest time for CE to become safe, or establish charging will start at that voltage in every state.

## New hard electrical counterexample
Previous candidate A proposed an adapter-derived pullup. A direct CE-to-VBUS pullup with VBUS allowed to reach 5.7V (existing TPS259533 clamp worst-case candidate in project) could expose CE to 5.7V, exceeding the BQ25185 5.5V absolute maximum by 0.2V. Even a nominal 5V VBUS cannot be considered safe without the complete surge/clamp/tolerance envelope. **Therefore VBUS-direct pullup is NO-GO if 5.7V is possible at CE**; the 5.7V is an existing project hypothesis, not a measured transient or guaranteed eFuse value. Confirm actual eFuse maximum clamp and transients separately.
At nominal 1.8V CE pullup (the datasheet logic-test condition), the static HIGH margin to VIH=1.3V is 0.5V. For a passive pullup R and total downward leakage I (including CE input, unpowered monitoring devices, PCB leakage), VCE>=1.8V-I*R. A 10k resistor would require I<=50uA to just reach 1.3V, or <=30uA for an ASSUMED 0.2V margin. This is a conditional arithmetic example, NOT a resistor recommendation, because the CE input leakage and available always-on 1.8V domain are UNKNOWN. At LOW, sink must guarantee VCE<=0.4V under all operating corners. Avoid using Pico 3V3 as a supposed always-on source when MCU power may be absent.

## Consequences for startup and fault handling
1. The charger may begin charging at VIN near 3..3.15V while any adapter-derived pullup remains below its guaranteed HIGH threshold, depending on power sequencing. A passive ramp therefore still cannot prove fail-inhibit; need specified powered-off CE behavior, charge-enable timing, or independent interruption.
2. Any added 1.8V regulator/supervisor must have guaranteed power-up and brownout output behavior, account for current, reverse feed, pin/connector space and BOM. No such component selected.
3. CE short-to-ground remains a single-fault unsafe counterexample even with a perfect pullup. CE does not isolate SYS/HV energy; independent battery-only thermal cut and HV discharge remain open.
4. Distinguish charger internal TS temperature enforcement from external charger inhibit. TS is not measured battery-only (TI §6.4 p19). Candidate cell 10..45C limit cannot be assumed satisfied by the direct nominal NTC entry points.

## Review / acceptance gates
- Determine CE input leakage across supply/temperature or qualify by conservative bench plus manufacturer support; verify actual CE pullup domain 0V-to-valid and input clamp/injection.
- Confirm TPS259533 clamp guaranteed maximum and surge path, not nominal; check every CE voltage against 5.5V abs max with margin.
- Compare actual supervisor/monitor candidates with guaranteed UVLO and output-off behavior; check CE timing against earliest charging state or independently block charge.
- Evaluate CE short, monitor stuck-permit, NTC detachment, cell PCM temperature cutoffs, battery-only load disconnect, and HV stored-energy discharge.
- Provide schematic-change request to Work/human; no adoption before independent Chat C review.

CONDITIONAL: CE threshold and static pullup margin constraints from primary data; a 5.7V direct CE exposure violates 5.5V stress rating. NO-GO limited to *unclamped* CE direct VBUS when VBUS can reach 5.7V; not a blanket rejection of adapter-derived safe logic.
BLOCKED: physical fail-safe charge inhibit, full temperature enforcement, sourceable part selection, power sequencing, PCB release. PENDING REVIEW.
No purchase, fabrication, HV application, main merge, or important requirement change.
