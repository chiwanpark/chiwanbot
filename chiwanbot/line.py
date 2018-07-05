# -*- coding: utf-8 -*-

from datetime import datetime

from flask import Blueprint, request, abort
from google.appengine.ext import ndb
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, SourceRoom, SourceGroup, SourceUser

from .models import Config, User
from .plugins import ChatPlugin

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
def callback_text_message(event):
    user = retrieve_user(event.source)
    context = retrieve_context(event.source)

    for plugin_cls in ChatPlugin.plugins:
        plugin = plugin_cls(line_api, event.reply_token)
        if plugin.callback_msg(user, context, event.message):
            break


def retrieve_user(source):
    key = ndb.Key(User, source.user_id)
    user = key.get()
    if user is None:
        user = User()
    elif user.is_valid_profile():
        return user

    if isinstance(source, SourceUser):
        profile = line_api.get_profile(source.user_id)
    elif isinstance(source, SourceGroup):
        profile = line_api.get_group_member_profile(source.group_id, source.user_id)
    elif isinstance(source, SourceRoom):
        profile = line_api.get_room_member_profile(source.room_id, source.user_id)

    user.name = profile.display_name
    user.last_profile_updated = datetime.now()
    user.key = key
    user.put()

    return user


def retrieve_context(source):
    if isinstance(source, SourceUser):
        return '1-on-1-chat'
    elif isinstance(source, SourceGroup):
        return source.group_id
    elif isinstance(source, SourceRoom):
        return source.room_id
