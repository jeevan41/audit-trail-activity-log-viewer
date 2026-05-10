from flask import Blueprint, request, jsonify
from services.groq_service import generate_description

describe_bp = Blueprint("describe", __name__)

@describe_bp.route("/describe", methods=["POST"])
def describe():

    data = request.get_json()

    required_fields = [
        "username",
        "action_type",
        "module",
        "timestamp",
        "ip_address",
        "status"
    ]

    for field in required_fields:
        if field not in data:
            return jsonify({
                "error": f"{field} is required"
            }), 400

    result = generate_description(data)

    return jsonify(result), 200