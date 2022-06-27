import os 
import socket
import numpy as np
import matplotlib.pyplot as plt 
import time
def work( sock , Fs , N ):
    print("Trying to get {} samples at {}".format(N,Fs))
    count = 0 
    bytes_total = b""
    # Get the sample bytes 
    while( count < N*8 ):
        bytes_in =  sock.recv( N*8 )# receive N complex64 bit numbers
        bytes_total = bytes_total + bytes_in
        count = count + len( bytes_in)
    # Make them into a complex 64
    samples = np.frombuffer( bytes_total , dtype=np.dtype('complex64'))    
    print("Got {} samples".format(len(samples)))
    # Take a FFT of the samples
    spectrum = np.fft.fft( samples  , norm="forward")
    freqs = np.fft.fftfreq(samples.shape[-1]) * Fs
    power = np.real(spectrum * np.conj( spectrum ) ) 
    max_ind = np.argmax( power )
    # Make a copy of the spectrum but zero out the values around the signal - this leaves only noise
    noise_band = spectrum 
    noise_band[max_ind] = 0 # remove the tone from the signal to get the noise only (only works for a pure carrier like this problem)
    noise_band[max_ind-1] = 0 
    noise_band[max_ind+1] = 0 
    # Take an iift of the noise only signal so that we get things in time domain 
    noise_only = np.fft.ifft( noise_band , norm='forward' ) 

    # Get the frequency of the sinusioid and its power
    freq = freqs[ max_ind ]
    max_power = np.real(power[max_ind])
    # Take the variance of the noise only signal to get its power
    noise_power = np.var( noise_only )  # Textbook definition of noise power is the variance of the noise
    # Put things in DB which is nice!
    sig_power_db = 10*np.log10( max_power) 
    noise_power_db = 10*np.log10( noise_power  ) 
    snr = sig_power_db - noise_power_db
    print("I think the answers are")
    print("Frequency (HZ): {}".format(freq))
    print("Signal Power: {}".format(sig_power_db))
    print("Noise Power: {}".format(noise_power_db))
    print("SNR (dB): {}".format(snr))
    return (freq,snr)

def get_samp_rate( text ):
    preamble = "The sample rate is"
    lines = text.split("\n")
    for line in lines:
        if( preamble in line ):
            fs_str = line.replace(preamble,"")
            fs_str = fs_str.replace(" ","")
            fs_str = fs_str.replace("\n","")
            return float( fs_str )


def solve( host , port , sample_port ): 
    # Get the challenge prompt
    print("Solver listening for challenge prompt on: {} {}".format( host,port))
    prompts = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    prompts.connect((host, port))
    ticket = os.getenv("CHAL_TICKET")
    if( ticket  != None ):
        prompts.recv(1000)
        print("Sending ticket - {}".format( ticket ), flush=True)
        prompts.send( ticket.encode('utf-8'))
        prompts.send( "\n".encode('utf-8'))
        ticket_sent = True
    

    out = prompts.recv(1000)
    text = out.decode('utf-8')
    print(text, flush=True)
    # Create a socket to listen for the samples
    sample_host = input("Enter sample host:")
    sample_port = int(input("Enter sample port:"))
    print("Solver listening for smaples on: {} {}".format( sample_host, sample_port))
    samps = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    samps.connect((sample_host, sample_port))
    # Deduce the sample rate from the challenge
    Fs = get_samp_rate( text )
    # Figure out what the frequency and snr is 
    answers = work( samps, Fs, int(Fs) )
    # Send the answers as text
    prompts.send( "{}\n".format(answers[0]).encode('utf-8'))
    prompts.send( "{}\n".format(answers[1]).encode('utf-8'))

    time.sleep(3)
    out = prompts.recv(1000)
    print(out.decode('utf-8'), flush=True)
    print("Solver exiting")

if __name__ == "__main__":
    host = os.getenv("CHAL_HOST","172.17.0.1")
    port = int(os.getenv("CHAL_PORT", 10000))
    sample_port = int(os.getenv("SAMPLE_PORT", 10001))
    solve( host , port , sample_port )