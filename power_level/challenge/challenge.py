import os
from sqlite3 import Time
import numpy as np
import random 
import siggen 
import argparse
import threading
import easteregg
import sys

from timeout import timeout,TimeoutError

to = int( os.getenv("TIMEOUT",120))

def run_siggen( gen , port ) :
    gen.send(port) 


@timeout(to)
def challenge( args ):
    # Constants
    Fs = 100000.0
    # allow a few random amplitudes
    amp_choices = [200, 400, 800] # increment by 2x amplitude ( 4x power since power is A^2)
    # Only one frquency 
    freq_choices = [   Fs/32  ]
    freq_tolerance = 100 # Hz
    snr_tolerance = 0.5 # dB
    N = int(Fs)
    # Noise variance  / Noise pwower
    noise_variance = 100.0
    
    # Make choices at random
    amp = random.choice( amp_choices )
    freq = random.choice( freq_choices )
    # This is both the textbook and wikipedia definition of snr.
    # SNR = Psig / Pnoise
    # Psig = A^2
    # Pnoise = var( noise )
    snr = 10 * np.log10( amp*amp /  noise_variance   )
    sample_host = os.getenv( "SERVICE_HOST", )
    sample_port = int( os.getenv("SERVICE_PORT", 1000))
    print("Connect via TCP to get the samples at {}:{}".format( sample_host,sample_port) , flush=True)
    print("The sample rate is {}".format( Fs ), flush=True)
    # Create some samples on a new thread
    gen = siggen.tcp_siggen( samp_rate=Fs , freq=freq , amp=amp,  noise_var=noise_variance , N=N)
    t = threading.Thread( target=run_siggen , args=(gen,args.port) , daemon=True)
    t.start()
    # Ask the player what they think the answer is
    # If they answer with the correct dragonball quote then print the easter egg!
    print("What is the frequency of the signal? (Hz)")
    freq_str = input() 
    easteregg.check_easteregg( freq_str )
    print("What is the signal to noise ratio (dB)")
    snr_str = input()
    easteregg.check_easteregg( snr_str )
    print("You answered freq: {} snr: {}".format( freq_str,snr_str))
    # Make sure the answers are floats
    try:
        snr_answer = float( snr_str )
        freq_answer = float( freq_str )
    except:
        print("input malformed - type in numbers like 123.456789")
        sys.exit(0)

    # Check if the answers are within the tolerance
    snr_correct = np.abs( snr - snr_answer ) < snr_tolerance 
    freq_correct = np.abs( freq - freq_answer ) < freq_tolerance

    if( snr_correct and freq_correct ):
        flag = os.getenv("FLAG")
        print("Here is your flag:")
        print(flag)
    else:
        # Wrong answer results in Napa's quote!
        print("What!!! there is no way that can be right!")
        

    print("Exiting")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample-port", dest="port", type=int, required=True)
    args = parser.parse_args()
    service_host = os.getenv("SERVICE_HOST" , "localhost")
    service_port = os.getenv("SERVICE_PORT" , args.port)
    print("Samples available at: {} {} ".format( service_host, service_port))
    try:
        challenge(args)
    except TimeoutError:
        print("Timeout ....bye")
