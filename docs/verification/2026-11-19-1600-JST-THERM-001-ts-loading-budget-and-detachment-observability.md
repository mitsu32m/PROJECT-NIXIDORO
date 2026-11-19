# THERM-001 / Issue #9 — TS shared-sensor loading budget and detachment observability
Date: 2026-11-19 16:00 JST (scheduled design analysis). Role: Chat A. Branch: `codex/reva-integrated-prototype-review`.
Starting branch HEAD: UNKNOWN (file API returns blob SHA, not branch commit; do not substitute). Claim: PROVISIONAL / NO FORMAL CLAIM. Review: PENDING REVIEW.
Scoped verdict: CONDITIONAL (mathematical loading bound); BLOCKED (actual temperature-safety implementation).

## Task contract and prior art
Question: Can an added resistive temperature-monitor input be called nonintrusive, and can electrical NTC validity checks detect sensor detachment? Exit: reproducible analytical upper bounds and explicit counterexample, without component adoption.
Read: ai-workflow, handoff, open-issues, decisions, tech-tree.yaml/md, WORK-INT-003, A 2026-11-19-1200 THERM-001, Issue #9 and other open issue summaries. Prior A report already showed 100k loading gives 15.2% at 10C. This report instead derives an arbitrary error-budget inequality and an impossibility limitation for detachment detection. No shared-index edit; Work owns integration.

## Manufacturer/assumption classification
TI BQ25185 Rev.B (Aug 2026): https://www.ti.com/lit/ds/symlink/bq25185.pdf . TS measurement is inactive in battery-only mode (§6.4 p19); /CE is charge inhibition, not load isolation. TE nominal GA10K3435STM010 R10=17.95kohm, R45=4.92kohm as transcribed and source-checked in WORK-INT-003; these are TYPICAL nominal, not installed or worst-case limits. Constant TS current 38uA is ASSUMED nominal model, not a guaranteed bias over operating conditions.

## New analytic bound
For NTC resistance R and any purely resistive shunt RL to ground, Rmeas=R*RL/(R+RL). Fractional resistance/TS-voltage reduction e=1-Rmeas/R=R/(R+RL). Thus to keep loading error at or below epsilon, RL >= R*(1-epsilon)/epsilon.
- At 10C, R=17.95kohm: epsilon=1% requires RL>=1.77705Mohm; epsilon=0.1% requires RL>=17.93205Mohm.
- At 45C, R=4.92kohm: epsilon=1% requires RL>=487.08kohm; epsilon=0.1% requires RL>=4.91508Mohm.
- An assumed 1Mohm shunt gives e=1.76335% at 10C and 0.48959% at 45C. This is **not** a claim about any real ADC input; ADC sampling charge, leakage, ESD paths, MCU unpowered states and TS/MR reset semantics need separate analysis.
- Ideal B3435 local temperature-equivalent loading error magnitude approximately e*Tkelvin^2/B: at 10C, 1% maps to ~0.233C; at 45C ~0.295C. This first-order approximation is illustrative only; real R/T tolerance, self-heating, placement and dynamics dominate the safety budget.
- The above is a *necessary loading bound* for a simple static parallel resistor, not a sufficient accuracy or safety qualification. Input leakage can flow either direction and nonlinear clamp effects invalidate the simple shunt model.

## New impossibility/counterexample: electrically valid detached NTC
Consider two physical states: S1 sensor electrically intact and bonded to a cell at 25C; S2 the same intact sensor detached from a hotter cell but still at ambient 25C. With identical NTC temperature and wiring, every measurement using only its electrical resistance produces identical outputs in S1 and S2. Therefore no open/short window or ADC diagnostic based only on that one resistance can reliably distinguish attachment in all cases. Mechanical attachment qualification, independent pack-coupled sensing, conservative limits, or another independent physical observable is required for a defensible safety case. Two electrical readers of the same detached NTC do not solve this common-cause failure.

## Mode and power implications
Do not attach a low-impedance divider or unpowered MCU pin to BQ TS/MR by assumption. An isolated buffer is only a candidate if input leakage over all power states and failure injection are bounded by a full error budget; it also does not resolve battery-only monitoring when BQ TS is inactive. Separate charge inhibit (/CE), discharge/load cut and HV hard-stop/discharge remain required, including startup and brownout defaults. No schematic edit or proposed threshold approval.

## Verification / next evidence
Independent algebra check: e(17.95k,1M)=17950/1017950=0.01763348; RL_min(1%)=99*17950=1,777,050 ohm. A subsequent reviewer should independently verify the first-order temperature formula and distinguish NTC loading from actual TS trip uncertainty. Next actionable task: manufacturer-guaranteed monitor input bias/leakage (powered/unpowered), comparator brownout/output defaults, qualified pack sensor mounting and exact charge inhibit/load cut interfaces; then full corners and faults. Chat C independent review and Work integration required.
No purchases, PCB production, HV application, main merge, or specification change.