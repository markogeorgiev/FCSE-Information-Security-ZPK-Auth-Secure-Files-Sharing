from flask import Blueprint, render_template
from flask_login import login_required
from app.models.repository import Repository

main = Blueprint("main", __name__)

@main.route("/")
@login_required
def home():
    repos = Repository.query.filter_by(is_private=False).all()
    return render_template("home.html", repos=repos)
