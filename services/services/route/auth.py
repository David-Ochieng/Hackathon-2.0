from flask import Blueprint, request, jsonify, current_app
from models import db, User
from utils.auth_utils import hash_password, check_password, generate_token
auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json() or {}
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 400
    pw_hash = hash_password(password)
    user = User(name=name, email=email, password_hash=pw_hash)
    db.session.add(user)
    db.session.commit()
    token = generate_token(user.id)
    return jsonify({"token": token, "user": {"id": user.id, "email": user.email, "name": user.name}})

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400
    user = User.query.filter_by(email=email).first()
    if not user or not check_password(password, user.password_hash):
        return jsonify({"error": "Invalid credentials"}), 401
    token = generate_token(user.id)
    return jsonify({"token": token, "user": {"id": user.id, "email": user.email, "name": user.name, "is_pro": user.is_pro}})
