# Fun in the Sun Challenge
from cmath import acos, pi
from numpy import dot, cross
from numpy.linalg import norm
from skyfield.api import load, wgs84
ts = load.timescale()

import os, sys
from time import sleep
from timeout import timeout, TimeoutError
time = int(os.getenv("TIMEOUT",90))

# Challenge Intro
def render_intro():
    art = [
        "            FUN                   ",
        "              IN                  ",
        "                THE               ",
        "                  SUN!!           ",
        "                                  ",
        "               y                  ",
        "              /              .    ",
        "           ////             <O>   ",
        "          ////o--z           '    ",
        "            |                     ",
        "            x                     ",
        " ",
        " "
    ]

    for row in art:
        print(row)
        sleep(0.05)
        sys.stdout.flush()
    
    return

def quaternion(u,v):
    u = u / norm(u)
    v = v / norm(v)

    q = [0,0,0,0]
    q[0:3] = cross(u,v)
    q[3] = 1 + dot(u,v)
    q = q / norm(q)
    return q

def vectorFromQuaternion(u,q):
    v = u + 2*q[3]*cross(q[0:3],u) + 2*(cross(q[0:3],cross(q[0:3],u)))
    return v

def angleBetweenVectors(u,v):
    angle = acos(dot(u,v)/(norm(u)*norm(v)))
    return angle.real

@timeout(time)
def challenge():
    # Load satellites
    sat = load.tle_file('sat.tle')
    #if sat: print("Loaded",len(sat),"TLE")
    #else: print("No TLEs :(")
    sat = sat[0]

    eph = load('de440s.bsp')
    sun, earth, mars = eph['Sun'], eph['Earth'], eph['Mars Barycenter']

    # Set simulation epoch
    # May 21, 2022, 14:00 UTC
    t = ts.utc(2022, 5, 21, 14, 0)

    # Challenge Question
    print("Provide the the quaternion (Qx, Qy, Qz, Qw) to point your spacecraft at the sun at",t.utc_strftime())
    print("The solar panels face the -X axis of the spacecraft body frame or [-1,0,0]")
    
    print("Qx = ",end='')
    x = float(input())
    print("Qy = ",end='')
    y = float(input())
    print("Qz = ",end='')
    z = float(input())
    print("Qw = ",end='')
    w = float(input())

    ansQ = [x, y, z, w]
    ansQ = ansQ / norm(ansQ)
    print("Quaternion normalized to:",ansQ)

    # Check answer
    bodyV = [-1,0,0] # -x axis is solar panels in sat body frame

    # TLE doesn't matter b/c this sat is so close to Earth relative to Earth-Sun distance
    # If it was farther away, need to convert the satellite geocentric coordinates (earth origin) to barycentric (sun origin)
    sunV = earth.at(t).observe(sun).position.km
    sunV = sunV / norm(sunV)
    #print(sunV)
    #sunQ = quaternion(bodyV,sunV)
    #print(sunQ)

    ansV = vectorFromQuaternion(bodyV,ansQ)
    angle = angleBetweenVectors(sunV,ansV) * 180/pi

    print("The solar panels are facing %.3f degrees away from the sun" %angle)
    # If pointed at sun within 1 degree, accept the answer
    if angle < 1:
        return 1

    return 0

if __name__ == "__main__":
    
    render_intro()

    # Challenge
    success = challenge()
    
    if success:
        print("You got it! Here's your flag:")
        flag = os.getenv('FLAG')
        print(flag)

    else:
        print("That didn't work, try again!")
