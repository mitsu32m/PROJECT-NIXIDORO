# PWR Rev.A v3 実測試作へ進むための設計確認

2026-11-15。対象 `codex/pwr-reva-v3-review`。**候補品番は発注指定ではない。** [v3回路図](../hardware/pwr/RevA-draft-v3/)、[電力・熱レビュー](pwr-reva-power-thermal-review.md)とメーカー一次資料を照合した。PCB寸法・層数、セル、HVトランスは未確定。

## 再現性

`python hardware/pwr/RevA-draft-v3/power-model.py` は同じ場所のCSVを生成する。`python hardware/pwr/RevA-draft-v3/power-model-check.py` は一時ディレクトリで再生成し、コミット版とバイト単位で比較する。さらに**全90行**のHV・5V・SYS電力、SYS入出力、BATFET降下、インダクタ電流を丸め誤差内で照合する。実行結果は `PASS: byte-identical regeneration; 90 rows checked; report anchors checked`。報告書のUSBのみ6.60 W、低電池＋音声の電池電流2.51/3.05 Aも照合した。これは**モデルの算術検証**であり、効率・セル・熱・過渡の妥当性検証ではない。

## 候補部品と実装確認

下表の「候補」はメーカー公表の品番と公称特性を確認済み。「保留」は回路値との整合、実効容量、温度・実装・在庫等を実験/見積で確認する段階。抵抗は[Panasonic ERJ3EKF系列](https://industrial.panasonic.com/ww/products/pt/general-purpose-chip-resistors/models/ERJ3EKF1802V)の**0603、0.1 W、±1%、TCR±100 ppm/°C、カテゴリ温度−55～155°C**を共通条件とする（[系列仕様](https://industrial.panasonic.com/cdbs/www-data/pdf/RDA0000/AOA0000C304.pdf)）。個別値のメーカー照合例: [1.2 kΩ](https://industrial.panasonic.com/ww/products/pt/general-purpose-chip-resistors/models?model_number=ERJ3EKF&order=atr-ind-pRDA0000J5_46_A&page=0&sort=asc)、[18 kΩ](https://industrial.panasonic.com/ww/products/pt/general-purpose-chip-resistors/models/ERJ3EKF1802V)、[100 kΩ](https://na.industrial.panasonic.com/products/resistors/smd-chip-resistors/series/57494/model/66385)、[442 kΩ](https://industrial.panasonic.com/ww/products/pt/general-purpose-chip-resistors/models/ERJ3EKF4423V)、[732 kΩ](https://industrial.panasonic.com/ww/products/pt/general-purpose-chip-resistors/models/ERJ3EKF7323V)。

| 回路・参照 | メーカー候補 | 定格・許容差・温度・大きさ | 残る確認 |
|---|---|---|---|
| BQ U1 | [TI BQ25185DLHR](https://www.ti.com/lit/ds/symlink/bq25185.pdf) | WSON10 DLH 2.2×2 mm、TJ −40～125°C | KiCad U1の露出パッドと実装熱設計、SYS/USB補助動作 |
| BQ R1/R2 | Panasonic ERJ3EKF1802V / ERJ3EKF1201V | 18 kΩ / 1.2 kΩ、系列共通条件 | R1の入力500 mA設定は実保証450/475/498 mA。R2の充電電流はセル定格と再照合 |
| BQ C1/C3 | [Murata GRM31CR71E106KA12L](https://ds.murata.com/simsurfing/mlcc.html?oripartnumbers=%5B%22GRM31CR71E106KA12L%22%5D&partnumbers=%5B%22GRM31CR71E106KA12%22%5D&rgear=zzo&rgearinfo=com)を**容量余裕候補** | 10 µF、25 V、X7R、±10%、−55～125°C、1206 3.2×1.6×1.8 mm | 回路図は各1 µF。実効容量≥1 µFをDCバイアス、温度、許容差、経年で確認後に値・フットプリント変更。入手性も要確認 |
| BQ C2 / TPS C4 / eFuse C9 | 同GRM31CR71E106KA12L | 10 µF、25 V、X7R、±10%、1206 | C2/C4は回路10 µF公称だが実効容量の下限未確認。C9は回路1 µFで容量変更要。局所配置と突入も確認 |
| BQ RT1 | **セル付属の10 kΩ/B3435 NTCを要指定** | 現行回路値だけ確定。実セルのR25・B値・許容差・配線サイズ不明 | セルメーカー品番と充電温度しきい値確認。仮の基板NTCに置換しない |
| TPS U2 | [TI TPS61023DRLR](https://www.ti.com/lit/ds/symlink/tps61023.pdf) | DRL SOT-5X3 1.6×1.6 mm、TJ −40～125°C | 銅箔・放熱・起動負荷は試作実測 |
| TPS R3/R4 | Panasonic ERJ3EKF7323V / ERJ3EKF1003V | 732 kΩ / 100 kΩ、系列共通条件 | FB配線ノイズ・出力電圧公差 |
| TPS L1 | [Coilcraft XEL4030-102MEC](https://www.coilcraft.com/getmedia/8245f050-f190-4295-8c41-7c03d662ee3d/xel4030.pdf) | 1 µH ±20%、DCR 8.89 typ/9.78 max mΩ、Isat 9 A（L−30%）、Irms 8.4 A（ΔT20°C）、約4.3×4.3×3.1 mm、周囲−40～125°C（40°C上昇Irms時）、部品最大165°C | 現行KiCadのL1フットプリントは未指定。実品の形状、温度時L、コア損、価格、調達を確認。モデルのL_min=0.7 µHは−30%仮定であり、この部品の±20%と同義ではない |
| TPS C5/C6 | [Murata GRM32ER71E226KE15L](https://ds.murata.com/simsurfing/mlcc.html?oripartnumbers=%5B%22GRM32ER71E226KE15L%22%5D&partnumbers=%5B%22GRM32ER71E226KE15%22%5D&rgear=suaykx&rgearinfo=com) | 各22 µF、25 V、X7R、±10%、−55～125°C、1210 3.2×2.5×2.7 mm | 5 V印加時の実効容量、ESR、起動・位相余裕。販売先では在庫切れの可能性があるため代替検討 |
| TPS R5 / eFuse R17 | Panasonic ERJ3EKF1003V | 100 kΩ、系列共通条件 | ENの停止時電位と異常時挙動 |
| eFuse U3 | [TI TPS259533DSGR](https://www.ti.com/lit/ds/symlink/tps2595.pdf) | DSG WSON8 2×2 mm、TJ −40～125°C | EP接地、放熱、OVLO/ILIMの実ばらつき |
| eFuse R16/R18 | Panasonic ERJ3EKF4423V / ERJ3EKF1781V | 442 kΩ / 1.78 kΩ、系列共通条件 | 5.7 Vをクランプの保証最大と扱わない。入力許容としきい値のmin/maxを再試験 |
| eFuse C7/C8 | **品番未確定** | 回路3.3 nF / 0.1 µF。必要定格・実効値・フットプリント未照合 | dV/dt過渡・バイパス条件をTIの式と実測で確認して選定 |
| USB保護 U4/D1 | [TI TPD2E2U06DCKR](https://www.ti.com/lit/ds/symlink/tpd2e2u06.pdf) / [TPD1E10B06DPYR](https://www.ti.com/lit/ds/symlink/tpd1e10b06.pdf) | CC用SC70-3、VBUS用X1SON-2 1×0.6 mm、各−40～125°C、作動5.5 V | 既存KiCadパッド対応を保持。VBUSサージのエネルギー・PCB入口配置は未確認。ESDと過電圧保護は別役割 |

USBコネクタ [GCT USB4105-GF-A](https://www.gct.co/connector/usb4105-gf-a) は現行回路の候補。CC1/CC2の5.1 kΩ Rdは別途実型番確認、実コネクタの全パッドとKiCadフットプリントはPCB化前に寸法照合する。**本表の大容量MLCCはKiCadにまだ割り当てていない。** 電圧定格25 VだけではDCバイアス後の実効容量を保証できない。コイルも現行フットプリント未指定。したがってこの表を製造BOMへ転記しない。

## TPS61023損失の内訳と熱条件

205 V×16 mA、5 Vロジック0.50 W、SYSその他0.50 W、音声追加0.80 W、`R_path=0.14 Ω`（BQ仕様条件外への仮外挿）、L=0.7 µH、1 MHz。`P_5=0.5+3.28/η_HV`、`P_SYS=P_5/η_B+1.3`、`P_B,total=P_5(1/η_B−1)`。`I_L,rms²≈I_L,DC²+ΔI_L²/12`。TIの[47/68 mΩ典型MOSFET抵抗](https://www.ti.com/lit/ds/symlink/tps61023.pdf)で`P_IC,cond≈I_L,rms²[D×0.047+(1−D)×0.068]`、コイルのDCR最大9.78 mΩで`P_L,DC≈I_L,rms²×0.00978`。**IC導通は典型抵抗を使う参考値、コイル銅損は25°C相当のDCR最大による参考値。高温保証損失ではない。**

| ηHV/ηB、VBAT、音声あり | VSYS | IBAT | Lピーク | 昇圧総損失 | IC導通概算 | L直流銅損 | 残差 |
|---|---:|---:|---:|---:|---:|---:|---:|
| 70%/85%、4.0 V | 3.72 V | 1.99 A | 2.62 A | 0.915 W | 0.181 W | 0.029 W | 0.705 W |
| 70%/85%、3.6 V | 3.29 V | 2.25 A | 2.89 A | 0.915 W | 0.224 W | 0.037 W | 0.654 W |
| 70%/85%、3.3 V | 2.95 V | 2.51 A | 3.12 A | 0.915 W | 0.267 W | 0.045 W | 0.602 W |
| 70%/85%、3.0 V | 2.60 V | 2.85 A | 3.38 A | 0.915 W | 0.330 W | 0.057 W | 0.528 W |
| 60%/80%、4.0 V | 3.67 V | 2.39 A | 3.12 A | 1.492 W | 0.269 W | 0.044 W | 1.179 W |
| 60%/80%、3.6 V | 3.22 V | 2.72 A | 3.43 A | 1.492 W | 0.334 W | 0.057 W | 1.101 W |
| 60%/80%、3.3 V | 2.87 V | 3.05 A | 3.71 A | 1.492 W | 0.405 W | 0.070 W | 1.017 W |
| 60%/80%、3.0 V | 2.51 V | 3.49 A | 4.04 A | 1.492 W | 0.510 W | 0.090 W | 0.892 W |

残差=ICスイッチング/制御、コイルコア/交流銅損、コンデンサESR、PCB配線の**合計**。コア材の損失曲線と実波形がないため分離不可。`P_IC = P_IC,cond + P_IC,switch/control`、`θJA必要 ≤ (125−TA)/P_IC`。TA=40°CならIC損失許容はTI標準基板θJA142.7°C/Wで0.596 W、TI EVM参考θJA91.4°C/Wでも0.930 W。ストレス3.3 Vでは総損失1.492 Wゆえ、標準基板並みなら**IC以外へ少なくとも0.896 W**、うち算出済み銅損0.070 Wを除き**0.826 W**が外部で消費される必要がある。これは成立を示す条件式であり、実際に外部でその量が散逸する根拠はない。逆に残差をすべてIC損失と見込む上限側では`θJA ≤ 85/(1.492−0.070)=59.8°C/W`が必要。単一の熱抵抗要求を決めるにはIC、L1の温度・電流波形と効率実測が必要。

## BQ25185: 保証条件と近似の境界

[TIのBQ25185仕様](https://www.ti.com/lit/ds/symlink/bq25185.pdf)にあるBATFET `R_ON=115 mΩ typ /140 mΩ max` は**VBAT=4.5 V、IBAT=400 mA**の測定条件。これを2～3.5 Aへ外挿した`P_BATFET≈I_BAT²×0.14`は設計モデルであって保証最大損失ではない。例として作業3.3 V＋音声は約0.882 W、ストレス3.3 V＋音声は約1.301 Wとなるが、セル・保護FET・接点抵抗を含まず、温度上昇と電圧低下は別途増える。TIのBAT放電OCP 3.13 A typと±18%精度は27°C等の指定条件で、下側2.56 Aを全温度の連続電流保証に使えない。

USB入力500 mA設定でも実制限は450/475/498 mA (min/typ/max)。SYS優先のDPPMは充電電流を減らし、SYSがVBATより約40 mV下がると電池補助へ入る**典型挙動**。USB＋電池4.0 V＋最大HV＋音声のモデルは作業で電池1.50 A、ストレスで1.90 Aを要求し、充電中ではなく放電。モデルの`I_USB=0.45 A`はSYSへ損失ゼロで流入する近似であり、実際のパス損失・入力低下・バッテリ保護・熱制限を含まない。充電状態と補助給電の遷移を実機で測る。

## 16 mA連続負荷の暫定使用制限

**現行構成で16 mA連続の成立は未証明。** 上表の電池3.0 Vは作業仮定でも2.85 A、ストレス仮定で3.49 Aとなり、OCPとセル側が未確定のため禁止候補。3.3 Vは作業2.51 AでOCP参考下側2.56 Aとほぼ同じ、ストレス3.05 Aで上回るため連続許可しない。3.6 Vはストレス2.72 A、参考下側を超える。4.0 Vでもストレス2.39 Aと近く、IC熱・セル・起動は未証明。**電池電圧だけで16 mAを解禁できる範囲は現時点でない。**

試作時は既報の暫定HVゲート（無負荷VBAT≥3.8 V、動作SYS≥3.4 V、5 V≥4.8 V）を診断用とし、USBのみ/セル不明/温度異常時はHV禁止。HV起動中は音声停止、表示は実測で対応付けた≤8 mA相当まで。16 mAは電子負荷を用いた定常・起動・熱の段階試験だけで扱う。成立判定にはセル保護と内部抵抗、USB入力、BQ/TPS/L1温度、5 V変動、HV効率、筐体内TA、PCB実効θJA、過渡電流、OVPと放電を同時に確認する。

## コネクタと資料整合

[統合仕様](reva-integrated-net-spec.md)、[Pico 2ピン表](pico2-pinmap.md)、[基板間接続](board-interconnects.md)はGP17=`ADC_SENSE_EN`、PWR J3 pin10、J3=10極で一致。PWR KiCadネットリストにもJ3 pin10がある。[電源シーケンス](pwr-sequencing.md)の旧GP17=`I2C_ISO_EN`、GP18=`PWR_3V3_EN`記述を現行案に修正した。CTRL回路図とファームは未実装。J3の実型番・嵌合方向・ピン1表示は決めず、実測基板のコネクタ設計条件として残す。

## 税込概算と予算ゲート

[概算BOM CSV](../hardware/pwr/RevA-draft-v3/prototype-bom-estimate.csv)の税別単価は2026-11-15に見えるDigiKey日本の**1個カットテープ価格**を引用し、税込を×1.10で計算。価格は更新される。BQ ¥467.5、TPS61023 ¥223.3、eFuse ¥188.1、CC ESD ¥118.8、VBUS ESD ¥73.7、USB-C ¥146.3で、各1個の**確認できた6品小計¥1,217.7税込**。抵抗・MLCC・L1・NTC付きセル・基板間コネクタ・HV安全部品は単価/仕様が揃わず、小計には含めない。CC ESDは確認時在庫0。DigiKey送料、複数店舗送料、関税条件、PCB寸法/層数/仕上げも未見積。したがって**全PWR BOMと全体¥50,000以内を現時点で証明できない**。

予算目標は税込総額≤¥50,000、予備費¥10,000を別置きし初回支出≤¥40,000。既存[調達計画](purchasing.md)の旧枠は実見積ではない。発注前に数量付き販売カートを作り、PWR/CTRL/HV/表示管/筐体とPCB試作回数、送料、税込、手持ち再利用分を積み上げる。保護・温度監視・HV OVP/放電は削減対象にしない。

見積が取れるまでの**内部計画枠**（実売価格ではない）を税込で置くと、確認済み6品¥1,217.7、PWR未価格部品・安全部品¥4,000～8,000、PWR/CTRL/HV試作PCBと再試作分¥6,000～12,000、複数店送料¥2,000～5,000、その他の表示管・MCU・HV・セル・筐体¥20,000～30,000で**¥33,217.7～56,217.7**。下側でも初回支出¥40,000の余地は¥6,782.3だけ、上側は総額目標を¥6,217.7超える。この区間は根拠ある販売見積ではなく、見積優先順位を決めるための配分シナリオ。PCBの寸法・層数・枚数と送料が未定のため、製造可否や予算達成を判断しない。

## 次の設計判断

1. 実セルの型番、温度センサ、許容放電電流、保護回路、内部抵抗と温度範囲。
2. 16 mA連続時の実測HV効率、音声/OLED実入力、許容筐体温度と昇圧ICの実効熱抵抗。熱不足なら銅箔/層数/昇圧構成の変更を判断。
3. C1～C9の実効容量と在庫、L1の温度時L・コア損・フットプリント、TPS259533の異常電圧・クランプ/遮断過渡。
4. J1/J2/J3/J5の実コネクタ、USB-Cの嵌合/パッド、セルとHVの安全部品、PCB製造見積と全体税込BOM。

KiCadの接続・定数は今回確定できる変更がなかったため回路図を変更せず、既存ネットリスト/ERC結果を維持。**ERC 0件は安全・熱・起動の証明ではない。** PCB製造データの確定、発注は行っていない。

