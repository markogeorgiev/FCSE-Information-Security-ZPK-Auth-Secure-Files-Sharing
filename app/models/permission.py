from app import db

class Permission(db.Model):
    repo_id = db.Column(db.Integer, db.ForeignKey("repositories.id"), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    access_type = db.Column(db.String(10), nullable=False)