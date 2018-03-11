from flask import Flask, render_template, request, Response
from flask_socketio import SocketIO
from flask_socketio import emit
import mraa, time
import os, sys
from urllib.parse import urlencode
from urllib.request import urlopen


app = Flask(__name__)
socketio = SocketIO(app)
disco_mode = False

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
    else:
        disco_mode = True
        msg = "on"
        url += "0"
    
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
