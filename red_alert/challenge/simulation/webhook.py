from flask import Flask,request,jsonify
import sim 
import threading
import satellite 
import sys
import logging
import os
import time
app = Flask(__name__)
sim_app = sim.SimApp()
log = logging.getLogger('werkzeug')
log.disabled = True


mutex = threading.Lock()

def run_webhook():
    mutex.acquire()
    app.run(host="0.0.0.0", port=5000 , debug=False )



@app.route('/')
def hello():
    print("HELLO")
    return "Received!"

@app.route('/detector-on', methods=['POST'])
def detector_on():
    print("API Command: Detector ON")
    sim_app.handle_hook("detector", True)
    data = request.json
    return data
@app.route('/detector-off', methods=["POST"])
def detector_off():
    print("API Command: Detector OFF")
    sim_app.handle_hook("detector", False)
    data = request.json
    return data

@app.route('/laser-off', methods=["POST"])
def laser_off():
    print("API Command: Laser OFF")
    sim_app.handle_hook("laser", False)
    data = request.json
    return data

@app.route('/laser-on', methods=["POST"])
def laser_on():
    print("API Command: Laser ON")
    sim_app.handle_hook("laser", True)
    data = request.json
    return data
@app.route('/play', methods=["POST"])
def play():
    mutex.release()
    data = request.json
    return data
if __name__ == '__main__':


    t = threading.Thread( target = run_webhook )
    t.setDaemon(True)
    t.start()
    print("Use the API to start the mission!", flush=True)
    try:
        flag = os.getenv("FLAG", "flag{TestFlagMcTestFlag}")
        mutex.acquire( )
        print("MISSION STARTING")
        sim_app.run_sim( flag )
        time.sleep(20)
    except (satellite.DestructionError , satellite.PowerError, satellite.HeatError) :
        print("MISSION FAILED")
        print("Leaving network up for a little while.")
        time.sleep(300)
    print("Exiting")
    sys.exit(0)