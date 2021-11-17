import numpy as np
from numba import njit, cuda
from numpy.lib import math

stream = cuda.stream()

@cuda.jit
def GenerateHexasGPU(hexaArray, sextandsArray, squareSextandsArray):
    """
    Generates hexas, sextands and square sextands using a GPU

    Parameters: 
    hexaArray (numpy array): an empty numpy array where the hexas will be populated. 
    Size of the array will determine the number of hexas generated. The array must be sent to the host with cuda.to_device.

    sextandsArray (numpy array): an empty numpy array where the sextands will be populated. 
    Size of array must match the size of the hexaArray. The array must be sent to the host with cuda.to_device.

    squareSextandsArray (numpy array): an empty numpy array where the square sextands will be populated.
    Size of array must match the size of the hexaArray. The array must be sent to the host with cuda.to_device.
    """
    hexas = hexaArray.size
    pos = cuda.grid(1)
    if(pos < hexas):
        hexaArray[pos] = 3*(pos + 1) + (3/2) - ((-1)**(pos + 1) * (1/2))
        sextandsArray[pos] = ((1/2) * (pos+1)) + (1/4) + ((1/4) * (-1)**((pos+1) - 1))
        if pos % 2 == 0:
            squareSextandsArray[pos] = 6*(sextandsArray[pos]**2) - 2*sextandsArray[pos]
        else:
            squareSextandsArray[pos] = 6*(sextandsArray[pos]**2) + 2*sextandsArray[pos]

def RunGenerateHexasGPU(hexas: int):
    """
    Runs GenerateHexasGPU kernel. Initializes arrays, sends them to the GPU, runs the kernel and returns the arrays to the host.
    
    Parameters: 
    hexas (int): the number of hexas to generate

    Returns:
    hexaArray (numpy array): an array of hexas of size hexas
    sextandsArray (numpy array): an array of sextands of size hexas
    squareSextandsArray (numpy array): an array of square sextands of size hexas
    """
    hexaArray = np.empty(hexas, dtype = np.uint64)
    sextandsArray = np.empty(hexas, dtype = np.uint64)
    squareSextandsArray = np.empty(hexas, dtype = np.uint64)

    deviceHexa = cuda.to_device(hexaArray, stream = stream)
    deviceSextands = cuda.to_device(sextandsArray, stream = stream)
    deviceSquareSextands = cuda.to_device(squareSextandsArray, stream = stream)

    threadsPerBlock = 32
    blocksPerGrid = (hexaArray.size + (threadsPerBlock - 1)) // threadsPerBlock
    GenerateHexasGPU[blocksPerGrid, threadsPerBlock](deviceHexa,deviceSextands,deviceSquareSextands)
    hexaArray = deviceHexa.copy_to_host(stream = stream)
    sextandsArray = deviceSextands.copy_to_host(stream = stream)
    squareSextandsArray = deviceSquareSextands.copy_to_host(stream = stream)
    
    return hexaArray,sextandsArray, squareSextandsArray

@cuda.jit
def GenerateCombosGPU(hexasChecked, start, end, hexaArray, comboArray):
    """
    Generates combos of length hexasChecked and checks for validity. First column is the index.
    Last column indicates validity, 0 for invalid, 1 for valid.
    
    Parameters: 
    hexasChecked (int): The number of hexas checked (must be less than the number of hexas generated)
    start (int): first index to check combo validity
    end (int): the last index to check combo validity
    hexaArray (numpy array): An array of hexas
    comboArray (numpy array): A 2d array that the function will alter with the index, combo and validity
    """
    x,y = cuda.grid(2)
    if(x < end and y < hexasChecked):
      if(y == 0):
        comboArray[x,0] = x
      if(y!= 0 or y!= (hexasChecked + 2)):
        comboArray[x, (y + 1)] = (x % hexaArray[y])
        if(x % hexaArray[y] == 1) or (x % hexaArray[y] == hexaArray[y] - 1):
          comboArray[x,-1] = 0

def RunGenerateCombosGPU(hexasChecked, start, length, hexaArray):
    """
    Runs GeneratesCombosGPU kernel. Initializes arrays, sends them to the GPU, runs the kernel and returns the arrays to the host.
    
    Parameters:
    hexasChecked (int): The number of hexas checked (must be less than the number of hexas generated)
    start (int): first index to check combo validity
    length int): The number of indices to check
    
    Returns: 
    combosLArray (numpy array): A 2d array of combos and their validity 
    """
    end = start + length
    comboArray = np.zeros([length, (hexasChecked + 2)],dtype = int)
    comboArray[:,-1] = 1
    
    deviceCombo = cuda.to_device(comboArray, stream = stream)
    deviceHexa = cuda.to_device(hexaArray, stream = stream)

    threadsPerBlock = (32,32)
    blocksPerGridX = math.ceil(length / threadsPerBlock[0])
    blocksPerGridY = math.ceil(hexasChecked / threadsPerBlock[1])
    blocksPerGrid = (blocksPerGridX,blocksPerGridY)
    GenerateCombosGPU[blocksPerGrid, threadsPerBlock](hexasChecked, start, end, deviceHexa, deviceCombo)

    comboArray = deviceCombo.copy_to_host(stream = stream)
    return comboArray

def FindInvalidChainsGPU(comboArray, squareSextandsArray):
    """
    Determines the longest chain of consecutive invalid indices. Must pass in an array generated with GenerateComboArray
    
    Parameters: 
    comboArray (numpyArray): An array generated with GenerateComboArray
    squareSextandsArray (numpyArray): An array of square sextands generated with GenerateHexasGPU

    Returns: 
    invalidStart (int): start of the longest invalid chain
    maxInvalid (int): the length of the longest invalid chain
    criticalZoneSize (int): the size of the critical area
    """
    invalidStart = 0
    invalidLength = 0
    maxInvalid = 0

    for i in range(comboArray.shape[0]):
        if(comboArray[i,-1] == 0):
            invalidLength += 1
            if(maxInvalid < invalidLength):
                maxInvalid = invalidLength
                invalidStart = i + 1 - maxInvalid
        else:
            invalidLength = 0
    hexasChecked = comboArray.shape[1]-2
    criticalZoneSize = (squareSextandsArray[hexasChecked - 1] - squareSextandsArray[hexasChecked - 2])
    return invalidStart, maxInvalid, criticalZoneSize

def ViewCritCombosGPU(hexasChecked, comboArray):
    """
    Slices an array generated with GenerateComboArray to contain the combos of the critical area.

    Parameters: 
    hexasChecked (int): The number of hexas to be checked
    comboArray (numpy array): An array of combos generated with GenerateComboGPU. Array must have 
    more indices than the critical area.  
   
    RETURNS:
    critCombosArray (numpy array): An array of combos in the critical area
    """
    sextand = int(((1/2) * (hexasChecked)) + (1/4) + ((1/4) * (-1)**((hexasChecked) - 1)))
    if((hexasChecked - 1) % 2 == 0):
        endPoint = 6*(sextand**2) - 2*sextand
    else:
        endPoint = 6*(sextand**2) + 2*sextand
    critCombosArray = comboArray[:endPoint+1,:]
    return critCombosArray
 
def FindAverageGapGPU(hexasChecked, hexaArray):
    """
    Calculates the hexorial, lexorial and gap of a hexasChecked amount of hexas.
    
    Parameters: 
    hexasChecked (int): The number of hexas to be checked
    hexaArray (numpy array): An array of hexas, generated with GenerateHexasGPU 
    
    Returns:
    num (int): Hexorial of n hexas
    denom (int): Lexorial of n hexas
    gap (float): average of hexorial/lexorial
    """
    num, denom = 1,1
    for i in range(0,hexasChecked):
        num *= int(hexaArray[i])
        denom *= int(hexaArray[i])-2
    gap = num/denom
    return num, denom, gap
  
def ValidCoordinatesGPU(comboArray, squareSextandsArray):
    """
    Calculates coordinates where x is the number of hexas checked and y is the number of valid combos in critical area.

    Parameters:
    comboArray (numpy array): An array of combos generated with GenerateComboGPU. Array must have 
    more indices than the critical area. 
    squareSextandsArray (numpy array): An array of square sextands generated with GenerateHexasGPU.

    Returns: 
    coordinatesArray (numpy array): An array of coordinates where the first column is the number of hexas checked 
    and the second column is the number of valid combos in critical area
    """
    coordinatesArray = np.zeros([(comboArray.shape[1] - 3),2],dtype = int)

    for i in range(2, comboArray.shape[1] - 1):
        coordinatesArray[i-2,0] = i
        validNum = 0
        for j in range(int(squareSextandsArray[i-2]), int(squareSextandsArray[i-1]+1)):
            if(comboArray[j,-1] == 1):
                validNum += 1
        coordinatesArray[i-2,1] = validNum
    return coordinatesArray

def ValidNumApproximationGPU(hexasNum, hexaArray, squareSextandsArray, comboArray):
    """
    Calculates the expected number of valid combos within the domain (i.e. [1, A] where A is the upper bound of
    the critical area), calculates the actual number of valid combos and calulates the error between the two.
    
    Parameters: 
    hexasNum (int): The number of hexas to be checked
    hexaArray (numpy array): An array of square sextands generated with GenerateHexasGPU
    squareSextandsArray (numpy array): an array of hexas generated with GenerateHexasGPU
    comboArray (numpy array): An array of combos generated with GenerateCombosGPU. The array must have been generated with at least hexasNum of hexas.

    Returns: 
    comboApproximation (float): The expected number of valid combos
    comboTrue (int): The actual number of valid combos
    errorPercent (int): The error between comboApproximation and comboTrue
    """
    endPoint = int(squareSextandsArray[hexasNum - 1])
    
    comboApproximation = 1
    for i in range(hexasNum):
        comboApproximation *= (float(hexaArray[i]-2))/(float(hexaArray[i]))
    comboApproximation *= endPoint

    comboTrue = np.count_nonzero(comboArray[1:endPoint,-1:])
    error = abs(comboTrue - comboApproximation)/comboTrue
    errorPercent = error * 100
    return comboApproximation, comboTrue, errorPercent

def ViewCritAreaGPU(hexasArray):
    """
    Calculates the start and end indices of the critical area
    
    Parameters:
    hexasArray (numpy array): An array of hexas generated with GenerateHexasGPU

    Returns:
    start (int): start of the critical area
    end (int): end of the critical area
    """
    length = hexasArray.size - 1
    limit = hexasArray[length]
    subtend = hexasArray[length -1]
    start = int((subtend**2 - 1)/6)
    end = int((limit**2 - 1)/6)
    return start, end
