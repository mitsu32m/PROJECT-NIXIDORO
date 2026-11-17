# C-REVIEW-002 — Independent first-stage review of HV-002A/B OVP threshold and tail-energy screen

Date: 2026-11-17 22:58 JST | Role: Chat C independent reviewer | Task: HV-002B, Issue #5 (parent #3; follow-up #6) | **NO FORMAL CLAIM**
Branch: `codex/reva-integrated-prototype-review` | Starting HEAD: `c540d41df5eeb9a7b302dd73468118463f037810`
Review status: **ACCEPTED (arithmetic/algebra only); CONDITIONAL (hypothetical design screen); BLOCKED (actual OVP implementation, safety and part adoption).**

## Bounded contract
Question: Are Chat A's 15:57 HV-002A and 20:03 HV-002B numerical OVP window and capacitance/tail-energy conclusions internally correct and manufacturer-compatible? Exit: independently reproduce table and challenge whether controller shutdown can be treated as instantaneous. Excluded: actual circuit design, guaranteed response, PCB approval, hardware testing.

Read: SOP, handoff, open-issues, decisions, tech-tree YAML/Mermaid, latest 21:00 Chat B SYS report, 20:03 HV-002B, 17:02 Chat B lamp report, 15:57 HV-002A, prior C-REVIEW-001, Issues #1–#6. Four new reports since prior C HEAD b8e9f8b were identified by GitHub compare. Shared indices remain integrator-owned.

## Independent numerical reproduction (not measurements)
ASSUMED normal static upper Vn=214.13495 V; ASSUMED aggregate independent OVP error epsilon=0.01; MANUFACTURER recommended HV5524 maximum 220 V; ASSUMED Cmin=1.0 uF, L=44 uH and Ipk=3.2 A. No actual comparator, reference, capacitor, magnetics or switch has been selected.

- Avoid false trip: Vt > Vn/(1-epsilon)=**216.2979293 V**.
- No post-trip rise: Vt < 220/(1+epsilon)=**217.8217822 V**. The open nominal window width is ~1.52385 V, BEFORE dynamic normal overshoot.
- Hypothetical pulse energy E=0.5*44e-6*3.2^2 = **0.22528 mJ**. It is NOT a guaranteed maximum; typical magnetic saturation current is not a current clamp.
- For Vh=1.01*Vt, Ehead=0.5*Cmin*(220^2 - Vh^2). At Vt=216.3, 217.0, 217.8 V respectively: **0.3369588, 0.18225555, 0.004839758 mJ** for Cmin=1uF.
- Corresponding minimum Cmin for one assumed pulse: **0.668568, 1.236067, 46.54778 uF**; two pulses: **1.337137, 2.472133, 93.09556 uF**. The Chat A 20:03 table rounds correctly.
- At 216.3 V nominal, nuisance-trip margin over the *incomplete static bound* is only **0.0020707 V**; at 217.8 V nominal, high-trip headroom is only **0.022 V**. These are mathematically correct and physically inadequate as an adopted protection design.

**Verdict:** ACCEPTED for symbolic equations and rounded sensitivity examples, NOT for a guaranteed capacitance, trip setting, pulse count or safe voltage. The capacitance screen requires a genuine upper bound on net energy injected after trip, including the converter's delayed stop, stored energy, parasitics and open-load state. An unknown actual Cmin also makes any suggested capacitor size non-actionable.

## Manufacturer primary-source challenge — new finding
Directly inspected:
- Microchip **HV5524 DS20006850A (2023), p.3**, Recommended Operating Conditions: **HVOUT -0.3 to +220 V**. Its **+230 V** figure is Absolute Maximum Rating, NOT a normal operating allowance. Source: https://ww1.microchip.com/downloads/aemDocuments/documents/APID/ProductDocuments/DataSheets/HV5524-32-Channel-Serial-to-Parallel-Converter-Data-Sheet-DS20006850.pdf
- Analog Devices/Maxim **MAX668/MAX669 Rev 3 (6/2016), p.3** electrical characteristics: a row **“SYNC/SHDN Falling Edge to Shutdown Delay” = 70 us** appears in the 0..85°C table. **The 70 us row is a datasheet characteristic, not a demonstrated guaranteed worst-case independent hardware cutoff**; verify the exact min/typ/max column from original table before treating it as a bound. Source: https://www.analog.com/media/en/technical-documentation/data-sheets/MAX668-MAX669.pdf

**Important timing counterexample:** 70 us is approximately **19.46 oscillator periods at 278 kHz** (or 15.75 periods at 225 kHz), compared with HV-002A's illustrative 2–3 periods. This does NOT prove that 19–20 full-energy pulses reach the output after a shutdown command: duty, light-load behavior, stop sequence and circuit topology are unknown. It DOES invalidate any casual assumption that toggling MAX668 SYNC/SHDN gives an immediate, independently bounded cutoff. A separate, fault-tolerant hard-off path and actual energy/latency proof remain mandatory. Do not interpret the 70us as an upper bound without the datasheet table's column and temperature conditions.

The datasheet's current-limit threshold 85–115mV is a **sense-voltage** specification, not a guaranteed peak-current limit in amperes without RCS, comparator delay, switching ripple, fault behavior and tolerances.

## Verdict / required corrections
1. **ACCEPTED (limited):** algebra, energy formula and sensitivity table in HV-002B; prior HV-002A nominal ±1% comparator window algebra.
2. **CONDITIONAL:** use these as counterexample screens only. The assumption of one hypothetical 0.22528mJ pulse cannot be used as a worst-case tail-energy upper bound.
3. **CHANGES_REQUESTED (documentation):** add MAX668's 70us SYNC/SHDN characteristic and independently verify its table-column and full-temperature meaning; explicitly distinguish controller shutdown from independent hard-off. Extend response model to time-varying input energy during comparator propagation and controller/switch stop.
4. **BLOCKED:** actual independent OVP selection, 205V/16mA safety, HV operation, purchase and PCB release. Neither nominal trip band nor 1uF output capacitance is approved.

## Work judgment package (safety-critical)
**Decision question:** May Work select an OVP threshold in 216.3–217.8V and use 1uF or a pulse-count argument to claim HV5524 remains under 220V?
**Answer: NO.** The valid static algebra lacks guaranteed dynamic normal max, independent trip min/max, shutdown latency, real worst-case current/energy and Cmin. The manufacturer shutdown-delay row highlights a specific missing timing path.
**Alternatives:** true independent hardware energy-interruption path; reduce regulator tolerance and dynamic excursions; qualified alternative HV topology; change output operating target ONLY with owner authorization. Higher capacitance trades voltage rise for larger stored energy/discharge burden.
**Next:** Chat A/HV-002C obtain selected OVP comparator/reference, capacitor, hardware hard-off path, complete worst-case delay and tail-energy model including MAX668 shutdown semantics; Chat B/HV-004A qualify actual lamp load. Work retains HV-002/HV-003 locked; no promotion of D-006/D-007.
**Handoff:** GitHub Issue #5 and follow-up #6; this report is a review package for Work. No requirements, shared indices, KiCad, main, manufacturing or HV tests changed.
