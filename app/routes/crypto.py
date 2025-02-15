
from quart import request, jsonify, Blueprint
import asyncio
from app.utils.run_async import run_in_back
from app.controller.handle_crypto_event import *

bp = Blueprint('crypto', __name__)


@bp.route('/event', methods=['POST'])
async def event():
    data = await request.get_json()
    print(data)
    # tasks = {
    #     'crypto_update': handle_crypto_update,
    #     'crypto_report': handle_crypto_report,
    #     'risk_report': handle_risk_report
    # }
    # if tasks.get(data['event']['event_key']):
    #     task = asyncio.create_task(run_in_back(tasks.get(data['event']['event_key'])))
    #     task.add_done_callback(lambda t: t.exception())
    # return jsonify({'message': 'Event received'}), 200
    return jsonify({'challenge': data.get('challenge')})