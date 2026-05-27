from flask import request, jsonify
from . import auth_bp

@auth_bp.get("/login")
def login_form():
    return "Login form (GET)"

@auth_bp.post("/login")
def login_submit():
    username = request.form.get("username", "")
    return jsonify({"message": "Logged in", "user": username})