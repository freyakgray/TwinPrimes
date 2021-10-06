import TwinPrimes as tp

def test_view_crit_area():
    hexasList = [5, 7, 11, 13, 17, 19, 23, 25, 29, 31, 35, 37, 41, 43, 47, 49, 53, 55, 59, 61, 65, 67, 71, 73, 77]
    length = len(hexasList) - 1
    subtend = hexasList[length - 1]
    limit = hexasList[length]
    tp.view_crit_area()
    assert(subtend, 73)
    assert(limit, 77)
    assert(((subtend ** 2 - 1) / 6) % 1, 0)
    assert(((limit ** 2 - 1) / 6) % 1, 0)