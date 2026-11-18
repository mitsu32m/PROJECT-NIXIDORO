# C-REVIEW-003 — SYS-001E/F: DCM current consistency and startup energy (independent review)

- Reviewer: Chat C, 2026-11-18 15:02 JST; provisional, no formal Claim.
- Start branch HEAD: `a86b0c66e0a3890bbb150c212179e4a0954405e9`.
- Branch: `codex/reva-integrated-prototype-review`.
- Parent: SYS-001 / HV-001 / PWR-002 / SYS-002; GitHub Issue #4 (and #2/#6 dependencies).
- B reports reviewed (2):
  - [SYS-001E, 05:03](2026-11-18-0503-JST-chatb-sys001e-lt3757-flyback-magnetics-risk.md)
  - [SYS-001F, 09:00](2026-11-18-0900-JST-chatb-sys001f-hv-startup-usb-battery-energy-budget.md)
- Scope: independently check DCM algebra, efficiency consistency, HV capacitor startup arithmetic, USB-only and battery-deficit bounds; inspect primary manufacturer sources only for explicitly identified parameters. No schematic, component selection, procurement, HV operation or safety approval.

## 1. Independent source checks

1. [ADI LT3757/LT3757A PDF](https://www.analog.com/media/en/technical-documentation/data-sheets/lt3757-3757a.pdf), accessed 2026-11-18, **current online PDF identifies itself as Rev. H**, whereas B SYS-001E calls the same link Rev. G. **CHANGES_REQUESTED**: pin the exact revision used, update citations/page numbers and re-check the relevant DCM design passage against Rev. H. Page 1 specifies 2.9–40V operating range and flyback support; this does not qualify 205V/16mA, a transformer or low-SYS start. The PDF's electrical table states 2.9V minimum operating range and a 100/110/120mV SENSE threshold across specified conditions, but the complete converter design must still be verified.
2. [TI BQ25185 SLUSF65B Rev.B, Aug 2026](https://www.ti.com/lit/ds/symlink/bq25185.pdf), accessed 2026-11-18: first page confirms configurable 500mA input current limit, power-path management, BATFET typical 115mOhm and *up to* 3.125A system-load feature. These are **not** a guarantee that an unspecified protected cell, PCB or 3V SYS can deliver the hypothetical 2.31A continuously. The exact 450/475/498mA electrical-table corners quoted by B/Work are not independently rechecked in this review, so retain as source-attributed, not newly certified.
3. Other manufacturer PDFs (TPS61023, HV5524, LM5155), user-reported magnetic failure and distributor stock were **not** independently inspected in this run. Preserve their existing unreviewed evidence status.

## 2. SYS-001E DCM consistency: CHANGES_REQUESTED

B assumes TARGET Vout=205V, Iout=16mA, Pout=3.28W; ASSUMED Vin=3.0V, eta=0.70, D=0.65, D2=0.25, D3=0.10, f=200kHz. Algebraic recheck:
- `Iin,avg=Pout/(eta*Vin)=1.56190476 A`.
- `Ipk,proxy=2*Iin,avg/D=4.80586081 A`.
- `Lp,proxy=Vin*D/(f*Ipk)=2.02877439 uH`.
- Ideal volt-second ratio `n=Ns/Np=Vout*D2/(Vin*D)=26.28205128` (diode ignored).
- But this ratio and primary peak imply `Is,avg=D2*Ipk/(2*n)=0.02285714286 A`, **not 0.016A**. Relative discrepancy `1/eta-1=42.8571%`.
- `0.5*Lp*Ipk^2*f=Pout/eta=4.685714 W` is consistent as a hypothetical **input** energy flow only. Treating that same lossless ideal transformer and turns ratio as delivering 16mA is inconsistent.

For a coherent **lossless ideal DCM** at the stated D/D2/n and target output: `Ipk,ideal=2*n*Iout/D2=3.36410256 A`; `Lp,ideal=Vin*D/(f*Ipk)=2.89824561 uH`; `0.5*Lp*Ipk^2*f=3.28W`. A **real** 70%-efficient design cannot be inferred by applying 70% to the input peak while leaving the ideal secondary current and ratio unchanged; specify actual loss distribution, flux/volt-second, switching intervals, effective turns, leakage, clamp, diode and output loading. The B report already labels the 4.8A as proxy, but it should explicitly state this contradiction and not present the 2uH/26:1/4.8A point as simultaneous feasible operating conditions.

Verdict by claim: algebraic input current **ACCEPTED** under eta assumption; ideal reset ratio **CONDITIONAL** under ideal transformer assumptions; simultaneous DCM operating point **CHANGES_REQUESTED**; transformer/205V/16mA hardware **BLOCKED**.

## 3. SYS-001F startup arithmetic: ACCEPTED only as a sensitivity screen

Independently computed with C=4.7uF, V=205V, t=0.5s:
- `E=0.5*C*V^2=0.09875875 J` (98.75875mJ).
- `Pcap,avg=E/t=0.1975175 W`.
- `Icap=C*V/t=0.001927 A` for a linear ramp.
- `Pcap,end=V*Icap=0.395035 W`, twice average.
- With full hypothetical 16mA load, `PHV,avg=3.4775175 W`; assumed etaHV=0.70, eta5=0.85, 5V logic=0.5W and other SYS=0.5W gives `PSYS=(PHV/0.70+0.5)/0.85+0.5=6.9328 W` (rounded).
- At 3.0V SYS, `I_SYS,avg≈2.311 A`, **not** a guaranteed battery current.
- `5V*0.498A=2.49W` ideal USB input maximum under the cited 500mA setting; hypothetical deficit `6.9328-2.49≈4.443W` is a lower bound on non-USB **power contribution** if these assumptions hold. It cannot be converted into a guaranteed 21700 current without BAT voltage, BATFET/protection drops, conversion losses and dynamic response.
- `0.5*100uF*(5^2-4.5^2)=0.0002375J`, `0.0002375/4.443≈0.05345ms`. Valid only as a small-cap energy example, not rail stability simulation.

Verdicts: energy/ramp arithmetic **ACCEPTED**; full-lamp startup and assumed efficiencies **CONDITIONAL**; actual USB/BAT startup feasibility, source handoff and thermal **BLOCKED**. Crucial missing evidence: same physical HV capacitor's Cmin for OVP and Cmax for startup/discharge, actual BQ SYS floor, battery protection path, TPS61023 startup, lamp blanking and physical thermal evidence. This supports D-013's joint capacitor design requirement, **not** a capacitor value or mode approval.

## 4. Work decision package (important, no implementation approval)

**Decision:** Should Work adopt SYS-001E's 2uH/26:1/4.8A hypothetical direct-SYS flyback as a component/BOM design point, and should startup be included in the system power contract?

**A/B claim:** B's 05:03 hypothetical 70%-efficiency DCM proxy yields 4.8A and 2uH; B's 09:00 report adds HV capacitor charging and source handoff to the load model. Work-INT-002 already flagged the DCM mismatch.

**Confirmed:** DCM proxy is internally inconsistent as a simultaneous ideal operating point; 16mA coherent ideal example is ~3.364A and ~2.898uH under identical timing assumptions; startup cap arithmetic and hypothetical 6.93W SYS demand are correct. Online LT3757/A PDF currently Rev. H, not B's cited Rev. G. TI BQ25185 supports power path and battery supplement features, not guaranteed complete system operation.

**Unconfirmed:** transformer and controller pair, actual efficiency/loss distribution, current sense, switching and startup envelopes, 21700/BATFET/thermal, manufacturer limits beyond the explicitly checked passages, real HV capacitor and OVP tail-energy.

**Alternatives:** compare actual 5V flyback/coupled MAX668, SYS-direct LT3757A/LM5155 and a staged LV-first prototype; consider lamp blanking only with independently reviewed fail-safe hardware. Do not alter 16mA or USB design requirements without owner decision.

**System impact:** PWR-001/002, BAT-001, HV-001/002/003, SYS-001/002, thermal and BOM. **Recommendation:** CHANGES_REQUESTED for SYS-001E simultaneous DCM point and PDF revision; ACCEPTED for bounded SYS-001F energy method; BLOCKED for adopting any specific HV part or declaring safe startup. Keep D-013 and prototype milestones locked. Work should link this review to Issue #4 and request A/B to produce a single loss-consistent converter+source+capacitor state table with primary part evidence.

**Evidence:** source reports above at start SHA `a86b0c66e0a3890bbb150c212179e4a0954405e9`; [WORK-INT-002](2026-11-18-work-integration-002.md); ADI/TI PDFs linked above. This package is for GitHub-mediated Work handoff, not a claim of direct Work invocation.

## 5. Queue and next action

Review batch: **2 reports**, 2 primary PDFs inspected at bounded sections, no measurements. Unreviewed high-priority A/B reports remain (including A tapped-boost 23:59/03:55/07:56, A PWR-002A 12:03, B PROTO-001 13:02 and earlier B lamp/direct-SYS reports); full queue count must be established from a complete branch tree and review-index cross-check, not guessed from this diff. Oldest candidate visible in current Work index: B 2026-11-17 17:02 lamp provenance (verify against full queue). Next review priority: PWR-002A low-cell/BATFET/thermal and PROTO-001 magnetics sourcing; then A tapped-boost batch and B lamp/direct-SYS evidence. No Claim; no changes to shared indices, schematic, BOM, main, purchases or HV operations.
