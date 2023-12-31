from flask import Blueprint,flash,render_template,redirect,url_for,request
from . import db
from .models import User
from flask_login import login_user,logout_user,login_required,current_user
from werkzeug.security import generate_password_hash,check_password_hash 
from werkzeug.utils import secure_filename
import re


#..................................................User/creator_portion..................................................


auth = Blueprint("auth",__name__)

@auth.route("/")
def main():
    return render_template("base.html",user=current_user)



@auth.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":

        email =request.form.get("log-email")
       
        password =request.form.get("log-password")
        user= User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                flash("logged in")
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Password is incorrect.",category="error")
        else:
            flash("EMail does not exists")
    
            
    return render_template("login.html",user=current_user)


@auth.route("/signup",methods=["GET","POST"])
def sign_up():
    if request.method=="POST":

        image = request.files["image"]

        
        
        filename =secure_filename(image.filename)
        mimetype_profile =image.mimetype
        

        email =request.form.get("sign-email")
        username =request.form.get("sign-username")
        password1 =request.form.get("sign-password1")
        password2 =request.form.get("sign-password2")
        is_creator =request.form.get("is_creator")
        if is_creator == "on":
            is_creator=True

        email_exists= User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()

        if email_exists:

            flash("Email is already in use",category="error")
        elif not image:
            flash("choose profile the image",category="error")
        elif username_exists:
            flash("username is already in use",category="error" )
        elif password1 != password2:
            flash("password don\'t match! ",category="error")
        elif len(username) <2:
            flash("Username is too short ." , category="error")
        elif len(password1)<6:
            flash("password is too short ", category="error")
        elif len(email)<4:
            flash("email is invalid", category="error")
            
        else:
            new_user = User(image=image.read(),mimetype_profile=mimetype_profile,name=filename,email=email,username=username,is_creater=is_creator,password=generate_password_hash(password1,method="sha256"))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user,remember=True)
            flash("User created ")
            return redirect(url_for("views.home"))
        
    return render_template("signup.html",user=current_user)


#..................................................admin_portion..................................................

@auth.route("/admin",methods=["GET","POST"])
def admin():
    predefine_password="Tvision@1011"

    if request.method=="POST":
        
        email=request.form.get("log-email")
        if email:
            password =request.form.get("log-password")
            Admin_password =request.form.get("log-ad-password")
            admin = User.query.filter_by(email=email).first()
            if admin:
                if check_password_hash(admin.password,password):
                    if admin.is_admin:
                        flash("logged in")
                        login_user(admin, remember=True)
                        return redirect(url_for("views.home"))
                    else:
                        flash("your not a admin",category="error")
                else:
                    flash("Password is incorrect.",category="error")
            else:
                flash("EMail does not exists")
            
        
        #.........sign-up portion............
        else:
        
            email =request.form.get("sign-email")
            username =request.form.get("sign-username")
            password =request.form.get("sign-password")
            Admin_password =request.form.get("sign-ad-password")

            image = request.files["image"]

           
            
            filename =secure_filename(image.filename)
            mimetype_profile =image.mimetype


            email_exists= User.query.filter_by(email=email).first()
            username_exists = User.query.filter_by(username=username).first()
        
            

            if Admin_password != predefine_password :
                flash("password don\'t match!  Enter valid Admin password ",category="error")
            elif not image:
                flash("choose profile the image",category="error")
            elif email_exists:
                flash("Email is already in use",category="error")
            elif username_exists:
                 flash("username is already in use",category="error" )
            elif len(username) <2:
                flash("Username is too short ." , category="error")
            elif len(password)<8:
                flash("password is too short ", category="error")
            elif not re.match(r"[^@]+@gmail\.com$", email):               #re.match() is a Python function that checks if a given string matches a specified regular expression pattern from the beginning of the string
                flash("Email is invalid or not a Gmail address", category="error")
            elif len(email) < 4:
                flash("Email is too short", category="error")
            else:
                new_admin = User(image=image.read(),mimetype_profile=mimetype_profile,name=filename,email=email,username=username,password=generate_password_hash(password,method="sha256"),is_admin=True)
                db.session.add(new_admin)
                db.session.commit()
                login_user(new_admin,remember=True)
                flash("Admin created ")
                return redirect(url_for("views.home"))
            
            



    return render_template("admin.html",user=current_user)



@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return  redirect(url_for("views.home"))