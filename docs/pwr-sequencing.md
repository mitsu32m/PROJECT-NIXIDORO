# PWR電源投入・停止・逆給電防止 — Rev.A設計方針 v0.1
Updated: 2026-11-14 JST
Status: PROPOSED / TO_VERIFY。**回路方式案でありPCB発注・電気安全合格を意味しない。**

## 目的・重要な結論
1. **Pico 2はBQ25185のSYSからVSYSへ独立の逆流防止経路で給電**し、USBデバッグとの電源ORingを維持する。Pico VBUSにPWR 5Vを直結しない。
2. **高電圧電源はデフォルトOFF**。Pico初期化・HV5524のブランキング/5Vロジックが安全状態になった後だけHV_EN_REQを有効にできる。
3. **5V昇圧のENは高電圧安全停止の代用にしない**。HV基板の独立OVPとHV_ENハード停止回路が優先。
4. **TPS61023にはシャットダウン中の入力と出力の真の切り離し（true disconnection）**がメーカー資料に明記されている。以前の「EN=LOWでVOUTがどうなるか未確認」はこの点を訂正。ただし出力コンデンサの残留電荷、GPIOや他経路からの逆給電は止めない。
5. 周辺3.3VレールとPico 2の3V3(OUT)を直結しない。電源ドメインを跨ぐI2C/STAT等でGPIOの保護ダイオードから逆給電が起こり得る。

## ドメインと電源の許可条件
| ドメイン | 接続先 | 通電方針 | 逆給電・異常対策 |
|---|---|---|---|
| USB_PROTECTED | BQ25185 IN | USB接続中のみ | VBUS ESD/入力保護、CC広告/入力制限、USBから電池への経路は充電IC制御 |
| BAT | 保護付き21700/BQ BAT | 常時または保守切離し | 保護付きセル、セルNTC、逆挿入禁止 |
| SYS | BQ SYS | USB/電池が有効なら可 | 他レールからSYSへの逆流を回路ごと検討 |
| PICO_VSYS | Pico 2 VSYS | SYS→外付けダイオードOR、内蔵USB→D1 OR | Pico 2 VBUSへPWR 5Vを注入しない |
| PERIPH_3V3 | TPS63031 | RTC/OLEDの制御要求に応じON候補 | Pico 3V3(OUT)との直結禁止、信号線逆給電を確認 |
| LOGIC_5V | TPS61023 | 原則Picoが有効化した時のみON | 真のshutdown disconnectはTIで確認。残留Cと他経路からの逆給電は別 |
| HV_200V | MAX668 | 5V良好＋表示制御初期化＋ハード保護正常＋表示要求時のみ | HV側デフォルトOFF、独立OVP/放電/接触防止 |

### メーカー資料で確認できた機能
- **TPS61023** にはTrue disconnection between input and output during shutdown、ENによるshutdown、5.7V級出力OVPが仕様としてある。ENを切った直後の5V負荷側Cが直ちに0Vになるという意味ではない。https://www.ti.com/lit/ds/symlink/tps61023.pdf
- **TPS63031** のEN=0は無効、EN=1は有効。PS/SYNC=LOWでpower-saveを選ぶ。PS/SYNCは有効化端子でなく運転モード端子。https://www.ti.com/lit/ds/symlink/tps63030.pdf
- **BQ25185** SYSはUSB/電池パワーパスであり、USB側の電力不足時に充電電流低下→電池補完する。電池がBUVLOより低いと補完不可。https://www.ti.com/lit/ds/symlink/bq25185.pdf
- **Pico 2** はUSB VBUS→内蔵ダイオード→VSYS、外部電源→外付けダイオード→VSYSという公式推奨ORingがある。https://datasheets.raspberrypi.com/pico/pico-2-datasheet.pdf

## 電源投入のシーケンス（設計要求。時間値未確定）
1. USB-Cまたは電池でBQ25185 SYSを生成。Pico 2 VSYSへ電源が供給される一方、**TPS61023 EN/HV_ENはプルダウン等で既定OFF**。TPS63031のEN既定状態はRTC/OLEDの要件に合わせて設計する。
2. Pico 2が起動し、電圧/温度/充電状態など、無通電でも安全な測定系を確認。BOOT_SAFEの間HVはOFF。
3. 必要なら周辺3.3Vを起動。I2Cバスのpull-upをどの3.3Vドメインにつなぐか確定し、未通電周辺からの逆給電を防止する。
4. 必要な場合のみ5Vレール（TPS61023 EN）を有効化し、電圧良好の確認後、74AHCT125/HV5524の論理電源を整える。
5. **HV5524全消灯**を保証するBL/POL/LE/シフトデータ初期化を行う。ロジック電源不安定時はブランキングを外部ハードで維持。
6. ユーザー要求と電源余力、HV OVP/FAULTの正常を確認して、HV_EN_REQを許可する。
7. HVを使わないときは、HV出力全消灯→HV_EN OFF→bleederで残留電荷放電。必要なら5VレールOFF（ただしRTC/OLED/MCUからの逆給電を監視）。

## デフォルト状態の部品・ネット案
| 信号 | 仮のデフォルト | 必要な外付け設計 |
|---|---|---|
| HV_EN_REQ | OFF (LOW案) | **HV基板側**プルダウン/論理AND with independent OVP; 3.3V GPIO直結の耐圧と過渡を確認 |
| TPS61023_EN | OFF | PWR基板側プルダウン。MCUから制御するルートと5V供給前のGPIOが3.3V有効であることを検証 |
| TPS63031_EN | ONまたはOFF（要件待ち） | RTCを常時動かすかバックアップ電源に委ねるかで決定。Picoが3.3V独立動作できることが前提 |
| HV5524_BL/LE/CLK/DATA | **起動時全OFF** | BLの論理極性・POL・電源シーケンスをHV5524 datasheetで確認し、電源不安定でも全消灯 |
| PWR_STATUS/FAULT | 通信不可時もHV安全停止 | OPEN DRAIN方式、未通電GPIO逆給電、配線断の検知/ハード停止要件 |
| BQ25185_/CE | 充電を許可/禁止する設計値 | 電池NTC・USB入力と整合。MCU起動を前提にせず、充電の単独動作を検討 |

## 逆給電テスト行列
| 給電条件 | 確認項目 | 合格観点 |
|---|---|---|
| BATのみ | SYS→Pico VSYS、5V/3.3V起動 | 望まないHV起動なし。セル電圧/5V電力の最低条件を満たす |
| USB入力のみ・セル低電圧 | BQ SYS/Pico起動と充電 | BAT低電圧保護に依存した予期しない起動/遮断なし |
| Pico 2 USBデバッグのみ | Pico 3V3→PERIPH_3V3/5V/ADCの漏洩 | MCUから周辺ICやSYSを逆給電しない（安全に規定した例外は除く） |
| BAT＋Pico USB同時 | VSYSの電圧/逆流電流、Pico USB VBUS | 外部SYSがPCポートへ逆流しない、PC USB電圧をPWRに混ぜない |
| BQ USB-C＋Pico USBを別々に接続 | グランド/ケーブル電流、SYS電圧・USB電流の合計 | USB間の誤逆流、過電流やMCU異常リセットなし |
| 5V=OFF / Pico=ON | GP0-3,GP4と5Vロジックの供給 | 74AHCT125/HV5524のVCCにGPIO経由の有意な逆給電が生じない |
| 3V3_PERIPH=OFF / Pico=ON | I2C pull-up、ADC、STAT | OLED/RTCへ信号ライン経由の逆給電・電池への戻りなし |
| MCUリセット・CTRL抜去 | HV_EN とHV5524 BL | 常時OFF、独立OVPの機能は失わない |
| 5V負荷の急変・USB抜去 | SYS, VSYS, 3V3,5V, HV_EN | brownoutで不意にHV再起動しない。異常なら安全停止 |

### 注意：ADCの測定分圧
- BAT/SYS/5Vの高い測定電圧をMCU GPIOへ直接接続しない。分圧器の常時電流・ノイズ・ADC入力許容と**MCU停止時の分圧上側からGPIOへの注入電流**を検討する。
- GPIO保護のため、シリーズ抵抗/アナログスイッチ/電源連動の測定方式を比較し、電池監視を犠牲にしない低消費電力方式を選定する。

## 回路図完成前の未解決ゲート
1. **TPS61023_EN**をどのGPIOで操作するか（既存GP割当21/26本との整合、予備GP使用の可否）。
2. **TPS63031_EN**の常時ON/スイッチ式方針とRTCのバックアップ電源の両立。
3. 74AHCT125の**powered-off I/O電流と保護機能**を個別型番で確認し、電源順序上の信号レベルを定量化（AHCT125一般名だけでは電源OFF時フェイルセーフは証明できない）。
4. HV5524のBLアクティブレベルと、レール停止時・ロジック不定時の出力状態をメーカー表で確認。
5. 電源ドメイン間のI2Cレベル/プルアップ/STAT/ADCの具体的保護回路と部品数・費用、5V railの切断後の残留電圧。
6. USBデバッグ、外部USB充電、電池の3電源組合せでスコープ波形・逆流電流を評価。
7. HV基板の独立OVP/bleederと、高電圧触れ防止・保護付き電池/温度評価を教員レビューしてから実機HV通電。

関連: [PWR schematic net list](pwr-schematic-nets.md), [Pico GPIO](pico2-pinmap.md), [電源状態遷移](power-state-machine.md)
