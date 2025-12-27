import pandas as pd
from fastapi import FastAPI, HTTPException
import os

app = FastAPI(title="Sovereign Intelligence API")

# --- THE FIX: ROBUST FILE PATH ---
# This gets the directory where THIS script (main_api.py) is located
base_dir = os.path.dirname(os.path.abspath(__file__))

# Option A: If CSV is inside the 'app' folder with the script (RECOMMENDED)
file_path = os.path.join(base_dir, "Sovereign_Intelligence_Hub.csv")

# Option B: If CSV is in the 'data' folder (one level up)
# file_path = os.path.join(base_dir, "..", "data", "Sovereign_Intelligence_Hub.csv")

try:
    df = pd.read_csv(file_path)
    print(f"✅ Loaded Data from: {file_path}")
except FileNotFoundError:
    # Fallback for debugging log
    print(f"❌ ERROR: Could not find file at {file_path}")
    print(f"   Current Directory: {os.getcwd()}")
    print(f"   Directory Contents: {os.listdir(base_dir)}")
    # Create empty DF so server doesn't crash immediately, but returns error on request
    df = pd.DataFrame()

@app.get("/")
def home():
    if df.empty:
        return {"status": "error", "message": "Data file not loaded."}
    return {"status": "online", "assets_tracked": len(df)}

@app.get("/api/v1/lookup/{brand}")
def lookup(brand: str):
    if df.empty: return {"error": "Database offline"}
    match = df[df['Brand'].str.contains(brand, case=False, na=False)]
    if match.empty: return {"error": "Brand not found"}
    return match.iloc[0].to_dict()