# WORK-INT-014 — HV-001 / SYS-001 / PWR-001 電源境界統合

2026-11-28 22:03 JST開始。Work、正式Claimなし。**NOT ORDER-READY / ハード採用BLOCKED**。

## 正本・差分・契約

branch `codex/reva-integrated-prototype-review`、live開始HEAD `430e259e55fae51aacdc7b8663077f1da73fdc76`。前回Work保存 `21a794a5a9353e2a837fc9c3eeb111876b209b98` から2commit/2追加報告: [C-030](2026-11-28-1500-JST-C-REVIEW-030-lt3751-da2033.md)、[B21:03](2026-11-28-2103-JST-chatb-low-vin-controller-screen.md)。必須6資料を開始SHA固定で取得。CのWork packageを先に読み、[Work013](2026-11-28-1004-JST-WORK-INT-013-rs-reproducibility-and-lt3751-boundary.md)と必要な新Bのみ照合。回路図/PCB・全A/Bの再調査なし。

問い: LT3751の2電源下限を成立条件へ反映し、新低VIN探索を未レビューのまま区別する。終了条件は一次資料でC訂正を独立確認、条件付き候補だけ索引化し、実型番/起動/損失熱/供給課題へ接続。仕様変更・実機試験・購入承認は対象外。

## C-030統合と重要修正

1. **D-031:** B08:56とWork013のLT3751 VCC4.75V表/grade、DA2033互換/測定条件はC-030で限定レビュー済み。LT3751/DA2033を**レビュー済み比較候補**へ昇格する。正式ハード採用、連続205V/16mA適格、発注可ではない。
2. **Work013差戻しを受け入れ:** LT3751はVCCだけでなく、**VTRANSも最小4.75V**。別VCC biasだけで低電圧1Sのトランス主電力をSYS直結できるとの成立根拠はない。前回の「SYS直結＋別biasを比較」は**メーカー範囲未対応の調査案**へ限定し、同等に成立候補と扱わない。新BもC訂正を受け入れている。1S仕様やHV目標は変更しない。
3. 直接メーカーPDF本体を再取得し、印刷p7 RVTRANS pin説明のVTRANS下限4.75Vをローカル描画で確認。p3表もVCC/RVTRANS4.75Vを記載。RVTRANSはsense pinで、VTRANS電源自体の最低条件の根拠はp7本文を優先し、sense-pin電圧と電源電圧を混同しない。VCC grade条件はp4Note2の範囲内。
4. 5V nominal−4.75V=0.25Vは**仮定nominalとの差**だけ。TPS61023出力誤差/配線・cut switch/リップル/起動・負荷過渡/温度の保証下限が4.75Vを下回らない証拠が必要。5V段を経る損失熱、起動CmaxとHV Cmin/Cmax、停止残留energyを同じ負荷境界で評価する。

一次出典: https://www.analog.com/media/en/technical-documentation/data-sheets/LT3751.pdf 3751fd pp3–4,7。2026-11-28今回直接取得651358bytes、SHA256 `51f55e0aa25cce8150483da86c0eb839a3d2093575495f7114a451c5b9f7ccda`（朝のfingerprintと一致）。**GUARANTEED**は当該表/grade/条件に限り、実SYS/5Vの保証ではない。C-030のDA2033 continuous RMS/core/AC copper熱・working voltage・起動/OVP/着地見積HOLDを維持。磁性5Aはpeak特性条件、耐圧試験は連続使用定格へ昇格しない。**D-032:** cold start、running、VCC/bias、VTRANSを別々に保証する分析要件。

## 新B低VIN探索の位置付け（PENDING C REVIEW）

| 方式/候補 | 今回の根拠・区別 | 採否 |
|---|---|---|
| LT3751＋DA2033、条件を満たす安定化電源経路 | C-030限定出典レビュー済み。VCCとVTRANS双方の下限、5V起動/過渡余裕・連続熱が必要 | 比較候補。主電力1S直結＋別VCCのみの成立主張は根拠不足として除外、部品全体を不採用とはしない |
| MAX668結合 / LT3757 / LT8365 multiplier / direct-SYS | 既存の条件付き比較。各実トポロジー/磁性/FET/整流/損失熱/停止/納期は未適格 | 維持。通常boostの限定不採用を他方式へ拡張しない |
| LM5155/LM51551 | 新Bは未レビュー。WorkはTI SNVSB75E Rev.E **August2023** pp1,3,6,14を限定確認。BIAS=VCC直結は2.97–16Vの推奨動作範囲、内部VCC regulator使用時BIAS3.5–45V。1.5Vは別BIAS条件のboost主電力側で、無条件flyback cold-start値でない | 未レビュー探索台帳のみ。Bの「通常3.5V」を全給電構成へ一般化しない。p6UVLO rising2.75/2.85/2.95Vは表のmin/typ/maxであって実起動余裕でない。実low-gate-drive FET/磁性/連続熱/停止証拠待ち |
| LT8301 / LT8302 | Bのcatalog switch値と仮定効率による探索、C未レビュー。LT8301の1.2Aを保証peak上限として部品不採用にしない。LT8302も実電気表/波形/熱/供給未確認 | 正式候補node化/採用/全負荷不採用なし。Bの優先度仮説に限定 |

TI一次出典: https://www.ti.com/lit/ds/symlink/lm5155.pdf 。p6推奨範囲脚注は推奨動作とElectrical Characteristics保証条件を区別。LM51551のみhiccupはp3 device tableで確認。新Bのpage日付May09をdatasheet版日付として採用せず、PDFはRev.E August2023。今回の追加照合は**PENDING C REVIEW**。LT8301旧候補URLのPDF直接web取得は不可だったため、同ICの表/定格は今回独立確認済みとしない。全候補の再探索/同じ効率表反復はしない。

## 電力・熱・本体成立性

205V×16mA=3.28W目標は未変更、5V×500mA=2.5Wより大きい。USB-only全出力不成立、USB+BATは放電し得る。新BのηHV=.75/η5=.9やSYS3.0Vからの電流は**ASSUMED**で、実BAT下限/充電保証/部品接合熱の保証値へ昇格しない。signed BATとUSB→SYS損失、bias、CTRL、bleeder/divider/driverを含む同一境界を維持。16mAがlamp-onlyかbusかは未決のまま。

| 統合領域 | 未検証事項/採否 |
|---|---|
| HV5524/独立OVP/停止/放電・容量 | 上流cut/inhibit/独立組合せ、実latch/最大遅延/共通原因・短絡・無給電・別給電、同じ実Cmin/Cmax・起動/残留energy待ち。D-029完全Cレビュー未了。220V推奨をfault目標にしない |
| BQ25185/TPS61023/5V | 充電電流別損失/JT、最低SYS・実L1/current/Ceff・5V負荷過渡と新4.75V条件、基板放熱/起動余裕待ち |
| 保護21700/NTC/充電禁止/BAT-only温度 | 実cell/PCM/holder/NTC装着/遅れ/断短絡・ヒステリシス、充電と電池単独load cutを別証明。CE=GND回路変更なし |
| 実IN-12B/ネオン | passport/lot/電流/decimal/DC寿命未確定。RS訂正維持、C-030は直接hash再検証をdefer。旧150µA/95Vを復活させない。A1A出典差とsuffix限定PCNも実lot保証でない |
| Pico2/RTC/OLED/UI | baseline提案維持、3V3外部負荷/backup/逆給電/起動停止UI・fault界面をLV測定待ち |
| PCB/PETG/絶縁 | 実EP/copper/via熱抵抗、HV抵抗/connector working voltage・距離、密閉筐体内cell温度/熱遅れを検証待ち |

**MEASUREDゼロ**。全体成立・安全未立証。初回≤4万円/予備≥1万円/総額≤5万円も未立証。実FET/整流・磁性/保護/cell assembly/PCB/rework・税送料・納期を含む着地段階BOMなし。メーカー互換や低VIN見出しだけでbudget/order-readyとしない。11/15 BOM/過去listingは歴史値。12/01方式/電力熱、12/15初回購入判断packageは提案のまま、2027年1月末より前の判断に必要な実部品/見積を優先。

## 同期・次課題・ユーザー判断

- D-031をC-030レビュー済み比較候補へ更新、D-032両電源/cold-start/running境界要件を記録。ツリーにLT3751/DA2033**alternative**を1node追加、HV-DR依存のみ。新verified hardwareなし、release locks保持。低VIN新Bは未レビュー台帳で、採用nodeを作らない。
- A #6/#8/#9: 実stop/latch/Cmin/Cmax/energy/faultと温度保護、5V最小・起動/過渡保証。LT3751直SYS＋別biasを成立済みとして進めない。
- B #2/#4/#7/#10: 同じ供給・負荷・停止条件で実controller suffix/FET/rectifier/磁性1組と損失/連続熱/working voltage/着地見積。LM5155はcold/run/BIAS/gate、LT830xは定格vs電流limit min/maxと実トポロジーを揃えてCへ。部品列挙/仮定効率反復を進捗にしない。
- C: 新B21:03とWorkのLM5155限定照合、D-029、RS原PDF hashを限定batch。B08:56/Work013のLT3751/DA2033範囲はC-030済み。歴史的backlog UNKNOWN。
- ユーザー判断: 実候補/金額を揃えてから16mA境界/電圧window/USB表示とnet-charge/LV-first試作範囲。今回具体的購入package未完成のため承認要求なし。

共有5文書は書込直前live HEAD/blob再確認、競合は再統合。日時固有報告と単一expected_sha保存、全変更再読一致、YAML/Mermaid全ID/状態/依存/DAGを検証。既存#2/#4/#7へ差分追記、重複Issueなし。旧成果/不採用枝保持。回路図/PCB/重要仕様変更、購入/PCB発注/HV印加/mainマージ/安全承認、タスク停止/削除/頻度変更なし。保存SHA/実行結果はGit履歴と最終結果。
