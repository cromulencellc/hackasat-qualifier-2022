

class linear_target:
    def __init__(self, x0 , dx):
        self.x0 = x0 
        self.dx = dx 
        self.x = x0
    def update(self ):
        self.x = self.x + self.dx 
        return self.x 
    def set_dx( self , dx):
        self.dx = dx 
