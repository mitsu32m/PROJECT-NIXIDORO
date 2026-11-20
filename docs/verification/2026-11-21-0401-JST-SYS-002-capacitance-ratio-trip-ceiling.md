# SYS-002 / Issue #6 — capacitor spread constrains the OVP trip ceiling
Date: 2026-11-21 04:01 JST. Chat A deep-design. Branch: codex/reva-integrated-prototype-review.
Status: **PENDING REVIEW**. Formal Claim: NONE (Issue labels/atomic Claim not demonstrated). Verdict: **CONDITIONAL** mathematical bound; **BLOCKED** hardware decision.

## Task contract and repository baseline
Question: Given the prior SYS-002 illustrative one-open bleeder discharge limit, how does a real capacitor's effective max/min ratio constrain the *highest possible* OVP trip voltage? Scope excludes actual capacitor selection, approval, and HV tests. Exit: independently derive the inversion, calculate sensitivity and identify missing guaranteed inputs.
Read ai-workflow, handoff, open-issues, decisions, tech-tree.yaml and tech-tree.md, Issue #6, and preceding 2026-11-21-0001 SYS-002 report. Branch search confirmed exact branch exists; GitHub connector did not expose branch HEAD commit SHA, so starting HEAD is UNKNOWN (do not confuse blob SHA with HEAD). Exhaustive latest-report enumeration and concurrent-agent overlap not established. Shared indexes intentionally unchanged pending Work/C review.

## New result: trip ceiling from component spread
Let k = Ceff,max/Ceff,min >=1 for the *same candidate component* over all relevant bias, tolerance, temperature, aging and fault conditions. Let D=T/[Rremain,max ln(V0,max/Vsafe)] be the maximum effective capacitance allowed by the one-open discharge model. Then Ceff,min <= D/k. The residual-energy constraint E_tail,max < (Ceff,min/2)(Vlim² - Vtrip,max²) implies the **necessary** condition

Vtrip,max < sqrt(Vlim² - 2*k*E_tail,max/D).

If the radicand is nonpositive, no trip voltage can meet this model. Even with a positive radicand, this is NOT sufficient: the normal maximum voltage, comparator spread, switching overshoot, startup, hard-stop and actual capacitor values must also pass.

Use ONLY the prior report's explicitly ASSUMED example: E_tail=0.2253mJ, Vlim=220V, D=1.100uF (2.1MΩ surviving branch, 220->60V within 3s). Computed trip ceilings:
| k (ASSUMED) | Max permissible Vtrip,max (V), strict upper bound | Ceff,min permitted by discharge (uF) |
|---:|---:|---:|
| 1.0 | 219.067 | 1.100 |
| 1.2 | 218.880 | 0.917 |
| 1.5 | 218.597 | 0.733 |
| 2.0 | 218.125 | 0.550 |
| 3.0 | 217.179 | 0.367 |

Numbers are illustrative, not manufacturer guarantees. The exact D should be recomputed from unrounded values; table uses D=1.100uF rounded to match the prior report. The prior 219.17V example remains infeasible even for k=1.

## Engineering consequence and challenge
The earlier two-inequality screen can be inverted to form an immediate *component-specific rejection test*: obtain guaranteed Ceff,min and Ceff,max, derive k, then compare the actual comparator's guaranteed high trip against this ceiling. A nominal 1uF label is insufficient. This explicitly exposes the penalty of capacitor spread: k=2 forces the hypothetical trip below ~218.13V, even though the discharge limit alone permits a nominal 1.1uF. It does NOT establish an acceptable lower trip threshold; that requires a guaranteed normal dynamic upper voltage, including load transients.

The post-trip 0.2253mJ is only one hypothetical 44uH/3.2A pulse, not an upper bound on MAX668 coupled-inductor energy. Likewise 60V/3s are NOT approved touch-safety limits; no source hard-off is proven. Capacitor voltage rebound, common bleeder-trace opens, converter re-energization and actual dielectric derating remain excluded. MAX668 datasheet: https://www.analog.com/media/en/technical-documentation/data-sheets/MAX668-MAX669.pdf . No manufacturer capacitor part was qualified in this run.

## Requested follow-up
Chat B: provide an exact in-stock HV capacitor MPN with manufacturer worst-case Ceff,min/max at 205–220V, rated voltage, temperature and aging. Chat A: obtain topology-specific guaranteed tail-energy and comparator trip bounds, not more assumed RC examples. Chat C: independently check inversion, strict inequalities and rounding; Work: do not adopt values until normal dynamic window and shutdown/discharge conditions are proven.
No purchasing, fabrication, HV energization, main merge, BOM/KiCad change or specification change. **PENDING REVIEW**.
