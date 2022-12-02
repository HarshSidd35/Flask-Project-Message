from flask import Blueprint,render_template,redirect,request,flash,url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,login_required,logout_user,current_user

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged In Successfully!",category="Info")
                login_user(user,remember=True)
                return redirect("/")
            else:
                flash("Incorrect Password!",category='Error')
        else:
            flash("User Dosent Exist!",category='Warning')

    return render_template("login.html", user=current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route("/signup", methods=["GET","POST"])
def signup():
    if request.method == "POST":
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        cpassword= request.form.get("password2")
        user = User.query.filter_by(email=email).first()

        if user:
            flash("Email already exists!",category='Warning') 
        elif email == '':
            flash("Please Enter The email",category="Error")
        elif name == '':
            flash("Please Enter The Name",category="Error")
        elif password == '':
            flash("Please Enter The Password",category="Error")
        elif email == '':
            flash("Please Enter The email",category="Error")
        elif len(email) < 4:
            flash("Email must be greater than 4 characters",category="Error")
        elif len(name) <2:
            flash("name must be greater than 2 characters", category="Error")
        elif len(password)<3:
            flash("Password length must be greater than 4 characters",category="Error")
        elif password != cpassword:
            flash("Password is not same ,make same password",category="Error")
        else:
            newUser = User(email=email,name=name,password=generate_password_hash(password,method="sha256"))
            db.session.add(newUser)
            db.session.commit()
            flash("Account Created" ,category="Success")
            return redirect(url_for("auth.login"))

    return render_template("signup.html", user=current_user)