from flask import Blueprint, request, jsonify
# from services.groq_service import generate_description
# from services.groq_service import generate_description, generate_recommendations

from services.groq_service import (
    generate_description,
    generate_recommendations,
    generate_report
)

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


@describe_bp.route("/recommend", methods=["POST"])
def recommend():

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

    result = generate_recommendations(data)

    return jsonify(result), 200


@describe_bp.route("/generate-report", methods=["POST"])
def report():

    data = request.get_json()

    required_fields = [
        "system_name",
        "total_events",
        "failed_logins",
        "suspicious_activities"
    ]

    for field in required_fields:
        if field not in data:
            return jsonify({
                "error": f"{field} is required"
            }), 400

    result = generate_report(data)

    return jsonify(result), 200