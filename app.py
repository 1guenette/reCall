from flask import Flask, jsonify, send_from_directory, send_file, request
import freeclimb
import os
from freeclimb.api import default_api
import requests
from requests.auth import HTTPBasicAuth
import time
import json
from flask_caching import Cache



config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 1
}

ACCOUNT_ID = os.environ.get('ACCOUNT_ID')
API_KEY = os.environ.get('API_KEY')
APP_ID=os.environ.get('APP_ID')
SRC_URL=os.environ.get('SRC_URL')
FC_NUMBER = os.environ.get('FC_NUMBER')
FC_URL = os.environ.get('FC_URL')
recording_percl = [
   {
      "Play" : {
         "file" : SRC_URL + "/happy_dude",
         "loop" : 1
      }
   }
]

app = Flask(__name__)
app.config["CACHE_TYPE"] = "null"
app.config.from_mapping(config)
cache = Cache(app)

counter = 0



@app.route('/voice', methods=['GET', 'POST'])
def api_endpoint(req):
    print(req)
    data = {'message': 'Hello, World!'}
    return jsonify(recording_percl)

@app.route('/start_call', methods=['GET', 'POST'])
def start_call():
    print('Starting outgoing call campaign...')
    make_outgoing_call( request.args.get('target'))
    data = {'message': 'Persistant sales pitch started'}
    return jsonify(data)


def make_outgoing_call(target):
    try:
        print("XXXXX")
        print(target)

        url = FC_URL + '/Accounts/' + ACCOUNT_ID + '/Calls'
        data = {
            'applicationId': APP_ID,
            'to': '+' + target,
            'from': FC_NUMBER,
            'callConnectUrl': SRC_URL + '/play_recording'
        }
        headers = { 'Content-Type': 'application/json', 'Cache-Control': 'no-cache', "Pragma": "no-cache"}
        auth = HTTPBasicAuth(ACCOUNT_ID, API_KEY)
        response = requests.post(url, json=data, headers=headers, auth=auth)
        print('Outgoing call initiated successfully.')
    except Exception as ex:
        print('Error making outgoing call:', ex)


@app.route('/callback', methods=['POST', 'GET'])
def on_call_disconnect():
    
    time.sleep(2)
    make_outgoing_call(request.json.get('to')[1:])
    print("Recalling possible customer")
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

@app.route('/play_recording', methods=['POST'])
def play_recording():
    print('RECORDING PERCL')
    return jsonify(recording_percl)

@app.route('/happy_dude', methods=['POST', 'GET'])
def happy_dude():
    response =  send_file('./recordings/happy_dude.wav',  as_attachment=False)
    response.headers['Cache-Control'] = 'no-cache, no-store'
    response.headers['Expires'] = '0'
    response.headers['Pragma'] = 'no-cache'
    return response

if __name__ == '__main__':
    app.run(port=3001)