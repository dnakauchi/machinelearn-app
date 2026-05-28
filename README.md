# 機械学習モデル作成アプリ

誰でも簡単に複数の機械学習モデルを比較・評価できるアプリです。

## 🚀 オンラインで使用

### Streamlit Cloud で実行

以下のリンクからすぐに使用できます：

> **[🔗 アプリを開く](https://machinelearn-app.streamlit.app)**

（Streamlit Cloud へのデプロイ準備中）

## 📋 機能

- ✅ Excel / CSV ファイルのアップロード対応
- ✅ 複数の被説明変数・説明変数を自由に選択
- ✅ 6つのアルゴリズムを同時比較
  - 線形回帰、リッジ回帰、ラッソ回帰
  - ランダムフォレスト、勾配ブースティング、SVR
- ✅ モデルスコア（R²、RMSE、MAE）の自動評価
- ✅ 予測値 vs 実際の値をプロット
- ✅ 説明変数の寄与度を可視化
- ✅ 相関行列と分布図行列
- ✅ 学習済みモデルを joblib 形式でダウンロード

## 💻 ローカルで実行

### セットアップ

```bash
# リポジトリをクローン
git clone https://github.com/dnakauchi/machinelearn-app.git
cd machinelearn-app

# 仮想環境を作成（推奨）
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 依存関係をインストール
pip install -r requirements.txt
```

### アプリを起動

```bash
streamlit run app.py
```

ブラウザで `http://localhost:8501` が自動的に開きます。

## 📊 使い方

1. **ファイルをアップロード**
   - Excel (.xlsx, .xls) または CSV ファイルを選択
   - 最大 100MB、100,000 行まで対応

2. **変数を選択**
   - 被説明変数（目的変数）を選択
   - 説明変数（特徴量）を複数選択可能

3. **アルゴリズムを選択**
   - 使用するモデルをチェック
   - テストデータ割合を設定

4. **「モデルを作成・評価」をクリック**
   - 各モデルが自動で学習・評価
   - スコア、グラフ、寄与度が表示

5. **モデルをダウンロード**
   - 学習済みモデルを `.joblib` 形式で取得
   - 後で `joblib.load()` で読み込み可能

## 🔒 セキュリティ

このアプリは以下のセキュリティ対策を実施しています：

| 対策 | 説明 |
|------|------|
| **ファイルサイズ制限** | 最大 100MB |
| **データ行数制限** | 最大 100,000 行 |
| **列数制限** | 最大 500 列 |
| **エラーメッセージ制限** | 情報漏洩防止 |
| **シークレット管理** | 環境変数で安全に管理 |
| **CORS 無効化** | クロスオリジンリクエスト防止 |
| **キャッシュ管理** | メモリ効率化 |

## 🔧 トラブルシューティング

### CSV が文字化けする
- ファイルのエンコーディングを UTF-8 に統一してください
- または Excel 形式（.xlsx）に変換してください

### モデル学習が遅い
- データサイズを縮小してください（行・列を削減）
- テストデータ割合を大きくしてください

### 「メモリ不足」エラー
- Streamlit Cloud の無料プランには制限があります
- ローカルで実行するか、アップグレードしてください

## 📦 ダウンロード済みモデルの使用方法

```python
import joblib
import pandas as pd

# モデルを読み込む
obj = joblib.load("model__target__algorithm.joblib")
model = obj["model"]
scaler = obj["scaler"]  # SVR の場合のみ使用
feature_cols = obj["feature_cols"]
target_col = obj["target_col"]

# 新しいデータで予測
X_new = pd.DataFrame([{col: value for col in feature_cols}])
if scaler is not None:
    X_new = scaler.transform(X_new)
predictions = model.predict(X_new)
print(predictions)
```

## 📝 入力データの形式

### Excel / CSV の要件
- **数値列のみ対応**（カテゴリ変数は事前に数値化してください）
- **最初の行がヘッダー**
- **欠損値（空白）は自動削除**

### 例：良いデータ形式

| 年齢 | 年収 | 経験年数 | 満足度 |
|------|------|---------|--------|
| 25   | 300 | 2       | 3.5    |
| 35   | 500 | 10      | 4.0    |
| 45   | 700 | 20      | 4.2    |

## 🚀 Streamlit Cloud へのデプロイ

### 前提条件
- GitHub アカウント
- このリポジトリをフォーク

### デプロイ手順

1. **Streamlit Cloud にアクセス**
   - https://share.streamlit.io

2. **GitHub アカウントで認証**

3. **「New app」をクリック**
   - Repository: `<your-username>/machinelearn-app`
   - Branch: `main`
   - Main file path: `app.py`

4. **デプロイボタンをクリック**

5. **自動更新が有効に**
   - GitHub にプッシュするたびに自動デプロイ

### GitHub Actions での自動テスト（オプション）

```bash
git push origin main
```

## 📄 ライセンス

MIT License

## 🤝 コントリビューション

改善提案やバグ報告は Issues から、機能追加は Pull Request でお願いします。

## 📧 サポート

問題が発生した場合は、GitHub Issues で報告してください。

---

**開発者:** dnakauchi  
**最終更新:** 2026-05-29
