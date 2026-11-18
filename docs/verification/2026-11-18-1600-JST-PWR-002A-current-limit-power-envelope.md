# PWR-002A — Current-limited constant-power feasibility envelope

Date: 2026-11-18 16:00 JST (scheduled-slot label; actual execution timestamp not independently verified). Role: Chat A deep-design. Parent GitHub issue #8, PWR-002/PWR-001/SYS-001. **PENDING REVIEW; NO FORMAL CLAIM.**

Starting branch HEAD: **UNKNOWN**. GitHub file reads on branch succeeded; GitHub commit search returned 172753a9436820cd9d71a3f4b36b138b62dcd5ee as recent repository commit, but search does not prove this is the exact working-branch HEAD. Do not substitute this SHA. Read ai-workflow v1.1, handoff, open-issues, decisions, tech-tree.yaml and tech-tree.md; examined previous PWR-002A 12:03 report, WORK-INT-002 and current open issues #1–#8. Chat B handles sourcing #7, C review; this analysis does not choose a cell/inductor or repeat earlier resistance sweep. Scope: **new current-limit-constrained power bound** on prior model. Exit: explicit inequality and voltage-dependent resistance threshold, identify misleading mathematical roots, no hardware qualification.

## Manufacturer-grounded and assumed inputs
- [TI BQ25185 Rev.B](https://www.ti.com/lit/ds/symlink/bq25185.pdf): BATFET RON=140mΩ MAX **at VBAT=4.5V, IBAT=400mA**, not guaranteed for multiamp/high temperature. BAT overcurrent 3.13A TYP and ±18% **at 27°C**. Arithmetic 3.13*(1-.18)=2.5666A is a **27°C scenario** and NOT a guaranteed full-temperature continuous rating or safe design current. Actual limit/time response UNKNOWN.
- [TI TPS61023 Rev.B](https://www.ti.com/lit/ds/symlink/tps61023.pdf): valley current limit minimum 2.7A at specified VIN=3.6V/VOUT=5V; this is not a guaranteed 5V rail continuous output current or startup rating at 2.57V SYS.
- Existing WORK-INT-002 assumed maximum-display load P_SYS=6.60084W at assumed HV efficiency 70%, 5V boost 85%, logic 0.5W and SYS other 0.5W. This is **ASSUMED**, not measured or guaranteed. Audio, battery heating feedback and converter efficiency variation excluded.
- VBAT=3.0/3.3/3.6/4.0V are **ASSUMED terminal voltages**, not selected-cell approved voltage limits. R_BQ=0.14Ω **ASSUMED extrapolation**; R_EXT sensitivity 0/0.1/0.2Ω **ASSUMED**.

## New bound (independent of quadratic root selection)
With battery discharge positive, V_SYS=V_BAT-I R_total and P_SYS=I(V_BAT-I R_total). The low-current root from prior report is I=(V-sqrt(V²-4RP))/(2R). A real root only requires R<=V²/(4P); **this alone can falsely imply feasible operation even if current protection intervenes**.

For an illustrative current ceiling I_lim=2.5666A at 27°C, and for the lower-current branch with I_lim < V/(2R), the additional necessary inequality is

P_SYS <= I_lim (V_BAT-I_lim R_total),
R_total <= (V_BAT-P_SYS/I_lim)/I_lim.

The I_lim<V/(2R) condition is met at all tabulated corners below. At other corners, maximize P over 0<=I<=I_lim rather than blindly evaluating the endpoint. This is **not** a full-temperature hardware limit: it is a comparison against the published OCP accuracy under its stated test conditions. Thermal derating and converter current limits can be more restrictive.

| Assumed VBAT | Maximum total R from 27°C OCP screen | Remaining R_EXT after assumed 0.14Ω BQ path | Illustrative 0.10Ω R_EXT verdict |
|---|---:|---:|---|
| 3.0V | 0.1668Ω | 0.0268Ω | Fails OCP screen (prior low root 2.850A) |
| 3.3V | 0.2837Ω | 0.1437Ω | Passes *only this* screen (2.430A) |
| 3.6V | 0.4006Ω | 0.2606Ω | Passes *only this* screen (2.138A) |
| 4.0V | 0.5564Ω | 0.4164Ω | Passes *only this* screen (1.857A) |

At 3.3V and R_EXT=0.20Ω (R_total=0.34Ω), the quadratic has a real low-current root 2.819A; yet the 27°C lower OCP screen is 2.5666A. The corresponding current-limited maximum power is only 2.5666*(3.3-2.5666*0.34)=**6.230W**, less than assumed 6.60084W. Thus **mathematically real root ≠ allowed power path**. At 3.0V and R_EXT=0.20Ω the prior 4.189A root is still more misleading: OCP screen 5.460W, below demand.

For the assumed full-load 6.60084W, P/I_lim=2.5718V SYS at the current ceiling. This is **not** evidence that TPS61023 can regulate or start at this voltage. Existing project provisional HV-enable gate SYS>=3.4V would, if enforced, prevent full-HV operation at VBAT<=3.4V on battery-only regardless of resistance, because SYS<=VBAT. The gate is a provisional firmware policy, not a manufacturer limit; do not silently change it.

## Sensitivity and design implication
- A candidate protected cell must supply evidence for its **minimum terminal voltage under pulsed current**, protection PCB resistance, connector/contact resistance and thermal limits, not just nominal capacity or a 21700 label.
- This new bound is **more restrictive than the discriminant** in important corners, but still **optimistic** because the 140mΩ is not characterized at 2–3A, efficiencies are held constant and no startup or enclosure thermal dynamics are included.
- For each measured cell and L1 candidate, compute V_SYS(t), 5V valley current and current-limit margin at worst thermal conditions; include signed battery current with USB present, where charger supply/assist differs from battery-only equations. Do not apply battery-only quadratic directly to USB-assisted operation.
- No design adoption from this model. Next bounded investigation: actual TPS61023 5V input-power/valley limit and thermal envelope with a traceable L1, Ceff and protected cell from B #7; reconcile with #8 and C review. If those data remain absent, mark BLOCKED rather than inventing part ratings.

## Verdict and safety
**CONDITIONAL** algebraic necessity only. **BLOCKED** actual low-cell continuous 205V/16mA, USB-assist startup and thermal operation. **PENDING REVIEW**; Work/Chat C must challenge this result before shared-index adoption. No purchasing, PCB manufacture, HV energization, main merge or requirements change. No shared ledgers edited because Work is integrator and concurrent writes are possible.

Reproduce with Python 3: `P=6.60084; I=3.13*(1-.18); [(v,(v-P/I)/I,(v-P/I)/I-.14) for v in (3,3.3,3.6,4)]`.
