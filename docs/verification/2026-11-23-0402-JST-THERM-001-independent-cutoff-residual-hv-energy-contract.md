# THERM-001 — Charge inhibit, battery-load isolation and residual HV are three separate safety functions
Date: 2026-11-23 04:02 JST
Role: Chat A / deep-design. Issue #9, related #6/#8. **PENDING REVIEW; NO FORMAL CLAIM.**
Branch: `codex/reva-integrated-prototype-review`
Starting verified HEAD: `29043fe8c3705c338e5403c236b85098cfeac117` (GitHub fetch_commit on exact branch).
Status: **CONDITIONAL** (logic/energy arithmetic), **BLOCKED** (real protection design). No hardware approval.

## Bounded question and exit
Question: Can a single thermal fault signal to BQ25185 /CE provide charging, battery-only load shutdown and safe HV de-energization? Answer by a state/fault matrix and energy calculation, without selecting components or changing KiCad. This extends C-REVIEW-020's battery-only cutoff blocker, rather than repeating prior CE threshold screens.

## Evidence and assumptions
- TI BQ25185 Rev.B (Aug 2026), https://www.ti.com/lit/ds/symlink/bq25185.pdf : /CE HIGH inhibits charge, LOW enables; §6.4 p19 battery-only TS measurement NO. Primary characteristics previously independently checked by C-REVIEW-010; not freshly retrieved here.
- Baseline PWR U1 /CE tied GND, TS/MR tied CELL_NTC per WORK-INT-003 and Issue #9. **PROPOSED baseline**, not a proven safety design.
- Independent review C-REVIEW-020 (2026-11-22) explicitly keeps BAT-only temperature cutoff BLOCKED.
- HV output 205V/16mA **TARGET**; C=1uF and discharge resistance R=1Mohm **ASSUMED illustration**, not selected BOM. No component ESR, leakage, fault energy or physical temperature measured.

## Three independent enforcement paths
1. **Charge admission**: thermal monitor and charger inhibit must work during USB insertion even if Pico 3V3 is absent; /CE alone is insufficient for /CE-short-to-GND single fault. A *separate upstream charge-energy interruption* or qualified independent pack charge protection must be investigated. The existing /CE=GND trace requires an approved redesign before it can act as an inhibit.
2. **Battery-only load isolation**: BQ TS measurement is absent in BAT-only. A temperature monitor powered in the relevant battery domain must inhibit a hardware load-energy path without depending on MCU execution. Distinguish switching off the 5V/HV converter from interrupting SYS/BAT; reverse feeds, monitor supply, and charger power-path continuity require analysis. A MOSFET with default-off gate is a *candidate architecture*, not a guaranteed isolated path until its body diode, orientation, gate leakage and off-domain paths are verified.
3. **Stored HV discharge**: removing charger or battery power does not instantly remove output capacitor energy. A supervised discharge mechanism must be separately specified and tested under power loss, switch open, bleeder open, short and MCU reset. Thermal inhibit cannot be called safe-HV-off without discharge proof.

## State and single-fault contract (proposal, not validated)
| Condition | Charge path requirement | Battery/HV load path requirement | Residual HV |
|---|---|---|---|
| USB present, MCU running, valid cell temperature | Permit only if verified temperature window | Load per power budget | OVP and discharge required |
| USB insertion, MCU off/booting | Default charge inhibited until monitor ready | Default HV off | Discharge still required |
| Battery only, MCU off | No charge possible | Hardware default HV/load off on fault | Discharge still required |
| NTC open/short/detached | Fault inhibits charge; distinguish contact thermal lag | Fault inhibits load | Discharge required |
| /CE short to GND | **/CE cannot inhibit**; independent charge energy cutoff needed | Independently evaluate load path | Discharge required |
| PCM opens while HV operating | Charger state and reverse feeds must be checked | No uncontrolled backfeed or restart | HV capacitor remains energized |
| Thermal monitor supply lost | Fail-inhibit required in all source states | Default load-off required | Discharge independent of monitor power |

## Reproducible residual-energy example
At V0=205V and assumed C=1uF, E0=0.5*C*V0^2=0.0210125J = **21.0125mJ**. If a *functioning* R=1Mohm bleeder is across the capacitor, tau=RC=1s; ideal decay to 60V is t=RC*ln(205/60)=**1.2287s**, and stored energy at 60V is **1.8mJ**. Initial bleeder power V0^2/R=**42.025mW**. A 1Mohm resistor's voltage rating, fault-open probability, effective C range and user-safe discharge threshold/time are UNKNOWN. This ideal RC example **does not establish safe touch or a discharge specification**. Cmax increases energy and time; bleeder-open gives no guaranteed decay. Converter tail energy and other capacitors are excluded.

## New cross-system conclusion
A single MCU fault flag or BQ /CE signal cannot be credited as all three barriers. The minimum research architecture needs distinct *charge energy interruption*, *battery-only HV/load interruption*, and *stored-HV discharge*, with fault coverage and power-domain independence established before any safety claim. This is a functional decomposition, not a mandate to add three particular switches. A thermally qualified pack may cover some functions only with controlled PCM evidence and faults.

## Next engineering evidence gates
- #9: select exact candidate charge cutoff and battery load cutoff devices and verify default-off under USB ramp, battery depletion, sensor faults, short-GND and off-domain backfeed; quantify bias, pin count, quiescent current, standby, cost and temperature accuracy/lag.
- #6: select Cmin/Cmax, bounded tail energy and guaranteed discharge path; jointly evaluate voltage ratings, OVP, resistor working voltage and open-fault coverage.
- #7: actual cell/PCM thermal trip behavior and pack-attached NTC evidence.
- #8: SYS/BAT power path under PCM opening and charger insertion, low-cell startup and sealed-enclosure thermal proof.
- Chat C independent review then Work shared-ledger integration; no shared indexes edited here to avoid concurrent writes.

No purchasing, PCB fabrication, HV energization, main merge, schematic edits or requirements changes.
