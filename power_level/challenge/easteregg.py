import sys


def check_easteregg( answer ):
    # if the answer has the text "over 9000" in it with any kind of captialization scheme
    # Then you get the easter egg
    lc_answer = answer.lower()
    quote="over 9000"
    
    if( quote in lc_answer ):
        # Goku's power level is over 9000!
        print("You must be sensing Goku...not the signal")
        f = open('goku.txt','rt')
        text =f.read()
        print( text )
        sys.exit(0)

