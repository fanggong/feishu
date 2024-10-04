from quart import Quart, request, jsonify
from utils import *
import asyncio

app = Quart(__name__)


async def run_in_back(sync_func):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, sync_func)


def run_update_task(mission, task_func, *args, **kwargs):
    """
    运行任务的通用函数，处理 try-except 逻辑，并发送消息
    :param mission: 任务名称
    :param task_func: 要执行的任务函数
    :param args: 任务函数的参数
    :param kwargs: 任务函数的关键字参数
    :return: 成功为 1，失败为 0
    """
    try:
        task_func(*args, **kwargs)
        send_text_msg_to_myself(f'[LongQi] [{now()}] Data update for Table {mission} succeeded.')
        return 1  # 成功
    except BaseException as e:
        send_text_msg_to_myself(f'[LongQi] [{now()}] Data update for Table {mission} failed. Reason for failure:：{str(e)}')
        return 0  # 失败


def handle_crypto_update():
    s = f = 0
    start_time = get_yesterday(datetime.datetime.now())
    start_time = int(time.mktime(time.strptime(start_time, '%Y-%m-%d %H:%M:%S')) * 1000)

    send_text_msg_to_myself(f'[LongQi] [{now()}] Starting data update')

    # 任务列表：任务名称和对应函数
    tasks = [
        ('BALANCE', synchronous_balance, {'conn': conn, 'account_api': account_api}),
        ('BILLS HISTORY', synchronous_bills_history, {'conn': conn, 'account_api': account_api, 'begin': start_time}),
        ('INSTRUMENTS SPOT', synchronous_instruments, {'conn': conn, 'public_api': public_api, 'instType': 'SPOT'}),
        ('INSTRUMENTS SWAP', synchronous_instruments, {'conn': conn, 'public_api': public_api, 'instType': 'SWAP'}),
        ('INSTRUMENTS MARGIN', synchronous_instruments, {'conn': conn, 'public_api': public_api, 'instType': 'MARGIN'}),
        ('MARK PRICE SWAP', synchronous_mark_price, {'conn': conn, 'public_api': public_api, 'inst_type': 'SWAP'}),
        ('MARK PRICE MARGIN', synchronous_mark_price, {'conn': conn, 'public_api': public_api, 'inst_type': 'MARGIN'}),
        ('POSITIONS', synchronous_positions, {'conn': conn, 'account_api': account_api}),
        ('WITHDRAW HISTORY', synchronous_withdraw_history, {'conn': conn, 'funding_api': funding_api}),
        ('DEPOSIT HISTORY', synchronous_deposit_history, {'conn': conn, 'funding_api': funding_api}),
        ('EXCHANGE RATE', synchronous_exchange_rate, {'conn': conn, 'market_api': market_api}),
    ]

    # 执行任务
    for mission, func, func_args in tasks:
        result = run_update_task(mission, func, **func_args)
        s += result
        f += (1 - result)  # 如果任务失败，增加 f 计数

    send_text_msg_to_myself(f'[LongQi] [{now()}] Data update completed. A total of {f + s} tasks were executed, with {s} successful and {f} failed.')

    update_log(conn=conn, s=s, f=f)


def handle_crypto_report():
    send_text_msg_to_myself(f'[LongQi] [{now()}] Finance Report Generating')
    send_interactive_card_to_my_self(
        template_variable=datapush_crypto_report(conn=conn),
        template_id=INTERACTIVE_CARD['crypto_report']['id'],
        template_version_name=INTERACTIVE_CARD['crypto_report']['version_name']
    )


def handle_risk_report():
    send_text_msg_to_myself(f'[LongQi] [{now()}] Risk Report Generating')
    send_interactive_card_to_my_self(
        template_variable=datapush_risk_report(conn=conn),
        template_id=INTERACTIVE_CARD['risk_report']['id'],
        template_version_name=INTERACTIVE_CARD['risk_report']['version_name']
    )


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


# @app.route('/webhook', methods=['POST'])
# def webhook():
#     print(request.json)
#     data = request.json
#
#     if data.get('type') == 'url_verification':
#         challenge = data.get('challenge')
#         return jsonify({'challenge': challenge}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=11066)


