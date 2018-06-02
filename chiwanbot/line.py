# -*- coding: utf-8 -*-

from flask import Blueprint, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from .models import Config

blueprint = Blueprint('line', __name__, url_prefix='/line')

line_api = LineBotApi(Config.get_by_name('LINE_CHANNEL_ACCESS_TOKEN'))
line_handler = WebhookHandler(Config.get_by_name('LINE_CHANNEL_SECRET'))

@blueprint.route('/callback', methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@line_handler.add(MessageEvent, message=TextMessage)
def echo_message(event):
    line_api.reply_message(
        event.reply_token, TextSendMessage(text=event.message.text))
