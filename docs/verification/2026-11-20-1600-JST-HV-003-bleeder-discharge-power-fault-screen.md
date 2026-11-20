# HV-003 / Issue #6 — HV bleeder discharge, continuous loss and single-fault screen
Date: 2026-11-20 16:00 JST (scheduled research slot). Role: Chat A deep-design.
Branch: codex/reva-integrated-prototype-review. Starting branch HEAD: UNKNOWN (connector does not provide a verified branch-specific HEAD; blob SHA is not a commit SHA).
Claim: NONE (provisional selection from open-issues.md). Review: **PENDING REVIEW**.
Verdict: **CONDITIONAL** for ideal RC arithmetic; **BLOCKED** for a qualified independent discharge and OVP solution.

## Task contract
Parent: HV-003/HV-002C, GitHub Issue #6. Question: What are the continuous power and safe-discharge-time tradeoffs for a permanently connected HV bleeder at the 205 V target, and which single faults invalidate the result? Exit: reproducible nominal calculations, explicit worst-case equation, and circuit/part evidence gaps. No design approval or schematic edits.

## Current repository basis and distinction from earlier work
Read docs/ai-workflow.md, docs/verification/handoff.md, docs/verification/open-issues.md, docs/verification/decisions.md, docs/tech-tree.yaml, docs/tech-tree.md, 2026-11-20-1204-JST-THERM-001-ce-floating-default-evm-evidence.md, and GitHub Issues #6/#9. Current register says HV-003 hard-off/discharge is absent and SYS-002 requires *joint* Cmin/Cmax. Unlike previous OVP tail-energy reports, this note quantifies the *discharge resistor continuous thermal cost* and its failure modes. Full latest-report enumeration and exact starting HEAD were not verified.

## Ideal passive RC model — assumptions, not hardware qualification
ASSUMED: V0=205 V, Vsafe=60 V **illustrative endpoint only, not an approved touch-safe threshold**; C=1.0 µF nominal, R=0.1/1/10 MΩ nominal. Assume capacitor starts at V0, isolated converter cannot re-energize output, no load other than resistor, negligible dielectric absorption and parasitic leakage. These assumptions do NOT hold automatically during controller failure or HV5524 operation.

V(t)=V0 exp[-t/(RC)], t=RC ln(V0/Vsafe). E0=0.5 C V0²=21.0125 mJ. P0=V0²/R, I0=V0/R. Initial resistor dissipation is *continuous* during regulated HV operation, unlike the finite discharge event.

| R nominal | t 205→60 V with 1µF | I at 205V | P at 205V | P at 220V |
|---|---:|---:|---:|---:|
| 100 kΩ | 0.123 s | 2.05 mA | 420.3 mW | 484 mW |
| 1 MΩ | 1.229 s | 0.205 mA | 42.0 mW | 48.4 mW |
| 10 MΩ | 12.29 s | 20.5 µA | 4.20 mW | 4.84 mW |

For 205V/16mA output target (3.28W), 100k adds 0.420W (12.8% of target load), 1M adds 0.042W (1.28%), and 10M adds 0.0042W (0.128%). This is HV-output power, *not* input loss; actual input demand is higher by converter inefficiency. A 100k bleeder is therefore a substantial load and thermal tradeoff, not a free safety feature.

## Tolerance and dynamic conditions
For a guaranteed upper discharge time use Rmax, Cmax and maximum credible initial voltage:
tmax >= Rmax Cmax ln(V0,max/Vsafe). This expression becomes an upper-bound calculation **only after** Rmax, Cmax, V0,max and absence of recharging are all guaranteed. For illustration only, with R+5%, C+20%, V0=220V, t(1M)=1.05*1.2*ln(220/60)=1.637 s. Real capacitor voltage/temperature/aging effects and resistor tolerances must be specified.
The capacitor initial energy at 220V and 1µF is 24.2mJ; Cmax increases it. HV5524 recommended 220V is a device operation constraint, NOT a permissible safety-trip voltage or proof that V0 cannot exceed 220V.

## Failure analysis
1. **Bleeder open circuit or solder crack:** RC discharge disappears; retained HV is uncontrolled. A single passive resistor is not a single-fault-safe discharge solution.
2. **HV converter remains active, feedback or shutdown fails:** V(t) exponential decay assumption is false. Independent power interruption must precede credible discharge-time claims.
3. **Resistor voltage/working-voltage rating:** power rating alone does not prove that one chip resistor tolerates 205–220V continuously or a transient; manufacturer voltage ratings and PCB creepage/clearance required. Multiple series resistors may distribute stress but common-mode failures and voltage sharing need analysis.
4. **Resistor short:** high-energy source short/load fault; protection, startup and thermal behavior must be assessed.
5. **Capacitor dielectric absorption and wiring:** residual/rebound voltage and connector-access hazards require controlled supervised measurement; not represented by ideal RC.
6. **Display load removal:** bleeder does not guarantee regulation/OVP, and HV capacitor minimum for OVP energy may conflict with maximum for startup/discharge.

## Decisions and next evidence
- CONDITIONAL: ideal RC discharge and continuous loss numbers only.
- NO-GO (limited): treating a single bleeder resistor alone as proven independent, single-fault-safe discharge.
- BLOCKED: actual HV capacitor part Cmin/Cmax, resistor rated working voltage/power/temperature, independent HV source cutoff, discharge endpoint/time policy, measured rebound and single-fault analysis.
- Request Chat C to check the arithmetic and challenge the assumed Vsafe endpoint. Work should integrate only reviewed scope; do not update canonical tech-tree or decisions from this unreviewed result.
- Next actionable design work: compare actual rated HV resistor chains and output capacitors with full tolerances, then combine Cmax discharge with Cmin OVP residual-energy and low-cell startup. Do not adopt a resistor value from this screen.

No purchase, PCB manufacture, HV energization, main merge, or requirements change.