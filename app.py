import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import Lasso, LinearRegression, Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR

warnings.filterwarnings("ignore")

st.set_page_config(page_title="ML モデル作成アプリ", layout="wide")

ALGORITHMS = {
    "線形回帰": lambda: LinearRegression(),
    "リッジ回帰": lambda: Ridge(),
    "ラッソ回帰": lambda: Lasso(),
    "ランダムフォレスト": lambda: RandomForestRegressor(n_estimators=100, random_state=42),
    "勾配ブースティング": lambda: GradientBoostingRegressor(random_state=42),
    "サポートベクター回帰": lambda: SVR(),
}

SVR_NAME = "サポートベクター回帰"


def load_excel(file) -> pd.DataFrame:
    return pd.read_excel(file)


def evaluate_model(model, X_train, X_test, y_train, y_test, scaled=False):
    scaler = None
    if scaled:
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    return {
        "R²": round(r2_score(y_test, y_pred), 4),
        "RMSE": round(np.sqrt(mean_squared_error(y_test, y_pred)), 4),
        "MAE": round(mean_absolute_error(y_test, y_pred), 4),
    }, y_pred


def plot_pred_vs_actual(y_test, y_pred, title: str):
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.scatter(y_test, y_pred, alpha=0.6, s=20, color="steelblue")
    lo = min(float(y_test.min()), float(y_pred.min()))
    hi = max(float(y_test.max()), float(y_pred.max()))
    ax.plot([lo, hi], [lo, hi], "r--", linewidth=1)
    ax.set_xlabel("実際の値")
    ax.set_ylabel("予測値")
    ax.set_title(title, fontsize=10)
    fig.tight_layout()
    return fig


def plot_correlation_matrix(df: pd.DataFrame, cols: list):
    corr = df[cols].corr()
    size = max(6, len(cols))
    fig, ax = plt.subplots(figsize=(size, size - 1))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0,
                square=True, ax=ax, annot_kws={"size": 8})
    ax.set_title("相関行列", fontsize=12)
    fig.tight_layout()
    return fig


# ── UI ────────────────────────────────────────────────────────────────────────

st.title("機械学習モデル作成アプリ")
st.caption("Excel ファイルをアップロードするだけで、複数の機械学習モデルを比較・評価できます。")

uploaded_file = st.file_uploader("Excel ファイルをアップロード (.xlsx / .xls)", type=["xlsx", "xls"])

if not uploaded_file:
    st.info("まず Excel ファイルをアップロードしてください。")
    st.stop()

df = load_excel(uploaded_file)

st.subheader("データプレビュー")
st.dataframe(df.head(10), use_container_width=True)
st.caption(f"行数: {len(df):,}　列数: {len(df.columns)}")

numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
if len(numeric_cols) < 2:
    st.error("数値列が 2 列以上必要です。")
    st.stop()

st.subheader("変数の設定")
col_left, col_right = st.columns(2)

with col_left:
    target_col = st.selectbox("被説明変数（目的変数）", numeric_cols)

with col_right:
    default_features = [c for c in numeric_cols if c != target_col]
    feature_cols = st.multiselect(
        "説明変数（特徴量）",
        options=default_features,
        default=default_features,
    )

st.subheader("アルゴリズムと学習設定")
col_algo, col_split = st.columns([3, 1])

with col_algo:
    selected_algos = st.multiselect(
        "使用するアルゴリズム",
        options=list(ALGORITHMS.keys()),
        default=["線形回帰", "ランダムフォレスト", "勾配ブースティング"],
    )

with col_split:
    test_size = st.slider("テストデータ割合", min_value=0.1, max_value=0.4,
                          value=0.2, step=0.05, format="%.0f%%",
                          help="全データのうちモデル評価に使う割合")

run = st.button("モデルを作成・評価", type="primary",
                disabled=not (feature_cols and selected_algos))

if not run:
    st.stop()

# ── Training ──────────────────────────────────────────────────────────────────

data = df[feature_cols + [target_col]].dropna()
if len(data) < 10:
    st.error("欠損除去後のデータが少なすぎます（10 行以上必要）。")
    st.stop()

X = data[feature_cols]
y = data[target_col]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=test_size, random_state=42
)

results = []
predictions: dict[str, np.ndarray] = {}

progress = st.progress(0, text="学習中...")
for i, name in enumerate(selected_algos):
    progress.progress((i + 1) / len(selected_algos), text=f"{name} を学習中...")
    model = ALGORITHMS[name]()
    metrics, y_pred = evaluate_model(
        model, X_train, X_test, y_train, y_test,
        scaled=(name == SVR_NAME),
    )
    results.append({"アルゴリズム": name, **metrics})
    predictions[name] = y_pred

progress.empty()

# ── Results ───────────────────────────────────────────────────────────────────

st.subheader("モデルスコア比較")
results_df = pd.DataFrame(results).sort_values("R²", ascending=False).reset_index(drop=True)
best = results_df.iloc[0]
st.success(f"最良モデル: **{best['アルゴリズム']}**　R² = {best['R²']}")

def highlight_best(s):
    return ["background-color: #d4edda" if i == 0 else "" for i in range(len(s))]

st.dataframe(
    results_df.style.apply(highlight_best, axis=0),
    use_container_width=True,
    hide_index=True,
)

# ── Predicted vs Actual ───────────────────────────────────────────────────────

st.subheader("予測値 vs 実際の値")
n_cols = min(len(selected_algos), 3)
cols = st.columns(n_cols)
for i, name in enumerate(selected_algos):
    with cols[i % n_cols]:
        fig = plot_pred_vs_actual(y_test.values, predictions[name], name)
        st.pyplot(fig)
        plt.close(fig)

# ── Correlation Matrix ────────────────────────────────────────────────────────

st.subheader("相関行列")
fig = plot_correlation_matrix(data, feature_cols + [target_col])
st.pyplot(fig)
plt.close(fig)
