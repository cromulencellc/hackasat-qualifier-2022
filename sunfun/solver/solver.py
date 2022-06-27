# SunFun Solver
import os, sys, socket

from cmath import acos, pi
from numpy import dot, cross
from numpy.linalg import norm
from skyfield.api import load, wgs84
ts = load.timescale()

def quaternion(u,v):
    u = u / norm(u)
    v = v / norm(v)

    q = [0,0,0,0]
    q[0:3] = cross(u,v)
    q[3] = 1 + dot(u,v)
    q = q / norm(q)
    return q

def solve():
    # Load satellites
    sat = load.tle_file('sat.tle')
    #if sat: print("Loaded",len(sat),"TLE")
    #else: print("No TLEs :(")
    sat = sat[0]

    eph = load('de440s.bsp')
    sun, earth = eph['Sun'], eph['Earth']

    # Set simulation epoch
    # May 21, 2022, 14:00 UTC
    t = ts.utc(2022, 5, 21, 14, 0)

    bodyV = [-1,0,0] # -x axis is solar panels in sat body frame

    # TLE doesn't matter b/c this sat is so close to Earth relative to Earth-Sun distance
    # If it was farther away, need to convert the satellite geocentric coordinates (earth origin) to barycentric (sun origin)
    sunV = earth.at(t).observe(sun).position.km
    sunV = sunV / norm(sunV)
    sunQ = quaternion(bodyV,sunV)
    
    return sunQ


if __name__ == "__main__":
    # get host from environment
    host = os.getenv("CHAL_HOST")
    if not host:
        print("No HOST supplied from environment")
        sys.exit(-1)

    # get port from environment
    port = int(os.getenv("CHAL_PORT","0"))
    if port == 0:
        print("No PORT supplied from environment")
        sys.exit(-1)

    # get ticket from environment
    ticket = os.getenv("TICKET")

    # connect to service
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
   
    # pass ticket to ticket-taker
    if ticket:
        prompt = s.recv(128)  # "Ticket please:"
        s.send((ticket + "\n").encode("utf-8"))

    # receive challenge
    i = 0
    while i < 14:
        challenge = s.recv(256)
        challenge = challenge.decode('UTF-8')
        print(challenge,end='')
        sys.stdout.flush
        i+=1

    # solve
    qAns = solve()

    for q in qAns:
        # provide response
        response = '%f\n' %q
        print(response,end='')
        s.send(response.encode("utf-8"))
        challenge = s.recv(256)
        challenge = challenge.decode('UTF-8')
        print(challenge,end='')
    
    # receive and print flag
    i = 0
    while (i <4):
        r = s.recv(256)
        print(r.decode('utf-8'),end='')
        i = i+1