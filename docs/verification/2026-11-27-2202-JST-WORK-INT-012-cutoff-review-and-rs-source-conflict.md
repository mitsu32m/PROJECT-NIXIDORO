# WORK-INT-012 — HV-002/003/004・SYS-002・PROTO-001 統合

2026-11-27 22:02 JST開始。Work、正式Claimなし。**ハード採用BLOCKED / NOT ORDER-READY**。文書のみ。新Work一次照合はCレビュー待ち。

## 契約・最新差分

正本 `codex/reva-integrated-prototype-review`、開始HEAD `4cf29b4284dc5cf297ae2d068c1c8807d726daf1`。朝のWork保存 `ebea7c02e6ce43914d7e089c72410270c104cdc6` から2commit/2報告追加: [B13:02 RS](2026-11-27-1302-JST-chatb-rs6559413-dc-sourcing-gate.md)、[C-028](2026-11-27-2102-JST-C-REVIEW-028-cutoff-energy.md)。必須6文書をHEAD固定で取得し、CのWork判断パッケージを先に使用。[Work008](2026-11-25-2159-JST-WORK-INT-008-neon-revision-and-lifecycle-gate.md)と必要なA04:01/新Bのみ参照。全A/B・KiCadの再調査なし。

問い: 停止エネルギーのレビュー状態を正しく更新し、RS655-9413のDC/供給根拠を採用条件にできるか。終了条件: 一次資料の条件差と新矛盾を記録、採用/候補/不採用/実測待ちを分離、既存#4/#6/#7へ接続。回路変更や試作承認は対象外。

## C-028統合・独立再確認

- **レビュー状態更新:** A11/25 04:01とWork007のTPS22918表解釈・限定算術・D-024はC-028で範囲付きレビュー済み。回路/安全適格ではない。Work008のA1A/PCNとB2件は未レビューのまま。旧pending記述は歴史的状態として保持。
- TI TPS22918 SLVSD76C Rev.C（July2017）p5–6を再取得、p6表を描画確認。2µsはVIN5V/TA25°C/RL10Ω/CIN1µF/CL0.1µF/CT1000pF/QOD open/steady VIN条件の**TYPICAL**、max欄なし。79mΩ **MAX**はVIN5V/IOUT−200mA/−40..105°C条件で、1A保証へ外挿しない。2A absolute/TA70°Cや基準基板θJAは製品連続熱適格を意味しない。
- 今回p13–14 §8.3.2〜.2まで直接確認。QOD抵抗はVIN依存、電源喪失で弱まり得る。p14はinternal QOD直結時の容量上限200µF、超過時外付抵抗、残留chargeを自然減衰させ外部から駆動しない条件を記載。**これは200µF以下なら安全という承認でも、HV放電/逆流遮断/energy分配保証でもない。** 実回路へ流用する前に全条件を確認。
- Cの73.107319µJと下流LV10/22/47µFの80/176/376µJは仮定値。今回独立算術でheadroom73.1073188µJを再現。100%転送は保守的比較仮定で、実HV過電圧の実証でない。10%転送の反例も実機推定でない。等号はmarginゼロ、採用上限にしない。
- **D-029分析要件:** 電圧依存容量は同じnode/時点/電圧範囲で差分エネルギーを積分（dW=V dQ、Cdiff=dQ/dV）又は保守境界化。一般的なCeffの単一点をCdiff(V)保証へ変換しない。trip前供給分とcut時蓄積分を二重加算せず、磁気/別給電/最大遅延/伝達経路・strict margin・同一HV Cmin/Cmax/startup/dischargeを揃える。実部品曲線/最大転送はUNKNOWN。

## 新B RS PRO 655-9413 — 新たな一次資料矛盾

| 根拠 | 記載・分類 | Work判断 |
|---|---|---|
| RSブランド日本商品ページ | 電流250µA、寿命20000h、1袋10個1126円税別/1239円税込。LISTED、条件未保証 | 2袋2478円税込/20個（12使用なら8予備）は表示価格計算のみ。送料/現納期/lot UNKNOWN |
| 同ページData sheetリンクのRS PDF p1 | exact stock655-9413、striking max AC65/DC95V、operating current(max)0.15mA、寿命≥20000h、抵抗案はAC100–120/220–250V用 | **新発見:**250µA掲載と150µA max表記の資料差。条件/改訂適用不明、0.15mAでも0.25mAでもDC設計値へ採用しない。DC striking情報は全てUNKNOWNとの解釈を訂正。ただしDC維持/明るさ/電流範囲/温度/寿命/lot適格はUNKNOWN |
| 今回取得した日本ページ | 在庫情報にアクセスできない表示。web取得側には古いcrawl表示あり | Bの国内110/海外3160は歴史的表示snapshotに限定。ライブ在庫保証でない。stock/配送確認未成立。販売状態変化/欠品と断定もしない |

PDFはブランド自身のexact-part資料だが、版適用/条件と商品ページの矛盾が解消されていない。抽出テキストは表を落としBNC cableのtemplate残骸も含むため、PDF表を画像で確認した。商品ページの抵抗説明/Warningも整合せず、そのまま205VDCへ転用しない。今回のRS PDF発見は**PENDING C REVIEW / CHANGES_REQUESTED to B evidence completeness**。新MPNの正式採用やverified node追加なし。Bの候補は調査待ち台帳だけに保持する。

### 一次出典（2026-11-27再取得）

- TI: https://www.ti.com/lit/ds/symlink/tps22918.pdf pp5–6,13–14。数値保証は当該試験条件に限定。
- RS日本brand-owner listing: https://jp.rs-online.com/web/p/indicator-lamps/6559413 。価格は参考表示で、現見積でない。
- 同ページリンク先RS datasheet: https://docs.rs-online.com/da36/0900766b81584987.pdf p1（表を目視）。現納入版への適用UNKNOWN。
- Bのint.rsdelivers英語ページは今回403で再確認不可。AXEL/Monotaro/IN12B二次販売者の全件再調査はせず、Bの未レビュー観測として保持。

## 方式比較・全体成立性・部品/測定

| 対象 | 採否・条件・不足 |
|---|---|
| 停止方式 | upstream cut、controller inhibit、独立組合せの3候補。upstreamのみでは下流cap/磁気/逆給電が残る。inhibitのみでも残留energyあり。組合せも共通原因・switch short・stuck-high・power loss/latch/最大停止が未証明。TPS22918代替候補のまま |
| HV200–205V/16mA | 未変更目標。MAX668結合、LT3757 flyback、LT8365 multiplier/direct-SYS比較を維持。実CJ5143/Würth磁性/FET/整流/clamp/損失/連続熱/供給の適格pairなし。通常boost限定不採用を他方式へ拡大しない |
| HV5524/OVP/放電/C | 220V推奨をfault目標にせず、正常dynamicとtrip/tailのstrict margin、無給電/共通return故障、同じCmin/Cmax・起動/放電の実部品証拠待ち |
| BQ25185/TPS61023/5V・セル/NTC | 最低SYS/起動/電流/充電別損失と接合/基板/筐体熱未適格。実保護21700/PCM/holder/NTC取付と遅れ/故障、充電禁止とBAT-only負荷遮断を別証明。CE=GND現draft変更なし |
| IN-12B/ネオン | IN12B二次値をメーカーpassportにしない。実lot/decimal/current未確定。RS新資料差/A1A資料差ともHOLD |
| Pico2/RTC/OLED/UI | baseline提案保持。3V3負荷/RTC backup/逆給電/OE/BLと停止UI・fault界面のLV実測待ち |
| PCB/PETG/BOM | 実EP/copper/via熱抵抗、HV抵抗working voltage/connector/絶縁距離、密閉cell温度を検証待ち。実型番/納期/着地費用未充足 |

Bの250µA/neon仮定に基づくPbus2.139912W、direct入力2.853216W、cascade3.170240Wは今回算術再現したが**ASSUMED**（205V,2digits×3mA,12neon×0.25mA,dual285k,η.75/.9、divider/driver等除外）。新PDFとの電流矛盾でDC適格性は増していない。この条件でもUSB理想2.5Wを上回る。USB+BATは放電し得て、実BAT電流/熱/充電保証ではない。効率やRS電流を変えた反復表は作らない。実測は今回ゼロ。

## 初回試作・予算・次課題

初回≤4万円/予備≥1万円/総額≤5万円は引き続き未立証。2478円はランプ2袋の表示価格だけで送料・PCB・HV/保護・cell assembly・reworkを含まない。安いlistingを根拠に予算成立や購入可としない。11/15 BOMは歴史値。11/25部品証拠checkpointを充足に更新できない。12/01方式/電力熱、12/15初回購入判断packageは提案のまま、2027年1月末より前の判断に向けLV-first/独立HVの段階BOMと実納期/着地額を優先。

- **採用:** D-024の分析要件はC-028限定確認済み、D-029はそのenergy bookkeeping補強。ハード採用なし。D-026 TPS22918は条件付き代替候補、D-030 RS資料差/DC調達HOLDを記録。実測待ち/不採用枝は保持。
- **A #6/#8/#9:** 実比較器/ref/divider/latch/cut/discharge候補一式、per-node Cdiff/保証境界とtrip/cut時点、故障最大energy/timing/温度・inrush。3停止方式を同じ負荷/部品で比較し、同じ仮定RC表を再提出しない。
- **B #4/#7/#10:** RS150対250µAの適用条件・現行版/lot/DC operating/寿命を解消、又は現行代替1型番。実IN12B/cell assembly/連続HVペアと現少量見積/納期をまとめる。未レビュー候補の正式BOM化なし。
- **C:** C-028でA04:01/Work007は限定review済み。次はB11/25 21:02、B11/27 13:02、Work008と今回RS PDF/補強を一括確認。未完了を完了扱いしない。歴史的backlog UNKNOWN。
- **ユーザー判断:** 具体的候補/金額を揃えてから16mA境界、電圧window、USB表示/net-charge、LV-first範囲を提示。今回は購入・PCB・HV・main・重要仕様変更・安全承認なし。回路図/PCB変更なし、タスク停止/頻度変更なし。

## 同期・検証

decisions/open-issues/handoffとtech-tree YAML/MDを同期し、状態/依存は33ノード/52辺を維持、release locked。既存#4/#6/#7を重複確認し差分のみ追記、Issue新設なし。共有ファイルは書込直前live HEAD/blobを再確認、expected_sha保存し、保存後全変更ファイル再読一致とYAML/MermaidのID/label/status/依存/DAGを検証する。旧報告と不採用案保持。保存SHA/実行結果はGit履歴と最終報告に記録。
