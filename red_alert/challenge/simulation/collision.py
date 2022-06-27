import numpy as np
import collision 

def collisions( satellites , junk , dt , dist_allowed ):
    collisions = []
    for name,sat in satellites.items():
        for name2,junk in junk.items():
            poca = closest_approach( sat.get_state() , junk , dt )
            if( np.abs(poca) < dist_allowed ):
                collision = dict()
                collision["Sat"] = name
                collision["Junk"] = name2
                collision["POCA"] = poca
                collisions.append( collision )
    return collisions

def closest_approach( object1 , object2 , dt ):
    # this expects skyfield objects 
    p1 = object1.position.km
    p2 = object2.position.km 
    v1 = object1.velocity.km_per_s
    v2 = object2.velocity.km_per_s
    # Convert the position and velocity to relative reference frame fixed at p2
    dP1 = p1-p2
    dV = v1 - v2
    # For a small enough time this is accurate
    dP2 = dP1 + ( dV * dt )
    
    alpha = np.arccos( np.dot( dP1 , dV )/ ( np.linalg.norm( dP1 ) * np.linalg.norm( dV) )) 
    beta = np.arccos( np.dot( dP2 , dV )/ ( np.linalg.norm( dP2 ) * np.linalg.norm( dV) )) 
    if( (alpha > np.pi/2  )):
        # Closest approach occurs at dP1
        poca = np.linalg.norm( dP1 )
    elif( beta > np.pi/2 ):
        # Closest approach occurs at dP2
        poca = np.linalg.norm( dP2 ) 
    else:
        # closest approach occurs betweent the two points
        poca = np.linalg.norm( dP1 ) * np.sin( alpha )
    return poca 