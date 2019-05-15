from flask import Flask
from flask import jsonify
from flask import request

import serverManager

#These were implemented straight into thermostat.py, so we just had 
#this file for extra reference, most likely none of this was used. 
 
import argparse#used to set password to make HTTP request secure
server = Flask('RPi Temperature Set Server')

@server.route('/setTemp',methods=['POST'])
def set_temp_callback():
    payload = request.get_json()
    print(payload)
    server_manager.set_temp(payload)
    response = {'Response': 'TempReceived'}
    return json.dumps(response)

def server_init():
    server_manager = serverManager.serverManager()
    server.run(debug=False,host = '0.0.0.0', port=4250)
if __name__=='__main__':
    server_init()
