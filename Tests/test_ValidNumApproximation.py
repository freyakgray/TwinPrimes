import TwinPrimes as tp
import os

def test_ValidNumApproximation():
    # Populate hexasList and squareSextandsList
    sxtnd = 0
    for i in range(5000):
        if((i + 1) % 2 == 1):
            tp.hexasList.append((3 * (i + 2)) - 1)
            sxtnd += 1
               
        else:
            tp.hexasList.append((3 * (i + 1)) + 1)

        tp.squareSextandsList.append(((tp.hexasList[i] * tp.hexasList[i]) - 1) / 6)
        tp.sextandsList.append(sxtnd)

    # run GenerateCombos(hexasNum = 2)
    tp.ValidNumApproximation(hexasNum = 2)

    # Test file creation
    file_name = "valid_num_approx.txt"
    path_to_file = os.path.join(os.getcwd(), file_name)
    assert os.path.exists(path_to_file)

    # Test the hexas checked in the file
    with open(path_to_file, "r") as file:
        lines_in_file = file.read().split("\n")
    
    correct_file_content_0 = "Valid at 2"
    assert lines_in_file[0] == correct_file_content_0

    correct_file_content_1 = "Valid at 3"
    assert lines_in_file[1] == correct_file_content_1

    correct_file_content_2 = "Valid at 5"
    assert lines_in_file[2] == correct_file_content_2

    correct_file_content_3 = "Valid at 7"
    assert lines_in_file[3] == correct_file_content_3

    correct_file_content_4 = "Checking to s = 8"
    assert lines_in_file[4] == correct_file_content_4

    correct_file_content_5 = "Approximate combos: 3.4285714285714284"
    assert lines_in_file[5] == correct_file_content_5

    correct_file_content_6 = 'Number of valid combos: 4.0'

    correct_file_content_7 = "Error: 14.28571428571429%"
    assert lines_in_file[7] == correct_file_content_7
    


test_ValidNumApproximation()