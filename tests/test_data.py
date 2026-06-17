import pandas as pd
from churn_predictor.data import preprocess, load_raw, split_features_target

CSV_PATH = "artifacts/telco_data.csv" 

def test_load_returns_dataframe_with_churn():
    df = load_raw(CSV_PATH)
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0
    assert "Churn" in df.columns

def test_preprocess_makes_totalcharges_numeric():
    df = preprocess(load_raw(CSV_PATH))

    assert pd.api.types.is_numeric_dtype(df["TotalCharges"])

def test_split_separates_features_and_target():
    df = preprocess(load_raw(CSV_PATH))
    Xtrain, y = split_features_target(df)

    assert len(Xtrain) == len(y) == len(df)        # X and y cover all rows
    assert "Churn" not in Xtrain.columns            # target pulled out of the features
    assert Xtrain.shape[1] == df.shape[1] - 1  # no columns lost except the target