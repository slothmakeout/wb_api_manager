import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "postgresql://postgres:@localhost/reflow"
    )
    WB_API_KEY = os.getenv("WB_API_KEY")
    WB_API_CONTENT_URL = "https://content-api-sandbox.wildberries.ru/content/v2"
    WB_API_CONTENT_PING_URL = "https://content-api-sandbox.wildberries.ru/ping"

    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "logs/wb_api_manager.log")


config = Config()
