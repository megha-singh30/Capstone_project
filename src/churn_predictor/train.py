"""Train the churn model and save it as a single artifact.

ALGORITHM CHOICE (be able to defend this in an interview):
  Start with LogisticRegression as a BASELINE. It's fast, interpretable, and
  gives you a number to beat. Then try a tree model (RandomForest or, better,
  XGBoost). On Telco, a tuned tree model usually lands ~0.84 ROC-AUC vs ~0.84
  for logistic too — the point is you can SAY "I baselined with logistic
  regression, compared against XGBoost, and chose X because Y", which is the
  real interview answer. Don't chase accuracy past ~80%; the model is the seed,
  not the project.

KEY DESIGN RULE: wrap preprocessing + model in ONE sklearn Pipeline and save
that whole pipeline. Then predict.py just calls pipeline.predict() and the
encoding happens automatically — no chance of train/serve skew.

CLASS IMBALANCE: churn is ~26% positive. Note this in your remarks. Easiest
lever: class_weight="balanced" (logistic/RF) or scale_pos_weight (XGBoost).
Mention you considered it — interviewers probe imbalance handling.
"""

from __future__ import annotations

import joblib
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.metrics import roc_auc_score, classification_report

from churn_predictor import data

MODEL_PATH = "model.joblib"


def build_pipeline(categorical_cols: list[str], numeric_cols: list[str]) -> Pipeline:
    """Build the preprocessing + model pipeline.

    TODO:
      - preprocessor = ColumnTransformer([
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols),
            ("num", StandardScaler(), numeric_cols),
        ])
        (handle_unknown="ignore" matters: at serve time a category you never
         saw in training shouldn't crash the request.)
      - model = LogisticRegression(max_iter=1000, class_weight="balanced")
        # swap for your tree model once the baseline works
      - return Pipeline([("prep", preprocessor), ("model", model)])
    """
    preprocessor = ColumnTransformer([
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols),
        ("num", StandardScaler(), numeric_cols),    
    ])
    model = LogisticRegression(max_iter=1000, class_weight="balanced")
    return Pipeline([("prep", preprocessor), ("model", model)]) 


def train(csv_path: str) -> tuple[Pipeline, float]:
    """Full training run: load -> clean -> split -> fit -> evaluate -> return.

    TODO (wire the functions from data.py together):
      1. df = data.load_raw(csv_path)
      2. df = data.clean(df)
      3. X, y = data.split_features_target(df)
      4. cat, num = data.get_feature_columns(X)
      5. X_train, X_test, y_train, y_test = train_test_split(
             X, y, test_size=0.2, stratify=y, random_state=42)
         (stratify=y keeps the 26% churn ratio in both splits — important with
          imbalance.)
      6. pipe = build_pipeline(cat, num); pipe.fit(X_train, y_train)
      7. proba = pipe.predict_proba(X_test)[:, 1]
         auc = roc_auc_score(y_test, proba)
      8. print(classification_report(y_test, pipe.predict(X_test)))
      9. return pipe, auc
    """
    df = data.load_raw(csv_path)
    df = data.clean(df)
    X, y = data.split_features_target(df)
    cat, num = data.get_feature_columns(X)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42)
    pipe = build_pipeline(cat, num)
    pipe.fit(X_train, y_train)
    proba = pipe.predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, proba)
    print(classification_report(y_test, pipe.predict(X_test)))
    return pipe, auc

def save(pipe: Pipeline, path: str = MODEL_PATH) -> None:
    """Persist the fitted pipeline. TODO: joblib.dump(pipe, path)."""
    joblib.dump(pipe, path)


if __name__ == "__main__":
    # TODO: pipe, auc = train("data/telco.csv"); print(f"AUC={auc:.3f}"); save(pipe)
    # This is what your Day-4 Dockerfile will run.
    pipe, auc = train("artifacts/telco_data.csv")
    print(f"AUC={auc:.3f}")
    save(pipe)