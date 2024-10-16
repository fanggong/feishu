from quart import Quart, request, jsonify
from utils import *
import asyncio
from typing import Callable

app = Quart(__name__)


async def run_in_back(sync_func: Callable, **kwargs):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, lambda: sync_func(**kwargs))


def run_update_task(mission: str, task_func: Callable, robot: FeishuAppRobot, *args, **kwargs) -> int:
    try:
        task_func(*args, **kwargs)
        send_text_msg_to_myself(robot, f'[{robot.get_robot_name()}] [{str_now()}] Data update for Table {mission} succeeded.')
        return 1  # success
    except BaseException as e:
        send_text_msg_to_myself(robot, f'[{robot.get_robot_name()}] [{str_now()}] Data update for Table {mission} failed. Reason for failure:：{str(e)}')
        return 0  # fail


def handle_crypto_update():
    start_time = get_yesterday(datetime.datetime.now())
    start_time = int(time.mktime(time.strptime(start_time, '%Y-%m-%d %H:%M:%S')) * 1000)

    # tasks
    tasks = [
        ('BALANCE', synchronous_balance, {'conn': CONN, 'account_api': ACCOUNT_API}),
        ('BILLS HISTORY', synchronous_bills_history, {'conn': CONN, 'account_api': ACCOUNT_API, 'begin': start_time}),
        ('INSTRUMENTS SPOT', synchronous_instruments, {'conn': CONN, 'public_api': PUBLIC_API, 'instType': 'SPOT'}),
        ('INSTRUMENTS SWAP', synchronous_instruments, {'conn': CONN, 'public_api': PUBLIC_API, 'instType': 'SWAP'}),
        ('INSTRUMENTS MARGIN', synchronous_instruments, {'conn': CONN, 'public_api': PUBLIC_API, 'instType': 'MARGIN'}),
        ('MARK PRICE SWAP', synchronous_mark_price, {'conn': CONN, 'public_api': PUBLIC_API, 'inst_type': 'SWAP'}),
        ('MARK PRICE MARGIN', synchronous_mark_price, {'conn': CONN, 'public_api': PUBLIC_API, 'inst_type': 'MARGIN'}),
        ('POSITIONS', synchronous_positions, {'conn': CONN, 'account_api': ACCOUNT_API}),
        ('WITHDRAW HISTORY', synchronous_withdraw_history, {'conn': CONN, 'funding_api': FUNDING_API}),
        ('DEPOSIT HISTORY', synchronous_deposit_history, {'conn': CONN, 'funding_api': FUNDING_API}),
        ('EXCHANGE RATE', synchronous_exchange_rate, {'conn': CONN, 'market_api': MARKET_API}),
    ]

    send_text_msg_to_myself(
        FEISHU_APP_ROBOT_CRYPTO,
        f'[{CRYPTO_APP_NAME}] [{str_now()}] Starting data update'
    )
    s = f = 0
    for mission, func, func_args in tasks:
        result = run_update_task(mission, func, FEISHU_APP_ROBOT_CRYPTO, **func_args)
        s += result
        f += (1 - result)
    send_text_msg_to_myself(
        FEISHU_APP_ROBOT_CRYPTO,
        f'[{CRYPTO_APP_NAME}] [{str_now()}] Data update completed. A total of {f + s} tasks were executed, with {s} successful and {f} failed.'
    )

    update_log(conn=CONN, s=s, f=f, role=CRYPTO_APP_NAME)


def handle_crypto_report():
    send_text_msg_to_myself(FEISHU_APP_ROBOT_CRYPTO, f'[{CRYPTO_APP_NAME}] [{str_now()}] Finance Report Generating')
    send_interactive_card_to_my_self(
        robot=FEISHU_APP_ROBOT_CRYPTO,
        template_variable=datapush_crypto_report(conn=CONN),
        template_id=INTERACTIVE_CARD['crypto_report']['id'],
        template_version_name=INTERACTIVE_CARD['crypto_report']['version_name']
    )


def handle_risk_report():
    send_text_msg_to_myself(FEISHU_APP_ROBOT_CRYPTO, f'[{CRYPTO_APP_NAME}] [{str_now()}] Risk Report Generating')
    send_interactive_card_to_my_self(
        robot=FEISHU_APP_ROBOT_CRYPTO,
        template_variable=datapush_risk_report(conn=CONN),
        template_id=INTERACTIVE_CARD['risk_report']['id'],
        template_version_name=INTERACTIVE_CARD['risk_report']['version_name']
    )


def handle_bar_update():
    start_time = get_yesterday(datetime.datetime.now())

    tasks = [
        ('CUSTOMERS', synchronous_customers, {'conn': CONN, 'customers_api': CUSTOMERS_API}),
        ('PRODUCTS', synchronous_product, {'conn': CONN, 'products_api': PRODUCTS_API}),
        ('TICKETS', synchronous_tickets, {'conn': CONN, 'sales_api': SALES_API, 'start_time': start_time, 'end_time': str_now()})
    ]

    send_text_msg_to_myself(FEISHU_APP_ROBOT_BAR, f'[{BAR_APP_NAME}] [{str_now()}] Starting data update')
    s = f = 0
    for mission, func, func_args in tasks:
        result = run_update_task(mission, func, FEISHU_APP_ROBOT_BAR, **func_args)
        s += result
        f += (1 - result)

    send_text_msg_to_myself(
        FEISHU_APP_ROBOT_BAR,
        f'[{BAR_APP_NAME}] [{str_now()}] Data update completed. A total of {f + s} tasks were executed, with {s} successful and {f} failed.'
    )

    update_log(conn=CONN, s=s, f=f, role=BAR_APP_NAME)


def handle_sales_report():
    send_text_msg_to_myself(FEISHU_APP_ROBOT_BAR, f'[{BAR_APP_NAME}] [{str_now()}] Sales Report Generating')
    send_interactive_card_to_my_self(
        robot=FEISHU_APP_ROBOT_BAR,
        template_variable=datapush_sales_report(conn=CONN),
        template_id=INTERACTIVE_CARD['sales_report']['id'],
        template_version_name=INTERACTIVE_CARD['sales_report']['version_name']
    )


def update_sales_report(token, start_date, end_date):
    template_id = INTERACTIVE_CARD['sales_report']['id']
    template_version_name = INTERACTIVE_CARD['sales_report']['version_name']
    template_variable = datapush_sales_report(conn=CONN, start_date=start_date, end_date=end_date)
    card = {
        'type': 'template',
        'data': {
            'template_id': template_id,
            'template_version_name': template_version_name,
            'template_variable': template_variable
        }
    }
    FEISHU_APP_ROBOT_BAR.update_card(token=token, card=card)


@app.route('/event', methods=['POST'])
async def event():
    data = await request.get_json()
    tasks = {
        'crypto_update': handle_crypto_update,
        'crypto_report': handle_crypto_report,
        'risk_report': handle_risk_report
    }
    if tasks.get(data['event']['event_key']):
        asyncio.create_task(run_in_back(tasks.get(data['event']['event_key'])))

    return jsonify({'message': 'Event received'}), 200


@app.route('/event-bar', methods=['POST'])
async def event_bar():
    data = await request.get_json()
    tasks = {
        'bar_update': handle_bar_update,
        'sales_report': handle_sales_report
    }
    if tasks.get(data['event']['event_key']):
        asyncio.create_task(run_in_back(tasks.get(data['event']['event_key'])))

    return jsonify({'message': 'Event received'}), 200


@app.route('/webhook-bar', methods=['POST'])
async def webhook_bar():
    data = await request.get_json()
    token = data['event']['token']
    form_values = data['event'].get('action').get('form_value')
    value = data['event'].get('action').get('value')

    start_date = form_values.get('start_date')[0:10] if form_values.get('start_date') else None
    end_date = form_values.get('end_date')[0:10] if form_values.get('end_date') else None

    tasks = {
        'sales_form': (update_sales_report, {'token': token, 'start_date': start_date, 'end_date': end_date})
    }

    task = tasks.get(value)
    if task:
        asyncio.create_task(run_in_back(task[0], **task[1]))

    return jsonify({}), 200

# @app.route('/webhook', methods=['POST'])
# async def webhook():
#     data = await request.get_json()
#     challenge = data.get('challenge')
#     return jsonify({'challenge': challenge}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=11066)


