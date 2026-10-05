import pandas as pd
import numpy as np
from pathlib import Path



def load_data(data_dir: str) -> pd.DataFrame:
    files = sorted(Path(data_dir).glob("*.csv"))

    frames = []

    for file in files:
        df = pd.read_csv(file, header=None)
        df = df.rename(columns={0: "timestamp"})
        # use DD-MM-YYYY HH:MM:SS format for timestamp parsing
        df["timestamp"] = pd.to_datetime(
            df["timestamp"],
            format="%d-%m-%Y %H:%M:%S"
        )

        frames.append(df)

    # Combine all chunks and the full-day file
    data = pd.concat(frames, ignore_index=True)

    # Sort chronologically
    data = data.sort_values("timestamp")

    # Remove overlapping measurements.
    # If the same timestamp occurs in multiple files, keep the first one.
    data = data.drop_duplicates(subset="timestamp", keep="first")

    # Restore a clean sequential index
    data = data.reset_index(drop=True)

    return data

def validate_data(data: pd.DataFrame) -> pd.DataFrame:
    print("Rows:", len(data))
    print("Columns:", len(data.columns))
    print("Start:", data["timestamp"].min())
    print("End:", data["timestamp"].max())

    timestamps = data["timestamp"]
    intervals = timestamps.diff().dropna()

    print("Sampling intervals:")
    print(intervals.value_counts().head())

    loads = data.iloc[:, 1:]

    print("Number of shards:", loads.shape[1])
    print("Missing values:", loads.isna().sum().sum())
    print("Non-zero measurements:", (loads > 0).sum().sum())
    print("Zero measurements:", (loads == 0).sum().sum())
    return data

def smooth_load(data: pd.DataFrame, tau: float = 30.0,) -> pd.DataFrame:
    data = data.sort_values("timestamp").reset_index(drop=True)

    shard_columns = [column for column in data.columns if column != "timestamp"]

    raw_load = data[shard_columns].to_numpy(dtype=float)
    timestamps = data["timestamp"].to_numpy()

    smoothed_load = np.empty_like(raw_load)

    # Initial state
    smoothed_load[0] = raw_load[0]

    for t in range(1, len(data)):
        delta_t = (timestamps[t] - timestamps[t - 1]) / np.timedelta64(1, "s")
        alpha = 1.0 - np.exp(-delta_t / tau)

        smoothed_load[t] = alpha * raw_load[t] + (1.0 - alpha) * smoothed_load[t - 1]

    result = data.copy()
    result[shard_columns] = smoothed_load

    return result