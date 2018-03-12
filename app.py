from flask import Flask, render_template, request, Response
from flask_socketio import SocketIO
from flask_socketio import emit
import mraa, time
import os, sys
from urllib import urlencode
from urllib2 import urlopen
import requests

app = Flask(__name__)
socketio = SocketIO(app)
disco_mode = False

pigtail=mraa.Gpio(10)
pigtail.dir(mraa.DIR_OUT)

towerColors={'framepair0':'k0r255g000b000m1t00500k1r022g039b197m1t00500', 'framepair1':'k2r062g231b092m1t00500k3r151g043b179m1t00500'}
towerUrl='http://atlas-tower.herokuapp.com/send'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/disco')
def disco():

    global disco_mode
    url = "http://192.168.20.66/servo/"
    if disco_mode:
        disco_mode = False
        msg = "off"
        url += "1"
        pigtail.write(0)
    else:
        disco_mode = True
        msg = "on"
        url += "0"
        pigtail.write(1)
        r=requests.get(towerUrl, params=towerColors)
    
    socketio.emit('update', {'msg':msg});

    try:
        content = urlopen(url=url)
        print("Success" + url)
    except:
        pass

    return str(disco_mode)

if __name__ == '__main__':
    #app.run(host='0.0.0.0')
    socketio.run(app)
