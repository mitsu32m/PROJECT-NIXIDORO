# Handoff — PROJECT-NIXIDORO

Current snapshot: **2026-11-25 JST**. Examined HEAD: **58976653bd8f41bdae82139f62199a30b9c549c0**. 正本は作業ブランチのlive HEAD。前回確認保存1b970784b6863f0f0c8a065863592b62e98234deから3件のreport追加。会話やこのSHAを永久最新としない。

## Current Work decision package

[WORK-INT-007](2026-11-25-0956-JST-WORK-INT-007-cutoff-energy-and-current-gates.md) integrates C-027 plus scoped Work checks of A04:01 (still PENDING C REVIEW). **Hardware adoption BLOCKED / NOT ORDER-READY.**
- C-027 accepts Work00529us polarity correction and Würth drawing/functional-insulation scope; B11/24 09:03 now reviewed within stated arithmetic/source limits. No actual continuous pair qualified.
- **D-024:** input capacitors downstream of upstream cutoff remain energy sources. ASSUMED5→3V/10,22,47uF gives80,176,376uJ available energy, compared to historical ASSUMED73.107uJ HV headroom. No guaranteed transfer/no hardware failure proof; do not shrink input C from this alone. Inventory all real Ceff/nodes/alternate feeds/magnetic energy and stop latency.
- TPS22918 upstream switch is a new comparison candidate only. TI2us tOFF is TYP under specific steadyVIN/25C/load conditions; no max. QOD weakens as VIN collapses and does not discharge HV capacitor. No independent reverse-blocking or full-load RON guarantee established.
- **D-025:** LT8365 boost-input proxy1.5A steady ceiling differs from1.5/2/2.7A current-limit table and actual pump branch current. At ASSUMED3V/.75 efficiency bus case only.08444A ripple budget; lamp-only+dual bleed negative. Actual topology/low-SYS qualification remains open.
- **11/25 evidence checkpoint at09:56: NOT SATISFIED YET.** No qualified HV pair/protection BOM/cell assembly/current landed quote; old BOM price/stock still11/15. Initial40k/reserve10k/total50k unproven. This is not an end-of-day failure or authorization.
- Next A: actual stop-latch/driver and downstream cap energy/fault table (#6/#8/#9). B: actual pump topology or concrete alternate pair, landed quote/staged BOM (#10/#7). C: A04:01 + Work007 energy/source scope. Prior system/thermal/UI holds apply.

## Previous integrated baseline (review status superseded above)

[WORK-INT-005](2026-11-24-1003-JST-WORK-INT-005-ovp-timing-and-magnetics-gates.md) integrates C-025/026. TLV6700 precision divider and CJ5143/Würth candidates remain **BLOCKED for hardware adoption**.
- **Correction to C-025/026 timing:** TI TLV6700 p6 footnote/Figure1 refers to input transitions. INB rising→OUTB falling is tPLH=29µs NOM, not18µs. Neither has max bound. At UVLO OUTB high-Z; VDD>1.8V requires450µs MAX before correct output under stated conditions. No comparator-only fail-off claim.
- **Static OVP:** ±0.1% ideal resistor proxy still leaves only0.657216V nominal interval and73.107µJ headroom per assumed1µF at its normalized midpoint. Actual divider/bias/TC/normal dynamic/tail/stop proof absent. ±1% proxy is limited rejected, TLV6700 itself remains alternative.
- **Magnetics:** CJ5143 Lmin13.5µH at1.2A is characterization, not continuous/Isat.3V/100kHz ideal fully-reset model cannot supply3.28W. Würth750315839 controlled drawing rev003.001 confirms N1=3dot–5,N2=7dot–8,N3=8dot–9 and functional-insulation wording;3.2A is TYP,50–200kHz is typical application. No full stage qualified.
- **Review status:** B11/23 21:03 and Work004 INFEASIBLE distinction reviewed arithmetically by C-025. B11/24 09:03 was subsequently reviewed by C-027 within arithmetic/source scope. Do not treat Work partial checks as C completion.
- **Next concrete work:** A real default-off OVP/stop-latch and HV resistor/cap guarantee table (#6); B continuous L(I,T)/thermal/controller match and landed small-order quotes (#2/#7); C validate29µs polarity correction and Würth/newB batch. Preserve prior thermal/PWR/lamp/UI requirements below.

## Previous integrated baseline (still applies except review-status supersession above)

[WORK-INT-004](2026-11-23-2201-JST-WORK-INT-004-power-discharge-topology-integration.md) integrates C-007〜024; original reviews preserved. **Analysis requirements adopted; hardware/parts adoption BLOCKED / NOT ORDER-READY.** B 11/23 21:03 arithmetic was subsequently checked by C-025; actual mode adoption remains BLOCKED.

1. **同じ負荷台帳:** digit/neon/bleeder/OVP-divider/driver-leakageを分離し、USB→SYS損失・Paux・signed IBAT（放電正）を記す。16mAがlamp-onlyかwhole-HV-busか未決。200〜205Vのnominal/windowも未決。仕様を変更しない。
2. **放電不整合を修正:** single330kとdual300k×2を別案にする。ASSUMED eta=.675,205V,3mA/digit,.5mA/neonではdual Rmin285k×2/450mA USB例はdigit2だけでも不成立。floorを0へclipして可としない。300kは採用品でない。60V/5sは安全基準でない。
3. **HV部品:** Q4434/35はメーカー1:1で205V適格ペアから除外。LT3757はcontroller-only比較候補、古いTDK DCT15EFD-U44S003参照は注文根拠でない。MAX668結合方式とLT8365 multiplier/direct-SYSは比較候補。ordinary boost限定却下を普遍化しない。
4. **保護を分離:** charge inhibit、BAT-only load cutoff、HV hard-off/residual dischargeを別証明。CE=GNDは実draftのまま。MCU3V3-only pullup/floatではfail-inhibitを保証しない。TI EVM PDFの直接取得は今回失敗、内部pull-down保証にしない。
5. **一次表の条件:** BQ500mA設定450/475/498mAはlimit threshold。VBSUP40/20mV、BUVLO3VはTYP。115/140mΩはVBAT4.5V/400mA条件。supplement非regulate・BAT-only TSなしをTI Rev.Bで今回確認。MAX66870µs=TYP、tail max不明。HV5524推奨220V、絶対230V。

## System holds

205V×16mA=3.28W > 5V×500mA=2.5W。USB-only full target不成立。USB+BATは放電し得る。
実磁性部品/dot/Llk/電流波形、FET/rectifier/clamp/core/銅損/熱、Cmin/Cmax/Etail/OVP/停止/共通return、TPS61023最低SYS/起動/熱、cell/PCM/NTC取付/熱遮断は未適格。P2150K/Rを混同せず、Rの15AをKへ移さない。
Pico2/RTC/OLED/UIの提案baseline保持。OE/BLは絶縁ではない。reverse feed、RTC backup、3V3負荷、board EP/via/copper、HV connector/抵抗working voltage、PETG内cell温度/遅れ未検証。新verified hardware nodeなし、release gate locked。

## Next bounded outputs — no formal Claim

- **A #6 + #9/#8:** 実比較器/ref/divider/cap/stop/discharge候補1式と保証表、Cmin/Cmax/Etail欠落、無給電/共通return fault matrix。CE/負荷cutの実候補と回路変更要求範囲を文書化。同じ仮定RC表のみを反復しない。
- **B #7/#2/#10 + #4:** 現行HV磁性部品1個のcontrolled図面/電気/熱/working voltageと国内少量納期/着地価格、又は具体的全候補除外理由。lamp/PCM/holder/NTC assemblyと段階BOM、同一topologyの負荷台帳。
- **C:** C-027がWork005訂正/B09:03を限定確認済み。次は未レビューA04:01とWork007のTPS/energy-fault batch。歴史的review backlog UNKNOWN。
- **Work:** 新MPN/保証/見積/実回路判断がなければ大型再調査せず確認SHAを短く保存。

## Prototype, budget and owner decisions

D-014 staged LV-first planning retained; no purchase/test authorization. 11/15価格/在庫は歴史値。初回≤40k/予備≥10k/総額≤50kは未立証、現着地額UNKNOWN。旧BOMは保持。11/25部品証拠、12/01方式/電力/熱、12/15初回購入判断packageは提案checkpoint。期限2027-01末前の判断を優先する。
具体費用/代替を揃えてから、16mA境界/電圧window、USB時net-chargeと表示動作、段階試作範囲をユーザーへ提示。重要仕様変更、購入/PCB/HV/mainマージ/安全承認は禁止のまま。

## Historical evidence

[INT-003](2026-11-19-work-integration-003.md), [INT-002](2026-11-18-work-integration-002.md), [INT-001](2026-11-17-work-integration-001.md) retained. INT-003限定Rs/Rp比証明はC-007で数学範囲レビュー済み。旧handoffはGit履歴に保持。旧schedule観測を現在の実行能力としない。本統合でautomation照会/変更なし。
