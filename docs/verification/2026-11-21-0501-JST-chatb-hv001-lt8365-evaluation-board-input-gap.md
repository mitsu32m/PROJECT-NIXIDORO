# Chat B — HV-001 / SYS-001 LT8365 evaluation-board input-gap screen
Date: 2026-11-21 05:01 JST
Status: **PENDING REVIEW** (Chat C); **BLOCKED** for circuit/parts adoption
Role: Chat B provisional research — **NO FORMAL CLAIM**
Starting branch HEAD: `2fea94d5108795181e04c598c660b1d86f88dc44`
Issues: #7 PROTO-001 (wide research), #4 SYS-001A; #2 HV topology remains Chat A deep design.

## Bounded question and result
Can the LT8365 manufacturer demonstration circuits be treated as a proven, readily adapted 5V/SYS -> 205V at 16mA solution? **No.** ADI documents positive-output DC2838A and negative-output DC2840A at **9–30V input, 250V at 10mA**, **400kHz**, whereas NIXIDORO needs ~5V stage (or lower SYS) and 205V/16mA continuous. The IC itself supports **2.8–60V input** but that does NOT qualify the demonstration circuit at 5V or battery-only low SYS.

## Primary manufacturer sources (retrieved 2026-11-21)
1. ADI LT8365 product page (Rev.A datasheet linked): input 2.8–60V, **integrated 150V/1.5A switch**, 100–500kHz, recommended for new designs. https://www.analog.com/en/products/lt8365.html
2. ADI DC2838A evaluation-board page and controlled schematic/manual links: **9–30V -> +250V/10mA at 400kHz**, boost/charge-pump topology. https://www.analog.com/en/resources/evaluation-hardware-and-software/evaluation-boards-kits/dc2838a.html
3. ADI DC2840A evaluation-board page: **9–30V -> -250V/10mA at 400kHz**, inverting output (NOT equivalent to +205V relative to NIXIDORO ground). https://www.analog.com/en/resources/evaluation-hardware-and-software/evaluation-boards-kits/dc2840a.html
4. ADI LT8365 Rev.A datasheet: https://www.analog.com/media/en/technical-documentation/data-sheets/LT8365.pdf
The ADI examples use an integrated **150V-rated switch** in multi-stage configurations. A 205V output must not be interpreted as an allowable direct 205V stress on SW. No topology/diode/charge-pump or OVP equivalence established.

## Reproducible power and thermal screening
- Required target: `Pout=205*0.016=3.280 W`. DC2838A example `250*0.010=2.500 W`. Ratio `3.28/2.50=1.312` (31.2% higher output power), and required current `16/10=1.60` times. This is NOT a 3.28W manufacturer demonstration.
- At hypothetical HV efficiency 75%/80% and 5V input: `Iin=Pout/(5*eta)=0.8747/0.8200 A`, **before** 5V stage loss and auxiliary load. For hypothetical 3.0V direct-SYS operation: `Iin=1.4578/1.3667 A`, before protection/contact losses. These are average estimates, not switch peak current ratings.
- For USB 5V/500mA, ideal `Pin,max=2.50W < 3.28W`: full target USB-only impossible. Battery supplement can produce negative net charge; no simultaneous charge guarantee.
- Losses at assumed 75%/80% HV efficiency: `Ploss=Pout*(1/eta-1)=1.093/0.820 W`, respectively. **Assumed**; not a verified LT8365 loss or junction-temperature estimate. `Tj=Ta+Pdevice*thetaJA` cannot be calculated without partitioning IC/inductor/diode/capacitor loss, real PCB thermal resistance and PETG enclosure ambient.
- The 150V integrated switch rating, internal switch peak current, 5V input startup, charge-pump component stress, 205V regulation and output capacitor Cmin/Cmax/OVP remain to be derived from an exact candidate schematic. Manufacturer demonstration at 9V minimum does not imply low-cell operation.

## Comparative gate (no BOM adoption)
| Candidate | Evidence | Specific gap | Status |
|---|---|---|---|
| LT8365 + DC2838A topology | ADI controlled +250V/10mA at 9–30V | 5V/low SYS, +205V/16mA, 150V SW stress, component temperatures and OVP | NOT QUALIFIED |
| LT8365 + DC2840A | ADI -250V/10mA at 9–30V | Wrong output polarity relative to system ground, 5V/16mA | NOT QUALIFIED |
| LT3757 + DCT15EFD-U44S003 | ADI 5–12V +350V/10mA flyback | TDK original listed obsolete; 205V/16mA and OVP not proven | SOURCING BLOCKED |
| MAX668 coupled inductor | Original candidate, Chat A #2 | Exact winding/polarity, Isat/leakage, thermals | RESEARCH ONLY |

The current-production status of LT8365 is **not** proof of availability of a suitable complete magnetics/charge-pump/diode set. Dated Japanese stock, unit price, tax, shipping, lead time and a qualified controller+magnetics pair remain **UNKNOWN**. The DC2838A circuit is not itself a proven flyback transformer pair; do not count it as such.

## Fault/temperature requirements for next candidate
Evaluate output open/load removal, short, input sag, battery cutoff, MCU reset, charge-pump capacitor and diode stress, power-down discharge, independent OVP hard-off, and worst effective HV Cmin/Cmax with 220V HV5524 recommended ceiling. Quantify low-VIN peak switch/inductor current, winding/inductor saturation, switch/diode dissipation and PCB/enclosure junction temperatures with manufacturer limits. No assumption of firmware-only safety.

## Review handoff and workflow proposal
Chat C: independently verify that ADI DC2838A/DC2840A specified 9–30V, 250V/10mA, 400kHz and the 150V switch topology do not qualify 5V/205V/16mA. Verify whether the positive-output circuit has a practical adaptation path and enumerate required components and worst-case stresses. Work: do not promote LT8365 to adopted HV architecture. Suggested SOP amendment (do not edit shared SOP): **Every manufacturer's high-voltage reference must explicitly list demonstrated VIN range, polarity, output watts/current, switch-node rating and whether its magnetics are required; a controller input rating alone must never substitute for reference-circuit operating range.**

No parts purchases, PCB fabrication, HV application, main merge, shared-index edits, requirements change or task schedule change.
