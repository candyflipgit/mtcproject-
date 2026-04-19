import numpy as np
import pandas as pd

def generate_data(n_samples=200, seed=42):
    np.random.seed(seed)

    snr_db = np.random.uniform(0, 30, n_samples)           # Signal-to-Noise Ratio (dB)
    distance = np.random.uniform(0.1, 10, n_samples)        # Distance (km)
    tx_power = np.random.uniform(10, 100, n_samples)        # Transmit Power (mW)
    frequency = np.random.uniform(0.9, 5.8, n_samples)     # Frequency (GHz)

    # BER formula inspired by real comms: higher SNR → lower BER, higher distance/freq → higher BER
    ber = (
        0.5 * np.exp(-0.3 * snr_db)
        + 0.05 * (distance / 10)
        - 0.002 * (tx_power / 100)
        + 0.01 * (frequency / 5.8)
        + np.random.normal(0, 0.005, n_samples)
    )
    ber = np.clip(ber, 1e-5, 0.5)

    df = pd.DataFrame({
        "SNR_dB": snr_db,
        "Distance_km": distance,
        "TX_Power_mW": tx_power,
        "Frequency_GHz": frequency,
        "BER": ber
    })
    return df
