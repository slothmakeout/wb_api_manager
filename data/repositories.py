from data.models import WbAccount, WbCard, WbPhotos
from utils.logger import get_logger

logger = get_logger(__name__)


class WbAccountsRepository:
    def __init__(self, db):
        self.db = db

    def get_wb_account_by_id(self, account_id: int) -> WbAccount | None:
        user = self.db.session.execute(
            self.db.select(WbAccount).where(WbAccount.id == account_id)
        ).scalar_one_or_none()
        logger.info(f"got user: {user.__repr__()}")
        return user

    def update_api_key(self, account_id: int, api_key: str) -> None:
        user = self.get_wb_account_by_id(account_id)
        if user:
            user.api_key = api_key
            self.db.session.commit()


class WbCardRepository:
    def __init__(self, db):
        self.db = db

    def add_wb_card(self, wb_card_data, photos_data):
        wb_card = WbCard(
            nm_id=wb_card_data.nm_id,
            title=wb_card_data.title,
            description=wb_card_data.description,
        )
        self.db.session.add(wb_card)
        self.db.session.commit()
        photos = WbPhotos(
            big=photos_data.big,
            c246x328=photos_data.c246x328,
            c516x688=photos_data.c516x688,
            square=photos_data.square,
            tm=photos_data.tm,
            card_id=wb_card.id,
        )
        self.db.session.add(photos)
        self.db.session.commit()