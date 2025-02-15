from app.main import app
import scheduler
import logging

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s][%(asctime)s][%(name)s] %(message)s',
    handlers=[
        logging.FileHandler('output.log'),
        logging.StreamHandler()
    ]
)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=11066)
