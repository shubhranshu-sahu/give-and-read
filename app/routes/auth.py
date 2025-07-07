from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from passlib.hash import pbkdf2_sha256 as hasher
from functools import wraps
from app.models.user import Users

from app import db

auth_bp = Blueprint("auth", __name__)



def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Login required", "warning")
            return redirect(url_for('auth.login', next=request.path))
        return f(*args, **kwargs)
    return decorated_function




@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = Users.query.filter_by(email=email).first()

        if user and user.verify_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            next_page = request.form.get('next') or request.args.get('next')
            if next_page and next_page.startswith('/'):
                return redirect(next_page) ##############################################################################################################
            return redirect(url_for('main.index'))

        else:
            
            flash("Invalid email or password.", "danger")  # 'danger' is Bootstrap class
            return redirect(url_for('auth.login'))  # redirect to show flash message

    return render_template("login.html")



@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        gender = request.form.get("gender")
        age = request.form.get("age")

        # Hash password
        hashed_pw = hasher.hash(password)

        # Check if email or username already exists
        if Users.query.filter_by(email=email).first():
            return "Email already registered."
        if Users.query.filter_by(username=username).first():
            return "Username already taken."

        new_user = Users(username=username, email=email, password=hashed_pw, gender=gender, age=age)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login'))

    return render_template("signup.html")

@auth_bp.route("/logout")
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect("/")
