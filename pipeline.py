import pandas as pd
import sqlite3

# STEP 1: Load data
df = pd.read_csv("user_activity.csv")

# STEP 2: Cleaning
df["timestamp"] = pd.to_datetime(df["timestamp"])

# STEP 3: Feature Engineering
df["hour"] = df["timestamp"].dt.hour
df["date"] = df["timestamp"].dt.date

df["is_productive"] = df["activity"].apply(
    lambda x: 1 if x in ["Work", "Study"] else 0
)

df["is_distraction"] = df["activity"].apply(
    lambda x: 1 if x in ["Social", "Entertainment"] else 0
)

def categorize_time(hour):
    if 6 <= hour < 12:
        return "Morning"
    elif 12 <= hour < 18:
        return "Afternoon"
    elif 18 <= hour < 24:
        return "Evening"
    else:
        return "Night"

df["time_period"] = df["hour"].apply(categorize_time)

# STEP 4: Save cleaned CSV
df.to_csv("cleaned_user_activity.csv", index=False)

# STEP 5: Load into SQL
conn = sqlite3.connect("user_activity.db")
df.to_sql("user_activity", conn, if_exists="replace", index=False)

print("Pipeline executed successfully!")