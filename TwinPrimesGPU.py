import numpy as np
from numba import njit, prange, cuda
import TwinPrimes as tp
import time

hexaArray = np.empty(100000, dtype = int)
sextandsArray = np.empty(100000, dtype = int)
squareSextandsArray = np.empty(100000, dtype = int)
hexaArrayGPU = np.empty(100000, dtype = int)
sextandsArrayGPU = np.empty(100000, dtype = int)
squareSextandsArrayGPU = np.empty(100000, dtype = int)

@njit(fastmath = True)
def GenerateHexasPara(hexas, hexaArray, sextandsArray, squareSextandsArray):
    for i in prange(hexas):
        hexaArray[i] = 3*(i + 1) + (3/2) - ((-1)**(i + 1) * (1/2))
        sextandsArray[i] = ((1/2) * (i+1)) + (1/4) + ((1/4) * (-1)**((i+1) - 1))
        if i % 2 == 0:
            squareSextandsArray[i] = 6*(sextandsArray[i]**2) - 2*sextandsArray[i]
        else:
            squareSextandsArray[i] = 6*(sextandsArray[i]**2) + 2*sextandsArray[i] 

@cuda.jit
def GenerateHexasGPU(hexas, hexaArray, sextandsArray, squareSextandsArray):
    for i in prange(hexas):
        hexaArray[i] = 3*(i + 1) + (3/2) - ((-1)**(i + 1) * (1/2))
        sextandsArray[i] = ((1/2) * (i+1)) + (1/4) + ((1/4) * (-1)**((i+1) - 1))
        if i % 2 == 0:
            squareSextandsArray[i] = 6*(sextandsArray[i]**2) - 2*sextandsArray[i]
        else:
            squareSextandsArray[i] = 6*(sextandsArray[i]**2) + 2*sextandsArray[i] 

start = time.time()
GenerateHexasPara(100000, hexaArray, sextandsArray, squareSextandsArray)
end = time.time()
print("Elapsed (with compilation) = %s" % (end - start))

start = time.time()
GenerateHexasPara(100000, hexaArray, sextandsArray, squareSextandsArray)
end = time.time()
print("para compElapsed (with compilation) = %s" % (end - start))

#start = time.time()
#GenerateHexasGPU(100000, hexaArrayGPU, sextandsArrayGPU, squareSextandsArrayGPU)
#end = time.time()
#print("GPU Elapsed (with compilation) = %s" % (end - start))

#start = time.time()
#GenerateHexasGPU(100000, hexaArrayGPU, sextandsArrayGPU, squareSextandsArrayGPU)
#end = time.time()
#print("GPU comp para compElapsed (with compilation) = %s" % (end - start))

start = time.time()
tp.GenerateHexas(100000)
end = time.time()
print("norm Elapsed (with compilation) = %s" % (end - start))

