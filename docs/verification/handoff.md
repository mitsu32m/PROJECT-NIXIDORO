# Handoff — PROJECT-NIXIDORO

Current snapshot: **2026-11-28 10:04 JST**. Examined live HEAD: **19660a2a5d2298e384aad49883b95b862fd27fa9**. 前回Work保存bc805d6f9334172dc5423e2c0de41d79221bf094から2commit/新B08:56+C-029。毎回live HEADを確認する。

## Current Work decision package

[WORK-INT-013](2026-11-28-1004-JST-WORK-INT-013-rs-reproducibility-and-lt3751-boundary.md) integrates C-029 and direct-source correction. **NOT ORDER-READY / no hardware adoption / no formal Claim.**
- **D-030 corrected:** withdraw confirmed150uA-max/95VDC claim from Work012. Direct downloaded RS655-9413 PDF p1 locally rendered0.25mA±10%,matching C-029. SHA25653508b834a6e82888b7b4fa323ce237517582e8ec4a6666a72698896c0af99d7. Web screenshot still differed; prior raw bytes absent, no proven manufacturer revision. Preserve observations as retrieval reproducibility/controlled-lot/DC HOLD. Do not demand resolution of a proven150vs250 part-spec conflict.
- C-029 scopes B21:02/B13:02 source/arithmetic and D-027/028 A1A source difference/A1A-T-only PCN as reviewed; no blanket Work008/full hardware review. DC current/life/lot and landed quote still UNKNOWN. D-029 fully independent review still pending.
- **D-031 pending investigation:** new B LT3751/DA2033 deferred by C. Work p3 electrical table shows VCC4.75–24V,not gate-driver wording alone; E/I grade Note2 matters. Manufacturer Doc510-1 confirms DA2033/LT3751 compatibility, not continuous3.28W/thermal/working-voltage qualification. No new formal hardware candidate/node adopted.
- Next B:#2/#7 actual VCC/VTRANS bias/startup/FET/rectifier/continuousmagnetics/thermal and quotes; RS controlled raw/hash/lot/DC. A:#6/#8/#9 actual stop/cap energy/timing/fault and thermal. C:newB08:56+Work013 VCC/rawPDF batch. Existing HV/PWR/cell/UI/PCB/PETG locks remain.
- Initial40k/reserve10k/total50k UNPROVEN;12/01 design/12/15 initial-order decision package remain proposed checkpoints beforeJan2027 deadline. No purchase/test authorization.

## Previous Work012 package (RS/review claims superseded above)

[WORK-INT-012](2026-11-27-2202-JST-WORK-INT-012-cutoff-review-and-rs-source-conflict.md) integrates C-028 and scoped new RS primary evidence. **Hardware BLOCKED / NOT ORDER-READY. No formal Claim.**
- C-028 scopes A04:01/Work007 TPS22918 table/arithmetic/D-024 as reviewed. Conditional transfer model; real stop/latch/timing/energy/fault/thermal remain blocked. Work008/A1A/PCN and both lamp B reports still pending C.
- D-029 extends energy inventory with voltage-dependent Cdiff or conservative bounds, consistent trip/cut nodes and no double-counting; equality is zero margin. Actual energy transfer UNKNOWN. Compare upstream cut/direct inhibit/independent combined stop on same circuit; none qualified.
- Work independently rechecked TI Rev.C p6 typical2us/max blank, p13–14 QOD conditions. Internal-QOD200uF constraint and VIN-loss weakening do not prove HV discharge/energy partition/reverse blocking.
- **D-030 RS655-9413 HOLD:** linked brand PDF p1 says operating current(max)0.15mA and DC striking max95V versus listing250uA. New Work evidence pending C; B DC-striking-unknown statement incomplete. Applicable lot/current/DC sustaining/life still unknown; no formal part adoption/node verification.
- RS Japanese page currently retrieved shows reference1126ex/1239incl per10, stock inaccessible (web content may be cached); two packs2478incl before shipping is not landed quote. Prior stock counts historical only. Full initial40k/reserve10k/total50k unproven.
- Next A:#6/#8/#9 actual latch/cut/cap per-node energy/timing/fault and thermal. B:#4/#7 resolve RS150vs250uA/lot/DC and landed staged BOM/qualifiedpair. C: batch lamp B21:02/B13:02+Work008/newRS evidence.12/01/12/15 proposed checkpoints retained.

## Previous Work008 package (review scope superseded above)

[WORK-INT-008](2026-11-25-2159-JST-WORK-INT-008-neon-revision-and-lifecycle-gate.md) integrates the new B lamp-source batch with scoped primary checks. **Hardware adoption BLOCKED / NOT ORDER-READY.** NewB/Work008 findings PENDING C REVIEW; no formal Claim.
- **D-027:** A1A manufacturer-authored03/17 Rev2 table nominal0.5mA/max breakdown95VDC versus undated manufacturer-hosted family design0.6mA/90VDC. Applicable revision/lot/DC current and life UNKNOWN. B's revision-unknown statement corrected; generic distributor voltage is not proven same quantity as max breakdown.
- **D-028:** PCN333 issued/effective2014-01-21 explicitly lists A1A-T obsolete. Do not extend to bareA1A. Exact suffix lifecycle, actual DC data and current landed quote required; cached NRND/stock/price are not current guarantees.
- C-027 accepts Work00529us correction/Würth drawing scope and B09:03 limited arithmetic; no continuous pair qualified. Work007 downstream LV cap/tail/alternate-feed energy and TPS22918 typical-timing/QOD limits remain; A04:01/Work007 still pending independent C review.
- At this examined HEAD11/25 evidence checkpoint remains incomplete. Qualified HV pair/protection/cell assembly/current landed staged BOM missing. Initial40k/reserve10k/total50k UNPROVEN. Not an end-of-day verdict or authorization.
- Next B:#4/#7 exact lot/revision/DC/lifecycle or one current alternate plus quote; actual HV/cell staged BOM. A:#6/#8/#9 actual stop/latch/caps/fault and thermal. C: newB21:02+Work008 source/PCN batch and pending Work007/A04:01. No broad repeat research.

## Previous Work007 package (still applies within scope)

[WORK-INT-007](2026-11-25-0956-JST-WORK-INT-007-cutoff-energy-and-current-gates.md): D-024 inventories downstream LV Ceff/magnetic/timing/alternatefeed in same HV Cmin/Cmax; D-025 separates LT8365 steady-input guide from actual pump SW peak; D-026 TPS22918 remains research alternative. No actual hardware qualified.

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
- **C:** C-029でB21:02/B13:02出典/仮定算術とA1A/PCN範囲を確認。次はB08:56 LT3751/DA2033とWork013のVCC表/RS本体hash。D-029完全レビュー未了、歴史的backlog UNKNOWN。
- **Work:** 新MPN/保証/見積/実回路判断がなければ大型再調査せず確認SHAを短く保存。

## Prototype, budget and owner decisions

D-014 staged LV-first planning retained; no purchase/test authorization. 11/15価格/在庫は歴史値。初回≤40k/予備≥10k/総額≤50kは未立証、現着地額UNKNOWN。旧BOMは保持。11/25部品証拠、12/01方式/電力/熱、12/15初回購入判断packageは提案checkpoint。期限2027-01末前の判断を優先する。
具体費用/代替を揃えてから、16mA境界/電圧window、USB時net-chargeと表示動作、段階試作範囲をユーザーへ提示。重要仕様変更、購入/PCB/HV/mainマージ/安全承認は禁止のまま。

## Historical evidence

[INT-003](2026-11-19-work-integration-003.md), [INT-002](2026-11-18-work-integration-002.md), [INT-001](2026-11-17-work-integration-001.md) retained. INT-003限定Rs/Rp比証明はC-007で数学範囲レビュー済み。旧handoffはGit履歴に保持。旧schedule観測を現在の実行能力としない。本統合でautomation照会/変更なし。



