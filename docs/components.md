# 部品候補台帳 — Draft v0.1

| 機能 | 候補 | 状態 | 決定前に必要な確認 |
|---|---|---|---|
| 12段階光点 | 汎用2端子ネオン球 ×12 | CONFIRMED (方式) | 実品型番と電流・輝度・極性・着火 |
| 国内試作候補 | RS PRO / MonotaRO 掲載品 655-9413 | PROPOSED | 正式仕様書、抵抗内蔵有無、実測 |
| 調査推奨品 | ILT N516 0.30mA級 | PROPOSED | 国内調達、輝度、実管確認 |
| 数字管 | IN-12B ×2 | PROPOSED | 調達、着火/維持、電流、コンマ未使用 |
| OLED | 白色1.3インチ 128×64 | PROPOSED | スモーク透過率、サイズ、インターフェース |
| 試作MCU | Seeed XIAO RP2350 | PROPOSED | ピン割り当て、消費電力 |
| 最終MCU | STM32U073K8 | PROPOSED | 開発工数と最終PCB |
| RTC | RV-3028-C7 | PROPOSED | 入手性、バックアップ条件 |
| HVシンク | HV5524 ×1 | PROPOSED | 32出力、電圧余裕、制御方法、調達 |
| ロジック変換 | 74AHCT125 | PROPOSED | HV5524入力条件 |
| 充電/Power Path | BQ25185 | PROPOSED | USB入力、SYS動作条件、熱、セル保護 |
| 電池 | 保護・温度監視付き1S Li-ion（21700等） | PROPOSED | サイズ、保持・交換、安全 |
| 高電圧電源 | 調整可能な昇圧系（Flyback等） | TO_VERIFY | 最終HV定格は実測後 |
| 通知音 | 小型スピーカー＋アンプ | PROPOSED | 音色・筐体共振 |

## 禁止事項
この表の PROPOSED を購入確定・基板定格確定として扱わない。安全に関わる変更は資料と計算根拠を添える。
