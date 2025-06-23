from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session, flash
import uuid
from app.models.dynamodb import users_table

auth_bp = Blueprint('auth', __name__)

# -------------------------
# GET: Show Login Page
# -------------------------
@auth_bp.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")


# -------------------------
# POST: Handle Login Form
# -------------------------
@auth_bp.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]
    role = request.form["role"]

    response = users_table.scan(
        FilterExpression="email = :email_val",
        ExpressionAttributeValues={":email_val": email}
    )

    users = response.get("Items", [])
    if not users:
        flash("No account found with that email.")
        return redirect(url_for("auth.login_page"))

    user = users[0]
    if user["password_hash"] != password:
        flash("Incorrect password.")
        return redirect(url_for("auth.login_page"))

    if user["role"] != role:
        flash("Selected role does not match account.")
        return redirect(url_for("auth.login_page"))

    # Set session
    session["user_id"] = user["user_id"]
    session["name"] = user["name"]
    session["role"] = user["role"]

    # Redirect based on role
    if role == "parent":
        return redirect(url_for("parent.get_all_creches"))
    elif role == "owner":
        return redirect(url_for("owner.get_owner_creches", owner_id=user["user_id"]))
    elif role == "admin":
        return redirect(url_for("admin.admin_dashboard"))

    return redirect("/")


# -------------------------
# POST: Register New User
# -------------------------
@auth_bp.route("/register", methods=["GET"])
def register_page():
    return render_template("register.html")

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    user_id = str(uuid.uuid4())

    item = {
        "user_id": user_id,
        "name": data["name"],
        "email": data["email"],
        "password_hash": data["password"],  # (Hash this in real case!)
        "role": data["role"],
        "created_at": data.get("created_at", "2024-06-16T00:00:00Z")
    }

    users_table.put_item(Item=item)
    return jsonify({"message": "User registered", "user_id": user_id})
