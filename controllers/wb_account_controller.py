from flask import jsonify, request
from services.wb_account_service import WbAccountService


class WbAccountController:
    def __init__(self, service: WbAccountService):
        self.service = service

    def get_account_by_id(self, account_id: int):
        account = self.service.get_account_by_id(account_id)
        if account:
            return jsonify(
                {"id": account.id, "api_key": account.api_key, "name": account.name}
            )
        return jsonify({"error": "Account not found"}), 404

    def update_account_api_key(self):
        data = request.get_json()
        if "api_key" not in data:
            return jsonify({"error": "API key is required"}), 400

        api_key = data["api_key"]
        try:
            is_valid = self.service.update_api_key(api_key)
            if not is_valid:
                return jsonify({"error": "API key validation failed"}), 400
            return jsonify({"message": "API key updated successfully"})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
