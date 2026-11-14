# CTRL Rev.A: HV5524 + SN74LV4T125接続案 / RTCバックアップ選定
Updated: 2026-11-14 JST
Status: **PROPOSED / NOT FOR FABRICATION**。一次資料で確認したピン番号と、追加検証が必要な抵抗値・回路方式を区別する。

## 1. 先に確定できる事実
- HV5524 (44-WQFN): **BL=LOW, POL=HIGHで全HV出力OFF**。BL=LOW, POL=LOWは全ONなので禁止。DATAはCLK**立下り**でシフト、LE=HIGHでラッチ透明/取り込み、LOWで保持。HV5524 VDD=5V、GPIO3.3V直結はVIH条件を満たさない。
- SN74LV4T125: 14ピンPW(TSSOP)とRGY(VQFN)。**5V VCCで3.3V入力を5Vへ変換可能、Ioff部分電源断対応**。各チャネル個別の**/OE=LOW有効、HIGHでHi-Z**。ただしVCC=0時のY出力印加絶対最大値は4.6V（データシートの条件）。/OE制御を無電源時の絶縁手段とみなさない。
- RTC RV-3028-C7: VBACKUP, バックアップ切替・トリクルチャージ。EEPROM 37h BSM=00初期値は切替OFF、DSM=01、LSM=11。EEPROM書込・読返しをFW試験する。バックアップモード中I²Cは無効。
- 既存の記録は[hv-blanking-rtc-backup.md](hv-blanking-rtc-backup.md)、[pwr-sequencing.md](pwr-sequencing.md)。

## 2. HV5524 制御回路（初回試作の省部品案）
| Pico | U_CTRL1 SN74LV4T125 PW package pin | U_DRV1 HV5524 pin | 電気的内容 |
|---|---|---|---|
| GP0 / HV_DATA | 1A pin2 → 1Y pin3 | DATA IN pin32 | DATA線 |
| GP1 / HV_CLK | 2A pin5 → 2Y pin6 | CLK pin28 | CLK線 |
| GP2 / HV_LE | 3A pin9 → 3Y pin8 | LE pin31 | LATCH |
| GP3 / HV_BL | 4A pin12 → 4Y pin11 | BL pin33 | BL=LOW全消灯 / HIGH有効 |
| － | 1OE pin1, 2OE pin4, 3OE pin10, 4OE pin13 | － | **4つの/OEをGND固定**案。電源投入時の入力不定を避けるため各Aを100kΩ程度でGNDへpull-downする |
| － | VCC pin14 = +5V_LOGIC | VDD pin30 = +5V_LOGIC | 0.1µFの近傍デカップリング/必要なbulkを実装 |
| － | GND pin7 = GND | VSS pin29 / Center tab = GND | GND基準・センターパッドはメーカー指示に従う |
| － | － | POL pin27 → +5V_LOGIC | **10kΩ pull-up** （初期値、直接固定も比較）|
| － | － | BL pin33 → GND | **10kΩ pull-down** （初期値、MCUおよびバッファOFF時全消灯） |
| － | － | DATA/CLK/LE pin32/28/31 | 必要に応じて10〜100kΩでGND pull-down、5V停止/中途半端な電源での挙動を比較 |
| － | － | DATA OUT pin23 | 単体運用なら原則NC、取り扱いはdatasheetに従う |
- **注意**: 4つの/OEをGND固定した構成は、5Vが有効ならA入力を100kΩ pull-downして全出力LOWに導く、部品点数を抑える案。**GP3が誤ってHIGHになるファーム不具合・GPIO故障、5Vのブラウンアウト中は安全保証なし**。重要な安全停止はHV_ENの独立ハードゲート/OVPが担う。
- **初期化手順**: HV_EN=OFF固定→5V rail good→BL=LOW確認→DATA=0を32bit CLKの立下りで送信→LE=HIGHでラッチ→LE=LOW→必要なデータ更新→要求時にBL=HIGH→HV_ENを許可。POL=HIGHなので論理1がONかどうかを低圧治具で確認する。
- **選択肢**: 「/OEを起動時HIGH→許可時LOW」方式は出力状態をHi-Zにするため、Y側のプル抵抗と/RST信号、トランジスタが増える。**製品初期版はシンプルなAプルダウン案を優先検証**し、低圧試験で不合格なら/ OEのゲーティングと5V GOODのANDゲートを追加。
- **故障試験**: MCU reset/リフラッシュ/Pico無給電だが5Vあり/5Vのみ遮断/HV_EN切断/GP3 HIGH stuckを想定。HVを実印加する前に電源OFF時/起動時のロジックピン波形・漏れを低圧で検証。
- 出力カソード先には個別制限抵抗/配線間隔を設計し、**出力OFFを200Vの危険電位が消えたと誤認しない**。

### 後から確認する重要点
1. HV5524真理値表ではBL=LOW POL=HIGH All Off。**VDD<4.5Vや未給電時の出力状態は保証されない**。HVの独立起動禁止、放電、カバーが必須。
2. 10kΩ/100kΩ値は**設計提案**。GPIO漏れ・静電気・PCBノイズ・高温を見た実測で調整。
3. 単一5VのHIGHを出力するLV4T125と、電源OFF時にHV5524入力に寄生電流が流れる経路を試験。
4. SN74LV4T125PWRは**TSSOP-14**。手はんだ/学校リフローでの実装負荷がRGYR VQFN版より低い可能性がある。HV5524自身はWQFN-44でリフロー前提。

## 3. RV-3028-C7 の供給とバックアップ
### 仕様・目的
- 主電源 **RTC VDD = Pico 2 3V3(OUT)**、共通I²C (GP20/GP21、SDA/SCL pull-upはPicoの3V3ドメイン)。OLEDをスイッチ式+3V3_PERIPHへ置くならOLEDへの逆給電は別途遮断。
- **電池交換など数分〜数十分**の時刻保持を初期要件として提案。「数日間」はユーザー要求として未確定なので、現段階で大型スーパーキャパシタを注文しない。
- **RTC VBACKUP初回比較候補: Murata GRM32ER71A476KE15K（47µF、10V、X7R、1210）×1～2個を並列**。電圧・温度・公差・DCバイアス下の有効容量/漏れ電流を確認。備考: 10Vで使用してもVBACKUPに10Vをかけない（RTC入力最大5.5V）。
- バックアップを**絶縁したVBACKUPに接続**。内蔵トリクル設定をFWで有効にする場合は正しいTCR設定と充電電圧・充電時定数を確認。新規基板ではRTCのVBACKUPに**評価用端子と比較キャパシタ実装フットプリントを2つ**用意。
- RTCのトリクル充電を無効のままにするとVBACKUPコンデンサは自動的には充電されない。EEPROMのBSM/FEDE/TCE/TCRと、起動ごとの設定読出/永続化/書込み回数制限をFW仕様に組み込む。
- **断電時間の理想式**: t≈C_eff×(Vstart−Vmin)/I, C_eff=47µFを仮置き、Vstart=3.0V, Vmin=1.1V, I=45nA → 約33分。2個94µFなら約66分。現実にはC_effが下がり、温度/漏れ/スイッチオーバーで短くなる。**メーカー保証の保持時間ではない**。
- スーパーキャパシタ (10mF〜0.1F) は、日単位バックアップ要件とリーク実測が確定してから再検討。一次コイン電池は数日〜年単位保持向け比較案だが、TCE=OFFにし絶対に充電しない。
- 基板で100µF近辺の低漏れMLCCを置くよりも、**実測した最低有効容量・漏れ・ホールド時間**で合否を判断する。PCBは部品が載らない状態でもRTCのVBACKUPを測定・交換できること。

## 4. 初回試験と合格ゲート
| 試験 | 方法 | 暫定合格条件 |
|---|---|---|
| データ/ブランキングの論理 | HVなし・5Vのみ | POL=HIGH/BL=LOWで全OFF、32bit更新後のみ選択出力ON |
| MCU reset/GP未駆動 | 5V残してPico reset、各AとBLを測る | BLがLOW、HV_ENは常時OFF |
| レベル変換器無給電 | PicoのGPIO状態を変化 | 5V railsの不意の電圧/発熱上昇なし、絶対最大・Ioff内 |
| RTC設定 | EEPROM 37hの書込/読返しとI²Cアクセス | BSMモード・トリクル設定が期待どおり、backup中I²C停止を許容 |
| RTCバックアップ | 主3.3V停止・充電済キャパシタから保持後復電 | 初期目標**5分以上**（提案値）、日時を継続。周囲温度/セル未装着などの条件を記録 |
| 長期保持 | 低温/高温でVBACKUPを測定 | 5分未達なら容量・損失・切替方式を再設計 |
| HV安全 | 教員レビュー後の高電圧使用、試験治具 | 5V喪失/MCU不具合でもOVP/起動禁止/放電/カバーが成立 |

## 一次資料
- Microchip HV5524: https://ww1.microchip.com/downloads/aemDocuments/documents/APID/ProductDocuments/DataSheets/HV5524-32-Channel-Serial-to-Parallel-Converter-Data-Sheet-DS20006850.pdf
- TI SN74LV4T125: https://www.ti.com/lit/ds/symlink/sn74lv4t125.pdf
- Micro Crystal RV-3028-C7 app manual: https://www.microcrystal.com/fileadmin/Media/Products/RTC/App.Manual/RV-3028-C7_App-Manual.pdf
- Murata GRM32ER71A476KE15: https://search.murata.co.jp/Ceramy/image/img/A01X/G101/ENG/GRM32ER71A476KE15-04CA.pdf
- DigiKey part GRM32ER71A476KE15K: https://www.digikey.jp/en/products/detail/murata-electronics/GRM32ER71A476KE15K/16033394
