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
4. 必要な場合のみ5Vレール（TPS61023 EN）を有効化し、電圧良好の確認後、SN74LV4T125/HV5524の論理電源を整える。
5. **HV5524全消灯**：Microchip真理値表でBL=LOW、POL=HIGHが全OFF（BL=LOW、POL=LOWは全ON）。POLを5Vにプルアップして固定、BLをGNDへプルダウンする案。ロジック5V安定→全ゼロデータ書込み・ラッチ→必要時のみBL=HIGH。電源不安定時はHV電源の起動をハード側で禁止。詳細は[hv-blanking-rtc-backup.md](hv-blanking-rtc-backup.md)。
6. ユーザー要求と電源余力、HV OVP/FAULTの正常を確認して、HV_EN_REQを許可する。
7. HVを使わないときは、HV出力全消灯→HV_EN OFF→bleederで残留電荷放電。必要なら5VレールOFF（ただしRTC/OLED/MCUからの逆給電を監視）。

## デフォルト状態の部品・ネット案
| 信号 | 仮のデフォルト | 必要な外付け設計 |
|---|---|---|
| HV_EN_REQ | OFF (LOW案) | **HV基板側**プルダウン/論理AND with independent OVP; 3.3V GPIO直結の耐圧と過渡を確認 |
| TPS61023_EN | OFF | PWR基板側プルダウン。MCUから制御するルートと5V供給前のGPIOが3.3V有効であることを検証 |
| TPS63031_EN | ONまたはOFF（要件待ち） | RTCを常時動かすかバックアップ電源に委ねるかで決定。Picoが3.3V独立動作できることが前提 |
| HV5524_BL/LE/CLK/DATA | **起動時全OFF** | **BL=LOWかつPOL=HIGHで全OFF、POL=LOWなら全ON**。5V VDDなしでの出力状態は保証しないためHV昇圧禁止と放電/接触防止を独立に設計 |
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

## 2026-11-14更新：異電源ドメインのIoff対策と必要部品の最小化

**重要変更**: HV5524制御信号4chの3.3V→5Vシフタ第一候補を**SN74AHCT125からSN74LV4T125へ変更する案**。TI SN74AHCT125はTTL互換入力(VIH≥2V @ VCC4.5–5.5V)を持つが、一般製品のdatasheetに明示された**partial-power-down Ioffの保証を現時点で確認できていない**。一方TI SN74LV4T125は3.3→5V変換とIoff動作が明示されている。
- SN74LV4T125 VCC=+5V_LOGIC, A0..A3=Pico GP0..GP3, Y0..Y3=HV5524 DATA/CLK/LE/BL。**OEはactive-low**。電源投入/停止中に全出力を無効化できるよう、OEの既定レベルと有効化条件を回路で定義する。出力ハイインピーダンス中にもHV5524の入力は**浮かせない**。BLの極性・必要なプル抵抗/ドライバ電源OFF時動作をHV5524メーカー表で別途確定。
- Ioffによる「VCC=0での漏れ防止」と「5V供給が立上るまで表示全消灯」は**別の要求**。後者はHV5524ブランキングのハード初期状態、OVP/ENのハードOFF既定、給電順で成立させる。
- 旧SN74AHCT125の例を使い続ける場合は**品番個別のpowered-off input/output leakage**、Pico 3.3V→非給電5Vへの電流注入を測定・評価。単にPico GPIO=LOWのソフト制御ではMCU reset中の安全性は保証できない。
- TI一次資料 SN74LV4T125 https://www.ti.com/lit/ds/symlink/sn74lv4t125.pdf , SN74AHCT125 https://www.ti.com/lit/ds/symlink/sn74ahct125.pdf

### RTC/OLED I2Cと3.3V電源の整理
- **基本案（安価）**: RTCとOLEDを電源OFF中もPicoからI2Cアクセスしたいなら、Pico 3V3(OUT)を周辺の基準電源とする方式と、RTCバックアップ電源の要否を比較する。ただしTPS63031の独立3.3Vと混結しない。OLEDを常時給電すると待機電力/スリープ時間が増える可能性がある。
- **電源分離案**: Pico 3V3が生きていて3V3_PERIPHが落ちるなら、I2CのSDA/SCLに**TCA39306**などのEN付き分離素子を候補とする。EN=LOWでI2C両側がHi-Zとなるが、**その電源OFFシーケンスとENのレベル、各側pull-up位置、無電源時の内部漏れ**をICの仕様で照合する。両側3.3Vで単なるレベル変換は不要だがバス分離目的で検討可。
- OLEDとRV-3028-C7の**基板モジュール上の内蔵プルアップ**が別電源に接続されている場合は、追加抵抗の有無で問題解決しない。OLEDの製品実機回路図/モジュールのプルアップを確認。RTC VBACKUPの供給も未確定。
- 低コスト第一方針は**RTCをタイマー保持用の常時/バックアップ電源ドメインに置き、OLEDは表示負荷として別扱い**。RTCとOLEDを無条件に同一スイッチ式レールに乗せる旧ブロック図を確定回路として扱わない。

### BQ25185充電状態 STATx
- TI BQ25185 STAT1/STAT2は**open-drain**、1kΩ～20kΩのpull-up、pull-up最大5V。まずPico側3V3(OUT)へ例えば10kΩ pull-upする案（TI範囲内）で、Pico給電中の読み出しを成立させる。BQ側未給電時のリークと論理状態が許容されることをメーカーの絶対最大定格・電気特性で別途確認。
- STATは充電状態通知で**安全遮断に使用しない**。BQ25185の充電許可/温度保護・電池保護はハード依存とする。open-drainの出力Highは必ずしも「充電している」の意味ではないためtruth tableに従って処理。
- TI一次資料 https://www.ti.com/lit/ds/symlink/bq25185.pdf

### ADC監視の逆給電
- BAT/SYS/5V分圧後のGP26/27/28について、**Pico電源OFF時に入力が高いままになり得る**ことを検証。未給電Picoの絶対最大/入力注入電流を超えないよう、分圧高抵抗化、Pico側電源連動アナログスイッチ/enable、保護を比較する。
- 3.3V GPIOの電流/保護ダイオードが耐えるから安全と**推測しない**。最終方式はPico公式の絶対最大定格と、電池常時リークから決める。

### GPIO予約案
- GP16: PWR_5V_EN（TPS61023 EN、PWR側プルダウンで既定OFF）。
- GP17: ADC_SENSE_EN（PWR Rev.A v3のJ3 pin10へ。PWR側R24=100kΩでLOW既定）。
- GP18: 予備。旧PWR_3V3_EN案は現行Rev.Aでは採用しない。
- この節は旧検討案を含む。現行第一候補は[統合ネット仕様](reva-integrated-net-spec.md)のGP17=ADC_SENSE_EN、J3=10極。GP18のPWR_3V3_EN案も現行Rev.Aには含めない。保護回路は予算調整で省略しない。

### KiCad設計の優先順位
1. レール（Pico 3V3(OUT)、SYS、PWR 3.3V、5V LOGIC）の**電源ツリー/ドメイン**を確定。
2. SN74LV4T125の個別型番・footprint/EN/OE挙動・Ioffの最大値・HV5524制御入力の全消灯回路をメーカー仕様と照合。
3. RTC・OLED実物のI2C pull-upとバックアップ方式、TCA39306採否を決める。
4. BQ_STATx/ADCのバックパワー計測と漏れ電流、USB同時電源シナリオを試験。
5. 5V_ENと3V3_ENのGPIO/配線本数を接続表・実回路図に反映してからPCBを発注する。

