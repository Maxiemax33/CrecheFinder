from flask import Blueprint, request, jsonify, render_template, redirect, url_for
import uuid
from app.models.dynamodb import creches_table

owner_bp = Blueprint('owner', __name__)

# ----------------------------------
# 1. Add New Creche
# ----------------------------------
@owner_bp.route("/creche/add", methods=["GET", "POST"])
def add_creche():
    if request.method == "POST":
        data = request.form
        creche_id = str(uuid.uuid4())
        item = {
            "creche_id": creche_id,
            "owner_id": data["owner_id"],
            "name": data["name"],
            "location": data["location"],
            "services": [s.strip() for s in data.get("services", "").split(",")],
            "photos": [p.strip() for p in data.get("photos", "").split(",")],
            "status": "pending",
            "added_on": data.get("added_on", "2025-06-22T00:00:00Z")
        }
        creches_table.put_item(Item=item)
        return redirect(url_for('owner.get_owner_creches', owner_id=data["owner_id"]))
    return render_template("creche_form.html", creche=None)


# ----------------------------------
# 2. Get All Creches by Owner
# ----------------------------------
@owner_bp.route("/owner/creches/<owner_id>", methods=["GET"])
def get_owner_creches(owner_id):
    response = creches_table.scan()
    all_creches = response.get('Items', [])
    owned = [c for c in all_creches if c.get("owner_id") == owner_id]
    return render_template("dashboard_owner.html", creches=owned)

# ----------------------------------
# 3. Update a Creche Listing
# ----------------------------------
@owner_bp.route("/creche/edit/<creche_id>", methods=["GET", "POST"])
def edit_creche(creche_id):
    response = creches_table.scan()
    creche = next((c for c in response.get('Items', []) if c["creche_id"] == creche_id), None)
    if not creche:
        return "Creche not found", 404
    
    if request.method == "POST":
        data = request.form
        creche.update({
            "name": data["name"],
            "location": data["location"],
            "services": [s.strip() for s in data.get("services", "").split(",")],
            "photos": [p.strip() for p in data.get("photos", "").split(",")],
        })
        creches_table.put_item(Item=creche)
        return redirect(url_for('owner.get_owner_creches', owner_id=creche["owner_id"]))

    return render_template("creche_form.html", creche=creche)


    return jsonify({"message": "Creche updated", "creche_id": creche_id})
