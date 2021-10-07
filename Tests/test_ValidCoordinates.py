import TwinPrimes as tp
import os
  

def test_ValidCoordinates():
    hexasNum = 10
    # Populate hexasList and squareSextandsList
    sxtnd = 0
    for i in range(5000):
        if((i + 1) % 2 == 1):
            tp.hexasList.append((3 * (i + 2)) - 1)
            sxtnd += 1
               
        else:
            tp.hexasList.append((3 * (i + 1)) + 1)

        tp.squareSextandsList.append(((tp.hexasList[i] * tp.hexasList[i]) - 1) / 6)

    # Run ValidateCoordinates with hexasNum = 10
    tp.ValidCoordinates(hexasNum)

    # Test file creation
    file_name = "valid_coordinates.txt"
    path_to_file = os.path.join(os.getcwd(), file_name)
    assert os.path.exists(path_to_file)

    # Test the hexas checked in the file
    with open(path_to_file, "r") as file:
        lines_in_file = file.read().split("\n")
    
    # assert statement
    assert_hexas_checked = "Hexas checked: " + str(hexasNum)
    assert lines_in_file[0] == assert_hexas_checked
   # Test the content of the file with the input hexasNum as the number of hexas checked
    assert_file_content = ["(2,2)", "(3,4)" , "(4,2)", "(5,7)", "(6,2)", "(7,4)", "(8,3)", "(9,5)", "(10,2)"]
    index = 0
    for line in assert_file_content:
        index += 1
        #print(lines_in_file[index], " == ", line)
        assert line == lines_in_file[index]