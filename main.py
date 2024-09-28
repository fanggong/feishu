import lark_oapi as lark
from config import FEISHU_CONFIG

app_id = FEISHU_CONFIG['LongQi']['app_id']
app_secret = FEISHU_CONFIG['LongQi']['app_secret']


def bot_menu_mission(data: lark.CustomizedEvent) -> None:
    if data.event['event_key'] == 'crypto_update':
        print('更新数据')
    elif data.event['event_key'] == 'crypto_report':
        print('数据报告')


event_handler = lark.EventDispatcherHandler.builder('', '') \
    .register_p2_customized_event('application.bot.menu_v6', bot_menu_mission) \
    .build()


def main():
    cli = lark.ws.Client(app_id=app_id, app_secret=app_secret, event_handler=event_handler, log_level=lark.LogLevel.DEBUG)
    cli.start()


if __name__ == '__main__':
    main()