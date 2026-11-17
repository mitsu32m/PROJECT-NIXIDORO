# Chat B SYS-001F — HV startup energy, USB/BAT supplement and mode transition screen

- Date: 2026-11-18 09:00 JST
- Role: Chat B wide research; provisional, **NO FORMAL CLAIM**
- Parent: SYS-001; related HV-004, PWR-001/002, BAT-001, HV-001 and Issue #4
- Starting branch HEAD: `9628970a5ad490d3fa733e15e6c9b5f764b79bd5`
- Review: **PENDING REVIEW** for Chat C
- Scoped result: **CONDITIONAL** for calculation method and proposed test contract; **BLOCKED** for actual HV startup/USB+BAT feasibility and any HV hardware authorization.
- Novelty vs Chat B SYS-001A–E: distinguish **HV output capacitor charging energy and startup time** from continuous 16mA load and from average display-duty reduction. Does not redo MAX668 coupled inductor or OVP post-trip design owned by Issues #2/#3/#5/#6.

## 1. Startup, concurrency and scope

Read required SOP/handoff/open-issues/decisions/tech-tree YAML and Mermaid, recent SYS-001D/E reports, and open Issues #1–#6. No verified atomic Claim or `role:wide-research` issue acquisition; continue owner-authorized provisional research. Shared indexes remain integrator-owned. No KiCad edits, purchasing, fabrication, HV energization, requirements changes or main merge.

Primary sources to verify by independent review:
- TI BQ25185 Rev.B (Aug 2026), [datasheet](https://www.ti.com/lit/ds/symlink/bq25185.pdf), electrical input-limit table and DPPM / battery supplement sections: 500mA configured input limit **450/475/498mA min/typ/max** at specified 5V condition; charge current is reduced to prioritize SYS and BAT can supplement. These are not guaranteed total output power or battery charging current.
- TI TPS61023 Rev.B [datasheet](https://www.ti.com/lit/ds/symlink/tps61023.pdf): startup and current-limit behavior is load-, VIN-, L- and effective-capacitance-dependent; example startup time is not a full HV load startup guarantee.
- Microchip HV5524 DS20006850A [datasheet](https://ww1.microchip.com/downloads/aemDocuments/documents/APID/ProductDocuments/DataSheets/HV5524-32-Channel-Serial-to-Parallel-Converter-Data-Sheet-DS20006850.pdf): recommended 220V HV maximum, independent OVP still mandatory. HV cap energy and post-trip rise are already under Issue #6; do not infer OVP feasibility from this report.

## 2. A missing load term: startup charge energy

Let the *effective* HV output capacitance be `C_HV` and `V_HV=205V`. Ideal stored energy `E_C=0.5*C_HV*V_HV²`. This energy must be supplied **in addition** to lamp load and conversion losses when the rail starts at 0V. Capacitor values below are **ASSUMED sensitivity cases**, not selected BOM or measured capacitance.

| Effective HV capacitance | Stored energy at 205V | Average capacitor-charging output power for 0.5s ramp | For 2s ramp |
|---:|---:|---:|---:|
| 0.10µF | 2.10mJ | 4.20mW | 1.05mW |
| 1.00µF | 21.01mJ | 42.0mW | 10.5mW |
| 4.70µF | 98.76mJ | 197.5mW | 49.4mW |
| 10.0µF | 210.1mJ | 420.3mW | 105.1mW |

These are **average energy/time** values, not peak switch/transformer current. Constant voltage slew gives `I_C=C*dV/dt` and instantaneous capacitor power `P_C=V*C*dV/dt`; at the end of a linear 0.5s ramp with 4.7µF, `I_C≈1.927mA` and `P_C≈0.395W`, **twice** the average. The transformer must additionally supply lamps, controller/bleeder and losses. Real capacitance depends on tolerance, voltage and temperature; verify actual part ratings.

For a **deliberately pessimistic** simultaneous full lamp load of 205V×16mA=3.28W during startup, plus 4.7µF charged in 0.5s, ideal *average* HV power is `3.28+0.1975≈3.478W`. At assumed `eta_HV=.70`, `eta_5=.85`, 5V logic 0.50W and SYS-other 0.50W, `P_SYS≈((3.478/.70+.50)/.85)+.50≈6.93W`. At 3.0V SYS that is 2.31A **average**, excluding cell/protection path drop and peak ripple. The existing 6.60W continuous model therefore does not bound all startup transients. Conversely, lamps may be blanked during charging and HV controller may current-limit; then this worst simultaneous scenario may not occur, but **a measured interlock and actual current waveform are required**.

## 3. USB-only vs USB+BAT during HV startup

At 5V, programmed BQ input-limit **450mA min** yields 2.25W electrical input, **498mA max** 2.49W; these are ideal upper powers at the input, not SYS deliverable. For 6.93W *hypothetical* startup demand, even a lossless 2.49W USB→SYS path leaves ≥4.44W from battery or energy storage. With `V_BAT=3.6V`, this represents ≥1.23A ideal equivalent cell current before BATFET, cell, connector and protector losses. A small 5V decoupling capacitor cannot bridge an extended multiwatt deficit: e.g. 100µF discharged 5.0→4.5V stores `0.5*100µF*(25-20.25)=0.2375mJ`, only about **0.053ms** at 4.44W (idealized). This is an energy upper bound, not a rail-droop simulation.

BQ25185 DPPM can first reduce charge current, then supplement SYS from BAT, but the charger datasheet does **not** guarantee that an unspecified protected 21700, connector and sealed enclosure can safely sustain the calculated current. At full display load, USB present may mean net **battery discharge**. Never infer positive charging from USB presence, /CE state or a charging icon.

## 4. Critical mode transitions to qualify

| Transition | Failure mechanism to investigate | Evidence required |
|---|---|---|
| USB-only low-load → HV startup | Input current limit, SYS sag, TPS61023 undervoltage, retry/oscillation | I_USB, V_SYS, 5V, HV voltage and input current waveforms; no unsafe auto-retry |
| USB+BAT → HV startup | DPPM charge taper, BAT supplement, BQ BATFET heating | Signed I_BAT, V_SYS and charger status; verify *net* charging vs discharge |
| Battery-only low-SOC → HV startup | Cell/protector voltage sag and 5V converter current limit | Actual protected-cell worst impedance, TPS61023 L1 saturation and UVLO |
| HV active → USB unplug | Source handoff and brownout may disable MCU before HV hardware | Independent HV hard-off, default-off and discharge; reviewed by HV-003 team |
| HV active → USB replug | Input protection/eFuse transients and charge-state changes | No spurious HV restart or excessive inrush |
| Lamp mode change 1→12 neon + 2 digits | Abrupt output power increase; output capacitor transient | Voltage overshoot/undershoot, controller current limit and recovery |
| MCU reset / display blank | Blanking is not HV isolation; cap remains charged | Independent OVP and controlled discharge, no automatic HV restart |

## 5. Architectural comparison, without premature adoption

- **Existing SYS→TPS61023→5V→HV:** startup needs coordinated enabling of 5V, HV and lamp load; actual 5V effective capacitance and L1 Isat/thermal remain unresolved.
- **Direct SYS→HV flyback:** removes one HV energy-conversion stage but **does not eliminate HV capacitor charge energy**, source handoff or BQ battery supplementation; MCU/HV5524 logic still needs appropriate rails. The previous LT3757A/LM5155 screens do not qualify a real transformer.
- **USB-only limited display:** may be feasible only if the *instantaneous* current and startup inrush stay within actual input/path constraints; average-duty savings do not excuse peak/startup limits.
- **Higher-current USB redesign:** could remove the fundamental 500mA budget issue, but requires USB-C source negotiation/advertisement, charger/eFuse/cable and heat redesign; owner approval required.
- **Staggered start / precharge / lamp blanking:** potentially reduces coincident loads, but must be implemented with **hardware fail-safe HV gating** and independently validated fault handling. It is not a substitute for OVP.

## 6. Loss and thermal scope

At 16mA and assumed 70% HV conversion, converter loss is 1.406W; assumed 85% 5V conversion adds ~0.915W under continuous full-load scenario. Startup capacitor energy is ultimately dissipated during discharge; at 4.7µF and 205V it is 98.8mJ per complete charge/discharge cycle (ignoring energy recovery). Frequent unintended restart loops can add average thermal load `P_restart=f_restart*E_C/eta_total`; at 1Hz, 4.7µF and assumed .595 combined efficiency this is ~0.166W input attributable to charging the HV cap, **before lamps and other switching losses**. Neither junction nor cell temperature is inferred; actual PCB and PETG thermal paths remain unknown.

## 7. Review questions and bounded next steps

1. **Chat C:** check capacitor energy arithmetic, instantaneous vs average startup load, and the **optimistic** USB+BAT deficit lower bound; confirm no assumption was mislabeled GUARANTEED. Review interaction with Issue #6 without merging OVP tasks.
2. **Chat A / PWR-001:** establish actual HV output C, effective 5V output C, selected L1 and SYS minimum; compute 5V startup with source current-limit and rail-droop transient; use manufacturer waveform conditions.
3. **Chat A / PWR-002:** analyze BQ DPPM→BAT supplementation at USB attach/detach and cell SOC extremes, including thermal; validate with *signed* cell current and charger states.
4. **Chat B / HV-004:** obtain selected exact lamp parts and mode matrix; establish whether lamp outputs can be held off until HV stable without violating display safety or behavior.
5. **Work / integrator:** after independent review, decide whether a mode-specific HV startup contract is required in shared specs. Do not change 205V/16mA target or imply any release.

## 8. Workflow proposal and non-actions

Nonblocking Claim fallback proposal already saved at `docs/verification/2026-11-17-1403-JST-chatb-provisional-workflow-sop-proposal.md`; do not duplicate or edit canonical SOP without integrator coordination. Record this new SYS-001F issue facet through Issue #4 comment. **PENDING REVIEW**. No formal Claim, no changes to shared indexes, KiCad, BOM or hardware safety state.
