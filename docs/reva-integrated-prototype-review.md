# PROJECT-NIXIDORO Rev.A 三基板統合・試作準備レビュー

2026-11-15。基点 `codex/pwr-reva-v3-review`、統合ブランチ `codex/reva-integrated-prototype-review`。**PCB製造・発注・高電圧印加の許可資料ではない。** 元の[PWR v3](../hardware/pwr/RevA-draft-v3/)は保存し、[PWR統合版](../hardware/pwr/RevA-integrated-draft/)、[HVドラフト](../hardware/hv/RevA-draft/)、[CTRL/DISPドラフト](../hardware/ctrl/RevA-draft/)を別に作成した。回路図生成スクリプト、KiCadネットリスト、ERC原文を各ディレクトリに保存。

## 結論と検証状態

| 基板 | 判定 | KiCad 10.0.4 ERC | 意味 |
|---|---|---:|---|
| PWR | **重要な未解決事項があり、設計変更候補** | 統合版0 error / 0 warning | J5を3線電池・セル搭載NTCへ修正。16mA連続時の熱、セル、コンデンサ実効容量、コネクタ、USB入力条件は未証明。旧v3は変更なし |
| HV | **重要な未解決事項があり、設計変更候補** | 2 error / 7 warning | MAX668の確認済みピンと低圧バイパスのみ。トランス・MOS・整流・FB・CS・独立OVP・放電が未選定。回路図は意図的に**昇圧しない** |
| CTRL/DISP | **重要な未解決事項があり、設計変更候補** | 3 error / 5 warning | Pico、シフタ、HV5524、RTC、任意アンプの確認済みピンと論理割当。RTCバックアップ、音声入力、表示管の実端子、/OE解除回路が未完成。HV表示は許可しない |

ERCの未解決エラーは消したふりをしていない。HVはFB/CSの未駆動、CTRLはRTC VBACKUPと音声アンプ入力2本の未駆動を示す。PWRのERC 0件も、電気安全・熱・機械適合を保証しない。[ネットリスト自動照合](../hardware/integration/verify-integrated-netlists.py)はJ3の全10ピン、PWR J5 pin3、CTRL GP17 pin22、HV5524全32出力、HVの停止状態を確認した。

## Phase 1 — HV電源

[ADI MAX668 Rev.3](https://www.analog.com/media/en/technical-documentation/data-sheets/MAX668-MAX669.pdf)は3～28Vで動作し、非ブートストラップ方式ならコントローラの出力電圧自体に28V制約はない。pin1=LDO、2=FREQ、3=GND、4=REF、5=FB、6=CS+、7=PGND、8=EXT、9=VCC、10=SYNC/SHDN。FREQの200kΩは`f≈5×10¹⁰/R≈250kHz`の初期候補。1µF LDO、0.22µF REF、0.1µF VCCのバイパスはメーカー推奨。FB=1.225/1.250/1.275V、CSしきい値85/100/115mV（min/typ/max）。MAX668EUB+Tは10ピンµMAX。KiCad MSOP-10 3×3mmを暫定選択したが、**uMAXの推奨ランド寸法との一致は未検証**。

**5V→205Vの単純な一段ブーストはMAX668では成立しない。** 理想的にも`D=1−5/205=97.56%`が必要で、MAX668最大デューティは発振抵抗200kΩ条件で87/90/93%（min/typ/max）。トランスを用いるフライバック、検証済み高圧モジュール、または二段構成を比較する。効率と費用を実測/見積で比較するまで方式を決めない。

旧資料の`TTRN-060S-013-T`は[JLCPCBの掲載](https://jlcpcb.com/partdetail/JLCPCBAssembly-TTRN_060S_013T/C9900124494)でSMD-5Pと分かるが、メーカー電気仕様（Lp、巻数比、Isat、漏れインダクタンス、絶縁耐圧、温度・熱抵抗）を確認できなかった。掲載フットプリントをトランスの適合証拠にしない。フライバックの設計には`Ipk≈√(2Pin/(Lp f))`（DCM近似）、MOS `VDS≈VIN+(Np/Ns)(VOUT+VD)+漏れサージ`、整流ダイオードの逆耐圧・回復損失、スナバの漏れエネルギー、CS抵抗`RCS≈0.085/Ipk,max`（minしきい値で早期制限を評価）などを**実トランスの条件**で求める必要がある。数式だけではFET・ダイオード・RCS・スナバを確定できない。

205V×16mA=3.28W。ηHV=80/70/60%仮定なら5V平均入力は4.10/4.69/5.47W（0.82/0.94/1.09A）、HV電力段損失は0.82/1.41/2.19W。これは[MAX668の別回路の効率曲線](https://www.analog.com/media/en/technical-documentation/data-sheets/MAX668-MAX669.pdf)から保証される値ではない。起動時のCout充電ピーク、トランス銅損・コア損、FET、整流、スナバの配分は未算定。

MAX668のFB分圧は205V公称なら`Rtop/Rbottom=205/1.25−1=163`。FBしきい値だけで約200.9～209.1Vに振れ、抵抗公差・漏れ・起動オーバーシュートは別。CTRLの[HV5524](https://ww1.microchip.com/downloads/aemDocuments/documents/APID/ProductDocuments/DataSheets/HV5524-32-Channel-Serial-to-Parallel-Converter-Data-Sheet-DS20006850.pdf)は推奨HV出力上限220V、絶対最大230V。205V通常上限と220V推奨上限の間は狭い。**独立比較器＋HV分圧＋ハード停止＋ラッチ/復帰条件**を設計し、全公差で通常最大<OVP最小かつOVP最大<220Vを示すまでHV回路を閉じない。OVPがMCUのADC/HV5524 BLだけに依存しないこと。電源断時の残留電荷は`E=½Cout V²`、ブリーダは`V(t)=V0 exp[-t/(Rbleed Cout)]`で実容量・抵抗定格・開放故障を含め設計する。たとえばCout=10µFなら205Vで0.210J（**仮例**）。接触許可電圧・時間は安全レビューで決め、放電完了を実測する。HV側の起動許可は低電圧5V有効・SYS/セル条件・独立OVP正常のANDとし、HV基板J1 pin3開放時はLOW。現ドラフトでは`HV_EN_REQ`をMAX668 pin10へ**接続していない**。

## Phase 2 — CTRL/DISP

[Pico 2公式ピン表](https://pip-assets.raspberrypi.com/categories/1005-raspberry-pi-pico-2/documents/RP-008299-DS-2-pico-2-datasheet.pdf)に従いGP0～3をHV DATA/CLK/LE/BL、GP4=HV_EN_REQ、GP5=HV_FAULT_N、GP16=PWR_5V_EN、**GP17=ADC_SENSE_EN**、GP20/21=I²C、GP26/27/28=ADCとした。Pico pin40 VBUSは本体USBデバッグ用でPWR 5Vへ直結しない。pin39 VSYSはPWR SYSから外付けSchottky OR候補を経る。Pico `3V3(OUT)`外部負荷はメーカー推奨<300mAだがRP2350自体の電流/VSYSで変わる。OLED・RTC・I²C pull-up・追加負荷を実測する。pin35 ADC_VREFはPico内部のフィルタ済み3V3なので、本ドラフトでは3V3 OUTへ短絡せずNCとした。

[TI SN74LV4T125](https://www.ti.com/lit/ds/symlink/sn74lv4t125.pdf) TSSOP14のpin2/3, 5/6, 9/8, 12/11を4信号のA/Yへ接続、/OEはpin1/4/10/13。5V VCC pin14、GND pin7。回路図のR3で/OEをHIGH既定とし、**解除用の電源正常・MCU準備完了ゲートは未設計**。現状はシフタ停止を意図し、表示を動作させる回路ではない。BL pin33はR2でLOW、POL pin27は5V HIGH固定。[Microchip真理値表](https://ww1.microchip.com/downloads/aemDocuments/documents/APID/ProductDocuments/DataSheets/HV5524-32-Channel-Serial-to-Parallel-Converter-Data-Sheet-DS20006850.pdf)ではBL=LOW/POL=HIGHで全32出力OFF。ただしVDD=0でHV電圧が残る状態のOFF保証ではない。HV_EN停止と放電が先行する。

HV5524 pin35～44=HV1～HV10、pin1～22=HV11～HV32、pin23=DATA OUT、27=POL、28=CLK、29=VSS、30=VDD、31=LE、32=DATA IN、33=BL、露出パッド=VSS。MicrochipのWQFN44は7×7mm、0.5mmピッチ、EP5.00～5.25mm。[KiCad QFN-44 7×7 P0.5 EP5.15](../hardware/ctrl/RevA-draft/CTRL_RevA.kicad_sch)を候補にした。熱ビアの数・径・はんだ流出防止はPCB設計時に確認。

論理チャンネル割当はHV1～10=IN-12B Aの0～9、HV11～20=IN-12B Bの0～9、HV21～32=ネオン01～12。`L1`～`L32`は電気負荷の**抽象記号**であり、実管の端子番号・フットプリントではない。2本の管陽極抵抗R100/101と12本のネオン抵抗R201～212は値・定格をTODOとした。もし各管2mA、各ネオン1mAなら最大同時電流は`2×2+12×1=16mA`（**仮定**）。実管の維持電圧・点弧電圧・寿命・選別差を確認して`R=(VHV−Vlamp−Vdriver)/Ilamp`、`PR=I²R`を再計算する。高圧抵抗の許容電圧と電力の**両方**を確認し、通常0603/0.1Wを無条件に流用しない。IN-12Bとネオンのメーカー一次仕様を取得できていないため、実抵抗値や管ピンを確定しない。

[RV-3028-C7公式](https://www.microcrystal.com/fileadmin/Media/Products/RTC/Datasheet/RV-3028-C7.pdf) pin3 SCL、4 SDA、5 VSS、6 VBACKUP、7 VDDを使用。VDDとOLEDをPico 3V3ドメインに統一し、I²C pull-up 4.7kΩは候補。OLEDモジュール側のpull-upとの並列とOFF時逆給電を測る。RTCバックアップは短時間保持目標の低漏れコンデンサ案と一次電池案を比較する。Micro Crystalの[アプリケーションマニュアル](https://www.microcrystal.com/fileadmin/Media/Products/RTC/App.Manual/RV-3028-C7_App-Manual.pdf)ではVBACKUP切替・トリクルのEEPROM 37h設定が必要で、出荷時のTCEはOFF。現回路のVBACKUP源は未接続で、**時刻保持は未成立**。一次電池を採る場合はTCE=OFFを維持する。部品の漏れ・セル保持時間・交換要件を決めてから方式を固定する。

ACTION GP8、NEXT左右GP6/7、エンコーダA/B/SW=GP9/10/11をJ6/J7へ仮配線。実スイッチの端子位置・プルアップ・ESD・デバウンスと配線長は未確認。任意[TPA2005D1](https://www.ti.com/lit/ds/symlink/tpa2005d1.pdf)はpin1 SHUTDOWN (HIGH運転、LOW停止)、pin3/4 IN+/IN−、pin5/8 BTLスピーカー、pin6 SYS、pin7/EP GNDを回路図へ接続。アンプの入力2本は未完成。メーカーの単端入力例は**両入力のAC結合と抵抗**を要し、GP12 PWMを生で接続しない。SYS無給電でGP19やPWMがHIGHの時の逆給電も未試験。アンプなし構成をコスト・熱比較対象として保持。

## Phase 3 — 物理インターフェースと故障モード

**J番号は基板ローカル。** 元資料の「J4=HV出力」はPWR基板の`PWR.J4=USB-C`と衝突する。今後は`基板.J番号`を使用する。

| ハーネス | PWR側 | 相手側 | ピン順・判断 |
|---|---|---|---|
| 低圧PWR→HV | PWR.J1 | HV.J1 | 1=+5V_PWR↔+5V_HV、2=GND、3=HV_EN_REQ、4=HV_FAULT_N。JST XH 4極は寸法候補、圧着/電流/誤挿し未確認 |
| PWR→CTRL電源 | PWR.J2 | CTRL.J2 | 1=SYS_BUS↔SYS_TO_MCU、2=SYS_BUS↔SYS_TO_AMP、3=+5V_PWR↔+5V_LOGIC、4/5=GND。5極候補。アンプなしでもpin2の扱いを決定する |
| PWR↔CTRL信号 | PWR.J3 | CTRL.J3 | 1/2=STAT、3～5=ADC、6=PWR_5V_EN、7=HV_EN_REQ、8=HV_FAULT_N、9=GND、10=ADC_SENSE_EN (GP17)。全10ピンをネットリストで照合 |
| HV→表示の高圧専用 | HV.J2 | CTRL.J4 | 1=HV_OUT_TODO、2=HV_RETURN_TODO。実HV定格コネクタ・絶縁距離・露出防止は未選定。低圧JSTを流用しない |
| USB-C | PWR.J4 | 外部5V充電器 | CC1/CC2各5.1kΩ Rd、eFuse/ESD。USB広告・500mA設定・充電器条件を再検証 |
| 保護付きセル＋NTC | PWR.J5 | 3線セル | 1=BAT、2=GND/NTC return、3=NTC。セル実品の極性・保護FET・NTC値/位置・接続品番未定 |

現PWR v3はJ5が2極なのに「セル搭載NTC」としてRT1を基板上に描いていた。統合版ではJ5を3極にし、RT1を**基板外・BOM外のモデル**へ変更した。型番未定セルのNTC値を10k/B3435と仮置きしているため、充電温度保護が実セルに適合するか未確定。統合仕様のJ4は上表の`HV.J2/CTRL.J4`へ置き換えて読む。元PWR v3と古い比較資料は履歴として保持する。

| 状態/故障 | 主な危険 | 現状と必要な試験 |
|---|---|---|
| USBのみ・電池なし | SYS電力不足で5V/HV起動失敗 | 500mA設定の入力制限450mA最小。205V/16mAは不成立。HV禁止 |
| 電池のみ・低電池 | BATFET/セル制限・昇圧熱 | 3.3V+音声+16mAのモデル2.51A（作業）/3.05A（ストレス）。連続許可しない |
| USB＋電池、充電中HV要求 | DPPMで充電停止・電池放電 | BQ補助給電を実測し、USB接続を充電中の証拠にしない |
| MCU停止・リセット・CTRL抜去 | HV_EN漂遊、HV5524無給電時の不定出力 | HV側のハードLOW・OVP優先・残留電荷放電が必要。現HVドラフトはEN未接続で停止側 |
| Pico USBのみ/PWRなし | STAT/ADC/I²C/音声から逆給電 | 3V3/5V/SYS各無給電組合せでピン電流とレール上昇を測定。PWR ADC MOS遮断も実測 |
| HV OVP/bleeder/変圧器故障 | 推奨220V超・残留高圧・過熱 | 独立ハード停止、故障ラッチ、放電時間、温度、触れ防止を教員安全レビュー後に試験 |

## Phase 4 — 電力・熱・BOM

[統合負荷スクリプト](../hardware/integration/system-load-model.py)は既存PWRモデルの**全90行**を読み、5Vロジック0.5WをHV5524 25mA×5V=0.125W（**16MHzというメーカー試験条件の最大**）、シフタ0.025W仮定、他0.350W仮定に分離。SYSその他0.5WをPico0.300W仮定、OLED40mA×3.3V=0.132W（典型使用説明）、RTC/余裕0.068W仮定に分離する。音声時0.8Wは未実測。出力[CSV](../hardware/integration/system-load-model.csv)の各行は元モデルのP5/PSYSと±0.001W内で一致した。これは消費電力を**再配分した仮定**で、最大表示・OLED全点灯・音声ピークを保証しない。MAX668の制御電流220µA typは電力段の入力から別途賄われるものとしてηHVシナリオへ包含、二重加算を避けた。

電池3.3V＋音声、205V/16mAの昇圧損失はηHV70%/η61023 85%で0.915W、60%/80%で1.492W。[前回の損失分解](pwr-reva-v3-prototype-readiness.md)ではストレス時IC導通概算0.405W、コイル直流銅損0.070W、残差1.017W（ICスイッチング＋コア/交流銅＋他）。[TPS61023の標準基板θJA142.7°C/W](https://www.ti.com/lit/ds/symlink/tps61023.pdf)でTA40°C/TJ125°CならIC自身の許容損失は0.596W。残差分配・基板銅箔・サーマルビア・密閉PETG内温度を測るまで**連続16mAは設計承認できない**。PWR U1のBATFET 140mΩ最大はVBAT4.5V/400mA条件のみで、2～3Aへの外挿は保証値でない。PWRの5VインダクタはIsat/DCR候補を前回調査済みでも、温度コア損と実効銅箔条件が残る。充電時のBQ、HV側MOS/トランス/スナバ、HV5524、セルの熱を筐体内で同時測定する。

[統合候補BOM](../hardware/integration/integrated-bom.csv)は2026-11-15に見える販売ページの数量1価格・在庫を記録。**税込を確認できた11行の小計¥8,198.3**（PWR既確認6品、MAX668、シフタ、RTC、Pico 2、OLED）。HV5524は[Mouser掲載¥1,702.5](https://www.mouser.jp/ja/ProductDetail/Microchip-Technology/HV5524K7-G)だが税込/送料条件を確認できず小計から除外。トランス・HV安全部品・セル・管・抵抗/MLCC・全コネクタ・PCB/送料は小計に含まない。JLCPCBの[標準2層≤100×100mm/5枚$2広告](https://jlcpcb.com/help/article/how-do-i-place-an-order)は三基板の製造見積ではなく、送料・税・仕上げ・層数・再試作費も未確認。

初回支出≤¥40,000、予備¥10,000、総額≤¥50,000のため、内部計画枠を税込で置くと、確認済み¥8,198.3に未見積の管/ソケット/ネオン¥8k～14k、残り電子部品・セル・HV安全¥7k～14k、PCB¥6k～12k、送料¥2k～5k、筐体¥2k～5k、再試作¥3k～8kを加え**¥36,198～66,198**。これらは販売見積でなく配分感度であり、下側でも初回支出枠の余裕は約¥3,802だけ。**予算成立は未証明**。安全回路やNTCを削って調整しない。Pico/OLED/シフタなど可逆の低圧評価部品は試作候補、セル・高圧磁性部品・HV定格抵抗・最終PCBは仕様確定後候補に分け、現時点ではどれも発注しない。

## Phase 5 — 実測順番と発注前ゲート

1. **高電圧なし:** PWR統合版をセル模擬・NTC模擬と電子負荷で評価。USBのみ/電池のみ/両方/切断/低電池でIIN、IBAT、VSYS、5V、温度、ADC逆給電と充電状態を記録。PWRの5V出力は負荷を徐々に上げ、16mA相当の定常・過渡・起動余裕を確認。
2. **低圧CTRLのみ:** Pico USBとPWRの各組合せでGPIO・STAT・ADC・I²C・OLEDを試験。/OEとBL/POLの立上り/MCUリセット時、HV5524の32出力を安全な低電圧治具で確認。RTC EEPROM/バックアップ切替と保持、音声フィルタ/BTL負荷を確認。
3. **HV設計レビュー:** トランスのメーカー仕様と試料、FET/ダイオード/CS/FB/OVP/bleederを選定し、全公差計算、絶縁/沿面距離、温度と放電時間、プローブ・治具・カバーを教員が承認。ここまで高電圧を印加しない。
4. **教員監督下のHV試験:** 電流制限付き電源・ダミー負荷から0/4/8/12/16mAへ段階評価。起動/停止/故障/放電、効率、L/FET/ダイオード/スナバ温度、OVP最悪しきい値、残留電圧を記録。HV5524と表示管は最後。
5. **密閉筐体統合:** 充電中・最大表示・OLED/音声同時・高周囲温度でセル/IC/コイル/トランス/表示温度と温度保護を評価。最大負荷を実測で解禁できなければHV電流制限、音声排他、5V/高圧電源方式を変更。

### 重大度順の未解決判断

1. **P0 安全/成立:** 5V→205Vの検証済み磁性部品/方式、独立OVP/ハード停止/放電、表示管の電流・実端子、HVコネクタと沿面/空間距離。現HV回路は意図的に不成立。
2. **P0 電池/熱:** 保護付き21700と実NTCの型番・セル電流/充電温度、16mA連続の電力・IC温度・密閉筐体TA。電池電圧だけで最大HVを許可しない。
3. **P1 CTRL停止:** レベルシフタ/OEの電源正常ゲート、RTCバックアップ方式、音声入力と電源逆給電、Pico USB同時接続、実表示管の配線。
4. **P1 製造/予算:** PWR/CTRL/HVの実コネクタ・嵌合方向、全部品のフットプリント/電圧電力定格/在庫、JLCPCB実見積と送料・税・再試作費。初回¥40,000以内をカートで積算。

ファーム側は5V安定前HV禁止、ADC/温度/FAULT異常時HV要求LOW、音声と最大表示の排他、復帰待ち時間を実装する。**ファームは独立OVP・放電・電池保護の代替ではない。**

## 2026-11-15 HV方式の追加判定

[HV電源方式の一次判定](hv-architecture-decision.md)を追加した。MAX668の5V→205V一段ブーストはデューティ条件で不成立。5V→約27V→205Vも入力上限までの余裕が少なく推奨しない。検証可能なトランスを使うフライバックを第一の詳細設計候補とし、独立OVP/停止/放電と16mA連続時の電力・熱を確認するまでHV回路を完成扱いしない。
