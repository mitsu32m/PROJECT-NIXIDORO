# C-REVIEW-021 — HV-001 / PROTO-001 independent primary-current and sourcing batch
Date: 2026-11-23 03:00 JST (review window)
Role: Chat C, independent first-pass; NO FORMAL CLAIM. NOT hardware safety approval.
Branch: `codex/reva-integrated-prototype-review`
Starting HEAD: `dea74e97cb5ba274409f6fca104259f25d503d18`
Input reports: A `2026-11-22-2356-JST-HV-001-adi-primary-current-rating-and-copper-loss-correction.md`; B `2026-11-23-0100-JST-chatb-hv001-lt3757-coilcraft-flyback-pair-screen.md`.
Issue scope: #2 HV-001 actual topology, #7 PROTO-001 magnetic sourcing. Exit: classify source wording, correct transformer ratio, independently recompute conditional losses/duty, define sourcing gate. No component selection, procurement, PCB, HV operation or spec changes.

## Independent source checks (2026-11-23)
1. ADI article, 2002-07-04, https://www.analog.com/en/resources/technical-articles/small-highvoltage-boost-converters-guide.html , Experimental Comparison: Sumida CMD-8LN 6313-T036 lists Lp=5.6uH, Ip=2.3A, Np:Ns=1:9, Rp=0.5ohm. Article **does not identify Ip as measured switching turn-off peak or guaranteed current limit**. Figure 11 is a switching waveform, but its actual image data/axes were not independently digitized. Article explicitly gives 150V/25.5mA at 77% and 330V/9.6mA at 60%, with different rectifier/output capacitors; not a 205V/16mA guarantee.
2. Coilcraft Q4434-BL manufacturer product specifications https://www.coilcraft.com/ja-jp/products/transformers/power-transformers/power-converter-transformers/q4434/ : **primary:secondary turns ratio 1:1**, 22uH nominal (0A), 19.8uH min at 5A, DCR max 0.028/0.028ohm at 25C, leakage max 2uH, 500Vrms winding-to-winding isolation. Manufacturer typical application 4–6V to 5V/1.6A, 100kHz with LM258X. This is not a high-voltage step-up winding. The 500Vrms isolation test is not proof of a 205V secondary design or safe working voltage.
3. Coilcraft Q4435-BL manufacturer product specifications https://www.coilcraft.com/en-us/products/transformers/power-transformers/power-converter-transformers/q4435/ : **1:1**, 22uH nominal (0A), 19uH min at 4.85A, primary DCR max 0.020ohm, secondary DCR max 0.025ohm, leakage max 0.7uH, 500Vrms winding isolation; 4–6V to 5V/1.6A at 100kHz LM258X example. Same voltage mismatch. These source-page numbers were directly read, but not crosschecked against controlled revisioned PDF drawings; stock and landed cost not independently established.
4. ADI LT3757/LT3757A product page https://www.analog.com/en/products/lt3757.html : Rev.H listed, VIN 2.9–40V, external MOSFET, flyback support, and **50kHz–1MHz** frequency range. Chat B's 100kHz–1MHz statement requires correction; 100kHz is not the manufacturer's stated lower programmable frequency bound on this page. 2.9V minimum IC operating supply is not 3.0V battery-system guaranteed startup.

## Independent calculations and adversarial counterexamples
- 205V * 0.016A = 3.280W. At illustrative efficiency 0.75 and 5V input: input 4.37333W, Iin=0.874667A; 0.80 => 4.10W, Iin=0.820A. USB 5V*0.5A=2.5W before losses, so USB-only continuous 3.28W impossible.
- Ideal isolated flyback CCM volt-second relation (neglect diode): Vout = n Vin D/(1-D), n=Ns/Np. For 205V/5V, n=1 requires D=205/210=0.976190; n=10 requires D=205/255=0.803922. At 3V n=1 requires D=205/208=0.985577; n=10 D=205/235=0.872340. These are necessary ideal CCM relations, not DCM or hybrid-autotransformer operating points. No manufacturer max duty/min-off or 205V winding proof was established. In particular, **a 1:1 5V-output transformer cannot be reclassified as a 1:10 205V design simply because the controller supports flyback**.
- Chat A triangular-pulse model: Irms²=Ipk² D/3 and Pcu=Rp Ipk² D/3. At Rp=0.5ohm, D=0.75 and assumed Ipk=1.5/2.3/3.2A, Pcu=0.28125/0.66125/1.280W. At 60K hotter and assumed copper alpha 0.00393/K, R=0.6179ohm; at 2.3A Pcu=0.81717W. At illustrative 77% efficiency, 3.28*(1/.77-1)=0.97974W total loss, and 0.66125/0.97974=67.49%. **Caution:** the triangular primary waveform is not established for the ADI hybrid circuit, and the Rp current path may conduct during OFF; thus even this copper-loss number is not a valid upper bound. Ip=2.3A must remain SOURCE-LISTED/UNDEFINED, not measured peak.
- Q4434 leakage 2uH and Q4435 0.7uH are product-table maxima at stated test conditions, not the ADI 1:9 Sumida leakage. Do not transplant them into the prior 250kHz/2.3A clamp-loss example. No actual Q4434/35 high-voltage converter waveform, rectifier stress, capacitor Cmin/Cmax, OVP, startup, winding temperature or isolation working-voltage qualification.

## Claim-by-claim disposition
- A: ADI Ip=2.3A provenance correction — **ACCEPTED**: no explicit measured peak definition in primary article.
- A: 0.5ohm copper loss arithmetic — **ACCEPTED (assumed triangular pulse only)**; real hybrid waveform/thermal inference **CONDITIONAL** and adoption **BLOCKED**.
- A: 77% precedent transferred to 205V — **REJECTED as a verified operating efficiency**; remains hypothetical sensitivity.
- B: LT3757 flyback controller plausible — **CONDITIONAL** (input/topology supported; actual stage unqualified).
- B: LT3757 frequency lower bound 100kHz — **CHANGES_REQUESTED**: ADI product page states 50kHz.
- B: Q4434/Q4435 as qualified 205V magnetics — **REJECTED**: both manufacturer pages explicitly state 1:1 and 5V output reference use.
- B: both parts as sourcing research examples, not qualified pairs — **ACCEPTED**; independent PDF drawing/revision and inventory still pending.
- Actual 205V/16mA transformer/controller pair, startup, thermal, OVP, fault discharge — **BLOCKED**.

## Work decision package — handoff to Work integrator
**Decision requested:** Keep LT3757 as controller-only research candidate; explicitly exclude stock Q4434-BL/Q4435-BL from any 205V-qualified first-order BOM or 'two viable pairs' count. Keep ADI MAX668 1:9 precedent as historical topology reference, not a measured 2.3A peak/current-rating guarantee. Do not approve hardware or change requirements.
**A/B positions:** A corrects Ip provenance and offers conditional copper loss; B proposes LT3757 and screens Q4434/Q4435/TA7608 as sourcing false positives.
**Independently verified:** ADI article wording and test points; Coilcraft Q4434/Q4435 1:1 primary:secondary specs; LT3757 product page 50kHz lower bound; numerical examples above.
**Unknown:** controlled PDF winding dot/pin and working-voltage specs, actual current waveforms, MOSFET/diode/transformer loss and thermal at 205V, low-cell duty and start, OVP tail energy, procurement stock and landed JPY. TA7608 details not independently rechecked in this batch.
**Alternatives:** manufacturer-controlled 205V-capable winding/controller pair with actual ratio/dots and rated working voltage; custom winding only after feasibility, sourcing, thermal and cost evidence; compare MAX668 hybrid and LT8365 charge pump without adoption.
**System impacts:** HV topology, MOSFET/rectifier/clamp voltage, thermal and PWR current, independent OVP, staged BOM/lead time. Preserve 205V/16mA target.
**Sources:** URLs above; original A/B reports in this branch at starting HEAD `dea74e97cb5ba274409f6fca104259f25d503d18`. Handoff: Work integration owner; no shared-index changes by Chat C.

## Queue and prohibitions
New A/B since C-020: 2; reviewed 2; new-window unreviewed 0; historical backlog NOT fully audited. Oldest new report 2026-11-22 23:56 JST. #2 and #7 remain open/PENDING as hardware tasks. Next priorities: #6 guaranteed OVP tail-energy/Cmin/bleeder and hard-off; #9/#8 cell temperature inhibit and low-cell PWR heat; #7 controlled high-voltage winding sourcing. Existing HV KiCad RevA draft explicitly labels transformer unverified and still uses MAX668, not LT3757; only text inspected, not netlist/ERC validated. No formal claim; no shared-index edits; no purchasing, HV tests, PCB fabrication, main merge, safety approval or automation changes.
