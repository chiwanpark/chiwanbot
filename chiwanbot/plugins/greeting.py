# -*- coding: utf-8 -*-

from linebot.models import TextMessage, TextSendMessage

from . import ChatPlugin


class GreetingPlugin(ChatPlugin):
    def __init__(self, line_api, reply_token):
        super(GreetingPlugin, self).__init__(line_api, reply_token)

    def callback_msg(self, user, context, msg):
        if not isinstance(msg, TextMessage) or not msg.text.startswith(u'안녕'):
            return False

        self.reply_message(TextSendMessage(text=u'안녕하세요! {}님'.format(user.name)))

        return True
