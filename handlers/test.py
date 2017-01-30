#!/usr/bin/python
# -*- coding: utf-8 -*-
import webapp2
import logging
from handlers import BaseHandler, Output
from external_api.facebook import Facebook as FacebookApi

class TestHandler(BaseHandler):
    @Output.json
    def get(self, *args, **kwargs):
        post_id = '0164613667c60cc6199b7fea56af024e:d41d8cd98f00b204e9800998ecf8427e'
        from models.post import ArcheryOrgHkPost
        post = ArcheryOrgHkPost.get_by_id(post_id)
        post_content = []
        title = post.title or ''
        content = post.content or ''
        tag_arr = [u'#{}'.format(tag) for tag in post.tags]
        tags = u' '.join(tag_arr)
        if title:
            post_content.append(title)
        if content:
            post_content.append(content)
        if tags:
            post_content.append(tags)
        post_fb_content = u'\n'.join(post_content)
        logging.debug('entered')
        client = FacebookApi()
        link = '{}/archery_org_hk?post_id={}'.format(self.request.host_url, post_id)
        result = client.create_post(post_fb_content, link=link)
        logging.debug(result)
        logging.debug(result.content)
        logging.debug(result.status_code)
        return {'result': result.content}

app = webapp2.WSGIApplication([
    (r'/api/v1/test', TestHandler),
])
