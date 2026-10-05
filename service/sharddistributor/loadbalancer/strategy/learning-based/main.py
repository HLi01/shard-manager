from data_processing.load_data import load_data, validate_data, smooth_load
from data_processing.statistics import statistics
from pathlib import Path


def main():
    data_dir = Path(__file__).resolve().parent / "load_data"
    data = load_data(str(data_dir))
    data = validate_data(data)
    print("Data validation completed successfully.")

    stats = statistics(data)

    print(stats["summary"])
    print(stats["load_distribution"])
    print(stats["largest_spikes"])

    smoothed_data = smooth_load(data,tau=30.0,)
    print("Raw data:\n", data.head())
    print("Smoothed data:\n", smoothed_data.head())


if __name__ == "__main__":
    main()
