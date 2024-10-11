import datetime
import utils

utils.send_text_msg_to_myself = print
import main

if __name__ == '__main__':
    main.handle_crypto_update()
    nowtime = datetime.datetime.now()
    if nowtime.hour in (8, 11, 14, 17, 20, 23) and nowtime.minute == 0:
        main.handle_bar_update()
