# In app/db.py or another appropriate file
from app.db import db
from datetime import datetime
from app.models.logs import DetectionLogs

def log_detection_to_db(timestamp, status, image_path=None):
    """
    Logs detection data to the database.
    """
    # Create a new DetectionLogs instance
    detection_log = DetectionLogs(
        timestamp=timestamp,
        status=status,
        image_path=image_path
    )
    
    # Add the log entry to the database
    db.session.add(detection_log)
    db.session.commit()
    print(f"📝 Detection log saved: {status} at {timestamp}")
