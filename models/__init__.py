from google.appengine.ext import ndb

class BaseModel(ndb.Model):
    create_time = ndb.DateTimeProperty(auto_now_add=True)
    update_time = ndb.DateTimeProperty(auto_now=True)
    mark_deleted = ndb.BooleanProperty(default=False)

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
            self.mark_deleted = True
        else:
            self.key.delete()

    def to_dict(self, include=None, exclude=None):
        d = super(BaseModel, self).to_dict(include=include, exclude=exclude)
        d['uid'] = self.key.id()
        del d['mark_deleted']
        return d
