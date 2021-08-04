from flask import abort, request
import config

def check_key(request):
    if request.headers.get('Authorization') != config.secret_key:
    	return abort(403, description = "Unauthorized")