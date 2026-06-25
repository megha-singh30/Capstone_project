from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import joblib, pandas as pd
from pathlib import Path
from churn_predictor.data import preprocess 


app = FastAPI()
pipeline = joblib.load(Path("models/model.joblib"))   # load ONCE at startup

class Customer(BaseModel):
    customerID : str
    gender: str
    SeniorCitizen: int
    Partner: str
    Dependents: str
    tenure: int = Field(ge=0, le=100)
    PhoneService: str
    MultipleLines: str
    InternetService: str
    OnlineSecurity: str
    OnlineBackup: str
    DeviceProtection: str
    TechSupport: str
    StreamingTV: str
    StreamingMovies: str
    Contract: str =Field(pattern="^(Month-to-month|One year|Two year)$")
    PaperlessBilling: str
    PaymentMethod: str
    MonthlyCharges: float = Field(ge=0)
    TotalCharges: float = Field(ge=0)


@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(c: Customer):
    try:
        df = pd.DataFrame([c.model_dump()])
        # df = preprocess(df) 
        # df = df.reindex(columns=pipeline.feature_names_in_, fill_value=0)  # force exact column match
        proba = pipeline.predict_proba(df)[0][1]
        return {"churn_probability": round(float(proba), 4)} # if your pipeline has a fit_transform, apply it here
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
 