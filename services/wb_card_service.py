from ctypes import c_char
from dataclasses import dataclass
from typing import Optional, List

from data.repositories import WbCardRepository
from data.wb_api import WbApi
from utils.logger import get_logger
import json

logger = get_logger(__name__)


@dataclass
class PhotoData:
    big: str
    c246x328: str
    c516x688: str
    square: str
    tm: str


@dataclass
class CardData:
    title: str
    description: str
    nm_id: int


class WBCardService:
    def __init__(self, wb_api: WbApi, wb_card_repository: WbCardRepository):
        self.wb_api = wb_api
        self.wb_card_repository = wb_card_repository

    def add_card_list(self):
        card_list = self.wb_api.get_card_list()
        # logger.info(f"card_list: {card_list}")
        # Добавить карточки в бд
        for card in card_list["cards"]:
            photos_data = [PhotoData(**photo) for photo in card["photos"]]

            card_data = CardData(
                title=card["title"],
                description=card["description"],
                nm_id=card["nmID"],
            )
            logger.info(f"card_data: {card_data}")
            # self.wb_card_repository.add_wb_card(card_data, photos_data)
        return card_list

    # def get_card_list(self):
