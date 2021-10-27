import TwinPrimes as tp
import FastTwinPrimes as ftp
import time
from numba import jit

test_size = 10000000
hexas_num = 8

print("###################################################################################")
print("GeneratHexas: \n Testing times @size = ", test_size, "...")
start = time.time()
ftp.GenerateHexas(test_size)
end = time.time()
print("numba.jit: ",end - start, "seconds")


start = time.time()
tp.GenerateHexas(test_size)
end = time.time()
print("lists: ",end - start, "seconds")
print("###################################################################################")

print("FindInvalidChains: \n Testing times @number of hexas ", hexas_num, "...")
start = time.time()
ftp.FindInvalidChains(test_size, hexas_num)
end = time.time()
print("numba.jit: ",end - start, "seconds")


start = time.time()
tp.FindInvalidChains(test_size, hexas_num)
end = time.time()
print("lists: ",end - start, "seconds")
print("###################################################################################")
