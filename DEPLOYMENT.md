# Streamlit Cloud デプロイガイド

## ステップバイステップ

### 1. GitHub リポジトリの準備

すべての変更をコミット・プッシュ：

```bash
git add .
git commit -m "Prepare for Streamlit Cloud deployment"
git push origin main
```

### 2. Streamlit Cloud アカウント作成

1. https://share.streamlit.io にアクセス
2. **「Sign up with GitHub」** をクリック
3. GitHub で認証

### 3. アプリをデプロイ

1. Streamlit Cloud ダッシュボードで **「+ New app」**
2. 以下を設定：
   ```
   Repository: dnakauchi/machinelearn-app
   Branch: main
   Main file path: app.py
   ```
3. **「Deploy」** をクリック

### 4. デプロイ完了

- URL が発行されます：`https://machinelearn-app.streamlit.app`
- 初回は 2〜3 分かかります

## セキュリティ設定

### Streamlit Cloud での環境変数管理

敏感情報（API キーなど）がある場合：

1. アプリ設定を開く
2. **「Secrets」** をクリック
3. 以下の形式で入力：
   ```toml
   api_key = "your-secret-here"
   db_password = "..."
   ```

コード内で以下でアクセス：
```python
import streamlit as st
api_key = st.secrets["api_key"]
```

### リソース制限

Streamlit Cloud の無料プランの制限：

| 項目 | 制限 |
|------|------|
| メモリ | 1GB |
| CPU | 共有 |
| ストレージ | 1GB（一時） |
| 実行時間 | 最大 24 時間連続 |
| 月間使用時間 | 無制限 |

## 自動デプロイメントの有効化

GitHub にプッシュするたびに自動デプロイされます：

```bash
git push origin main
# → Streamlit Cloud が自動的に再デプロイ
```

## トラブルシューティング

### デプロイエラー：「requirements.txt not found」

解決法：
```bash
ls -la | grep requirements.txt
```

ファイルが存在することを確認。存在しない場合：
```bash
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Add requirements.txt"
git push origin main
```

### アプリが遅い / 落ちる

- CSV/Excel ファイルサイズが大きすぎないか確認
- ローカルで動作確認
```bash
streamlit run app.py --logger.level=debug
```

### メモリ不足エラー

Streamlit Cloud は無料プランで 1GB に制限されています。

**対策：**
1. キャッシュを有効化（既に実装済み）
2. ファイルサイズを制限（既に実装済み：100MB）
3. [有料プランへのアップグレード](https://streamlit.io/cloud)を検討

## モニタリング

Streamlit Cloud ダッシュボード：
- ログの確認
- アクセス数の追跡
- 使用状況の確認

## カスタムドメイン（有料機能）

有料プランでカスタムドメイン設定可能：
- `https://yourcompany.com` など

## セキュリティチェックリスト

- ✅ `.gitignore` で `secrets.toml` を除外
- ✅ `.streamlit/config.toml` で安全な設定
- ✅ ファイルサイズ制限（100MB）
- ✅ データ行数制限（100,000 行）
- ✅ 列数制限（500 列）
- ✅ エラーメッセージの情報漏洩防止
- ✅ CORS 無効化

## よくある質問

### Q: 誰でもアプリにアクセスできますか？
**A:** はい、デフォルトは公開です。認証は有料プランでの追加機能です。

### Q: 学習済みモデルはダウンロードできますか？
**A:** はい、`.joblib` 形式でダウンロード可能です。

### Q: 大規模データの処理はできますか？
**A:** 無料プランは 1GB メモリに制限されています。有料プランへのアップグレードを検討してください。

---

**デプロイ完了後の URL 例:**
```
https://machinelearn-app.streamlit.app
```

この URL をユーザーと共有してください。
