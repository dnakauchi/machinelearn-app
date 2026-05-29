# 🤖 機械学習モデル作成アプリ

**非技術者でも簡単に機械学習モデルを比較・評価できるWebアプリケーション**

![GitHub](https://img.shields.io/badge/github-dnakauchi-blue?logo=github) ![Python](https://img.shields.io/badge/python-3.8%2B-blue) ![Streamlit](https://img.shields.io/badge/streamlit-1.35%2B-FF6B6B) ![License](https://img.shields.io/badge/license-MIT-green)

---

## 📌 プロジェクト概要

このアプリは、**機械学習の知識がなくても**、ExcelやCSVのデータから簡単に複数の機械学習モデルを比較・評価できることを目指しています。

### 🎯 解決する課題

- **課題:** 機械学習モデル選定は専門知識が必要で、多くの時間を消費する
- **解決策:** ドラッグ&ドロップでデータをアップロードするだけで、複数モデルが自動比較される
- **結果:** 誰でも5分でモデル選定ができる

### 対象ユーザー

| ユーザー | 用途 |
|---------|------|
| **データアナリスト** | 複数モデルの素早い比較 |
| **経営者・営業** | 機械学習の可能性を確認 |
| **学生・初心者** | 実践的な学習 |
| **プロトタイピング** | PoC（概念実証）の早期段階 |

---

## 🚀 クイックスタート

### オンラインで今すぐ試す

**[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://machinelearn-app.streamlit.app)**

> 環境セットアップ不要。ブラウザで即実行できます

### ローカルで 30 秒で開始

```bash
git clone https://github.com/dnakauchi/machinelearn-app.git
cd machinelearn-app
pip install -r requirements.txt
streamlit run app.py
```

---

## ✨ 主な機能

### 1. **複数アルゴリズムの同時比較**

6つの機械学習アルゴリズムを同時に学習・評価：

| アルゴリズム | 特徴 | 適用例 |
|-------------|------|--------|
| **線形回帰** | シンプル・解釈性高 | 線形関係の予測 |
| **リッジ回帰** | 過学習対策版 | 多変量データ |
| **ラッソ回帰** | 変数選択機能 | 特徴量削減 |
| **ランダムフォレスト** | 非線形・頑健 | **一般的に最も優秀** |
| **勾配ブースティング** | 高精度 | 複雑なパターン |
| **SVR** | 複雑な関係 | 非線形回帰 |

### 2. **自動評価指標**

各モデルを3つの指標で評価：

```
R² スコア       → モデルの当てはまり度（0～1、高いほど良い）
RMSE           → 予測誤差の標準偏差（低いほど良い）
MAE            → 平均絶対誤差（低いほど良い）
```

[詳細は下を参照](#-評価指標の解釈)

### 3. **可視化機能**

| グラフ | 用途 |
|-------|------|
| **予測値 vs 実際の値** | モデル精度を直感的に把握 |
| **説明変数の寄与度** | 各変数の影響度を可視化 |
| **相関行列（ヒートマップ）** | 変数間の相関を一目で確認 |
| **分布図行列（Pairplot）** | 全変数間の関係を同時表示 |

### 4. **モデルの再利用**

学習済みモデルを `.joblib` 形式でダウンロード → 本番環境で使用可能

```python
# ダウンロードしたモデルを読み込んで予測
import joblib
obj = joblib.load("model__売上__ランダムフォレスト.joblib")
predictions = obj["model"].predict(new_data)
```

---

## 📊 使用方法（詳細版）

### ステップ 1: ファイルをアップロード

**対応形式:**
- Excel（`.xlsx`, `.xls`）
- CSV（UTF-8, Shift-JIS 自動検出）

**ファイル要件:**
- ✅ 最初の行はヘッダー（列名）
- ✅ 数値列のみ対応
- ✅ 最大 100MB、100,000行
- ⚠️ 欠損値は自動削除

**サンプルデータ:**

```csv
年齢,年収,経験年数,満足度,成績
25,300,2,3.5,70
35,500,10,4.0,85
45,700,20,4.2,92
```

### ステップ 2: 変数を選択

**被説明変数（Y / 目的変数）:**
- 予測対象の変数（例：売上、気温）
- 複数選択可能 → 複数の目的変数で同時学習

**説明変数（X / 特徴量）:**
- 予測に使う情報（例：広告費、来店数）
- 複数選択推奨（最大500個まで対応）

**💡 Tips:**
- 関連がない変数は外す → 精度向上
- 相関が高い変数ペアは注意 → 共線性問題

### ステップ 3: アルゴリズムを選択

```
☑ 線形回帰          ← シンプルさ重視ならこれ
☑ ランダムフォレスト ← 迷ったらこれ
☑ 勾配ブースティング ← より正確さ重視ならこれ
```

**テストデータ割合:** `20%` を推奨
- 80% で学習 → 20% で評価
- 小さいデータセット: 30% に増やす

### ステップ 4: 「モデルを作成・評価」をクリック

自動で以下を実行：
1. ✅ データの前処理（正規化など）
2. ✅ 各モデルの学習
3. ✅ 性能評価
4. ✅ グラフ生成

### ステップ 5: 結果を確認

**モデルスコア表:**
- 左から高精度順に表示
- 最良モデルが緑でハイライト

**グラフ解釈:**
- 散布図が右上対角線に沿っている → 良好
- ばらつきが大きい → 要改善

**寄与度グラフ:**
- 青い棒 → 正の影響（その変数が増えると目的変数↑）
- 赤い棒 → 負の影響（その変数が増えると目的変数↓）

---

## 🧠 各モデルの詳細ガイド

### 線形回帰

```
特徴: y = a₁x₁ + a₂x₂ + ... + c （一次式）
メリット: 
  • 解釈が簡単（係数 = 影響度）
  • 計算が高速
デメリット:
  • 直線関係のみ対応
  • 複雑なパターンに弱い
推奨: 初期確認、解釈性重視
```

### リッジ回帰・ラッソ回帰

```
特徴: 過学習を防いだ線形回帰
メリット:
  • 線形回帰より頑健
ラッソ: 自動的に不要な変数を削除
デメリット:
  • 非線形パターンに弱い
推奨: 変数が多い場合
```

### ランダムフォレスト ⭐ 最推奨

```
特徴: 複数の決定木を組み合わせ
メリット:
  • ほぼすべての問題に対応
  • 非線形パターンに強い
  • 外れ値に強い
  • 過学習しにくい
デメリット:
  • 「なぜ？」という理由説明が難しい
推奨: 迷ったらこれ、バランス型
```

### 勾配ブースティング

```
特徴: 弱い学習器を順序立てて強化
メリット:
  • 高精度（競技で頻出）
  • 複雑なパターンに対応
デメリット:
  • パラメータ調整が複雑
  • 計算時間が長い
  • 過学習のリスク
推奨: 最高精度を求める場合
```

### サポートベクター回帰（SVR）

```
特徴: 高次元空間へのマッピング
メリット:
  • 複雑な非線形パターン対応
デメリット:
  • 大規模データで遅い
  • パラメータ調整が難しい
推奨: 変数が少ない場合
```

---

## 📈 評価指標の解釈

### R² スコア（決定係数）

```
式: R² = 1 - (残差平方和 / 総平方和)
範囲: 0 ～ 1
解釈:
  • 1.0 → 完全な予測
  • 0.8～1.0 → 優秀
  • 0.5～0.8 → 中程度
  • 0.0～0.5 → 要改善
  • マイナス → 悪い（平均値未満の精度）
```

**例:**
```
R² = 0.85 → データの変動の85%をモデルが説明できている
```

### RMSE（二乗平均平方根誤差）

```
式: √(Σ(実際値 - 予測値)² / n)
特徴:
  • 大きな誤差を厳しく評価
  • 目的変数と同じ単位
  • 外れ値の影響を受けやすい
利用: 予測精度の目安
```

### MAE（平均絶対誤差）

```
式: Σ|実際値 - 予測値| / n
特徴:
  • 外れ値に強い
  • 直感的（平均でこのくらい外れる）
  • RMSE より小さい値になる
利用: 中央値ベースの評価
```

**比較例:**
```
RMSE = 10.5, MAE = 8.2
→ 平均8.2ずれる、大きな誤差がある（10.5 > 8.2）
```

---

## 💾 ダウンロードしたモデルの使用方法

### 基本的な使い方

```python
import joblib
import pandas as pd

# ① モデルを読み込む
obj = joblib.load("model__売上_2025年Q1__ランダムフォレスト.joblib")

model        = obj["model"]         # 学習済みモデル
scaler       = obj["scaler"]        # 前処理用スケーラー（SVRのみ）
feature_cols = obj["feature_cols"]  # 特徴量の列名
target_col   = obj["target_col"]    # 目的変数の名前

# ② 新しいデータを準備
new_data = pd.DataFrame({
    "年齢": [30],
    "経験年数": [5],
    "学歴": [4]
})

# ③ スケーリング（SVRの場合のみ）
if scaler is not None:
    new_data_scaled = scaler.transform(new_data)
else:
    new_data_scaled = new_data

# ④ 予測
predictions = model.predict(new_data_scaled)
print(f"予測結果: {predictions[0]:.2f}")
```

### 複数件の予測

```python
# バッチ予測
new_data = pd.DataFrame({
    "年齢": [25, 35, 45],
    "経験年数": [2, 10, 20],
    "学歴": [3, 4, 4]
})
predictions = model.predict(new_data)
# → array([70, 85, 92])
```

### 実装例：バッチ処理

```python
import joblib
import pandas as pd
from pathlib import Path

def batch_predict(model_path, input_csv, output_csv):
    """CSVファイルを一括予測"""
    obj = joblib.load(model_path)
    model = obj["model"]
    scaler = obj["scaler"]
    
    df = pd.read_csv(input_csv)
    X = df[obj["feature_cols"]]
    
    if scaler:
        X = scaler.transform(X)
    
    predictions = model.predict(X)
    df["予測値"] = predictions
    df.to_csv(output_csv, index=False)
    print(f"✓ {output_csv} に保存しました")

# 使用例
batch_predict(
    "model__売上__ランダムフォレスト.joblib",
    "input.csv",
    "output_with_predictions.csv"
)
```

---

## 🛠️ 環境要件と詳細セットアップ

### 必須要件

| 項目 | 要件 |
|------|------|
| **Python** | 3.8 以上 |
| **OS** | Windows / macOS / Linux |
| **RAM** | 2GB 以上（推奨 4GB以上） |
| **ディスク** | 500MB 以上 |

### セットアップ（OS別）

#### Windows

```bash
# 1. リポジトリをクローン
git clone https://github.com/dnakauchi/machinelearn-app.git
cd machinelearn-app

# 2. 仮想環境を作成
python -m venv venv

# 3. 仮想環境を有効化
venv\Scripts\activate

# 4. 依存ライブラリをインストール
pip install -r requirements.txt

# 5. アプリを起動
streamlit run app.py
```

#### macOS / Linux

```bash
# 1. リポジトリをクローン
git clone https://github.com/dnakauchi/machinelearn-app.git
cd machinelearn-app

# 2. 仮想環境を作成
python3 -m venv venv

# 3. 仮想環境を有効化
source venv/bin/activate

# 4. 依存ライブラリをインストール
pip install -r requirements.txt

# 5. アプリを起動
streamlit run app.py
```

### 技術スタック

```
言語:       Python 3.8+
Web フレームワーク: Streamlit 1.35+
機械学習:   scikit-learn 1.3+
データ処理: pandas 2.0+, numpy 1.24+
可視化:    matplotlib 3.7+, seaborn 0.12+
ファイル処理: openpyxl 3.1+
モデル保存: joblib (sklearn付属)
```

---

## 📋 入力データのベストプラクティス

### データ形式の例

✅ **良い例**

```csv
顧客ID,年齢,購買額,来店頻度,満足度
1,25,150,5,4.5
2,35,250,10,4.8
3,45,300,15,5.0
```

❌ **悪い例**

```
顧客ID    年齢    購買額    来店頻度    満足度
1         25      150      5          4.5
2         35      250      10         4.8
3         45      300      15         5.0
（スペース区切り → CSVに変換すること）
```

❌ **カテゴリ変数がある場合**

```csv
顧客ID,名前,性別,年齢,購買額
1,田中,男,25,150
2,山田,女,35,250
```

→ 数値化してから使用：

```csv
顧客ID,性別_コード,年齢,購買額
1,1,25,150
2,2,35,250
（性別: 男=1, 女=2）
```

### データクリーニングのコツ

| 問題 | 対策 |
|------|------|
| **欠損値** | 削除 or 補完（平均値など）してからアップロード |
| **外れ値** | 極端な値は削除するか別途確認 |
| **文字列** | 数値に変換 |
| **日付** | Unix タイムスタンプなど数値に変換 |
| **カテゴリ変数** | One-Hot エンコーディングで数値化 |

---

## ❓ よくある質問（FAQ）

### 🤔 使い方

**Q1: モデルを本番環境で使えますか？**
```
A: はい。ダウンロードした .joblib ファイルを使用して、
   Python環境で予測できます。
```

**Q2: 複数の目的変数で同時に学習できますか？**
```
A: はい。「被説明変数」で複数選択すれば、
   各目的変数について別々に学習・評価されます。
```

**Q3: モデルは自動的に保存されますか？**
```
A: いいえ。結果画面から手動でダウンロードしてください。
   （Streamlit Cloud では一時ストレージなため）
```

### 📊 データ・精度

**Q4: どのアルゴリズムを選ぶべき？**
```
A: 迷ったら「ランダムフォレスト」をお勧めします。
   最もバランスの取れた精度が得られることが多いです。
```

**Q5: R² が 0.5 以下。モデルが悪いのか？**
```
A: データの複雑さによります。
   - 改善案1: 説明変数を追加
   - 改善案2: データの質をチェック
   - 改善案3: 目的変数選択を見直す
```

**Q6: 小さいデータセット（数十行）でも動きますか？**
```
A: 動きますが、精度は期待できません。
   推奨: 最低 100 行、理想的には 1,000 行以上
```

### 🔐 セキュリティ・プライバシー

**Q7: アップロードしたデータは安全ですか？**
```
A: 
 - ローカル実行: ローカルPC内で処理
 - Streamlit Cloud: サーバーで一時処理 → 自動削除
 - 本番利用なら「ローカル実行」推奨
```

**Q8: 個人情報を含むデータでも大丈夫？**
```
A: セキュリティ上、個人情報は含めないことを推奨。
   必要な場合は、マスキング処理してからアップロード。
```

### ⚠️ トラブル

**Q9: CSV が文字化けします**
```
A: 
 1. Excel で開く
 2. 「名前を付けて保存」
 3. ファイル形式: CSV (UTF-8)
 4. 保存
```

**Q10: 「メモリ不足」エラー**
```
A:
 - ローカル実行を試す
 - または Streamlit Cloud の有料プランへアップグレード
 - データサイズを削減（サンプリング）
```

**Q11: モデル学習が終わらない**
```
A:
 - Ctrl+C で中止
 - データサイズを削減
 - 説明変数の数を減らす
 - ローカルで実行（高速）
```

---

## 🔒 セキュリティと制限

### ファイルアップロード制限

```
最大ファイルサイズ: 100MB
最大行数:          100,000 行
最大列数:          500 列
最小行数:          10 行
```

### セキュリティ機能

- ✅ ファイルサイズ・データサイズの自動チェック
- ✅ エラーメッセージの情報漏洩防止
- ✅ CSRF トークン保護
- ✅ タイムアウト処理
- ✅ キャッシュによるメモリ効率化

---

## 📈 パフォーマンス目安

| データサイズ | 学習時間 | メモリ使用量 | 推奨環境 |
|------------|---------|-----------|----------|
| 100 行 × 5 列 | < 1秒 | < 50MB | 任意 |
| 1,000 行 × 10 列 | 1～3秒 | 100MB | ローカル or Cloud |
| 10,000 行 × 20 列 | 5～15秒 | 300MB | ローカル推奨 |
| 100,000 行 × 50 列 | 30～60秒 | 800MB | ローカルのみ |

---

## 🚀 デプロイ

### Streamlit Cloud へのデプロイ

詳細は [DEPLOYMENT.md](DEPLOYMENT.md) を参照

```bash
# 1. Streamlit Cloud にサインアップ
#    https://share.streamlit.io

# 2. GitHub リポジトリを接続
#    Repository: dnakauchi/machinelearn-app
#    Branch: main
#    Main file: app.py

# 3. 今後、git push するだけで自動デプロイ
git push origin main
```

---

## 🛣️ ロードマップ

### Version 1.1（近日実装予定）

- [ ] 分類問題への対応（ロジスティック回帰など）
- [ ] テキストデータ処理（TFIDF など）
- [ ] 自動ハイパーパラメータ調整
- [ ] クロスバリデーション結果の表示

### Version 1.2

- [ ] ユーザー認証機能
- [ ] モデルの保存・管理
- [ ] バッチ予測機能
- [ ] データセットの共有機能

### Version 2.0

- [ ] 深層学習（ニューラルネットワーク）対応
- [ ] 時系列予測対応
- [ ] 自動機械学習（AutoML）機能
- [ ] REST API サーバー提供

---

## 🤝 開発への参加

### バグ報告

```
GitHub Issues → 「New Issue」 → 環境・再現手順を記載
```

### 機能提案

```
「Discussions」タブで機能リクエスト議論
```

### コード貢献

```bash
# フォーク → ローカルで改善 → Pull Request
```

**コントリビューション例:**
- アルゴリズムの追加
- UI 改善
- 日本語以外への言語対応
- パフォーマンス改善
- ドキュメント改善

---

## 👨‍💻 開発環境セットアップ（開発者向け）

```bash
# リポジトリをクローン
git clone https://github.com/dnakauchi/machinelearn-app.git
cd machinelearn-app

# 開発用依存ライブラリをインストール
pip install -r requirements.txt
pip install black flake8 pytest  # 開発ツール

# コード品質チェック
black app.py      # フォーマット
flake8 app.py     # リント

# テスト実行
pytest tests/     # 単体テスト

# ローカルで実行
streamlit run app.py --logger.level=debug
```

---

## 📚 参考資料・外部リンク

### 機械学習の学習

- 📖 [scikit-learn 公式ドキュメント](https://scikit-learn.org/)
- 📖 [Kaggle 機械学習チュートリアル](https://www.kaggle.com/learn/intro-to-machine-learning)
- 📖 [Andrew Ng「Machine Learning」Coursera](https://www.coursera.org/learn/machine-learning)

### Streamlit

- 📖 [Streamlit 公式ドキュメント](https://docs.streamlit.io/)
- 📖 [Streamlit Cloud デプロイガイド](https://docs.streamlit.io/streamlit-cloud)

### Python

- 📖 [Python 公式ドキュメント](https://docs.python.org/3/)
- 📖 [pandas チュートリアル](https://pandas.pydata.org/docs/)

---

## 📄 変更履歴

### v1.0.0 (2026-05-29)

**初版リリース**
- ✨ 6つのアルゴリズムに対応
- ✨ 複数目的変数対応
- ✨ 寄与度グラフ表示
- ✨ 分布図行列表示
- ✨ モデルのダウンロード機能
- 🔒 セキュリティ機能実装
- 📱 Streamlit Cloud 対応
- 📚 日本語ドキュメント完備

---

## 📄 ライセンス

MIT License - 自由に利用、改変、配布可能

```
詳細は LICENSE ファイルを参照
```

---

## 🙋 サポート・コンタクト

| 項目 | 連絡先 |
|------|--------|
| **バグ報告** | GitHub Issues |
| **機能提案** | GitHub Discussions |
| **一般的な質問** | GitHub Discussions |
| **セキュリティ問題** | Email にてご連絡ください |

---

## 🎓 このプロジェクトが役立つなら

- ⭐ Star をお願いします
- 🍴 Fork して改善提案してください
- 📢 友人に紹介してください

---

<div align="center">

**Made with ❤️ by dnakauchi**

**最終更新:** 2026-05-29

![GitHub Stars](https://img.shields.io/github/stars/dnakauchi/machinelearn-app?style=flat-square)
![GitHub Forks](https://img.shields.io/github/forks/dnakauchi/machinelearn-app?style=flat-square)

</div>
