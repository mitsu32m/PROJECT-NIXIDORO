# 設計ドキュメントの読み方

このプロジェクトでは、**希望・調査結果・採用決定・実測済み**を混同しない。

## Status
- **CONFIRMED**: ユーザーが方針として決めた要件（電気的な検証完了を意味しない）
- **PROPOSED**: 調査から有力だが未採用・未評価の案
- **TO_VERIFY**: データシートまたは実機検証が必要
- **REJECTED**: 現時点で不採用
- **VERIFIED**: 実測またはテストで条件付き確認済み（証拠を添付）

## 主要ファイル
- [ai-workflow.md](ai-workflow.md): AI設計・調査・レビューの必須手順、役割分担、引き継ぎ、コミット運用
- [tech-tree.md](tech-tree.md): 研究テックツリー（進捗可視化）
- [tech-tree.yaml](tech-tree.yaml): 機械可読な課題ノード・依存関係・達成基準
- [verification/README.md](verification/README.md): 検証台帳と記録フォーマット
- [requirements.md](requirements.md): 何を作りたいか、必須機能・デザイン
- [architecture.md](architecture.md): 電源・電子回路・分割基板の暫定構成
- [components.md](components.md): 候補部品と確認待ち項目
- [ui-spec.md](ui-spec.md): 操作と状態遷移
- [decisions/0001-record-decisions.md](decisions/0001-record-decisions.md): 設計決定の記録
- [research/README.md](research/README.md): Deep Research資料の索引
- [pwr-reva-v2-review.md](pwr-reva-v2-review.md): PWR Rev.A KiCadドラフトv2とメーカー照合・未解決事項

## 運用ルール
1. Deep Researchの「推奨」は自動的にCONFIRMEDにしない。
2. 回路図やPCBを作成する前にTO_VERIFYを解消する。
3. 部品を変更するときは理由・影響範囲・検証方法を決定記録に残す。
4. ハードの高電圧・リチウムイオン系は設計/実物ともに有資格または経験ある指導者のレビューを受ける。
5. 重要な変更はPull Requestで差分を確認してから反映する。
