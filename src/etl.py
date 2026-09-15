import json
import glob
import sqlite3
from datetime import datetime

def load_summarized_activities(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        activities = data[0]["summarizedActivitiesExport"]
        print(f"Loaded {len(activities)} summarized activities from JSON file.")
    return activities

def load_all_activities(folder_path):
    files = glob.glob(f"{folder_path}/*_summarizedActivities.json")
    data = []
    
    for (file_path) in files:
        data.extend(load_summarized_activities(file_path))
        
    return data
        
    
all_activities = load_all_activities("data\\raw")
print(f"Total activities: {len(all_activities)}")

def create_db(db_path):
    conn = sqlite3.connect(db_path)
    
    conn.execute('''CREATE TABLE IF NOT EXISTS activities (
        id INTEGER PRIMARY KEY,
        name TEXT,
        type TEXT,
        start_time TEXT,
        duration_sec REAL,
        distance_km REAL,
        avg_speed REAL,
        max_speed REAL,
        avg_hr REAL,
        max_hr REAL,
        training_load REAL,
        hr_zone_0 REAL,
        hr_zone_1 REAL,
        hr_zone_2 REAL,
        hr_zone_3 REAL,
        hr_zone_4 REAL,
        hr_zone_5 REAL,
        hr_zone_6 REAL
        )''')
    conn.commit()
    
    return conn

conn = create_db("data\\processed\\activities.db")

def prepare_activity_row(activity):
    start_time = datetime.fromtimestamp(activity["startTimeGmt"] / 1000).isoformat()
    distance = activity.get("distance", 0) / 100000
    duration = activity.get("duration", 0) / 1000

    return (
        activity["activityId"],
        activity["name"],
        activity["activityType"],
        start_time,
        duration,
        distance,
        activity.get("avgSpeed"),
        activity.get("maxSpeed"),
        activity.get("avgHr"),
        activity.get("maxHr"),
        activity.get("activityTrainingLoad"),
        activity.get("hrTimeInZone_0"),
        activity.get("hrTimeInZone_1"),
        activity.get("hrTimeInZone_2"),
        activity.get("hrTimeInZone_3"),
        activity.get("hrTimeInZone_4"),
        activity.get("hrTimeInZone_5"),
        activity.get("hrTimeInZone_6"),
    )


def insert_all_activities(conn, activities):
    rows = [prepare_activity_row(a) for a in activities]

    conn.executemany('''
        INSERT OR REPLACE INTO activities
        (id, name, type, start_time, duration_sec, distance_km,
         avg_speed, max_speed, avg_hr, max_hr, training_load,
         hr_zone_0, hr_zone_1, hr_zone_2, hr_zone_3, hr_zone_4, hr_zone_5, hr_zone_6)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', rows)

    conn.commit()
    print(f"Inserted {len(rows)} activities.")


insert_all_activities(conn, all_activities)