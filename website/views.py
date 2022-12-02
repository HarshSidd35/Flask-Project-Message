from flask import Blueprint,render_template,redirect,request,flash
from .models import User,Note
from flask_login import login_required,current_user
from . import db

views = Blueprint("views", __name__)

@views.route("/", methods=['GET','POST']) 
@login_required
def index(): 
    if request.method == "POST":
        note = request.form.get('note')

        newNote = Note(data=note, user_id=current_user.id)
        db.session.add(newNote)
        db.session.commit()
        # flash("New Note added",category='Success')

    return render_template("home.html", current_user=current_user)

@views.route('/delete-note/<int:id>')
def delete_note(id):
    note = Note.query.filter_by(id=id).first()
    db.session.delete(note)
    db.session.commit()
    return redirect("/")


@views.route("/delete/<int:id>")
def delete(id):
    record = User.query.filter_by(id=id).first()
    db.session.delete(record)
    db.session.commit()
    return redirect("/display")

@views.route("/display")
@login_required
def show():
    userData = User.query.all()
    return render_template("show.html", Data=userData)