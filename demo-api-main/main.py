from flask import Flask, request, jsonify, Response
from flask_restful import Resource, Api
import os, requests, socket, json, yaml, logging
import dlp
from google.cloud import dlp_v2
from google.api_core.exceptions import GoogleAPICallError, InvalidArgument
# from dlp import _get_crypto_replace_ffx_config, _get_infotype_transformations

print("Entering main.py...")

# === Endpoints ===
# This is a dictionary of endpoints that are available in the API
ENDPOINTS = {
        'endpoint1':'/',
        'endpoint2':'/serverinfo',
        'endpoint3':'/dlp-inspect',
        'endpoint4':'/dlp-deidentify',
        'endpoint5':'/dlp-reidentify'
    }

# Load config
config_filename = "config/config.yaml"
with open(config_filename, "r") as config_file:
    config = yaml.load(config_file.read(), Loader=yaml.FullLoader)

GCP_PROJECT = os.environ.get('GCP_PROJECT')
GCP_LOGGING_LEVEL = os.environ.get('GCP_LOGGING_LEVEL')

# Configure the basic logging level per the config
logging.basicConfig(level=int(GCP_LOGGING_LEVEL))

# Create an instance of Flask
app = Flask(__name__)

# Create the API
api = Api(app)

class HelloFLASK(Resource):
    def get(self):
        data = {
            'name': config['app']['name'],
            'description': config['app']['description'],
            'version': config['app']['version'],
            'author': config['app']['author'],
            'endpoints': ENDPOINTS
        }
        try:
            data['user'] = os.getlogin()
        except Exception as e:
            data['user'] = "Unknown"
            logging.warning("Error getting user: {}".format(e))

        try:
            data['ip'] = socket.gethostbyname(socket.gethostname())
        except Exception as e:
            data['ip'] = "Unknown"
            logging.warning("Error getting IP: {}".format(e))

        response = Response()
        response = jsonify(data)
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
    def post(self):
        some_json = request.get_json()
        return {'you sent': some_json}, 201

class GetEnv(Resource):
    def get(self):
        data = {}
        for key,value in os.environ.items():
            data[key] = value
        response = Response()
        response = jsonify(data)
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

class GetServerInfo(Resource):
    def get(self):
        # Initialize the data dictionary
        data = {}
        try:
            data['os_information'] = os.uname()
        except Exception as e:
            data['os_information'] = "Unknown"
            logging.warning("Error getting os_information: {}".format(e))

        try:
            data['user'] = os.getlogin()
        except Exception as e:
            data['user'] = "Unknown"
            logging.warning("Error getting user: {}".format(e))

        try:
            data['terminal'] = os.ctermid()
        except Exception as e:
            data['terminal'] = "Unknown"
            logging.warning("Error getting terminal: {}".format(e))

        try:
            data['cpu'] = os.ctermid()
        except Exception as e:
            data['cpu'] = "Unknown"
            logging.warning("Error getting CPU: {}".format(e))

        try:
            data['external_ip'] = str(requests.get("http://wtfismyip.com/text").text)
        except Exception as e:
            data['external_ip'] = "Unknown"
            logging.warning("Error getting External IP: {}".format(e))

        try:
            data['internal_ip'] = socket.gethostbyname(socket.gethostname())
        except Exception as e:
            data['internal_ip'] = "Unknown"
            logging.warning("Error getting Internal IP: {}".format(e))

        response = Response()
        response = jsonify(data)
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response


# DLP Inspection
class DLPInspect(Resource):
    def post(self):
        """
        Receives JSON, inspects specified infoTypes using FFX, returns JSON.
        """
        data = {
            "findings": [],
            'message': "",
            'http_status_code': 200
        }

        output = dlp.inspect_text(request.data)
        data['findings'] = output['findings']
        data['message'] = output['message']
        data['http_status_code'] = output['http_status_code']
        
        # # Prep the response object to be sent back to the caller
        response = Response()
        response = jsonify(data)
        response.status_code = data['http_status_code']
        return response

# DLP De-Identification
class DLPDeIdentify(Resource):
    def post(self):
        """
        Receives JSON, de-identifies specified infoTypes using FFX, returns JSON.
        """
        data = {
            "deidentified_text": "",
            'message': "",
            'http_status_code': 200
        }

        output = dlp.deidentify_data(request.data)
        data['deidentified_text'] = output['deidentified_text']
        data['message'] = output['message']
        data['http_status_code'] = output['http_status_code']
        
        # # Prep the response object to be sent back to the caller
        response = Response()
        response = jsonify(data)
        response.status_code = data['http_status_code']
        return response

        
# === Re-Identification Endpoint (Function B) ===
class DLPReIdentify(Resource):
    def post(self):
        """
        Receives JSON, de-identifies specified infoTypes using FFX, returns JSON.
        """
        data = {
            "reidentified_text": "",
            'message': "",
            'http_status_code': 200
        }

        output = dlp.reidentify_data(request.data)
        data['reidentified_text'] = output['reidentified_text']
        data['message'] = output['message']
        data['http_status_code'] = output['http_status_code']
        
        # # Prep the response object to be sent back to the caller
        response = Response()
        response = jsonify(data)
        response.status_code = data['http_status_code']
        return response



api.add_resource(HelloFLASK, '/')
api.add_resource(GetEnv, '/getenv')
api.add_resource(GetServerInfo, '/serverinfo')
api.add_resource(DLPInspect, '/dlp-inspect')
api.add_resource(DLPDeIdentify, '/dlp-deidentify')
api.add_resource(DLPReIdentify, '/dlp-reidentify')

# app name
@app.errorhandler(404)
# inbuilt function which takes error as parameter
def not_found(e):  
# defining function
    data = {
        'user_message': "Invalid URL. See valid endpoints for the URL, and proceed.",
        'endpoints': ENDPOINTS
    }
    response = Response()
    response = jsonify(data)
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.status_code = 404
    return response

if __name__ == "__main__":
    port="80"
    print("Starting api-template Flask API on Port {}...".format(port))
    app.run(debug=True, host='0.0.0.0',port=port)