import jwt
import datetime
from flask import current_app
import bcrypt
from functools import wraps
from flask import request, jsonify
from models import User

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(password: str, pw_hash: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), pw_hash.encode('utf-8'))

def generate_token(user_id: int, days_valid: int = 7) -> str:
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=days_valid),
        "iat": datetime.datetime.utcnow()
    }
    return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm="HS256")

def decode_token(token: str):
    return jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get("Authorization")
        if not auth:
            return jsonify({"error": "Token missing"}), 401
        token = auth.split("Bearer ")[-1] if "Bearer " in auth else auth
        try:
            data = decode_token(token)
            user = User.query.get(data["user_id"])
            if not user:
                raise Exception("User not found")
        except Exception as e:
            return jsonify({"error": "Invalid or expired token", "details": str(e)}), 401
        return f(user, *args, **kwargs)
    return decorated
