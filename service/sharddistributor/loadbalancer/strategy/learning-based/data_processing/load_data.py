import pandas as pd
from pathlib import Path


def load_data(data_dir: str) -> pd.DataFrame:
    files = sorted(Path(data_dir).glob("*.csv"))

    frames = []

    for file in files:
        df = pd.read_csv(file, header=None)

        # First column is timestamp
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