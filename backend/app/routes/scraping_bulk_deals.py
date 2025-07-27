

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.crypto_services import get_current_price, make_init_data
import logging
import json
from app import db

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

bulk_deals_bp = Blueprint("bulk_deals", __name__)

@bulk_deals_bp.route("/top_bulk_deals", methods=["GET"])
def top_5_bulk_deals():
    try:
        query = """
            SELECT symbol,
                   SUM(quantity_traded) AS total_buy_volume
            FROM public.bulk_data
            WHERE buy_sell = 'BUY'
            GROUP BY symbol
            ORDER BY total_buy_volume DESC
            LIMIT 10;
        """
        result = db.session.execute(query).fetchall()

        top_deals = [
            {"symbol": row[0], "total_buy_volume": int(row[1])}
            for row in result
        ]

        return jsonify({"top_bulk_deals": top_deals}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


