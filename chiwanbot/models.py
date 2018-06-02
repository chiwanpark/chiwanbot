# -*- coding: utf-8 -*-

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
