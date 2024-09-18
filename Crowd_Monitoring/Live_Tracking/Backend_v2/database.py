from pymongo import MongoClient
import time
from datetime import datetime, timedelta

class Database:
    def __init__(self):
        self.client = MongoClient("mongodb+srv://amborse31:hoanhuy31@crowdtracking.ozaoo6n.mongodb.net/")
        self.db = self.client["CrowdTracking"]
        self.collection = self.db["Crowd"]
        self.lastRecorded = time.time()

    def insertRecord(self, count, frameId=None):
        currentTime = datetime.now()
        currentTimestamp = time.time()

        if currentTimestamp - self.lastRecorded >= 1:
            record = {
                "frameId": frameId,
                "peopleCount": count,
                "timestamp": currentTime.strftime("%d-%m-%Y %H:%M:%S")
            }
            try:
                self.collection.insert_one(record)
                print(f"Recorded: Frame {frameId}, Time {currentTime}, People {count}")
            except Exception as e:
                print(f"Failed to insert record into database: {e}")
            self.lastRecorded = currentTimestamp

    def getLastHourData(self):
        one_hour_ago = datetime.now() - timedelta(hours=1)
        pipeline = [
            {"$addFields": {
                "timestamp": {
                    "$dateFromString": {
                        "dateString": "$timestamp",
                        "format": "%d-%m-%Y %H:%M:%S"
                    }
                }
            }},
            {"$match": {"timestamp": {"$gte": one_hour_ago}}},
            {"$group": {
                "_id": {
                    "minute": {"$minute": "$timestamp"},
                    "hour": {"$hour": "$timestamp"}
                },
                "avgCount": {"$avg": "$peopleCount"}
            }},
            {"$sort": {"_id.hour": 1, "_id.minute": 1}}
        ]
        return list(self.collection.aggregate(pipeline))

    def getLast30MinutesData(self):
        
        # Create a list of all minutes in the last 30 minutes
   
        # MongoDB pipeline
        pipeline = [
            {"$addFields": {
                "timestamp": {
                    "$dateFromString": {
                        "dateString": "$timestamp",
                        "format": "%d-%m-%Y %H:%M:%S"
                    }
                }
            }},
            {"$match": {
                "timestamp": {
                    "$gte": datetime.utcnow() - timedelta(minutes=30)
                }
            }},
            {"$group": {
                "_id": {
                    "minute": {"$minute": "$timestamp"}
                },
                "avgCount": {"$avg": "$peopleCount"}
            }},
            {"$sort": {"_id.minute": 1}}
        ]
        return list(self.collection.aggregate(pipeline))


from datetime import datetime

class Database:
    def __init__(self):
        # Initialize the MongoDB client and database
        self.client = MongoClient("")
        self.db = self.client["CrowdTracking"]
        self.collection = self.db["Crowd"]
        self.lastRecorded = time.time()  # Initialize with current timestamp

    def insertRecord(self, count, frameId):
        currentTime = datetime.now()  # Use datetime object for formatting
        currentTimestamp = time.time()  # Get current timestamp

        # Only record data every second
        if currentTimestamp - self.lastRecorded >= 1:  # Use timestamps for comparison
            record = {
                "frameId": frameId,
                "peopleCount": count,
                "timestamp": currentTime.strftime("%d-%m-%Y %H:%M:%S")  # Format datetime object
            }
            try:
                self.collection.insert_one(record)
                print(f"Recorded: Frame {frameId}, Time {currentTime.strftime('%d-%m-%Y %H:%M:%S')}, People {count}")
            except Exception as e:
                print(f"Failed to insert record into database: {e}")
            self.lastRecorded = currentTimestamp  # Update the last recorded timestamp

    def getlastestRecord(self):
        latestRecord = self.collection.find_one(sort=[("timestamp", -1)])
        return latestRecord["peopleCount"] if latestRecord else 0
    
    def close(self):
        self.client.close()
