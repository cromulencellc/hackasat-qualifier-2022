import socket 

class TcpReader( ):
    def __init__(self, host , port ):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect( (host , port) )
        self.text = ""
    def read_until(self, stop_at ):
        keep_going = True 
        section = ""
        while( keep_going ):
            out = self.s.recv(2000 )
            chunk = out.decode('utf-8')
            self.text = self.text + chunk
            found = False
            for item in stop_at:
                if( item in self.text ):
                    found = True
                    found_text = item 
            if( True == found ):
                
                ind = self.text.find( found_text ) + len( found_text )
                section = self.text[:ind]
                self.text = self.text[ind:]
                keep_going= False 
        
        return section
    def get_remaining( self ):
        out = self.text
        return out
    def read_all(self):
        out = self.s.recv( 1000 )
        section = self.text + out.decode('utf-8')
        self.text = ""
        return section 
    def send(self, text ):
        self.s.send( text.encode('utf-8'))