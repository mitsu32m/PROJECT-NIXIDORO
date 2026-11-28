# WORK-INT-013 — HV-004 / HV-001 / PROTO-001 再現性訂正と候補境界

2026-11-28 10:04 JST開始。Work、正式Claimなし。**NOT ORDER-READY / ハード採用BLOCKED**。

## 正本・差分・契約

live開始HEAD `19660a2a5d2298e384aad49883b95b862fd27fa9`、branch `codex/reva-integrated-prototype-review`。前回Work保存 `bc805d6f9334172dc5423e2c0de41d79221bf094` 以後2commit/2報告: [C-029](2026-11-28-0900-JST-C-REVIEW-029-lamp-source-recheck.md)、[B08:56 LT3751/DA2033](2026-11-28-0856-JST-chatb-lt3751-da2033-evidence-gate.md)。必須6資料を開始SHAで取得。まずCのWork package、次に[Work012](2026-11-27-2202-JST-WORK-INT-012-cutoff-review-and-rs-source-conflict.md)と必要な新Bのみを読む。問いはD-030再現性差戻しと新HVペアの一次証拠境界。全A/BやKiCad再調査を行わず、判断訂正・未レビュー境界・次の実部品課題を同期する。

## 重要訂正: RS655-9413の150µA/95V確定表現を撤回

C-029のCHANGES_REQUESTEDを受け、今回はURLのPDF本体を直接ダウンロードし、ローカルPDFレンダラでp1を描画した。**実バイト列では0.25mA ±10%、T1.25、電圧100/120/220/250V、20000Hrs**。DC striking95V/最大0.15mA表記はこの本体にない。Cの今回観測を独立再現した。250µA自体は設計特性の資料表記、±10%もDC・温度・lot保証としない。DC strike/sustain/許容電流/明るさ/暗所遅延/寿命条件はUNKNOWN。

- URL: https://docs.rs-online.com/da36/0900766b81584987.pdf
- 直接取得: 398686 bytes、SHA-256 `53508b834a6e82888b7b4fa323ce237517582e8ec4a6666a72698896c0af99d7`。
- HTTP ETag `"ddaa42437a2c088aa7071e617e477f1a"`、Last-Modified `Mon, 01 Jul 2024 09:26:20 GMT`。これは製品資料の保証改訂日でない。日付/版の可視表示は確認できない。
- 今回もweb経由のPDF screenshotは150µA/95Vを示す像を返した一方、直接取得本体の描画は250µA±10%。**取得/描画経路の不整合**として記録する。同一URLでメーカーが改訂したと断定しない。前回Work012時点の原PDFバイト列/ハッシュは未記録で、当時の像の由来はUNKNOWN。旧観測を消さず、確定部品仕様としての主張を撤回する。
- **D-030更新:** 「確認済み150対250µAの部品資料矛盾」から「旧観測は本体から再現できず、資料取得再現性・controlled revision/lot・DC適用のHOLD」へ訂正。B13:02のDC strike UNKNOWNを不完全としたWork012の差戻しも、今回本体の範囲では撤回。C-029の資料scopeを採用し、ハード採用はしない。

この訂正は安全解除でない。RS商品ページの250µAと今回PDF値は一致するが、DC適格性・供給/納期・着地価格を満たさない。前回のweb screenshotだけによる確定が不十分だった。今後この争点は直接本体hashと実描画を照合し、同じ曖昧な像の反復で判断しない。hashは同梱[source fingerprint CSV](2026-11-28-1004-JST-WORK-INT-013-source-fingerprint.csv)にも保存。

## C-029の残りの統合範囲

- VCC A1Aの03/17 Rev2 nominal0.5mA/max breakdown95VDCとundatedメーカーhost design0.6mA/90VDCの差、およびPCN333発効2014-01-21のA1A-T限定廃止はCが範囲付き確認。**D-027/028の出典差・suffix範囲をレビュー済みに更新**。bare A1A廃止、実lotのDC寿命/電流適格とはしない。Work008全文をCが独立レビュー済みとはしない。
- B11/25 21:02とB11/27 13:02はC-029で出典/仮定算術を範囲付きレビュー済み。200–205V/16mA仕様、実表示モード、battery net-chargeの採用ではない。C-028停止inventoryの条件付き範囲は維持。D-029追加energy bookkeepingは今回C-029の完全レビュー対象外のまま。
- 価格/在庫は各取得時の表示にすぎず、Cの新stock countも現在在庫保証へ昇格しない。再度の同じ効率感度表は作らない。実測MEASUREDはゼロ。

## 新B LT3751 + DA2033 — Work一次照合と修正（PENDING C REVIEW）

| 出典・条件 | 一次照合結果 | 採否・必要証拠 |
|---|---|---|
| ADI LT3751 datasheet 3751fd pp1,3–4 | p1 feature5–24Vとは別にp3 Electrical CharacteristicsのVCC表は4.75–24V、full-range marker。default VCC/CHARGE5V、CLAMP0。p4Note2でE/I grade保証範囲区別 | **Bの「4.75Vはgate-driver説明のみ」と読める境界は修正**。電気表にもVCC4.75V下限あり。ただし選定suffix未定、最低SYSや5V起動/低下余裕未適格。4.75V以下の1Sを無biasで可とはしない |
| 同p4Note8 | VCC≤8V時LVGATEとHVGATEを並列使用する条件 | 実FET/ゲート電荷/駆動損失と電源条件を回路で確認。内部FAULT/OVLOは独立HV停止/放電保証ではない |
| Coilcraft linked datasheet Doc510-1 Revised03/07/25 p1 | DA2033/34がLT3751にもspecified、DA2033行10µH±10%@0A/9µH min@Ipk5A、1:10。DCRmax一次0.015/二次1.10Ω等は25°C・一次並列等の脚注条件 | メーカーのcontroller互換記載は確認。Ipk5Aは低入力でのpeak/inductance条件、連続RMS/温度rise定格ではない。core/AC copper/熱・working voltageは未適格 |
| 同一次表/用途説明 | 1500Vrms/1min巻線間、750Vrms巻線coreの試験、capacitor charging用途 | 耐圧試験値を連続working voltageやsystem絶縁保証にしない。typ3–24V LT3750用途とLT3751全条件を混同しない |

LT3751に外部FET、DA2033にメーカー互換記載がある点は既存controller-onlyより具体的。しかし**連続205V/16mA適格ペアでない**。新BはC-029が明示deferしPENDING REVIEW。今回Work確認も限定で、正式採用/新verified node追加なし。LT3751/DA2033は未レビュー調査台帳として保持し、Cレビュー後の比較候補昇格を判断する。主電力をSYS直結し別VCC biasを用いる案とSYS→5V案は、bias負荷・損失・起動を含む同境界で比べる必要がある。

出典（2026-11-28取得）:
- https://www.analog.com/media/en/technical-documentation/data-sheets/LT3751.pdf pp1,3–4（p3表画像確認）。新VCC表解釈/grade範囲はCへ差戻し依頼。
- https://www.coilcraft.com/en-us/products/transformers/power-transformers/capacitor-charging/da203x/da2033-al/ （exact DA2033-ALD、表示USD6.06 qty1は着地見積でない）。
- 上記リンク先 https://www.coilcraft.com/getmedia/88ef6a9b-3558-4004-8c5f-af97c95c7e8c/da2032.pdf Doc510-1/2。ページのLT3750 typicalとPDFのLT3751互換記述を分離。

## 全体統合・方式比較・試作判断

| 領域 | 今回の採否/未検証事項 |
|---|---|
| MAX668結合/LT3757/LT8365 multiplier/direct-SYS | 条件付き候補を維持、実磁性/FET/整流/clamp/損失/連続熱/供給ペアなし。通常boost限定不採用を拡大しない。新LT3751は未レビュー比較待ち |
| HV5524/独立OVP/停止/放電/Cmin/Cmax | upstream cut/inhibit/独立組合せはすべて実回路/最大遅延/故障/同一energy/startup/discharge未証明。D-024/029のscope維持、220V推奨をfault目標にしない |
| BQ25185/TPS61023/5V/21700/NTC | 新LT3751 biasも5V起動/最低SYS契約に追加検討。充電別損失/接合/基板/密閉PETG熱、実PCM/holder/NTC取付/故障、充電禁止とBAT-only遮断を別証明 |
| 実IN-12B/ネオン | メーカーpassport/実lot/decimal/current未確定。RS本体再現性を訂正してもDC保証なし。A1A出典差は確認済みでも適用版未定 |
| Pico2/RTC/OLED/UI・PCB/PETG | 提案baseline、3V3/backup/逆給電/停止UIとfault界面、銅箔/EP/via熱抵抗/HV connector/抵抗working voltage/絶縁・cell温度は実測待ち |

全体成立性と安全は未立証。初回≤4万円/予備≥1万円/総額≤5万円も未立証。ランプ2袋2478円や磁性部品USD表示では税送料・PCB・保護・cell assembly・rework込み予算を評価できない。11/15 BOMは歴史値。新保証値/代表値/仮定/実測/UNKNOWNの境界を守り、未レビューを採用しない。12/01方式/電力熱・12/15初回購入判断packageは提案checkpoint維持、2027年1月末より前の初回判断に実型番・段階BOM・国内少量着地額/納期を優先。期限変更/購入承認なし。

## 判断・次課題・ユーザー判断

- D-030を上記訂正、D-027/028はC-029限定出典レビュー済み。**D-031:** LT3751/DA2033は未レビュー調査候補、VCC表4.75V/grade/bias・連続magnetics/熱/working voltageの適格性待ち。回路採用や仕様変更なし。
- A #6/#8/#9: 実stop/latch/cap/energy/timing/fault保証表とcharge/BAT-only温度保護。新bias候補を採用済みとして設計しない。
- B #2/#7: LT3751 exact suffix/VCC/VTRANS startup・FET/rectifier/clamp・DA2033 continuous L(I,T)/RMS/core熱/working voltageと着地見積。RS直接PDF hash/controlled revision/lot/DC情報、実IN12B/cell assembly/段階BOM。同じ理想効率表の反復不要。
- C: 次はdeferされたB08:56と今回VCC表解釈/RS本体hashを限定一括確認。D-029完全レビュー未了、歴史的backlog UNKNOWN。
- 次のユーザー判断: 実候補/金額を揃えてから16mA境界/電圧window/USB表示とnet-charge/LV-first範囲。判断package未完成のため今回承認要求なし。

共有decisions/open-issues/handoffとtech-tree YAML/MDへ同期し、旧Work012/不採用案は保持。既存#2/#4/#7で重複確認、同争点のIssue新設なし。ノード状態/依存は33/52を維持、release locked。書込直前HEAD/共有blob確認、expected_sha保存、全変更再読一致とツリー整合検証。購入/PCB発注/HV印加/mainマージ/回路図・PCB・重要仕様変更/安全承認/タスク停止・頻度変更なし。保存SHA/結果はGit履歴と最終報告。
