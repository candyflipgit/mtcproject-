import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error

FEATURES = [
    'avg_download_mbps',    # raw download speed
    'download_stability',   # 0-1, how steady the speed was
    'avg_ping_ms',          # idle ping
    'ping_jitter_ms',       # ping variation (std dev)
    'upload_mbps',          # upload speed
    'dl_ul_ratio',          # download / upload asymmetry
    'speed_trend',          # -1 to +1, was speed going up or down
    'device_memory_gb',     # RAM
    'cpu_cores',            # logical CPU cores
    'connection_type_score' # 0.3=cellular, 0.6=wifi2.4, 0.8=wifi5, 1.0=ethernet
]

def generate_network_data(n=1200, seed=42):
    np.random.seed(seed)

    # Bimodal download: 45% slow-mid (5–100 Mbps), 55% fast (80–500 Mbps)
    # Ensures the linear model is well-trained across the full real-world range
    slow_dl     = np.random.uniform(5, 100, n)
    fast_dl     = np.random.uniform(80, 500, n)
    avg_dl      = np.where(np.random.random(n) < 0.45, slow_dl, fast_dl)
    avg_dl      = np.clip(avg_dl, 1, 500)

    dl_std      = avg_dl * np.random.uniform(0.03, 0.40, n)
    dl_stab     = np.clip(1 - dl_std / avg_dl, 0.05, 0.99)

    # Bimodal ping: 55% fast (5–60ms), 45% slow (60–350ms) — covers real-world range
    fast_ping   = np.random.uniform(5, 60, n)
    slow_ping   = np.random.uniform(60, 350, n)
    avg_ping    = np.where(np.random.random(n) < 0.55, fast_ping, slow_ping)
    avg_ping    = np.clip(avg_ping, 2, 350)

    ping_jitter = np.clip(avg_ping * np.random.uniform(0.05, 0.4, n), 0.5, 80)

    # Upload can be very asymmetric (e.g., ADSL, mobile data) → ratio up to 20x
    asym_mask   = np.random.random(n) < 0.35          # 35% very asymmetric
    ul_asym     = np.random.uniform(0.05, 0.15, n)    # ADSL/mobile: 5–15% of download
    ul_norm     = np.random.uniform(0.15, 1.50, n)    # broadband to symmetric/upload-dominant fibre
    ul_ratio    = np.where(asym_mask, ul_asym, ul_norm)
    upload      = np.clip(avg_dl * ul_ratio, 0.3, 600)
    # ratio < 1 means upload > download (symmetric fibre); clip floor at 0.5
    dl_ul_ratio = np.clip(avg_dl / np.maximum(upload, 0.1), 0.5, 20)

    speed_trend = np.random.uniform(-1, 1, n)
    device_mem  = np.random.choice([1,2,4,8,16], n,
                                    p=[0.05,0.1,0.3,0.4,0.15]).astype(float)
    cpu_cores   = np.random.choice([2,4,6,8,12,16], n,
                                    p=[0.10,0.30,0.20,0.25,0.10,0.05]).astype(float)
    conn_score  = np.random.choice([0.3,0.6,0.8,1.0], n,
                                    p=[0.20,0.30,0.30,0.20])

    # Effective throughput: tuned so good connections hit 75–85% efficiency.
    # Each factor has a generous floor — no single parameter can collapse output.

    # Ping penalty: gentle curve; 30ms→0.928, 80ms→0.819, 200ms→0.607
    ping_factor   = np.exp(-avg_ping / 400)

    # Jitter penalty: minor — TCP SACK handles retransmits efficiently; max 8% drag
    jitter_factor = 1 - np.clip(ping_jitter / 1000, 0, 0.08)

    # Stability: floor at 75% — real-world connections rarely drop below this
    stab_factor   = 0.75 + 0.25 * dl_stab                               # range: 0.75–1.00

    # Device factor: narrow range — hardware rarely bottlenecks <1 Gbps
    device_factor = 0.91 + 0.09 * (device_mem / 16) * (np.log2(np.maximum(cpu_cores, 1)) / 4)

    # Connection type: overhead penalty; ethernet→1.0, wifi5→0.956, wifi2.4→0.929, cell→0.885
    conn_factor   = 0.855 + 0.145 * conn_score

    effective = (avg_dl * stab_factor * ping_factor * jitter_factor
                 * device_factor * conn_factor * (1 + speed_trend * 0.03))
    noise = np.random.normal(0, avg_dl * 0.012, n)
    effective = np.clip(effective + noise, 0.1, avg_dl * 0.98)

    return pd.DataFrame({
        'avg_download_mbps':     avg_dl,
        'download_stability':    dl_stab,
        'avg_ping_ms':           avg_ping,
        'ping_jitter_ms':        ping_jitter,
        'upload_mbps':           upload,
        'dl_ul_ratio':           dl_ul_ratio,
        'speed_trend':           speed_trend,
        'device_memory_gb':      device_mem,
        'cpu_cores':             cpu_cores,
        'connection_type_score': conn_score,
        'effective_throughput':  effective
    })


def train_throughput_model(df=None):
    if df is None:
        df = generate_network_data()

    X = df[FEATURES].values
    y = df['effective_throughput'].values
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)

    scaler = StandardScaler()
    X_tr_s = scaler.fit_transform(X_tr)
    X_te_s = scaler.transform(X_te)

    model = LinearRegression()
    model.fit(X_tr_s, y_tr)
    y_pred = model.predict(X_te_s)

    return {
        'model':        model,
        'scaler':       scaler,
        'r2':           r2_score(y_te, y_pred),
        'mse':          mean_squared_error(y_te, y_pred),
        'coef':         model.coef_.tolist(),
        'intercept':    float(model.intercept_),
        'scaler_mean':  scaler.mean_.tolist(),
        'scaler_std':   scaler.scale_.tolist(),
        'features':     FEATURES,
        'df':           df,
        'y_test':       y_te,
        'y_pred':       y_pred,
    }
