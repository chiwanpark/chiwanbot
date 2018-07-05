# -*- coding: utf-8 -*-

import importlib
import os


class PluginMount(type):
    def __init__(cls, name, bases, attrs):
        if not hasattr(cls, 'plugins'):
            cls.plugins = []
        else:
            cls.plugins.append(cls)

    @classmethod
    def load_plugins(cls):
        plugin_dir = os.path.dirname(__file__)
        for file_name in os.listdir(plugin_dir):
            if file_name.startswith('_'):
                continue
            module_name = file_name.split('.')[0]
            importlib.import_module('chiwanbot.plugins.{}'.format(module_name))


class ChatPlugin(object):
    __metaclass__ = PluginMount

    def __init__(self, line_api, reply_token=None):
        self._line_api = line_api
        self._reply_token = reply_token

    def push_message(self, user, msg):
        self._line_api.push_message(user.key.string_id(), msg)

    def reply_message(self, msg):
        self._line_api.reply_message(self._reply_token, msg)

    def callback_msg(self, user, context, msg):
        return False

    def callback_cron(self):
        return False
