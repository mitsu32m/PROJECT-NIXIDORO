# PROTO-001I — Protected 21700 holder qualification contract and dimensional go/no-go
Date: 2026-11-19 21:00 JST
Role: Chat B (wide research). Issue #7. **PENDING REVIEW / NO FORMAL CLAIM**.
Branch: codex/reva-integrated-prototype-review.
Starting HEAD: **UNKNOWN** — GitHub connector supports branch-specific file reads but does not expose branch commit SHA; repository-wide commit search returned stale/default-branch history, and GitHub API branch URL retrieval failed. Do not confuse file blob SHA or previous report commit with current branch HEAD.

## Scope and exit
After PROTO-001H identified P2150R, derive a falsifiable holder acceptance checklist and worst-case dimensional bounds for both P2150R/P2150K. Avoid repeating NTC R/T or claiming a holder has been selected. Exit: explicit geometry/electrical/thermal/procurement evidence contract, a quantitative rejection screen, and next actual-MPN retrieval priorities.

## Sources and traceability (manufacturer primary, accessed in previous same-day report)
- Keeppower P2150K: https://www.keeppower.com/product/keeppower-21700-5000mah-protected-li-ion-rechargeable-battery-p2150k/ ; Dmax 21.5mm, L=75.0±0.2mm, charge +10..45 C. Datasheet-level PCM trip thresholds and actual holder fit UNKNOWN.
- Keeppower P2150R: https://www.keeppower.com/product/p2150r-keeppower-21700-5000mah-protected-li-ion-rechargeable-battery-max-15a/ ; Dmax 21.6mm, L=74.5±0.2mm, continuous discharge rating stated 15A, charge +10..45 C. This rating is not proof of terminal/holder/PCM/enclosure thermal limits.
- Internal baseline: docs/verification/2026-11-19-1703-JST-chatb-proto001h-p2150r-protected-cell-alternative.md; docs/verification/2026-11-19-work-integration-003.md; docs/verification/handoff.md and open-issues.md, read at working branch.

## Dimensional rejection screen (GUARANTEED only insofar as source dimensional wording is correct)
| Cell | Stated length interval | Stated max diameter | Holder evidence needed |
|---|---:|---:|---|
| P2150K | 74.8..75.2 mm | 21.5 mm | Holder manufacturer working length range must cover 74.8..75.2mm; bore/side clearance must accommodate 21.5mm plus wrap and insertion tolerance |
| P2150R | 74.3..74.7 mm | 21.6 mm | Holder working length range must cover 74.3..74.7mm; bore/side clearance must accommodate 21.6mm plus wrap and insertion tolerance |

These bounds are *necessary*, not sufficient: actual contact protrusion, button-top geometry, spring force vs travel, wrap, dimensional measurement conventions, cell polarity and insertion/removal are unqualified. A holder labeled '21700' does NOT imply accommodation of a ~75mm protected cell. If manufacturer holder supported maximum length <75.2mm, reject it for P2150K unless an actual controlled drawing/qualified exception proves otherwise. If holder supported maximum diameter <21.6mm, reject it for P2150R. A holder that only supports 70mm nominal bare cells is not a qualified candidate.

## Current and thermal screen (ASSUMED)
Worst target output P_HV = 205*0.016=3.28W. With illustrative eta=0.7 and Vbat=3.0V, Ibat=3.28/(0.7*3)=1.562A *before* MCU, PCM/contact/wire losses. At 2.5V, 1.874A. These are not validated low-cell states.
For two terminal contacts of 25mohm EACH (ASSUMED), contact dissipation at 1.874A is I²*0.050=0.176W; for 100mohm EACH, 0.702W. This fourfold difference is a strong reason to demand per-contact Rmax, rated current, contact plating and temperature-rise evidence; no such limits have been established for any actual holder. Peak startup currents and wear/corrosion may exceed this example.

## Mechanical, safety and procurement qualification matrix
- Actual holder **MPN and controlled manufacturer drawing**: UNKNOWN; get min/max supported battery length and diameter, contact geometry, spring compression range/force, terminal polarity and retention under shock.
- Holder current rating and contact resistance at operating temperature, aging/cycles and after enclosure assembly: UNKNOWN; compare against startup and continuous *bounded* current from Chat A #8, not cell's 15A marketing alone.
- Probe attachment: candidate TE STM010 head diameter 5mm, length 20±1mm (manufacturer PDF body, NOT misleading 15mm document name); do not simply add 20mm to cell length unless axial layout is actually selected. Verify separate clearance, cable bend radius, strain relief, insulating layer, cell sleeve integrity, and reproducible cell contact.
- Battery thermal interlock: no primary proof P2150R/P2150K PCM provides temperature cutoff. BQ25185 TS battery-only measurement inactive per TI Rev.B §6.4; Chat A #9 must define separate enforcement. Do not infer thermal safety from holder geometry.
- Sourcing: Japan distributor, SKU, landed JPY incl tax and shipping, quantity/stock timestamp, lead time, authenticity, substitutes and return terms all UNKNOWN. No invented vendor stock/price.
- Do not solder to cell, modify PCM or deform sleeve. No electrical/HV bench test is authorized by this report.

## Decision and Chat C handoff
**CONDITIONAL analytical screening; physical holder adoption BLOCKED; PENDING REVIEW.** Reject unqualified nominal-21700 holders and any model with documented envelope smaller than candidate cell maxima. This is a research contract, not part selection. For next B run obtain at least two real holder MPNs with manufacturer dimension drawings and Japanese availability, or explicitly document that no source-qualified candidate was found. Also prioritize actual DC neon lamp MPN and controller+magnetics pair to avoid repeated NTC-only work.
Review requests: (1) confirm length/diameter bounds from manufacturer wording; (2) challenge assumed contact heating and whether 'two contacts' model is adequate; (3) check that thermal interlock remains separate; (4) require dated vendor evidence before BOM adoption.
SOP proposal: docs/ai-workflow.md v1.1 already authorizes provisional research and separate dated reports; no direct shared index edit proposed. Work should consolidate after Chat C review.
