import subprocess
import numpy as np
import time
import pmt
import zmq

from numpy.linalg import norm
from skyfield.api import load, wgs84
ts = load.timescale()

sat = load.tle_file('sat.tle')
sat = sat[0]
gnd = wgs84.latlon(28.079, -80.6092, 0)
tArray = ts.utc(2022, 5, 21, 14, 9, np.arange(740,740+600,1)/10)

distance = []
doppler = []
pathLoss = []
prevDistance=0

for t in tArray:
  satPos = sat.at(t).position.km
  gndPos = gnd.at(t).position.km
  distance.append(norm(satPos - gndPos))
  pathLoss.append(1e13*(0.33/(4*3.14*(distance[-1]*1000)))**2)
  if len(distance)>1:
    doppler.append((distance[-2]-distance[-1])/0.1*1000)

#print("Range:",distance)
#print("Path Loss:",pathLoss)
#print("Doppler:",doppler)


context = zmq.Context()
dopplerSocket = context.socket(zmq.PUB)
dopplerSocket.bind("tcp://127.0.0.1:5555")

pathLossSocket = context.socket(zmq.PUB)
pathLossSocket.bind("tcp://127.0.0.1:5556")

print("Turning on receiver")
p = subprocess.Popen(['python3', 'doppler.py'])

print("Receiving signal (should take ~1 minute)")
i=0
while(i<len(doppler)):
  msg = pmt.cons(pmt.intern("freq"), pmt.from_double(doppler[i]))
  sb = pmt.serialize_str(msg)
  dopplerSocket.send(sb)
  
  msg = pmt.cons(pmt.intern("freq"), pmt.from_double(pathLoss[i]))
  sb = pmt.serialize_str(msg)
  pathLossSocket.send(sb)
  #pathLoss = pathLoss + .00001

  i=i+1
  time.sleep(0.01)