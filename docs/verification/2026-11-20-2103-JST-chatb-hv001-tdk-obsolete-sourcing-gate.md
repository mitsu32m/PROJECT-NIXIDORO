# Chat B — HV-001 / SYS-001: TDK reference-transformer sourcing blocker
Date: 2026-11-20 21:03 JST. Role: wide-research. Branch: `codex/reva-integrated-prototype-review`.
Starting HEAD: `69dc021dc3b562f2f51f620091e061dec62f03fd` (GitHub branch REST).
Claim: NONE; provisional research, issue #7 sourcing / #2 HV topology / #4 SYS modes. Review: **PENDING REVIEW** for Chat C.
Decision: **BLOCKED** as orderable transformer; **CONDITIONAL** as historical manufacturer application reference.

## Contract
Question: Is the TDK DCT15EFD-U44S003 transformer in the ADI LT3757 350V/10mA example orderable and documented sufficiently for a 205V/16mA prototype? Exit: check part lifecycle, domestic distribution, source-controlled drawing, numerical limitations and alternatives. No procurement or circuit modification.

## New sourcing evidence
- DigiKey's TDK DCT15EFD-U44S003 listing explicitly states **Obsolete / no longer manufactured**, 16.50 x 17.00 x 8.50 mm, SMD. Source: https://www.digikey.com/en/products/detail/tdk-corporation/DCT15EFD-U44S003/1473742 (checked 2026-11-20). This is distributor lifecycle evidence, not direct manufacturer end-of-life notice.
- Japanese distributor Marutsu listing https://www.marutsu.co.jp/pc/i/12297346/ reports **DigiKey inventory 0 as of 2026-08-01 04:00**, MOQ/SPQ 500, 12-week listed lead time and unit JPY 851.86 tax included at 500 pcs. Historical page, NOT a current purchase quote or confirmed supply. MOQ * unit cost = JPY 425,930, far beyond project JPY 50,000 total budget, even before shipping; do not assume this is the only sourcing route.
- A TDK-authored drawing mirrored at https://www.alldatasheet.com/html-pdf/532711/TDK/DCT15EFD-U44S003/63/1/DCT15EFD-U44S003.html (manufacturer-authored content, third-party host, verify against TDK original) states Lpri 10uH +/-10%, leakage <=1uH, primary winding DC resistances 120mOhm and 140mOhm max, secondary 4.0Ohm max, 1:10 ratio, 1kVAC/2s withstand. Drawing dated 2005; it does not establish continuous 205V/16mA operation or safe thermal limits. Manufacturer-controlled current PDF not retrieved.

## Engineering implications
At 205V*16mA = 3.28W, USB 5V*0.5A = 2.5W is insufficient even with lossless conversion. At assumed etaHV 75-80%, 5V HV input requires 4.373-4.100W = 0.875-0.820A; at assumed eta5=90%, SYS/battery-side input 4.859-4.556W before controller/charger/OLED/MCU loads. Battery supplement is potentially net discharge, not charging.
If hypothetical secondary RMS current were 16mA, Rsec=4Ohm max implies <=1.024mW at that RMS; this is NOT an upper bound for actual pulsed secondary RMS current and ignores copper heating, core loss, leakage and rectifier loss. Do not misuse the 5A distributor description as a guaranteed 205V/16mA operating rating.
Independent hardware OVP is required. Chat C C-REVIEW-012 flagged LT3757 internal FBX OVLO 6-8% over nominal, which could extend above 220V at nominal 205V even before tolerance/overshoot. No HV5524 safety qualification.

## Candidate comparison and next actions
1. LT3757 + DCT15EFD-U44S003: published ADI 5-12V -> 350V/10mA reference, but **obsolete transformer / 500-piece domestic listing**; research precedent only, not purchase-ready.
2. MAX668 coupled-inductor: candidate remains; original topology, actual magnetic, switching stress and procurement not qualified. Ordinary uncoupled boost rejection does not reject coupled variant.
3. Alternative current-production 5V-input flyback controller + catalog transformer: highest-value next research. Require a manufacturer reference showing >=3.28W nominal output OR documented component limits supporting a 205V/16mA re-design, exact winding drawing, single-unit Japan sourcing, and worst-case low-VIN, losses, temperature, open-load/OVP and discharge.
4. Direct SYS/1S flyback: possible efficiency benefit but needs actual low-cell-capable controller/magnetics; LT3757 5V-min reference is not direct-1S proof.

## Review handoff and SOP proposal
Chat C: verify DigiKey obsolete classification, Marutsu historical MOQ/stock and TDK drawing provenance; challenge any claim that 10uH/5A or 3.5W ADI example proves 205V/16mA operation. Work: mark this exact TDK part procurement BLOCKED; preserve LT3757 circuit as research-only reference. Suggested SOP addition (do not directly edit shared SOP): every manufacturer example used for an order-ready proposal must pass independent lifecycle + MOQ/quantity + lead-time gate, separately from electrical feasibility.
New issue candidate: **HV-001-SRC** find currently manufactured, single-unit sourceable HV transformer/controller combination; link to existing #7/#2 rather than duplicating issue.
No formal Claim, no shared-index changes, no purchasing, PCB, HV, main merge, spec or schedule changes.
