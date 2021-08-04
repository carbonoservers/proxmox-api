# Configuration
import config

# Flask and other
import logging
from flask import Flask, jsonify

app = Flask(__name__)
#logging.basicConfig(level=logging.DEBUG)
# Forbidden error (403)
@app.errorhandler(403)
def forbidden_error(e):
    return jsonify(error = 403, message = str(e)), 403

# Not found error (404)
@app.errorhandler(404)
def page_not_found(e):
    return jsonify(error = 404, message = str(e)), 404

# Server error (500)
@app.errorhandler(500)
def internal_server_error(e):
    return jsonify(error = 500, message = str(e)), 500

# VM control
from vm_control.views import vm_control
app.register_blueprint(vm_control)

# Intialize Flask App
if __name__ == '__main__':
    app.run(host = config.host, port = config.port, debug = config.debug)