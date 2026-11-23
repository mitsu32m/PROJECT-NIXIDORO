# Handoff — PROJECT-NIXIDORO

Current snapshot: **2026-11-23 JST**. Examined HEAD: **4752f388ba7e55a509a84cbdc8ad8c6d8a88ce87**. 正本は作業ブランチのlive HEAD。前回統合保存1e053400d2bcf70e57b63f7ba19dcbd8659a8582から72件のresearch/review追加。会話やこのSHAを永久最新としない。

## Current Work decision package

[WORK-INT-004](2026-11-23-2201-JST-WORK-INT-004-power-discharge-topology-integration.md) integrates C-007〜024; original reviews preserved. **Analysis requirements adopted; hardware/parts adoption BLOCKED / NOT ORDER-READY.** B 11/23 21:03 is still PENDING C REVIEW; Work independently checked only its arithmetic.

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
- **C:** Work004とB21:03の限定再計算/一次条件/INFEASIBLE表現を確認。実回路保証/fault pathを優先。歴史的review backlog UNKNOWN。
- **Work:** 新MPN/保証/見積/実回路判断がなければ大型再調査せず確認SHAを短く保存。

## Prototype, budget and owner decisions

D-014 staged LV-first planning retained; no purchase/test authorization. 11/15価格/在庫は歴史値。初回≤40k/予備≥10k/総額≤50kは未立証、現着地額UNKNOWN。旧BOMは保持。11/25部品証拠、12/01方式/電力/熱、12/15初回購入判断packageは提案checkpoint。期限2027-01末前の判断を優先する。
具体費用/代替を揃えてから、16mA境界/電圧window、USB時net-chargeと表示動作、段階試作範囲をユーザーへ提示。重要仕様変更、購入/PCB/HV/mainマージ/安全承認は禁止のまま。

## Historical evidence

[INT-003](2026-11-19-work-integration-003.md), [INT-002](2026-11-18-work-integration-002.md), [INT-001](2026-11-17-work-integration-001.md) retained. INT-003限定Rs/Rp比証明はC-007で数学範囲レビュー済み。旧handoffはGit履歴に保持。旧schedule観測を現在の実行能力としない。本統合でautomation照会/変更なし。
