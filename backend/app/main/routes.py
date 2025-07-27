from flask import Blueprint, render_template, redirect, url_for, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User
import pandas as pd
import os  

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def home():
    return redirect(url_for("auth.login"))

@main_bp.route("/dashboard")
@jwt_required()
def dashboard():
    user_id = get_jwt_identity()  
    user = User.query.get(int(user_id))  
    return render_template("dashboard.html", user=user)

@main_bp.route("/success")
@jwt_required()
def success():
    user_id = get_jwt_identity()  
    user = User.query.get(int(user_id))  
    return render_template("success.html", user=user)

@main_bp.route("/api/card-data")
@jwt_required()
def card_data():
    try:
        # Correct path to access CSV inside backend/data/
        base_dir = os.path.abspath(os.path.dirname(__file__))  # /backend/app/main
        csv_path = os.path.join(base_dir, "..", "..", "data", "cards_data.csv")  # relative to main/

        df = pd.read_csv(csv_path)

        # Clean 'credit_limit' column (remove $ and convert to float)
        df["credit_limit"] = df["credit_limit"].replace('[\$,]', '', regex=True).astype(float)

        return jsonify(df.to_dict(orient="records"))
    except Exception as e:
        return jsonify({"error": str(e)}), 500
