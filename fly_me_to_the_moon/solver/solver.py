import helper
import argparse 
import os
import sys

def solve( host , port , maneuver_file ):
    io = helper.stdio_solve_helper( host=host ,port=port, prompt="Input next maneuver:" , solved="Complete!" , wrong="Incorrect", encoding="UTF-8")
    io.add_challenge_block(name="info",header="Save our mining operation!", reset = False)
    io.handle_ticket()
    # open maneuver file
    f = open(maneuver_file , "rt")
    maneuvers = f.readlines()
    # loop over all maneuvers
    for dv in maneuvers:
        io.wait_for_single_challenge( )
        io.send_answer(dv)
        io.reset()
    io.wait_for_single_challenge()
    io.send_answer("DONE")
    io.wait_for_single_challenge()
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Description of your program')
    parser.add_argument('--maneuvers', help='Run the solver but skip relativity', default="solution.txt")
    args = vars(parser.parse_args())
    host = os.getenv("CHAL_HOST") 
    port = int( os.getenv("CHAL_PORT" , 0)  ) 

    if( not host ):
        sys.exit(-1)
    if( not port ):
        sys.exit(-1)
    solve( host, port , args["maneuvers"] )
    sys.exit(0)