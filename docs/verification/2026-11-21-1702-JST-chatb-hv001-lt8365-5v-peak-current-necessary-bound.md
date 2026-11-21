# Chat B — HV-001 / SYS-001: LT8365 5V input peak-current necessary-condition screen
Date: 2026-11-21 17:02 JST
Status: **PENDING REVIEW**; provisional research, **NO FORMAL CLAIM**.
Branch: `codex/reva-integrated-prototype-review`
Starting branch HEAD: **UNKNOWN** (GitHub connector exposes branch search names and file blob SHAs, but no verified commit SHA in this run; do not substitute a blob SHA).
Related issues: #10, #7, #4. Scope: current feasibility *necessary* bound, not actual stage qualification.

## Primary evidence
- ADI LT8365 product/datasheet entry: https://www.analog.com/en/products/lt8365.html — 150V, 1.5A internal switch headline; input range of IC is not demonstration-board rating.
- ADI DC2838A evaluation board: https://www.analog.com/en/resources/evaluation-hardware-and-software/evaluation-boards-kits/dc2838a.html — 9–30V input, 250V/10mA, 400kHz, charge-pump stage(s); not qualified for 5V.
- ADI demo manual Rev.0 (2020-03-02): https://www.analog.com/media/en/technical-documentation/user-guides/dc2838a.pdf . Exact SW current limit min/max over temperature, stage waveform and startup behavior **UNKNOWN** pending controlled datasheet electrical table and circuit simulation.

## Reproducible necessary-condition screen
Target **ASSUMED requirement**, unchanged: 205V * 0.016A = 3.28W. For HV-stage efficiency eta (ASSUMED), 5V input average current is 3.28/(5 eta): 0.820A @80%; 0.875A @75%; 0.937A @70%. This is *not* USB 500mA feasibility: USB 2.5W max ideal < 3.28W and battery supplementation or reduced load is required.

For a **hypothetical** 10uH inductor at 400kHz, during ON with 5V across L, ripple ΔI = Vin*D/(L*f)=1.25D A. For CCM triangular current with no parallel input path, peak = Iin + ΔI/2, so at D=0.8: 1.320A @80%, 1.375A @75%, 1.437A @70%; at D=0.95: 1.414A @80%, 1.469A @75%, 1.531A @70%. These are idealized sensitivity results, **NOT** validated DC2838A peaks: charge-pump diode currents, input filter, actual duty, minimum input voltage, L tolerance, DCM, switching ripple and switch/inductor waveforms can alter stress. 1.5A is a product headline, not established guaranteed minimum peak current limit. A nominal result below 1.5A is not GO.

At 4.5V and eta=75%, Iin=3.28/(4.5*0.75)=0.972A; with D=0.95 and same L/f, ΔI=1.069A, peak≈1.506A. This demonstrates narrow nominal headroom even before startup/transient, not a proven current-limit violation.

For a 5V **intermediate rail** from a cell/SYS, total battery demand exceeds the HV input power by the inverse 5V-stage efficiency. For eta5=0.9 and etaHV=0.75, P_SYS≈4.86W excluding control and charger loss. USB 5V/500mA cannot sustain full 3.28W display even with ideal stages; USB+BAT may be net discharging, not charging.

## Corrective observation
Do **not** use an assumed 102.5V intermediate node as if it were measured to infer duty/peak; previous Chat B 13:04 report used a hypothetical stage. The actual DC2838A NET1/NET2/NET3 connectivity, waveform and switch stress need a schematic/netlist-based derivation. Do not treat manufacturer demonstration at 9–30V as 5V startup proof.

## Decision and risks
**BLOCKED** for LT8365/DC2838A 5V→205V/16mA adoption. Need guaranteed minimum current limit over conditions, actual stage current/voltage waveforms, diode/flying-cap RMS and surge, L Isat and copper/core losses, 5V startup and lower SYS, worst-case fault/open load/OVP/hard-off, sealed PETG thermal estimate, and one-piece domestic stock/price for each exact MPN. Existing 150V SW means a plain single-inductor direct 205V boost is NO-GO; charge-pump alternative remains research-only. LT3757 flyback with obsolete TDK magnetics and MAX668 coupled-inductor remain comparative candidates, not proven assemblies.

## Chat C independent review request
1. Check input-current and triangular-ripple arithmetic and assumptions; distinguish switch current from input current for the real charge-pump topology.
2. Extract datasheet **guaranteed** current-limit minimum and evaluate 4.5V and startup, with stage-node schematic and stress.
3. Check ADI demo-manual revision, actual inductor MPN and rated/temperature parameters before any BOM adoption.
4. Reject any claim that USB-only 500mA or 5V startup is established.

## Suggested SOP improvement (proposal only; do not edit shared SOP)
Require a source-specific **necessary versus sufficient** classification for every HV feasibility screen and explicit distinction between product headline current, guaranteed limit, and measured peak. Integrator to consider adding to docs/ai-workflow.md.

No purchasing, PCB release, HV application, main merge, or requirement change authorized.