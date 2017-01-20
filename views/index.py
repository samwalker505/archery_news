import logging
import common.micro_webapp2 as micro_webapp2
from common.constants import Error
from views import BaseView
app = micro_webapp2.WSGIApplication()

@app.route(r'/<:.*>')
class Index(BaseView):
    pass
