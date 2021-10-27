from numba.np.ufunc import parallel
import numpy as np
import numba 
from numba import jit
import warnings
warnings.filterwarnings('ignore')


#size = int(input("Enter size of your own choosing to intialize arrays: "))
@jit(fastmath = True)
def GenerateHexas(size):
    """INPUT: 
    n: the number of hexas to be examined during the run of the program
    OUTPUT: 
    hexasList: the list of hexas
    sextandsList: the list of related sextands
    squareSextandsList: the list of related square sextands
    """
    # Arrays 
    hexas_array = np.empty(size)
    sextands_array = np.empty(size)
    square_sextands_array = np.empty(size)

    assert size >= 1
    for i in range(size):
        current_hexa = 3*(i + 1) + (3/2) - ((-1)**(i + 1) * (1/2))
        hexas_array[i] = current_hexa
        current_sextand = ((1/2) * (i+1)) + (1/4) + ((1/4) * (-1)**((i+1) - 1))
        sextands_array[i] = int(current_sextand)
        # if the hexa = 6s - 1 for some s, 
        # then its square-sextand is 
        # 6(s^2) - 2s, and if the hexa is 6s + 1 
        # then its square-sextand is 6(s^2) + 2s

        if(i % 2 == 0):
            square_sextand =  6*(current_sextand**2) - 2*current_sextand
            square_sextands_array[i] = square_sextand

        else:
            square_sextand =  6*(current_sextand**2) + 2*current_sextand
            square_sextands_array[i] = square_sextand
    print(hexas_array.astype(int))

@jit(fastmath = True)
def FindInvalidChains(size, n):
    """INPUT: n: the number of hexas to be examined during the run of the program
    OUTPUT: Determines the longest chain of consecutive invalid indices. 
    Prints out the starting index of this chain and its length
    """
    # Arrays
    hexas_array = np.empty(size)
    square_sextands_array = np.empty(size)
    sextands_array = np.empty(size)

    
    sxtnd = 0
    for i in range(size):
        if((i + 1) % 2 == 1):
            hexas_array[i] =  ((3 * (i + 2)) - 1)
            sxtnd += 1
               
        else:
            hexas_array[i] = ((3 * (i + 1)) + 1)

        square_sextands_array[i] =  (((hexas_array[i] * hexas_array[i]) - 1) / 6)
        sextands_array[i] =  sxtnd

    # Integers
    hexorial = 1
    invalid_start = 0
    invalid_length = 0
    max_invalid = 0


    # Boolean
    valid = True

    for i in range(n - 1):
        hexorial *= hexas_array[i]
    
    for i in range((hexorial - 1) / 2):
        valid = True
        for j in range(n - 1):
            result1 = (6 * i) % hexas_array[j] == 1 
            result2 = (6 * i) % hexas_array[j] == hexas_array[j] - 1
            if(result1 or result2):
                valid = False

        if(valid != True):
            invalid_length = invalid_length + 1
            if(max_invalid < invalid_length):
                max_invalid = invalid_length
                invalid_start = i + 1 - max_invalid

        else:
            invalid_length = 0

    
    print("Start of max chain: " + str(invalid_start) + '\n')
    print("Max length chain: " + str(max_invalid) + '\n')
    print("Critical Zone size: " + str(square_sextands_array[n - 1] - square_sextands_array[n - 2]))

FindInvalidChains(1000, 8)


    
 

    
