from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.stock_services import FyersAPI
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

stocks_bp = Blueprint("stocks", __name__)
fyers_api_client = FyersAPI()

@stocks_bp.route("/quote", methods=["GET"])
def quote():
    stock_name = request.args.get("stock_name")
    if not stock_name:
        return jsonify({"error": "Missing 'stock_name' query parameter"}), 400

    logger.info(f"Fetching quote for stock: {stock_name}")
    result = fyers_api_client.get_ltp(stock_name)
    return jsonify({
        "stock_name": stock_name,
        "quote": result
    }), 200
