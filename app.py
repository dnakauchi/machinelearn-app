import io
import platform
import warnings

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st
import joblib
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import Lasso, LinearRegression, Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.inspection import permutation_importance
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR

# ── Japanese font fix ─────────────────────────────────────────────────────────
_FONTS = {"Windows": "MS Gothic", "Darwin": "Hiragino Sans", "Linux": "IPAexGothic"}
matplotlib.rcParams["font.family"] = _FONTS.get(platform.system(), "sans-serif")
matplotlib.rcParams["axes.unicode_minus"] = False

warnings.filterwarnings("ignore")

st.set_page_config(page_title="ML モデル作成アプリ", layout="wide")

ALGORITHMS = {
    "線形回帰":        lambda: LinearRegression(),
    "リッジ回帰":      lambda: Ridge(),
    "ラッソ回帰":      lambda: Lasso(),
    "ランダムフォレスト": lambda: RandomForestRegressor(n_estimators=100, random_state=42),
    "勾配ブースティング": lambda: GradientBoostingRegressor(random_state=42),
    "サポートベクター回帰": lambda: SVR(),
}
SVR_NAME = "サポートベクター回帰"


# ── Data loading ──────────────────────────────────────────────────────────────

@st.cache_data
def load_file(file) -> pd.DataFrame:
    name = file.name.lower()
    if name.endswith(".csv"):
        for enc in ("utf-8-sig", "utf-8", "shift-jis", "cp932"):
            try:
                file.seek(0)
                return pd.read_csv(file, encoding=enc)
            except (UnicodeDecodeError, Exception):
                continue
        file.seek(0)
        return pd.read_csv(file, encoding="utf-8", errors="replace")
    return pd.read_excel(file)


# ── Model training ────────────────────────────────────────────────────────────

def train_model(name, X_train, X_test, y_train, y_test):
    """Returns metrics dict, y_pred array, fitted model, and scaler (or None)."""
    model = ALGORITHMS[name]()
    scaler = None
    Xtr, Xte = X_train.copy(), X_test.copy()

    if name == SVR_NAME:
        scaler = StandardScaler()
        Xtr = scaler.fit_transform(Xtr)
        Xte = scaler.transform(Xte)

    model.fit(Xtr, y_train)
    y_pred = model.predict(Xte)

    metrics = {
        "R²":   round(r2_score(y_test, y_pred), 4),
        "RMSE": round(np.sqrt(mean_squared_error(y_test, y_pred)), 4),
        "MAE":  round(mean_absolute_error(y_test, y_pred), 4),
    }
    return metrics, y_pred, model, scaler


# ── Plotting ──────────────────────────────────────────────────────────────────

def plot_pred_vs_actual(y_test, y_pred, title: str):
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.scatter(y_test, y_pred, alpha=0.6, s=20,
               color="steelblue", label="予測値")
    lo = min(float(np.min(y_test)), float(np.min(y_pred)))
    hi = max(float(np.max(y_test)), float(np.max(y_pred)))
    ax.plot([lo, hi], [lo, hi], "r--", linewidth=1.5, label="完全予測線")
    ax.set_xlabel("実際の値")
    ax.set_ylabel("予測値")
    ax.set_title(title, fontsize=9)
    ax.legend(fontsize=8)
    fig.tight_layout()
    return fig


def get_feature_importance(
    name: str, model, scaler, X_test: pd.DataFrame, y_test: pd.Series, feature_cols: list
) -> tuple[pd.Series, str]:
    """
    Returns (importance_series, kind).
    kind: 'coef' for linear models, 'importance' for tree models, 'permutation' for SVR.
    Linear models return signed coefficients; others return non-negative values.
    """
    if name in ("線形回帰", "リッジ回帰", "ラッソ回帰"):
        return pd.Series(model.coef_, index=feature_cols), "coef"

    if name in ("ランダムフォレスト", "勾配ブースティング"):
        return pd.Series(model.feature_importances_, index=feature_cols), "importance"

    # SVR — use permutation importance on scaled data
    Xte = scaler.transform(X_test) if scaler is not None else X_test.values
    result = permutation_importance(model, Xte, y_test, n_repeats=10, random_state=42)
    return pd.Series(result.importances_mean, index=feature_cols), "permutation"


def plot_feature_importance(series: pd.Series, title: str, kind: str):
    sorted_s = series.reindex(series.abs().sort_values().index)
    colors = ["tomato" if v < 0 else "steelblue" for v in sorted_s]
    height = max(3.0, len(series) * 0.45)

    fig, ax = plt.subplots(figsize=(5, height))
    ax.barh(sorted_s.index, sorted_s.values, color=colors)
    ax.axvline(0, color="black", linewidth=0.8)

    if kind == "coef":
        ax.set_xlabel("係数  (正: 正の影響 / 負: 負の影響)")
    elif kind == "importance":
        ax.set_xlabel("重要度（不純度減少量）")
    else:
        ax.set_xlabel("置換重要度（スコア低下量）")

    ax.set_title(title, fontsize=9)
    fig.tight_layout()
    return fig


def plot_correlation_matrix(df: pd.DataFrame, cols: list):
    corr = df[cols].corr()
    size = max(6, len(cols))
    fig, ax = plt.subplots(figsize=(size, max(4, size - 1)))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm",
                center=0, square=True, ax=ax, annot_kws={"size": 8})
    ax.set_title("相関行列", fontsize=12)
    fig.tight_layout()
    return fig


# ── Model serialization ───────────────────────────────────────────────────────

def to_bytes(model, scaler, feature_cols: list, target_col: str) -> bytes:
    buf = io.BytesIO()
    joblib.dump({
        "model":        model,
        "scaler":       scaler,
        "feature_cols": feature_cols,
        "target_col":   target_col,
    }, buf)
    buf.seek(0)
    return buf.read()


def highlight_best(s):
    return ["background-color: #d4edda" if i == 0 else "" for i in range(len(s))]


# ── UI ────────────────────────────────────────────────────────────────────────

st.title("機械学習モデル作成アプリ")
st.caption("Excel / CSV をアップロードするだけで複数の機械学習モデルを比較・評価できます。")

uploaded_file = st.file_uploader(
    "ファイルをアップロード (.xlsx / .xls / .csv)",
    type=["xlsx", "xls", "csv"],
)

if not uploaded_file:
    st.info("まず Excel または CSV ファイルをアップロードしてください。")
    st.stop()

df = load_file(uploaded_file)

st.subheader("データプレビュー")
st.dataframe(df.head(10), use_container_width=True)
st.caption(f"行数: {len(df):,}　列数: {len(df.columns)}")

numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
if len(numeric_cols) < 2:
    st.error("数値列が 2 列以上必要です。")
    st.stop()

# ── Variable selection ────────────────────────────────────────────────────────

st.subheader("変数の設定")
col_left, col_right = st.columns(2)

with col_left:
    target_cols = st.multiselect(
        "被説明変数（目的変数）※複数選択可",
        options=numeric_cols,
        default=[numeric_cols[-1]],
    )

with col_right:
    available_features = [c for c in numeric_cols if c not in target_cols]
    feature_cols = st.multiselect(
        "説明変数（特徴量）",
        options=available_features,
        default=available_features,
    )

# ── Algorithm & split settings ────────────────────────────────────────────────

st.subheader("アルゴリズムと学習設定")
col_algo, col_split = st.columns([3, 1])

with col_algo:
    selected_algos = st.multiselect(
        "使用するアルゴリズム",
        options=list(ALGORITHMS.keys()),
        default=["線形回帰", "ランダムフォレスト", "勾配ブースティング"],
    )

with col_split:
    test_size_pct = st.slider(
        "テストデータ割合",
        min_value=10, max_value=40, value=20, step=5,
        format="%d%%",
        help="全データのうちモデル評価に使う割合",
    )
    test_size = test_size_pct / 100

can_run = bool(target_cols and feature_cols and selected_algos)
run = st.button("モデルを作成・評価", type="primary", disabled=not can_run)

if not run:
    st.stop()

# ── Training loop (one section per target variable) ───────────────────────────

all_cols = list(dict.fromkeys(feature_cols + target_cols))
data = df[all_cols].dropna()
if len(data) < 10:
    st.error("欠損除去後のデータが少なすぎます（10 行以上必要）。")
    st.stop()

X = data[feature_cols]

for target_col in target_cols:
    y = data[target_col]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42
    )

    st.markdown("---")
    st.markdown(f"## 目的変数: **{target_col}**")

    results = []
    predictions: dict[str, np.ndarray] = {}
    trained: dict[str, tuple] = {}   # name -> (model, scaler)

    progress = st.progress(0, text=f"[{target_col}] 学習中...")
    for i, name in enumerate(selected_algos):
        progress.progress(
            (i + 1) / len(selected_algos),
            text=f"[{target_col}] {name} を学習中...",
        )
        metrics, y_pred, model, scaler = train_model(
            name, X_train, X_test, y_train, y_test
        )
        results.append({"アルゴリズム": name, **metrics})
        predictions[name] = y_pred
        trained[name] = (model, scaler)

    progress.empty()

    # Scores table
    st.subheader("モデルスコア比較")
    results_df = (
        pd.DataFrame(results)
        .sort_values("R²", ascending=False)
        .reset_index(drop=True)
    )
    best = results_df.iloc[0]
    st.success(f"最良モデル: **{best['アルゴリズム']}**　R² = {best['R²']}")
    st.dataframe(
        results_df.style.apply(highlight_best, axis=0),
        use_container_width=True,
        hide_index=True,
    )

    # Predicted vs actual plots
    st.subheader("予測値 vs 実際の値")
    n_cols = min(len(selected_algos), 3)
    plot_cols = st.columns(n_cols)
    for i, name in enumerate(selected_algos):
        with plot_cols[i % n_cols]:
            fig = plot_pred_vs_actual(
                y_test.values, predictions[name],
                f"{name}\n({target_col})",
            )
            st.pyplot(fig)
            plt.close(fig)

    # Feature importance
    st.subheader("説明変数の寄与度")
    fi_note = {
        "coef":        "係数の大きさ（絶対値が大きいほど影響大。正負で方向を示す）",
        "importance":  "不純度に基づく重要度（値が大きいほど予測に貢献）",
        "permutation": "置換重要度（その変数をシャッフルしたときのスコア低下量）",
    }
    fi_cols = st.columns(min(len(selected_algos), 3))
    for i, name in enumerate(selected_algos):
        model, scaler = trained[name]
        imp_series, kind = get_feature_importance(
            name, model, scaler, X_test, y_test, feature_cols
        )
        with fi_cols[i % 3]:
            st.caption(fi_note[kind])
            fig = plot_feature_importance(
                imp_series, f"{name}\n({target_col})", kind
            )
            st.pyplot(fig)
            plt.close(fig)

    # Model download
    st.subheader("学習済みモデルのダウンロード")
    st.caption("ダウンロードした `.joblib` ファイルは `joblib.load()` で読み込めます。")

    dl_cols = st.columns(min(len(selected_algos), 3))
    for i, name in enumerate(selected_algos):
        model, scaler = trained[name]
        model_bytes = to_bytes(model, scaler, feature_cols, target_col)
        safe = lambda s: s.replace("/", "_").replace(" ", "_")
        filename = f"model__{safe(target_col)}__{safe(name)}.joblib"
        with dl_cols[i % 3]:
            st.download_button(
                label=f"⬇ {name}",
                data=model_bytes,
                file_name=filename,
                mime="application/octet-stream",
                key=f"dl_{target_col}_{name}",
            )

    with st.expander("モデルの使い方（コード例）"):
        st.code(
            f"""import joblib
import pandas as pd

# モデルを読み込む
obj = joblib.load("model__{safe(target_col)}__{safe(best['アルゴリズム'])}.joblib")
model  = obj["model"]
scaler = obj["scaler"]   # SVR 以外は None

# 新しいデータで予測
X_new = pd.DataFrame([{{ col: 値 for col in {feature_cols} }}])
if scaler:
    X_new = scaler.transform(X_new)
pred = model.predict(X_new)
print(pred)
""",
            language="python",
        )

# Correlation matrix (once, covering all selected columns)
st.markdown("---")
st.subheader("相関行列")
fig = plot_correlation_matrix(data, feature_cols + target_cols)
st.pyplot(fig)
plt.close(fig)
