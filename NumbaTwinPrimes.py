from logging import critical
from numba.np.ufunc import parallel
import numpy as np
from numba import jit
import warnings
import os
from numpy.core.fromnumeric import size
warnings.filterwarnings('ignore')

@jit(nopython = True, parallel = True)
def InitializeArrays(size):
    # Arrays 
    hexas_array = np.empty(size)
    sextands_array = np.empty(size)
    square_sextands_array = np.empty(size)
    return hexas_array, sextands_array, square_sextands_array

@jit(nopython = True, parallel = True, fastmath = True)
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

@jit(nopython = True, parallel = True, fastmath = True)
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

@jit(fastmath = True)
def ViewCritCombos(hexas_checked):
    """INPUT: 
    hexasChecked: The number of hexas to be checked 
    OUTPUTS: 
    displays the combos in the critical area
    RETURNS:
    combosList: list of combos
    """
    hexas_array, sextands_array, square_sextands_array = GenerateArrays(hexas_checked)
    start = 1
    length = int(square_sextands_array[hexas_checked - 1] + 1)
    combos_array = ViewCombo(hexas_checked, start, length)
    return combos_array

@jit(nopython = True, parallel = True, fastmath = True)
def FindAverageGap(hexas_checked):
    """INPUTS: 
    hexasChecked: The number of hexas to be checked 
    OUTPUTS: 
    Displays the expected average gap between valid combos (hexorial / Lexorial)
    Returns:
    num: Hexorial of n hexas
    denom: Lexorial of n hexas
    gap: average of hexorial/lexorial
    NOTES: May want to take an input and find the average gap in that range (e.g. if n = 2, find the average gap in [0, (5*7)) range
    """
    hexas_array, sextands_array, square_sextands_array = GenerateArrays(hexas_checked)
    gap, num, denom = 1,1,1
    for i in range(0,hexas_checked):
        num *= hexas_array[i]
        denom *= hexas_array[i]-2
    gap = num/denom

    return num, denom, gap

@jit(fastmath = True)
def ValidCoordinates(hexas_num):
    """INPUTS:
    hexasNum: The number of hexas being examined
    OUTPUT: .txt document given the coordinates where x is the number of hexas checked and y is the number of valid combos in critical area
    """
    combo = ""
    validNum = 0
    combos_list = []

    hexas_array, sextands_array, square_sextands_array = GenerateArrays(hexas_num)

    for i in range(2, hexas_num + 1): # Cycle through all hexa pairs
        combo = "(" + str(i) + ","
        # print(combo)
        validNum = 0

        for j in range(int(square_sextands_array[i-2]), int(square_sextands_array[i-1] + 1)):
            valid = True
            for k in range(i):
                result1 = ((6 * j) % hexas_array[k] == 1)
                result2 = (6 * j) % hexas_array[k] == hexas_array[k] - 1
                if(result1 or result2):
                    valid = False

            if(valid):
                validNum += 1

        combo += str(validNum) + ")"
        combos_list.append(combo)
    
    WriteValidCoordinates(combos_list, hexas_num)
    return combos_list

def WriteValidCoordinates(combos_list, hexas_num):

    hexas_checked = "Hexas checked: " + str(hexas_num) + "\n"
    file_name = "valid_coordinates.txt"

    if os.path.exists(file_name):
        os.remove(file_name)

    with open(file_name, "a") as file:
        file.write(hexas_checked)

        for i in combos_list:
            file.write(i)
            file.write("\n")

@jit(fastmath = True)
def GenerateCombos(hexas_num):
    """INPUTS:
    hexasNum: The number of hexas being examined (e.g. if hexasnum = 3, then 5,7, and 11 are being examined)
    OUTPUTS: Combines functionality of findInvalidChains() and viewChains()
    """
    # boolean variables
    adv = True 
    valid = True

    # combos_array initialized with size of hexasNum
    combos_array = np.empty(hexas_num)
    combos_list = []
    hexas_array, sextands_array, square_sextands_array = GenerateArrays(hexas_num)

    # integer varaibles
    index = 1
    invalidChainLength = 0
    maxChainLength = 0
    invalidStart = 0

    # float variables 
    chainLengthSum = 0.0
    chainsNum = 0.0

    # information list
    info_list = []

    while (adv):
        adv = False
        valid = True

        print_statement = str(str(index) + ": ")
        for i in range(0 , len(combos_array)):
            combos_array[i] = (index % hexas_array[i])

            if(combos_array[i] != 0):
                adv = True
            
            if(i % 2 == 0):
                result1 = combos_array[i] == ((i + 2) / 2) 
                result2 = combos_array[i] == hexas_array[i] - ((i + 2) / 2)
                if (result1) or (result2):
                    valid = False

            elif(i % 2 == 1):
                result3 = combos_array[i] == ((i + 1) / 2)
                result4 = combos_array[i] == hexas_array[i] - ((i + 1) / 2)
                if (result3) or (result4):
                    valid = False
            
            print_statement += " "
            print_statement += str(combos_array[i])

        if(valid):
            print_statement += " <"
            combos_list.append(print_statement)
            chainLengthSum += invalidChainLength
            chainsNum+=1
            invalidChainLength = 0
        else:
            invalidChainLength +=1 

            if(invalidChainLength > maxChainLength):
                maxChainLength = invalidChainLength
                invalidStart = index - maxChainLength + 1

        index+=1
        
    return combos_list, maxChainLength, invalidStart

@jit(fastmath = True)
def ValidNumApproximation(hexas_num):
    """INPUTS: hexasNum
    OUTPUTS: Calculates an approximated for the expected number of valid combos within the domain (i.e. [1, A] where A is the upper bound of
   the critical area), counts the true number of valid combos within the domain, and displays the error between them. Outputs to a txt file named
   valid_num_approx.txt as well as the console. 
    """

    '''
        prodApprox is the approximated number of valid combos by taking quotient of the lesser hexorial and the true hexorial,
		then multiplying that by the index, which in this case is the square-sextand of the greatest hexa being examined, i.e.
		the upper boundary of the critical area

        prodTrue is the actual number of valid combos counted within the range of [1, A], where A is the upper boundary of the
		critical area
    '''
    # Generate arrays  
    hexas_array, sextands_array, square_sextands_array = GenerateArrays(hexas_num + 1)
    valid_list = []

    # integers
    endPoint = int(square_sextands_array[hexas_num - 1])
    marker = 1

    # floats
    prodTrue = 0.0
    prodApprox = 1.0

    # boolean values
    validCombo = False

    for i in range(1, endPoint):
        validCombo = True
        if(i > square_sextands_array[marker]):
            marker += 2

        for j in range(0, marker):
            result1 = i % hexas_array[j] == sextands_array[j]
            result2 = i % hexas_array[j] == (hexas_array[j] - sextands_array[j])
            if (result1) or (result2):
                validCombo = False
                break
        
        if(validCombo == True):
            prodTrue+=1
            print_statement = "Valid at " + str(i)
            valid_list.append(print_statement)
                
    for j in range(0, hexas_num):
        prodApprox *= ((float(hexas_array[j] - 2)) / (float(hexas_array[j])))
    
    prodApprox *= endPoint
    error = (prodTrue - prodApprox) / float(prodTrue)
    error_percentage = error * 100

    return valid_list, endPoint, prodApprox, prodTrue, error_percentage
     
    