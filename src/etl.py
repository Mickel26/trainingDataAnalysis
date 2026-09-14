import json
import glob
import sqlite3

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
        type TEXT
        )''')
    conn.commit()
    
    return conn

conn = create_db("data\\processed\\activities.db")

def insert_activity(conn, activity):
    conn.execute('''INSERT INTO activities (id, name, type) VALUES (?, ?, ?)''', (activity["activityId"], activity["name"], activity["activityType"]))
    conn.commit()
    
insert_activity(conn, all_activities[0])