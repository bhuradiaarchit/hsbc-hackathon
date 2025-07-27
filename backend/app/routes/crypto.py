

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.crypto_services import get_24hr_ticker_update, get_current_price
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

crypto_bp = Blueprint("crypto", __name__)

@crypto_bp.route("/quote", methods=["GET"])
def quote():
    stock_name = request.args.get("crypto_name")
    if not stock_name:
        return jsonify({"error": "Missing 'stock_name' query parameter"}), 400

    logger.info(f"Fetching quote for stock: {stock_name}")
    result = get_24hr_ticker_update(stock_name)
    return jsonify({
        "stock_name": stock_name,
        "quote": result
    }), 200