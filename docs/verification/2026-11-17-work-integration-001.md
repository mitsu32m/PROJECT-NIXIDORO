# Work integration 001 — HV/PWR/CTRL adoption gates

- Task: WORK-INT-001; parent SYS-001, HV-001/002/003/004, PWR-001/002, BAT-001.
- Date: 2026-11-17 JST. Role: Work / system integration; no separate agents launched.
- Repository / branch: mitsu32m/PROJECT-NIXIDORO / codex/reva-integrated-prototype-review.
- Examined baseline SHA: 0d83c2d0d551e0893aa1eced613a250ec6a12181.
- Result: **CONDITIONAL for continued comparative design research; BLOCKED for HV topology/component adoption. PENDING REVIEW. NOT ORDER-READY.**

## 1. Bounded contract

Question: What is the highest-value integration decision justified by the currently available reviewed evidence?
Exit criteria: identify evidence/review availability, independently check decisive power and voltage constraints, preserve candidate options, state adoption gates, BOM consequences and bounded next tasks.
Exclusions: re-investigating every report, selecting production values, modifying KiCad or requirements, physical testing, purchasing, fabrication, merging, creating a recurring schedule.

## 2. Repository evidence and review status

Read all six SOP startup documents, verification directory and recursive branch tree, Issues #1/#2 and their comments, and PR search (all states). Relevant source inspection: requirements.md; reva-integrated-net-spec.md; reva-integrated-prototype-review.md; pwr-reva-power-thermal-review.md; hv-voltage-window.md; hardware/integration/system-load-model.py; hardware/hv/RevA-draft/HV_RevA.kicad_sch and .net.

Latest research artifact: Chat A's 2026-11-17-1025-JST-HV-001-max668-quantitative-screen.md, explicitly PENDING REVIEW. The 09:30 precedent report is conditional research. No separately attributable new Chat B report or Chat C review/judgment package was found in the examined branch tree, issue comments or PR search. This is a bounded repository observation, not proof those chats have done no work elsewhere. **Do not present this integration as adoption of Chat C-reviewed work.**

Issue #2 already tracks HV-001A topology-specific review. Do not duplicate it or claim it. Issue #1 concerns workflow/claim implementation; its incompleteness does not stop useful technical research. No formal claim made here.

## 3. Most important integration decision

**D-012 / proposed:** establish a mode-specific HV–PWR–CTRL power contract before choosing a final HV stage. Continue the existing 205V/16mA target as an unverified design target. In parallel with Issue #2, prioritize HV-004 to substantiate the actual lamp demand. No reduction of maximum current, input-current increase or voltage relaxation is adopted.

Reason: reva-integrated-prototype-review.md derives 16mA from **assumed** 2mA per IN-12B plus 1mA per neon: 2×2+12×1=16mA. requirements.md leaves HV voltage/capacity undecided and describes the digits as used when needed and OLED normally off. An operational profile may lower average energy but cannot replace worst simultaneous load, startup or fault analysis. A 4/8mA scenario is not an approved product requirement or permission to operate hardware.

Required contract fields: mode; simultaneously illuminated loads; lamp current tolerances; nominal/maximum HV; minimum SYS/5V; continuous and startup demand; charging/supplement state; audio/OLED demand; battery temperature/current limits; fault behavior and automatic recovery conditions. Separate peak, continuous and average quantities.

## 4. Primary checks and reproducible calculations

Sources accessed 2026-11-17 JST:

| Source | Exact location / condition | Classification and use |
|---|---|---|
| [TI BQ25185 SLUSF65B Rev.B, Aug 2026](https://www.ti.com/lit/ds/symlink/bq25185.pdf) | §5.5 p6 input limit; §6.3.2–6.3.3 p15 DPPM/supplement | GUARANTEED table limit 450/475/498mA at VIN=5V for 500mA configuration; supplement behavior described |
| [ADI MAX668/MAX669 Rev3, Jun 2016](https://www.analog.com/media/en/technical-documentation/data-sheets/MAX668-MAX669.pdf) | pp2–4 electrical tables, ROSC=200kΩ±1%; p1 topology description | Guaranteed limits under stated temperature conditions; topology support is not 205V/16mA proof |
| [Microchip HV5524 DS20006850A, 2023](https://ww1.microchip.com/downloads/aemDocuments/documents/APID/ProductDocuments/DataSheets/HV5524-32-Channel-Serial-to-Parallel-Converter-Data-Sheet-DS20006850.pdf) | p3 recommended conditions; p8 power sequence | Recommended output maximum 220V; 230V is absolute maximum; no VDD-off safety isolation inferred |

Target inputs 205V, 16mA are **ASSUMED/TARGET**, not guaranteed device capability. Efficiencies ηHV=.70 and η5=.85, 5V logic=.50W, SYS other=.50W are **ASSUMED**, from the existing model; no new measurements.

Equations:
- PHV = 205 × IHV.
- P5 = PHV/.70 + .50.
- PSYS = P5/.85 + .50.
- PHV-stage loss = PHV × (1/.70−1).
- P5-stage loss = P5 × (1/.85−1).

| Scenario HV current | PHV | P5 | PSYS (no audio) | HV+5V conversion loss |
|---:|---:|---:|---:|---:|
| 4mA | .820W | 1.671W | 2.466W | .351+.295=.646W |
| 8mA | 1.640W | 2.843W | 3.845W | .703+.502=1.205W |
| 16mA | 3.280W | 5.186W | 6.601W | 1.406+.915=2.321W |

These independently recomputed values match the prior PWR scenario arithmetic. PSYS−PHV is **not** converter loss: it also includes logic/UI allocations. Conversely PHV is not all emitted light; lamps, series resistors and driver dissipate much of it. Enclosure heat needs spatial loss allocation, charger/BATFET/cell losses and measured optical/audio escape; do not use 2.321W as whole-enclosure heat. No temperature can be certified without actual component losses, board thermal paths, cell specifications and enclosure ambient.

Decisive USB-only check, independent of efficiency assumptions: at VIN=5V and the specified maximum 498mA input limit, electrical input is at most 2.490W under those table conditions, already below 3.280W HV output. Even 100% conversion and zero other demand cannot sustain 205V/16mA. At the 450mA lower limit a conservative input budget is 2.250W, before charger/path losses. Thus **USB-only full target is NO-GO under the existing 500mA configuration**. Higher-current external adapter alone cannot bypass this configured limit. This is not a new USB source-compatibility certification.

With battery assistance, USB presence does not establish net charging. BQ reduces charging in DPPM and may supplement from BAT after charging reaches zero. requirements.md's “operation while charging” therefore needs a defined mode and measured net battery current before claiming full-load simultaneous charging.

Voltage check: MAX668 FB=1.22–1.28V at −40..85°C; ratio=205/1.25−1=163; each divider resistor ±1%.
Vnormal,max=1.28×(1+163×1.01/.99)=214.13495V.
Only 5.86505V remains to the HV5524 recommended 220V; FB bias, resistor temperature/voltage coefficients, dynamic normal excursion and OVP latency/energy are excluded.
Adoption requires normal dynamic maximum < OVP trip minimum and OVP trip maximum + worst post-trip rise <220V, with independent shutdown, power-loss behavior and discharge. No OVP value selected.

Ordinary non-coupled boost D=1−5/205=.97561 exceeds MAX668 maximum duty; rejection stays topology-specific. Coupled boost and flyback remain research candidates.

**Review correction to Chat A's 10:25 report:** 225–275kHz at ROSC=200kΩ is the 0..85°C table. Full −40..85°C table pp3–4 gives **222–278kHz** (with −40°C limits guaranteed by design). It remains outside the cited transformer's 50–200kHz typical application band, but a typical application band alone is not proof of an absolute prohibited frequency. Require actual magnetic loss/thermal qualification. The report's mixed lossy input-power/ideal CCM-duty currents are sizing proxies, as it acknowledges; they cannot close winding, MOSFET, CS or thermal design gates.

## 5. Candidate comparison and adoption conditions

| Candidate | Current standing | Adoption evidence required |
|---|---|---|
| MAX668 conventional single-inductor boost | REJECTED for 5→205V | Fundamentally different topology required |
| MAX668 coupled-inductor boost | Comparative candidate; Issue #2 | Original winding polarity/connections; topology-specific stress model; primary magnetics specifications, losses, startup, OVP and thermal evidence |
| MAX668 ordinary flyback | Comparative candidate | Valid continuous operating-point/loss model, actual magnetics, loop/compensation, frequency corners, FET/diode/CS bounds |
| LT8304-1 flyback | Prior conditional candidate; not re-audited this run | Reopen prior current-limit/efficiency screen with qualified actual magnetics and measured/justified losses |
| Module/cascade or altered supply architecture | Alternatives; no new selection | Current documented fit, safety/power/cost evidence; any consequential specification change requires user approval |
| Lower-current display profile | Sensitivity proposal only | HV-004 current/brightness evidence and explicit approval if target is changed |

There is no supported winner yet. Do not populate procurement BOM by treating the 10:25 flyback proxy's 60V FET / ≥400V diode suggestions as selected ratings, or by transferring flyback stress equations to a coupled-boost circuit.

## 6. Interface, safety and BOM impact

Existing proposed SYS→TPS61023→5V HV/logic and SYS→Pico VSYS→3V3 OLED/RTC remain the comparison baseline. HV schematic and exported netlist confirm FB/CS/MOS gate interfaces and HV generation are unfinished; annotations explicitly say HV_EN_REQ is not connected to HV_RUN_TODO, and OVP/discharge are absent. No functional integrated prototype is implied. No schematic edits this run.

PWR must prove continuous/step/startup current with actual inductor and effective capacitance. CTRL must prove OE/BL behavior, GPIO reverse-feed and fault handling across powered/unpowered domains. Independent HV hard-stop and discharge must remain effective when CTRL or 5V logic disappears. BL=LOW/POL=HIGH is not an electrical safety isolator.

BOM impact: transformer, FET, rectifier, clamp/snubber, CS/FB, HV capacitor, independent OVP/latch/hard-stop, bleeder, HV-rated connectors/resistors remain **TBD / engineering hold**. Cell/NTC and L1 remain unqualified. Keep safety components in all cost comparisons. Record voltage/current/temperature ratings, footprint, source, tax/shipping and cost delta once selected. No new verified prices or total-cost claims; integrated-bom.csv unchanged.

## 7. Next task contracts and batching trigger

1. **HV-004A (proposed research task, no claim): display-current evidence.** Obtain original IN-12B and exact neon-lamp specifications or mark provenance UNKNOWN; tabulate ignition/maintaining voltage, recommended/min/max current, temperature/lifetime constraints and simultaneous display modes. Deliver current/resistor-power/voltage-tolerance table and a proposed supervised brightness test plan. Stop at unknown ratings; do not infer minimum current from appearance, generic NE-2 naming or operate HV. Review by Chat C before target adoption.
2. **HV-001A: existing Issue #2.** Continue actual coupled topology and stress identification; keep it separate from ordinary flyback sizing.
3. **C-REVIEW-001 (proposed):** review the 10:25 report and this integration together; return per-claim accepted/corrected/rejected/unknown, exact source pages, full-temperature frequency correction, coherent operating point vs proxy, missing magnetics and adoption scope. No review package has yet been received.
4. **SYS-001A (proposed):** after lamp-current evidence and credible HV-stage input bounds, produce the mode contract above with low-cell, USB-only, battery assistance, charging, audio/OLED and startup; cross-link PWR-001/002 and BAT-001. Design research may proceed while physical tests remain separately gated.

Run Work again when an important C-reviewed package provides a topology with qualified magnetics/stresses, an evidenced load/current proposal, a feasible OVP window or a changed system power/thermal result. Batch such items; no need to re-audit unchanged reports. Maximum twice/day is a future ceiling, not an enabled schedule. Usage quota/execution overlap were not available or verified; no automation was created or changed.

## 8. Decision and state changes

D-003 remains rejected only for conventional boost. D-004/D-005/D-006 remain proposed/target/undecided. Add D-012 as **PROPOSED, PENDING REVIEW**. SYS-001 stays OPEN, elevated from P1 to P0 because the integrated supply/demand mismatch blocks feasibility; no requirement is changed. Tech tree adds SYS-001 and PWR-002 coverage and cross-subsystem release dependencies. No safety node is marked verified or unlocked; HV-004 and alternative exploration continue.

## 9. Commit audit

Baseline SHA above. Updated: this report, verification/decisions.md, verification/open-issues.md, verification/handoff.md, tech-tree.yaml, tech-tree.md. All documentation committed together with expected-head check; final resulting SHA and readback are reported in the Work response. This document cannot contain its own final commit hash. No main merge, purchasing, fabrication, HV testing, or hardware safety certification.
