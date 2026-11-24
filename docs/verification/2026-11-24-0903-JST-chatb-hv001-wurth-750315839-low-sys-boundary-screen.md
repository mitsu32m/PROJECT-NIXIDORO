# Chat B — HV-001 / SYS-001: Würth 750315839 low-SYS boundary-mode screening
Date: 2026-11-24 09:03 JST
Role: Chat B wide research. **PENDING REVIEW / NO FORMAL CLAIM / NOT ORDER-READY**
Start HEAD: `2a73c10ac9dea34d836bbf5d1d7b7f882882990b`
Issues: #2 (HV-001), #7 (PROTO-001), #4 (SYS-001).

## Bounded task and provenance
Question: Does an already documented, sourceable 1:10 transformer provide a more credible low-SYS alternative than CJ5143 in the ideal fully-reset boundary-mode model? Exit: reproducible voltage/current/frequency/efficiency bounds, source limitations and procurement holds. No physical design approval.
Repository evidence: `docs/hv-transformer-screen.md` (2026-11-15); `docs/verification/2026-11-24-0900-JST-C-REVIEW-026-ovp-bias-cj5143-reset-batch.md`; `docs/verification/handoff.md`; six required governance documents and GitHub Issues checked.
Manufacturer primary datasheet: Würth 750315839 https://www.we-online.com/components/products/datasheet/750315839.pdf (manufacturer-published, as transcribed in repository transformer screen; live revision and current distributor stock NOT independently reconfirmed in this run). Manufacturer application: 4–36V, 50–200kHz, 200V/12mA typical design, NOT 205V/16mA continuous guarantee.
Manufacturer parameters carried from repo: Lp=40uH ±10%; Ns/Np=10; Isat=3.2A **TYPICAL at 20% L drop**, not a guaranteed continuous 3.2A limit; DCR primary 85mOhm ±10%@20C; leakage <=0.5uH. These are not complete high-temperature L(I) and core-loss curves.

## Reproducible ideal boundary-mode model
ASSUMED ideal triangular primary current rising from zero to Ipk and complete secondary reset each cycle, constant Lp=40uH, Vout=205V, n=10, no dead time, winding drop or parasitic energy. For Ipk=3.2A (TYPICAL characterization point, not guaranteed):
ton=Lp*Ipk/Vin; toff=Lp*Ipk*n/Vout;
f_boundary=1/(ton+toff);
Pmag=0.5*Lp*Ipk^2*f_boundary = 0.5*Ipk*Vin*(Vout/n)/(Vin+Vout/n).
Pout=eta*Pmag; eta_needed=3.28W/Pmag.

| Vin (at primary) | ton | toff | f boundary | Pmag ideal | eta needed for 3.28W | Pout at assumed 75% |
|---|---:|---:|---:|---:|---:|---:|
| 3.0V | 42.667us | 6.244us | 20.445kHz | 4.187W | 78.33% | 3.140W |
| 3.6V | 35.556us | 6.244us | 23.924kHz | 4.900W | 66.94% | 3.675W |
| 5.0V | 25.600us | 6.244us | 31.403kHz | 6.431W | 51.00% | 4.824W |

**Interpretation:** At 3V and 75% assumed efficiency, this ideal 3.2A boundary-mode scenario is insufficient for 205V×16mA. At 3.6V and 5V it passes only the ideal energy-power screen. All calculated frequencies are **below the manufacturer's cited 50–200kHz typical application window**, so none constitutes a validated manufacturer operating point. The 3.2A characterization includes a 20% inductance drop; constant-40uH timing is not a verified actual waveform, and the current is typical rather than guaranteed. Actual low-SYS minimum at primary remains UNKNOWN.

Important nuance: the 3V result is NOT a proof that every circuit using 750315839 fails; a different current waveform, switching frequency, higher current, CCM, or another efficiency may change the outcome, subject to magnetic saturation and heat. Likewise 5V pass does NOT qualify the pair. In contrast, the prior CJ5143 3V/100kHz ideal DCM bound was 2.017W magnetic; models and switching constraints differ, so this is a *comparison of hypothetical screens*, not a performance ranking.

## Power-path and mode contract
At 205V×16mA, P_HV=3.28W. USB 5V×500mA=2.50W gross, so USB-only continuous full-target output is impossible even at 100% efficiency. BQ25185 programmed 500mA input limit and its minimum threshold are NOT guaranteed SYS delivery. USB+BAT supplement may have positive signed battery discharge; battery-only must qualify worst low-SYS and BATFET/cell/PCM thermal. Neither 16mA whole-bus vs lamp-only nor bleeder topology is approved. Keep separate digit, neon, bleeder, OVP divider, driver leakage and auxiliary power ledger; do not double-count ballast heat already inside bus power.

## Thermal, fault, sourcing
Theoretical primary RMS at boundary is Ipk*sqrt(D/3), but winding copper loss must use actual hot DCR and measured/qualified current waveform; 85mOhm at 20C is not high-temperature DCR. Secondary RMS, core loss, leakage clamp, rectifier, MOSFET, switching and control loss remain UNKNOWN. 205V no-load, sudden load loss, output short, feedback open, OVP hard-off, startup and residual discharge are unqualified. HV5524 recommended 220V is not a trip target. 1500VAC winding insulation test does not prove system creepage/working-voltage safety.

Historical DigiKey Japan stock 510 and 478 JPY before tax (2026-11-15) is NOT current stock, landed price or order approval. Current quote/lead time/tax/shipping/footprint still UNKNOWN. No qualified controller+transformer pair.

## Candidate comparison and decision
- 750315839: concrete 1:10 part, manufacturer 200V/12mA reference; 3V/75%/3.2A ideal boundary mode fails 16mA; 3.6–5V hypothetical pass but frequency outside cited application and typical current cannot guarantee it. **BLOCKED**.
- CJ5143-ALC: compact capacitor charger, 3V/100kHz fully-reset DCM upper bound insufficient; 5V nearly boundary and 1.2A characterization not continuous rating. **BLOCKED**.
- MAX668 coupled, LT3757A external-MOSFET flyback, LT8304-1 with T086, LT8365 multiplier: retain as research alternatives; none is an order-ready full 3.28W/low-SYS pair. No universal topology rejection.

## Chat C review and Work handoff
Please independently verify equations and rounding; check whether 50–200kHz is application-only, whether Isat 3.2A at 20% drop may be used as a conservative bound (probably not), and reconcile actual L(I,T), control IC mode, switching-frequency capability, core thermal, current limit and present Japan landed quote. Prioritize a **manufacturer-validated 3–5V continuous 205V/16mA pair** or explicitly document its absence. Work to update shared indices after review.

SOP proposal for integrator (do not edit `docs/ai-workflow.md` as worker): every candidate screening must tag manufacturer example operating frequency separately from absolute limits, typical Isat separately from guaranteed saturation, and demonstrate frequency/time/current/temperature together before saying 'feasible'.

**Status: PENDING REVIEW; hardware decision BLOCKED.** No shared index, requirements, KiCad, schedule, purchase, PCB, HV energization, or main merge changes.
