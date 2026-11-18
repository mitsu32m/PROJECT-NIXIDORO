# Chat B PROTO-001A — HV magnetics sourcing and prototype schedule gate

- Date: 2026-11-18 13:02 JST
- Task: PROTO-001A, parent [GitHub Issue #7](https://github.com/mitsu32m/PROJECT-NIXIDORO/issues/7); related SYS-001, HV-001, HV-004, BOM-001
- Role: Chat B wide research, **PROVISIONAL / NO FORMAL CLAIM**
- Starting branch HEAD: `ca28be2e2cefcce4fc24ef2b1c2419bf0a667633`
- Review status: **PENDING REVIEW** (Chat C)
- Scoped verdict: **CONDITIONAL** for traceable sourcing evidence; **BLOCKED** for 205V/16mA continuous magnetics qualification and procurement release.
- No changes to target, schematic, shared indexes, schedule or safety authorization.

## 1. Task and novelty

Work's latest `docs/verification/2026-11-18-work-integration-002.md` assigns Issue #7 to Chat B: source actual prototype parts, not more idealized topology exercises. This run isolates a time-critical bottleneck: **can an actual controller+transformer pair be procured and shown to meet the 205V/16mA target before the Jan 2027 spending deadline?** The full five-category BOM of Issue #7 remains open. Unlike Chat B SYS-001D/E and Chat A Issue #2, this is an *actual supplier and manufacturer-document screen*, not a new switching model.

Startup: read six mandatory documents (`docs/ai-workflow.md`, `docs/verification/handoff.md`, `docs/verification/open-issues.md`, `docs/verification/decisions.md`, `docs/tech-tree.yaml`, `docs/tech-tree.md`), latest Work integration, previous Chat B SYS-001E/F and lamp report, `docs/hv-transformer-screen.md`, and Issues #1–#8. GitHub Issue #7 has role in title/body but no proven atomic claim; therefore provisional append-only work, no ownership lock. Shared indexes are integrator-owned.

## 2. Manufacturer and distributor evidence matrix (accessed 2026-11-18 JST)

| Exact MPN / pairing candidate | Primary manufacturer evidence | Distributor observation (not manufacturer guarantee) | Qualification verdict |
|---|---|---|---|
| **Sumida 13324-T086 + ADI LT8304(-1)** | [Sumida LT8304 transformer family PDF](https://products.sumida.com/products/pdf/CEP1311F%20%2813324-T083%20to%20T087%29%20LT8304%20ver%201.pdf): 40µH LPRI **TYP**, 1:5, leakage 1.2µH **TYP**, target **4–36V→200V/12mA** (manufacturer's **TARGET APPLICATION**, not guaranteed 205V/16mA). [ADI LT8304 datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/lt8304.pdf) for controller conditions; LT8304-1 current-limit/efficiency screen already in `docs/hv-transformer-screen.md`. | [JLCPCB part C17554736](https://jlcpcb.com/partdetail/Sumida-13324T086/C17554736): **0 in stock**, pre-order, minimum 3, indicative **US$4.0302/part** before tax/shipping, 2026-11-18 retrieval. [LCSC C17554736](https://www.lcsc.com/zh-CN/product-detail/C17554736.html): **out of stock**. [DigiKey](https://www.digikey.pl/en/products/detail/sumida-america-inc/13324-T086/8020773): **0 in stock**, displayed 24-week manufacturer standard lead time; one regional page forecasts 200 on **2027-04-02** (regional/time-varying). | **NO-GO for immediate JLC/LCSC stock-based sourcing at snapshot**. **UNKNOWN** for 205V/16mA; 12mA target is 25% below 16mA, and 200V below 205V. Controller-specific switching, low-input current limit, thermal and OVP not qualified. |
| **Würth 750315839 + LT8304-1 / alternative qualified 5V flyback controller** | [Würth 750315839 datasheet](https://www.we-online.com/components/products/datasheet/750315839.pdf): 1:10, Lp=40µH±10%, saturation 3.2A **TYP** at 20% L reduction, leakage ≤0.5µH, primary DCR 85mΩ±10%@20°C, secondary 8.4Ω±10%, manufacturer reference **200V/12mA** at 4–36V and 50–200kHz. | Previous repository `docs/hv-transformer-screen.md` says sourcing had been checked 2026-11-15, but **this run did not independently reconfirm a Japanese distributor's live stock, JPY price or lead time**: UNKNOWN. | **UNKNOWN** availability and 205V/16mA capability; 16mA is 1.333× the reference output current. MAX668 ROSC=200kΩ full-temperature 222–278kHz is outside the 50–200kHz *reference application* band; not proof of absolute prohibition, but a frequency/core-loss qualification gap. |
| **Sumida 13324-T087 + LT8304(-1)** | Same [Sumida family primary PDF](https://products.sumida.com/products/pdf/CEP1311F%20%2813324-T083%20to%20T087%29%20LT8304%20ver%201.pdf) and [individual specification](https://media.digikey.com/pdf/Data%20Sheets/Sumida%20PDFs/13324-T087_Spec.pdf), 40µH-class, 1:10 according to existing project screen. | **Live stock, JPY tax-inclusive price, shipping and lead time not checked** in this run. | **UNKNOWN**; no 205V/16mA continuous guarantee. |
| **Direct SYS→HV LT3757A or LM5155 + actual magnetics** | [ADI LT3757A datasheet](https://www.analog.com/media/en/technical-documentation/data-sheets/lt3757-3757a.pdf) flyback DCM design method; [TI LM5155 datasheet](https://www.ti.com/lit/ds/symlink/lm5155.pdf). Existing SYS-001E hypothetical ~2µH / 1:26 / 4.8A is **not a coherent qualified design point**; Work integration explicitly requested correction. | **No qualified exact transformer MPN, stock, price or footprint** established. | **BLOCKED** for pair qualification. Do not treat minimum controller input voltage as a proven 3V→205V/16mA power train. |

**Availability caution:** Search-indexed regional DigiKey pages disagree about expected replenishment dates (e.g. Dec 2026 vs Apr 2027). Only **0 current stock** was consistently observed in retrieved JLC/LCSC and one DigiKey regional listing. ETA is not guaranteed, and the Japan checkout region/stock pool may differ. Verify with live Japan-specific seller/quotation before procurement planning; no order authorized. Prices above are distributor displayed USD, **not JPY, not tax-inclusive, not delivered cost**. A `24-week standard lead time` is not a promised shipping date for a single sample.

## 3. Decision-critical calculations and constraints

**ASSUMED TARGET**: 205V*16mA=3.28W continuous. Sumida T086 and Würth 750315839 manufacturer **application examples**: 200V*12mA=2.40W. The output-power gap is `3.28/2.40=1.367`, **36.7% more output power** than the documented reference point; current gap `16/12=1.333`. This does **not** mathematically establish impossibility; it establishes that the published reference is not sufficient qualification. Thermal and current-limit margins must be recalculated using actual controller, input, switching frequency and selected PCB.

**ASSUMED** `etaHV=.70`: HV-stage input `3.28/.70=4.686W`, stage loss `1.406W`. At 5V, HV-stage input average `0.937A` excluding 5V logic; at 3V direct input, `1.562A` average excluding logic and path loss. Neither number is a guaranteed MOSFET or transformer peak. Actual peak, `Isat_min(T)`, leakage spike, rectifier voltage/current and winding temperature remain **UNKNOWN**. Sumida's 4V minimum target input is not a demonstrated 3V direct-SYS use case.

USB 5V / configured BQ25185 input 450/475/498mA [TI datasheet](https://www.ti.com/lit/ds/symlink/bq25185.pdf) offers only 2.25–2.49W electrical input at the input-limit corners. Therefore **USB-only 16mA is NO-GO** regardless of these magnetics. USB+BAT supplement is not simultaneous positive charging; cell and thermal limits remain unresolved. No change to 16mA target.

## 4. Prototype sourcing gate / staged BOM

Issue #7's complete initial BOM is **not yet deliverable**. Do not claim the ≤JPY40,000 initial or ≥JPY10,000 reserve targets are met: major parts, assembly, taxes and shipping remain UNKNOWN. A controller listing alone does not count as a qualified HV subsystem.

For an **LV-first prototype research BOM**, preserve the existing Pico 2, BQ25185, TPS61023, USB protection, ADC gating and LV connector interface as **proposed**, but qualify exact 21700 protected cell/NTC, TPS61023 L1 Isat and real capacitor derating, connector/footprint and charger temperature before purchase approval. For a **separate HV draft BOM**, reserve explicit placeholders for controller, qualified transformer, FET, rectifier, snubber, sense, FB, HV capacitor Cmin/Cmax, independent OVP latch/hard-off, discharge network, HV-rated resistor/connector and physical cover. Do not fill placeholders with incompatible parts just to generate a price.

**High-impact schedule discovery:** the Sumida T086 0-stock observations mean a JLCPCB assembly workflow cannot assume this part will be available by the suggested 2026-12-15 first-order decision checkpoint. The candidate may require an independently sourced substitute, a different topology or a different staging plan, each subject to technical review. An LCSC/JLCPCB catalog entry or PCB footprint does **not** establish physical stock or fit for a 205V/16mA stage.

## 5. Next narrow research and review tasks

1. **Chat B / PROTO-001B:** search actual Japanese suppliers for Würth 750315839 and alternate manufacturer-qualified 200V-class flyback magnetics; record live quantity, tax-inclusive JPY unit cost, minimum order, dispatch/lead time and exact manufacturer PDF. Mark unavailable or UNKNOWN rather than fabricate.
2. **Chat B / PROTO-001C:** select an *exact* NE-2-class lamp and protected 21700+attached NTC candidate; verify manufacturer DC lamp characteristics and cell charge/thermal limits, current stock and footprint. Existing IN-12B archival 2.5–3.5mA and San Guang 110VAC/68kΩ ~0.7mA must **not** be promoted to selected DC lamp guarantees.
3. **Chat A:** qualify a controller+magnetics pair at low supply, 205V/16mA continuous including worst-case peak, efficiency, heat, voltage stress and independent OVP. Correct mixed efficiency/ideal DCM current ratios noted in WORK-INT-002.
4. **Chat C:** independently review manufacturer *reference output* versus guaranteed ratings, the 36.7% power gap, supplier 0-stock and regional ETA interpretation, and staged BOM's unpriced placeholders.
5. **Work:** integrate only reviewed evidence into canonical BOM/issues/tech tree; preserve design/ordering hold and the 2027-01 spending deadline. SOP v1.1 already contains non-blocking provisional research fallback; no new SOP amendment needed.

**PENDING REVIEW. NO FORMAL CLAIM. NOT ORDER-READY.** No purchases, fabrication, HV operation, safety signoff, main merge, or requirement changes.
