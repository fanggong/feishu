from quart import Quart, request, jsonify
from utils import *
from funcs import *
import asyncio

app = Quart(__name__)


async def handle_crypto_update():
    send_text_msg_to_myself(f'[LongQi] [{now()}] 已接收到数据更新请求')
    synchronous_withdraw_history(conn=conn, funding_api=funding_api)
    send_text_msg_to_myself(f'[LongQi] [{now()}] 数据更新成功')


async def handle_crypto_report():
    send_text_msg_to_myself(f'[LongQi] [{now()}] 已接收到数据报告请求')


@app.route('/event', methods=['POST'])
async def event():
    data = await request.get_json()
    if data['event']['event_key'] == 'crypto_update':
        await handle_crypto_update()
    elif data['event']['event_key'] == 'crypto_report':
        await handle_crypto_report()
    return jsonify({'message': 'Event received'}), 200


# @app.route('/webhook', methods=['POST'])
# def webhook():
#     print(request.json)
#     data = request.get_json
#
#     if data.get('type') == 'url_verification':
#         challenge = data.get('challenge')
#         return jsonify({'challenge': challenge}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=11066)

