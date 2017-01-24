#!/usr/bin/python
# -*- coding: utf-8 -*-
from google.appengine.ext import ndb
import logging
from models import BaseModel
from google.appengine.ext.ndb import polymodel
class Post(polymodel.PolyModel, BaseModel):
    url = ndb.StringProperty()
    content = ndb.TextProperty()
    tags = ndb.StringProperty(repeated=True)
    content_hash = ndb.StringProperty()
    url_hash = ndb.StringProperty()

    @classmethod
    def create(cls, params):
        model = cls._create(params)
        model.put()
        return model

    @classmethod
    def _create(cls, params):
        model = cls()
        model._update(params)
        return model

    @ndb.transactional(retries=10)
    def update(self, params):
        self._update(params)
        self.put()
        return self

    def _update(self, params):
        update_dict = {}
        keys = ['url', 'content', 'content_hash', 'url_hash']
        for key in keys:
            if key in params:
                update_dict[key] = params[key]

        if 'tags' in params and params['tags']:
            self.tags.extend(params['tags'])

        self.populate(**update_dict)



class ArcheryOrgHkPost(Post):

    @classmethod
    def _create_from_spider(cls, params):
        if 'url_hash' not in params or 'content_hash' not in params:
            # TODO: throw proper exception
            raise Exception('ERROR_NO_HASH')
        url_hash = params['url_hash']
        content_hash = params['content_hash']
        post = cls(id='{}:{}'.format(url_hash, content_hash))
        post._update(params)
        return post

    @classmethod
    def create_from_spider_batch(cls, params_arr):
        logging.debug('create_from_spider_batch: {}'.format(len(params_arr)))
        posts = []
        for params in params_arr:
            post = cls._create_from_spider(params)
            posts.append(post)
        ndb.put_multi(posts)
        return posts
