# CTRL Rev.A OLED・操作部・通知音の接続ドラフト

> **2026-11-14 Rev.A電源構成の第一候補更新:** RTC・OLEDはPico 2の3V3(OUT)へ統合、アンプはSYS給電＋SHUTDOWNとし、TPS63031とI²C分離ICを削減する案を追加。**実測/発注前検証未了**。詳細：[CTRL電源ドメイン統合案](ctrl-power-domains.md)。以下に残る3V3_PERIPHや分離構成は従来案・比較対象。

Updated: 2026-11-14 JST
Status: PROPOSED / NOT FOR FABRICATION。手配前に各部品の実物ピン配置、ドメイン間逆給電、音量と実装寸法を試験する。

## 目的と境界
この文書は[HV5524/RTC配線ドラフト](ctrl-driver-rtc-schematic.md)を補完する。Pico 2の既存GPIOを優先利用し、ネオン/ニキシーの200V系とは完全に別の低圧ユーザー操作回路として配線する。
- 入力は静的な機械接点、3.3Vロジック/GNDのみに限定。HV出力・5V負荷回路と同ハーネスに混在しない。
- 実コネクタのピン番号（部品の物理端子）・実フットプリントはCAD/部品個別図面確認後に確定。

## 1. Pico 2 GPIO割当
| ネット | GPIO | GPIO物理pin | 先 |
|---|---|---:|---|
| UI_ACTION_N | GP8 | 11 | OBSF-30 N.O.接点→GND |
| UI_NEXT_L_N | GP6 | 9 | M-N18S1W 左投端子→GND (中央共通) |
| UI_NEXT_R_N | GP7 | 10 | M-N18S1W 右投端子→GND (中央共通) |
| ENC_A_N | GP9 | 12 | EC11E15244G1 A相→GND (common) |
| ENC_B_N | GP10 | 14 | EC11E15244G1 B相→GND (common) |
| ENC_SW_N | GP11 | 15 | EC11E押込みN.O.→GND |
| AUDIO_PWM | GP12 | 16 | RC/アナログ信号生成→TPA2005D1入力 |
| AUDIO_AMP_EN | **GP19** | 25 | TPA2005D1 SHUTDOWN（HIGH運転、LOW shutdown） |
| I2C_SDA | GP20 | 26 | OLED + RV-3028-C7 |
| I2C_SCL | GP21 | 27 | OLED + RV-3028-C7 |

**GP19をアンプ停止制御に使う追加提案**。音をなくす案ならGP19は予備に戻せる。GP12 PWMだけではClass-Dアンプの消費とポップ音を低く保つ要求を満たせない可能性がある。

## 2. ACTION / NEXT / Encoder 電気回路
- ACTION: Pico入力→3.3Vプルアップ（GPIO内部pull-upを第一案、外付け10kΩを評価用フットプリントとして残す）・N.O.→GND。3.3V信号に5Vを印加しない。
- NEXT M-N18S1W: メーカー形名は**SPDT (ON)-OFF-(ON)**、左右どちらへ倒しても戻る。**中央COM→GND、左右2端子→GP6/GP7**。左右に個別プルアップ。誤操作のUndoはアプリ側UI仕様と合わせる。接点のメーカー端子番号/上下方向/はんだラグは現物測定で確定。
- EC11E15244G1: **30 detents / 15 pulses / 2-phase A-B / push-on switch**。A/B→GP9/GP10、共通→GND、push switch→GP11/GND。実端子位置はAlps Alpine寸法図から確認し、単なる図の端子並びを推測しない。各信号にプルアップ。
- デバウンス: 機械接点のバウンスはGPIO割込みだけで解決しない。ACTION/NEXT/SWは例えば5–15ms程度のソフトウェア安定判定を初期候補とし実測で調整。ENC A/Bは二相状態遷移（00→01→11→10など）の有効な遷移だけ数えて、クリック数とパルス数の関係を実測。強いコンデンサでA/Bを鈍らせると方向誤検知し得る。
- EMI/ESD: スイッチまで長い配線をする場合はシリーズ抵抗(例100–330Ω)・小容量C/ESDを**必要に応じて**実装。GND/信号のツイスト・引回し、筐体外からの手による静電気、過剰な入力リークを確認。
- 接点定格: M-N18S1Wは銀接点で定格電力が大きい。一方**3.3Vと微小GPIOプルアップ電流での接触安定性/最低負荷**は別問題。長期間の誤接触が懸念される場合は微小電流対応金接点スイッチを比較し、UIでの信頼性を実測する。
- 端子絶縁: 金属ノブ/トグルは外部から触れられるので、露出金属に200V系が触れない機構、基板接地/ESDをレビュー。

## 3. OLED Adafruit #938: I2Cと電源
- メーカー掲載: **1.3インチ 白色128×64 SSD1306**, 既定I²C、7bit address **0x3C/0x3D**、基板**35.6×33mm**、VINには3/5V対応のオンボード3.3Vレギュレータ/レベルシフトがあり、基板自体にはSTEMMA QTコネクタを持つ。メーカー製品ページのピン表/基板Revを調達時に確認して配線する。
- **更新後の第一候補はOLED VIN→Pico 3V3(OUT)、GND→GND、SDA→GP20、SCL→GP21**。旧案の+3V3_PERIPH給電は比較対象として残す。ただしPico 3V3(OUT)でRTCを駆動する既存方針では**電源ドメインが異なる**。
- 重要：OLEDの3V3_PERIPHをOFFにしても、Pico SDA/SCLに3.3Vプルアップがある場合、OLEDモジュールのI/Oクランプ経由で逆給電が発生する可能性がある。**ボードのレベルシフタ・プルアップ・ESD構造を実機回路図で確認**し、原則「バス絶縁が必要ならI2C ENスイッチ」「絶縁が高価ならOLEDをPico側3V3へ統合（表示OFF電力を実測）」の2案を選択する。混線したままPCB完成扱いしない。
- レイアウト: スモークPMMA窓の透過率とOLED可視領域、コネクタ奥行き35.6×33mm、高さとネジ穴を3D CADで照合。5V表示ドライバ・MAX668高周波SW/200V HVから距離を取る。
- 消費電流: 製品説明は表示内容依存、平均約40mAと記載、実用時25mA程度の説明もある。**定格/最大は計測条件が異なる**ためOLED点灯最大パターンと表示OFFの電流測定で最終予算化。
- 正規部品を使わずOffice-K等のSH1106 OLEDに変更するなら、**コントローラと電源・I2C pull-up・配線図も変更**する。代替品のピン番号をAdafruit品から流用しない。

## 4. 通知音：TPA2005D1（オプション）
- TIの**TPA2005D1は2.5–5.5Vのアナログ入力、BTL filter-free Class-Dモノラルアンプ**。8ΩスピーカーとBTL出力2端子を接続し**どちらもGNDへ落とさない**。3.3V電源で最大1.4Wと解釈しない（1.4Wは5V/8Ω/THD10%のメーカー条件）。
- **Pico GP12 PWM→ローパス/AC結合/入力ゲイン設定→IN+/IN−の適切な片側信号入力回路**（メーカー典型接続を基準に抵抗・コンデンサを確定）。生PWMをそのまま入力せず、アンプ入力同相電圧/不要DCを確認。
- **Pico GP19→SHUTDOWN**。TI仕様上 LOWでshutdown、HIGHで運転。10–100kΩ程度のGND pull-downを初期案としてPCBに置き、MCU起動中はアンプ停止。通知時は音信号を整えてからアンプON、停止時はフェード/ミュート後OFF。起動・電源断ポップ音を実機で確認。
- **第一候補：アンプVDDをBQ25185 SYSから供給**し、GP19でSHUTDOWN制御する（LOW=OFF）。GP19がHIGHでもSYS無通電の場合に入力からアンプを逆給電しない保護・ゲーティングを要検証。SYSでの出力・ノイズとスピーカー最大入力を測定。
- 非使用時はアンプ電源/SHUTDOWNを下げ、必要に応じて低価格の圧電ブザー単独案と比較（アンプとスピーカーのコスト/PCB面積/消費が削減）。
- アンプICの正式フットプリント、VDDデカップリング、IN+/IN−入力ネットおよび熱設計は**TI datasheetの適用回路から転記**し、パッケージとピンアサインを未検証のまま固定しない。

## 5. 試験・合格ゲート
| 内容 | 試験 | 合格観点 |
|---|---|---|
| ACTION/NEXT | 操作100回程度、チャタリング/同時押し | GPIOの誤判定なし、UndoのUX |
| Encoder | 低速/高速回転、15ppr/30detents整合 | 正逆・クリック検出の欠落/ダブルカウントなし |
| OLED I2C | RTC共存、アドレス・プルアップ実測、OLED OFF | NACK処理が成立、**OLED OFFでも他デバイスへの逆給電なし** |
| OLED外観 | 19%と高透過率スモーク窓の比較 | 明室で視認、OFF時に隠れる |
| AUDIO | 音量/歪み、電源OFF→ON、無負荷/8Ω | 不快なポップ音なし、電池電流と熱が許容範囲 |
| SYS/HV EMI | MAX668ダミー負荷時のみ教員安全レビュー後 | I2Cリセット/接点誤検出、音声混入がない |
| 予算 | OLED正規/代替、アンプ/圧電 | 50,000円総額、再試作費・送料を別計上 |

## 6. 実装前の残件
1. **OLED電源分離/バス絶縁**を選び、RTCの3V3ドメインと矛盾を解消する。
2. 機械部品のピン配置、ねじ/穴/ノブ干渉、半田端子位置はCAD・現物で確定。
3. TPA2005D1の具体的フィルタ/Rin/Cin/SHUTDOWN/出力負荷をメーカー例から確定。アンプを実装するか判断。
4. GPIO GP19の追加を既存ピンマップへ反映し、変更があれば他のシートを整合。
5. **高電圧の機械的隔離は別の必須安全要件**。ユーザーが触る入力端子周辺にはHVが存在しない構造とする。

## 参考
- Adafruit #938: https://www.adafruit.com/product/938
- Alps Alpine EC11E15244G1: https://tech.alpsalpine.com/e/products/detail/EC11E15244G1/
- NKK M-N18S1W: https://www.nkkswitches.co.jp/product/detailed/M-N18S1W.html
- TI TPA2005D1: https://www.ti.com/lit/ds/symlink/tpa2005d1.pdf
- [UI仕様](ui-spec.md) / [GPIO割当](pico2-pinmap.md) / [表示ドライバ・RTC](ctrl-driver-rtc-schematic.md) / [電源順序](pwr-sequencing.md)
