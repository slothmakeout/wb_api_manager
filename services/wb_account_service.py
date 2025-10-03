from data.wb_api import WbApi
from data.repositories import WbAccountsRepository
from utils.logger import get_logger

logger = get_logger(__name__)


class WbAccountService:
    def __init__(self, wb_api: WbApi, wb_account_repository: WbAccountsRepository):
        self.wb_api = wb_api
        self.wb_account_repository = wb_account_repository

    def get_account_by_id(self, account_id: int):
        return self.wb_account_repository.get_wb_account_by_id(account_id)

    def update_api_key(self, api_key: str) -> bool:
        logger.info(f"Updating API key for account, api_key: {api_key}")
        is_valid = self.wb_api.validate_api_key(api_key)
        logger.info(f"is_valid: {is_valid}")
        if is_valid:
            # Достаём account_id из нашей сессии в браузере (пока что заглушка id=1)
            account_id = 1
            self.wb_account_repository.update_api_key(account_id, api_key)

        return is_valid
