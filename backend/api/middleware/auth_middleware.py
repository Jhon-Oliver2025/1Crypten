from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            verify_jwt_in_request()
            return f(*args, **kwargs)
        except:
            return jsonify({"error": "Invalid or missing token"}), 401
    return decorated