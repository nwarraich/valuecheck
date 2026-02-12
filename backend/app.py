from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

from database import db
from routes.auth_routes import auth_bp
from routes.analysis_routes import analysis_bp

load_dotenv()

def create_app():
    app = Flask(__name__)

    # ------------------
    # Basic config
    # ------------------
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///valuecheck.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # ------------------
    # Extensions
    # ------------------
    CORS(app)
    db.init_app(app)

    # ------------------
    # Routes / Blueprints
    # ------------------
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(analysis_bp, url_prefix="/analyze")

    return app


app = create_app()

# ------------------
# Create DB tables (DEV ONLY)
# ------------------
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, port=8001)
