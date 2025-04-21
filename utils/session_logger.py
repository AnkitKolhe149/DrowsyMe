import os
import pandas as pd
from datetime import datetime

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

def log_metrics(user_id: str, ear: float):
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")

    filename = f"{user_id}_{date_str}.csv"
    filepath = os.path.join(DATA_DIR, filename)

    entry = pd.DataFrame([[time_str, ear]], columns=["timestamp", "ear"])

    if os.path.exists(filepath):
        entry.to_csv(filepath, mode='a', header=False, index=False)
    else:
        entry.to_csv(filepath, index=False)
