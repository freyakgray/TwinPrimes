import TwinPrimes as tp
import FastTwinPrimes as ftp
import time
from numba import jit
import pandas as pd


# Global Variables 
size = 1000
hexas_num = 6
index = 28
hexas_checked = 10
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
    print("List: " + str(elapsed_tp))

def run_fast_twin_primes():
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
    print("numba.jit: " + str(elapsed_ftp))

def best():
    size_req = (size >= 10000000 or hexas_num >= 6 or size >= 10000000)
    if(size_req):
        return run_fast_twin_primes()
    else:
        return run_twin_primes()


def compare_both():
    print("Comparing Both ... ")
    run_fast_twin_primes()
    run_twin_primes()
    
compare_both()
best()
    


