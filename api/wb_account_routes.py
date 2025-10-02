from flask import Blueprint
from controllers.wb_account_controller import WbAccountController

bp = Blueprint("wb_account", __name__, url_prefix="/api/wb/accounts")


def init_wb_account_routes(controller: WbAccountController):
    @bp.route("/<int:account_id>", methods=["GET"])
    def get_account(account_id):
        return controller.get_account_by_id(account_id)

    @bp.route("/api-key", methods=["PUT"])
    def update_api_key():
        return controller.update_account_api_key()

    return bp
