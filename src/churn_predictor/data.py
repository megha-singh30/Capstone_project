"""Data loading and preprocessing for the Telco churn dataset.

This module owns everything between the raw CSV and a model-ready feature
matrix. Keep ALL cleaning logic here so train.py and predict.py apply the
exact same transforms — a mismatch between training and serving preprocessing
is the #1 cause of "works in notebook, broken in production" bugs.

Dataset: IBM Telco Customer Churn (Kaggle).
Shape: ~7043 rows, 21 columns. Target column: "Churn" (Yes/No).
"""

from __future__ import annotations

import pandas as pd

# Columns that are NOT features. customerID is an identifier (leaks nothing
# useful, would just be memorized). Churn is the target.
ID_COL = "customerID"
TARGET_COL = "Churn"


def load_raw(csv_path: str) -> pd.DataFrame:
    """Read the raw Telco CSV into a DataFrame.

    TODO:
      - pd.read_csv(csv_path)
      - return the DataFrame unchanged (do NO cleaning here — keep load and
        clean separate so you can inspect the raw mess if a bug shows up)
    """
    raise NotImplementedError


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Apply the Telco-specific cleaning steps. Returns a cleaned copy.

    The Telco dataset has THREE specific traps. Handle each:

    1. TotalCharges is stored as TEXT, not numbers. ~11 rows contain a single
       space " " instead of a value (these are customers with tenure == 0, i.e.
       brand new, never billed). If you naively cast to float it explodes.
       TODO:
         - pd.to_numeric(df["TotalCharges"], errors="coerce")  -> blanks become NaN
         - fill those NaN with 0 (a tenure-0 customer has paid 0 total)

    2. SeniorCitizen is already 0/1 int while every other yes/no column is the
       strings "Yes"/"No". Leave it as-is, just be aware so it doesn't get
       double-encoded later.

    3. customerID must be dropped before modelling (identifier, not a feature).
       TODO: drop ID_COL.

    Work on a copy (df = df.copy()) so you never mutate the caller's frame.
    Return the cleaned DataFrame (target column still included).
    """
    raise NotImplementedError


def split_features_target(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """Separate X (features) and y (target).

    TODO:
      - y = df[TARGET_COL] mapped to 1/0  ("Yes" -> 1, "No" -> 0)
      - X = df without TARGET_COL
      - return (X, y)
    """
    raise NotImplementedError


def get_feature_columns(X: pd.DataFrame) -> tuple[list[str], list[str]]:
    """Return (categorical_cols, numeric_cols) for building the encoder.

    Numeric in Telco: tenure, MonthlyCharges, TotalCharges (and SeniorCitizen,
    which is already 0/1 — your call whether to treat it as numeric).
    Everything else is categorical (object dtype).

    TODO:
      - numeric_cols  = columns where X[col].dtype is numeric
      - categorical_cols = the rest
      - return (categorical_cols, numeric_cols)

    Hint: X.select_dtypes(include="number").columns and include="object".
    """
    raise NotImplementedError
