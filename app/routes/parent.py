from flask import Blueprint, request, jsonify, render_template
import uuid
from app.models.dynamodb import reviews_table, creches_table

parent_bp = Blueprint('parent', __name__)

# -------------------------------
# 1. Submit Review (Already Done)
# -------------------------------
@parent_bp.route("/review", methods=["POST"])
def post_review():
    data = request.json
    review_id = str(uuid.uuid4())

    item = {
        "review_id": review_id,
        "creche_id": data["creche_id"],
        "user_id": data["user_id"],
        "rating": data["rating"],
        "text": data["text"],
        "timestamp": data.get("timestamp", "2024-06-16T00:00:00Z")
    }

    reviews_table.put_item(Item=item)
    return jsonify({"message": "Review submitted", "review_id": review_id})


# -----------------------------------
# 2. View All Approved Creches
# -----------------------------------
@parent_bp.route("/creches", methods=["GET"])
def get_all_creches():
    response = creches_table.scan()
    creches = response.get('Items', [])
    approved = [c for c in creches if c.get('status') == 'approved']
    return render_template("dashboard_parent.html", creches=approved)

# -----------------------------------
# 3. Filter Creches by Location
# -----------------------------------
@parent_bp.route("/creches/location/<location>", methods=["GET"])
def get_creches_by_location(location):
    response = creches_table.scan()
    creches = response.get('Items', [])
    
    filtered = [
        c for c in creches
        if c.get('status') == 'approved' and location.lower() in c.get('location', '').lower()
    ]
    return jsonify(filtered)


# -----------------------------------
# 4. View Creche Details by ID
# -----------------------------------
@parent_bp.route("/creche/<creche_id>", methods=["GET"])
def creche_detail(creche_id):
    # Get creche details
    creche_resp = creches_table.get_item(Key={"creche_id": creche_id})
    creche = creche_resp.get("Item")

    # Get all reviews for this creche
    review_resp = reviews_table.scan(
        FilterExpression="creche_id = :cid",
        ExpressionAttributeValues={":cid": creche_id}
    )
    reviews = review_resp.get("Items", [])

    if not creche:
        return "Creche not found", 404

    return render_template("creche_detail.html", creche=creche, reviews=reviews)
