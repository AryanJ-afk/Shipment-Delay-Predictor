import pandas as pd

def clean_csv(
    input_path: str,
    output_path: str,
    numeric_cols: list = None,
    categorical_cols: list = None,
    target_col: str = None,
    reorder_target_first: bool = True
):
    """
    General CSV cleaner to prepare any CSV for Athena/SageMaker.

    Parameters:
    - input_path: path to input CSV
    - output_path: path to save cleaned CSV
    - numeric_cols: list of columns to convert to numeric
    - categorical_cols: list of columns to strip whitespace
    - target_col: name of the target column (optional)
    - reorder_target_first: whether to move target column as first column
    """

    df = pd.read_csv(input_path)

    # Strip column names
    df.columns = df.columns.str.strip()

    # Convert numeric columns
    if numeric_cols:
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

    # Strip categorical columns
    if categorical_cols:
        for col in categorical_cols:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip()

    # Reorder target column to first
    if target_col and target_col in df.columns and reorder_target_first:
        cols = [target_col] + [c for c in df.columns if c != target_col]
        df = df[cols]

    # Save cleaned CSV
    df.to_csv(output_path, index=False)
    print(f"Cleaned CSV saved to {output_path}")
