# 🔐 セキュリティレビューレポート

**プロジェクト:** 機械学習モデル作成アプリ  
**レビュー日:** 2026-05-29  
**レビュー対象:** app.py, requirements.txt, .streamlit/config.toml  
**評価:** ⚠️ **中程度のセキュリティリスク** (本番環境では改善推奨)

---

## 📊 セキュリティスコア

| 項目 | スコア | 状態 |
|------|--------|------|
| **入力検証** | ⭐⭐⭐⭐ (8/10) | ✅ 良好 |
| **認証・認可** | ⭐⭐ (2/10) | ⚠️ 未実装 |
| **暗号化** | ⭐ (0/10) | ⚠️ 未実装 |
| **エラーハンドリング** | ⭐⭐⭐ (6/10) | ⚠️ 改善推奨 |
| **依存関係管理** | ⭐⭐⭐ (6/10) | ⚠️ 改善推奨 |
| **ファイル処理** | ⭐⭐⭐ (6/10) | ⚠️ 改善推奨 |
| **メモリ・リソース管理** | ⭐⭐⭐ (7/10) | ✅ 良好 |
| **ロギング・監査** | ⭐ (2/10) | ⚠️ 未実装 |
| **総合スコア** | **4.9/10** | ⚠️ **中程度** |

---

## ✅ 検出した良好な実装

### 1. **ファイルサイズ制限** ✓ 良好

```python
MAX_FILE_SIZE_MB = 100
if file_size_mb > MAX_FILE_SIZE_MB:
    st.error("...")
    st.stop()
```

**効果:** DoS 攻撃 (大容量ファイルアップロード) を防止  
**推奨値:** 100MB は適切

---

### 2. **データサイズ制限** ✓ 良好

```python
MAX_ROWS = 100000
MAX_COLS = 500
if len(df) > MAX_ROWS or len(df.columns) > MAX_COLS:
    st.error("...")
```

**効果:** メモリ枯渇、計算量爆発を防止  
**推奨値:** 100K行 × 500列は適切

---

### 3. **エラーメッセージの情報隠蔽** ✓ 良好

`.streamlit/config.toml`:
```toml
[client]
showErrorDetails = false
```

**効果:** スタックトレース、内部パス等の情報漏洩防止  
**推奨:** 本番環境では必須

---

### 4. **CSRF 保護** ✓ 良好

```toml
[server]
enableXsrfProtection = true
```

**効果:** クロスサイトリクエストフォージェリ攻撃を防止

---

### 5. **エンコーディング自動検出** ✓ 良好

```python
for enc in ("utf-8-sig", "utf-8", "shift-jis", "cp932"):
    try:
        file.seek(0)
        return pd.read_csv(file, encoding=enc)
    except (UnicodeDecodeError, Exception):
        continue
```

**効果:** 様々なファイル形式に対応、ユーザーの手間削減  
**配慮:** ユーザーフレンドリー

---

### 6. **依存関係のバージョン制御** ✓ 良好

```
streamlit>=1.35.0
pandas>=2.0.0
scikit-learn>=1.3.0
```

**効果:** 既知の脆弱性を持つ古いバージョンを避ける  
**推奨:** `==` で固定バージョン化をさらに検討

---

## ⚠️ 検出した脆弱性と改善案

### 【重度】1. 警告の無視（本番環境では危険）

**現在のコード:**
```python
warnings.filterwarnings("ignore")  # ❌ 危険
```

**問題:**
- セキュリティ関連の警告が無視される
- 将来のバージョンで動作しなくなる可能性
- デバッグが困難

**改善案 1（推奨）:**
```python
# 特定の警告のみ無視
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", message=".*some_specific_warning.*")
```

**改善案 2:**
```python
# 本番環境では有効化
import os
if os.getenv("ENV") != "production":
    warnings.filterwarnings("ignore")
```

**修正優先度:** 🔴 **高**

---

### 【中度】2. 過度に広い例外処理

**現在のコード:**
```python
except (UnicodeDecodeError, Exception):  # ❌ Exception は広すぎる
    continue
```

**問題:**
- `KeyboardInterrupt` や `SystemExit` も捕捉してしまう
- エラーの本質が隠される
- デバッグが困難

**改善案:**
```python
except (UnicodeDecodeError, pd.errors.ParserError, ValueError) as e:
    logger.debug(f"エンコーディング {enc} 失敗: {e}")
    continue
```

**修正優先度:** 🟡 **中**

---

### 【中度】3. ファイル拡張子検証が不足

**現在のコード:**
```python
uploaded_file = st.file_uploader(
    "...",
    type=["xlsx", "xls", "csv"],  # UI レベルのみ
)

name = file.name.lower()
if name.endswith(".csv"):  # ❌ 拡張子スプーフィングの可能性
    ...
return pd.read_excel(file)  # エラーハンドリングなし
```

**問題:**
- 拡張子スプーフィング (`file.txt` を `file.csv` に改名)
- 不正なファイル形式での攻撃
- read_excel で予期しない例外

**改善案:**
```python
import magic  # python-magic ライブラリ

def validate_file_type(file) -> str:
    """MIME タイプで検証"""
    mime = magic.from_buffer(file.read(512), mime=True)
    file.seek(0)
    
    allowed_mimes = {
        "text/csv": "csv",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "xlsx",
        "application/vnd.ms-excel": "xls",
    }
    
    if mime not in allowed_mimes:
        raise ValueError(f"不正なファイル形式: {mime}")
    
    return allowed_mimes[mime]
```

**修正優先度:** 🟡 **中**

---

### 【中度】4. XML ボム / Zip ボム対策がない

**問題:**
- openpyxl, xlrd で XML / Zip ボムの脆弱性がある
- 悪意あるファイルでサーバーを停止させられる可能性

**改善案:**
```python
# requirements.txt に以下を追加
defusedxml>=0.0.13  # XML ボム対策

# app.py で使用
from defusedxml import ElementTree as ET
import defusedxml.ElementTree
openpyxl.load_workbook(file, data_only=True)  # 安全版を使用
```

**修正優先度:** 🟡 **中**

---

### 【中度】5. キャッシュの有効期限がない

**現在のコード:**
```python
@st.cache_data  # ❌ 永続キャッシュ
def load_file(file) -> pd.DataFrame:
    ...
```

**問題:**
- ユーザー B が同じ名前のファイルをアップロード → ユーザー A のキャッシュが返される
- メモリリーク（Streamlit Cloud で制限あり）

**改善案:**
```python
from datetime import timedelta

@st.cache_data(ttl=timedelta(hours=1))  # 1時間で失効
def load_file(file) -> pd.DataFrame:
    ...
```

**修正優先度:** 🟡 **中**

---

### 【軽度】6. ダウンロードファイルへの署名がない

**問題:**
- ユーザーが改ざんされたモデルをダウンロードしたことに気づかない
- 供給チェーン攻撃のリスク

**改善案:**
```python
import hashlib
import hmac

def sign_model(obj: dict, secret: str) -> bytes:
    """モデルに HMAC 署名を追加"""
    model_bytes = joblib.dumps(obj)
    signature = hmac.new(
        secret.encode(), 
        model_bytes, 
        hashlib.sha256
    ).hexdigest()
    return joblib.dumps({"data": obj, "signature": signature})

def verify_model(signed_bytes: bytes, secret: str) -> dict:
    """署名を検証"""
    loaded = joblib.loads(signed_bytes)
    expected_sig = hmac.new(
        secret.encode(),
        joblib.dumps(loaded["data"]),
        hashlib.sha256
    ).hexdigest()
    if not hmac.compare_digest(loaded["signature"], expected_sig):
        raise ValueError("改ざんされたモデル")
    return loaded["data"]
```

**修正優先度:** 🟢 **低** (プロトタイプ段階では不要)

---

### 【軽度】7. ロギング・監査が未実装

**問題:**
- セキュリティイベント（大容量ファイル、エラーなど）の記録がない
- 攻撃検知ができない

**改善案:**
```python
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger(__name__)
handler = RotatingFileHandler(
    "app.log", 
    maxBytes=10_000_000,  # 10MB
    backupCount=5
)
logger.addHandler(handler)

# 使用例
logger.info(f"ファイルアップロード: {file.name}, サイズ: {file_size_mb:.1f}MB")
logger.warning(f"ファイルサイズ超過: {file_size_mb:.1f}MB (制限: {MAX_FILE_SIZE_MB}MB)")
logger.error(f"読み込みエラー: {e}")
```

**修正優先度:** 🟢 **低**

---

### 【軽度】8. 乱数シードが固定

**現在のコード:**
```python
RandomForestRegressor(n_estimators=100, random_state=42)  # ❌ 本番では予測可能
```

**問題:**
- 再現性は必要だが、本番環境では予測可能性は悪
- セキュリティ観点では問題ないが、ML 品質面で注意

**改善案:**
```python
import os

def get_random_state():
    """環境に応じて乱数シードを決定"""
    if os.getenv("ENV") == "production":
        return None  # ランダムに
    else:
        return 42  # 開発環境では固定

random_state = get_random_state()
RandomForestRegressor(n_estimators=100, random_state=random_state)
```

**修正優先度:** 🟢 **低**

---

### 【軽度】9. バージョン番号が正確でない

**requirements.txt:**
```
streamlit>=1.35.0
pandas>=2.0.0
```

**問題:**
- `>=` は柔軟だが、予期しないバージョン間での不具合の可能性
- 既知の脆弱性を持つバージョンが入る可能性

**改善案:**
```
streamlit==1.35.0
pandas==2.0.3
numpy==1.24.4
scikit-learn==1.3.2
```

**修正優先度:** 🟢 **低（ただし本番環境では推奨）**

---

## 🛡️ 認証・認可（未実装）

**現在:** 完全に公開  
**リスク:** なし（ウェブアプリの性質上、認証不要と判断）

**必要に応じた実装:**
```python
import streamlit_authenticator as stauth

names = ["Admin"]
usernames = ["admin"]
passwords = ["hashed_password_here"]

authenticator = stauth.Authenticate(names, usernames, passwords, "app", "abcdef")
name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status:
    st.write(f'Welcome {name}')
    authenticator.logout("Logout", "sidebar")
else:
    st.error("ユーザー認証に失敗しました")
    st.stop()
```

**優先度:** 🟢 **低** (現在は不要)

---

## 🔒 データ暗号化（未実装）

**現在:** 未実装  
**Streamlit Cloud での対策:**
- HTTPS: ✅ 自動で有効化
- ファイル転送: ✅ TLS 1.2+
- ストレージ: ⚠️ 一時ファイルのみ（暗号化なし）

**本番環境での推奨:**
```python
from cryptography.fernet import Fernet

def encrypt_sensitive_data(data: str, key: bytes) -> str:
    f = Fernet(key)
    return f.encrypt(data.encode()).decode()

def decrypt_sensitive_data(token: str, key: bytes) -> str:
    f = Fernet(key)
    return f.decrypt(token.encode()).decode()
```

**優先度:** 🟢 **低（クラウド環境では TLS で十分）**

---

## 🧪 脆弱性チェック結果

### 依存関係のセキュリティスキャン

```bash
# 実行コマンド
pip install safety
safety check -r requirements.txt
```

**推奨:** GitHub の Dependabot で自動チェック

---

## 📋 改善優先度まとめ

| 優先度 | 項目 | 対応 | 影響度 |
|--------|------|------|--------|
| 🔴 高 | warnings.filterwarnings("ignore") | 即時改善 | 中 |
| 🟡 中 | 過度な例外処理 | 1～2週間 | 低 |
| 🟡 中 | ファイル型検証（MIME） | 1～2週間 | 中 |
| 🟡 中 | XML ボム対策 | 1～2週間 | 高 |
| 🟡 中 | キャッシュ有効期限 | 1～2週間 | 中 |
| 🟢 低 | ファイル署名 | オプション | 低 |
| 🟢 低 | ロギング実装 | オプション | 低 |
| 🟢 低 | バージョン正確化 | オプション | 低 |

---

## ✅ 実装推奨リスト

### フェーズ 1（今週中）：必須修正

```python
# 1. 警告処理の改善
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# 2. 例外処理の改善
try:
    return pd.read_csv(file, encoding=enc)
except (UnicodeDecodeError, pd.errors.ParserError):
    continue
```

### フェーズ 2（1～2週間）：推奨修正

```bash
# requirements.txt に追加
defusedxml>=0.0.13
python-magic>=0.4.27

# app.py で使用
import defusedxml.ElementTree
from magic import Magic
```

### フェーズ 3（本番環境化時）：オプション

- ロギング実装
- バージョン固定化
- ファイル署名

---

## 🎯 結論

| 項目 | 評価 |
|------|------|
| **現在の安全性** | ✅ 開発・テスト環境では安全 |
| **本番環境への適性** | ⚠️ 改善が必要 |
| **優先修正項目** | 🔴 warnings フィルタ、XML ボム対策 |
| **全体的なセキュリティレベル** | 中程度（改善で改良可能） |

---

## 📝 セキュリティベストプラクティス推奨事項

```markdown
1. ✅ GitHub で Dependabot を有効化
2. ✅ requirements.txt で fixed version を使用
3. ✅ CI/CD パイプルで safety/bandit を実行
4. ✅ 定期的なセキュリティ監査（3～6ヶ月ごと）
5. ✅ ユーザーデータは暗号化・秘匿化
6. ✅ アップロード後のファイルは即座に削除
7. ✅ ログ記録とモニタリング
8. ✅ セキュリティ脆弱性の即報告体制
```

---

**レビュー実施者:** Claude Code  
**レビュー完了日:** 2026-05-29  
**次回レビュー予定日:** 2026-08-29（3ヶ月後）
