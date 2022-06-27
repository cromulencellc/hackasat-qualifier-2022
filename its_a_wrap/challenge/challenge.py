#!/usr/bin/python3

from functools import reduce
from operator import add
import os
import sys
import subprocess
import random

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

    # if "SEED" in os.getenv():
    #     random.seed(int(os.getenv('SEED'), 2)

    #
    # Get input from player
    print(" Enter phrase> ",end='')
    phrase_in = input()
    print(" Enter encrypted phrase> ",end='')
    team_encrypt_input = input().strip()
 
    print(" Entered phrase: ", phrase_in)
    print(" Encrypted phrase: ", team_encrypt_input)

    # Do some basic verification of the input
    verified = verify_input(phrase_in,team_encrypt_input)

    # Call encryption function to compare players input
    if  verified == True:
        print("\nComputing encrypted phrase...")
        call_args = ["python3", "encrypt.pyc", "-d", f"{phrase_in}"]
        output = subprocess.check_output(call_args)
        flat_result = output.decode().strip().split(",")
        flat_result_int = list(map(int,flat_result))
        # print("Encypted Output:")
        # print(flat_result_int)
        team_list_input = list(team_encrypt_input.split(","))
        team_int_list = list(map(int,team_list_input))
        # print("Provided Encrypted Input:")
        # print(team_int_list)

        # Do they match?
        if team_int_list == flat_result_int:
            verified = True
        else:
            verified = False

    return verified

if __name__ == "__main__":

    if challenge() == True:
        print("\n----------------------------------")
        print("Congradulations you got it right!!\n")
        flag = os.getenv('FLAG')
        print("Here is your flag: ",flag)
        print("----------------------------------\n")

    else:
        print("\nSorry wrong answer, try again...\n")
        sys.exit(1)

