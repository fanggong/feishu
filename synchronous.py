from database.Mysql import MysqlEngine
from config import *
from script import *
from okx.Trade import TradeAPI
from okx.PublicData import PublicAPI
from okx.Account import AccountAPI
from okx.Funding import FundingAPI
import time
import json


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

    synchronous_bills_history(account_api=account_api, path=None, begin=start_time, conn=conn)
    synchronous_withdraw_history(conn=conn, funding_api=funding_api)
    synchronous_deposit_history(conn=conn, funding_api=funding_api)

    # result = account_api.get_bills_archive(year=2024, quarter='Q2')
    # print(json.dumps(result['data'], indent=4, ensure_ascii=False))