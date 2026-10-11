from pathlib import Path
import pandas as pd

DATA_DIR = Path(__file__).resolve().parent
EVENT_FILE = DATA_DIR / "patient_events.csv"


def print_event_log_summary(df: pd.DataFrame) -> None:
    """Print a helpful validation summary for an event log dataset."""
    print("\n--- Dataset Overview ---")
    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")
    print("\nColumn names:")
    print(df.columns.tolist())

    print("\n--- Missing Values ---")
    print(df.isnull().sum())

    print("\n--- Duplicate Rows ---")
    print(df.duplicated().sum())

    print("\n--- Data Types ---")
    print(df.dtypes)

    print("\n--- First Five Records ---")
    print(df.head().to_string(index=False))

    print("\n--- Missing Values ---")
    print(df.isnull().sum())

    print("\n--- Timestamp Validation ---")
    if "timestamp" in df.columns:
        df_for_validation = df.copy()
        df_for_validation["timestamp"] = pd.to_datetime(
            df_for_validation["timestamp"], errors="coerce"
        )
        invalid_timestamps = df_for_validation[df_for_validation["timestamp"].isna()]
        print(f"Invalid timestamps: {len(invalid_timestamps)}")
        if not invalid_timestamps.empty:
            columns_to_show = [col for col in ["case_id", "activity", "timestamp"] if col in invalid_timestamps.columns]
            if columns_to_show:
                print(invalid_timestamps[columns_to_show].head().to_string(index=False))
            else:
                print(invalid_timestamps.head().to_string(index=False))
    else:
        print("Missing 'timestamp' column; skipping timestamp validation.")

    print("\n--- Duplicate Events ---")
    required_columns = {"case_id", "activity", "timestamp"}
    if required_columns.issubset(df.columns):
        duplicate_events = df.duplicated(subset=["case_id", "activity", "timestamp"])
        print(f"Duplicate events: {duplicate_events.sum()}")
        sample_duplicates = df[duplicate_events]
        if not sample_duplicates.empty:
            print("\nSample duplicate events:")
            print(sample_duplicates.head().to_string(index=False))
    else:
        print(
            "Missing one or more required columns for duplicate-event check: "
            "case_id, activity, timestamp"
        )


def main() -> None:
    if not EVENT_FILE.exists():
        print(f"Dataset not found: {EVENT_FILE}")
        return

    df = pd.read_csv(EVENT_FILE)
    print_event_log_summary(df)


if __name__ == "__main__":
    main()