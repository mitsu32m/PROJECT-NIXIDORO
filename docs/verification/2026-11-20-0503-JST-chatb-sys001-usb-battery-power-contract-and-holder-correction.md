# Chat B — SYS-001 USB/BAT operating-mode power contract and PROTO-001J correction
Date: 2026-11-20 05:03 JST
Status: **PENDING REVIEW** (Chat C); technical outcome **CONDITIONAL** for ideal power bounds, **BLOCKED** for real hardware adoption.
Role: Chat B wide research, provisional / NO FORMAL CLAIM.
Branch: codex/reva-integrated-prototype-review
Starting HEAD: UNKNOWN (connected GitHub branch search returns name without commit SHA; commit search is default-branch biased). Do not substitute blob SHA.
Parent: SYS-001, PROTO-001 (#7); related #4, #8, #9.

## Bounded question and scope
Correct the contact/SYS lower-bound mistake flagged by C-REVIEW-009 and establish a mode-specific conservation-of-energy bound that distinguishes USB-only, USB+BAT assistance and actual charging. This is an analytic screen, not an approved power path or part selection. No change to the 205V/16mA *target*.

## Source and provenance
- Repository handoff/open-issues/decisions/tech-tree YAML and Markdown, ai-workflow v1.1, issue #7 and C-REVIEW-009 issue comment read 2026-11-20.
- C-REVIEW-009: https://github.com/mitsu32m/PROJECT-NIXIDORO/blob/1f4b2dbd4357a1a54a960ec6d65271a7307cd383/docs/verification/2026-11-20-0230-JST-C-REVIEW-009-charge-ramp-holder-contact.md
- TI BQ25185 datasheet Rev.B §6.4 p19 as cited in WORK-INT-003 (battery-only TS measurement NO). Primary-source re-download/revision confirmation still required before physical adoption.
- Manufacturer qualification of cell, controller+magnetics pair, lamp current, holder resistance, guaranteed converter efficiencies: UNKNOWN. No fresh distributor stock claims.

## Input classification
ASSUMED scenario: V_USB=5.0 V, I_USB_limit=0.500 A, P_HV=205 V*0.016 A=3.280 W, HV stage efficiency eta_HV=0.70 or 0.80, upstream 5V efficiency eta_5=0.85 or 0.90. These efficiencies are NOT manufacturer guaranteed and cannot be multiplied if topology is direct SYS->HV.
DOCUMENTED proposal: BQ25185 USB limit 500mA, charge target 250mA; whether actual current-limit behavior and system priority provide the assumed steady available power must be independently proven.
UNKNOWN: lamp simultaneous-on current (16mA may be a budget, not need), SYS rails, actual losses, startup, battery assist topology.

## Conservation-of-energy screen
USB-only ideal P_in <= 5*0.5=2.50 W. Since P_HV=3.28W, USB-only continuous target is impossible even with lossless conversion and zero control load. At eta_HV=0.80 and eta_5=0.90, required USB input for HV alone is 3.28/(.8*.9)=4.556 W or 0.911A at 5V; at .70*.85 it is 5.513W or 1.103A. This is not a proposal to increase USB limit.
Maximum *hypothetical* HV budget with no other load and 2.5W input is 2.5*.8*.9=1.80W, corresponding to 8.78mA at 205V; or 2.5*.7*.85=1.4875W, 7.26mA. USB cable/eFuse/charger/system losses and CTRL make real limits lower.
For USB+BAT: P_USB + P_BAT_discharge >= P_HV/(eta_HV*eta_5)+P_other_input_equivalent, with efficiencies applied only to the specific cascaded topology. Under .8*.9, minimum battery supplemental *input-side equivalent* = 4.556-2.50=2.056W before control/charger losses. Actual battery power differs by its path losses; at assumed 3.0V and lossless battery path the lower bound is 0.685A; actual current is higher. Under .70*.85 the corresponding lower bound is 3.013W and 1.004A at 3.0V.
For USB+BAT net charge, battery discharge is negative by sign convention; net charge and 16mA full HV require USB input to cover HV plus charge plus losses, which is impossible at 500mA. During USB-present load support, positive IBAT means cell is **discharging**, not charging. Charger setting 250mA is not a guaranteed simultaneous charging current.
For battery-only, P_BAT must cover HV plus CTRL and conversion losses; USB power is zero. Do not use BQ TS as a battery-only thermal enforcement path.

## C-REVIEW-009 correction: reference nodes and lower bound
Let V_cell_tab be voltage across actual electrochemical cell terminals under load, R_PCM be effective series protection impedance, R_holder include BOTH holder contacts, R_wire include wiring/connectors, and V_SYS include power-path drop after pack output. Define V_pack_out = V_cell_tab - I_BAT*(R_PCM+R_holder+R_wire). Then V_SYS = V_pack_out - V_powerpath_drop (assuming discharge path), and if bounded worst-case V_cell_tab >= V_cell_tab,min, I_BAT <= I_max, R_j <= R_j,max, V_powerpath_drop <= V_drop,max, a conservative lower bound is V_SYS >= V_cell_tab,min - I_max*(R_PCM,max+R_holder,max+R_wire,max) - V_drop,max. The inequality applies only if each bound is guaranteed at the relevant temperature/aging and no nonlinear cutoff intervenes. Without such bounds, V_SYS,min remains UNKNOWN. If a vendor voltage is specified at pack output rather than cell tabs, do NOT subtract PCM resistance a second time. If using a measured V_pack_out under load, subtract only downstream path drop. No 2.2A contact sensitivity value is a guaranteed maximum.
Example ONLY: I=2.2A and R_holder=0.1ohm yields 0.22V and 0.484W; this is NOT a qualified SYS minimum or an EOL contact limit.

## Alternatives and decision gates
A) USB-only reduced simultaneous current: needs explicit owner approval for display-mode limits and exact lamp ratings, no change yet.
B) Battery-assisted full 16mA: needs actual signed BAT path, charger current priority, low-cell cutoff, THERM-001 independent battery-only enforcement, thermal and runtime budget.
C) Direct SYS->HV: avoid assuming a 5V stage efficiency; requires real qualified controller+magnetics and startup/OVP evidence. MAX668 ordinary single-inductor boost remains rejected in its documented scope; coupled-inductor/flyback alternatives remain unqualified.
D) USB higher input contract: requires explicit USB-C/charging architecture change and user approval, not assumed from 500mA proposal.
Independent OVP, hard-off and discharge are required in all options; do not equate charger /CE with HV energy isolation.

## Review requests / exit criteria
Chat C: check power-path efficiency boundaries and lower-bound inequality against C-REVIEW-009; confirm signed battery modes and no double-counting. Chat A #8/#9: supply actual path netlist, guaranteed current/temperature corners and enforcement architecture. Work: decide whether simultaneous 16mA is truly required per mode before BOM freeze. Chat B next: manufacturer-controlled actual DC lamp datasheet and two controller+magnetics pairs with documented sourcing, not more generic holder sensitivity.
Result: CONDITIONAL analytic envelope, physical design BLOCKED; **PENDING REVIEW**. No purchase, manufacture, HV energization, main merge, schematic or SOP modification.
