from flask import render_template, request, redirect, flash, session, url_for
from main.utils import usermanager # type: ignore
from . import auth_bp


@auth_bp.route("/Login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        if usermanager.authenticate(username, password):
            session.clear()
            session["access"] = True
            session["username"] = username
            return redirect(url_for("main.home"))
        
        flash("Invalid username or passowrd", "danger")
    return render_template("login.html")


@auth_bp.route("/Register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm")

        if not username or not password:
            flash("Please enter a username and password", "warning")
            return render_template("register.html")

        elif password != confirm_password:
            flash("Password didn't matched. Please try again", "warning")
            return render_template("register.html")
        
        elif usermanager.register(username, password):
            flash("Registered successfully", "success")

        else:
            flash(f"{username} already exist", "warning")

    return render_template("register.html")
