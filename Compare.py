import TwinPrimes as tp
import FastTwinPrimes as ftp
import time
from numba import jit
import pandas as pd

size = 1000


start_tp = time.time()
tp.GenerateHexas(size)
tp.FindInvalidChains(8)
tp.GenerateCombo(7, 28)
tp.ViewCombo(4, 20, 4)
end_tp = time.time()
elapsed_tp = end_tp - start_tp
print("Lists: ", elapsed_tp)

start_ftp = time.time()
ftp.GenerateHexas(size)
ftp.FindInvalidChains(8)
ftp.GenerateCombo(7, 28)
ftp.ViewCombo(4, 20, 4)
end_ftp = time.time()
elapsed_ftp = end_ftp - start_ftp
print("numba.jit: ", elapsed_ftp)




