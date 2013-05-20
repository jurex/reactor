import sys, os, pymongo
from bson import json_util, ObjectId
from datetime import datetime
from flask import json, request, Response

_basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

class CustomEncoder(json.JSONEncoder):
    """A C{json.JSONEncoder} subclass to encode documents that have fields of
    type C{bson.objectid.ObjectId}, C{datetime.datetime}
    """
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        elif isinstance(obj, datetime):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)
    
def JSONResponse(data, status=200):
    
    if(data == None):
        return Response(json.dumps(dict(), cls=CustomEncoder), mimetype='application/json', status=404)
    
    if(isinstance(data, pymongo.cursor.Cursor)):
        docs = list()
        for d in data:
            docs.append(d)
        
        return Response(json.dumps(docs, cls=CustomEncoder), mimetype='application/json', status=status)
        
        
    return Response(json.dumps(data, cls=CustomEncoder), mimetype='application/json', status=status)