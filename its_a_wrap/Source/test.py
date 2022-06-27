#!/usr/bin/python3

from functools import reduce
from operator import add
from ctypes import c_void_p, cdll
from numpy.ctypeslib import ndpointer
import numpy as np

#result = np.zeros(9)

#
# Print a single nxm matrix.
def print_matrix(matrix: np.array, n: int, m: int) -> np.array:
    for i in range(0,n):
        for j in range(0,m):
            print( i, j, matrix[i,j])
  
    return 

#
# Call C function to encrypt phrase.
def do_encryption(phrase:list) -> np.array:
    np_phrase = np.zeros(8)
    np_phrase = np.array(phrase)

    try:
        # Load C DLL and define call/return parameters,
        foo = cdll.LoadLibrary("./libfoo.so")
        foo = foo.encrypt_it
        foo.restype = ndpointer(dtype=np.int64, shape=(3,3))
    except Exception as error:
        print("\n ***Load library error: ",error,"\n")

    try:
        # Call the C function to encrypt the phrase.
        result = np.zeros(9)
        result = foo(c_void_p(np_phrase.ctypes.data))
    except Exception as error:
        print("\n *** Function call error: ",error,"\n")

    return result

#
# Verify input is the right size and convertable to a list (comma separated)
def verify_input(phrase_string, encrypt_string):
    try:
        ph_list = [int(s) for s in phrase_string.split(',')]
        if len(ph_list) != 9:
            print("*** Invalid number of phrase characters ***")
            return False
    except Exception as error:
        print("*** Invalid phrase list format ***")
        return False

    try:
        en_list = [int(s) for s in encrypt_string.split(',')]
        if len(en_list) != 9:
            print("*** Invalid number of encrypted characters ***")
            return False
    except Exception as error:
        print("*** Invalid encrypted list format ***")
        return False

    #print("\nInput Validated\n")
    return True

#
# Define challenge, collect input and determine if team input is correct
def challenge():
    print("You have inherited a simple encryption dll from previous project")
    print("that you must use.  It used to work but now it seems it does not.")
    print("Given the encryption matrix:")
    print("| -3 -3 -4 |")
    print("|  0  1  1 |")
    print("|  4  3  4 |")
    print("...and the phrase 'HACKASAT3'.")
    print("\n Enter the phrase in standard decimal ASCII")
    print(" and the resulting encrypted list")
    print("    Example: 'XYZ': 88,89,90")
    print("             Encrypted list: 1,2,3,4,5,6,7,8,9")

    #
    # Get input from player
    print(" Enter phrase> ",end='')
    phrase_in = input()
    print(" Enter encrypted phrase> ",end='')
    team_encrypt_input = input()
 
    print(" Entered phrase: ", phrase_in)
    print(" Encrypted phrase: ", team_encrypt_input)

    # Do some basic verification of the input
    verified = verify_input(phrase_in,team_encrypt_input)

    # Call encryption function to compare players input
    if  verified == True:
        print("\nComputing encrypted phrase...")

        # Turn phrase into integer list
        ph_list = [int(s) for s in phrase_in.split(',')]

        result = np.zeros(9)
        result = do_encryption(ph_list)
    
        # Convert result from C function to an integer list
        flat_result = result.flatten()
        flat_result = flat_result.tolist()

        # Convert team input to an integer list
        team_encrypt_input = list(team_encrypt_input.split(","))
        list_list = list(map(int,team_encrypt_input))

        # Do they match?
        if list_list == flat_result:
            verified = True
        else:
            verified = False

    return verified

if __name__ == "__main__":

    if challenge() == True:
        print("\n----------------------------------")
        print("Congradulations you got it right!!")
        print("----------------------------------\n")

    else:
        print("\nSorry wrong answer, try again...\n")

