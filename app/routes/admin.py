from flask import Blueprint, render_template, redirect, url_for
from app.models.dynamodb import creches_table

admin_bp = Blueprint('admin', __name__)

@admin_bp.route("/admin/creches")
def admin_dashboard():
    response = creches_table.scan()
    creches = response.get("Items", [])
    return render_template("admin_dashboard.html", creches=creches)

@admin_bp.route("/admin/approve/<creche_id>")
def approve_creche(creche_id):
    response = creches_table.scan()
    creche = next((c for c in response.get("Items", []) if c["creche_id"] == creche_id), None)
    if creche:
        creche["status"] = "approved"
        creches_table.put_item(Item=creche)
    return redirect(url_for("admin.admin_dashboard"))

@admin_bp.route("/admin/reject/<creche_id>")
def reject_creche(creche_id):
    response = creches_table.scan()
    creche = next((c for c in response.get("Items", []) if c["creche_id"] == creche_id), None)
    if creche:
        creches_table.delete_item(Key={"creche_id": creche_id})
    return redirect(url_for("admin.admin_dashboard"))
