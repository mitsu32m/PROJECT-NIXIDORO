# WORK-INT-005 — OVPタイミングと実磁性部品の採用ゲート

日時: 2026-11-24 10:03 JST（開始）。対象: #6 HV-002/SYS-002、#2 HV-001、#7 PROTO-001、関連#4/#8/#9。
正本branch: `codex/reva-integrated-prototype-review`。
開始HEAD: `3453693f7595f015b23ae66a98647191a78b656b`。
前回Work保存: `a91a4e7cfb0785e0ff58ba8cb6b18cc80019d7fb`。live compareで**8 commits / 8 added reports**、共有索引・回路図・BOM変更なしを確認。
役割: Work設計統合。NO FORMAL CLAIM。購入/PCB/HV印加/mainマージ/回路図変更/重要仕様変更/安全承認なし。

## 契約と統合結果

C-025/026のWork判断パッケージから、(1)実TLV6700候補のOVP誤差/電源投入/遅延、(2)CJ5143のreset時間と連続電力、(3)新B09:03のWürth候補を一括統合。終了条件は一次資料と独立計算で採否を分離し、共有索引/ツリーを同期、保存後再読込で検証すること。
**CONDITIONAL: 文書解析と候補探索継続。BLOCKED: 部品/安全回路採用と統合試作Go。** 200〜205V/16mA連続目標、電圧nominal/window・lamp/bus境界の未決状態は変更しない。

C-025はB11/23 21:03とWork004のINFEASIBLE区別を数学範囲で確認した。これまでの「B21:03はC未レビュー」という現状記述を更新する。歴史レポートのPENDING表記は保持。
C-026はA04:00/A08:01/B05:02を対象にした。B09:03はその後の**PENDING C REVIEW**であり、Workによる限定再計算/一次確認をCレビュー完了としない。全履歴backlogはUNKNOWN。

## 一次資料の独立確認と差戻し

確認日:2026-11-24。GUARANTEED=明記されたmin/maxをその条件内で使用、TYPICAL/NOMINAL=代表値、ASSUMED=モデル入力、MEASURED=今回なし、UNKNOWN=未根拠。メーカー典型用途と保証定格を区別。

### TLV6700 — C-025/026のタイミング解釈を修正

[TI TLV6700 SNVSAV2B Rev.B, Nov2019](https://www.ti.com/lit/ds/symlink/tlv6700.pdf) pp5–6を直接確認。**p6を画像化し§7.6脚注(1)とFigure1のINB−/OUTBを目視確認**した。

- §7.6のhigh-to-low / low-to-highは**入力端子**の遷移。INB−が上昇してOUTBがLOWになるOVP assertionは `tPLH=29µs NOM`。18µs NOMの `tPHL` はINB−下降側。C-025の18µsを出力H→Lに対応させる読みに**CHANGES_REQUESTED**。C-026もINB過電圧停止側と18µsを結びつけないよう補足する。
- 条件:VDD5V、input overdrive10mV、Rp10k、指定VOH/VOL。両行MAX空欄。**29µsへの修正でも最大hard-off遅延はUNKNOWN**。他段/電力FETまで含む遅延を保証しない。
- §7.5 positive-going396..404mVは−40..125°C、VDD1.8V/18Vの記載条件。INB−入力電流±15nAは**VI0.1V**条件で、実sense約0.4Vへ無条件保証外挿しない。閾値誤差への二重加算も未確定。
- 起動はVDD>1.8V後450µs MAX（脚注のramp/POR条件を保持）。UVLOでOUTB high-Z、POR未満の出力不定。high-Zをstop assertedとみなさず、無給電default-offを実外付け回路で証明する。

### CJ5143-ALC — 実カタログ値と限界

[Coilcraftメーカー表](https://www.coilcraft.com/en-us/products/transformers/power-transformers/capacitor-charging/cj5143/)を直接確認。25°C条件、L0=15µH±10%、Lmin13.5µH at1.2A、一次/二次DCR max1/25Ω、Llk max0.3µH、比1:15、hipot1000Vrms/1min。**1.2AはL評価条件でありIsat/連続許容電流ではない**。用途はNCP5080 photoflash充電器、2.7–5.5V→350V典型。205V/16mA連続の保証なし。現サイト表示の単価だけでは国内配送税込/在庫保証にならず、着地費UNKNOWN。
C-025/026のハード採用BLOCKEDを維持。DCR最大値を実損失の下限にしない。

### Würth 750315839 — 新B報告の一次証拠を追加

[メーカーPDF revision003.001 /2022-11-10](https://www.we-online.com/components/products/datasheet/750315839.pdf) pp1–2を直接確認し、p1図面を画像で読んだ。
**SOURCE-DOCUMENTED（実回路採用ではない）**:
N1=pin3(dot)–5、N2=7(dot)–8、N3=8(dot)–9。N1:(N2+N3)=1:10。N2/N3の合計比を各巻線に割り当てない。
L40µH±10%（10kHz/100mV）、Isat3.2AはTYPICALかつ|ΔL/L|<20%条件。DCR一次0.085Ω±10%、二次N2+N3=8.4Ω±10% at20°C、Llk max0.5µH（100kHz/100mV）。高電流/高温のL(I,T)/core-loss/連続熱はUNKNOWN。

p2は**Typical Application**として4–36V、50–200kHz、200V/12mA。「50kHz未満だから絶対禁止」という定格ではなく、その条件から外れる今回仮定をメーカー実証点と扱えないという判断。
1500VAC試験だけで絶縁全体を証明しないが、p2に**functional insulation、265Vrms/400Vpeak、OVC II、列挙規格へdesigned to comply**という追加記載がある。「メーカーworking-voltage記載が一切ない」という扱いは修正する。これはbasic/reinforced insulation、安全認証の取得証明、実基板の沿面/空間/筐体適合を意味しない。
図面は入手できたが既存KiCadとの接続/footprint適合を今回確認したとはしない。現国内供給/税込配送価格は未確認。

## 独立再計算（ASSUMEDモデルのみ）

再現コード/CSV: `hardware/integration/work-int-005-ovp-magnetics-audit.py/.csv`。

### OVP静的窓

C-026の仮定:normal static max214.13495V（不完全）、ceiling220V、comparator±1%、ratio541.5、各抵抗独立±r。動的ripple、TC/aging/bias、stop tailは未算入。
- r1%: nominal条件>220.659367Vかつ<213.516273Vで空。**当該分圧案は限定NO-GO**。
- r0.1%: nominal interval216.730158..217.387374V、幅0.657216V。normalized midpoint217.058766Vでtrip214.459623..219.667443V、Cmin仮定1µFの高側energy headroom73.107319µJ。
- Rtop5.415M/Rbottom10kとVref400mVを固定した実名目は217.000V。上記自由Vnのmidpointを同一固定抵抗で実現したと扱わない。この固定例のtrip214.401560..219.607970V。いずれも部品値/threshold採用なし。
- ±15nAを仮に使った入力電流感度は5.415mV/nA、15nAで81.225mVのHV換算。0.4Vにおける保証値ではない。

精密化は静的必要条件を改善するが、dynamic normal max、実Cmin、Etail,max、最大停止遅延、無給電/共通return faultとdischargeが不明。**抵抗0.1%だけでOVP完成という主張は不採用**。29µs NOMを73µJ予算へ保証値として掛け合わせない。

### CJ5143 resetと電力境界

仮定:constant15µH、n15、205V、理想単一pulse fully-reset、deadtime0。境界でton+toff=周期（idle余裕ゼロ）。厳密DCMのpowerはこの境界未満。
`Ipk_max=1/f/[L*(1/Vin+n/Vout)]`、
`Pmag=.5*L*Ipk^2*f`。

| Vin | f | Ipk境界 | Pmag | eta仮定75%のPout |
|---:|---:|---:|---:|---:|
| 3V |100kHz|1.640000A|2.017200W|1.512900W|
| 5V |100kHz|2.440476A|4.466943W|3.350207W|
| 3V |200kHz|0.820000A|1.008600W|0.756450W|
| 5V |200kHz|1.220238A|2.233472W|1.675104W|

5V/100kHzの磁気入力marginは4.466943−3.28/.75=0.093610W、出力marginは0.070207W。B旧0.092Wの丸め/電力境界をC-026通り修正する。3V/100kHzはモデル内で効率100%でも3.28W未満。5V例もIpkは1.2AのL評価条件を超え、L一定と効率は未保証。**限定モデル不成立と、部品/CCM/結合方式全般の不成立を区別する**。

### Würth新B09:03の扱い

仮定constant40µH、Ipk3.2A、n10、完全reset境界でf=20.445/23.924/31.403kHz（Vin3/3.6/5V）、Pmag4.187234/4.899585/6.431373W、必要eta78.333/66.944/51.000%。B丸めを確認。
3V/75%例Pout3.140426Wは目標未達。typ Isatの3.2A、L低下を無視したconstantL、50–200kHz典型外という条件なので、3.6/5Vの数値passも成立証明としない。B09:03はPENDING C REVIEWを保持。
MAX668 fixed-frequencyやLT3757可変周波数とこの仮想boundary-modeは同じ制御契約ではない。原回路がautotransformerならisolated-flyback式を無断転用しない。

## 比較・採否

| 対象 | 今回の判断 | 採用へ必要な証拠 |
|---|---|---|
| TLV6700 +各1%抵抗の当該proxy | 限定不採用 | 他の窓/誤差配分は別審査 |
| TLV6700 +precision chain | 条件付き候補、実装BLOCKED | 実HV抵抗MPN/TC/aging、実sense bias/閾値条件、normal dynamic、default-off latch/無給電、Etail/Cmin/Cmax/放電 |
| CJ5143-ALC | 実型番探索候補、連続採用BLOCKED | 高電流L(I,T)、RMS/core/銅損、実controller/dot/drive/rectifier、stop、少量国内見積 |
| Würth750315839 | 図面/機能絶縁記載を追加、ハードBLOCKED | topology一致の制御周波数/波形/温度/損失・供給、Cレビュー |
| MAX668結合/LT3757 flyback/direct-SYS/LT8365 multiplier | 前回の比較候補を維持 | 新しい適格pair証拠なし。従来ordinary boost却下範囲も維持 |

## 全体成立性・試作と予算

205V×16mA連続目標の成立は未立証。全体Goは不可。500mA USB-onlyの3.28W不足、signed IBAT/USB net-charge、lamp/bus16mA境界、single/dual/switched bleeder台帳はINT-004を継承。C-025の確認を同じ仮説の新成果として重複計上しない。

| 領域 | 現在の未検証事項/次に必要な測定・部品 |
|---|---|
| HV5524/OVP/容量 | 推奨220Vを保持、最大停止/tail、実Cmin/Cmax/ripple/起動/残留、divider/共通return故障、discharge endpoint/timeが必要。60V/5sは未承認例 |
| BQ25185/TPS61023/5V | 低SYS/BATFET/PCM/contact、実L1/Ceff、充電電流別損失/Tj、起動・USB遷移、bleeder込みpower/thermal未適格 |
| 保護21700/NTC/THERM | 実pack/PCM/probe取付/holder、充電禁止とBAT-only負荷遮断、MCU-off・CE短絡・NTC脱落・熱遅れ未検証 |
| IN-12B/neon | 実lot DC strike/holding/current/brightness/同時点灯とrated ballast/short fault未適格 |
| Pico2/RTC/OLED/UI | 提案保持。OE/逆給電/backup/3V3負荷/thermal fault interface、power-off default未検証。仕様/回路変更なし |
| PCB/PETG | EP/copper/via/磁性/抵抗の放熱、実cell/contact温度、沿面/空間/取付・隔離未検証。機能絶縁の部品記載はシステム評価に置換不可 |
| BOM/費用 | 新規実候補の国内着地見積なし。11/15価格は歴史値。初回≤4万円/予備≥1万円/総額≤5万円は未立証、最新総額UNKNOWN |

測定は実候補/安全計画が人間審査された後の課題。switch/diode/winding/bleeder/ballast/ICとcell/PCM/contact、内外ambient温度、起動/無負荷/遮断後電圧、signed BATを評価する必要があるが、今回実測/試験許可なし。
11/25部品証拠、12/01設計判断、12/15初回購入判断packageという提案checkpointを維持し、2027-01末より前の判断を目指す。11/25までに現行pair/保護/見積がなければ不足を明示し、LV-first範囲と代替を具体化。納期/予算達成は約束しない。

## 状態同期と次課題

D-021: TLV候補と1%案限定却下、29µs NOMと最大遅延UNKNOWN。
D-022: magnetics energyとreset/controller/温度を同時成立させる解析要件（ハード採用でない）。
D-023: Würthcontrolled図面/functional insulation記載を部分根拠として記録、working-voltage情報の全面UNKNOWNを訂正。システム適格は未確認。
新ツリー候補HV-OVP-TLV/HV-CJ5143/HV-WE839はalternative、他ノード/依存状態/安全ロック維持。全てに今回根拠を追加しYAML/Mermaidを同期する。

- **A #6:** actual comparator/ref/HV chain/stop-latch候補1式。INB rising→OUTB falling29µs NOMを正しく追跡し、max不明を残す。ramp450µs/UVLO/high-Z/POR/return-open/power-lossを含むdefault-off回路と、Cmin/Cmax/Etail/放電の保証表。既存KiCad変更は具体依頼後のみ。
- **B #7/#2:** CJとWürthのcontrolled L(I,T)/continuous thermalと実controller同一topologyの条件、国内少量税込配送見積か具体除外根拠。Würthworking-voltage/端子図面は今回確認済みを再利用し、同じtyp Isat感度表だけを繰り返さない。
- **C:** Work005の入力遷移/出力極性と29µs NOM訂正、Würth記載/新B09:03を関連batchで審査。メーカー試験点の保証と実装適格を分ける。歴史backlogゼロを主張しない。
- **Work:** 実MPN/保証/見積/回路判断の新証拠がなければ次は短い確認SHAログに留める。

次のユーザー判断は、具体代替/費用が整った時点で16mA境界・200〜205Vwindow、USB時表示/net-charge、段階試作範囲。今回は重要仕様を変えず文書作業を継続する。

## 出典・検証範囲

入力C: [C-025](2026-11-24-0300-JST-C-REVIEW-025-ovp-cj5143-usb-batch.md)、[C-026](2026-11-24-0900-JST-C-REVIEW-026-ovp-bias-cj5143-reset-batch.md)。
必要原本: [A precision](2026-11-24-0400-JST-HV-002-precision-divider-static-margin-energy-screen.md)、[A bias/startup](2026-11-24-0801-JST-HV-002-tlv6700-input-bias-startup-primary-gate.md)、[B reset](2026-11-24-0502-JST-chatb-hv001-cj5143-dcm-reset-time-bound.md)、[B Würth](2026-11-24-0903-JST-chatb-hv001-wurth-750315839-low-sys-boundary-screen.md)。SHAは開始HEADに固定。
旧成果・不採用案保持、#2/#6/#7へ既存課題追記。書込直前ref/blob再確認、一括commit+expectedSHA ref更新、保存後全文再読込とYAML/Mermaid/計算/差分検証を行う。保存後SHAは自己参照を避け最終報告に記す。
