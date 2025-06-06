from flask import render_template, url_for, request, redirect, session, flash
from .utils import usermanager
from . import main_bp




@main_bp.route("/", methods=["GET", "POST"])
def home():
    if not session.get("username") or not session.get("access"):
        return redirect(url_for("auth.login"))

    data = usermanager.user_data(session.get("username"))
    if data:
        tasks = data["tasks"]
    else:
        tasks = []
        
    return render_template("home.html", tasks=tasks, user=session.get("username").title())

@main_bp.route("/create", methods=["POST"])
def create():
    task = request.form.get("task")
    if not usermanager.add_task(session.get("username"), task):
        flash("You can not add empty task", "warning")
    return redirect(url_for("main.home"))


@main_bp.route("/done", methods=["POST"])
def done():
    task = request.form.get("finish_task")
    if usermanager.mark_as_done(session.get("username"), task):
        flash("Great!", "success")
        return redirect(url_for("main.home"))
    
    task = request.form.get("remove_task")
    if usermanager.remove_task(session.get("username"), task):
        return redirect(url_for("main.home"))
    
    flash("Task doesn't exist", "warning")
    return redirect(url_for("main.home"))


@main_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("auth.login"))