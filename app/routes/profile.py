from flask import Blueprint, render_template, request, session , redirect, url_for, flash
from app.models.user import Users
from functools import wraps

from app import db

profile_bp = Blueprint("profile", __name__)



def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Login required", "warning")
            return redirect(url_for('auth.login', next=request.path))
        return f(*args, **kwargs)
    return decorated_function



@profile_bp.route("/profile")
@login_required
def profile():
    user_id = session.get('user_id')
    user = Users.query.get(user_id)
    return render_template("profile.html", user=user)
