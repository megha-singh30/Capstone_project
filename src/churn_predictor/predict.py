"""Load the trained pipeline and make predictions on new customer records.

This is the module your FastAPI app (Day 5) will import. Keep it dumb: load
the artifact once, expose a predict function that takes a dict/DataFrame and
returns churn probability. No cleaning logic here that isn't already baked into
the saved pipeline — if you find yourself re-cleaning here, it belongs in
data.py and inside the pipeline instead.
"""

from __future__ import annotations

import joblib
import pandas as pd

from churn_predictor.train import MODEL_PATH


def load_model(path: str = MODEL_PATH):
    """Load the saved pipeline from disk.

    TODO: return joblib.load(path)

    Later (Day 9) this changes to load from the MLflow registry instead of a
    local file — leave a comment to your future self here.
    """
    raise NotImplementedError


def predict_one(model, record: dict) -> float:
    """Predict churn probability for a single customer.

    `record` is a dict of feature_name -> value, e.g. the JSON body your API
    receives. The saved pipeline handles encoding, so just shape it into a
    one-row DataFrame.

    TODO:
      - df = pd.DataFrame([record])
      - proba = model.predict_proba(df)[0, 1]
      - return float(proba)

    Gotcha: the incoming record must have the SAME columns the pipeline was
    trained on (minus customerID and Churn). Decide now how you'll validate
    that — Pydantic on Day 5 is the clean answer.
    """
    raise NotImplementedError


if __name__ == "__main__":
    # Quick manual smoke test once train.py works:
    # m = load_model()
    # sample = {... one customer's fields ...}
    # print(predict_one(m, sample))
    pass
