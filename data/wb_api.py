import requests
from utils.logger import get_logger

logger = get_logger(__name__)


class WbApi:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://content-api-sandbox.wildberries.ru"
        self.content_url = f"{self.base_url}/content/v2"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

    def validate_api_key(self) -> bool:
        try:
            ping_url = f"{self.base_url}/ping"
            response = requests.get(ping_url, headers=self.headers)
            logger.info(f"ping_url: {ping_url}, headers: {self.headers}")
            response.raise_for_status()
            return True
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                return False
            elif e.response.status_code == 429:
                raise WBAPIError("Too many requests - rate limit exceeded") from e
            else:
                raise WBAPIError(f"API error: {e.response.status_code}") from e

        except requests.exceptions.RequestException:
            raise

    def get_card_list(self):
        try:
            card_list_url = f"{self.content_url}/get/cards/list"
            payload = {
                "settings": {"cursor": {"limit": 100}, "filter": {"withPhoto": -1}}
            }

            response = requests.post(card_list_url, headers=self.headers, json=payload)
            response.raise_for_status()
            logger.debug(f"response status code: {response.status_code}")

            card_list = response.json()
            return card_list
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code
            if status_code == 401:
                raise WBAPIError("Unathorized") from e
            elif status_code == 429:
                raise WBAPIError("Too many requests - rate limit exceeded") from e
            elif 400 <= status_code < 500:
                raise WBAPIError(
                    f"Client error {status_code}: {e.response.text}"
                ) from e
            elif 500 <= status_code < 600:
                raise WBAPIError(f"Server error {status_code}") from e
            return None


class WBAPIError(Exception):
    pass
