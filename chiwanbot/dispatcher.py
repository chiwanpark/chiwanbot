from flask import abort, request
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from .root import app, linebot_api, line_handler

@app.route('/callback', methods=['POST'])
def line_callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@line_handler.add(MessageEvent, message=TextMessage)
def echo_handler(event):
    text = event.message.text
    linebot_api.reply_message(event.reply_token, TextMessage(text=text))
