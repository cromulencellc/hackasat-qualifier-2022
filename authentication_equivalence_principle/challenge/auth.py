import datetime
import hmac

class totp:

    def __init__(self , secret_key , epoch , period_secs ):
        # 
        self.epoch = epoch
        self.period = period_secs 
        self.key = secret_key.encode('utf-8')
    def generate( self , time ):
        dt = time - self.epoch
        count = int( dt.total_seconds() / self.period )
        count_bytes = count.to_bytes(8,"little")
        keygen =  hmac.new( self.key, msg = count_bytes , digestmod='sha256')
        
        key = keygen.hexdigest()
        #print( "Count: {}".format( count ) )
        
        
        #print( key )
        return key


if __name__ == "__main__":
    epoch = datetime.datetime.utcnow()
    dt =datetime.timedelta(minutes=10, microseconds=11)
    keygen = totp( "mikes-key" , epoch , 0.00001 )
    keygen.generate( epoch + dt )
    keygen.generate( epoch + 2*dt )
    keygen.generate( epoch + dt )
