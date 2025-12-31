from flask import Blueprint, request, jsonify
import requests
from ..services.portfolio_service import PortfolioService
from app.config import Config

portfolio_bp = Blueprint('portfolio', __name__)



def get_current_user_from_user_service():
    # Forward the Authorization header if present
    headers = {}
    if 'Authorization' in request.headers:
        headers['Authorization'] = request.headers['Authorization']
    try:
        resp = requests.get(Config.USER_SERVICE_URL, headers=headers, timeout=3)
        if resp.status_code == 200:
            return resp.json().get('user')
    except Exception as e:
        # Optionally log error here if needed
        pass
    return None

@portfolio_bp.route('/total', methods=['GET'])
def get_total_net_holding():
    user = get_current_user_from_user_service()
    if not user:
        return jsonify({"status": "error", "message": "User not authenticated"}), 401
    user_id = user['id']
    total = PortfolioService.get_total_net_holding(user_id)
    return jsonify({"status": "success", "user_id": user_id, "total_net_holding": total})

@portfolio_bp.route('/add', methods=['POST'])
def add_holding():
    user = get_current_user_from_user_service()
    if not user:
        return jsonify({"status": "error", "message": "User not authenticated"}), 401
    user_id = user['id']
    data = request.get_json()
    coin_id = data.get('coin_id')
    amount = data.get('amount')
    if not coin_id or amount is None:
        return jsonify({"status": "error", "message": "coin_id and amount required"}), 400
    holding = PortfolioService.add_holding(user_id, coin_id, amount)
    return jsonify({"status": "success", "holding": {"coin_id": holding.coin_id, "amount": holding.amount}})

@portfolio_bp.route('/remove', methods=['POST'])
def remove_holding():
    user = get_current_user_from_user_service()
    if not user:
        return jsonify({"status": "error", "message": "User not authenticated"}), 401
    user_id = user['id']
    data = request.get_json()
    coin_id = data.get('coin_id')
    if not coin_id:
        return jsonify({"status": "error", "message": "coin_id required"}), 400
    success = PortfolioService.remove_holding(user_id, coin_id)
    if not success:
        return jsonify({"status": "error", "message": "holding not found"}), 404
    return jsonify({"status": "success", "message": "holding removed"})
