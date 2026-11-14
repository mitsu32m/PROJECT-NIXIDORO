# PROJECT-NIXIDORO PWR Rev.A v3 設計レビュー

2026-11-14。KiCad 10の設計検討用ドラフト。製造・発注用ではない。基準は [`docs/reva-integrated-net-spec.md`](https://github.com/mitsu32m/PROJECT-NIXIDORO/blob/main/docs/reva-integrated-net-spec.md)。TPS63031は現行候補から省略したままとする。v2からの回路トポロジー・定数変更はない。v3ではTPS259533のクランプ表現、USB給電条件、ADC代替案の判定根拠を訂正・追加した。

## TPS259533DSGR（U3）

[TIデータシート Rev.C](https://www.ti.com/lit/ds/symlink/tps2595.pdf) のTPS2595x3はEN/OVLOが**LOWでON、しきい値超過でOFF**。KiCadのU3 pin 2はR16=442 kΩ（VBUS_RAW側）とR17=100 kΩ（GND側）の接点`EFUSE_OVLO`。5 V時は0.923 VでON側。TIの立上りピンしきい値1.13/1.20/1.27 Vから、入力遮断は理想抵抗値で**6.125/6.504/6.883 V（min/typ/max）**。抵抗各1%のみを加えた範囲は約**6.02～7.00 V**。ENピン漏れ±0.1 µAを含めるとさらに約±0.044 Vずれる可能性がある。復帰は立下りピンしきい値1.03/1.10/1.17 Vに対応して理想抵抗値で5.583/5.962/6.341 V。6 V台前半の入力が確実に遮断される設計ではない。

R18=1.78 kΩ時の電流制限はTI規格で**1.09/1.17/1.24 A（min/typ/max）**。これはeFuse出力電流の規格条件であり、USB-C電流広告の検出や500 mAの入力上限ではない。抵抗1%と実装熱条件を加えた全範囲は未計算・未実測。

出力クランプは二つの仕様を分ける。`VOVC`（クランプ開始、VIN上昇・ROUT=10 kΩ）は**5.5/5.7/5.9 V**。`VCLAMP`（VIN≥VOVC、IOUT=10 mAでクランプ中の出力）は**5.2/5.45/5.7 V**。ゆえに**5.7 Vはすべての条件で保証される出力最大値ではない**。応答時間はIOUT=4 Aで典型5 µs、100 mAで典型10 µsであり、入力ステップ中のピーク電圧を規定する値ではない。BQ25185のIN、C1/C9、後段の定格と過渡を別途検証する。U3は18 V推奨動作上限、20 V絶対最大。D1のESD TVSは持続的な20 V入力対策ではない。

## ADC監視方式

現行回路はQ1–Q3=Nexperia [BSS84AK](https://assets.nexperia.com/documents/data-sheet/BSS84AK.pdf)、Q4–Q6=Nexperia [2N7002](https://assets.nexperia.com/documents/data-sheet/2N7002.pdf)。各SOT-23のピンは1=G、2=S、3=D。P-MOSのゲートは各1 MΩで電源に戻し、2N7002のゲート`ADC_SENSE_EN`をR24=100 kΩでGNDへ。CTRL未給電時はOFFを意図する。分圧は各100 kΩ/47 kΩ、C10–C12各1 nF。比0.31973、テブナン抵抗31.97 kΩ、ON時の分圧電流は4.2/4.5/5.0 Vで28.6/30.6/34.0 µA、合計93.2 µA。1 MΩゲート抵抗にはON時に最大約13.7 µAが追加され、R24には3.3 V制御時に33 µAが流れる。抵抗1%組合せのみで分圧比誤差は約−1.36～+1.37%。

比較候補はTI [TMUX1101DBVR](https://www.ti.com/lit/ds/symlink/tmux1101.pdf)を各監視電源から給電し、各電源と上側100 kΩの間に1個ずつ置く案（各VDDに0.1 µFデカップリング候補）。同ICはSEL=HIGHでON、3.3 V信号から5 V電源を制御可能。信号は0～VDDの範囲。SELはVDD=0でも5.5 Vまで許容するが、**アナログS/Dの電源断保護を意味しない**。各VDDを被測定レールへつなぐ案なので、電源断時はS/Dも原則0 Vとなる設計仮説である。

代替ICのメーカーDBVパッケージは5ピンSOT-23（1=D、2=S、3=GND、4=SEL、5=VDD）。KiCad候補フットプリントは`Package_TO_SOT_SMD:SOT-23-5`で、1～5のパッド番号を確認した。回路へは未実装で、ランド寸法の製造承認ではない。

| 項目 | 現行MOS方式 | TMUX1101×3案 |
|---|---|---|
| OFF漏れのメーカー規格 | BSS84AK IDSS最大1 µA@25°C、2 µA@150°C、VDS=−50 V。5 V時の保証値には転用不可 | TMUX1101 OFF S/D最大±0.08 nA@25°C、±0.9 nA@125°C、VDD=5 V、VS/VD=4.5/1.5 Vの試験条件。今回のS≈VDD、D≈0 Vでの保証値ではない |
| OFF時ADCピン電圧の単純換算 | 仮に2 µAが47 kΩへ流れれば94 mV | 仮に0.9 nAなら42 µV。どちらも実条件の保証値ではない |
| 静止時電源電流 | MOSゲート回路は理想DCでほぼ0、漏れは部品・温度依存。BQ/Pico等は別 | TMUX 5 V条件でIDD典型3 nA、最大1 µA/個、3個合計典型9 nA・最大3 µA（規格条件）。ADC配線漏れは別 |
| ON時誤差 | 分圧抵抗誤差が主、MOS RDS(on)分の誤差は現条件で未確定 | RON典型1.8 Ω、最大4.9 Ω@125°C。147 kΩ分圧に対し上側直列4.9 Ωなら約0.0033%の電流差。OFF漏れとADC基準誤差は別 |
| 部品数 | MOS 6、ゲート抵抗3、共通プルダウン1 =10個。分圧R6/C3は共通 | IC3、VDDデカップリング3、共通プルダウン1 =7個。分圧R6/C3は共通 |
| 単品価格参考 | [DigiKey](https://www.digikey.jp/ja/products/detail/nexperia-usa-inc/BSS84AK-215/2779831) BSS84AK ¥28×3 + [2N7002](https://www.digikey.jp/ja/products/detail/nexperia-usa-inc/2N7002-215/762973) ¥30×3 = **¥174**（税別、抵抗・送料除く） | [DigiKey](https://www.digikey.jp/en/products/detail/texas-instruments/TMUX1101DBVR/11308781) ¥368×3 = **¥1,104**（税別、C・送料除く）。差額は半導体だけで+¥930 |

TMUXへの変更は現時点で行わない。低漏れの利点は大きいが、今回の電圧条件におけるOFF漏れ、Pico停止時のADC入力注入電流、3電源間のシーケンス、0.1 µF容量の実品番と実装寸法を検証してから判断する。現行MOS方式についても、Pico無給電で逆給電ゼロを保証しない。各ADCは1 nFと分圧源でτ≈32 µs。ファームのEN後1 ms、チャネル切替後0.3 msとダミー変換は試験候補。ADC取得窓、ADC基準、電源オフ過渡は実機で確定する。[RP2350資料](https://pip-assets.raspberrypi.com/categories/1214-rp2350/documents/RP-008373-DS-2-rp2350-datasheet.pdf)のIOVDD超過時の保護ダイオード漏れに注意。

## USB-Cの使用条件

第一候補は**仕様で5 V・500 mA以上を供給できることを確認した専用USB-C充電器**。J4=[GCT USB4105-GF-A](https://gct.co/files/drawings/usb4105.pdf)、CC1/CC2は独立した5.1 kΩ Rd、U4=[TPD2E2U06](https://www.ti.com/lit/ds/symlink/tpd2e2u06.pdf)、VBUSにはD1=[TPD1E10B06](https://www.ti.com/lit/ds/symlink/tpd1e10b06.pdf)とU3 eFuse。Rdは受電機器の接続表示であり、ソースの電流広告を**読み取らない**。R1=18 kΩはBQ25185を4.2 V・入力500 mAに設定するが、USBソースに500 mA能力がある証明ではない。PCポート、C-A変換、無銘充電器、PD高電圧を要求する運用は未承認。USB-IFの[給電ポリシー](https://compliance.usb.org/index.asp?UpdateFile=Policies)との適合、ソース広告、接続過渡、突入、充電とSYS負荷の合算を評価する。充電器限定の表示・取扱説明も発注前に決める。

## BQ25185と安全

U1 pin 4 `/CE` はGND固定で、[TI BQ25185 Rev.B](https://www.ti.com/lit/ds/symlink/bq25185.pdf)に従い有効なVINと正常なTS/MRがあるとMCU停止でも充電を許可する。R1=18 kΩは4.2 V/500 mA、R2=1.2 kΩは公称250 mA候補。RT1はセル密着10 kΩ・B3435 NTC候補で、断線・短絡・熱異常と配線を試験する。TIはTS/MRが熱範囲外で充電と安全タイマを停止すると記す。/CE固定では充電停止をMCUから指令できず、充電安全はIC・NTC・保護付きセルに依存する。TIのILIM/VSET検出には`/CE`を再有効化する場合のTS/MR条件に注意書きがあるため、電源再投入とセル接続の順序を実測する。

SYS負荷は充電より優先され、入力500 mA枠を超えると充電電流が減り、さらに負荷が増すと電池の補助給電が起き得る。/CEは補助給電を禁止しない。**充電器接続中も電池が放電し得る**ため、Pico、5 V昇圧、HV起動時のSYS最大負荷を測定する。電池未接続時はBATコンデンサの充放電とSTAT変動があり、SYS安定性をセルなしで試験する。高電圧基板の独立OVP・放電・フェイルセーフは省略しない。

## KiCad検証と発注前TODO

`PWR_RevA.kicad_sch`のU1/U3/J4/Q1–Q6と、各ネット・定数を直接確認した。KiCad標準フットプリントの**パッド番号存在**は`netlist-footprint-check.txt`で確認する。U1 DLH0010A、U3 DSG0008A、J4 GCT USB4105、MOS SOT-23の実装寸法・ランドパターン・リフロー可否までの承認ではない。抵抗・コンデンサ・インダクタおよびJ1/J2/J3/J5は未割当または実型番未決。プロジェクト独自の箱形シンボルを使っており、ERC 0は部品の動作・製造性を保証しない。`PWR_RevA.net`と`erc.txt`を同梱する。

発注前には、(1)5 V充電器とUSB電流条件、(2)セル・保護回路・NTC実品番、(3)SYS/充電同時負荷と熱、(4)ADC無給電注入・OFF漏れ・ファーム取得時間、(5)全フットプリント・コネクタ嵌合、(6)税込送料込みBOMで総額50,000円・予備費10,000円、(7)HV安全回路、を確定する。PCBレイアウト、ガーバー、発注は行っていない。
