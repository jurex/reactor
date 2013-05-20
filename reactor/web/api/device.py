from reactor import log, component
from reactor.web.utils import JSONResponse
from bson import ObjectId
from flask import request, escape
#from rpgtracker.auth import login_required
import datetime

api = component.get('API')
app = api.app

@app.route('/device', methods=['GET'])
#@login_required
def select_devices():
    return JSONResponse('devices')

@app.route('/device', methods=['POST'])
#@login_required
def insert_device():
    # todo validation
    model = request.json
    return JSONResponse(model)
        
@app.route('/device/<id>', methods=['GET'])
#@login_required
def select_device(id):
    id = escape(id)
    model = request.json
    return JSONResponse(model)

@app.route('/device/<id>', methods=['PUT'])
#@login_required
def update_device(id):
    id = escape(id)
    model = request.json
    return JSONResponse(model)


@app.route('/device/<id>', methods=['DELETE'])
#@login_required
def delete_device(id):
    id = escape(id)
    model = request.json
    return JSONResponse(model)