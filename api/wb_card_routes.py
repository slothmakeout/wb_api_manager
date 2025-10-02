from flask import Blueprint
from controllers.wb_card_controller import WbCardController

bp = Blueprint("wb_cards", __name__, url_prefix="/api/wb/cards")


def init_wb_card_routes(controller: WbCardController):
    @bp.route("/", methods=["GET"])
    def add_card_list():
        return controller.add_card_list()

    return bp
