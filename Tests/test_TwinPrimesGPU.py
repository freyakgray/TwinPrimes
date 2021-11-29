import os
os.environ['NUMBA_ENABLE_CUDASIM'] = "1"
os.environ['DISABLE_JIT'] = "1"

import TwinPrimesGPU as gpu
import numpy as np

hexas = np.array([[5, 7, 11, 13, 17, 19, 23, 25, 29, 31, 35, 37, 41, 43, 
    47, 49, 53, 55, 59, 61, 65, 67, 71, 73, 77],
    [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11, 12, 12, 13],
    [4, 8, 20, 28, 48, 60, 88, 104, 140, 160, 204, 228, 280, 308, 368, 400, 468, 504, 580, 620, 704, 748, 840, 888, 988]])
correctCombo = np.array([[0,0,0,0,0,0,0,0],
                        [1,1,1,1,1,1,1,1],
                        [2,2,2,2,2,2,2,1],
                        [3,3,3,3,3,3,3,1],
                        [4,4,4,4,4,4,4,0],
                        [5,0,5,5,5,5,5,1],
                        [6,1,6,6,6,6,6,0],
                        [7,2,0,7,7,7,7,1],
                        [8,3,1,8,8,8,8,0],
                        [9,4,2,9,9,9,9,0],
                        [10,0,3,10,10,10,10,1],
                        [11,1,4,0,11,11,11,0],
                        [12,2,5,1,12,12,12,1],
                        [13,3,6,2,0,13,13,0],
                        [14,4,0,3,1,14,14,0],
                        [15,0,1,4,2,15,15,0],
                        [16,1,2,5,3,16,16,0],
                        [17,2,3,6,4,0,17,1],
                        [18,3,4,7,5,1,18,1],
                        [19,4,5,8,6,2,0,0],
                        [20,0,6,9,7,3,1,0],
                        [21,1,0,10,8,4,2,0],
                        [22,2,1,0,9,5,3,0],
                        [23,3,2,1,10,6,4,1],
                        [24,4,3,2,11,7,5,0],
                        [25,0,4,3,12,8,6,1],
                        [26,1,5,4,0,9,7,0],
                        [27,2,6,5,1,10,8,0],
                        [28,3,0,6,2,11,9,0],
                        [29,4,1,7,3,12,10,0],
                        [30,0,2,8,4,13,11,1],
                        [31,1,3,9,5,14,12,0],
                        [32,2,4,10,6,15,13,1],
                        [33,3,5,0,7,16,14,1],
                        [34,4,6,1,8,0,15,0],
                        [35,0,0,2,9,1,16,0],
                        [36,1,1,3,10,2,17,0],
                        [37,2,2,4,11,3,18,0],
                        [38,3,3,5,12,4,0,1],
                        [39,4,4,6,0,5,1,0],
                        [40,0,5,7,1,6,2,1],
                        [41,1,6,8,2,7,3,0],
                        [42,2,0,9,3,8,4,0],
                        [43,3,1,10,4,9,5,0],
                        [44,4,2,0,5,10,6,0],
                        [45,0,3,1,6,11,7,1],
                        [46,1,4,2,7,12,8,0],
                        [47,2,5,3,8,13,9,1],
                        [48,3,6,4,9,14,10,0],
                        [49,4,0,5,10,15,11,0],
                        [50,0,1,6,11,16,12,0],
                        [51,1,2,7,12,0,13,0],
                        [52,2,3,8,0,1,14,1],
                        [53,3,4,9,1,2,15,0],
                        [54,4,5,10,2,3,16,0],
                        [55,0,6,0,3,4,17,0],
                        [56,1,0,1,4,5,18,0],
                        [57,2,1,2,5,6,0,0],
                        [58,3,2,3,6,7,1,1],
                        [59,4,3,4,7,8,2,0],
                        [60,0,4,5,8,9,3,0]])
def test_GenerateHexasGPU():
    hexaArray = gpu.RunGenerateHexasGPU(25)
    assert np.array_equal(hexas, hexaArray) 

def test_GenerateCombosGPU():
    comboArray = gpu.RunGenerateCombosGPU(6,61,hexas)
    assert np.array_equal(correctCombo,comboArray)

def test_FindInvalidChainsGPU():
    invalidStart, maxInvalid, criticalZoneSize = gpu.FindInvalidChainsGPU(2,hexas)
    assert invalidStart == 13
    assert maxInvalid == 4
    assert criticalZoneSize == 4 

def test_ViewCritCombosGPU():
    critCombosArray = gpu.ViewCritCombosGPU(6,correctCombo)
    assert np.array_equal(correctCombo, critCombosArray)

def test_FindAverageGapGPU():
    num, denom, gap = gpu.FindAverageGapGPU(6, hexas)
    assert num == 1616615
    assert denom == 378675
    assert gap == 4.269135802469136

def test_ValidCoordinatesGPU():
    coordinates = gpu.ValidCoordinatesGPU(correctCombo, hexas)
    coarCorrect = np.array([[2, 2],
                            [3, 4],
                            [4, 2],
                            [5, 7],
                            [6, 2]])
    assert np.array_equal(coordinates, coarCorrect)

def test_ValidNumApproximationGPU():
    comboApproximation, comboTrue, errorPercent = gpu.ValidNumApproximationGPU(6, hexas, correctCombo)
    assert comboApproximation == 14.054366685945633
    assert comboTrue == 20
    assert errorPercent == 29.728166570271835

def test_ViewCritAreaGPU():
    start, end  = gpu.ViewCritAreaGPU(hexas)
    assert start == 888
    assert end == 988
