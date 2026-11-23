# HV-002 / Issue #6 — TLV6700 independent OVP threshold first-pass screen
Date: 2026-11-24 00:00 JST. Role: Chat A deep-design. Branch: `codex/reva-integrated-prototype-review`.
**PENDING REVIEW; NO FORMAL CLAIM; hardware status BLOCKED / NOT ORDER-READY.**

## Bounded task
Question: Can an actual catalog comparator with manufacturer stated overtemperature threshold accuracy and an illustrative high-voltage divider fit the narrow historical 214.13495V normal-static-high to 220V HV5524 recommended ceiling window? This is a *necessary static screen*, not a complete OVP implementation. No hardware modifications or approval.

Repository checked: docs/ai-workflow.md, docs/verification/handoff.md, docs/verification/open-issues.md, docs/verification/decisions.md, docs/tech-tree.yaml, docs/tech-tree.md, WORK-INT-004 (2026-11-23 22:01), Chat A 20:00 report, issue #6 via issue search. Branch search verified name; **starting branch commit SHA not obtainable from branch-search output**; no Claim, no assertion of exhaustive new-report listing. Work's handoff explicitly prioritizes actual comparator/ref/divider candidate rather than another RC table.

## Manufacturer primary candidate and classification
Texas Instruments **TLV6700**, datasheet Rev. B, manufacturer product page https://www.ti.com/product/TLV6700 (accessed 2026-11-23 JST). Listed: internal 400mV reference, **0.5% max at 25C and 1.0% max overtemperature threshold accuracy**, 1.8–18V supply, open-drain outputs (18V rated), propagation delay **18us product-page figure (not a guaranteed worst-case stop latency)**, input bias **15nA max** (listed), internal hysteresis **5.5mV typical**. Exact threshold accuracy definition, bias polarity, resistor conditions, startup and guaranteed timing need verification in the electrical-characteristics table before adoption. The IC is **NOT a 220V input**: external HV-rated resistor chain and independent safe supply/stop latch are necessary.

## Reproducible necessary-condition calculation
ASSUMED illustrative divider: top=5.415Mohm, bottom=10kohm, each independently +/-1% (no real resistor MPN/working voltage/aging assigned). ASSUMED threshold reference 0.400V with +/-1% as a **proxy** for manufacturer's 1% overtemperature threshold accuracy; this is not an exact datasheet transfer model.
Ideal trip V=Vref*(1+Rtop/Rbottom).
- nominal = 217.000V
- low trip = 0.396*(1+0.99*5415000/(1.01*10000)) = 210.584V
- high trip = 0.404*(1+1.01*5415000/(0.99*10000)) = 223.590V
- static historical normal high = 214.13495V **INCOMPLETE ASSUMPTION**, not a guaranteed dynamic normal max
- HV5524 220V **recommended upper bound**, not a design trip target.
Thus **210.584V < 214.13495V and 223.590V > 220V**. The assumed 1% discrete divider plus 1% threshold proxy is **NO-GO for this narrow historical static window**, even *before* post-trip energy. This does **not** reject TLV6700 generally: tighter precision resistor network, different normal voltage window or independently bounded trip/energy may change outcome, but requirement changes need owner approval.

At 220V nominal divider current=220/5425000=40.55uA; bottom input node nominal ~0.406V; worst 15nA bias times ~9.98kohm Thevenin implies ~0.150mV, or ~0.081V HV equivalent (sign depends on input current). **This is an independent magnitude illustration**, not a guaranteed additive worst-case because the datasheet's threshold accuracy may already include some bias effects. HV chain dissipates approximately 8.922mW total, but individual resistor voltage ratings and open-resistor faults are UNKNOWN.

## Essential stop-path and common-cause matrix (not proven)
- TLV6700 supply absent / brownout: open-drain output may be high impedance; pull-up alone can accidentally enable HV. Need independently defined default-OFF enable and hardware latch.
- Top HV divider open: sense node falls; overvoltage can be falsely invisible. A second independent detection or topology-specific fault response is required.
- Bottom divider open: sense input can rise beyond safe input limits; input protection and fail-off path must be designed.
- Shared return open: both detector and discharge path may lose reference. Physical return placement/independent continuity and single-fault review required.
- Converter FET/controller stuck on: comparator signal alone cannot guarantee removal of energy. Hard-off energy interruption and worst-case Etail required.
- MCU reset/USB loss/BAT loss: comparator supply, latch and discharge must retain a safe state; charged capacitor can outlive logic power.
- Startup/no load/load removal: worst-case response delay, Cmin and post-trip energy still UNKNOWN.
- Comparator output open/short: latch/driver logic polarity and independent shutdown must be tested.

## Decision and handoff
**CONDITIONAL**: TLV6700 is a concrete manufacturer-supported candidate for research, not a qualified independent OVP.
**NO-GO (limited)**: illustrative 1% divider + 1% threshold-proxy meets the historical 214.135–220V static window.
**BLOCKED**: guaranteed exact comparator threshold transfer over temp/age, real HV resistor chain, supply/POR, hard-off latch and tail-energy upper bound, real Cmin/Cmax, common-return faults, actual operating voltage window.
**PENDING REVIEW**: Chat C independent check; Work handles shared index integration. Do not select resistor values, comparator, threshold or schematic as final.
Next: obtain Rev.B electrical-characteristics min/max and timing conditions; compare matched <=0.1% HV-rated resistor network with worst input bias, temperature coefficient, aging and individual working voltage; identify hardware default-OFF controller gate and a physical discharge path, all using actual MPNs.
No purchase, PCB manufacture, HV energization, main merge or requirements changes.
