

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.crypto_services import get_current_price, make_init_data
import logging
import json

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

crypto_bp = Blueprint("crypto", __name__)

@crypto_bp.route("/quote", methods=["GET"])
def quote():
    stock_name = request.args.get("crypto_name")
    if not stock_name:
        return jsonify({"error": "Missing 'stock_name' query parameter"}), 400

    logger.info(f"Fetching quote for stock: {stock_name}")
    result = get_current_price(stock_name)
    return jsonify({
        "stock_name": stock_name,
        "quote": result
    }), 200


@crypto_bp.route("/historical", methods=["GET"])
def historical():

    crypto_name = request.args.get("crypto_name", 'BTCUSDT')
    time_frame = request.args.get("timeframe", "1m")

    logger.info(f"Crypto name: {crypto_name}, Time frame: {time_frame}")

    if not crypto_name:
        return jsonify({"error": "Missing 'stock_name' query parameter"}), 400

    logger.info(f"Fetching historical data for stock: {crypto_name}")
    result = make_init_data(crypto_name, time_frame)

    if result is not None and not result.empty:
        result_json = json.loads(result.to_json(orient="records")) 
    else:
        result_json = []
    
    return jsonify({
        "stock_name": crypto_name,
        "historical_data": result_json
    }), 200