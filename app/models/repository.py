from app import db

class Repository(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    creator_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    is_private = db.Column(db.Boolean, default=False)

    creator = db.relationship("User", backref="repositories")