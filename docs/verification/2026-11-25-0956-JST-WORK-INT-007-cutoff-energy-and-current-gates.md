# WORK-INT-007 — 上流遮断後エネルギーと低SYS電流余裕

日時:2026-11-25 09:56 JST（確認開始）。役割:Work設計統合、NO FORMAL CLAIM。
正本branch:`codex/reva-integrated-prototype-review`。開始HEAD:`58976653bd8f41bdae82139f62199a30b9c549c0`。
前回確認保存`1b970784b6863f0f0c8a065863592b62e98234de`から3 commits/3 added reports。前回実質統合`eda377ae20a0ee397fb716334c6d52f9f634c9c2`からは確認ログを含む4 commits/4 files。共有索引/回路図/PCB/BOM変更なし。

## 契約・統合結論

C-027の判断パッケージを入口に、関連#6 HV-002/SYS-002、#10 HV-MULT/SYS-001、#7 PROTO-001をまとめて扱う。必要原本はB01:00とA04:01のみ。終了条件は遮断エネルギー/電流の根拠クラスをそろえ、候補と採用を区別し、11/25証拠チェックの不足を具体化、索引/ツリー/計算を保存後検証すること。
**分析要件の追加は採用。ハード/部品/方式の採用とfull-HV試作GoはBLOCKED / NOT ORDER-READY。** 200〜205V/最大16mA連続目標・lamp/bus境界の未決状態を変更しない。

C-027がWork005のTLV6700 INB上昇→OUTB下降29µs NOM訂正と、Würth図面/functional-insulation限定根拠、B11/24 09:03の限定算術をレビューした。共有索引の「B09:03未レビュー」を現在状態として更新する。旧成果は保持。新A04:01はC-027後の**PENDING C REVIEW**で、今回Workは一次表/数式の限定範囲を独立確認したが、Cレビュー完了や正式部品採用とは主張しない。全履歴backlog UNKNOWN。

## 重要な新事実と一次資料

確認日2026-11-25。GUARANTEEDはmin/maxと試験/温度/grade条件内、TYPICALは代表、ASSUMEDはモデル、MEASUREDは今回なし、UNKNOWNは欠落。

### TPS22918上流遮断候補 — 採用なし

[TI SLVSD76C Rev.C July2017](https://www.ti.com/lit/ds/symlink/tps22918.pdf) §§6.1/6.3–6.6、8.3.1–8.3.2を直接再確認。
- ONはactive-high、浮遊不可。pin表はON3、VIN1、VOUT6、GND2、QOD5、CT4。実回路への割当/配線変更は未実施。
- RON max79mΩはVIN5V、IOUT−200mA、−40..105°C条件。約1Aや低SYSでの保証値へ転用しない。連続2AはTA70°Cのabsolute max欄であり、小型筐体内の連続動作/温度成立証明ではない。θJA183.2°C/Wはreference条件、PETG実熱抵抗ではない。
- tOFF2µsは**TYPICAL、MAX欄なし**。VIN5V、RL10Ω、CIN1µF、CL0.1µF、CT1000pF、TA25°C、QOD open、VINがsteady後にON操作する条件。全温度/電源喪失時/任意loadの最大hard-offではない。
- 推奨VOUT上限VIN。reverse-blocking機能の保証を当該資料から確立できず、残留cap/別経路からの逆給電を安全隔離とみなさない。
- RPD max30ΩもVIN5V/ON0の指定条件。**§8.3.2.1はVIN低下でQODが弱くなり放電が遅れる**と説明。QODはLV VOUTの機能でHV出力capの放電と同じではない。§8.3.2.2はQODへの外部継続駆動を避ける旨と内部QOD単独の容量/熱制約を記載。QODがconverterより先に必ずエネルギーを奪う保証なし。

結論: Aのsource/energy screenはWork限定確認、TPS22918は**条件付き比較候補**のみ。2µsを最大保証にする/ON pulldownだけで全故障default-offを主張する案は不採用。実latch、driver、stuck-high/short、無給電、reverse-feed、cell/thermal stopとの関係はUNKNOWN。

### LT8365電流余裕 — C-027レビュー範囲を統合

[ADI LT8365 Rev.A](https://www.analog.com/media/en/technical-documentation/data-sheets/lt8365.pdf) p3/p14を直接再確認。
p3 limit threshold min/typ/max1.5/2/2.7A、既定VIN=EN12V、温度marker/grade注記を保持。p14 **boost**用の定常peak≤1.5Aおよび飽和せず2.7A以上を扱うinductor選定説明を確認。定常設計目安、電流limit表、実fault transient peakを区別する。実charge-pumpのbranch pulseを通常boostのIavg+ΔI/2と同一視しない。

ASSUMED:205V、etaHV=.75、Vin3/5V、peak screen1.5A、aux0、bleederはINT004のdual285k×2仮定。
| 16mA解釈 | P_HV | Vin | Iavg proxy | ΔIpp budget=2(1.5−Iavg) |
|---|---:|---:|---:|---:|
| whole-bus |3.280000W|3V|1.457778A|0.084444A|
| lamps-only+dual bleeder |3.574912W|3V|1.588850A|−0.177700A（proxy不成立）|
| whole-bus |3.280000W|5V|0.874667A|1.250667A|
| lamps-only+dual bleeder |3.574912W|5V|0.953310A|1.093380A|

zero-ripple必要etaは3Vで72.889/79.442%。ゼロrippleは現実の設計達成値ではない。3V busの小さい余裕、lamp-onlyの負余裕は候補比較の絞り込みに使えるが、actual pump回路/効率/low-SYS保証がないため普遍的device不採用ではない。5V preboostはcurrent marginを緩め得る一方、TPS61023/起動/変換損失/熱を追加する。外付FET方式も条件付き候補のまま。

## 遮断エネルギー契約の追加

**D-024: 上流スイッチ後に残るLV capも、同じHV OVP/停止/Cmin/Cmax契約へ含める。**
理想的な瞬時上流遮断でも下流入力capの利用可能energyは残る。
`E_LV_available=.5*C_L*(Vstart²−Vstop²)`。
ASSUMED Vstart5V/Vstop3Vでは10/22/47µF→80/176/376µJ。INT005のnormalized OVP例Cmin1µF/headroom73.107319µJと比較すると、**100%がHVへ移る最悪仮定では**どれも予算を超える。これは実転送量でも実機NO-GOの証明でもない。
同仮定/他tail0ならC_L≤9.138415µF（5→3V）、≤5.848586µF（5→0V）。**実input capを減らす採用値ではない**。effective Cmax、controller stop電圧、転送効率、QOD競合、実停止timing、蓄積magnetic energy、別feedが未確定だからである。

次の設計計算では、遮断成立までのsource供給energy、遮断時点のLV capacitorsと磁性蓄積、他電源/逆給電からの供給、HV capからの実dischargeをエネルギー源ごとに追跡し、重複計上せずEtail,maxを上限化する必要がある。capごとに電圧node、effective Cmin/Cmax、供給元、遮断後の転送pathを記す。RPDやconverter停止typ値だけでenergy分配を保証しない。
最終要件は引き続き `Vnormal,dynamic,max < Vtrip,min` と `Etail,max < .5*C_HV,min*(220²−Vtrip,max²)`、同じC_HV,maxでstartup/残留/放電も満たすこと。独立直接gate inhibit、上流遮断+独立stop、適格な別controllerの比較を継続し、どれも未承認。

## 採否・全体成立性

| 対象 | 今回の処理 | 採用条件/残課題 |
|---|---|---|
| Work005の29µs訂正/Würth原資料範囲 | C-027による限定確認済みへ更新 | typ→max/機能絶縁→システム承認へ昇格しない |
| LT8365 low-SYS current proxy | C-027レビュー済み分析として採用 | 実pump SW/diode/flying-cap電流、VIN/duty/温度保証・startup・熱・quoteが必要 |
| TPS22918 upstream cut | alternative、実装BLOCKED | full-load RON/最大stop/reverse-feed/QOD電源喪失/short fault/latch検証 |
| LV stored-energy inventory | 必須解析契約として採用、A原本C待ち | 実MPN/Ceff/node/transfer/timing/その他feedと共同OVP証明 |
| MAX668 coupled/LT3757 flyback/direct-SYS/LT8365 multiplier | 比較候補維持 | 新しい適格205V/16mA pairなし。ordinary boost限定却下も保持 |

200〜205V/16mAは目標であり成立未立証。HV5524推奨220Vを停止目標に使わず余裕を確保。BQ25185/TPS61023の低cell/充電電流別loss/Tj、実L1/Ceff、signed IBAT、cell/PCM/contactは未適格。21700/NTCの充電禁止とBAT-only独立温度保護、CE短絡/MCU-off/センサ脱落未検証。IN-12B/neonの実DC lot/current/ballast fault、Pico2/RTC/OLED/UIの電源/OE/backup/逆給電、PCB copper/via/EP/絶縁とPETG実cell温度はWork005のhold継承。今回回路図/PCBを変更せず、実測もなし。

必要測定は実候補/監督者の安全計画が整った後: upstream ON/VOUTとcontroller gate/磁性/rectifier/HV波形の遮断連動、power-loss/別feed/capacity範囲、driver/FET/磁性/QOD/bleeder/ballast/IC温度、cell表面/PCM/端子/contact/内外ambient、充電/BAT-onlyとUSB遷移。受入限度は実部品/セル仕様と誤差/遅れから定義する。測定実施許可や安全認定ではない。

## 11/25証拠チェック — 09:56時点未充足

提案checkpointであって自動発注日ではない。本日終了までの未提出を断定しない。開始SHAのBOM blob `06c32829ab49e8aa32fc7dccaff6ad3a62fe1ae3` を再取得し、価格/stock列が11/15観測のままと確認。
| 必要成果 | 現根拠 | 不足/影響 |
|---|---|---|
| 実HV controller+magnetics continuous pair | Würth/CJ/LT8365資料・proxy | low-SYS/波形/温度/保護の適格pair0組、first-HV構成未確定 |
| 独立OVP/停止/放電部品一式 | TLV6700/TPS22918候補 | 実HV抵抗/基準/latch/cap、最大tail/default-off/short faultが未解決 |
| cell/NTC/holder/PCM assembly | 既存候補のみ | 実型番保証・取付・充電/放電温度とcontact熱不足 |
| 段階BOM/国内少量着地見積 | 歴史BOM | 最新税込/送料/PCB/実装/再製作/供給納期UNKNOWN |

**初回≤4万円、予備≥1万円、総額≤5万円は未立証**。TPS22918追加による費用/基板面積/損失も未計上。部分価格や典型lossから予算達成を主張しない。12/01方式/電力/熱判断、12/15初回購入判断package、2027年1月末使用期限は既存計画提案を維持する。
full-HV発注packageは今朝時点で出せない。継続可能なのはcell/HV-free LV評価の**準備案**であり、それも具体BOM・test planと人間承認前の購入/試験Goではない。

## 次の役割契約とユーザー判断

- **A #6/#8/#9:** 一つの実stop-latch/driver候補回路案と全cap node一覧を出す。上流供給停止とcontroller gate inhibitの役割、QOD/無給電/short/別feedと最大timing/Etailを同じ表へ。input Cを単に減らして逃げない。実RON/timing保証不足なら別候補との具体比較を行う。
- **B #7/#10/#2:** 実charge-pump回路をON/OFF各状態で追いSW/diode/flying-cap/Lの実peak/RMSと3–5V条件を出す。若しくは外付FET/5V前段込みの実pairへ絞る。現国内少量税込配送・納期と段階BOMを優先し、同じ1.5A感度表の反復だけを進捗にしない。
- **C:** 未レビューA04:01と今回WorkのLV capエネルギー契約/TPS一次表をまとめてレビュー。C-027の既確認内容は重複全調査しない。source limitsと仮定、保証と測定、actual topologyとproxyを区別。
- **Work:** 新MPN/実回路/保証/見積があれば再統合。無ければ短いSHAログ。#6/#7/#10へ既存Issue追記、重複新設なし。

次のユーザー判断は、実代替/費用が揃ってから16mA lamp/bus境界・電圧nominal/window、USB表示/net-charge、段階試作範囲。現時点で仕様変更を求めたり達成不能と断定しない。原レポート/不採用案を保持し、正式Claimを主張しない。

## 根拠・保存検証

[C-027](2026-11-25-0301-JST-C-REVIEW-027-ovp-wurth-lt8365.md)、[B current](2026-11-25-0100-JST-chatb-lt8365-input-current-margin.md)、[A cutoff](2026-11-25-0401-JST-HV-002-tps22918-guarantee-and-input-tail.md)を開始HEADで取得。Work005を継承。
再計算: `hardware/integration/work-int-007-energy-current-audit.py/.csv`。共有索引/ツリーにD-024/025/026とreview状態を同期し、HV-CUT-TPS candidateのみ追加。安全gate/既存statusは昇格なし。
書込直前ref/blob確認、base-tree一括commit+expected_sha更新、保存後全内容再読込・差分・YAML/Mermaid状態/辺/循環/リンク/計算再現を検証。保存後SHAは最終報告に記す。購入、PCB、HV、main、重要仕様、回路図、安全承認、タスク変更なし。
