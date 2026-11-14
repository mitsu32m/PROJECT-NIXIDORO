# HV5524フェイルセーフ表示・RV-3028-C7時刻保持 — Draft v0.1

**実ピン番号・TSSOP-14配線・RTC用47µF MLCCの初回比較候補:** [CTRL回路図接続ドラフト](ctrl-driver-rtc-schematic.md)。こちらが最新の具体接続案。
Updated: 2026-11-14 JST
Status: PROPOSED / TO_VERIFY — **未実装、未発注。高電圧出力の安全性をハードウェア/実機試験で証明するまで「安全確定」としない。**

## 1. HV5524 メーカー真理値表の重要事項
Microchip HV5524 DS20006850A, Table 3-1, 3-2, Figure 3-1:
- **BL=LOW, POL=HIGH → 32出力すべてOFF（open drain Hi-Z）**、DATA/CLK/LE状態に依存しない。
- **BL=LOW, POL=LOW → 32出力すべてON（全カソードシンク）**。**POL=LOW固定 + BLのLOWプルでは危険**。
- BL=HIGH, POL=HIGHでシフトデータ/ラッチに応じて通常駆動。CLKは**立下り**でシフト、LE=HIGHでラッチに転送し、LE=LOWで保持。
- 通電手順 Table 3-1: ground→VDD→logic input known state、切断は logic inputs removed→VDD→ground。MCU 3.3Vが生きて5V VDDが無い場合のインターフェースは別途対策。
- VDD推奨4.5–5.5V、HVOUT推奨220V max、絶対最大230V。**論理BLでHVOUT電圧耐圧を上げられない**。OVP/bleeder必要。
- 一次資料: https://ww1.microchip.com/downloads/aemDocuments/documents/APID/ProductDocuments/DataSheets/HV5524-32-Channel-Serial-to-Parallel-Converter-Data-Sheet-DS20006850.pdf

## 2. 表示安全側ハード初期値・具体回路候補
**有力接続例**（抵抗値は初期候補で部品定格/ロジック出力を確認）:
- HV5524 **POL (pin27)** → +5V_LOGICに10kΩ pull-up。POLをPico GPIOに出さず**固定HIGH**。5Vが安定している間はBL=LOWで全消灯。
- HV5524 **BL (pin33)** → 10kΩ pull-down to GND。Pico GP3→Ioff対応の**SN74LV4T125** 3.3→5Vシフタ→BL。MCUリセット時はシフタ出力を高インピーダンスとしてBLのLOWを維持。
- SN74LV4T125の**/OE(active-low)** は起動時HIGHで出力Hi-Zとなるハード回路（例: pull-up to +5V_LOGICと、MCU/PowerGood論理でLOWを駆動）。ただし**/OE=OFF時にHV5524のDATA/CLK/LEも浮かないよう**必要に応じて各ラインにpull抵抗を設ける。/OEの実装素子とMOSFETなどのトランジスタ構成、Ioffとpower-up条件は型番個別に確認。
- GP0/GP1/GP2→同ICの残り3ch→DATA (pin32)、CLK(pin28)、LE(pin31)。SPI風のシフト制御だが**CLK falling edgeとLE high透明ラッチ**に注意し、まず全ゼロを書込んでラッチしてからBLをHIGHへ。
- 起動直後は**HV_EN=LOW**が最上位。5V_LOGIC安定→POL HIGH/BL LOW確認→シフトレジスタを0で初期化→ラッチ→表示許可→必要なときだけHV_EN許可。
- シャットダウンはBL=LOW→HV_EN=OFF→bleederによる放電確認→5V_LOGIC停止。異常時は**HV電源独立OVPを優先**し、BLだけのOFFを感電保護と扱わない。
- **5V VDDがゼロ/途中/電源断でHVOUTに200Vが残る条件の出力OFFは保証できない**。HV停電時は残留電荷が安全に放電するよう設計し、異常切断でVDDが先に消えても人がHV端子に接触できない構造が必須。
- **注意**: 出力「OFF」はカソードシンクの不導通を意味し、陽極側の200Vを消す意味ではない。ニキシー管・ネオン電流制限抵抗を各管に実装、HVを遮断する機能とは混同しない。

### 設計検証
1. 高電圧の供給前に**5Vロジックのみ、出力側LED/抵抗等の安全な治具**で、VDD立上り/MCUリセット/USB抜去/シフタOFF時に全出力がOFFになるか検証。
2. 独立OVP動作時のHV停止はBLに依存せず評価。高電圧の試験は教員監督で保護カバー/放電装置/適切な測定プローブを使用。
3. 10kΩプル抵抗は基本候補。真理値表の入力閾値、抵抗公差、漏洩/ノイズ/信号立上り、+5V消費電力を見て確定。

## 3. RTC RV-3028-C7: バックアップ電源方針
- RTCの消費電流45nA@3V typ、動作範囲1.1–5.5V、VBACKUPと自動切替・トリクルチャージ機能あり。**45nAは全温度・全設定・全電圧での最大値ではない**。
- 目的は**Picoが停止・電池抜去後の時刻保持**。タイマーのWORK/PAUSE等の状態保存はMCUの不揮発メモリ等が別途必要。バックアップRTCはセッション状態を自動保存しない。
- **主電源案:** RV-3028 VDD←Picoの3V3(OUT)（I²Cを同じ3.3V電源ドメインにする低コスト案）。代替としてPWR 3V3 PERIPH利用の場合はI²Cオフ時逆給電とバックアップモードの制約を再検討。
- **バックアップ第一検討案:** VBACKUPに適切な低漏れスーパーキャパシタまたは専用バックアップコンデンサを接続。RTCの内部トリクルチャージ/切替を使用する場合は**EEPROM 37hのTCE/BSM/TCRを正しくプログラムして永続化**。出荷初期値はバックアップ切替・トリクル機能OFFとして扱い、書込読返しで確認。RTCのCLKOUT不要時は無効化し消費電流低減。
- **予備代替案:** 一次電池（例:適切なコイン電池）をVBACKUPへ供給する場合は**TCEを必ずOFF**、RTC主3.3Vから一次電池へ充電しない。電池ソケット・誤装着・寸法・廃棄を含めて費用比較。充電式バックアップ電池は別規格/充電条件が必要。
- スイッチオーバーは**Direct Switching Mode (DSM)** と **Level Switching Mode (LSM)** があり、コンデンサ・電池の特性と希望電圧範囲に合わせて選択。動作条件とI²Cアクセス可能/不可をアプリマニュアルで評価。
- **重要**: Micro Crystal app manualの発行版によってトリクルチャージ抵抗値の表記に差異が存在する（2018版 1/3/6/11kΩ vs 2021版 3/5/9/15kΩという資料表示）。**最終採用のRTC枝番と最新版メーカー資料の改訂番号で確定するまで、抵抗設定コードを固定しない**。
- 一次資料: https://www.microcrystal.com/en/products/real-time-clock-rtc-modules/rv-3028-c7/ ; 2018 App Manual https://download.mikroe.com/documents/datasheets/rv-3028-c7-app-manual.pdf

## 4. バックアップ容量の試算（理想化モデル、予算・体積比較用）
理想式 t=C×(Vstart−Vstop)/I。例: Vstart=3.0V, Vstop=1.1V、I=45nA一定（*室温typ、漏れゼロの仮想条件*）。
| C | 理想の保持時間 | 注意 |
|---|---:|---|
| 100µF | 約1.17時間 | MLCC DCバイアスとリークを無視。実物では短い |
| 0.01F (10mF) | 約4.9日 | スーパーキャパシタの漏れ電流/自己放電は45nAを大幅に超える可能性 |
| 0.047F (47mF) | 約23日 | 実保持時間はセルのリーク・ESR・温度/RTC動作で短縮 |
| 0.1F | 約49日 | 体積/価格/充電時間増加、電池断電時の接続条件も検証 |
- **容量だけで日単位のバックアップを保証しない**。スーパーキャパシタの実漏れ電流（温度・充電直後含む）が支配的になることがある。高額・大きなものを先買いせず、低漏れ実測後に選ぶ。
- バックアップ要求を「電池交換時5分」なのか「数日」なのか先に定義する。数日なら容量/漏れが課題で、小型一次電池方式も比較。

## 5. ハードウェア/ファームウェアの実装ToDo
- HV5524 POL pull-up、BL pull-down、SN74LV4T125 /OE起動無効、DATA/CLK/LE初期値、5V PGOOD連動等をKiCadへ転記（**10kΩは仮**）。
- RTCのVDD/VBACKUP/GND、I²C pull-ups（Pico 3V3ドメイン）、バックアップ電源充電/切替とEEPROM設定を回路図・ファームに反映。
- RTCのGPIO/アラーム/バックアップ時I²C停止時の扱いを確認。時計日時保持とセッション状態保存を分けて試験。
- **最大電流・最悪温度・故障安全・200V時の耐圧を測定してから完成品へ転用**。高電圧回路は教員レビュー必須。
