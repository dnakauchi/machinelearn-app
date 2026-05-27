# ML_app

## プロジェクト概要

機械学習アプリケーションの開発リポジトリ。

## Git 運用ルール

### コード変更後は必ず GitHub にプッシュする

コードを変更するたびに、以下の手順で GitHub へプッシュすること：

```bash
git add <変更ファイル>
git commit -m "変更内容を簡潔に説明するメッセージ"
git push origin <ブランチ名>
```

- `git add .` や `git add -A` は避け、変更ファイルを明示的に指定する
- コミットメッセージは英語または日本語で変更の意図が伝わるよう記述する
- `main` ブランチへの直接プッシュは避け、feature ブランチ経由の PR を推奨する
- `.env` や認証情報ファイルは絶対にコミットしない

### ブランチ戦略

- `main` — リリース可能な状態を保つ
- `feature/<機能名>` — 新機能開発
- `fix/<バグ内容>` — バグ修正

## 開発環境

- Python（機械学習ライブラリ: scikit-learn / PyTorch / TensorFlow など）
- 仮想環境: `venv` または `conda`
- パッケージ管理: `requirements.txt` または `pyproject.toml`

## ディレクトリ構成（予定）

```
ML_app/
├── data/          # 学習・評価データ（Git 管理対象外）
├── notebooks/     # 実験用 Jupyter Notebook
├── src/           # アプリケーションコード
│   ├── models/    # モデル定義
│   ├── train/     # 学習スクリプト
│   └── predict/   # 推論スクリプト
├── tests/         # テストコード
├── .gitignore
├── requirements.txt
└── CLAUDE.md
```

## .gitignore に含めるべきもの

- `data/` — 大容量データセット
- `*.pkl`, `*.h5`, `*.pt` — 学習済みモデルファイル
- `__pycache__/`, `*.pyc`
- `.env`, `.env.*`
- `venv/`, `.venv/`

## コーディング規約

- フォーマッター: `black`
- リンター: `flake8` または `ruff`
- 型ヒント: 積極的に使用する
- テスト: `pytest`
