from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.repository import Repository

repo_bp = Blueprint("repository", __name__)

@repo_bp.route("/create_repo", methods=["POST"])
@login_required
def create_repo():
    data = request.json
    new_repo = Repository(name=data["name"], creator_id=current_user.id, is_private=data["is_private"])
    db.session.add(new_repo)
    db.session.commit()
    return jsonify({"message": "Repository created successfully"}), 201