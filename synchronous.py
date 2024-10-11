import datetime
import utils

utils.send_text_msg_to_myself = print
import main

if __name__ == '__main__':
    main.handle_crypto_update()
    # if datetime.datetime.now().minute == 0:
    #     main.handle_bar_update()
