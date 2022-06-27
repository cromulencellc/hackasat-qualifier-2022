#!/usr/bin/env python3
import random
import os
import hashlib
from timeout import timeout,TimeoutError

to = int( os.getenv("TIMEOUT",60))


class Values:
    BAD_IMAGE_CMDS = ["TAKE_IMG", "GET_IMAGE_SIZE", "DLINK_IMG", "SHELL_CMD", "SEND_FILE", "LOAD_TBL", "START_APP", "DECOMPRESS_FILE"]
    CORRECT_CMD = ["PLAYBACK_FILE"]
    
    FLAG = os.getenv('FLAG', "flag{IF_YOU_SEE_THIS_CONTACT_AN_ADMIN}")
    codes = [ {"name":"vegas.jpg"    , "code":"letsgolasvegas" , "sha":"3b20a3b5b327c524674ca5a8310beb2d9efc5c257e60c4a9b0709d41e63584a3"},
              {"name":"la.jpg"       , "code":"cityofangels"   , "sha":"242f693263d0bcc3dd3d710409c22673e5b6a58c1a1d16ed2e278a8d844d7b0b"},
              {"name":"sf.jpg"       , "code":"housingmarket"  , "sha":"f37e36824f6154287818e6fde8a4e3ca56c6fea26133aba28198fe4a5b67e1a1"},
              {"name":"miami.jpg"    , "code":"springbreak"    , "sha":"2aa0736e657a05244e0f8a1c10c4492dde39907c032dba9f3527b49873f1d534"},
              {"name":"nyc.jpg"      , "code":"fuhgeddaboudit" , "sha":"983b1cc802ff33ab1ceae992591f55244538a509cd58f59ceee4f73b6a17b182"},
              {"name":"slc.jpg"      , "code":"skiparadise"    , "sha":"088f26f7c0df055b6d1ce736f6d5ffc98242b752bcc72f98a1a20ef3645d05c1"},
              {"name":"chicago.jpg"  , "code":"deepdish"       , "sha":"04ca7d835e92ae1e4b6abc44fa2f78f6490e0058427fcb0580dbdcf7b15bbb55"},
              {"name":"portland.jpg" , "code":"stayweird"      , "sha":"b4447c4b264b52674e9e1c8113e5f29b5adf3ee4024ccae134c2d12e1b158737"},
              {"name":"boston.jpg"   , "code":"beanpot"        , "sha":"d6bc6fbee628c3278ef534fd22700ea4017914c2214aa86447805f858d9b8ad4"},
    ]

def random_challenge():
    choices = random.sample( Values.codes , 5)
    for item in choices:
        img = item["name"]
        code = item["code"]
        img_sha =item["sha"]
        print("{}?".format( img_sha ))
        print(">>" ,end="")
        answer = input()
        if ( answer == code ):
            print("Thank you",flush=True)
        else:
            print("Wrong",flush=True)
            return False
    return True
def run_command( msg ):
    if( msg in Values.CORRECT_CMD ):
        good = random_challenge()
        if( good == True):
            print("OK you can have the satellite back")
            print("{}".format( Values.FLAG),flush=True)
        else:
            print("Failed",flush=True)
    elif( msg in Values.BAD_IMAGE_CMDS):
        good = random_challenge()
        if( good == True ):
            print("You did it")
            print("I'm still not giving you the satellite back",flush=True)
        else:
                print("Failed ",flush=True)
        pass
    else:
        print("----INVALID------",flush=True)
    
@timeout(to)
def challenge():
    print("Can you regain control!")
    print("CMD>",flush=True, end="")
    msg = input( )
    run_command(msg)
    
    
if __name__ == "__main__":
    try:
        challenge()
    except TimeoutError:
        print("Timeout...bye",flush=True)
