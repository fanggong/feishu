from quart import request, jsonify, Blueprint
import asyncio
from app.controller.handle_bar_event import handle_bar_update, handle_sales_report
from app.controller.handle_bar_webhook import update_sales_report
from app.utils.run_async import run_in_back

bp = Blueprint('bar', __name__)


@bp.route('/event-bar', methods=['POST'])
async def event():
    data = await request.get_json()
    tasks = {
        'bar_update': handle_bar_update,
        'sales_report': handle_sales_report
    }
    if tasks.get(data['event']['event_key']):
        task = asyncio.create_task(run_in_back(tasks.get(data['event']['event_key'])))
        task.add_done_callback(lambda t: t.exception())

    return jsonify({'message': 'Event received'}), 200
    # return jsonify({'challenge': data.get('challenge')})


@bp.route('/webhook-bar', methods=['POST'])
async def webhook():
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
        new_mission = asyncio.create_task(run_in_back(task[0], **task[1]))
        new_mission.add_done_callback(lambda t: t.exception())

    return jsonify({}), 200
    # return jsonify({'challenge': data.get('challenge')})