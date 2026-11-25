# WORK-INT-008 — HV-004 / BOM-001 ネオン資料版・型番別ライフサイクル統合

日時: 2026-11-25 21:59 JST（開始）。Workによる限定統合、正式Claimなし。**BLOCKED / NOT ORDER-READY**。新しい一次資料照合はCレビュー待ち。購入・PCB・HV印加・mainマージ・安全承認・仕様/回路変更なし。

## 契約と差分

- 正本: `codex/reva-integrated-prototype-review`、開始HEAD `c3bda46b3a1a63a6a77f6e0ba431fc32028a9522`。
- 前回Work保存 `4b97c93eaff705fb58d710368262db6e1eed3aea` から1commit/1追加ファイル: [B 21:02](2026-11-25-2102-JST-chatb-hv004-vcc-a1a-source-conflict.md)。新Cなし。
- SOP、handoff、open-issues、decisions、tech-tree YAML/MDをHEAD固定で確認。まず最新[C-027](2026-11-25-0301-JST-C-REVIEW-027-ovp-wurth-lt8365.md)と[Work007判断パッケージ](2026-11-25-0956-JST-WORK-INT-007-cutoff-energy-and-current-gates.md)を使用し、新Bだけ原報告へ遡った。A/B全回・KiCad再調査なし。
- 問い: A1AをDCネオンの確定負荷・発注部品にできるか。終了条件: 資料版、電気量、型番suffix、廃止範囲、見積鮮度を分離し、必要証拠を既存#4/#7へ接続する。新しい一般的方式比較の反復はしない。

## 新事実・矛盾・修正（一次資料を独立確認）

| 資料・ページ | 記載 | 分類と今回の扱い |
|---|---|---|
| S1 メーカー作成family PDF、販売店ホスト、03/17 Rev2、p1 | A1A rated nominal current 0.5mA、maximum breakdown 65VAC/95VDC。A1A-Tは0.5mA、65VAC/90VDC | 電流はNOMINAL/TYPICAL、最大breakdownは資料記載上限。ただし納入lotへのGUARANTEED適用はUNKNOWN。Bの「版/日付不明」を修正 |
| S2 メーカーホストfamily PDF、版/日付表示不明、p1 | A1A design current 0.6mA、maximum breakdown 65VAC/90VDC。A1A-Tも0.6mA、65VAC/90VDC | design currentは保証最大電流でない。S1と同一型番の資料値が異なる。ホスト/取得時刻だけで新旧・優先版を決めない |
| S3 メーカーPCN333、p1/p25 | 発行/発効2014-01-21、OBS。リストにA1A-T、代替欄空白 | A1A-Tの廃止を文書確認。bare A1Aまで廃止と拡張しない。URLの2024/10は通知発行日でない。現流通在庫/代替供給はUNKNOWN |
| B引用DigiKey販売情報 | Voltage Rating 90VDC、NRND、在庫/価格 | メーカーmax breakdownとgeneric voltage ratingは同一条件の量と未確認。販売表示だけで同一量の矛盾と断定しない。今回直接ページ403、検索cacheは現時点見積でない |

S1とS2の実資料差が新しい判断対象。NE-2相当という分類もDC維持電圧・電流・寿命・実lot保証を代替しない。S2の寿命注記は原則AC、同じDC/RMS電流でDC寿命は約60%との記述であり、実際の本機DC寿命保証へ転用しない。**実測値は今回ゼロ**。IN-12Bの実lot・電流も新証拠なし。

### 出典（2026-11-25取得、PDFを描画して表/日付/suffix確認）

- S1: [VCC Neon Indicator Lamps, 03/17 Rev2](https://www.mouser.lt/datasheet/2/423/visu_s_a0002921483_1-2286113.pdf) p1–2（メーカー著作、販売店配布。付属販売資料をメーカー表と混同しない）。
- S2: [VCC Neon Indicator Lamps, pages 7/8](https://vcc.co/_pdf/Neon%20Indicator%20Lamps_7_%26_8.pdf) p1。メーカー移転先vcc.coで取得。版/発行日UNKNOWN。
- S3: [VCC PCN333](https://vcc.co/wp-content/uploads/2024/10/PCN_333_CML-LAMPS1.pdf) p1、印刷p25。A1A-T行を目視確認。
- 販売情報: 新B記載URL/取得条件を保持。cached NRNDはメーカーbare A1A EOL保証でない。現見積・税送料・納期はUNKNOWN。

## 方式比較・採否とシステム統合

| 対象 | 現判断・採用条件 |
|---|---|
| A1A / A1A-T /他NE-2代替 | A1Aは資料適用・DC使用・供給HOLD。A1A-Tは廃止文書あり、新規設計の確定BOMへ採用しない。旧候補を削除せず現行代替の同条件資料/見積を要求。電流0.5/0.6mAどちらも確定しない |
| MAX668結合 / LT3757 flyback / LT8365 multiplier / direct-SYS | 条件付き比較候補、採用ゼロ。CJ5143/Würth750315839を含む実磁性部品のL(I,T)、pin/dot、controller適合、FET/整流/clamp/銅鉄損/連続熱/供給が未適格。通常boostの限定不採用を別方式へ拡張しない |
| HV5524・独立OVP/停止/放電・容量 | 推奨220Vをfault目標にしない。C-027の29us NOM訂正は維持、max停止不明。TPS22918は研究候補。下流LV Ceff/磁気/別給電/遅延を含む同一HV Cmin/Cmax、起動・残留エネルギー/無給電放電の証明待ち |
| BQ25185 / TPS61023 / 5V | 205V×16mA=3.28W > USB5V×500mA=2.5Wは維持。実効入力電流/補助電池/最低SYS/起動/損失/熱が未証明。Bの仮定効率例は実効率・実電池電流でない |
| 保護21700 / NTC /温度 | PCM付きセルだけで温度保護完了にしない。実型番/holder/NTC接触・遅れ/断短絡、充電禁止とBAT-only負荷遮断を別証明。CE=GND回路は変更しない |
| Pico2 / RTC / OLED / UI | 提案baseline保持、OE/BLは安全絶縁でない。3V3負荷/RTC backup/逆給電/起動停止UIとfault界面のLV検証待ち |
| PCB / PETG筐体 | EP/銅箔/via熱抵抗、HV抵抗working voltage・connector・絶縁距離、密閉時電池温度/熱遅れの測定待ち。資料差を放熱成立と誤認しない |

Bの2digits×3mA+12neon×0.5mA=12mAは**ASSUMED**。参考に0.6mAへ置くと12球分が1.2mA/205Vで0.246W増えるが、これは資料差の影響の説明のみで新負荷仕様/測定でない。breakdown上限はDC維持電圧でないため、ballast抵抗/損失をこの数値だけで決めない。16mAがlamp-onlyか全HV busかはユーザー判断未了。

## 全体成立性・試作・費用

本日の追加証拠は「確定ネオン型番を増やした」成果ではなく、資料適用とsuffix別調達ゲートを具体化した成果。全体成立性・安全・予算は引き続き未立証。初回≤40,000円/予備≥10,000円/総額≤50,000円は目標維持。11/15 BOMを現在見積として使わず、Bの12球1,326円税別/1,458.60円税込という計算もcached単価・送料別の参考に留める。

11/25部品証拠checkpointはこの開始HEAD時点でも未充足。これは全日失敗断定や期限変更でない。12/01方式/電力熱、12/15初回購入判断packageは提案のまま、2027年1月末より前に判断できるよう、LV-first段階BOMと独立HV試作BOMの実型番・不足品・着地価格/納期を優先する。金額/範囲未確定の購入承認は求めない。

## 判断・ツリー・次課題

- D-027: **採用するのは資料適用の分析要件**。A1A実電流/DC条件/適用版/lot未確定、0.5mAや95VDCを製品保証へ昇格しない。新Bの版不明と販売電圧の比較表現は根拠付き修正、原報告保持。新Work照合はC独立レビュー待ち。
- D-028: A1A-T廃止は文書確認、bare A1Aへ一般化しない。suffix別ライフサイクル/代替実型番/現見積をBOM採用条件とする。ハードウェア採用なし。
- HV-004 / SYS-001 / BOM-001 / PROTO-001へ証拠と未解決条件を同期。ツリー33node/52edgeの状態・依存を維持、release locked。旧成果/不採用枝を保持。
- **A (#4/#6/#8/#9):** 実ランプ/ballastが決まり次第、同じ負荷台帳へ反映。今は実OVP/stop/latch/cap保証表と故障経路を優先、仮定RC表の反復は不要。
- **B (#4/#7/#10):** A1A納入版/DC動作/寿命/型番別メーカー状態、又は現行代替1型番の同条件一次資料・現見積。実IN-12B lot、cell/PCM/holder/NTC、連続HVペアと段階BOMを優先。全候補の無差別再探索はしない。
- **C:** 新B21:02+本Work資料差/PCNのscopeを一括独立確認。未レビューA04:01/Work007の停止エネルギーも残る。C-027で新Bまでレビュー済みとはしない。
- **次のユーザー判断:** 実価格/回路候補/電力代替を揃えた後、16mAの境界、200–205Vの意味、USB時の表示とnet-charge、LV-first試作範囲を提示。今回重要仕様を変更せず、判断可能な購入パッケージ未完成。

## 保存・検証方針

共有5ファイルは書込直前にlive HEAD/blobを再確認し、変更時は再統合する。単一commitをexpected_sha付きで反映、保存後7ファイルを再読し一致確認する。YAML/Mermaidの全ID/label/status/依存と参照先を検証。既存Issues #4/#7の本文・コメントを確認し、重複Issueを作らず今回の差分のみ追記する。保存SHA/実行結果は最終報告とGit履歴で確認できる。
