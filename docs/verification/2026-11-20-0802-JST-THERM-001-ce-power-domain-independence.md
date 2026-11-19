# THERM-001 / Issue #9 — /CE inhibit supply-domain independence and startup counterexample
Date: 2026-11-20 08:02 JST. Role: Chat A deep-design.
Branch: codex/reva-integrated-prototype-review.
Starting branch HEAD: UNKNOWN (fetch_file exposes blob SHAs; repository-wide commit search does not establish this branch HEAD).
Claim: NONE; provisional selection from open-issues.md. Status: PENDING REVIEW.
Verdict: **NO-GO (limited)** for MCU/Pico-only powered charge-inhibit pullup as a guaranteed fail-safe. **BLOCKED** for any implemented charge thermal interlock.

## Task contract
Question: Can the proposed 1.8V /CE HIGH pullup be derived from the current Pico power domain and still guarantee charge inhibit when Pico is OFF or unpowered? Exit: inspect baseline power domains and present an explicit counterexample and power-domain contract. No actual circuit or part adoption; no KiCad edits.

## Sources and branch context
- docs/ai-workflow.md; docs/verification/handoff.md; docs/verification/open-issues.md; docs/verification/decisions.md; docs/tech-tree.yaml and docs/tech-tree.md; docs/reva-integrated-net-spec.md (all fetched from working branch this run).
- Prior A report 2026-11-20-0403-JST-THERM-001-ce-primary-threshold-and-vbus-clamp.md (fetched); earlier 2026-11-20-0004 ramp concern referenced there. Issue #9 and #8 fetched through issue search. GitHub directory listing and exhaustive latest-report discovery not supported by the attempted fetch; branch HEAD not verified.
- TI BQ25185 Rev.B: https://www.ti.com/lit/ds/symlink/bq25185.pdf ; logic VIL=0.4V, VIH=1.3V specified at 1.8V pullup as documented in preceding report. These are **GUARANTEED only under stated table conditions**, not unpowered/ramp behavior.
- Baseline net spec: BQ SYS -> Schottky OR -> Pico VSYS -> Pico 3V3 OUT; Pico 3V3 powers OLED and RTC. The proposed Rev.A has no separate always-on 1.8V rail. /CE is presently tied GND.

## New topology-specific counterexample
**ASSUMED failure scenario:** USB VBUS is present and BQ25185 is powered; Pico 2 is not running, absent, held in reset, or its VSYS/3V3 supply is interrupted. If a /CE pullup is supplied *only* by Pico 3V3 or by a derived 1.8V rail that depends on Pico 3V3, the pullup source can be 0V while BQ input power remains present. Thus no guaranteed VCE >= VIH exists. /CE is not proven HIGH; its unpowered behavior and any internal bias are UNKNOWN. With current /CE=GND, charging is positively permitted by logic unless internal TS or other charger controls intervene.

This is a structural dependency failure independent of the choice of 10k vs 100k pullup: if VPU=0, then VCE<=VPU for a passive pullup without a separate source. The prior report's 1.8V static margin cannot be applied to this state. Therefore **NO-GO** for claiming *MCU-derived-only* pullup as an independent fail-inhibit mechanism. This does NOT prove charging actually begins in this scenario, because TS and charger state also apply.

## Power-domain contract for any future candidate
1. Charge-inhibit permission must be enforceable when MCU power is absent and USB is present; a USB-derived independent supply is a candidate, but it must never drive /CE above its abs-max 5.5V or inject current into an unpowered BQ pin.
2. Supply ramp/UVLO must not create a window of uncontrolled charge before inhibit is valid. A supervisor without a guaranteed startup output is not sufficient merely by its name.
3. Any charge-permit sink must be inactive until cell-temperature validity, attachment/fault detection and selected cell's charge window are verified. Define polarity and power-off behavior explicitly.
4. /CE short-to-GND or monitor stuck-permit remains a single-fault hole. If single-fault charge interruption is required, investigate an independently controlled energy cut path and its BAT/SYS power-path interactions; do not casually open the battery path under load.
5. The battery-only load-temperature interlock is separate: BQ TS measurement is inactive in battery-only mode (TI §6.4 p19); stopping /CE does not remove HV energy. HV hard-off and residual discharge need separate guarantees.
6. A proposed added independent monitor changes PWR local BOM, quiescent current, layout, possibly NTC harness and PWR/CTRL interface. Do not assume a spare GPIO can serve as a safety-rated interlock.

## State counterexamples / evidence status
| State | MCU-derived /CE pullup | Independent USB-domain inhibit | Required next evidence |
|---|---|---|---|
| USB present, Pico healthy | Could work (not proven) | Candidate | /CE VIH/VIL, leakage, startup timing |
| USB present, Pico 3V3=0 | **No HIGH guarantee** | Candidate | startup/UVLO, CE pin powered-off behavior |
| USB ramp, monitor not valid | No guarantee | No guarantee without proven sequencing | guaranteed inhibit-before-charge or separate interruption |
| /CE short to GND | No inhibit | No inhibit | independent cut path / fault coverage |
| Battery-only, USB absent | /CE irrelevant to discharge cutoff | /CE irrelevant | separate load thermal shutdown, HV discharge |

## New bounded action for Chat C / Work
Request a **power-domain state table** for any actual monitor/charger alternative: USB=0/ramping/valid, BAT=absent/low/valid, MCU=off/reset/on, NTC=open/short/detached, /CE short, monitor rail absent. For each, prove VCE min/max, charge current permitted/blocked, SYS/HV state, and residual energy. Candidate selection requires manufacturer electrical and timing data, actual cell and PCM, standby budget, cost and schematic-change approval.

Do not repeat resistor-only calculations until a valid always-on domain and its startup behavior are specified. Escalate thermal and HV release locks unchanged. No procurement, manufacture, HV energization, main merge, or requirements change.
