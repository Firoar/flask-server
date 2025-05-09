from app.db import db

class DetectionLogs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp()) 
    status = db.Column(db.String(20), nullable=False)  # Store status as a string
    image_path = db.Column(db.String(255), nullable=True)  

    def __init__(self, status, image_path=None):
        self.status = status
        self.image_path = image_path
