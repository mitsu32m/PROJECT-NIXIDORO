# PROJECT-NIXIDORO — Research Tech Tree

Status snapshot: **2026-11-25 JST**. Canonical data: [tech-tree.yaml](tech-tree.yaml).
Evidence: [WORK-INT-008](verification/2026-11-25-2159-JST-WORK-INT-008-neon-revision-and-lifecycle-gate.md), [WORK-INT-007](verification/2026-11-25-0956-JST-WORK-INT-007-cutoff-energy-and-current-gates.md), [decisions](verification/decisions.md), [open issues](verification/open-issues.md).

Views below partition the canonical dependency edges. Repeated IDs denote the same node; all incoming prerequisites apply together, including MILE-02 parts A and B. Alternative nodes are candidates, not adopted hardware. Locked release gates do not prohibit research. No node count implies percentage complete or permission to buy/test/fabricate.

States: documented = artifact exists; in_progress = exit evidence incomplete; alternative = comparison candidate; rejected = rejected in stated scope; locked = release gate incomplete; verified = only a precisely passed scope. There are no newly verified hardware nodes.

## 1. Requirements and draft baseline

```mermaid
flowchart TB
  N_REQ_001["REQ-001 Requirements baseline documented (documented)"]
  N_NET_001["NET-001 Rev.A net spec proposed (documented)"]
  N_PWR_DR["PWR-DR PWR Rev.A schematic draft (documented)"]
  N_CTRL_DR["CTRL-DR CTRL schematic draft (documented)"]
  N_HV_DR["HV-DR HV logic/interface draft (documented)"]
  N_HV_OLD["HV-OLD MAX668 non-coupled single-inductor boost rejected (rejected)"]
  N_NET_001 --> N_CTRL_DR
  N_NET_001 --> N_HV_DR
  N_NET_001 --> N_HV_OLD
  N_NET_001 --> N_PWR_DR
  N_REQ_001 --> N_NET_001
  classDef documented fill:#18794e,color:#fff
  class N_CTRL_DR,N_HV_DR,N_NET_001,N_PWR_DR,N_REQ_001 documented
  classDef rejected fill:#991b1b,color:#fff
  class N_HV_OLD rejected
```

## 2. HV comparisons and voltage protection

```mermaid
flowchart TB
  N_HV_DR["HV-DR HV logic/interface draft (documented)"]
  N_HV_COUPLED["HV-COUPLED MAX668 coupled-inductor boost comparison candidate (alternative)"]
  N_HV_001["HV-001 Proven HV power stage or approved reduced-current alternative (in_progress)"]
  N_HV_002["HV-002 HV regulation tolerance and OVP window (in_progress)"]
  N_HV_003["HV-003 Independent OVP hard-off and discharge (locked)"]
  N_HV_004["HV-004 IN-12B and neon lamp current budget (in_progress)"]
  N_HV_DIRECT["HV-DIRECT Direct SYS HV controller and magnetics alternative (alternative)"]
  N_HV_001 --> N_HV_002
  N_HV_002 --> N_HV_003
  N_HV_DR --> N_HV_001
  N_HV_DR --> N_HV_004
  N_HV_DR --> N_HV_COUPLED
  N_HV_DR --> N_HV_DIRECT
  classDef documented fill:#18794e,color:#fff
  class N_HV_DR documented
  classDef in_progress fill:#a16207,color:#fff
  class N_HV_001,N_HV_002,N_HV_004 in_progress
  classDef locked fill:#475569,color:#fff
  class N_HV_003 locked
  classDef alternative fill:#2563eb,color:#fff
  class N_HV_COUPLED,N_HV_DIRECT alternative
```

## 3. Supply and operating modes

```mermaid
flowchart TB
  N_PWR_DR["PWR-DR PWR Rev.A schematic draft (documented)"]
  N_CTRL_DR["CTRL-DR CTRL schematic draft (documented)"]
  N_THERM_001["THERM-001 Charge and battery-only thermal enforcement interface (in_progress)"]
  N_HV_001["HV-001 Proven HV power stage or approved reduced-current alternative (in_progress)"]
  N_HV_004["HV-004 IN-12B and neon lamp current budget (in_progress)"]
  N_PWR_001["PWR-001 5V regulator power and thermal feasibility (in_progress)"]
  N_BAT_001["BAT-001 Protected cell and NTC specification (in_progress)"]
  N_PWR_002["PWR-002 Charger and battery-assist loss and thermal validation (in_progress)"]
  N_SYS_001["SYS-001 Mode-specific HV PWR CTRL power contract (in_progress)"]
  N_CTRL_DR --> N_THERM_001
  N_PWR_DR --> N_THERM_001
  N_THERM_001 --> N_BAT_001
  N_BAT_001 --> N_SYS_001
  N_HV_001 --> N_SYS_001
  N_HV_004 --> N_SYS_001
  N_PWR_001 --> N_SYS_001
  N_PWR_002 --> N_SYS_001
  N_PWR_DR --> N_BAT_001
  N_PWR_DR --> N_PWR_001
  N_PWR_DR --> N_PWR_002
  classDef documented fill:#18794e,color:#fff
  class N_PWR_DR,N_CTRL_DR documented
  classDef in_progress fill:#a16207,color:#fff
  class N_BAT_001,N_HV_001,N_HV_004,N_PWR_001,N_PWR_002,N_SYS_001,N_THERM_001 in_progress
```

## 4. Shared capacitor energy contract

```mermaid
flowchart TB
  N_HV_002["HV-002 HV regulation tolerance and OVP window (in_progress)"]
  N_HV_003["HV-003 Independent OVP hard-off and discharge (locked)"]
  N_PWR_001["PWR-001 5V regulator power and thermal feasibility (in_progress)"]
  N_HV_CUT_TPS["HV-CUT-TPS TPS22918 upstream cutoff comparison candidate (alternative)"]
  N_SYS_002["SYS-002 Joint HV capacitance OVP startup and discharge contract (in_progress)"]
  N_HV_002 --> N_SYS_002
  N_HV_003 --> N_HV_CUT_TPS
  N_HV_003 --> N_SYS_002
  N_PWR_001 --> N_SYS_002
  classDef in_progress fill:#a16207,color:#fff
  class N_HV_002,N_PWR_001,N_SYS_002 in_progress
  classDef locked fill:#475569,color:#fff
  class N_HV_003 locked
```

## 5. Physical interfaces and HV bench review

```mermaid
flowchart TB
  N_NET_001["NET-001 Rev.A net spec proposed (documented)"]
  N_HV_001["HV-001 Proven HV power stage or approved reduced-current alternative (in_progress)"]
  N_HV_003["HV-003 Independent OVP hard-off and discharge (locked)"]
  N_HV_004["HV-004 IN-12B and neon lamp current budget (in_progress)"]
  N_MILE_01["MILE-01 HV bench prototype safety review (locked)"]
  N_SYS_002["SYS-002 Joint HV capacitance OVP startup and discharge contract (in_progress)"]
  N_MECH_001["MECH-001 Physical HV interfaces insulation and enclosure thermal evidence (in_progress)"]
  N_HV_001 --> N_MILE_01
  N_HV_003 --> N_MILE_01
  N_HV_004 --> N_MILE_01
  N_MECH_001 --> N_MILE_01
  N_NET_001 --> N_MECH_001
  N_SYS_002 --> N_MILE_01
  classDef documented fill:#18794e,color:#fff
  class N_NET_001 documented
  classDef in_progress fill:#a16207,color:#fff
  class N_HV_001,N_HV_004,N_MECH_001,N_SYS_002 in_progress
  classDef locked fill:#475569,color:#fff
  class N_HV_003,N_MILE_01 locked
```

## 6. Integrated release prerequisites, part A

```mermaid
flowchart TB
  N_PWR_001["PWR-001 5V regulator power and thermal feasibility (in_progress)"]
  N_MILE_01["MILE-01 HV bench prototype safety review (locked)"]
  N_MILE_02["MILE-02 Integrated prototype approval (locked)"]
  N_PWR_002["PWR-002 Charger and battery-assist loss and thermal validation (in_progress)"]
  N_SYS_001["SYS-001 Mode-specific HV PWR CTRL power contract (in_progress)"]
  N_MILE_01 --> N_MILE_02
  N_PWR_001 --> N_MILE_02
  N_PWR_002 --> N_MILE_02
  N_SYS_001 --> N_MILE_02
  classDef in_progress fill:#a16207,color:#fff
  class N_PWR_001,N_PWR_002,N_SYS_001 in_progress
  classDef locked fill:#475569,color:#fff
  class N_MILE_01,N_MILE_02 locked
```

## 7. Integrated release prerequisites, part B and CTRL

```mermaid
flowchart TB
  N_CTRL_DR["CTRL-DR CTRL schematic draft (documented)"]
  N_BAT_001["BAT-001 Protected cell and NTC specification (in_progress)"]
  N_CTRL_001["CTRL-001 CTRL reverse-feed, HV gating and RTC (in_progress)"]
  N_MILE_02["MILE-02 Integrated prototype approval (locked)"]
  N_SYS_002["SYS-002 Joint HV capacitance OVP startup and discharge contract (in_progress)"]
  N_BAT_001 --> N_MILE_02
  N_CTRL_001 --> N_MILE_02
  N_CTRL_DR --> N_CTRL_001
  N_SYS_002 --> N_MILE_02
  classDef documented fill:#18794e,color:#fff
  class N_CTRL_DR documented
  classDef in_progress fill:#a16207,color:#fff
  class N_BAT_001,N_CTRL_001,N_SYS_002 in_progress
  classDef locked fill:#475569,color:#fff
  class N_MILE_02 locked
```

## 8. Parts, cost and manufacturing gate

```mermaid
flowchart TB
  N_NET_001["NET-001 Rev.A net spec proposed (documented)"]
  N_BOM_001["BOM-001 Fully costed parts list (in_progress)"]
  N_MILE_02["MILE-02 Integrated prototype approval (locked)"]
  N_MILE_03["MILE-03 PCB manufacturing release (locked)"]
  N_PROTO_001["PROTO-001 Traceable staged prototype BOM and sourcing (in_progress)"]
  N_BOM_001 --> N_MILE_03
  N_MILE_02 --> N_MILE_03
  N_NET_001 --> N_BOM_001
  N_NET_001 --> N_PROTO_001
  N_PROTO_001 --> N_BOM_001
  classDef documented fill:#18794e,color:#fff
  class N_NET_001 documented
  classDef in_progress fill:#a16207,color:#fff
  class N_BOM_001,N_PROTO_001 in_progress
  classDef locked fill:#475569,color:#fff
  class N_MILE_02,N_MILE_03 locked
```

## 9. Flyback sourcing and scoped rejection

```mermaid
flowchart TB
  N_HV_DR["HV-DR HV logic/interface draft (documented)"]
  N_HV_FLYBACK["HV-FLYBACK LT3757 controller with qualified HV magnetics candidate (alternative)"]
  N_HV_Q44["HV-Q44 Q4434 Q4435 qualified 205V pair claim rejected (rejected)"]
  N_HV_DR --> N_HV_FLYBACK
  N_HV_FLYBACK --> N_HV_Q44
```

## 10. Multiplier and ordinary boost distinction

```mermaid
flowchart TB
  N_HV_DR["HV-DR HV logic/interface draft (documented)"]
  N_HV_MULT["HV-MULT LT8365 multiplier adaptation candidate (alternative)"]
  N_HV_LT8365_BOOST["HV-LT8365-BOOST LT8365 ordinary boost to 205V rejected (rejected)"]
  N_HV_DR --> N_HV_MULT
  N_HV_DR --> N_HV_LT8365_BOOST
```

## 11. Comparator and actual magnetic candidates

```mermaid
flowchart TB
  N_HV_002["HV-002 HV regulation tolerance and OVP window (in_progress)"]
  N_HV_OVP_TLV["HV-OVP-TLV TLV6700 precision OVP comparison candidate (alternative)"]
  N_HV_002 --> N_HV_OVP_TLV
```

```mermaid
flowchart TB
  N_HV_FLYBACK["HV-FLYBACK LT3757 controller with qualified HV magnetics candidate (alternative)"]
  N_HV_CJ5143["HV-CJ5143 CJ5143 continuous flyback comparison candidate (alternative)"]
  N_HV_WE839["HV-WE839 Wurth 750315839 continuous flyback comparison candidate (alternative)"]
  N_HV_FLYBACK --> N_HV_CJ5143
  N_HV_FLYBACK --> N_HV_WE839
```

## Current integration notes

[WORK-INT-008](verification/2026-11-25-2159-JST-WORK-INT-008-neon-revision-and-lifecycle-gate.md) adds A1A revision/DC current and exact-suffix lifecycle gates (D-027/D-028).03/17 Rev2 nominal0.5mA/95VDC differs from undated manufacturer design0.6mA/90VDC; no applicable lot established. PCN333 lists A1A-T obsolete2014, not bareA1A. New B/Work evidence pending C; all node states/dependencies unchanged. Landed budget/11/25 evidence incomplete at examined HEAD; no adoption/release.

[WORK-INT-007](verification/2026-11-25-0956-JST-WORK-INT-007-cutoff-energy-and-current-gates.md) integrates C-027 and partially checks still-pending A04:01. D-024 inventories downstream LV cap energy after upstream opening, magnetic storage, timing supply and alternate feeds with same actual HV Cmin/Cmax. TPS22918 candidate is alternative,2us is typical,no maximum, LV QOD weakens atVIN loss and is notHV discharge.
C-027 confirms Work005 timing/Wurth scope and B09:03 arithmetic. D-025 keeps LT8365 lowSYS proxy distinct from actual charge-pump SW current. No real topology/parts or safety gate qualified.11/25 09:56 evidence and landed budget remain incomplete; no hardware/spec change.


[WORK-INT-005](verification/2026-11-24-1003-JST-WORK-INT-005-ovp-timing-and-magnetics-gates.md) integrates C-025/026. TI p6 Figure1 correction: INB rising→OUTB falling=tPLH29us NOM, not18us;maximum stop unknown. Precision-divider arithmetic is not OVP proof; TLV candidate stays alternative.
CJ5143 1.2A is L characterization, not continuous rating. Würth003.001 pins/dots and functional-insulation wording partially verified;typ3.2A and50–200kHz typical application do not guarantee target. New candidate nodes are alternatives, no hardware verification/gate unlock.
B11/23 21:03 arithmetic subsequently reviewed by C-025. B11/24 09:03 subsequently reviewed by C-027 within arithmetic/source scope. All whole-system, temperature/thermal, actual lamp and budget holds below still apply.


[WORK-INT-004](verification/2026-11-23-2201-JST-WORK-INT-004-power-discharge-topology-integration.md) integrates C-007〜024 and independently checks manufacturer conditions. No hardware node verified or release gate unlocked.
D-017 canonical load accounting separates lamps/bleeder/OVP-divider/driver-leakage, consistent voltage nodes, overhead and signed BAT current. 16mA lamp/bus boundary remains undecided. Single330k and dual300k discharge are separate alternatives; negative budget means INFEASIBLE. Example dual bleeder/450mA cannot support two digits alone. No real lamp current, resistor, capacitor or mode adopted.
D-018 retains passive/switched/hybrid discharge alternatives with same actual Cmin/Cmax, tail, startup, common-return and no-power fault proof. D-019 records manufacturer1:1 false-positive sourcing and LT8365 ordinary-boost exclusion while retaining multiplier/controller candidates.
THERM-001 remains independent charge and battery-only load enforcement plus separate HV residual discharge. C-007 reviewed the restricted Rs/Rp ratio theorem only. B11/23 21:03 arithmetic was subsequently reviewed by C-025; no physical mode qualified.
Current landed budget UNKNOWN; initial40k/reserve10k/total50k unproven. Real drawings/MPNs/thermal/fault/quotes take priority over repeated hypothetical tables. Historical reports and rejected branches preserved. YAML/Mermaid IDs, states and all dependency edges must be validated before and after commit.

