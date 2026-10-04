from data_processing.validation import validate_data
from data_processing.load_data import load_data
from pathlib import Path


def main():
    data_dir = Path(__file__).resolve().parent / "load_data"
    data = load_data(str(data_dir))
    data = validate_data(data)
    print("Data validation completed successfully.")


if __name__ == "__main__":
    main()
