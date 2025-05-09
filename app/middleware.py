import jwt
from flask import request, jsonify
from functools import wraps
import os

SECRET_KEY = os.getenv("SECRET_KEY")

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        
        # Check if token is sent in the request header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            # Ensure the token is in 'Bearer <token>' format
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]  # Get the token part
            else:
                return jsonify({"message": "Invalid token format!"}), 401

        if not token:
            return jsonify({"message": "Token is missing!"}), 401

        try:
            # Decode the token using the secret key
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.user = decoded_token  # Attach the decoded token to the request object
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token!"}), 401

        return f(*args, **kwargs)

    return decorated_function
