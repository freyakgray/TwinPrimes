import TwinPrimes as tp

def test_FindAverageGap():
    tp.hexasList.clear()
    tp.sextandsList.clear()
    tp.squareSextandsList.clear()
    tp.GenerateHexas(25)
    assert tp.FindAverageGap(2) == (35, 15, (35/15))
    assert tp.FindAverageGap(5) == (85085, 22275, (85085/22275))
    assert tp.FindAverageGap(25) == (80118103117639340983549243596751203125, 7650888424384967051538892125278671875, 
    (80118103117639340983549243596751203125/7650888424384967051538892125278671875))