# Chat B — SYS-001 / HV-001: LT8365 5V current-limit qualification gate
Date: 2026-11-21 21:00 JST
Status: **PENDING REVIEW**; provisional research, **NO FORMAL CLAIM**.
Branch: `codex/reva-integrated-prototype-review`.
Starting HEAD SHA: **UNKNOWN** — branch name and files were read through connected GitHub, but branch-head SHA was not exposed by the available branch-search endpoint. Do not confuse file blob SHA or repository-wide commit search with branch HEAD.
Related: #10 HV-001, #7 PROTO-001, SYS-001. Scope: analytical necessary conditions only; no circuit adoption.

## Source state
Read the six mandatory files: docs/ai-workflow.md, docs/verification/handoff.md, docs/verification/open-issues.md, docs/verification/decisions.md, docs/tech-tree.yaml, docs/tech-tree.md. Reviewed #10 and #7 and prior 2026-11-21 17:02 Chat B calculation (reported in preceding run). The repo-wide commit search returned old commits, so it **cannot** certify latest branch logs or HEAD. No formal Issue claim is asserted.

## Quantitative gate: necessary, not sufficient
Unchanged 205 V × 16 mA = **3.280 W** continuous target. For assumed HV-stage efficiency η, input voltage Vin, inductance L=10µH and switching f=400kHz, a single-inductor continuous-conduction *proxy* gives:

- Iin,avg = 3.28/(η Vin)
- ΔIL = Vin D/(L f)
- IL,peak = Iin,avg + ΔIL/2.

At Vin=5V and **assumed** D=0.95, ΔIL=1.1875A. For η=0.80/0.75/0.70, Iavg=0.820/0.875/0.937A and Ipeak=1.414/1.469/1.531A. At Vin=4.5V, η=.75 and D=.95, Iavg=.9719A, ΔIL=1.06875A, peak=1.5063A.

**Important model limitation:** In DC2838A's charge-pump topology, D is determined by its intermediate voltage, diode/flying-cap conduction and control regime. D=.95 is a stress *scenario*, not a validated operating duty; switching current may not equal total input current. Therefore these values are neither guaranteed device stresses nor a proof of failure. A 1.5A advertised switch rating is not a guaranteed minimum cycle-by-cycle current limit. Compare **datasheet guaranteed minimum limit over temperature** against true peak plus startup/fault margins before claiming feasibility.

## USB and battery-assist modes
USB 5V × 0.5A = 2.5W **ideal input ceiling**. Full 3.28W HV output cannot be sustained from USB alone at any physical efficiency <=100%, even with control loads excluded. Battery-assisted USB operation must budget signed battery current, input-limit tolerance, charger/system power path, battery temperature and whether charging is actually possible; it is not a positive-charge state by default. For ηHV=.75, 5V HV-stage input is 4.373W; the *ideal* deficit against 2.5W USB is >=1.873W before upstream loss/control/charger dissipation. Battery-only mode must also meet SYS minimum and protection/thermal limits. Reduced-current lamp scenarios are research only, not a change to the 16mA target.

## Comparison and disposition
| Candidate | Primary evidence / limitation | Gate |
|---|---|---|
| LT8365 DC2838A charge pump | ADI DC2838A documented 9–30V to +250V/10mA; 5V/205V/16mA outside board demonstration | **BLOCKED**: guarantee-limit, exact stage currents/voltage, startup, efficiency, thermal, fault, procurement |
| LT3757 flyback + TDK DCT15EFD-U44S003 | ADI reference 5–12V to 350V/10mA; candidate transformer reported obsolete by distributor | **BLOCKED** sourcing; replacement needs verified magnetics/loss |
| MAX668 coupled inductor | Prior comparison candidate, no qualified transformer+loss+fault proof | **BLOCKED** |
| Direct SYS flyback | Potential removal of 5V conversion loss, but input voltage and magnetics unknown | **BLOCKED** |

The LT8365 ordinary single-inductor boost directly to 205V remains **NO-GO** because its 150V internal switch cannot sustain the required off-state voltage; charge pump is a distinct topology.

## Required independent review / next bounded work
1. Extract guaranteed minimum LT8365 switch current limit and max switch voltage from exact ADI datasheet revision and identify relevant conditions.
2. Trace DC2838A switch and flying-cap currents, node maxima, diode and capacitor voltages in the manufacturer schematic, including cold startup and load removal.
3. Source **two current-production controller + magnetics combinations** with exact manufacturer MPN, winding, Isat/core loss, availability/date, unit quantity and landed cost; report UNKNOWN where evidence missing.
4. Provide loss budget (switch, copper/core, diodes, flying caps) and enclosure temperature bounds. Independently prove OVP, safe stop and discharge with Cmin/Cmax and tail energy; 220V HV5524 recommended ceiling must not be exceeded.
5. SOP proposal (not direct edit): explicitly distinguish branch HEAD from blob SHA and repository-wide commit search; require source links and model applicability statement on every sensitivity calculation.

Sources for subsequent verification: ADI LT8365 product/data sheet https://www.analog.com/en/products/lt8365.html ; ADI DC2838A demo board https://www.analog.com/en/resources/evaluation-hardware-and-software/evaluation-boards-kits/dc2838a.html ; project #10 https://github.com/mitsu32m/PROJECT-NIXIDORO/issues/10 . These are source pointers, not a claim of fresh datasheet extraction in this run.

No procurement, fabrication, HV energization, main merge, requirements edit, or schedule changes authorized or performed.
