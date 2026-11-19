# PROJECT-NIXIDORO — Research Tech Tree

Status snapshot: **2026-11-19 JST**. Canonical data: [tech-tree.yaml](tech-tree.yaml).
Evidence: [WORK-INT-003](verification/2026-11-19-work-integration-003.md), [decisions](verification/decisions.md), [open issues](verification/open-issues.md).

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
  N_SYS_002["SYS-002 Joint HV capacitance OVP startup and discharge contract (in_progress)"]
  N_HV_002 --> N_SYS_002
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

## Current integration notes

[WORK-INT-003](verification/2026-11-19-work-integration-003.md) integrates C-REVIEW-003/004/005/006 within reviewed scopes. Mode/startup/DC algebra has additional review; no actual HV stage, cell or temperature-sensor assembly is qualified.

THERM-001 (#9) makes charge inhibit and separate battery-only thermal enforcement an explicit BAT-001 prerequisite. The integrated PWR draft still has CE=GND; BQ TS is inactive battery-only. Direct NTC alone cannot enforce candidate P2150K +10..45C. Proposed circuitry is pending review, not implemented. New restricted Rs/Rp ratio screen in INT-003 is PENDING INDEPENDENT REVIEW.

TE STM010 PDF body is 20±1mm, while its environmental ratings differ from the web page; actual attachment and thermal lag remain unqualified. PROTO-001 partial candidate evidence is in thermal-qualification-holds.csv, not a purchase BOM. HV actual topology/magnetics #2 and joint OVP/capacity #6 remain urgent.

YAML nodes, statuses, evidence paths and full dependency edges are structurally validated against all Mermaid views; no missing dependency or cycle is accepted. Historical research/rejected branches are preserved; no hardware gate is unlocked. Physical tests, purchases, fabrication, main merge or important specification changes require the existing explicit approvals.
