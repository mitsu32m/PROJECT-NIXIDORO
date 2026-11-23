# WORK-INT-004 — 電力・放電・実磁性部品の横断統合

日時: 2026-11-23 22:01 JST（統合開始）。対象: HV-001〜004 / SYS-001〜002 / PWR-001〜002 / BAT-001 / THERM-001 / PROTO-001 / CTRL-001。
正本: `codex/reva-integrated-prototype-review`。
開始HEAD: `4752f388ba7e55a509a84cbdc8ad8c6d8a88ce87`。
前回統合保存コミット: `1e053400d2bcf70e57b63f7ba19dcbd8659a8582`（INT-003の記載した検討開始SHAとは区別）。比較: **72 commits / 72 added report files**。前回保存後に共有索引・回路図の変更なし。
役割: Work統合責任者。NO FORMAL CLAIM。既存 #2/#4/#6/#7/#8/#9/#10 に統合し重複Issueを作らない。

## 契約・結論

C-007〜024の判断パッケージを入口に、関連する電力・放電・温度保護・磁性部品の争点を一括処理する。必要な原文はA 11/23 16:02・20:00、B 21:03、既存BOMのみ追加参照。終了条件は相互矛盾の修正、根拠クラスと採否の明示、索引/ツリー同期と保存後再読込。新しい回路図/PCB変更、購入、HV印加、mainマージ、仕様変更、安全承認は範囲外。

**統合分析要件は採用。実部品/方式採用と全体試作リリースはBLOCKED / NOT ORDER-READY。** 200〜205V / 最大16mA連続は変更しない。「16mA」がランプ合計かHVバス総量かは未決であり、暗黙に補助電流を足し引きしない。数式のレビュー完了は実装成立の証明ではない。11/23 21:03 BはC-024後の未レビュー成果として保持し、Workが独立再計算した範囲のみ分析に用いた。Cによる当該追加レポートのレビュー完了とは主張しない。

## 1. Cパッケージの統合範囲

| C | 統合する内容 | 留保・差戻し |
|---|---|---|
| 007/008 | 限定Rs+(Rp||NTC)比の不可能証明、充電/負荷/HV残留の機能分離、NTC脱落の不可観測性 | 比の証明は指定回路・名目値のみ。PCM/実回路/取付け未適格 |
| 009/010/011 | CE閾値条件、MCU電源由来pullupの反例、電圧基準点とUSB電力の修正 | EVM文言は今回も直接PDF取得失敗。IC内部pull-down保証へ昇格しない |
| 012/013 | LT3757一次典型回路と磁性部品供給リスク、Cmin/Cmax共同制約 | 古いTDK在庫/MOQは現見積でない。EOLはCの流通証拠でありメーカーEOL通知を再確認したとはしない |
| 014/015/016/017 | LT8365通常boost除外、multiplierは継続候補、限定isolated-DCM計算と数値訂正 | DCM/BCMモデルを実MAX668結合方式へ転用しない。5V switch peakは未証明 |
| 018/019/020/021 | ADI実験先例、FET/diode/漏れ/銅損の限定計算、BQ supplement、K/R区別、1:1磁性部品除外 | 77%やIp=2.3Aを205Vの保証効率/実測遮断ピークにしない |
| 022/023/024 | 放電公差/単一openと連続熱、ballast/全体熱、USBモードとbleeder不整合 | 「neon最大0」はdigit単独の可否を別判定。仮定の60V/5sを安全基準にしない |

原レビューを削除/書換えない。C-014のcap-spread表、C-015のBCM/DCM数値訂正は原レポートにリンクしたまま保持し、誤った旧値を設計入力へ採用しない。全履歴の未レビュー件数はUNKNOWN（網羅的Claim監査未実施）。

## 2. 今回独立確認したメーカー一次資料

全て確認日2026-11-23。GUARANTEEDは該当表の試験条件/温度/grade内のmin/max、TYPICALは代表値、ASSUMEDは解析入力、MEASUREDは今回なし、UNKNOWNは未根拠。メーカー掲載典型回路/実験は製品性能保証とは区別する。

| 出典 | 確認内容とクラス | 設計上の扱い |
|---|---|---|
| [TI BQ25185 SLUSF65B Rev.B](https://www.ti.com/lit/ds/symlink/bq25185.pdf) pp4–8, §6.3.2/3 p15, §6.4 p19 | CE active-low。VIL max0.4V/VIH min1.3VはVPULLUP=1.8V条件。500mA設定ILIM min/typ/max=450/475/498mA、VIN=5V。RON_BAT typ/max115/140mΩはVBAT=4.5V, IBAT=400mA。VBSUP1/2=40/20mVとBUVLO=3VはTYPICAL。BAT-only TS=No。supplement currentは非regulate、BATOCP有効 | 450mAを供給保証としない。low-cell大電流に140mΩを保証外挿しない。/CEは充電停止用。充電減少→0→supplementを確認、signed IBATと温度はUNKNOWN |
| 同TI p5/p8 | IN以外5.5V絶対最大、CEの浮遊high保証/充電開始に対するpullup ramp先行保証は当該記載で未証明 | 生VBUSから無制限pullup不可。5.7V到達は未確認の条件付き反例。EVM URL通常/日本語版は取得エラー、検索抜粋は回路保証へ採用しない |
| [MAX668/MAX669 Rev3](https://www.analog.com/media/en/technical-documentation/data-sheets/MAX668-MAX669.pdf) pp2–4 | ROSC500k±1% 85/100/115kHz（0..85°C、全温度表でも85/115）。ROSC200k全温度222..278kHz。max-duty min87%は200k、500kでは86%。shutdown70µsはTYPICALでmaxなし | 100kHzを保証下限としない。40µH fully-reset isolated DCMの限定不成立は結合方式全般を除外しない。Etail,max不明 |
| [ADI 2002-07-04記事](https://www.analog.com/en/resources/technical-articles/small-highvoltage-boost-converters-guide.html) Experimental Comparison | Sumida CMD-8LN 6313-T036, Lp5.6µH, Ip2.3A, 1:9, Rp0.5Ω。150V/25.5mA 77%、別diode/Cで330V/9.6mA 60%はメーカー記事の実験報告 | Ipの測定定義なし。205V/16mA保証なし。効率転用不可。図9の端子/巻線dotと実磁性図面の突合せ未実施 |
| [Coilcraft Q4434](https://www.coilcraft.com/en-us/products/transformers/power-transformers/power-converter-transformers/q4434/) / [Q4435](https://www.coilcraft.com/en-us/products/transformers/power-transformers/power-converter-transformers/q4435/) | メーカー表25°Cで両方1:1、典型用途4–6V→5V/1.6A。500Vrms巻線間試験記載 | 205V適格磁性部品/「成立した2組」に計上しない。1:1自体があらゆる回路で205V不可能という普遍命題ではなく、提案された適格ペアの根拠不在 |
| [LT3757/LT3757A PDF本文Rev.H](https://www.analog.com/media/en/technical-documentation/data-sheets/lt3757-3757a.pdf) p32, pp3–4 | 5–12V→350V/10mA,100kHz,1:10 TDK DCT15EFD-U44S003,Si7850DP,GSD2004Sは典型例。50kHz–1MHzはIC範囲。正FBX OVP6/7/8% | 205V×1.08=221.4Vは理想比例例でも220Vを超える。内蔵FBX OVPを独立保護に置換不可。参照FET/diodeも採用品でない |
| [LT8365 Rev.A](https://www.analog.com/media/en/technical-documentation/data-sheets/lt8365.pdf) pp2–4 | SW150V絶対最大、current limit1.5/2.0/2.7A min/typ/max、VIN=12V既定条件・温度/grade注記あり。Rds700mΩは0.5AでTYPICAL | 5Vでの保証/current波形に転用不可。multiplier実回路の解析は未完了 |
| [Microchip HV5524 DS20006850A](https://ww1.microchip.com/downloads/aemDocuments/documents/APID/ProductDocuments/DataSheets/HV5524-32-Channel-Serial-to-Parallel-Converter-Data-Sheet-DS20006850.pdf) pp3–4 | HVOUT推奨max220V、絶対max230V。3.4W/θJA typ19°C/Wは1oz4layer 3×4inch基板条件。IDD max25mAはCLK16MHz/DATA8MHz、VOL max15Vは100mA条件 | 230VをOVP目標にしない。データシート放熱能力を小型PETG筐体へ転用しない。低電流実VOL/全ch/clock条件を含む実損失UNKNOWN |
| [Keeppower P2150K](https://www.keeppower.com/product/keeppower-21700-5000mah-protected-li-ion-rechargeable-battery-p2150k/) / [P2150R](https://www.keeppower.com/product/p2150r-keeppower-21700-5000mah-protected-li-ion-rechargeable-battery-max-15a/) | メーカー掲載:両者充電+10..45°C/放電−20..60°C。Rは15A continuous掲載、Kへ移植不可。過充電/過放電/過電流/短絡保護を列記、温度cutoff閾値は未掲載 | SOURCE-LISTED。現物PCM revision、電流/温度de-rating/trip delay、国内供給、取付NTC/holder適合はUNKNOWN。採用なし |

## 3. 同じ負荷境界で比較する — C-024への補足修正

採用するのは**負荷台帳の定義**のみ。式:
`I_HV_total = I_digit + I_neon + I_bleeder + I_OVP/divider + I_driver/leakage`。
`P_SYS = P_HV/eta_HV/eta_5 + P_aux_SYS`（cascade時）。
USB→SYS損失/charge allocationは別項。IBATは放電を正とする。SYS→5V効率をUSB→SYS効率に代用しない。16mAの境界は未決のまま両方の解釈を残す。

以下はASSUMED:205V,digit3mA,neon0.5mA,eta5=.90,etaHV=.75、USB5V nominal、aux0。450mAは仮定の入力budget、500mAは名目比較で実IC通過保証ではない。

| 放電案/抵抗条件 | USB入力例 | digit0時neon上限 | digit1時 | digit2時 |
|---|---:|---:|---:|---:|
| P1:単一330k等価 | 450mA | 12 | 7 | 1 |
| P1:単一330k等価 | 500mA | 12 | 9 | 3 |
| P2:独立300k±5%×2、双方285k | 450mA | 11 | 5 | **不成立（neon=0でも不足）** |
| P2:同上 | 500mA | 12 | 7 | 1 |

C-024/B21:03のfloorを0へclipした表示は、digitだけの不成立を隠し得るため、**negative residual→INFEASIBLE**を正式な解析表示にする。450mA例のP2で7.438596mA需要>7.408537mA予算、P_SYS=2.259129W>2.25W。これは実モードの承認でも新しいUI制限でもない。補助/経路損失でさらに悪化する。498mA上限例も再計算しscript/CSVへ収録したが、上限閾値は最低供給保証ではない。

P1 bleeder=0.127348W、P2最熱=0.294912W at205V。2digit+12neon全点灯のP_SYSはそれぞれ3.833109/4.081351W。16mAがlamp-onlyならP2を含む需要は少なくとも5.296166W SYS（aux別）、whole-busならlamp許容は16mA未満。205×16mA=3.28W>5×.5=2.5Wなので、500mA USB-only full target不成立は効率仮定に依存しない。

direct-SYSの優位条件は、補助/経路を同境界にそろえて `eta_direct > eta5*etaHV`。例では>67.5%、65%ではcascadeより悪い。電源段削減だけで採用しない。

## 4. 放電/OVP/容量の採否

ASSUMED:Cmax12µF,V0 220V,Vend60V,T5s,R±5%。220Vは解析ceiling、60V/5sは未承認例。
`Rsurv,max <= T/(Cmax*ln(V0/Vend))`。
再計算:320689.697Ω、Rnom<=305418.759Ω。C-024の320689.2/305418.3との差は約0.0002%未満の丸め差で結論不変。二重passiveの最大散逸に関する下限0.333623W at220V。これは各実抵抗cornerの散逸が常にこの値以上という意味ではない。

300k×2例:一方open時Rmax315kで4.911290s、双方Rmin285kで0.339649W at220V。330k単一/+5%,Cmax12µFでは5.402419sで5s例に不適合。E220=0.2904J、E60=0.0216Jが残る。電圧到達だけでtouch-safeとはしない。

| 案 | 分析上の利点 | 不採用/採用条件・現状態 |
|---|---|---|
| P1 single passive | 単純、0.127W例 | openで経路消失、公差で時間超過。安全採用BLOCKED |
| P2 dual independent passive | 指定single-open RC例を満たせる | 0.295W連続熱、共通HV/GND断線/short/残留drive未対処。部品値採用なし |
| S1 switched discharge | run時散逸を減らせる可能性 | switch-open/電源喪失/MCU-off/共通returnを含むdefault無給電動作・pulse rating・hard-off未証明。BLOCKED |
| H1 hybrid | 常時/能動経路の相補性候補 | 二経路の独立性と全故障matrix、待機消費/費用が必要。条件付き探索 |

CminはOVP post-trip energy、Cmaxはstartup/残留/放電に使用する**同一実MPN**。tail energyは単一仮想pulseへ置換しない。必要条件:
`Vnormal,dynamic,max < Vtrip,min`,
`Etail,max < .5*Cmin*(220^2−Vtrip,max^2)`、
かつ出力への全供給停止・single fault・共通配線を評価。MAX66870µs TYPのみでは最大Etailが決まらない。Cmin/Cmax、実比較器/基準/分圧/停止素子/抵抗定格は未選定。

## 5. HV方式・実型番の比較と採否

| 方式/候補 | 現根拠 | 統合判断 |
|---|---|---|
| MAX668 ordinary5V boost | duty不足 | 既存限定REJECTED保持 |
| MAX668 autotransformer/coupled | ADI実験先例、低FET stress可能 | CONDITIONAL比較候補。旧isolated-DCM不成立を普遍化しない。実dot/端子/Llk/Isat/DCR/core、205V波形と供給未適格 |
| LT3757 + qualified HV transformer | 一次350V/10mA例、IC50kHz〜1MHz | controller-only候補。TDK旧参照をorder-ready扱いしない。Si7850DP/GSD2004Sも引用例のみ |
| LT3757 + Q4434/Q4435 | メーカー1:1、5V用典型 | **205V適格ペアとして不採用**。500Vrms試験はworking205V保証でない |
| LT8365 direct ordinary boost | SW150V vs205V | 限定REJECTED |
| LT8365 DC2838A multiplier | 9–30V/250V10mAデモ、実5V未適格 | CONDITIONAL比較候補 #10。current-limit表は波形の証明でない |
| direct-SYS flyback | 段数/効率比較 | 候補維持。minimum SYS、gate drive、PCM/drop、startup、OVPと実磁性が必要 |

40V FET/400V diodeはクラススクリーニングでありMPN採用ではない。漏れの.5LI²fは処理エネルギーで全量clamp heatとは限らず、Rp×Ipk²D/3は仮定三角波のみ。実結合回路のON/OFF電流経路、Qg/Coss/rr、core/銅損、温度/PCB/スナバを同時評価する。

## 6. PWR/BAT/CTRL/筐体と予算の成立性

- **BQ25185/TPS61023:** 最小SYS/最大load/起動HV Cmax、実L1 XEL4030-102MEC候補とeffective C未適格。USBあり≠net charge。充電電流別loss/Tj、BATFET低cell実電流、eFuse/配線/PCM/contact損失と熱を同じ電圧nodeで評価する。既存250mA充電設定は変更しない。JEDEC θJAを密閉PETGへ代用不可。
- **21700/NTC:** P2150K/RとTE STM010候補未採用。実セル表面取付、熱遅れ/剥離、NTC open/short、MCU-off、USB ramp、CE-GND shortを含める。充電禁止・battery-only負荷遮断・残留HV放電を別々に証明する。正のRs/Rp限定比証明はC-007でレビュー済みへ更新し、全補償回路不可能とはしない。
- **ランプ/熱:** IN-12B supplier値とAC NE-2試験条件は実205V DCの保証でない。2×3mA+12×.5mAの例ではlamp1.230W+ballast1.230W=bus2.460W。bus電力を全部converter IC熱へ加算しない。bleederは追加熱。短絡digitの20k例2.10125Wは定格選定/故障時間が未解決。輝度/始動/保持/寿命/最大同時点灯を実lotで評価する。
- **HV5524/Pico2/RTC/OLED/UI:** 提案baseline維持。OE/BL/POLはHV切断と同等でない。clock/同時ch/currentによるdriver損失、logic supply power-off、RTC backup、OLED3V3負荷、逆給電/standby、thermal fault表示と許可の分離が未完了。時計/encoder/switch UIを今回自動変更しない。
- **PCB/PETG:** copper/via/EP熱経路、実HV connector/抵抗working-voltage、沿面/空間/取付公差、電池とHV部の隔離、probe配線/アクセスが未検証。実装温度はcharger EP/上面、5V IC/L1、HV FET/diode/磁性/bleeder/ballast/HV5524、cell表面/端子/PCM/contact、筐体内外・ambientで測る計画が必要。合格は各選定部品/セル定格から誤差/遅れを引いた設計限度、誤検出/復帰hysteresis、遮断後残留を定義してから。固定の安全温度や60V/5sを捏造しない。
- **予算:** integrated-bom.csvの価格/stockは2026-11-15観測の歴史値。未価格/未数量/未選定行、税/国内配送/PCB/再製作/実装/保護追加が残り、最新着地額はUNKNOWN。初回≤4万円+予備1万円=総額≤5万円は**未達ではなく未立証**。部分合計を完成費としない。必要qty×現税込単価+vendor毎配送+PCB/実装+治具/絶縁+reworkをBが埋める。予備を本体に先食いしない。

**試作の現判断:** full-HV/密閉統合のGoは不可。D-014のcell/HV-free LV評価準備→適格電池assembly→独立HVの人間安全審査→密閉統合という段階案は保持するが、試験/購入の許可ではない。2027-01末期限に対して既存11/25実部品証拠、12/01方式/電力/温度判断、12/15初回購入判断packageを提案checkpointとして維持。11/25に欠落が残れば「不足MPN/見積/代替と影響」を明記し、定性比較の反復で通過扱いしない。

## 7. 次の役割契約・ユーザー判断

| 担当 | 既存Issue/境界 | 次回に必要な具体成果・終了条件 |
|---|---|---|
| A | #6中心、#9/#8接続 | 実比較器/ref/divider/cap/stop/discharge候補1式のデータシート表、Cmin/Cmax、tailの保証欠落、shared-return/電源全喪失fault matrix。採用不能なら不足保証を特定。CE/負荷独立cutoffの実候補と変更要求範囲を文書化し、同じRC感度表だけを再提出しない |
| B | #7/#2/#10、#4 | 現行生産HV磁性部品1個のcontrolled図面/dot/pin/Llk/DCR/Isat/working-voltageと国内少量価格/納期、又は全候補を除外した具体根拠。実lamp/holder/PCM/NTC assemblyと段階BOM、輸送税込。canonical負荷台帳にoverhead/符号付きBATを埋める |
| C | #6/#9と最新B21:03 | 今回Workの計算/一次表と差戻しの限定レビュー。原報告数でなく実回路・保証値・fault path/同じtopologyの成立条件を審査。歴史的backlogはUNKNOWNのままゼロ宣言しない |
| Work | #2/#4/#6/#7/#8/#9/#10 | 新しいMPN/一次保証/見積/回路判断が来た場合にまとめて統合。重要差分がなければ確認SHA付き短いログのみ |

次のユーザー判断は、(a)16mAのバス境界と200〜205Vがnominalか保証windowか、(b)USB接続中のfull表示時net-charge要否/表示モード、(c)実部品と総額が提示された段階試作範囲。現時点で仕様・購入承認を求めず、具体代替と費用を準備する。既存要件を維持して文書設計を継続。

## 8. 保存・検証

保存対象は本報告、decisions/open-issues/handoff、tech-tree.yaml/md、再計算script/CSV。KiCad/PCB/BOM旧成果は変更しない。
書込直前に最新refと共有索引blobを再確認し、base treeから一括commit、expected_sha付きref更新を行う。競合時は再取得/再統合。
保存後HEADと全変更fileを再読込し内容一致、YAML parse/ノードID/状態/Mermaid全依存辺、存在するevidence、cycleなし、再計算を検証する。保存後SHAはcommit自己参照を避け最終報告に記す。検証未完了を完了としない。

### Cレビュー原本
- [2026-11-19-1504-JST-C-REVIEW-007-therm001-proto001g-ratio-and-fault-contract.md](2026-11-19-1504-JST-C-REVIEW-007-therm001-proto001g-ratio-and-fault-contract.md)
- [2026-11-19-C-REVIEW-008-thermal-hv-batch.md](2026-11-19-C-REVIEW-008-thermal-hv-batch.md)
- [2026-11-20-0230-JST-C-REVIEW-009-charge-ramp-holder-contact.md](2026-11-20-0230-JST-C-REVIEW-009-charge-ramp-holder-contact.md)
- [2026-11-20-0902-JST-C-REVIEW-010-therm-ce-and-usb-power.md](2026-11-20-0902-JST-C-REVIEW-010-therm-ce-and-usb-power.md)
- [2026-11-20-1500-JST-C-REVIEW-011-ce-evm-neon-usb-power.md](2026-11-20-1500-JST-C-REVIEW-011-ce-evm-neon-usb-power.md)
- [2026-11-20-2100-JST-C-REVIEW-012-hv003-bleeder-lt3757-source.md](2026-11-20-2100-JST-C-REVIEW-012-hv003-bleeder-lt3757-source.md)
- [2026-11-21-0300-JST-C-REVIEW-013-ovp-capacitor-transformer-sourcing.md](2026-11-21-0300-JST-C-REVIEW-013-ovp-capacitor-transformer-sourcing.md)
- [2026-11-21-0903-JST-C-REVIEW-014-hv001-sys002-batch.md](2026-11-21-0903-JST-C-REVIEW-014-hv001-sys002-batch.md)
- [2026-11-21-1503-JST-C-REVIEW-015-dcm-dc2838a-batch.md](2026-11-21-1503-JST-C-REVIEW-015-dcm-dc2838a-batch.md)
- [2026-11-21-2105-JST-C-REVIEW-016-flyback-frequency-lt8365-current-batch.md](2026-11-21-2105-JST-C-REVIEW-016-flyback-frequency-lt8365-current-batch.md)
- [2026-11-22-0300-JST-C-REVIEW-017-max668-lt8365-primary-batch.md](2026-11-22-0300-JST-C-REVIEW-017-max668-lt8365-primary-batch.md)
- [2026-11-22-0900-JST-C-REVIEW-018-hv-autotransformer-sys-supplement-batch.md](2026-11-22-0900-JST-C-REVIEW-018-hv-autotransformer-sys-supplement-batch.md)
- [2026-11-22-1504-JST-C-REVIEW-019-autotransformer-supplement-batch.md](2026-11-22-1504-JST-C-REVIEW-019-autotransformer-supplement-batch.md)
- [2026-11-22-2108-JST-C-REVIEW-020-hv-leakage-batfet-cell-batch.md](2026-11-22-2108-JST-C-REVIEW-020-hv-leakage-batfet-cell-batch.md)
- [2026-11-23-0300-JST-C-REVIEW-021-magnetics-ratio-current-provenance.md](2026-11-23-0300-JST-C-REVIEW-021-magnetics-ratio-current-provenance.md)
- [2026-11-23-0900-JST-C-REVIEW-022-thermal-bleeder-sys-efficiency-batch.md](2026-11-23-0900-JST-C-REVIEW-022-thermal-bleeder-sys-efficiency-batch.md)
- [2026-11-23-1500-JST-C-REVIEW-023-bleeder-lamp-ballast-batch.md](2026-11-23-1500-JST-C-REVIEW-023-bleeder-lamp-ballast-batch.md)
- [2026-11-23-2100-JST-C-REVIEW-024-sys002-sys001-batch.md](2026-11-23-2100-JST-C-REVIEW-024-sys002-sys001-batch.md)
