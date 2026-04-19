import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

def train_models(df):
    feature_cols = ["SNR_dB", "Distance_km", "TX_Power_mW", "Frequency_GHz"]
    X = df[feature_cols].values
    y = df["BER"].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # --- Linear Regression via Normal Equation (manual, NumPy) ---
    X_b = np.hstack([np.ones((X_train.shape[0], 1)), X_train])
    theta = np.linalg.pinv(X_b.T @ X_b) @ X_b.T @ y_train

    X_test_b = np.hstack([np.ones((X_test.shape[0], 1)), X_test])
    y_pred_manual = X_test_b @ theta
    r2_manual = r2_score(y_test, y_pred_manual)
    mse_manual = mean_squared_error(y_test, y_pred_manual)

    # --- Sklearn Linear Regression ---
    lr = LinearRegression()
    lr.fit(X_train, y_train)
    y_pred_lr = lr.predict(X_test)
    r2_lr = r2_score(y_test, y_pred_lr)
    mse_lr = mean_squared_error(y_test, y_pred_lr)

    # --- Polynomial Regression (degree 2) ---
    poly = PolynomialFeatures(degree=2, include_bias=False)
    X_poly_train = poly.fit_transform(X_train)
    X_poly_test = poly.transform(X_test)
    pr = LinearRegression()
    pr.fit(X_poly_train, y_train)
    y_pred_poly = pr.predict(X_poly_test)
    r2_poly = r2_score(y_test, y_pred_poly)
    mse_poly = mean_squared_error(y_test, y_pred_poly)

    return {
        "feature_cols": feature_cols,
        "X_test": X_test,
        "y_test": y_test,
        "manual": {
            "theta": theta,
            "y_pred": y_pred_manual,
            "r2": r2_manual,
            "mse": mse_manual,
        },
        "linear": {
            "model": lr,
            "y_pred": y_pred_lr,
            "r2": r2_lr,
            "mse": mse_lr,
            "coef": lr.coef_,
            "intercept": lr.intercept_,
        },
        "poly": {
            "model": pr,
            "poly": poly,
            "y_pred": y_pred_poly,
            "r2": r2_poly,
            "mse": mse_poly,
        },
    }

def predict(results, snr, distance, tx_power, frequency):
    x = np.array([[snr, distance, tx_power, frequency]])

    # Manual (normal equation)
    x_b = np.hstack([np.ones((1, 1)), x])
    ber_manual = float((x_b @ results["manual"]["theta"]).item())

    # Sklearn linear
    ber_lr = float(results["linear"]["model"].predict(x)[0])

    # Polynomial
    x_poly = results["poly"]["poly"].transform(x)
    ber_poly = float(results["poly"]["model"].predict(x_poly)[0])

    return {
        "manual": max(ber_manual, 0),
        "linear": max(ber_lr, 0),
        "poly": max(ber_poly, 0),
    }
