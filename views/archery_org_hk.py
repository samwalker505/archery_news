import logging
import common.micro_webapp2 as micro_webapp2
from common.constants import Error
from views import BaseView
app = micro_webapp2.WSGIApplication()
NOT_FOUND = 'ERROR_NOT_FOUND'
@app.route(r'/<:archery_org_hk.*>')
class ArcheryOrgHk(BaseView):

    def render(self, *args, **kwargs):
        post_id = self.request.get('post_id')
        if post_id:
            from models.post import ArcheryOrgHkPost
            post = ArcheryOrgHkPost.get_by_id(post_id)
            if post:
                self.values['post'] = post
            else:
                raise Exception(NOT_FOUND)
        else:
            raise Exception(NOT_FOUND)
