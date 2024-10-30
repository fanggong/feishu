from quart import Quart
from app.routes import crypto, bar


app = Quart(__name__)

app.register_blueprint(crypto.bp)
app.register_blueprint(bar.bp)
