from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.stock_services import FyersAPI
import logging
import json

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


@stocks_bp.route("/historical", methods=["GET"])
def historical():
    stock_name = request.args.get("stock_name")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    time_frame = request.args.get("timeframe", "1")

    logger.info(f"Fetching historical data for stock: {stock_name}")
    result = fyers_api_client.get_symbol_data(stock_name, start_date, end_date, time_frame)

    if result is not None and not result.empty:
        result_json = json.loads(result.to_json(orient="records")) 
    else:
        result_json = []

    return jsonify({
        "stock_name": stock_name,
        "historical_data": result_json
    }), 200
