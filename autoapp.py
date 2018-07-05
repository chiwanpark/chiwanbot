# -*- coding: utf-8 -*-

from chiwanbot.app import create_app
from chiwanbot.plugins import ChatPlugin

app = create_app()
ChatPlugin.load_plugins()
