# PROJECT-NIXIDORO

**低ストレス・グローチューブ式ポモドーロタイマー** / Design stage

球体状の表示部に**汎用2端子ネオン球12灯**の残り時間ゲージと**2桁のニキシー表示**を組み合わせ、傾斜した台座にACTION・NEXT・押し込みエンコーダ・スモーク窓OLEDを配置する構想。

**重要:** 本リポジトリは設計検討中。掲載されている候補部品・回路定格は動作保証や安全確認済みという意味ではありません。

## どこを見ればいい？

| 目的 | ファイル |
|---|---|
| 作りたい製品の要件 | [docs/requirements.md](docs/requirements.md) |
| 電源と回路のブロック構成（暫定） | [docs/architecture.md](docs/architecture.md) |
| 部品の候補と確定/検証状況 | [docs/components.md](docs/components.md) |
| ボタン・モード・状態遷移 | [docs/ui-spec.md](docs/ui-spec.md) |
| なぜその方針を選んだか | [docs/decisions/0001-record-decisions.md](docs/decisions/0001-record-decisions.md) |
| 参考調査資料の索引 | [docs/research/README.md](docs/research/README.md) |
| 記録ルール | [docs/README.md](docs/README.md) |

## 設計上の大原則
- **CONFIRMED:** 方針として採用（電気的検証済みとは限らない）
- **PROPOSED:** 有力案・検討中
- **TO_VERIFY:** 実測・一次資料などで検証が必要
- **REJECTED:** 見送り
- **VERIFIED:** 条件・記録・証拠付きで検証済み

調査レポートの推薦をそのまま「確定」としない。部品の型番や高電圧電源は特に注意。高電圧とLi-ionの実装には指導者による設計・実物レビューが必要。

## 開発順序
1. LED12灯＋OLED＋操作系の低電圧UI試作
2. 筐体・スモーク窓の実寸試作
3. ネオン球・ニキシーの個別特性確認（適切な監督下）
4. 高電圧ドライバ・電源・バッテリー統合
5. 最終PCB・筐体と安全検証

設計変更はGit履歴と決定記録に残す。
