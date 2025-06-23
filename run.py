from flask import Flask, render_template
from dotenv import load_dotenv
import os

from app.routes.auth import auth_bp
from app.routes.parent import parent_bp
from app.routes.owner import owner_bp
from app.routes.admin import admin_bp

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

# Register all Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(parent_bp)
app.register_blueprint(owner_bp)
app.register_blueprint(admin_bp)

# Route for landing page
@app.route("/")
def landing():
    return render_template("landing.html")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)

