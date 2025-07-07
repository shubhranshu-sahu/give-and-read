from flask import Blueprint, render_template, request, session #redirect, url_for, flash
from app.models.contact import contact_us

from app import db

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    return render_template("index.html")




@main_bp.route("/contact" , methods = ['GET' , 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        msg = request.form.get('msg')

        entry = contact_us(name = name , email=email , message = msg )
        db.session.add(entry)
        db.session.commit()

    all_data = None
    if session.get('username') == 'admin':
        all_data = contact_us.query.order_by(contact_us.date.desc()).all()

    return render_template("contact.html", data=all_data)




@main_bp.route("/about")
def about():
    return render_template("about.html")