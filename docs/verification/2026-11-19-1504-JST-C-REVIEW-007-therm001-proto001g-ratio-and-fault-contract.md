# C-REVIEW-007 — THERM-001 / PROTO-001G: independent ratio, fail-safe interlock and packaging review

- Date: 2026-11-19 15:04 JST. Reviewer: Chat C. **NO FORMAL CLAIM**; review is not hardware safety approval.
- Branch: `codex/reva-integrated-prototype-review`; start HEAD `b4e9b27d07acfd0c3f1f57b5a0426a72af603ea0`; prewrite HEAD rechecked same.
- Bounded batch: Chat A [THERM-001 12:00](2026-11-19-1200-JST-THERM-001-interlock-fault-contract.md), Chat B [PROTO-001G 13:00](2026-11-19-1300-JST-chatb-proto001g-cell-probe-packaging-and-pcm-evidence-gate.md), and the explicitly PENDING C REVIEW mathematical claim in [WORK-INT-003](2026-11-19-work-integration-003.md). Issues #9/#7. Goal: validate algebra and proposed safety-state *requirements*, identify unproved circuit functions and mechanical claims, prepare one Work decision package.
- Startup read: `docs/ai-workflow.md`, `docs/verification/handoff.md`, `docs/verification/open-issues.md`, `docs/verification/decisions.md`, `docs/tech-tree.yaml`, `docs/tech-tree.md`; plus integration net spec, thermal holds CSV, C-REVIEW-006, the three target reports and Issues #7/#8/#9. Branch compare since C-006 showed three commits with these two new A/B reports and WORK-INT-003.
- Primary references: [TI BQ25185 Rev.B product/document index](https://www.ti.com/product/BQ25185) (Rev.B indexed 2026-08-25; direct PDF §6.4 not re-opened in this run; its p19 adapter/battery-only finding is from C-REVIEW-006), [Keeppower P2150K official product page](https://www.keeppower.com/product/keeppower-21700-5000mah-protected-li-ion-rechargeable-battery-p2150k/) (manufacturer page checked in this run; 21.5×75.0 mm ±0.2, charge +10..45°C, discharge -20..60°C, lists overcharge/overdischarge/overcurrent/short protection but **does not document thermal PCM cutoffs**). TE [GA10K3435STM010 manufacturer PDF](https://www.te.com/commerce/DocumentDelivery/DDEController?Action=srchrtrv&DocFormat=pdf&DocLang=English&DocNm=Single_Insulated_TPE_OM_Probe_5x15mm&DocType=Data+Sheet&PartCntxt=GA10K3435STM010) dimension/R-T figures are from independently source-checked C-006; PDF **not re-opened in this run**. No physical tests or exact PCB-netlist reinspection in this run.

## 1. Work restricted positive-resistor ratio theorem — ACCEPTED (algebra and stated topology only)

Let `a=R_NTC(10°C)=17.95kΩ`, `b=R_NTC(45°C)=4.92kΩ` (TE nominal table as cited by C-006), `a>b>0`. For `R_eff(T)=Rs+(Rp||R_NTC(T))`, `Rs>=0`, `Rp>0`, and temperature-independent positive components:
- `a/b = 3.6483739837`; nominal BQ entry voltage ratio `V_cold/V_hot=1.0075/0.115=8.7608695652`.
- `(Rp||a)/(Rp||b) = (a/b)*(Rp+b)/(Rp+a) < a/b`. Adding `Rs>=0` further contracts the ratio: for `x>y>0`, `(Rs+x)/(Rs+y) <= x/y`.
- Thus `R_eff(10)/R_eff(45) <= 3.648374 < 8.760870`; cannot simultaneously align *both nominal entry thresholds* at 10°C and 45°C in this restricted passive GND-to-TS network, with a fixed current bias.
- This does **not** prove impossibility of a different sensor, active circuit, temperature-dependent additional element, changed bias/reference, alternate charger, or independent /CE control. It also does not provide guaranteed trip temperatures; TE table values are nominal, TI thresholds have tolerance and hysteresis, and candidate 10..45°C is not a project-wide fixed specification.
- A single positive series or parallel resistor also cannot repair the ratio; don't waste design cycles optimizing that restricted family. **Verdict: ACCEPTED (mathematical impossibility under explicit restrictions), no component adoption.**

## 2. Chat A THERM-001 architecture and TS loading — CONDITIONAL / BLOCKED hardware

Independent arithmetic for assumed `I_TS=38µA`, `R_L=100kΩ` parallel to TE nominal NTC:
- 10°C: `R_eff=17.95*100/(117.95)=15.21831kΩ`; `V_TS=0.578296V` vs unloaded `0.682100V`; change `-0.103804V` (-15.22%).
- 45°C: `R_eff=4.92*100/(104.92)=4.689287kΩ`; `V_TS=0.178193V` vs unloaded `0.186960V`; change `-0.008767V` (-4.69%).
- A's rounded figures are consistent. **ACCEPTED as an illustrative DC resistor loading counterexample**, not as an actual ADC input impedance or measured BQ pin voltage. Actual MCU ADC sampling is dynamic; unpowered input clamp/backfeed and TS/MR multifunction semantics remain unproven.
- The proposed state table correctly separates **CHARGE_PERMIT** (must be able to inhibit charge without firmware), **LOAD_PERMIT** (battery-only thermal monitoring and effective load cut) and **HV_FAULT_STOP + capacitor discharge**. This is **CONDITIONAL as a design requirement contract**; not a proven implementation. /CE disables charging, not SYS/HV energy. `/CE=GND` in integrated draft means no independent inhibit wired today (from Work netlist inspection; not independently rerun).
- **CHANGES_REQUESTED** for fault-table precision: “MCU off/reset -> charge OFF” is a chosen fail-safe policy, while “unless independent hardware qualifies charge” is an exception; specify the exact independent power/enable arbitration and cold-start default. Distinguish battery-only “charge OFF (no adapter)” as no source present, not proof of hardware inhibit. Clarify a temperature monitor power-domain loss cannot leave a default-ON load switch. Require a concrete comparator/reference/switch/CE interface with guaranteed electrical levels and fault recovery, not just named signals.
- **BLOCKED** for actual safety qualification: no proven independent always-powered monitor, cell-surface temperature measurement and attachment, open/short/detachment diagnostics, fail-safe MOSFET/load isolation, standby drain, full-temperature tolerance/hysteresis/lag, cell/PCM qualification, or independent HV discharge.

## 3. Chat B PROTO-001G geometry and PCM — ACCEPTED arithmetic / CONDITIONAL envelope / BLOCKED sourcing

- Assuming cell length 75.0±0.2mm and probe head 20±1mm from previously reviewed manufacturer documents: `74.8+19=93.8mm`, `75.2+21=96.2mm` end-to-end bare axial envelope. **ACCEPTED arithmetic only**, with zero terminal, spring, insulation, cable or tolerance stack beyond those assumptions.
- Simple side-by-side diameter sum `21.5+5=26.5mm` is a **nominal outer span only** for unoverlapped round cross-sections. It is *not* a guaranteed minimum enclosure width across offset/curvature, mounting, protective sleeve and real holder geometry. B correctly flags this; avoid CAD clearance signoff.
- Manufacturer P2150K lists operating temperature ranges but no verified PCM thermal cutoffs. “Protected” alone is not charge/discharge temperature enforcement. **ACCEPTED** the evidence-gap distinction; **BLOCKED** holder fit, real PCM trip thresholds, contact resistance, harness assembly and JPY landed cost. Do not treat historical TE/SEMITEC sensor-only prices as assembly BOM.
- **CHANGES_REQUESTED**: require exact holder MPN/drawing and permissible 75.2mm cell length, mechanical sensor attachment/cable routing, controlled TE head drawing, PCM IC/revision or vendor written “unknown/no thermal cutoff”, and full assembled price/stock/tax/shipping. A generic holder name or unverified thermal PCM marketing claim cannot unlock PROTO-001.

## 4. Work decision package — P0 THERM-001 / BAT-001 / PROTO-001

**Decision target:** whether to retain BQ25185 with an independently enforced charge temperature window and battery-only load shutdown, versus a qualified temperature-protected pack/alternative charger; and whether P2150K+STM010 is ready for mechanical/BOM selection.

**A/B claims:** A proposes separate charge, load and HV-stop permits with fail-safe defaults and TS shared-sensor loading counterexample. B screens 93.8..96.2mm axial / 26.5mm nominal lateral geometry and identifies missing PCM cutoff and assembled BOM. Work proposes restricted Rs+(Rp||NTC) impossibility theorem.

**Verified:** Work resistor-ratio theorem under restricted assumptions; A DC loading arithmetic; B bare geometry arithmetic; Keeppower official P2150K published size, operating ranges and listed PCM protection types (no published temperature cutoff). TI Rev.B and TE PDF detailed tables rely on earlier C-006 verification, not new direct inspection here.

**Unverified:** actual TS threshold/cold-start/fault hardware behavior; selected pack/PCM cutoff, cell-probe thermal coupling, tolerances and installed geometry; exact 75.2mm holder fit, independent /CE default and load isolation; HV stored-energy discharge; cost, stock and full temperature envelope.

**Alternatives:** (1) BQ25185 plus qualified always-powered hardware charge window and battery-only monitor/load disconnect; (2) exact documented thermal-PCM pack plus compatible charging and separate HV isolation; (3) alternate charger/pack after owner authorization. Single passive Rs/Rp family cannot solve two nominal entry thresholds for P2150K/TE.

**System impact:** current /CE-GND draft cannot enforce candidate pack charge interval; battery-only TS is not active; fail-safe load cut and HV discharge need explicit hardware interfaces; extra sensors, comparator, switches, wiring, enclosure clearance, standby power and cost. No release gates unlocked.

**Recommended Work decision:** **ACCEPTED** limited ratio proof and arithmetic; **CONDITIONAL** fault-state *requirements*; **CHANGES_REQUESTED** specific fault default/arbitration and sourced assembly; **BLOCKED** component/circuit adoption and order readiness. Request Chat A #9 deliver one concrete primary-documented candidate circuit, guaranteed error/fault/latency/power table and full interface changes. Request Chat B #7 deliver actual holder drawing, PCM thermal evidence/non-disclosure and assembled cost. Work should keep D-014 staged LV-first only as a planning path, without physical-test authorization. No user requirements or HV targets changed.

**Provenance:** Chat A THERM-001 12:00, Chat B PROTO-001G 13:00, WORK-INT-003 and C-006 on starting HEAD `b4e9b27d07acfd0c3f1f57b5a0426a72af603ea0`; commit introducing this review is discoverable in GitHub history.

## 5. Queue / limits

- **New A/B reports reviewed in this batch:** 2, plus 1 new Work analytical claim.
- **Unreviewed important results:** at least **4** previously identified HV reports remain (A 2026-11-17 23:59 tapped ideal; A 2026-11-18 03:55 tapped CCM; A 2026-11-18 07:56 rectifier/capacitance; B 2026-11-18 13:02 magnetics sourcing). This is a lower bound, **not** an exhaustive tree count. Oldest known: A 2026-11-17 23:59 JST.
- **Next priorities:** (1) HV-001 tapped/coupled transformer and real sourcing batch #2/#7; (2) HV-002C joint Cmin/Cmax tail-energy OVP #6; (3) #9 actual fail-safe circuit and #7 PCM/holder evidence follow-up.
- **No formal Claim, no hardware safety approval, no purchase, PCB order, main merge, HV energization, important spec change or scheduler change.** Shared indices and KiCad untouched.
