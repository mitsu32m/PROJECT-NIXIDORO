# PWRモジュール回路図設計ノート — Draft v0.1
Updated: 2026-11-14 JST
Status: PROPOSED / TO_VERIFY — **KiCad実配線前のブロック接続設計**。メーカー定数、熱、電池規格、充電動作、電源切替、PCBは未検証。

## 目的
BQ25185のPower Pathから周辺3.3V、HV向け5Vを供給し、XIAO RP2350を安全に給電する。試作PWR基板を合格後そのまま完成品に搭載できる構成を目指す。

## 1. トポロジー（論理接続）
```mermaid
flowchart TB
  USB[USB-C 5V sink] --> INPUT[CC/ESD/入力保護]
  INPUT --> IN[BQ25185 IN]
  CELL[保護付き21700 1S + セル密着NTC] <--> BAT[BQ25185 BAT / TS]
  IN --> SYS[BQ25185 SYS]
  BAT --> SYS
  SYS --> V5[TPS61023 5V]
  SYS --> V33[TPS63031 3.3V]
  V5 --> HV[HV PCB MAX668 + HV driver logic]
  V33 --> PER[OLED/RTC等 周辺]
  V5 -. 経路・逆流防止未確定 .-> XIAO[XIAO RP2350]
```
- これは**回路図そのものではない**。電源経路の損失、保護、シーケンス、USB-C広告電流検出、コネクタ実装は未確定。

## 2. BQ25185：メーカー仕様に沿ったネット表
| ピン（10pin WSON DLH） | ネット | 必要処理・評価 |
|---|---|---|
| IN=10 | USB_PROTECTED_5V | IN-GND 1uF以上のバイパス、USB ESD/保護と配線の確認 |
| SYS=1 | SYS | SYS-GND 10uF以上のセラミック、**DCバイアス時の実効容量1uF以上**、5V/3.3Vレールへ |
| BAT=2 | CELL_PLUS | BAT-GND 1uF以上、保護付きセルとセル専用の温度センシング、逆挿入保護の要否 |
| GND=5 + exposed pad | GND | メーカー推奨の放熱ビアとGND面、充電時の熱計算 |
| TS/MR=6 | CELL_TS | セル密着NTCの抵抗値、分圧/電流源のデータシート回路、誤検出・factory modeを検証 |
| ILIM/VSET=7 | ILIM_VSET_CFG | **入力電流制限と終止電圧の両設定が関わる**。セル定格に対応する4.2V等と100/500/1100mAを同時に設定する抵抗を公式表で選ぶ |
| ISET=8 | ICHG_CFG | 250/500mA充電候補に対応する抵抗を公式式で計算。充電熱の実測前に1A採用しない |
| /CE=4 | CHARGE_EN_N | active-low：Lowで充電許可、Highで停止。MCU不在/初期化時のデフォルトを要定義 |
| STAT1=9, STAT2=3 | CHG_STAT1/2 | オープンドレイン、適切なプルアップ（TI: 1k～20kΩの範囲）とMCU入力閾値、電源OFF時逆流を検証 |
| Thermal pad | GND | WSONパッドの熱設計は必須 |

**一次資料:** TI BQ25185 Rev.B (Aug 2026) https://www.ti.com/lit/ds/symlink/bq25185.pdf

## 3. 5V / 3.3V DC-DCレール
- **TPS61023**をSYS→5Vの候補とする（VIN 0.5–5.5V、起動時1.8V以上、典型電流制限3.7A、5V/1.5A@3.6V入力時94%参考効率）。リミットは保証出力電流でない。インダクタ、入力/出力容量、FB抵抗、出力リップル、EN/UVLO、SW配線と温度をメーカー推奨回路に基づいて確定する。https://www.ti.com/product/TPS61023
- **TPS63031**をSYS→3.3V周辺電源の候補とする（VIN 1.8–5.5V、3.3V固定、昇圧時の出力公称上限参考約500mA@VIN>2.4V）。XIAOの3V3へ無条件で給電しない。https://www.ti.com/product/TPS63031
- 200V×16mAのHV最大ストレス負荷=3.2W、MAX668効率70%仮定→5V側0.914A。5Vロジック等0.5W仮定なら5V合計約1.014A、TPS61023 85%仮定・SYS3.3VならSYSから約1.81A。**これは起動突入・外部負荷・熱・電源配線の設計値ではない**。

## 4. XIAO RP2350：要注意事項
- Seeed公式Pin Map：**5V=VBUS（Power Input/Output）**、**3V3=3V3_OUT（Power Output）**。専用内蔵USB充電IC SGM40567およびBAT padが存在する。https://wiki.seeedstudio.com/xiao_rp2350_arduino/ ; https://files.seeedstudio.com/wiki/XIAO-RP2350/res/Seeed-Studio-XIAO-RP2350-v1.0.pdf
- **外部PWRの5VをXIAO 5V/VBUSへ直結し、同時にPC USBを挿す運用は回路確認なしに禁止**（電源逆流、USB VBUS誤印加、XIAO内蔵充電経路への給電の可能性）。
- XIAOのBAT padをBQ25185 BATへつないだり、外部TPS63031の3.3VをXIAO 3V3へ直結することも未承認。
- **実装選択肢**：(A) XIAOは試作用として独立USB給電、PWRはパワー負荷の試験に限定。(B) 完成品ではメーカー回路図に照らして5V給電の逆流ブロック/切替を設計。(C) 完成版ではRP2350チップ直接実装を含め、コスト・作業量・USBプログラミング経路で比較。
- 5V入力とUSBデータ線を同時接続する際の全電源経路・MOSFETボディダイオード・3.3V逆流・MCU GPIOのパワーシーケンスをレビューするまでピン配線は確定しない。

## 5. USB-Cと電池の最低限の回路検討
- USB Type-C 5V sinkのCC1/CC2にそれぞれRd=5.1kΩ（型番/許容差とソース電流広告は別途仕様整合）、ESD/過電流/サージ・保護を検討。BQ25185への1100mA入力設定はCC広告またはUSB仕様に基づいた能力確認なしでは禁止。
- Li-ionセルは**保護付き製品**を前提とし、充電電圧4.2Vを想定する場合はセル仕様とILIM/VSETを適合させる。BQ25185は保護付きセル自体を代替しない。
- 専用セルNTCの配置と抵抗定数は、BQ25185 TS/MR方式をTI公式回路で確認し、セル温度だけでなく充電IC基板温度も測る。
- SYS電圧、BAT電圧、USB VBUS、5V、3.3V、充電/放電電流の測定端子（シャントは電源損失を増すため試験条件を分離）を確保。
- BQ25185の工場モード、長押しMR、充電/電池不足時の起動条件を確認。

## 6. 発注用KiCad確定前のゲート
1. **BQ25185のILIM/VSETとISET抵抗の公式式・対応表**から、保護付き21700の電圧、USB入力制限500mA、充電250/500mAの両立を計算。
2. **XIAOへの給電**を内蔵充電ICとUSBデバッグ時の同時電源を含め、Seeed回路図でトランジスタ/ダイオード単位に確認。
3. TPS61023の3V近辺の入力・1A超出力について、インダクタピーク、SW current limit最小値、効率、温度、入力配線を計算。
4. TPS63031の必要3.3V負荷、効率、EN状態、放電を評価。
5. 充電時とHV負荷時の熱、USB入力制限、cell NTCとPETG密閉条件のgo/no-go。
6. コネクタ型番・GPIO・UVLO・抵抗コンデンサ定格、KiCad footprintとJLCPCBの実際の購買/実装可能性を確認。

関連: [module-interfaces.md](module-interfaces.md) / [power-state-machine.md](power-state-machine.md) / [components.md](components.md)
