from quart import Quart, request, jsonify
from utils import *
from funcs import *
import asyncio

app = Quart(__name__)


async def run_in_back(sync_func):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, sync_func)


def handle_crypto_update():
    s = f = 0
    send_text_msg_to_myself(f'[LongQi] [{now()}] 开始数据更新任务，任务开始')
    # instruments
    mission = 'INSTRUMENTS'
    try:
        for each in ['SPOT', 'SWAP', 'MARGIN']:
            synchronous_instruments(conn, public_api, instType=each)
        send_text_msg_to_myself(f'[LongQi] [{now()}] {mission} 数据更新成功')
        s = s + 1
    except BaseException as e:
        send_text_msg_to_myself(f'[LongQi] [{now()}] {mission} 数据更新失败，报错信息如下：{str(e)}')
        f = f + 1

    # mark price
    mission = 'MARK PRICE'
    try:
        synchronous_mark_price(conn=conn, public_api=public_api, inst_type='MARGIN')
        send_text_msg_to_myself(f'[LongQi] [{now()}] {mission} 数据更新成功')
        s = s + 1
    except BaseException as e:
        send_text_msg_to_myself(f'[LongQi] [{now()}] {mission} 数据更新失败，报错信息如下：{str(e)}')
        f = f + 1

    # positions
    mission = 'POSITIONS'
    try:
        synchronous_positions(conn=conn, account_api=account_api)
        send_text_msg_to_myself(f'[LongQi] [{now()}] {mission} 数据更新成功')
        s = s + 1
    except BaseException as e:
        send_text_msg_to_myself(f'[LongQi] [{now()}] {mission} 数据更新失败，报错信息如下：{str(e)}')
        f = f + 1

    send_text_msg_to_myself(f'[LongQi] [{now()}] 结束数据更新任务，共计{s+f}项任务，成功{s}项，失败{f}项')


def handle_crypto_report():
    send_text_msg_to_myself(f'[LongQi] [{now()}] 已接收到数据报告请求')


@app.route('/event', methods=['POST'])
async def event():
    data = await request.get_json()
    if data['event']['event_key'] == 'crypto_update':
        asyncio.create_task(run_in_back(handle_crypto_update))
    elif data['event']['event_key'] == 'crypto_report':
        asyncio.create_task(run_in_back(handle_crypto_report))
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


