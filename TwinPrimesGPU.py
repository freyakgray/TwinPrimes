import numpy as np
from numba import cuda
from numpy.lib import math

stream = cuda.stream()

@cuda.jit
def GenerateHexasGPU(hexaArray: np.array):
    """
    Generates hexas, sextands and square sextands using a GPU

    Parameters: 
    hexaArray (numpy array): an empty numpy array where the hexas, sextands and square sextands will be populated. 
    Size of the array will determine the number of hexas, sextands and square sextands  generated. 
    The array must be sent to the host with cuda.to_device.
    """
    hexas = hexaArray.size
    x,y = cuda.grid(2)
    if(x < hexaArray.shape[0] and y < hexaArray.shape[1]):
        if(x == 0 ):
            hexaArray[0,y] = 3*(y + 1) + (3/2) - ((-1)**(y + 1) * (1/2))
        if(x == 1):
            hexaArray[1,y] = ((1/2) * (y+1)) + (1/4) + ((1/4) * (-1)**((y+1) - 1))
        if(x == 2):
            currentSextand = ((1/2) * (y+1)) + (1/4) + ((1/4) * (-1)**((y+1) - 1))
            if (y % 2 == 0):
                hexaArray[2,y] = 6*(currentSextand**2) - 2*currentSextand
            else:
                hexaArray[2,y] = 6*(currentSextand**2) + 2*currentSextand

def RunGenerateHexasGPU(hexas: int):
    """
    Runs GenerateHexasGPU kernel. Initializes array, sends it to the GPU, runs the kernel and returns the array to the host.
    
    Parameters: 
    hexas (int): the number of hexas to generate

    Returns:
    hexaArray (numpy array): an array of hexas, sextands and square sextands of size hexas
    """
    hexaArray = np.empty([3,hexas], dtype = np.uint64)

    deviceHexa = cuda.to_device(hexaArray, stream = stream)

    threadsPerBlock = (16,16)
    blocksPerGridX = math.ceil(3 / threadsPerBlock[0])
    blocksPerGridY = math.ceil(hexas / threadsPerBlock[1])
    blocksPerGrid = (blocksPerGridX,blocksPerGridY)
    GenerateHexasGPU[blocksPerGrid, threadsPerBlock](deviceHexa)
    hexaArray = deviceHexa.copy_to_host(stream = stream)
    
    return hexaArray

@cuda.jit
def GenerateCombosGPU(hexasChecked: int, length: int, hexaArray: np.array, comboArray: np.array):
    """
    Generates combos of length hexasChecked and checks for validity. First column is the index.
    Last column indicates validity, 0 for invalid, 1 for valid.
    
    Parameters: 
    hexasChecked (int): The number of hexas checked (must be less than the number of hexas generated)
    length (int): the last index to check combo validity
    hexaArray (numpy array): An array of hexas, sextands and square sextands
    comboArray (numpy array): A 2d array that the function will alter with the index, combo and validity
    """
    x,y = cuda.grid(2)  
    if(x < length and y < hexasChecked):
      if(y == 0):
        comboArray[x,0] = x
      if(y!= 0 or y!= (hexasChecked + 2)):
        comboArray[x, (y + 1)] = (x % hexaArray[0,y])
        if(x % hexaArray[0,y] == hexaArray[1,y]) or (x % hexaArray[0,y] == hexaArray[0,y] - hexaArray[1,y]):
          comboArray[x,-1] = 0

def RunGenerateCombosGPU(hexasChecked: int, length: int, hexaArray: np.array):
    """
    Runs GeneratesCombosGPU kernel. Initializes arrays, sends them to the GPU, runs the kernel and returns the arrays to the host.
    
    Parameters:
    hexasChecked (int): The number of hexas checked (must be less than the number of hexas generated)
    length int): The number of indices to check
    
    Returns: 
    combosLArray (numpy array): A 2d array of combos and their validity 
    """
    comboArray = np.zeros([length, (hexasChecked + 2)],dtype = np.uint64)
    comboArray[:,-1] = 1
    
    deviceCombo = cuda.to_device(comboArray, stream = stream)
    deviceHexa = cuda.to_device(hexaArray, stream = stream)

    threadsPerBlock = (32,32)
    blocksPerGridX = math.ceil(length / threadsPerBlock[0])
    blocksPerGridY = math.ceil(hexasChecked / threadsPerBlock[1])
    blocksPerGrid = (blocksPerGridX,blocksPerGridY)
    GenerateCombosGPU[blocksPerGrid, threadsPerBlock](hexasChecked, length, deviceHexa, deviceCombo)

    comboArray = deviceCombo.copy_to_host(stream = stream)
    return comboArray

def FindInvalidChainsGPU(hexasChecked: int, hexaArray: np.array):
    """
    Determines the longest chain of consecutive invalid indices. Must pass in an array generated with GenerateComboArray
    
    Parameters: 
    hexasChecked (int): The number of hexas to be checked
    hexaArray (numpyArray): An array of hexas, sextands and square sextands

    Returns: 
    invalidStart (int): start of the longest invalid chain
    maxInvalid (int): the length of the longest invalid chain
    criticalZoneSize (int): the size of the critical area
    """
    invalidStart = 0
    invalidLength = 0
    maxInvalid = 0
    hexorial = 1
    
    for i in range(hexasChecked):
        hexorial *= hexaArray[0,i]
    hexorial = int((hexorial - 1)/2)

    comboArray = RunGenerateCombosGPU(hexasChecked,hexorial,hexaArray)

    for i in range(hexorial):
        if(comboArray[i,-1] == 0):
            invalidLength += 1
            if(maxInvalid < invalidLength):
                maxInvalid = invalidLength
                invalidStart = i + 1 - maxInvalid
        else:
            invalidLength = 0

    criticalZoneSize = (hexaArray[2,hexasChecked - 1] - hexaArray[2,hexasChecked - 2])
    return invalidStart, maxInvalid, criticalZoneSize

def ViewCritCombosGPU(hexasChecked: int, comboArray: np.array):
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
 
def FindAverageGapGPU(hexasChecked: int, hexaArray: np.array):
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
    for i in range(hexasChecked):
        num *= int(hexaArray[0,i])
        denom *= int(hexaArray[0,i])-2
    gap = num/denom
    return num, denom, gap
  
def ValidCoordinatesGPU(comboArray: np.array, hexaArray: np.array):
    """
    Calculates coordinates where x is the number of hexas checked and y is the number of valid combos in critical area.

    Parameters:
    comboArray (numpy array): An array of combos generated with GenerateComboGPU. Array must have 
    more indices than the critical area. 
    hexaArray (numpy array): An array of hexas, sextands and square sextands generated with GenerateHexasGPU.

    Returns: 
    coordinatesArray (numpy array): An array of coordinates where the first column is the number of hexas checked 
    and the second column is the number of valid combos in critical area
    """
    coordinatesArray = np.zeros([(comboArray.shape[1] - 3),2],dtype = int)

    for i in range(2, comboArray.shape[1] - 1):
        coordinatesArray[i-2,0] = i
        validNum = 0
        for j in range(int(hexaArray[2,i-2]), int(hexaArray[2, i-1])):
            if(comboArray[j,-1] == 1):
                validNum += 1
        coordinatesArray[i-2,1] = validNum
    return coordinatesArray

def ValidNumApproximationGPU(hexasChecked: int, hexaArray: np.array, comboArray: np.array):
    """
    Calculates the expected number of valid combos within the domain (i.e. [1, A] where A is the upper bound of
    the critical area), calculates the actual number of valid combos and calulates the error between the two.
    
    Parameters: 
    hexasChecked (int): The number of hexas to be checked
    hexaArray (numpy array): An array of hexas, sextands and square sextands generated with GenerateHexasGPU
    comboArray (numpy array): An array of combos generated with GenerateCombosGPU. The array must have been generated with at least hexasChecked of hexas.

    Returns: 
    comboApproximation (float): The expected number of valid combos
    comboTrue (int): The actual number of valid combos
    errorPercent (int): The error between comboApproximation and comboTrue
    """
    endPoint = int(hexaArray[2,hexasChecked - 1])
    
    comboApproximation = 1
    for i in range(hexasChecked):
        comboApproximation *= (float(hexaArray[0,i]-2))/(float(hexaArray[0,i]))
    comboApproximation *= endPoint

    comboTrue = np.count_nonzero(comboArray[1:endPoint,-1:])
    error = abs(comboTrue - comboApproximation)/comboTrue
    errorPercent = error * 100
    return comboApproximation, comboTrue, errorPercent

def ViewCritAreaGPU(hexaArray):
    """
    Calculates the start and end indices of the critical area
    
    Parameters:
    hexaArray (numpy array): An array of hexas, sextands and square sextands generated with GenerateHexasGPU

    Returns:
    start (int): start of the critical area
    end (int): end of the critical area
    """
    length = hexaArray.shape[1]
    start = hexaArray[2,length - 2]
    end = hexaArray[2,length - 1]
    return start, end
