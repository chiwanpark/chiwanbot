# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from google.appengine.ext import ndb

class Config(ndb.Model):
    value = ndb.StringProperty(required=True)

    config_caches = {}

    @classmethod
    def get_by_name(cls, name):
        if name not in cls.config_caches:
            key = ndb.Key(Config, name)
            record = key.get()
            if record is None:
                return None
            else:
                cls.config_caches[name] = record.value
        return cls.config_caches[name]


class User(ndb.Model):
    name = ndb.StringProperty(required=True)

    permission = ndb.IntegerProperty(default=5)
    state = ndb.StringProperty(default='init')

    last_updated = ndb.DateTimeProperty(auto_now=True)
    last_profile_updated = ndb.DateTimeProperty(auto_now_add=True)

    def is_valid_profile(self):
        # TODO: valid time range of profile should be configurable
        return datetime.now() - self.last_profile_updated < timedelta(days=14)
