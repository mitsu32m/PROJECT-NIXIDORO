# Chat B — HV-004A lamp provenance and SYS-001 demand-envelope correction

Date: 2026-11-17 17:02 JST | Role: Chat B wide research | Technical task HV-004A / SYS-001; related GitHub Issue #4
Branch: `codex/reva-integrated-prototype-review`
Starting branch HEAD: `143b12833a8d304feb632720538a47ee00cb8c19`
Status: **PENDING REVIEW — CONDITIONAL research; NOT ORDER-READY; NO FORMAL CLAIM**.
Claim infrastructure is not demonstrated concurrency-safe; work is provisional and nonexclusive. No hardware operation, component procurement, manufacturing, main merge, design-target change or shared-index edits.

## Question / novelty / exit

Determine whether 16mA is an evidence-based *necessary* simultaneous display current, and what 12-stage gauge modes imply for SYS-001. Novel vs Chat B 14:03 report: locate primary neon manufacturer example and archival IN-12B technical material, contrast them with actual product usage requirements, and derive a transparent current sensitivity envelope. Do not repeat Chat A MAX668/OVP topology studies or assume an NE-2 designation identifies a unique device.

Startup read: `docs/ai-workflow.md`, `docs/verification/handoff.md`, `docs/verification/open-issues.md`, `docs/verification/decisions.md`, `docs/tech-tree.yaml`, `docs/tech-tree.md`; latest 15:57 HV-002A OVP report; 14:03 Chat B SYS-001 report; 10:25 Chat A HV-001 report; `docs/requirements.md`; open GitHub Issues #1–#5. Existing Issue #4 is SYS-001A review; no separate GitHub task is formally claimed. Source access 2026-11-17 JST.

## Primary/secondary source provenance

- **IN-12B archival technical document:** [IN-12B_data.pdf](https://nixie-tube.com/nixie/data/in-12/IN-12B_data.pdf), original-style Russian pinout with anode pin 1, cathodes 0–9 and decimal point on IN-12B pin 12. This is archival material (manufacturer document provenance not independently authenticated). The linked indexed English technical table reports **typical** anode voltage about 145V and **typical** cathode current 2.5–3.5mA; the English table may be an added secondary compilation rather than a guaranteed original Soviet specification. **Source class: TYPICAL, secondary/archival; not GUARANTEED.** Cross-check independent [IN-12B tube reference](https://www.tube-tester.com/sites/nixie/data/in-12b.htm), also 2.5–3.5mA typical. Neither validates a 2mA requirement or a minimum visible brightness. Tube source and ageing are UNKNOWN.
- **Neon primary manufacturer example:** [San Guang Electronics NE-2 6x16x50 PDF](https://www.taydaelectronics.com/datasheets/files/1039.PDF), specifies **110VAC with 68kΩ series resistor, approximate 0.7mA current**, breakdown ≤65VAC, lifetime ≥25,000h under the listed application. **Source class: manufacturer example, approx current/TYPICAL**, not a 205V DC current recommendation and not necessarily the purchased lamp. The data do not give DC maintaining voltage, DC lifetime or DC 205V series-resistor specification. The selected exact neon part is **UNKNOWN**.
- **Another marketed NE-2 variant:** [Jameco ValuePro NE-2](https://www.jameco.com/z/NE-2-Jameco-ValuePro-Neon-Lamp-NE-2-1A1-65-120VAC-0-3mA-Wire-Leads_27351.html), listing says 0.3mA in the specifications and 0.5mA in overview; even the product listing is inconsistent, illustrating why generic NE-2 ratings cannot be transferred across variants. **Vendor listing; not guaranteed application data**.
- **Requirements**: `docs/requirements.md` says 12 neon bulbs are a **12-step remaining-time gauge**, two digits are displayed **only when exact minutes are needed**, and OLED is **normally off during focus**. Thus 2 digits + all 12 neon + OLED/audio simultaneously is a useful electrical stress test but **not an established normal-use duty cycle**. The 12-step semantics do **not** prove a one-hot gauge or a bar graph; that choice must be explicit.
- **Current project assumption**: 2 digits × 2mA plus 12 neon × 1mA = 16mA, from `docs/verification/2026-11-17-work-integration-001.md`. This remains **ASSUMED** and is not revised by this report.

## 1. Reproducible load envelope

For `n_D` active IN-12B digits (0–2), `n_N` lit neon bulbs (0–12), actual digit current `i_D`, and actual neon current `i_N`:
`I_HV = n_D*i_D + n_N*i_N + I_leak`, with `I_leak` UNKNOWN (driver off-state, bleeder, feedback, other HV loads). **Never omit leakage/bleeder from final power budget.**

Sensitivity (NOT an approved design point): `i_D=2.5–3.5mA` (archival typical), `i_N=0.3–0.7mA` (illustrative span across *different* NE-2 product examples; not an allowable range for a single chosen part). At 205V and neglecting unknown extra HV current:

| UI state / interpretation | n_D | n_N | Illustrative I_HV | P_HV=205V×I |
|---|---:|---:|---:|---:|
| No lamps active | 0 | 0 | 0mA | 0W, excluding HV quiescent/bleeder |
| One-hot 12-step gauge, digits off | 0 | 1 | 0.3–0.7mA | 0.0615–0.1435W |
| Bar gauge half-filled, digits off | 0 | 6 | 1.8–4.2mA | 0.369–0.861W |
| Bar gauge fully filled, digits off | 0 | 12 | 3.6–8.4mA | 0.738–1.722W |
| Digits on demand, gauge off | 2 | 0 | 5.0–7.0mA | 1.025–1.435W |
| Both digits and all neon active | 2 | 12 | 8.6–15.4mA | 1.763–3.157W |

These are *illustrative conditional bounds only*, not manufacturer-guaranteed extremes, and cannot be used to lower the current design target without owner approval. In particular, the nominal 16mA stress target may remain useful even if expected typical usage is lower. Decimal point or other HV loads may increase demand. Confirm if 12-stage gauge is one-hot, bar graph, or cumulative pattern and if digits can overlap neon states.

## 2. Resistor and heat screening, not a component selection

For a digit at 205V supply and assumed 145V sustaining voltage, `R=(205-145)/i_D`. For 2.5mA, `R=24kΩ`, `P_R=(60V)(.0025A)=0.150W`; for 3.5mA, `R≈17.14kΩ`, `P_R=0.210W`. These are **nominal illustration**; include supply tolerance, sustaining voltage min/max, driver voltage drop, resistor tolerance, voltage coefficient, DC voltage/power derating and pulse/transient conditions before selection. In particular, an assumed 1/4W resistor may have insufficient hot-enclosure derating even if nominal 0.21W <0.25W.

For neon, do **not** transfer San Guang's 68kΩ at 110VAC directly to 205V DC. Its data give no DC sustaining voltage; `R=(205-V_neon,maintain-V_driver)/i_N` and `P_R=i_N*(205-V_neon,maintain-V_driver)` must remain symbolic until exact purchased bulb and its DC specifications are known. Current variation, ignition margin, dark effect, polarity/aging and visibility through the intended window require explicit verification.

At the illustrated simultaneous 2 digits+12 neon scenario, a **205V/16mA design target** is still required as specified; this report does not certify a reduction. Resistive and tube dissipation largely becomes enclosure heat even when HV conversion efficiency improves.

## 3. Connection to USB 500mA / battery assist and topology

Prior report [SYS-001A](2026-11-17-1403-JST-chatb-sys001-supply-mode-alternatives.md) shows at 205V/16mA, 3.28W HV output already exceeds USB 5V×498mA=2.49W ideal input ceiling. **NO-GO for USB-only 16mA at the configured BQ25185 limit.** Battery supplement can support higher loads in principle but may discharge battery even while USB is present. BQ DPPM is not proof of simultaneous charging. Source [TI BQ25185](https://www.ti.com/lit/ds/symlink/bq25185.pdf) §5.5/6.3.

Using the prior **ASSUMED** efficiencies `eta_HV=.70`, `eta_5=.85`, `P_5logic=.50W`, `P_SYSother=.50W`, `P_SYS=(205*I_HV/.70+.50)/.85+.50`. For a one-hot neon-only 0.3–0.7mA, `P_SYS≈1.19–1.33W`; for 12 neon only 3.6–8.4mA, `P_SYS≈2.35–3.98W`; for 2 digits only 5–7mA, `P_SYS≈2.82–3.51W`; for 2 digits+12 neon 8.6–15.4mA, `P_SYS≈4.05–6.39W`. The model includes hypothetical fixed overhead even when actual OLED off; it is **not** a measured operating profile. Compare USB power only after BQ SYS conversion loss and current-limit corners. The exact **same** HV output demand can be supplied via SYS→5V→flyback or a qualified 1S→HV flyback, but the latter changes efficiency, low-cell peak current, magnetics, thermal and OVP and is **not** automatically preferable. MAX668 coupled-inductor topology is already owned by separate Issue #2 research; do not duplicate.

A possible user-experience/architecture opportunity is a *low-power gauge-only USB mode* if actual bulb current, visibility and power-path constraints allow. This is **an alternative**, not an approved requirement or firmware rule. Higher USB input-current budget is another alternative but requires USB-C current advertisement, BQ configuration, eFuse and heat review; cannot be solved merely by using a larger adapter.

## 4. Required adversarial checks and decision gates

1. **Selected bulb traceability:** exact manufacturer and P/N of IN-12B and 12 neon; retrieve genuine manufacturer DC current, strike, maintaining voltage, aging/life and polarity limits. The archival 2.5–3.5mA and San Guang AC 0.7mA are not interchangeable with guaranteed device ratings.
2. **UI mode contract:** one-hot vs bar gauge, maximum simultaneously active neon, digits and decimal point overlap, OLED/audio startup and duty. Define worst simultaneous **peak**, continuous and average separately.
3. **HV electrical resistor chain:** at V_HV min/max, Vmaint min/max, driver drops, tolerance, temp, voltage coefficient and resistor voltage/power ratings, calculate min/max actual currents and lamp strike. No single resistor value approved here.
4. **Power path:** BQ DPPM and battery assist across 3.3/3.6/4.0V, battery absent, USB unplug/replug and load steps. Measure I_USB, I_BAT sign, V_SYS and 5V; prove low-cell L1/charger/cell thermal before continuous HV.
5. **Fault/safety:** independent OVP and hard stop, discharge, HV5524 unpowered state and sealed PETG temperature remain blockers; no HV operation without supervised safety approval.
6. **Chat C:** review archival PDF provenance, the nonhomogeneous 0.3–0.7mA neon comparison, numerical table, and risk that mode averages could be mistaken for 16mA stress-target replacement.
7. **Work:** after review, decide if SYS-001 should distinguish normal one-hot/bar usage vs full-stress mode. Owner must approve any change to 16mA design target or USB operation requirements.

## Outcome

**CONDITIONAL research:** evidence suggests the earlier 1mA/neon and 2mA/IN-12B were not uniquely justified, and UI semantics materially affect typical energy. **BLOCKED for actual lamp-current approval** due to exact part provenance and DC ratings; **NO-GO** USB-only full 16mA remains unchanged. **PENDING REVIEW**. Do not edit integrator-owned shared indexes. No Claim, no component adoption, no manufacturing/HV testing.
