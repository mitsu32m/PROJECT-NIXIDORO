# C-REVIEW-004 — HV-004 lamp evidence and SYS-001 direct-SYS architecture (batch independent review)

- Date: 2026-11-18 21:03 JST; reviewer: Chat C, no formal Claim.
- Branch: `codex/reva-integrated-prototype-review`; **start HEAD `460099cd5bacdb3afac296d71cd88185a5039ce5`**.
- Scope: Chat B [HV-004A 2026-11-17 17:02](2026-11-17-1702-JST-chatb-hv004-lamp-provenance-load-envelope.md), [SYS-001C 2026-11-17 21:00](2026-11-17-2100-JST-chatb-sys001-direct-sys-hv-power-path-screen.md), and [SYS-001D 2026-11-18 01:00](2026-11-18-0100-JST-chatb-sys001d-direct-hv-controller-primary-screen.md). Parent GitHub Issue #4; related #7/#8. Scope excludes full transformer qualification, actual lamp testing, OVP implementation, battery selection.
- Exit: rederive the load and SYS-power tables, challenge heterogeneous lamp data, identify conditional design decision and source checks, retain unreviewed claims as such.
- Read mandatory six canonical files and WORK-INT-002, C-REVIEW-003, issue queue and relevant A tapped-inductor report at branch; the full branch report tree was not available via connector, so **queue totals are lower bounds only**.
- Evidence labels: **TARGET** 205V/16mA, **ASSUMED** etaHV=.70, eta5=.85, etaDirect=.60/.70/.80, P5logic=.50W, Pother=.50W; **TYPICAL/illustrative** archival IN-12B 2.5–3.5mA, cross-product NE-2 .3–.7mA; **UNKNOWN** exact lamp P/N, guaranteed DC current/voltage, ageing, selected magnetic and SYS minimum. No measured data.

## 1. Primary-source and provenance checks

- Directly inspected San Guang Electronics one-page [NE-2 6x16x50 manufacturer sheet](https://www.taydaelectronics.com/datasheets/files/1039.PDF) on 2026-11-18: the page explicitly couples **110 VAC**, **68 kOhm**, and **approx. 0.7mA**. It also says breakdown voltage **65 VAC max** and lifetime **25,000h min** under the described application. The source **does not state a 205V DC recommended current, DC maintaining voltage, DC life or selected lamp equivalence**. Verdict **ACCEPTED** for source classification; **BLOCKED** for transferring its AC values to 205V DC resistor/current design.
- Opened the [IN-12B archival scan](https://nixie-tube.com/nixie/data/in-12/IN-12B_data.pdf), but its one-page scanned contents did **not yield independently readable text** through the available source interface. **UNVERIFIED** in this review: the cited 145V and 2.5–3.5mA, original manufacturer's identity, and exact pin mapping. They remain B's source-attributed secondary/archival values, not Chat C-certified ratings. Independent physical pinout verification is required before wiring.
- Jameco listing (different NE-2 marketed variant), TI BQ25185, TPS61023 and both direct-controller datasheets were **not directly re-opened in this batch**; their manufacturer specifications remain source-attributed, not newly verified. Prior C-REVIEW-003/WORK-INT-002 checked bounded BQ sections. No claim of complete primary-source review.

## 2. Independent arithmetic: HV-004A — CONDITIONAL

`I_HV = n_digit*i_digit + n_neon*i_neon + I_bleeder + I_driver_leak + I_other`.
Ignoring unknown extras **only for sensitivity**, using the mixed-source illustrative intervals `i_digit=2.5..3.5mA`, `i_neon=0.3..0.7mA`, `V=205V`:

| Digits | Neon | I low..high mA | P low..high W | Verdict |
|---:|---:|---:|---:|---|
| 0 | 1 | 0.3..0.7 | 0.0615..0.1435 | ACCEPTED arithmetic only |
| 0 | 6 | 1.8..4.2 | 0.369..0.861 | ACCEPTED arithmetic only |
| 0 | 12 | 3.6..8.4 | 0.738..1.722 | ACCEPTED arithmetic only |
| 2 | 0 | 5.0..7.0 | 1.025..1.435 | ACCEPTED arithmetic only |
| 2 | 12 | 8.6..15.4 | 1.763..3.157 | ACCEPTED arithmetic only |

This is **not** a min/max specification for any purchasable set of lamps: the .3 and .7mA values refer to different marketed lamps and AC usage; 2.5..3.5mA is archival typical, not worst-case. The 16mA continuous HV target stays unchanged.

The B report's derived SYS ranges have minor rounding errors at the low end:
`P_SYS=(205*I_HV/0.70+0.50)/0.85+0.50` (I in A) yields for 12 neon alone **2.3286..3.9824W** (B writes **2.35..3.98W**), for two digits alone **2.8109..3.5000W** (B writes **2.82..3.51W**). For one-hot **1.1916..1.3294W** and 2 digits + 12 neon **4.0513..6.3941W**, matching B within ordinary rounding. **CHANGES_REQUESTED** for the two lower-end table entries, but the conceptual mode comparison is **CONDITIONAL** and not a hardware operating guarantee.

Resistor illustration with 205V source and assumed 145V tube drop: at 2.5mA `R=24kOhm, P_R=.15W`; at 3.5mA `R=17.1429kOhm, P_R=.21W`. **ACCEPTED** algebra only; the 145V and current limits are not independently authenticated and no voltage/thermal derating proven. No resistor value approved.

## 3. Independent arithmetic: SYS-001C/D — CONDITIONAL

For identical HV output and retained 5V logic:
`P_base=(P_HV/eta_HV+P_5logic)/eta_5+P_other`
`P_direct=P_HV/eta_direct+P_5logic/eta_5+P_other`.
Subtract: `Delta=P_HV*(1/(eta_HV*eta_5)-1/eta_direct)`; direct path saves SYS power **iff eta_direct > .70*.85 = .595**, ignoring topology-dependent quiescent and changing-load efficiency. **ACCEPTED algebra**.

At 205V/16mA: baseline **6.60084W**; direct 60% **6.55490W**, 70% **5.77395W**, 80% **5.18824W**. B 21:00 table writes 5.775 and 5.189W at the last two points; these are minor rounding (~1mW), not material. At direct 70%, saving **0.82689W**. **CONDITIONAL** as a hypothetical scenario, not measured efficiency or reduced cell temperature. Direct SYS→HV retains SYS→5V logic and is **not** BAT→HV: the latter bypasses the BQ SYS path and requires separate cell/UVLO/fault/charging review.

For USB-only at full HV target: **205*0.016=3.28W** output; configured 5V*0.498A=**2.49W** ideal maximum USB input under B's quoted 498mA corner (this particular manufacturer limit not freshly re-read in this batch). Even at 100% efficiency **2.49<3.28**, so **ACCEPTED energy-conservation impossibility under stated 500mA setting**. Real 5V source tolerances and losses only worsen this; USB presence cannot be taken as evidence of net charging. The full-mode USB-only design is **NO-GO** under this setting, not a reason to silently reduce 16mA.

SYS-001D: LT3757A and LM5155 low-VIN product specifications were **not independently re-opened** in this batch; candidate status remains **PENDING independent manufacturer verification**, **BLOCKED** as actual 205V/16mA controller+magnetics design. The 1.5A LM5155 gate-driver figure must not be misread as permissible primary current. Real SYS floor, UVLO, FET gate voltage, magnetics and BOM remain unknown.

## 4. Faults, alternatives, and cross-system decision

- Actual lamp current and brightness must be established from **exact selected parts** at **DC** with manufacturer guarantees or a separately approved, supervised test; verify ignition, maintaining voltage, polarity, dark effect, ageing and current-limit resistor hot/voltage derating. The AC NE-2 sheet cannot fill these fields.
- Define one-hot vs cumulative/bar 12-lamp gauge, digits/decimal-point overlap and peak/continuous/average separately. A low-load normal mode does not supersede the 16mA maximum target.
- Check BQ power-path signed battery current, min SYS, USB unplug, battery absent/protector trip, TPS61023 L1 Isat/DCR and thermal; calculate both actual direct and two-stage efficiency at relevant loads. A theoretical .8269W saving does not justify a new controller without real controller+magnetics pair.
- HV5524 220V recommended limit, independent OVP, hard-off, tail energy, capacitor Cmin/Cmax and discharge remain BLOCKED. Tube and resistor dissipation is enclosure heat regardless of improved conversion efficiency. Actual sealed PETG cell temperature remains UNKNOWN.
- No component selection, 16mA target change, main merge, procurement, PCB manufacturing, HV energization or hardware safety signoff.

## 5. Work decision package — priority P0, **handoff through GitHub only**

**Decision:** Separate actual display operating modes from maximum 16mA stress while retaining the latter; should Work consider a direct-SYS HV path before a real lamp/BQ power contract exists?

**A/B claim:** B HV-004A argues the existing 2mA/digit+1mA/neon current sum is assumed and gauge mode dominates typical demand; B SYS-001C/D proposes direct SYS flyback and two-controller screening.

**Independently verified:** San Guang's 110VAC/68kOhm/~0.7mA is AC-specific; illustrative HV-current and most SYS-power arithmetic, corrected two low-end rounding entries; .595 break-even formula; 3.28W>2.49W ideal USB-only contradiction.

**Unverified:** IN-12B scanned technical data and pin mapping, exact neon DC specs, UI simultaneity, lamp ageing/brightness, BQ full corners in this batch, LT3757A/LM5155 full manufacturer ranges, controller+magnetics matched pair, real efficiency and thermal/OVP.

**Alternatives:** preserve two-stage baseline, compare SYS-direct controller+qualified transformer, consider lower-load gauge-only USB mode **only after** lamp and UI evidence and human approval of behavior, or change USB input-current architecture only by explicit human design approval. BAT-direct is a separate architecture.

**System effects:** HV-004/SYS-001 load and mode envelope, HV-001 magnetics, PWR-001/002/BAT-001 battery-assist/thermal, SYS-002 capacitor/startup/OVP, BOM-001/PROTO-001. Normal lamp usage may reduce average load, but maximum current target and protection margins remain unchanged.

**Recommended Work disposition:** **ACCEPTED** limited arithmetic/source classification; **CHANGES_REQUESTED** minor SYS table corrections; **CONDITIONAL** research comparison; **BLOCKED** actual lamp resistor/part selection and any SYS-direct HV architecture adoption. Require #7 exact lamp P/N, manufacturer DC evidence and mode policy, #8 SYS/BAT thermal table, and manufacturer-backed controller+magnetics pair before selecting HV architecture. No unconditional forwarding of all B reports.

**Sources and provenance:** three linked B reports above, [WORK-INT-002](2026-11-18-work-integration-002.md), [C-REVIEW-003](2026-11-18-1502-JST-C-REVIEW-003-sys001e-f-dcm-startup.md), manufacturer San Guang PDF; start SHA `460099cd5bacdb3afac296d71cd88185a5039ce5`. The resulting review commit SHA is given in the GitHub commit/issue comment (cannot be embedded into its own committed content).

## 6. Backlog and next review

- **3 source reports reviewed** in this batch, some claims deliberately remain unverified.
- **At least 4 high-priority source reports remain unreviewed** (A 23:59/03:55/07:56 tapped series; A PWR-002A), plus B PROTO-001 and other later work if present; **complete count UNKNOWN** without recursive branch tree and exhaustive review-index comparison. Do not misstate this as a complete queue.
- **Oldest identified still-unreviewed candidate:** A 2026-11-17 23:59 tapped-boost ideal screen (verify full tree).
- **Next:** (1) A PWR-002A cell/BATFET/thermal and B PROTO-001 exact part sourcing as a related P0 batch if reports exist; (2) A tapped-boost 23:59/03:55/07:56 equations and real circuit mismatch; (3) B SYS-001D primary controller table after opening actual datasheets.
- No formal Claim; shared indices left to Work integrator.
