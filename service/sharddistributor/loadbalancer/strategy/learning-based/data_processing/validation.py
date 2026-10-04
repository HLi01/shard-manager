def validate_data(data):
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

    