from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from core.database import Database

settings_bp = Blueprint('settings', __name__)
db = Database()

@settings_bp.route('/', methods=['GET'])
@jwt_required()
def get_settings():
    settings = db.get_all_config()
    return jsonify(settings), 200

@settings_bp.route('/update', methods=['POST'])
@jwt_required()
def update_settings():
    data = request.get_json()
    db.update_config(data)
    return jsonify({"message": "Settings updated"}), 200