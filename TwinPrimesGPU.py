import numpy as np
from numba import njit, prange, cuda, jit
import TwinPrimes as tp
import time

hexaArrayGPU = np.empty(100000000, dtype = int)
sextandsArrayGPU = np.empty(100000000, dtype = int)
squareSextandsArrayGPU = np.empty(100000000, dtype = int)
hexaArray = np.empty(100000000, dtype = int)
sextandsArray = np.empty(100000000, dtype = int)
squareSextandsArray = np.empty(100000000, dtype = int)
hexasList = []
sextandsList = []
squareSextandsList = []


@cuda.jit
def GenerateHexasGPU(hexas, hexaArrayGPU, sextandsArrayGPU, squareSextandsArrayGPU):
    for i in prange(hexas):
        pos = cuda.grid(1)
        hexaArrayGPU[pos] = 3*(pos + 1) + (3/2) - ((-1)**(pos + 1) * (1/2))
        sextandsArrayGPU[pos] = ((1/2) * (pos+1)) + (1/4) + ((1/4) * (-1)**((pos+1) - 1))
        if i % 2 == 0:
            squareSextandsArrayGPU[pos] = 6*(sextandsArrayGPU[pos]**2) - 2*sextandsArrayGPU[pos]
        else:
            squareSextandsArrayGPU[pos] = 6*(sextandsArrayGPU[pos]**2) + 2*sextandsArrayGPU[pos] 

@njit(fastmath = True)
def GenerateHexasPara(hexas, hexaArray, sextandsArray, squareSextandsArray):
    for i in prange(hexas):
        hexaArray[i] = 3*(i + 1) + (3/2) - ((-1)**(i + 1) * (1/2))
        sextandsArray[i] = ((1/2) * (i+1)) + (1/4) + ((1/4) * (-1)**((i+1) - 1))
        if i % 2 == 0:
            squareSextandsArray[i] = 6*(sextandsArray[i]**2) - 2*sextandsArray[i]
        else:
            squareSextandsArray[i] = 6*(sextandsArray[i]**2) + 2*sextandsArray[i] 



threads_per_block = 32
blocks_per_grid = (hexaArrayGPU.size +(threads_per_block -1))
#blocks_per_grid = (hexaArrayGPU.shape[0]/threads_per_block)
d_HexaArray = cuda.to_device(hexaArrayGPU)
d_SextandsArray = cuda.to_device(sextandsArrayGPU)
d_SextandsArray = cuda.to_device(squareSextandsArrayGPU)

print('Generate Hexas GPU for ' + str(hexaArrayGPU.size) + ' hexas')
start = time.time()
GenerateHexasGPU[blocks_per_grid, threads_per_block](100000000, d_HexaArray,d_SextandsArray, d_SextandsArray )
end = time.time()
print("GPU time elapsed = %s" % (end - start))
#gpuArray = d_ary.copy_to_host()
#print(gpuArray)

print('Generate Hexas Numba for ' + str(hexaArrayGPU.size) + ' hexas')
start = time.time()
GenerateHexasPara(100000000, hexaArray, sextandsArray, squareSextandsArray)
end = time.time()
print("Numba time elapsed = %s" % (end - start))

print('Generate Hexas normal for ' + str(hexaArrayGPU.size) + ' hexas')
start = time.time()
tp.GenerateHexas(100000000)
end = time.time()
print("normal time elapsed = %s" % (end - start))

