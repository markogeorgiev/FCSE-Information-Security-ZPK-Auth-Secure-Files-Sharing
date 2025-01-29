from app import db

class FileAddition(db.Model):
    file_id = db.Column(db.Integer, db.ForeignKey("files.id"), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    action_date = db.Column(db.DateTime, default=db.func.current_timestamp())