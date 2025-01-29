from flask import Blueprint, request, jsonify
from flask_login import login_required
from app import db
from app.models.file import File

file_bp = Blueprint("file", __name__)

@file_bp.route("/upload_file", methods=["POST"])
@login_required
def upload_file():
    data = request.json
    new_file = File(repo_id=data["repo_id"], file_name=data["file_name"], file_path=data["file_path"])
    db.session.add(new_file)
    db.session.commit()
    return jsonify({"message": "File uploaded successfully"}), 201