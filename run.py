from app.main import app
from app.services.message_service import MessageService
from app.feishu.FeishuAppRobot import FeishuAppRobot
from app.config import Config
from app.controller.handle_bar_event import handle_bar_update
from app.controller.handle_crypto_event import handle_crypto_update
from app.models.tickets import Tickets
from app.repositories.query_repository import QueryRepository
from app.repositories.update_repository import UpdateRepository
from app.services.update_strategy import UpdateStrategy
from app.controller.handle_crypto_event import CryptoReportService
from app.models.balance import Balance
from app.services.sync_service import SyncService
from app.models.products import Products

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=11066)
    # SyncService.update_table(Balance, Balance.update_strategy)

