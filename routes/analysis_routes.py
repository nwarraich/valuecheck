from flask import Blueprint, request, jsonify
from analyzer import analyze_listing

analysis_bp = Blueprint("analysis", __name__)

@analysis_bp.route("/", methods=["POST"])
def analyze():
    data = request.get_json()
    listing_text = data.get("listing_text", "")

    if not listing_text:
        return jsonify({"error": "Listing text is required"}), 400

    result = analyze_listing(listing_text)
    return jsonify(result)
