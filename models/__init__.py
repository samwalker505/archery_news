#!/usr/bin/python
# -*- coding: utf-8 -*-
from google.appengine.ext import ndb

class ToDict(ndb.Model):

    FOR_PUBLIC = 10
    FOR_OWNER = 50
    FOR_ADMIN = 100

    def to_dict_by_level(self, level):
        return self.to_dict()
    def to_dict_for_public(self):
        return self.to_dict_by_level(ToDict.FOR_PUBLIC)
    def to_dict_for_owner(self):
        return self.to_dict_by_level(ToDict.FOR_OWNER)
    def to_dict_for_admin(self):
        return self.to_dict_by_level(ToDict.FOR_ADMIN)



class BaseModel(ToDict):
    create_time = ndb.DateTimeProperty(auto_now_add=True)
    update_time = ndb.DateTimeProperty(auto_now=True)
    deleted = ndb.BooleanProperty(default=False)

    @classmethod
    def create(cls, create_dict):
        instance = cls(**create_dict)
        instance.put()
        return instance

    def update(self, update_dict):
        for key, val in update_dict.iteritems():
            if key in self.__class__._properties:
                setattr(self, key, val)
                self.put()
        return self

    def delete(self, is_mark_deleted=True):
        if is_mark_deleted:
            self.deleted = True
            self.put()
        else:
            self.key.delete()
