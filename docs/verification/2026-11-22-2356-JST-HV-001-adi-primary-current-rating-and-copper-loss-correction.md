# HV-001 / Issue #2 — ADI 1:9 magnetics current provenance and copper-loss gate
Date: 2026-11-22 23:56 JST
Role: Chat A / deep-design
Review: **PENDING REVIEW**; **NO FORMAL CLAIM**
Result: **CONDITIONAL** analytical screening; actual 205 V / 16 mA hardware **BLOCKED**

## Task contract
Question: Does the primary manufacturer article actually identify 2.3 A as a measured peak current, and what can its 0.5-ohm primary winding resistance establish about efficiency/thermal design?
Exit: independently check the exact primary-source wording; quantify a conditional copper-loss model and identify measurements needed. Excludes schematic changes, component adoption and HV tests.
Branch: `codex/reva-integrated-prototype-review`. Starting HEAD **UNKNOWN**: the available connected GitHub tools read branch files but did not expose an exact branch commit SHA. No atomic Claim confirmed. Required SOP/handoff/open-issues/decisions/YAML and Markdown tech trees, preceding Chat A 20:01 report and Issue #2 read. Full report directory and concurrent B/C coverage not exhaustively established; this unique file avoids shared-index conflicts.

## Manufacturer evidence and important correction
Primary source: Analog Devices, *Small, High-Voltage Boost Converters*, published **2002-07-04**, https://www.analog.com/en/resources/technical-articles/small-highvoltage-boost-converters-guide.html , sections *Experimental Comparison* and *Efficiency Considerations* (Figure 9/11/12).
The article states Sumida CMD-8LN 6313-T036: **Lp=5.6 uH, Ip=2.3 A, Np:Ns=1:9, Rp=0.5 ohm**. It does **not explicitly call Ip=2.3 A a measured turn-off peak** in that component list. It may represent a part current rating. Thus previous reports using 2.3 A as a precedent **measured peak** overstate provenance. Reclassify 2.3 A as **SOURCE-LISTED Ip, DEFINITION UNKNOWN**, not guaranteed NIXIDORO peak or measured waveform. The article reports 150 V x 25.5 mA = 3.825 W at 77% efficiency, and separately 330 V x 9.6 mA = 3.168 W at 60% using a 400 V CMR1U-04 diode and changed capacitors. Neither is a 205 V / 16 mA demonstration. ADI notes primary resistance and leakage as important losses and says the transformer winding limits practical high-voltage operation.

## Independent conditional calculations
Assume for **illustration only** triangular primary current from zero to Ipk during ON fraction D, zero otherwise, one pulse per cycle. Then I_rms^2 = Ipk^2 D/3, and primary copper loss Pcu = Rp Ipk^2 D/3. This waveform is **ASSUMED**, not confirmed for the hybrid autotransformer; actual secondary/primary current routing and possible nonzero currents require source schematic and measured waveforms.
With Rp=0.5 ohm (ADI component listing, temperature unspecified), D=0.75 (ASSUMED):
- Ipk=1.5 A (ASSUMED): I_rms=0.750 A, Pcu=0.281 W.
- Ipk=2.3 A (ASSUMED, not measured): I_rms=1.150 A, Pcu=0.661 W.
- Ipk=3.2 A (ASSUMED): I_rms=1.600 A, Pcu=1.280 W.
At fixed Ipk=2.3 A, D=0.5 gives Pcu=0.441 W; D=0.8 gives Pcu=0.705 W. These are *primary winding only*, before MOSFET, diode, secondary winding, leakage, core and switching losses.
At 205 V x 16 mA = 3.28 W, if efficiency were 77% (ASSUMED transfer of 150V precedent), total converter loss would be 3.28(1/0.77-1)=0.980 W. The illustrative 0.661 W copper estimate would consume 67.5% of that hypothetical loss budget. **Do not add the preceding leakage-energy scenario as guaranteed extra heat**, and do not assert 77% efficiency at 205 V.
Copper resistance rises with temperature: assuming copper alpha=0.00393/K and a 60 K winding temperature increase, Rp would become ~0.618 ohm and illustrative 2.3A, D=0.75 loss ~0.817 W. Rp temperature coefficient and winding rise are **ASSUMED**, not a qualified transformer thermal rating.

## Implications / challenge to earlier Chat A
The 20:01 leakage report correctly labelled leakage inductance and f as assumptions but called 2.3 A a 'reported peak'. Correct the interpretation: ADI reports Ip=2.3 A in a transformer component list, with no explicit measurement definition. The leakage scaling remains mathematically valid for any *assumed* actual turn-off current; its numeric table is not a measured or bounded converter loss.
More valuable than another voltage-only screen is to obtain a qualified magnetic component with Lp, DC resistance vs temperature, saturation current definition, primary-referred leakage test condition, turns/dot/pin diagram, and core loss at actual waveform. Then calculate actual primary and secondary RMS currents and thermal rise at low input / 205 V / 16 mA / startup and load removal.

## Decision and handoff
**CONDITIONAL:** ADI gives an actual 0.5-ohm primary winding resistance and 150V/3.825W plus 330V/3.168W test points; conditional triangular copper-loss math reproducible.
**NO-GO (limited):** describing ADI's Ip=2.3A as a measured turn-off peak or using 77% at 205V as established.
**BLOCKED:** qualified transformer and waveform, maximum current, 205V/16mA continuous, MOSFET/diode stress and loss, thermal, startup, independent OVP and safe discharge.
**PENDING REVIEW:** Chat C to check source wording, hybrid current waveform, copper temperature assumptions and comparison against recent B/C research. Work may integrate after review. No issue closure or approved part.
No purchase, fabrication, HV energization, main merge or specification change.
