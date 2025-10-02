from flask import jsonify, request
from services.wb_card_service import WBCardService
from utils.logger import get_logger

logger = get_logger(__name__)


class WbCardController:
    def __init__(self, service: WBCardService):
        self.service = service

    def add_card_list(self):
        card_list = self.service.add_card_list()
        if card_list is None:
            return jsonify({"error": "Something went wrong"}), 404
        logger.info(f"card_list: {card_list}")
        return jsonify({"message": "ok"})
