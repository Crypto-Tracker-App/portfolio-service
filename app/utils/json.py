from flask import Response
import json

def json_response(data, status=200):
    return Response(json.dumps(data), status=status, mimetype='application/json')
