# Rev.A 三基板統合ドラフト

基点は `codex/pwr-reva-v3-review`。元のPWR v3は保持し、`hardware/pwr/RevA-integrated-draft`、`hardware/hv/RevA-draft`、`hardware/ctrl/RevA-draft` にKiCad 10用の別回路図を置いた。設計判断・安全上の保留事項は [`docs/reva-integrated-prototype-review.md`](../../docs/reva-integrated-prototype-review.md) に記録する。

## 再計算と検査

リポジトリ直下からPython 3で次を実行する。

```text
python hardware/integration/build_pwr_integrated.py
python hardware/integration/build_integrated_drafts.py
python hardware/integration/system-load-model.py
python hardware/integration/verify-integrated-netlists.py
```

回路図生成後、KiCad 10の `kicad-cli sch erc` と `kicad-cli sch export netlist` を各回路図へ実行する。保存済みの `erc.txt` と `.net` は今回の結果。PWRはERC 0件。HVとCTRLは未設計の電力段、RTCバックアップ、音声入力などに対応するエラーを残す。

## フットプリント

実装面積を検討できるICだけ候補を記入した。MAX668のµMAX、HV5524のWQFN44、TPS61023などはメーカー推奨ランド図との最終照合が必要。表示管、ネオン球、HV磁性部品、基板間コネクタ、HV定格抵抗は型番と実寸法が未確定なので、フットプリントを発注確定扱いにしない。`L1`～`L32`は表示負荷を表す抽象記号で、実装部品ではない。

HV回路図は制御ICのピンを記録したドラフトであり、高電圧を生成できる回路ではない。PCB製造データ、発注、通電試験には使用しない。

## HV方式の一次判定

[HV電源方式の比較](../../docs/hv-architecture-decision.md)に、MAX668一段/二段、トランス・フライバック、高電圧カスコード、市販モジュールの成立条件を記録した。`python hardware/hv/hv-option-model.py` で仮定した効率の90条件を再計算できる。方式と部品が確定していないためHV KiCad回路図は今回変更していない。

## HVトランスの一次選別

[候補3型番の比較と432条件の再計算](../../docs/hv-transformer-screen.md)を追加した。適合する16mA連続回路は未確認のため、HV KiCadドラフト、ERC、ネットリストは変更していない。
