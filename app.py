import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")

from data_generator import generate_data
from model import train_models, predict
from speedtest_component import get_speedtest_html

st.set_page_config(page_title="Mini ML Model – MTC Project 10", layout="wide")

# ── Pre-compute model once ─────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    df = generate_data()
    results = train_models(df)
    return df, results

df, results = load_model()
coef = results['linear']['model'].coef_.tolist()
intercept = float(results['linear']['model'].intercept_)

# ── Header ─────────────────────────────────────────────────────────────────────
st.title("Mini ML Model using Linear Algebra & Statistics")
st.caption("Project 10 · Mathematical Theory of Communication · Assignment 10")

tab_speed, tab_data, tab_math, tab_results, tab_predict = st.tabs([
    "Speed Test", "Dataset", "Math & Models", "Model Results", "Manual Predictor"
])

# ── Tab: Speed Test ────────────────────────────────────────────────────────────
with tab_speed:
    st.subheader("Live Network Speed Test")
    st.markdown("""
Runs entirely in your **browser** — measures your device's actual download speed, upload speed, and ping
using Cloudflare's speed endpoints. Results are fed into the **ML regression model** to estimate
channel quality metrics (SNR, BER, TX Power).
""")
    components.html(get_speedtest_html(coef, intercept), height=780, scrolling=False)

# ── Tab: Dataset ───────────────────────────────────────────────────────────────
with tab_data:
    st.subheader("Synthetic Communication Channel Dataset")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Samples", len(df))
    col2.metric("Features", 4)
    col3.metric("Avg SNR", f"{df.SNR_dB.mean():.1f} dB")
    col4.metric("Avg BER", f"{df.BER.mean():.4f}")

    st.dataframe(df.head(20).style.format("{:.4f}"), use_container_width=True)

    st.subheader("Feature Distributions")
    fig, axes = plt.subplots(1, 4, figsize=(14, 3))
    for ax, col in zip(axes, ["SNR_dB", "Distance_km", "TX_Power_mW", "Frequency_GHz"]):
        ax.hist(df[col], bins=25, color="#4F8EF7", edgecolor="white")
        ax.set_title(col)
        ax.set_ylabel("Count")
    fig.tight_layout()
    st.pyplot(fig)
    plt.close()

    st.subheader("BER vs SNR")
    fig2, ax2 = plt.subplots(figsize=(8, 3))
    sc = ax2.scatter(df["SNR_dB"], df["BER"], c=df["Distance_km"],
                     cmap="plasma", alpha=0.6, s=20)
    plt.colorbar(sc, ax=ax2, label="Distance (km)")
    ax2.set_xlabel("SNR (dB)")
    ax2.set_ylabel("BER")
    ax2.set_title("BER vs SNR (colour = distance)")
    fig2.tight_layout()
    st.pyplot(fig2)
    plt.close()

# ── Tab: Math & Models ─────────────────────────────────────────────────────────
with tab_math:
    st.subheader("Linear Regression via Normal Equation")
    st.markdown(r"""
The model fits: $\hat{y} = X\theta$

where $X$ is the feature matrix (with a bias column of 1s) and $\theta$ is the weight vector.

**Closed-form solution (Normal Equation):**
$$\theta = (X^T X)^{-1} X^T y$$

This uses:
- **Matrix transpose** $X^T$
- **Matrix multiplication** $X^T X$
- **Matrix inversion** $(X^T X)^{-1}$

All implemented with `numpy.linalg.pinv` for numerical stability.
""")

    theta = results["manual"]["theta"]
    feature_cols = results["feature_cols"]
    coef_df = pd.DataFrame({
        "Feature": ["Bias"] + feature_cols,
        "θ value": theta
    })
    st.dataframe(coef_df.style.format({"θ value": "{:.6f}"}), use_container_width=True)

    st.subheader("Polynomial Regression (Degree 2)")
    st.markdown(r"""
Extends linear regression by adding squared and cross-product terms:
$$\hat{y} = \theta_0 + \theta_1 x_1 + \theta_2 x_2 + \theta_3 x_1^2 + \theta_4 x_1 x_2 + \dots$$

Captures **non-linear relationships** between features and BER using `PolynomialFeatures` from Scikit-learn.
""")

    st.subheader("Correlation Matrix")
    corr = df.corr()
    fig3, ax3 = plt.subplots(figsize=(5, 4))
    im = ax3.imshow(corr.values, cmap="coolwarm", vmin=-1, vmax=1)
    plt.colorbar(im, ax=ax3)
    ax3.set_xticks(range(len(corr)))
    ax3.set_yticks(range(len(corr)))
    ax3.set_xticklabels(corr.columns, rotation=45, ha="right", fontsize=8)
    ax3.set_yticklabels(corr.columns, fontsize=8)
    for i in range(len(corr)):
        for j in range(len(corr)):
            ax3.text(j, i, f"{corr.values[i, j]:.2f}",
                     ha="center", va="center", fontsize=7)
    ax3.set_title("Feature Correlation Matrix")
    fig3.tight_layout()
    st.pyplot(fig3)
    plt.close()

# ── Tab: Model Results ─────────────────────────────────────────────────────────
with tab_results:
    st.subheader("Model Performance Comparison")

    r2_m  = results["manual"]["r2"]
    r2_l  = results["linear"]["r2"]
    r2_p  = results["poly"]["r2"]
    mse_m = results["manual"]["mse"]
    mse_l = results["linear"]["mse"]
    mse_p = results["poly"]["mse"]

    perf_df = pd.DataFrame({
        "Model": ["Normal Equation (NumPy)", "Linear Regression (Sklearn)",
                  "Polynomial Regression (deg 2)"],
        "R² Score": [r2_m, r2_l, r2_p],
        "MSE":      [mse_m, mse_l, mse_p],
    })
    st.dataframe(perf_df.style.format({"R² Score": "{:.4f}", "MSE": "{:.6f}"}),
                 use_container_width=True)

    st.subheader("Actual vs Predicted BER")
    y_test = results["y_test"]
    fig4, axes = plt.subplots(1, 3, figsize=(14, 4))
    for ax, (name, y_pred, r2) in zip(axes, [
        ("Normal Equation",      results["manual"]["y_pred"], r2_m),
        ("Linear Regression",    results["linear"]["y_pred"], r2_l),
        ("Polynomial Regression",results["poly"]["y_pred"],   r2_p),
    ]):
        ax.scatter(y_test, y_pred, alpha=0.5, s=15, color="#4F8EF7")
        mn = min(y_test.min(), y_pred.min())
        mx = max(y_test.max(), y_pred.max())
        ax.plot([mn, mx], [mn, mx], "r--", linewidth=1)
        ax.set_xlabel("Actual BER")
        ax.set_ylabel("Predicted BER")
        ax.set_title(f"{name}\nR²={r2:.4f}")
    fig4.tight_layout()
    st.pyplot(fig4)
    plt.close()

    fig5, ax5 = plt.subplots(figsize=(6, 3))
    names = ["Normal Eq.", "Linear Reg.", "Poly Reg."]
    r2s   = [r2_m, r2_l, r2_p]
    bars  = ax5.bar(names, r2s, color=["#4F8EF7", "#F78C4F", "#4FD1A8"])
    for bar, val in zip(bars, r2s):
        ax5.text(bar.get_x() + bar.get_width() / 2,
                 bar.get_height() + 0.005, f"{val:.4f}", ha="center", fontsize=10)
    ax5.set_ylim(0, 1.1)
    ax5.set_ylabel("R² Score")
    ax5.set_title("Model Comparison")
    fig5.tight_layout()
    st.pyplot(fig5)
    plt.close()

# ── Tab: Manual Predictor ──────────────────────────────────────────────────────
with tab_predict:
    st.subheader("Manual BER Predictor")
    st.markdown("Adjust sliders to simulate a communication channel and get BER predictions.")

    col1, col2 = st.columns(2)
    with col1:
        snr      = st.slider("SNR (dB)",          0.0,  30.0,  15.0, 0.5)
        distance = st.slider("Distance (km)",      0.1,  10.0,   3.0, 0.1)
    with col2:
        tx_power  = st.slider("TX Power (mW)",    10.0, 100.0,  50.0, 1.0)
        frequency = st.slider("Frequency (GHz)",   0.9,   5.8,   2.4, 0.1)

    preds = predict(results, snr, distance, tx_power, frequency)

    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    c1.metric("Normal Equation BER",    f"{preds['manual']:.5f}")
    c2.metric("Linear Regression BER",  f"{preds['linear']:.5f}")
    c3.metric("Polynomial Reg. BER",    f"{preds['poly']:.5f}")

    quality = ("Excellent" if preds["linear"] < 0.01
               else "Good" if preds["linear"] < 0.05
               else "Poor")
    color = {"Excellent": "green", "Good": "orange", "Poor": "red"}[quality]
    st.markdown(f"**Channel Quality:** :{color}[{quality}]")
    st.info("""
**Interpretation:**
- BER < 0.01 → Excellent channel quality
- 0.01 ≤ BER < 0.05 → Acceptable quality
- BER ≥ 0.05 → Poor quality, retransmission likely needed
""")
