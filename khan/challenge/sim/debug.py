import matplotlib.pyplot as plt
from Basilisk.utilities import (SimulationBaseClass, macros, orbitalMotion,
                                simIncludeGravBody, unitTestSupport, vizSupport)

import numpy as np
def make_plots( time , position , velocity ):
    plt.figure(1)
    fig = plt.gcf()
    ax = fig.gca()
    ax.ticklabel_format(useOffset=False, style='plain')


    plt.plot( time* macros.NANO2SEC / 3600  m position )
    plt.xlabel('Time [hrs]')
    plt.ylabel('Position')
    plt.savefig("position.png")
def velocity( time , velocity ):
    plt.figure(1)
    fig = plt.gcf()
    ax = fig.gca()
    ax.ticklabel_format(useOffset=False, style='plain')

    plt.plot( time* macros.NANO2SEC / 3600 , velocity )
    plt.xlabel('time [hrs]')
    plt.ylabel('velocity')
def moar( time , data   ):
    plt.figure(2)
    fig = plt.gcf()
    ax = fig.gca()
    ax.ticklabel_format(useOffset=False, style='plain')
    plt.plot( time* macros.NANO2SEC / 3600  , data )
    plt.xlabel('Time [hrs]')
    plt.ylabel('Force [N]')
    plt.show()