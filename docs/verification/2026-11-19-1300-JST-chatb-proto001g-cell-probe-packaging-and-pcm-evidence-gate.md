# Chat B PROTO-001G — protected 21700 / probe assembly envelope and PCM evidence gate

- Date: 2026-11-19 13:00 JST
- Role: Chat B wide research; Issue #7, dependency #9; **provisional research, NO FORMAL CLAIM**
- Branch: `codex/reva-integrated-prototype-review`
- Starting branch HEAD: **UNKNOWN** (GitHub connector fetch_file/search_branches succeeded but did not expose branch commit SHA; commit search returned older unrelated history; do not confuse blob SHA with HEAD).
- Status: **PENDING REVIEW** for Chat C; engineering disposition: **CONDITIONAL analytical screening / BLOCKED component qualification**.
- Scope: dimensional bounds, exact missing PCM evidence, assembled sourcing gates; not another NTC electrical comparison, not a thermal-interlock schematic, no purchase/test authorization.

## Repository baseline and prior reviews

Read `docs/ai-workflow.md` v1.1, `docs/verification/handoff.md`, `docs/verification/open-issues.md`, `docs/verification/decisions.md`, `docs/tech-tree.yaml`, `docs/tech-tree.md`, `hardware/integration/thermal-qualification-holds.csv`, `docs/verification/2026-11-19-work-integration-003.md`, and GitHub Issues including #7, #8, #9 and #7 review comments. Work explicitly asks B to stop repeating generic NTC analyses, and to find actual PCM thermal cutoffs/holder/probe controlled drawings and complete cost. C-006 establishes TE STM010 PDF BODY 20±1 mm head (not 15 mm), 5 mm nominal diameter, 1 m lead; TE page versus PDF environmental limits conflict. No qualifying PCM thermal cutoff evidence is present in the examined canonical matrix.

## A. Geometry: measurable envelope before choosing a holder

| Item | Source-class | Known | Still unknown |
|---|---|---|---|
| Keeppower P2150K candidate | manufacturer page, rechecked in WORK-INT-003 | 21.5 × 75.0 mm, stated ±0.2 mm | actual purchased lot and sleeve geometry, terminal and spring geometry, permitted contact/adhesive regions |
| TE GA10K3435STM010 | manufacturer PDF body 01/2022, independently reviewed C-006 | nominal Ø5 mm head; axial length 20±1 mm; 1 m cable | complete tolerance envelope, bend radius, adhesive/insulation stack and cable exit |
| Holder | UNKNOWN | no qualified MPN/drawing | protected-21700 fit, spring travel, contact force, terminal contact resistance, cable routing, creepage and PETG mounting |
| Pack PCM | UNKNOWN | marketed as protected, not proof of thermal cutoff | actual PCM part/revision, overcurrent trip curve, charge/discharge thermal cutoff presence, hysteresis and cell-surface sensing location |

**Analytical fit bounds, not a CAD fit claim:** If the 20±1 mm probe head were placed *end-to-end* with a maximum-length 75.2 mm cell, the bare axial occupied length would be 96.2 mm, **before** terminals, spring travel, wire exit, insulation, and mechanical clearance. Minimum corresponding head+cell is 74.8+19=93.8 mm. This is a deliberately pessimistic orientation screen, not a recommendation. Side-mounting the Ø5 mm probe can avoid that additive axial length, but nominal cell diameter 21.5 mm plus nominal 5 mm radial head yields a minimum **26.5 mm side-by-side bounding width**, before tape, cable and holder wall; physical overlap/offset, curvature and mounting can alter the bound. Both arrangements need actual assembly drawing. The nominal 26.5 mm is not a guaranteed maximum or minimum outside the stated simple side-by-side geometry.

**CAD acceptance checklist:** obtain holder manufacturer drawing and stated compatible protected-cell length; dimension maximum cell, minimum/maximum holder spring travel and contact force; probe attachment surface and adhesive thickness; insulated cable strain relief and minimum bend radius; serviceability and cell replacement; thermal distance from charger/HV components; assembly interference at tolerance corners. An ordinary 21700 holder label does not guarantee 75 mm protected cell fit.

## B. PCM thermal protection: explicit proof gap

The P2150K manufacturer's +10..45°C charge / −20..60°C discharge **operating ranges are not evidence that the PCM automatically disconnects at these temperatures**. A PCM marketed for overcharge, overdischarge, short and overcurrent cannot be assumed to implement charge-temperature and discharge-temperature cutoffs. The currently reviewed BQ25185 §6.4 p19 does not monitor TS in battery-only mode; present /CE=GND permits charge when other conditions allow. Hence separate charge and battery-only enforcement remains Issue #9, not a part property supplied by a generic 'protected' label.

Required vendor evidence request (do not assert answers): exact pack revision and PCM PCB/protection IC marking; charge/discharge continuous and pulse current at specified temperatures; charge/discharge temperature cutoff thresholds with tolerance/hysteresis, actual sensing element and position, and whether temperature protection exists at all; short/OCP thresholds and delay; contact and PCM resistance at ~2 A, thermal dissipation; datasheet/certification traceability, stock and seller authenticity. If temperature cutoff is absent, explicitly mark **NO PCM THERMAL CUTOFF** and retain independent hardware thermal enforcement requirement. If vendor does not disclose the data, **UNKNOWN, not qualified**.

## C. Preliminary cost and schedule gate

The canonical holds CSV records historical reported sensor-only prices: TE STM010 JPY 2,830.30, TE DM010 JPY 1,808.40, SEMITEC 103AT-2 JPY 123.20. These are **dated observations, not current quotes**. No cost is yet confirmed for protected cell + qualified holder + sensor harness + cable termination + attachment + thermal inhibit hardware + shipping/tax/rework. Thus neither the JPY40k initial / JPY10k reserve split nor the complete JPY50k budget is proven.

A sourceable BOM row must include exact MPN/revision, manufacturer drawing URL and version, distributor and observed date, Japan stock and delivery date, tax, shipping allocation, MOQ, physical footprint, qualification hold, alternatives and a separate assembled-cost subtotal. Do not compare a bare 103AT-2 price with a finished insulated probe price without harness labor/material and tests.

## D. Decision and next research

- **CONDITIONAL:** P2150K + STM010 remain candidates for controlled mechanical layout only; no fit, PCM thermal protection or charge safety approved.
- **BLOCKED:** holder/probe assembled BOM and PCM temperature protection claims until controlled primary evidence and exact sourced parts.
- **Priority next Chat B:** obtain a real protected-21700 holder MPN/drawing, manufacturer PCM cutoff documentation or documented non-disclosure, exact DC neon lamp model and two complete controller+magnetics sourcing pairs. Escalate lack of evidence rather than repeat sensor-only sensitivity.
- **Chat A #9:** independent charge-inhibit and battery-only load cut paths, including MCU-off and fault, are still required regardless of this packaging screen.
- **Chat C:** review geometric assumptions and challenge any mistaken interpretation of a pack's allowed temperature range as an automatic cutoff.
- **SOP proposal:** when branch HEAD cannot be resolved by connector, report UNKNOWN explicitly, avoid blob-SHA substitution; prefer a branch metadata endpoint before commit and reread after. Do not directly edit `docs/ai-workflow.md` from Chat B.

## Sources

- https://www.keeppower.com/ja/product/keeppower-21700-5000mah-protected-li-ion-rechargeable-battery-p2150k/
- https://www.te.com/commerce/DocumentDelivery/DDEController?Action=srchrtrv&DocFormat=pdf&DocLang=English&DocNm=Single_Insulated_TPE_OM_Probe_5x15mm&DocType=Data+Sheet&PartCntxt=GA10K3435STM010
- https://www.ti.com/lit/ds/symlink/bq25185.pdf (Rev.B §6.4 p19)
- `docs/verification/2026-11-19-work-integration-003.md`; `docs/verification/2026-11-19-0905-JST-C-REVIEW-006-ts-entry-te-probe-primary-check.md`; `hardware/integration/thermal-qualification-holds.csv`.

No hardware operations, requirements change, main merge, task schedule changes or part adoption.
