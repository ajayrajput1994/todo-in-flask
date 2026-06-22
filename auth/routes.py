from flask import request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import auth_bp
from extensions import db
from models import User

@auth_bp.get("/login")
def login_form():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    # for now, simple inline HTML; later use templates/login.html
    return """
    <form method="post" action="/auth/login">
        <label>Username: <input name="username" /></label><br>
        <label>Password: <input type="password" name="password" /></label><br>
        <button type="submit">Login</button>
    </form>
    """

@auth_bp.post("/login")
def login_submit():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    if not username or not password:
        flash("Username and password required", "error")
        return redirect(url_for("auth.login_form"))

    user = User.query.filter_by(username=username).first()

    if user is None or not user.check_password(password):
        flash("Invalid username or password", "error")
        return redirect(url_for("auth.login_form"))

    login_user(user)  # creates session
    return redirect(url_for("index"))

@auth_bp.get("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login_form"))