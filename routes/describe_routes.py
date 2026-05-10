from flask import Blueprint

describe_bp = Blueprint("describe", __name__)

@describe_bp.route("/describe")
def describe():
    return {
        "message": "Describe endpoint working"
    }