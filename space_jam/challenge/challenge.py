import argparse 
import transmitter
import json
import os

from timeout import timeout,TimeoutError

to = int( os.getenv("TIMEOUT",300))

def make_flag( N):
    # Create the flag file we are going to use for the transmitter
    # Flags are NOT equivalent in length so we have done the following to keep things fair:
    #    The flag file is generated to be N characters in length no matter what.
    #    If N is the desired length of the file and M is the length of the flag we will put K = M-N pad bytes in front of the flag
    # This way everyone has to decode until the end of the signal in order to get their flag
    flag = os.getenv("FLAG")
    f = open("flag.txt",'wt')
    text = "Here is your flag:\n{}\n".format(flag)
    L = len( text )
    pad = "*"
    wait_text = "FlagComingSoon"
    wait_rep = int( (N-L)/len(wait_text) ) 
    wait_pad = wait_text*wait_rep
    pad_rep  = N - len( wait_pad )- L 
    pad_text = pad * pad_rep 
    f.write( wait_pad )
    f.write( pad_text )
    f.write( text )
    f.close()
@timeout( to )
def challenge( args ):
    # Make the flag so that it is N in length
    make_flag(args.N)
    # Prompt the user for an un-pretty json text 
    print("Enter transmitter configuration as JSON (no newlines)", flush=True)
    config_text = input()
    # Turn the json into a dictionary
    config = json.loads( config_text )
    # Run our transmitter
    transmitter.run_transmitter( config=config  , port=args.snk_port )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample-port", dest="snk_port", type=int, required=True)
    parser.add_argument("--flag_max_length" , dest="N",  type=int , default=1500)
    args = parser.parse_args()
    try:
        challenge(args)
    except TimeoutError:
        print("Timeout....bye", flush=True)