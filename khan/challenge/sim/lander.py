import os
from Basilisk.simulation import spacecraft, dragDynamicEffector, exponentialAtmosphere
from Basilisk.utilities import (SimulationBaseClass, macros, orbitalMotion,
                                simIncludeGravBody, unitTestSupport, vizSupport)
from Basilisk.simulation import extForceTorque

from Basilisk.architecture import messaging
from Basilisk import __path__
import matplotlib.pyplot as plt
from . import Parachute
from . import HeatShield
from . import Thruster
from . import Surface
from . import fswInterface
from . import plots
bskPath = __path__[0]
fileName = os.path.basename(os.path.splitext(__file__)[0])

def run():
    simulationTime = macros.sec2nano(5*3600.0)

    #####  Create a sim module
    sim = SimulationBaseClass.SimBaseClass()
    sim.SetProgressBar(True)
    ##### Setup processes and tasks 
    # Process for all C++ things
    physicsProcessName = "PhysicsProcess"
    environmentTaskName = "EnvTask"
    physicsDt = macros.sec2nano(0.1)
    dataDt = macros.sec2nano(1)
    physicsProcess = sim.CreateNewProcess(physicsProcessName , priority=20 )
    physicsProcess.addTask(sim.CreateNewTask(environmentTaskName, physicsDt))
    # Create a process for Python things
    inProcessName = "InputProcess"
    inTaskName = "InputTask"
    inProcess = sim.CreateNewPythonProcess(inProcessName , priority=1)
    inProcess.createPythonTask(inTaskName, dataDt, True, 10)
    outProcessName = "OutputProcess"
    outTaskName = "OutputTask"
    outProcess = sim.CreateNewPythonProcess(outProcessName , priority=10)
    outProcess.createPythonTask(outTaskName, dataDt, True, 1)
    # Make a spacecraft model
    probe = spacecraft.Spacecraft()
    probe.ModelTag = "genisis"
    
    #
    #   Setup data logging before the simulation is initialized

    nData = 10000
    samplingTime = unitTestSupport.samplingTime(simulationTime, physicsDt, nData)
    dataRec = probe.scStateOutMsg.recorder(samplingTime)
    
    


    # Make a gravity model
    gravFactory = simIncludeGravBody.gravBodyFactory()
    # mu is in meters^3/ s^2
    planet = gravFactory.createCustomGravObject( label="Seti-Beta-VII",
                                                 mu =2527105126400000.0,
                                                 radiusRatio = 1.0,
                                                 radEquator = 13120.0e3,
                                                 displayName="Seti-Beta-VII"   )
    planet.isCentralBody = True
    probe.gravField.gravBodies = spacecraft.GravBodyVector(list(gravFactory.gravBodies.values()))
    ## Make an atomosphere model
    atmosphere = exponentialAtmosphere.ExponentialAtmosphere()
    atmosphere.ModelTag = "Atmosphere"
    atmosphere.addSpacecraftToModel(probe.scStateOutMsg)
    atmosphere.planetRadius =  planet.radEquator 
    atmosphere.scaleHeight = 8500.0
    atmosphere.baseDensity = 1.217
    
    navInterface = fswInterface.NavIntrface(5001, "NavInterface")
    thrusterInterface = fswInterface.EngineInterface( 5000 , "EngineInterface")
    extFTObject = extForceTorque.ExtForceTorque()
    extFTObject.ModelTag = "externalDisturbance"
    probe.addDynamicEffector(extFTObject)
    

    ## Make a drag model 
    Cd = .1
    A = 1 
    dragEffector = dragDynamicEffector.DragDynamicEffector()
    dragEffector.ModelTag = "DragEff"
    dragEffector.coreParams.projectedArea = A
    dragEffector.coreParams.dragCoeff = Cd
    dragEffector.coreParams.comOffset = [0., 0., 0.]
    probe.addDynamicEffector(dragEffector)
    ## Make a drag model for the parachute
    parachuteEffector = dragDynamicEffector.DragDynamicEffector()
    parachuteEffector.ModelTag = "ChuteDragEff"
    parachuteEffector.coreParams.projectedArea = 0
    parachuteEffector.coreParams.dragCoeff = .1
    parachuteEffector.coreParams.comOffset = [0., 0., 0.]
    probe.addDynamicEffector(parachuteEffector)
    
    
    chuteCharge = Parachute.Parachute( parachuteEffector,  "Chute")
    heatShield = HeatShield.HeatShield( "HeatShield" )
    thruster = Thruster.Thruster( "Thruster")
    surface = Surface.Surface( planet, "PlanetSurface ")

    ##### Add all the models to tasks
    
    ## add input models to highest priority task
    inProcess.addModelToTask( inTaskName, thrusterInterface )
    inProcess.addModelToTask(inTaskName , thruster )
    inProcess.addModelToTask( inTaskName, chuteCharge )
    ## add c++ models to middle priroity task
    sim.AddModelToTask(environmentTaskName, atmosphere)
    sim.AddModelToTask(environmentTaskName , parachuteEffector)
    sim.AddModelToTask(environmentTaskName , dragEffector)
    sim.AddModelToTask(environmentTaskName, extFTObject)
    sim.AddModelToTask(environmentTaskName, probe)
    sim.AddModelToTask(environmentTaskName, dataRec)
    ## add output models to lowest priority task
    outProcess.addModelToTask( outTaskName , heatShield)
    outProcess.addModelToTask( outTaskName, surface )
    outProcess.addModelToTask( outTaskName, navInterface )
    ## Setup initial conditions - lets make this really easy
    altitude = 300e3
    mu = planet.mu 
    oe = orbitalMotion.ClassicElements()
    
    oe.a = planet.radEquator  + altitude
    oe.e = 0.01
    oe.i = 0.0
    oe.Omega = 1.0 # Radians
    oe.omega = 0.0 # Radians 
    oe.f = 0.01 # Radians
    rN, vN = orbitalMotion.elem2rv(mu, oe)
    probe.hub.r_CN_NInit = rN  # m   - r_BN_N
    probe.hub.v_CN_NInit = vN  # m/s - v_BN_N

    # Connect up the messaging
    dragEffector.atmoDensInMsg.subscribeTo(atmosphere.envOutMsgs[-1])
    parachuteEffector.atmoDensInMsg.subscribeTo(atmosphere.envOutMsgs[-1])
    surface.pvtMsg.subscribeTo(probe.scStateOutMsg)
    chuteCharge.popMsg.subscribeTo( thrusterInterface.chuteCmdMsg )
    chuteCharge.pvtMsg.subscribeTo( probe.scStateOutMsg )
    heatShield.popMsg.subscribeTo( thrusterInterface.shieldCmdMsg )
    heatShield.pvtMsg.subscribeTo( probe.scStateOutMsg )
    heatShield.atmMsg.subscribeTo(atmosphere.envOutMsgs[-1])
    thruster.inForceMsg.subscribeTo(thrusterInterface.forceCmdMsg)   
    extFTObject.cmdForceInertialInMsg.subscribeTo(thruster.outForceMsg)
    navInterface.inMsg.subscribeTo( probe.scStateOutMsg )
    # Setup Recording
    dataRec2 = thrusterInterface.chuteCmdMsg.recorder(samplingTime)
    dataRec3 = thrusterInterface.shieldCmdMsg.recorder(samplingTime)
    sim.AddModelToTask(environmentTaskName, dataRec2)
    # Run everything

    sim.InitializeSimulation()
    sim.ConfigureStopTime(simulationTime)
    try:
        bus = "OK"
        sim.ExecuteSimulation()
    except Surface.Landing:

        return True
    except HeatShield.BurnUpError:
        bus = "VAPORIZED"
    except  Surface.ImpactError:
        bus = "SMASHED"
    plots.position( dataRec.times() ,  dataRec.r_BN_N )
    plots.velocity( dataRec.times() ,  dataRec.v_BN_N )
    plots.g_sensor( dataRec.times() ,  dataRec.nonConservativeAccelpntB_B  )
    plots.accel( dataRec.times() ,  dataRec.nonConservativeAccelpntB_B   )
    plots.commands( dataRec2.times() , dataRec2.deviceCmd , dataRec3.times() , dataRec3.deviceCmd  )
    plots.dmg(  thruster.status() , chuteCharge.status() ,bus )
    return False
if __name__ == "__main__":
    run()