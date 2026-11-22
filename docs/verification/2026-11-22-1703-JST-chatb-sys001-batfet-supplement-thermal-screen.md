# Chat B — SYS-001/PWR-002: battery-supplement current and BATFET thermal screening
Date: 2026-11-22 17:03 JST
Status: **PENDING REVIEW**; scoped result **CONDITIONAL** (power algebra), **BLOCKED** (actual current/thermal qualification). **NO FORMAL CLAIM**.
Branch: `codex/reva-integrated-prototype-review`. Starting HEAD: `3a7d656453a7f13421a27f2174fddf9314000482`.
Issue: #4 SYS-001A; dependencies #8 PWR-002A, #9 THERM-001, #7 PROTO-001.

## Task contract and overlap control
Question: What battery discharge current and BATFET conduction heat are implied by the 205V/16mA target at different cell voltages, without incorrectly treating the charger current-limit MIN or RON MAX at a different test point as guaranteed supply or low-cell performance?
Exit: reproduce parametric mode equation, corner table and source/thermal limits, then hand to Chat C.
Read the six canonical SOP/handoff/open-issues/decisions/tech-tree YAML/MD documents, latest A 16:03, C-REVIEW-019 15:04, B 13:00 and open Issues. No reliable atomic Claim evidence; provisional work only. No shared index edits.

## Primary source and evidence classes
TI BQ25185, SLUSF65B Rev.B (Aug 2026), https://www.ti.com/lit/ds/symlink/bq25185.pdf , electrical characteristics and §§6.3.2–6.3.3, §6.4.
Predecessor transcription: configured 500mA input limit 450/475/498mA MIN/TYP/MAX; supplement VBSUP1 40mV TYP, exit 20mV TYP; battery UVLO 3.0V TYP; BATOCP 3.13A TYP; BATFET RON 115mΩ TYP/140mΩ MAX **at VBAT=4.5V, IBAT=400mA**; JEDEC RthetaJA 68.3°C/W. Values and test conditions must be rechecked by Chat C against the actual PDF before integration. None is a guarantee of continuous 3V supplement operation.

## Parametric energy equation
Project target (not proven real lamp current): P_HV=205*0.016=3.28W.
Define eta_HV and eta_5 (ASSUMED efficiencies), P_aux SYS-side auxiliary load, P_USB,SYS actual delivered USB-to-SYS power (not nominal current limit times voltage), eta_BAT effective battery-path delivery fraction including BATFET/protector/contact. For discharge-positive I_BAT:
P_SYS = 3.28/(eta_HV*eta_5)+P_aux;
I_BAT >= max(0,P_SYS-P_USB,SYS)/(V_BAT*eta_BAT).
This is a necessary steady-state energy screen, not a sufficient transition/thermal guarantee. In particular P_USB,SYS <= V_USB*I_USB,actual, and I_USB,actual is NOT guaranteed to equal the BQ input-limit threshold. Battery assist means negative net charge current; DPPM first reduces charge current to zero.

Illustrative ASSUMED eta_HV=.75, eta_5=.90, P_aux=0, eta_BAT=1, USB=5.0V, USB-to-SYS loss=0:
P_SYS=4.859259W.
| Actual USB current scenario (ASSUMED) | P_USB,SYS ideal | Battery deficit | I_BAT @ 3.0V | @ 3.6V | @ 4.2V |
|---|---:|---:|---:|---:|---:|
| 0mA (battery only) | 0W | 4.8593W | 1.620A | 1.350A | 1.157A |
| 300mA | 1.50W | 3.3593W | 1.120A | 0.933A | 0.800A |
| 450mA | 2.25W | 2.6093W | 0.870A | 0.725A | 0.621A |
| 498mA | 2.49W | 2.3693W | 0.790A | 0.658A | 0.564A |
The 450/498mA rows are **hypothetical actual current scenarios**, NOT guaranteed delivery by a MIN/MAX current-limit threshold. At 3.0V battery UVLO TYP, this row is a mathematical boundary only, not an approved operating point. Real efficiencies, P_aux, source droop and losses worsen required current.

## BATFET loss sensitivity — not a low-cell guarantee
Using P_cond=I_BAT²*R only as an illustrative screen:
- battery-only 3.0V, 1.620A: 0.302W at 115mΩ; 0.367W at 140mΩ.
- USB actual 450mA, 3.0V, 0.870A: 0.087W at 115mΩ; 0.106W at 140mΩ.
- battery-only 3.6V, 1.350A: 0.210W at 115mΩ; 0.255W at 140mΩ.
These are **ASSUMED fixed-resistance sensitivity values**, not warranted device losses: published 115/140mΩ test is VBAT=4.5V, IBAT=400mA, and low-voltage/high-current RON, PCB copper and enclosed thermal impedance are unknown. Applying 68.3°C/W JEDEC to these illustrative losses would give ~25°C rise for 0.367W, but **must not** be presented as PETG enclosure junction rise: JEDEC board, heat coupling, switching/dynamic loss, charger concurrent dissipation and ambient differ. Battery protector/contact resistances and cell self-heating add separately.

## Mode and fault boundary
- USB-only continuous 16mA: NO-GO at 5V/500mA even lossless; 3.28W > 2.5W.
- USB+BAT: conceptually supported by BQ supplement but current/thermal, startup, low-cell cutoff and droop BLOCKED; net battery discharge, not net charging.
- BAT-only: largest illustrative discharge current and conduction heat; selected 21700+PCM limits, TPS61023 VIN/inductor/peak and thermal behavior UNKNOWN.
- BAT UVLO/PCM opening during HV output, USB hotplug, charge inhibit and MCU-off must trigger independent HV hard-off and discharge; BQ /CE alone does not remove SYS/HV energy. Battery-only TS measurement absent per Rev.B §6.4.
- No continuous safe current may be inferred from BATOCP 3.13A TYP or JEDEC RthetaJA.

## HV alternatives and sourcing handoff
MAX668 series-aiding autotransformer, LT3757 flyback, LT8365 charge pump, direct-SYS flyback remain unqualified alternatives. Recent A 16:03 evaluates *only* ideal joint voltage-rating interval; no verified winding polarity, magnetic MPN, thermal, startup, OVP or in-stock pair. This run does NOT duplicate that analysis or assert new sourceable pairs. Candidate controller+magnetics MPN, current price/stock, and 205V/16mA measured feasibility remain UNKNOWN.

## Review request and next work
Chat C: independently recheck TI Rev.B RON/ILIM/OCP conditions; recompute mode table and loss arithmetic; challenge the omission of eta_BAT and all source-current assumptions; do not treat 68.3°C/W as an enclosure thermal bound. Work: retain PWR-002/SYS-001 BLOCKED, no hardware adoption.
Next Chat B: exact protected-cell PCM discharge limits and physical NTC/holder BOM, or two actually sourceable controller+magnetics pairs with controlled datasheets, verified winding drawings and price/stock timestamp.
SOP proposal for Work (do not directly edit docs/ai-workflow.md): require a separate 'actual delivered USB current' variable and explicitly mark every battery-path resistance at its datasheet test voltage/current before computing I²R.
No purchasing, PCB fabrication, HV energization, main merge, significant specification or schedule change.
