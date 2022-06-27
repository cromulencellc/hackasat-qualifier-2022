import matplotlib.pyplot as plt
from Basilisk.utilities import (SimulationBaseClass, macros, orbitalMotion,
                                simIncludeGravBody, unitTestSupport, vizSupport)

import numpy as np
def position( time , position  ):
    plt.figure(1)
    fig = plt.gcf()
    ax = fig.gca()
    ax.ticklabel_format(useOffset=False, style='plain')
    plt.plot( time* macros.NANO2SEC / 3600  , position / ( ( 1000.0 * 1.60934))  )
    plt.xlabel('Time [hrs]')
    plt.ylabel('Position')
    plt.savefig("static/position.png")
def velocity( time , velocity ):
    plt.figure(2)
    fig = plt.gcf()
    ax = fig.gca()
    ax.ticklabel_format(useOffset=False, style='plain')
    plt.plot( time* macros.NANO2SEC / 3600 , velocity /  ( 1000.0 * 1.60934) )
    plt.xlabel('time [hrs]')
    plt.ylabel('Velocity')
    plt.savefig("static/velocity.png")
def g_sensor( time , data   ):
    plt.figure(3)
    fig = plt.gcf()
    ax = fig.gca()
    ax.ticklabel_format(useOffset=False, style='plain')
    linear  = - np.linalg.norm( data , axis=1)
    plt.plot( time* macros.NANO2SEC / 3600  , linear )
    plt.xlabel('Time [hrs]')
    plt.ylabel('G-Sensor')
    plt.savefig("static/gsensor.png")
def accel(time , data   ):
    plt.figure(4)
    fig = plt.gcf()
    ax = fig.gca()
    ax.ticklabel_format(useOffset=False, style='plain')
    plt.plot( time* macros.NANO2SEC / 3600  , data )
    plt.xlabel('Time [hrs]')
    plt.ylabel('Three Axis Accelerometer')
    plt.savefig("static/accel.png")
def commands( time , parachute , time2, shield ):
    plt.figure(5)
    fig = plt.gcf()
    ax = fig.gca()
    ax.ticklabel_format(useOffset=False, style='plain')
    plt.plot( time* macros.NANO2SEC / 3600  , parachute )
    plt.plot( time2* macros.NANO2SEC / 3600 , shield )
    plt.xlabel('Time [hrs]')
    plt.ylabel('Commands')
    plt.legend(['Parachute Command', 'Heat Shield Command'])
    plt.savefig("static/commands.png")
    
def dmg( fuel , chute  , sat_bus):
    rows = ["Fuel Tank", "Parachute" , "Satellite Bus"]
    cols = ["Status"]
    cells = [[fuel] , [chute] , [sat_bus] ]
    plt.figure(6)
    fig = plt.gcf()
    ax = fig.gca()
    ax.set_axis_off()
    ax.table( cellText = cells , rowLabels=rows , colLabels=cols , 
              rowColours=["palegreen"]*3 , colColours=["palegreen"]*1, 
              cellLoc='center',)
    plt.savefig("static/dmg.png")