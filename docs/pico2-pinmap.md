# Pico 2 GPIO割当・CTRL電気接続 — Draft v0.1
Updated: 2026-11-14 JST
Status: PROPOSED / TO_VERIFY。**ピン配置は設計初案で、購入/PCB発注確定ではない。**

## 選定根拠
- Raspberry Pi Pico 2を仮の第一候補（51×21mm、26 external GPIO）。公式ピン配置 https://pip-assets.raspberrypi.com/categories/1005-raspberry-pi-pico-2/documents/RP-008301-DS-1-Pico-2-Pinout.pdf
- Pico 2 datasheet https://datasheets.raspberrypi.com/pico/pico-2-datasheet.pdf
- GP0–GP22 + GP26–GP28が外部GPIO、GP23/24/25/29は基板内部用途（GP29はVSYS/3計測経路）で、独立外部コネクタGPIOとして数えない。USB VBUS senseとVSYS ADC3は回路図確認・測定方式に依存。
- HV5524は32カソードをシリアル制御するため、Picoの32 GPIOは不要。

## GPIO初回アサイン
| Pico GPIO | Pico基板物理pin | 信号名 | 行先/用途 | 注意点 |
|---|---:|---|---|---|
| GP0 | 1 | HV_DATA | SN74LV4T125候補 → HV5524 DATA | 5Vレベル変換、OFF中の逆給電防止 |
| GP1 | 2 | HV_CLK | SN74LV4T125候補 → HV5524 CLK | 同上 |
| GP2 | 4 | HV_LE | SN74LV4T125候補 → HV5524 LE | 同上 |
| GP3 | 5 | HV_BL | SN74LV4T125候補 → HV5524 BL | 電源投入時の全消灯レベルはHV5524資料で確定 |
| GP4 | 6 | HV_EN_REQ | HV電源起動要求 | HV基板ハードOFF既定。独立OVPが上位優先 |
| GP5 | 7 | HV_FAULT_N | OVPなど異常通知 | ハードウェア側で停止が完結すること |
| GP6 | 9 | NEXT_L | NEXTスイッチ左 | チャタリング、プルアップ |
| GP7 | 10 | NEXT_R | NEXTスイッチ右 | 同上 |
| GP8 | 11 | ACTION | 大型ボタン | 同上 |
| GP9 | 12 | ENC_A | エンコーダA | チャタリング/EMC |
| GP10 | 14 | ENC_B | エンコーダB | 同上 |
| GP11 | 15 | ENC_SW | エンコーダ押込 | 同上 |
| GP12 | 16 | AUDIO_PWM | ブザー/アンプ制御 | 動作電圧とアンプの消費電力確認 |
| GP13 | 17 | BQ_STAT1 | BQ25185 STAT1 | 3.3V適合プルアップ、電源OFF時逆給電注意 |
| GP14 | 19 | BQ_STAT2 | BQ25185 STAT2 | 同上 |
| GP15 | 20 | PWR_5V_OK | 5V PowerGood（回路は未確定） | 単純に5VをGPIOへ入力しない |
| GP16 | 21 | PWR_5V_EN | TPS61023のENをPWRへ | 電源OFFデフォルト、PWRプルダウン |
| GP17 | 22 | I2C_ISO_EN (option) | RTC/OLEDの異電源I2C分離 | 使わなければ予備 |
| GP18 | 24 | PWR_3V3_EN (option) | 周辺3.3V制御 | RTCの保持電源方針決定まで予備 |
| GP19 | 25 | SPARE | 予備 | 将来拡張 |
| GP20 | 26 | I2C_SDA | OLED+RTC | I2C0 SDA |
| GP21 | 27 | I2C_SCL | OLED+RTC | I2C0 SCL |
| GP22 | 29 | SPARE | 予備1本 | 電源保持/MCUリセット拡張候補 |
| GP26 | 31 | ADC_BAT | 電池電圧監視 | 分圧/保護/逆給電防止/セル保護との整合 |
| GP27 | 32 | ADC_SYS | BQ25185 SYS監視 | 分圧/ノイズ/保護 |
| GP28 | 34 | ADC_5V | 5Vブースト監視 | 分圧/逆給電防止 |
- **既存21本+GP16の5V_ENで22本/26本を使用する方向**。GP17/GP18はオプション、GP19/GP22は予備。オプション全実装なら24本使用、予備2本。GP15の5V_OKは選択部品の有無で削減可能。
- GPIOの機能割当はRP2350の利用可能ペリフェラルと重複していない。ただしPCB配置・信号品質・実装しやすさで変更可能。
- GP26–GP28の外部ADCは3.3V範囲のピン入力定格・ADC精度を厳守。分圧器は未給電時のGPIOクランプ経由の逆給電と常時損失を防ぐ構造で設計。入力低抵抗化で常時電池消費を増やさない。
- GP29内部のVSYS監視をADC_SYSとして流用すると、**外付けショットキー後のVSYS**でありBQ25185 SYSそのものではない。測り分けるのでGP27を確保する。

## PWR↔CTRLの暫定ネットセット
| 信号 | 方向 | 内容 | 基板間接続での注意 |
|---|---|---|---|
| SYS_TO_MCU | PWR→CTRL | BQ25185 SYSからPico VSYSの外付けORダイオードへ | **Pico VBUSには配線しない**。USBとVSYSの同時給電は公式図・実測で確認 |
| GND_LOGIC | 共通 | MCU/周辺の基準 | 電源帰路、ADC基準、ノイズ分離 |
| +3V3_PERIPH | PWR→CTRL | OLED/RTC等の周辺機器 | **Pico 3V3(OUT)へ直結しない**、I2C逆給電に注意 |
| +5V_LOGIC | PWR→CTRL | HV5524/74AHCT125等のロジック | 5V耐圧、起動時BL制御、MCU未通電時の逆給電 |
| BQ_STAT1, BQ_STAT2 | PWR→CTRL | 充電状態 | 3.3V側プルアップ、電源ドメイン間対策 |
| ADC_BAT, ADC_SYS, ADC_5V | PWR→CTRL | 安全な分圧後の監視信号 | **生BAT/SYS/5VをそのままADCへ送らない**。分圧回路をどちらのPCBに置くか未決定 |
| HV_EN_REQ | CTRL→PWR→HV | HV起動要求をPWR経由でパススルーする構成案 | PWR-HVコネクタ3極(+5V/GND/EN)との整合。PWR未接続・CTRL抜去ではOFF |
| HV_FAULT_N | HV→CTRL | OVP/PowerFaultの状態 | **PWR-HVの4極案に追加済み**。PWR経由でCTRLに通知する想定。部品型番と配線は別途検証 |
| PWR_5V_OK | PWR→CTRL | 5Vレールの妥当性 | PWR上の比較器/PG方式が確定するまでオプション |
- **コネクタのピン番号、極数、部品型番は未確定**。HV_FAULTを採用する場合はJST XH 3極をそのまま確定しない。電源・GNDの帰路、圧着品質、接続方向、誤挿入対策を先に確定。
- 高圧出力HV_OUT/HV_RETURNは別系統で、低圧コネクタに混在させない。

## 初回作業時のチェック
1. GPIO番号とPico基板の**物理pin番号**をKiCadに転記し、GP23/24/25/29を外部I/Oとして誤使用しない。
2. 74AHCT125とHV5524の電源投入順・BL極性を確認し、MCUリセットでも全消灯が維持されるようにする。
3. BQ STAT、I²CとADCの**異電源間逆給電**を確認する。3V3_PERIPHとPico 3V3(OUT)は直結禁止。
4. PWR→HVの起動信号をPWR経由で配線するか、CTRL→HV直結にするかを基板位置から決める。4極コネクタ案(+5V/GND/EN/FAULT)と各端子の安全動作を確認する。
5. 最低電池電圧からUSBデバッグ併用まで、SYS→外付けダイオード→Pico VSYSの電圧範囲とパワーシーケンスを確認。
6. 合計GPIO、コネクタ極数、台座内の配線・5V電源能力、余剰GPIOのアクセス方法を設計レビュー。

詳細なJ1/J2/J3/J4基板間配線案: [board-interconnects.md](board-interconnects.md)。

電源OFF時のバス保護とレベルシフタ候補の更新: [pwr-sequencing.md](pwr-sequencing.md)。HV5524 POL=HIGH/BL=LOWの全消灯案とRTCバックアップは[hv-blanking-rtc-backup.md](hv-blanking-rtc-backup.md)を参照。
