import TwinPrimes as tp

def test_GenerateHexas():
    tp.GenerateHexas(25)
    assert tp.hexasList == [5, 7, 11, 13, 17, 19, 23, 25, 29, 31, 35, 37, 41, 43, 
    47, 49, 53, 55, 59, 61, 65, 67, 71, 73, 77]
    assert tp.sextandsList == [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11, 12, 12, 13]



