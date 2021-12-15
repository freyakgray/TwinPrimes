"""
    Description:
    --------------------
    Numba Implementation of TwinPrimes.py. The difference being, instead of using python lists to store data, this 
    implementation combines the use of NumPy arrays as well as numba.jit to store and compute data.
    The goal is to make a faster implementation of TwinPrimes.py

    Tools/library:
    --------------------
    - Numba
    - NumPy
    - Jit

    Drawbacks:
    --------------------
    - @size < 100,000: TwinPrimes.py is faster
    - numba and jit reduce python functionality, being theses library's are designed for NumPy specifically.  

    Additives/Benifits
    ---------------------
    - @ size > 100,000: NumbaTwinPrimes.py can be significantly faster depending on the desired size of the array. Generally, 
                            The bigger the size, the bigger difference there is between lists and array population with NumPy arrays
                            being faster.

    - Memory: Less Memory is used to store the data. 

    Numba and Jit Description
    ---------------------------
    - From URL: http://numba.pydata.org
    - Numba is an open source JIT compiler that translates a subset of Python and NumPy code into fast machine code.
    - Numba translates Python functions to optimized machine code at runtime using the industry-standard LLVM compiler library. 
        Numba-compiled numerical algorithms in Python can approach the speeds of C or FORTRAN.
    - Numba is designed to be used with NumPy arrays and functions. Numba generates specialized code for different array data types 
        and layouts to optimize performance. Special decorators can create universal functions that broadcast over NumPy arrays just 
        like NumPy functions do.

"""

# Imports
# Numba/Numba.jit
from numba import jit

# Numpy
import numpy as np

# os for file writing - Only used in WriteValidCoordinates
import os

# filter depreciation warnings for numba
import warnings
warnings.filterwarnings('ignore')

@jit()
def InitializeArrays(size):
    """ 
        Description
        -----------
        Initalizes hexasArray, sextandsArray, squareSextandsArray with a given size

        numba.jit Parameters
        --------------------
        - No Parameters to pass here. 

        Parameters
        ----------
        size: The desired size/len of the numpy array.

        Returns:
        --------
        Empty hexasArray, sextandsArray, squareSextandsArray of @param: size. 
    """
    # Initialize empty arrays of @param: size 
    hexasArray = np.empty(size)
    sextandsArray = np.empty(size)
    squareSextandsArray = np.empty(size)
    return hexasArray, sextandsArray, squareSextandsArray

@jit(fastmath = True)
def GenerateHexas(hexasNum):
    """ 
        Description
        -----------
        Generates hexas given desired hexasNum.

        numba.jit Parameters
        --------------------
        fastmath = True

        Parameters
        ----------
        hexasNum: the desired number of hexas the user wants to generate

        Returns:
        --------
        Populated hexasArray, sextandsArray, squareSextandsArray of @param: size. 
    """
    # Initializes empty arrays 
    hexasArray, sextandsArray, squareSextandsArray = InitializeArrays(hexasNum)

    # Make sure hexasNum is greater than or equal  to size = 1
    assert hexasNum >= 1

    # Get the index (used to calculate the current hexa as well as the square sextand)
    index = np.arange(hexasArray.shape[0])

    # Calculate the current hexa and place into hexasArray
    currentHexa = 3*(index + 1) + (3/2) - ((-1)**(index + 1) * (1/2))
    hexasArray = currentHexa

    # Calculate the current sextand and place into sextandsArray
    currentSextand = ((1/2) * (index + 1)) + (1/4) + ((1/4) * (-1)**((index + 1) - 1))
    sextandsArray = currentSextand

    # Using np.where, place square sextands into squareSextandsArray given condition: index % 2 == 0
    squareSextandsArray = np.where(index % 2 == 0, 6*(currentSextand**2) - 2*currentSextand,  6*(currentSextand**2) + 2*currentSextand).astype(int)
    return hexasArray, sextandsArray, squareSextandsArray
    
@jit(fastmath = True)
def FindInvalidChains(hexasNum):  
    """ 
        Description
        -----------
        Determines the longest chain of consecutive invalid indices and prints out the the starting index
        and its length

        numba.jit Parameters
        --------------------
        fastmath = True

        Parameters
        ----------
        hexasNum: the desired number of hexas the user wants to generate

        Returns:
        --------
        maxChain, maxLength, criticalZone

    """
    # Generate Hexas and populate hexasArray, sextandsArray, squareSxtandsArray --> Note: sextandsArray  not used in this function
    hexasArray, sextandsArray , squareSextandsArray = GenerateHexas(hexasNum)
    
    # Integers
    hexorial = 1
    invalidStart = 0
    invalidLength = 0
    maxInvalid = 0

    # Boolean Value
    valid = True

    for i in range(hexasNum - 1):
        hexorial *= hexasArray[i]
    
    # Find valid hexas
    for i in range((hexorial - 1) / 2):
        valid = True

        for j in range(hexasNum - 1):
            result1 = (6 * i) % hexasArray[j] == 1 
            result2 = (6 * i) % hexasArray[j] == hexasArray[j] - 1
            if(result1 or result2):
                valid = False

        # set invalid lengths
        if(valid != True):
            invalidLength = invalidLength + 1
            if(maxInvalid < invalidLength): 
                maxInvalid = invalidLength
                invalidStart = i + 1 - maxInvalid

        else:
            invalidLength = 0

    # calculate return values
    maxChain = invalidStart
    maxLength = maxInvalid
    criticalZone = squareSextandsArray[hexasNum - 1] - squareSextandsArray[hexasNum - 2]
    return maxChain, maxLength, criticalZone
@jit(fastmath = True)
def GenerateCombo(hexasNum, index):
    """ 
        Description
        -----------
        Using an index and the number of desired hexas the user wants to check, this function determines
        the combo for the index. 
        < Denotes a valid Combo. 

        numba.jit Parameters
        --------------------
        fastmath = True

        Parameters
        ----------
        hexasNum: the desired number of hexas the user wants to generate
        index: The index number the user wants to check 

        Returns:
        --------
        combo: a string with the combos for a certain index, < denotes the combo is valid 

    """

    # Iinitialize empty arrays
    hexasArray, sextandsArray, squareSextandsArray = GenerateHexas(hexasNum + 1)

    # assertions
    assert hexasNum < len(hexasArray)
    assert hexasNum >= 1
    assert index >= 1

    # Boolean Value Valid
    valid = True

    # Initialize combo string
    combo = ""
    
    # find valid combos 
    for i in range(hexasNum):
        mod = int(index % hexasArray[i])
        strMod = str(mod)
        combo += strMod + " "
        one = mod == 1
        previous = mod == hexasArray[i] - 1
        if (one or previous):
            valid = False
    
    # Mark valid combo with '<' 
    if(valid):
        combo += "< "
        
    return combo

@jit(fastmath = True)
def ViewCombo(hexasNum, start, length):
    """ 
        Description
        -----------
        Displays the combos for the indices starting at 'start' and ending at ('start + length'); also marks valid 
        combos and returns a list containing the combos. This function calls GenerateCombo(hexasNum, index)

        numba.jit Parameters
        --------------------
        fastmath = True

        Parameters
        ----------
        hexasNum: The number of desired hexas checked
        start: The starting index of the chain to be displayed
        length: The number of index combinations to be displayed 
        
        Returns:
        --------
        combosArray: an array of string 'combos'

    """

    # Insert the combos into a list then into  an array 
    combosList = []
    end = start + length
    for i in range(start,end):
        combo = str(i) + ": "
        combo += GenerateCombo(hexasNum, i)
        combosList.insert(i, combo)
    combosArray = np.array(combosList)
    return combosArray

@jit(fastmath = True)
def ViewCritCombos(hexasNum):

    """ 
        Description
        -----------
        Displays the combos in the critical area 

        numba.jit Parameters
        --------------------
        fastmath = True

        Parameters
        ----------
        hexasNum: The number of desired hexas checked
        
        Returns:
        --------
        combosArray: an array of string 'combos' in the critical area

    """
    hexasArray, sextandsArray, squareSextandsArray = GenerateHexas(hexasNum)
    start = 1
    length = int(squareSextandsArray[hexasNum - 1])
    combosArray = ViewCombo(hexasNum, start, length)
    return combosArray

@jit(fastmath = True)
def FindAverageGap(hexasNum):
    """ 
        Description
        -----------
        Displays the expected average gap between valid combos (hexorial / Lexorial)

        numba.jit Parameters
        --------------------
        fastmath = True

        Parameters
        ----------
        hexasNum: The number of desired hexas to check
        
        Returns:
        --------
        num: Hexorial of number of hexas checked
        denom: Lexorial of number of hexas checked
        gap: average of hexorial/lexorial

    """

    hexasArray, sextandsArray, squareSextandsArray = GenerateHexas(hexasNum)
    gap, num, denom = 1,1,1
    for i in range(0,hexasNum):
        num *= hexasArray[i]
        denom *= hexasArray[i]-2
    gap = num/denom

    return num, denom, gap

@jit(fastmath = True)
def ValidCoordinates(hexasNum):
    """ 
        Description
        -----------
        Prints coordinates (x, y) where x is the number of hexas checked and y is the number of valid combos in the
        critical area as well as the number of Hexas checked. 

        numba.jit Parameters
        --------------------
        fastmath = True

        Parameters
        ----------
        hexasNum: The number of desired hexas to check


    """
    validNum = 0
    # Generate arrays
    hexasArray, sextandsArray, squareSextandsArray = GenerateHexas(hexasNum)

    # coordinates list
    coor_list = []

    print("Hexas Checked: ", hexasNum)
    for i in range(2, hexasNum + 1): # Cycle through all hexa pairs
        validNum = 0
        x = str(i)
        for j in range(int(squareSextandsArray[i-2]), int(squareSextandsArray[i-1] + 1)):
            valid = True
            for k in range(i):
                result1 = ((6 * j) % hexasArray[k] == 1)
                result2 = (6 * j) % hexasArray[k] == hexasArray[k] - 1
                if(result1 or result2):
                    valid = False

            if(valid):
                validNum += 1
            y = str(validNum)

        print_statement = str(x) + "," + str(y)
        print(print_statement)
        coor_list.append(print_statement)
        write_valid_coordinates(hexasNum, coor_list)

    return coor_list

def write_valid_coordinates(hexasNum, coor_list):
    """ 
        Description
        -----------
        writes to file for valid coordinates called valid_coordinates.txt

        Parameters
        ----------
        hexasNum: The number of checked hexas
        coors_list: A list of coordinates

    """
    file_name = "valid_coordinates.txt"
    if os.path.exists(file_name):
        os.remove(file_name)

    with open("valid_coordinates.txt", "a") as file:
        hexas_checked = "Hexas Checked = " + str(hexasNum)
        file.write(hexas_checked)
        file.write("\n")
        for element in coor_list:
            file.write(element)
            file.write("\n")


@jit(fastmath = True)
def GenerateCombos(combosNum):
    """ 
        Description
        -----------
        Combines functionality of FindInvalidChains() and ViewChains() to generate multiple combos 
        and inputes data to a list with the combos. 

        numba.jit Parameters
        --------------------
        fastmath = True

        Parameters
        ----------
        hexasNum: The number of desired hexas to check
        
        Returns:
        --------
        combosList: a list containing the combos

    """
    # boolean variables
    adv = True 
    valid = True

    # combos_array initialized with size of hexasNum
    combosArray = np.empty(combosNum)
    combosList = []
    hexasArray, sextandsArray, squareSextands_array = GenerateHexas(combosNum)

    # integer varaibles
    index = 1
    invalidChainLength = 0
    maxChainLength = 0
    invalidStart = 0

    # float variables 
    chainLengthSum = 0.0
    chainsNum = 0.0

    while (adv):
        adv = False
        valid = True

        printStatement = str(str(index) + ": ")
        for i in range(0 , len(combosArray)):
            combosArray[i] = (index % hexasArray[i])

            if(combosArray[i] != 0):
                adv = True
            
            if(i % 2 == 0):
                result1 = combosArray[i] == ((i + 2) / 2) 
                result2 = combosArray[i] == hexasArray[i] - ((i + 2) / 2)
                if (result1) or (result2):
                    valid = False

            elif(i % 2 == 1):
                result3 = combosArray[i] == ((i + 1) / 2)
                result4 = combosArray[i] == hexasArray[i] - ((i + 1) / 2)
                if (result3) or (result4):
                    valid = False
            
            printStatement += " "
            printStatement += str(combosArray[i])

        if(valid):
            printStatement += " <"
            combosList.append(printStatement)
            chainLengthSum += invalidChainLength
            chainsNum+=1
            invalidChainLength = 0
        else:
            invalidChainLength +=1 

            if(invalidChainLength > maxChainLength):
                maxChainLength = invalidChainLength
                invalidStart = index - maxChainLength + 1

        index+=1
        
    return combosList, maxChainLength, invalidStart

@jit(fastmath = True)
def ValidNumApproximation(hexasNum):

    """ 
        Description
        -----------
        Calculates an approximated for the expected number of valid combos within the domain (i.e. [1, A] 
        where A is the upper bound of the critical area), counts the true number of valid combos within the domain, 
        and displays the error between them.

        numba.jit Parameters
        --------------------
        fastmath = True

        Parameters
        ----------
        hexasNum: The number of desired hexas to check
        
        Returns:
        --------
        validList: A list containing the valid combos within the domain.
        endPoint: The end of the domain area.
        prodApprox: the approximated number of valid combos by taking quotient of the lesser hexorial and the true hexorial,
		            then multiplying that by the index, which in this case is the square-sextand of the greatest hexa being examined, i.e.
		            the upper boundary of the critical area.
        prodTrue:   prodTrue is the actual number of valid combos counted within the range of [1, A], where A is the upper boundary of the
		            critical area.
        errorPercentage: a percentage of the error. 

    """


    # Generate arrays  
    hexasArray, sextandsArray, squareSextandsArray = GenerateHexas(hexasNum)
    validList = []

    # integers
    endPoint = int(squareSextandsArray[hexasNum - 1])

    # floats
    prodTrue = 0.0
    prodApprox = 1.0

    # boolean values
    validCombo = False

    for i in range(0, endPoint):
        validCombo = True
        for j in range(0, hexasNum):
            result1 = i % hexasArray[j] == sextandsArray[j]
            result2 = i % hexasArray[j] == (hexasArray[j] - sextandsArray[j])
            if (result1) or (result2):
                if(i != sextandsArray[j]):
                    validCombo = False
                    break
        
        if(validCombo == True):
            prodTrue+=1
            printStatement = "Valid at " + str(i)
            validList.append(printStatement)
                
    for j in range(0, hexasNum):
        prodApprox *= ((float(hexasArray[j] - 2)) / (float(hexasArray[j])))
    
    prodApprox *= endPoint
    error = (prodTrue - prodApprox) / float(prodTrue)
    errorPercentage = error * 100

    return validList, endPoint, prodApprox, prodTrue, errorPercentage
