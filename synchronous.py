from database.Mysql import MysqlEngine
from config import *
from funcs import *
from okx.Trade import TradeAPI
from okx.PublicData import PublicAPI
from okx.Account import AccountAPI
from okx.Funding import FundingAPI
import time


if __name__ == '__main__':
    api_key = OKX_CONFIG['api_key']
    secret_key = OKX_CONFIG['secret_key']
    passphrase = OKX_CONFIG['passphrase']
    conn = MysqlEngine(
        user_name=DB_CONFIG['mysql']['username'], password=DB_CONFIG['mysql']['password'],
        host=DB_CONFIG['mysql']['host'], port=DB_CONFIG['mysql']['port'],
        database=DB_CONFIG['mysql']['database']
    )
    trade_api = TradeAPI(api_key, secret_key, passphrase, False, '0')
    account_api = AccountAPI(api_key, secret_key, passphrase, False, '0')
    funding_api = FundingAPI(api_key, secret_key, passphrase, False, '0')
    public_api = PublicAPI(api_key, secret_key, passphrase, False, '0')
    start_time = int(time.mktime(time.strptime('2024-07-01 00:00:00', '%Y-%m-%d %H:%M:%S'))*1000)

    for each in ['SPOT', 'SWAP', 'MARGIN']:
        synchronous_instruments(conn, public_api, instType=each)

    synchronous_mark_price(conn=conn, public_api=public_api, inst_type='MARGIN')
    synchronous_bills_history(conn=conn, account_api=account_api, begin=start_time)
    synchronous_withdraw_history(conn=conn, funding_api=funding_api)
    synchronous_deposit_history(conn=conn, funding_api=funding_api)
    synchronous_positions(conn=conn, account_api=account_api)

