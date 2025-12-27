
import pandas as pd
from fastapi import FastAPI, HTTPException
import uvicorn

app = FastAPI(title="Sovereign Intelligence API")
df = pd.read_csv("Sovereign_Intelligence_Hub.csv")

@app.get("/api/v1/lookup/{brand}")
def lookup(brand: str):
    match = df[df['Brand'].str.contains(brand, case=False, na=False)]
    if match.empty: return {"error": "Brand not found"}
    return match.iloc[0].to_dict()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
