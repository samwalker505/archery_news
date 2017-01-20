from datetime import datetime
from google.appengine.ext import ndb
from google.appengine.datastore.datastore_query import Cursor
import json

class JSONEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        elif isinstance(o, ndb.Key):
            return o.id()

        elif isinstance(o, Cursor):
            return o.to_websafe_string()

        return json.JSONEncoder.default(self, o)
