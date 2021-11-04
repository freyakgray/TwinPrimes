import TwinPrimes as tp
import FastTwinPrimes as ftp
import time
from numba import jit
import pandas as pd


# Global Variables 
size = 10000
hexas_num = 3
index = 28
hexas_checked = 3
start = 20
length = 4


def run_twin_primes():
    start_tp = time.time()  
    tp.GenerateHexas(size)
    tp.FindInvalidChains(hexas_num)
    tp.GenerateCombo(hexas_num, index)
    tp.ViewCombo(hexas_checked, start, length)
    tp.ViewCritCombos(hexas_checked)
    tp.FindAverageGap(hexas_checked)
    tp.ValidCoordinates(hexas_num)
    tp.GenerateCombos(hexas_num)
    tp.ValidNumApproximation(hexas_num)
    end_tp = time.time()
    elapsed_tp = end_tp - start_tp
    return elapsed_tp

def run_numba_twin_primes():
    start_ftp = time.time()
    ftp.GenerateHexas(size)
    ftp.FindInvalidChains(hexas_num)
    ftp.GenerateCombo(hexas_num, index)
    ftp.ViewCombo(hexas_checked, start, length)
    ftp.ViewCritCombos(hexas_checked)
    ftp.FindAverageGap(hexas_checked)
    ftp.ValidCoordinates(hexas_num)
    ftp.GenerateCombos(hexas_num)
    ftp.ValidNumApproximation(hexas_num)
    end_ftp = time.time()
    elapsed_ftp = end_ftp - start_ftp
    return elapsed_ftp



print()
print("Comparing times....")
print("At Size: ", size)
print("At Hexas Number: " , hexas_num)
time_ftp = run_numba_twin_primes()
time_tp = run_twin_primes()
print("List: ", time_tp)
print("numba.jit: ", time_ftp)

size_req = (size >= 10000000 or hexas_num >= 6)
if(size_req):
    print(run_numba_twin_primes())
else:
    print(run_twin_primes())

    


