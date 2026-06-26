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
from xml.parsers.expat import model

import joblib
import mlflow
from pathlib import Path
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


import mlflow

def train(csv_path):
    df = data.load_raw(csv_path)
    df = data.preprocess(df)
    X, y = data.split_features_target(df)
    cat, num = data.get_feature_columns(X)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42)

    with mlflow.start_run():
        pipe = build_pipeline(cat, num)
        pipe.fit(X_train, y_train)
        auc = roc_auc_score(y_test, pipe.predict_proba(X_test)[:, 1])
        mlflow.log_metric("auc", auc)          # ← the one new line that matters
        print(classification_report(y_test, pipe.predict(X_test)))
    return pipe, auc


Path("models").mkdir(exist_ok=True)
def save(pipe: Pipeline, path: str = MODEL_PATH) -> None:
    """Persist the fitted pipeline. TODO: joblib.dump(pipe, path)."""   
    joblib.dump(pipe, "models/model.joblib")  # inside models/, which is mounted


if __name__ == "__main__":
    # TODO: pipe, auc = train("data/telco.csv"); print(f"AUC={auc:.3f}"); save(pipe)
    # This is what your Day-4 Dockerfile will run.
    pipe, auc = train("artifacts/telco_data.csv")
    print(f"AUC={auc:.3f}")
    save(pipe)