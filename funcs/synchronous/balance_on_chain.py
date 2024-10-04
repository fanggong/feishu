import pandas as pd
from moralis import sol_api, evm_api
from database.Mysql import MysqlEngine


def get_balance_on_chain_sol_native(api_key, params):
    dat = sol_api.account.balance(api_key=api_key, params=params)
    dat = pd.DataFrame({
        'mint': None,
        'amount': dat['solana'],
        'name': 'Solana',
        'symbol': 'SOL',
        'chain': 'sol',
        'network': params['network'],
        'address': params['address']
    }, index=[0])
    return dat


def get_balance_on_chain_sol_token(api_key, params):
    columns = {
        'mint': 'mint',
        'amount': 'amount',
        'name': 'name',
        'symbol': 'symbol'
    }
    dat = sol_api.account.get_spl(api_key=api_key, params=params)

    dat = pd.DataFrame(dat)
    dat = dat[columns.keys()]
    dat = dat.rename(columns=columns)
    dat['chain'] = 'sol'
    dat['network'] = params['network']
    dat['address'] = params['address']
    return dat


def get_balance_on_chain_evm_token(api_key, params):
    columns = {
        'token_address': 'mint',
        'balance_formatted': 'amount',
        'name': 'name',
        'symbol': 'symbol'
    }

    params['exclude_spam'] = True
    cursor = 1
    dat = []
    while cursor:
        tmp = evm_api.wallets.get_wallet_token_balances_price(api_key=api_key, params=params)
        dat = dat + tmp['result']
        cursor = tmp['cursor']
        params['cursor'] = tmp['cursor']

    dat = pd.DataFrame(dat)
    dat = dat[columns.keys()]
    dat = dat.rename(columns=columns)
    dat['chain'] = 'evm'
    dat['network'] = params['chain']
    dat['address'] = params['address']
    return dat


def synchronous_balance_on_chain(conn: MysqlEngine, api_key: str, params_dict: dict):
    dat = pd.DataFrame()
    for chain, params in params_dict.items():
        for each in params:
            if chain == 'sol':
                token = get_balance_on_chain_sol_token(api_key=api_key, params=each)
                native = get_balance_on_chain_sol_native(api_key=api_key, params=each)
                tmp = pd.concat([token, native])
            elif chain == 'evm':
                tmp = get_balance_on_chain_evm_token(api_key=api_key, params=each)
            else:
                tmp = pd.DataFrame()
            dat = pd.concat([dat, tmp])
    conn.replace_dat(dat=dat, tbl_name='balance_on_chain')