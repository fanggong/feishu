from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    print(request.json)
    data = request.json

    if data.get('type') == 'url_verification':
        challenge = data.get('challenge')
        return jsonify({'challenge': challenge}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=11066)