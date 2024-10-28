from app.repositories.update_repository import UpdateRepository
from app.services.update_strategy import UpdateStrategy
from app.services.log import LogService
from app.services.message_service import MessageService
from app.config import Config


class SyncService:
    fetcher_classes = {
        # crypto
        'balance': 'app.services.balance_fetcher.BalanceFetcher',
        'bills_history': 'app.services.bills_history_fetcher.BillsHistoryFetcher',
        'deposit_history': 'app.services.deposit_history_fetcher.DepositHistoryFetcher',
        'withdraw_history': 'app.services.withdraw_history_fetcher.WithdrawHistoryFetcher',
        'instruments': 'app.services.instruments_fetcher.InstrumentsFetcher',
        'mark_price': 'app.services.mark_price_fetcher.MarkPriceFetcher',
        'positions': 'app.services.positions_fetcher.PositionsFetcher',

        # bar
        'customers': 'app.services.customers_fetcher.CustomersFetcher',
        'products': 'app.services.products_fetcher.ProductsFetcher',
        'tickets': 'app.services.tickets_fetcher.TicketsFetcher'
    }

    @staticmethod
    def get_data_fetcher(table_class):
        fetcher_class_path = SyncService.fetcher_classes.get(table_class.__tablename__)
        if not fetcher_class_path:
            raise ValueError(f'No data fetcher defined for table: {table_class.__tablename__}')

        module_name, class_name = fetcher_class_path.rsplit('.', 1)
        module = __import__(module_name, fromlist=[class_name])
        fetcher_class = getattr(module, class_name)
        return fetcher_class()

    @staticmethod
    def update_table(table_class, strategy: UpdateStrategy, **kwargs):
        data_fetcher = SyncService.get_data_fetcher(table_class)
        data_list = data_fetcher.fetch_data(**kwargs)

        if not data_list:
            print("No data to update for table:", table_class.__tablename__)
            return
        try:
            if strategy == UpdateStrategy.FULL:
                UpdateRepository.full_update(table_class, data_list)
            elif strategy == UpdateStrategy.INCREMENTAL:
                UpdateRepository.incremental_update(table_class, data_list)
            LogService.record_update_logs(table_class, 1)
        except Exception as e:
            LogService.record_update_logs(table_class, 0, str(e))
            raise e

    @staticmethod
    def update_multiple_table(table_class, strategy, **kwargs):
        data_fetcher = SyncService.get_data_fetcher(table_class)
        data_list = data_fetcher.fetch_data(**kwargs)

        if not data_list:
            print("No data to update for table:", table_class.__tablename__)
            return

        for index, (key, value) in enumerate(strategy.items()):
            try:
                if value == UpdateStrategy.FULL:
                    UpdateRepository.full_update(key, data_list[index])
                elif value == UpdateStrategy.INCREMENTAL:
                    UpdateRepository.incremental_update(key, data_list[index])
                LogService.record_update_logs(table_class, 1)
            except Exception as e:
                LogService.record_update_logs(table_class, 0, str(e))
                raise e