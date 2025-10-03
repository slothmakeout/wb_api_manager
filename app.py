from flask import Flask

from api.wb_account_routes import init_wb_account_routes
from api.wb_card_routes import init_wb_card_routes
from config import Config
from controllers.wb_account_controller import WbAccountController
from controllers.wb_card_controller import WbCardController
from data.database import init_db, db
from data.repositories import WbAccountsRepository, WbCardRepository
from data.wb_api import WbApi
from services.wb_account_service import WbAccountService
from services.wb_card_service import WBCardService


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    init_db(app)

    wb_api = WbApi()

    wb_account_repository = WbAccountsRepository(db)
    wb_account_service = WbAccountService(wb_api, wb_account_repository)
    wb_account_controller = WbAccountController(wb_account_service)
    app.register_blueprint(init_wb_account_routes(wb_account_controller))

    wb_card_repository = WbCardRepository(db)
    wb_card_service = WBCardService(wb_api, wb_card_repository)
    wb_card_controller = WbCardController(wb_card_service)
    app.register_blueprint(init_wb_card_routes(wb_card_controller))

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
