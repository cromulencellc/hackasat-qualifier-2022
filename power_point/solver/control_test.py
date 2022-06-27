import control 
import matplotlib.pyplot as plt
import numpy as np 
class power_model:
    def __init__( self, max_power , width , center ):
        self.p = max_power
        self.w = width
        self.c = center
    def get_power(self,  x , count):
        center = self.c + 0*1*count/100
        dx = x - center
        if( abs(dx) < self.w ):
            p = self.p * (self.w - abs(dx))/self.w 
            pass
        else:
            p = 0
        return p
class power_model2:
    def __init__( self , max_power , width , x0 , y0 ):
        self.p = max_power
        self.x0  = np.deg2rad( x0 )
        self.y0 = np.deg2rad(y0) 
        kx= np.cos( self.y0)*np.cos(self.x0 )
        ky = np.cos( self.y0 )*np.sin(self.x0)
        kz = np.sin(self.y0)
        self.w = np.deg2rad( width )
        self.k = np.array( [ kx, ky,kz ])
    def get_power( self, x0  ,y0 , count ):
        az = np.deg2rad(x0)
        el = np.deg2rad(y0)
        kx= np.cos(el)*np.cos(az )
        ky = np.cos(el )*np.sin(az)
        kz = np.sin(el)
        pointing = np.array( [ kx,ky,kz ])
        delta = np.arccos( np.dot( pointing, self.k))

        if( abs(delta) < self.w ):
            p = self.p * ((self.w - abs(delta))/self.w )
            pass
        else:
            p = 0
        #print("Delta {} {} {}".format( np.rad2deg(delta) , self.w , p))
        return p
def test(  ):
    x_o = []
    y_o = []
    x0  = 0
    x=x0
    m = power_model( max_power=400 , width=5, center=2 )
    c = control.controller( 0 , 0.001 , 0.001 )
    for k in range( 700 ):
       y = m.get_power(  x , k)
       dx = c.update( x , y )
       dt = 2*np.pi/4
       cx = 1*np.cos( k * dt )
       
       x0 = x0+dx
       x =  x0  + cx 
       print( "{} {}".format(dx,y))
       x_o.append( x0 )
       y_o.append( y )

    #plt.plot( x_o  )
    plt.plot(  y_o )
    #plt.plot( xpoints,ypoints)
    plt.show()
    
def test2( ):
    x_o = [] 
    y_o = []
    p_o = []
    x = 12
    y = 23
    m = power_model2( max_power=400 , width=5, x0=10,y0=20 )
    c = control.power_max( x,y ,  0.001 , 0.0001)
    
    for k in range(200):
        p = m.get_power( x , y , k )
        #print("Power {}".format(p))
        cmd = c.update( p  )
        x = cmd[0]
        y = cmd[1]
        x_o.append(x)
        y_o.append(y)
        p_o.append(p)
    c.plot()
if __name__ == "__main__":
    print("Testing controller ")

    test(  )
    test2()