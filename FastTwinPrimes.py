from logging import critical
from numba.np.ufunc import parallel
import numpy as np
import numba 
from numba import jit
import warnings
warnings.filterwarnings('ignore')


#size = int(input("Enter size of your own choosing to intialize arrays: "))

@jit(nopython = True, parallel = True)
def InitializeArrays(size):
    # Arrays 
    hexas_array = np.empty(size)
    sextands_array = np.empty(size)
    square_sextands_array = np.empty(size)
    return hexas_array, sextands_array, square_sextands_array

@jit(nopython = True, parallel = True)
def GenerateArrays(size):
    hexas_array, sextands_array, square_sextands_array = InitializeArrays(size)
    sxtnd = 0
    for i in range(size):
        if((i + 1) % 2 == 1):
            hexas_array[i] =  ((3 * (i + 2)) - 1)
            sxtnd += 1
               
        else:
            hexas_array[i] = ((3 * (i + 1)) + 1)

        square_sextands_array[i] =  (((hexas_array[i] * hexas_array[i]) - 1) / 6)
        sextands_array[i] =  sxtnd
    return hexas_array, sextands_array, square_sextands_array


@jit(fastmath = True)
def GenerateHexas(hexas_num):
    """INPUT: 
    n: the number of hexas to be examined during the run of the program
    OUTPUT: 
    hexasList: the list of hexas
    sextandsList: the list of related sextands
    squareSextandsList: the list of related square sextands
    """
    # Arrays 
    hexas_array, sextands_array, square_sextands_array = InitializeArrays(hexas_num)

    assert hexas_num >= 1
    for i in range(hexas_num):
        current_hexa = 3*(i + 1) + (3/2) - ((-1)**(i + 1) * (1/2))
        hexas_array[i] = current_hexa
        current_sextand = ((1/2) * (i+1)) + (1/4) + ((1/4) * (-1)**((i+1) - 1))
        sextands_array[i] = int(current_sextand)

        if(i % 2 == 0):
            square_sextand =  6*(current_sextand**2) - 2*current_sextand
            square_sextands_array[i] = square_sextand

        else:
            square_sextand =  6*(current_sextand**2) + 2*current_sextand
            square_sextands_array[i] = square_sextand

    hexas_array = hexas_array.astype(int)
    square_sextands_array = square_sextands_array.astype(int)
    sextands_array = sextands_array.astype(int)
    return hexas_array, square_sextands_array, sextands_array
    
@jit(fastmath = True)
def FindInvalidChains(n):
    """INPUT: n: the number of hexas to be examined during the run of the program
    OUTPUT: Determines the longest chain of consecutive invalid indices. 
    Prints out the starting index of this chain and its length
    """
    # Arrays
    hexas_array, sextands_array, square_sextands_array = GenerateArrays(n)
    
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

    max_chain = invalid_start
    max_length = max_invalid
    critical_zone = square_sextands_array[n - 1] - square_sextands_array[n - 2]
    return max_chain, max_length, critical_zone

@jit(fastmath = True)
def GenerateCombo(hexas_num, index):
    """
    INPUT: 
    hexasChecked: The number of hexas checked (must be less than the number of hexas generated)
    index: index to check combo
    RETURNS:
    combo: a string with the combos for a certain index, < denotes the combo is valid
    """
    # Arrays
    hexas_array, sextands_array, square_sextands_array = InitializeArrays(hexas_num + 1)
    sxtnd = 0
    for i in range(hexas_num):
        if((i + 1) % 2 == 1):
            hexas_array[i] =  ((3 * (i + 2)) - 1)
            sxtnd += 1
               
        else:
            hexas_array[i] = ((3 * (i + 1)) + 1)

        square_sextands_array[i] =  (((hexas_array[i] * hexas_array[i]) - 1) / 6)
        sextands_array[i] =  sxtnd

    assert hexas_num < len(hexas_array)
    assert hexas_num >= 1
    assert index >= 1
    valid = True
    combo = ""
    for i in range(hexas_num):
        mod = int(index % hexas_array[i])
        str_mod = str(mod)
        combo += str_mod + " "
        one = mod == 1
        previous = mod == hexas_array[i] - 1
        if (one or previous):
            valid = False
    if(valid):
        combo += "< "
    return combo 

@jit(fastmath = True)
def ViewCombo(hexas_checked, start, length):
    """INPUT:
    hexasChecked: The number of hexas checked (must be less than the number of hexas generated)
    start: The starting index of the chain to be displayed
    length: The number of index combinations to be displayed
    OUTPUT: 
    Displays the combos for the indices starting at start and ending at start + length; also marks valid combos 
    Returns: 
    combosList: list of combos
    """
    combos_list = []
    end = start + length
    for i in range(start,end):
        combo = str(i) + ": "
        combo += GenerateCombo(hexas_checked, i)
        combos_list.insert(i, combo)
    combos_array = np.array(combos_list)
    return combos_array