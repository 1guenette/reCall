from flask import Flask, jsonify, send_from_directory, send_file
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

def increment():
    global counter
    counter = counter + 1
    print(counter)

@app.route('/voice', methods=['GET', 'POST'])
def api_endpoint(req):
    print(req)
    data = {'message': 'Hello, World!'}
    return jsonify(recording_percl)

@app.route('/start_call', methods=['GET', 'POST'])
def start_call():
    print('Starting outgoing call campaign...')
    make_outgoing_call()
    data = {'message': 'Persistant sales pitch started'}
    return jsonify(data)


def make_outgoing_call():
    try:
        url = FC_URL + '/Accounts/' + ACCOUNT_ID + '/Calls'
        data = {
            'applicationId': APP_ID,
            'to': '+13128063546',
            'from': FC_NUMBER,
            'timeout': 15,
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
    make_outgoing_call()
    print("Recalling possible customer")
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

@app.route('/play_recording', methods=['POST'])
def play_recording():
    print('RECORDING PERCL')
    return jsonify(recording_percl)

@app.route('/happy_dude', methods=['POST', 'GET'])
def happy_dude():
    increment()
    # if counter%2 == 0:
    response =  send_file('./recordings/happy_dude.wav',  as_attachment=False)
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response
    # else:
    #     response = send_file('./recordings/happy_dude_2.wav',  as_attachment=False)
    #     response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    #     response.headers['Pragma'] = 'no-cache'
    #     response.headers['Expires'] = '0'
    #     return response

if __name__ == '__main__':
    app.run(port=3001)