import argparse
from ctypes import c_void_p, cdll
from numpy.ctypeslib import ndpointer
import numpy as np


def print_matrix(matrix: np.array, n: int, m: int) -> None:
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--data", required=True, help="Comma seperated string data to encrypt")

    args = parser.parse_args()
    if args.data:
        phrase_in = args.data
        # Turn phrase into integer list
        ph_list = [int(s) for s in phrase_in.split(',')]

        result = np.zeros(9)
        result = do_encryption(ph_list)
        # print(str(result))

        # Convert result from C function to an integer list
        flat_result = result.flatten()
        flat_result = flat_result.tolist()
        print(",".join(map(str,flat_result)))
    else:
        print("No data processeed")

  