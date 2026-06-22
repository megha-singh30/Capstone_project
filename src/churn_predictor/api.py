from fastapi import FastAPI
from pydantic import BaseModel
import joblib, pandas as pd
from pathlib import Path
from churn_predictor.data import preprocess 


app = FastAPI()
model = joblib.load(Path("models/model.joblib"))   # load ONCE at startup

class Customer(BaseModel):
    customerID : str
    gender: str
    SeniorCitizen: int
    Partner: str
    Dependents: str
    tenure: int
    PhoneService: str
    MultipleLines: str
    InternetService: str
    OnlineSecurity: str
    OnlineBackup: str
    DeviceProtection: str
    TechSupport: str
    StreamingTV: str
    StreamingMovies: str
    Contract: str
    PaperlessBilling: str
    PaymentMethod: str
    MonthlyCharges: float
    TotalCharges: float


@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(c: Customer):
    df = pd.DataFrame([c.dict()])
    df = preprocess(df) 
    df = df.reindex(columns=model.feature_names_in_, fill_value=0)  # force exact column match
    proba = model.predict_proba(df)[0][1]
    return {"churn_probability": round(float(proba), 4)} # if your pipeline has a fit_transform, apply it here
    
 