from flask import Blueprint, request, jsonify
from app.models.user import User
from app.db import db
import jwt
import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Secret key for encoding and decoding JWT tokens (loaded from .env)
SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise ValueError("No SECRET_KEY found in .env file!")

auth_bp = Blueprint("auth", __name__)

import bcrypt

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Missing credentials"}), 400
    
    print(username, password)

    user = User.query.filter_by(username=username).first()
    if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        # Password matches, generate JWT token
        token = generate_jwt_token(user)
        return jsonify({"token": token, "userlevel": user.userlevel})
    else:
        return jsonify({"error": "Invalid credentials"}), 401


def generate_jwt_token(user):
    """
    Generate a JWT token for a user.
    """
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # 1 hour expiration
    payload = {
        "sub": user.id,  # Subject of the token (user ID)
        "username": user.username,
        "userlevel": str(user.userlevel),  # Convert Enum to string here
        "exp": expiration_time  # Expiration time
    }
    # Generate JWT token
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token
