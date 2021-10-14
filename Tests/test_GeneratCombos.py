import TwinPrimes as tp
import os
  
def test_GenerateCombos():
    # Populate hexasList and squareSextandsList
    sxtnd = 0
    for i in range(5000):
        if((i + 1) % 2 == 1):
            tp.hexasList.append((3 * (i + 2)) - 1)
            sxtnd += 1
               
        else:
            tp.hexasList.append((3 * (i + 1)) + 1)

        tp.squareSextandsList.append(((tp.hexasList[i] * tp.hexasList[i]) - 1) / 6)

    # run GenerateCombos(hexasNum = 2)
    tp.GenerateCombos(hexasNum = 2)

    # Test file creation
    file_name = "generate_combos.txt"
    path_to_file = os.path.join(os.getcwd(), file_name)
    assert os.path.exists(path_to_file)

    # Test the hexas checked in the file
    with open(path_to_file, "r") as file:
        lines_in_file = file.read().split("\n")
    
    correct_file_content_0 = "1:  1 1"
    assert lines_in_file[0] == correct_file_content_0

    correct_file_content_1 = "2:  2 2 <"
    assert lines_in_file[1] == correct_file_content_1
    
    correct_file_content_2 = "3:  3 3 <"
    assert lines_in_file[2] == correct_file_content_2
    correct_file_content_3 = "4:  4 4"
    assert lines_in_file[3] == correct_file_content_3

    correct_file_content_4 = "5:  0 5 <"
    assert lines_in_file[4] == correct_file_content_4

    correct_file_content_5 = "6:  1 6"
    assert lines_in_file[5] == correct_file_content_5

    correct_file_content_6 = "7:  2 0 <"
    assert lines_in_file[6] == correct_file_content_6

    correct_file_content_7 = "8:  3 1"
    assert lines_in_file[7] == correct_file_content_7

    correct_file_content_8 = "9:  4 2"
    assert lines_in_file[8] == correct_file_content_8

    correct_file_content_9 = "10:  0 3 <"
    assert lines_in_file[9] == correct_file_content_9

    correct_file_content_10 = "11:  1 4"
    assert lines_in_file[10] == correct_file_content_10

    correct_file_content_11 = "12:  2 5 <"
    assert lines_in_file[11] == correct_file_content_11

    correct_file_content_12 = "13:  3 6"
    assert lines_in_file[12] == correct_file_content_12
    
    correct_file_content_13 = "14:  4 0"
    assert lines_in_file[13] == correct_file_content_13

    correct_file_content_14 = "15:  0 1"
    assert lines_in_file[14] == correct_file_content_14

    correct_file_content_15 = "16:  1 2"
    assert lines_in_file[15] == correct_file_content_15

    correct_file_content_16 = "17:  2 3 <"
    assert lines_in_file[16] == correct_file_content_16

    correct_file_content_17 = "18:  3 4 <"
    assert lines_in_file[17] == correct_file_content_17

    correct_file_content_18 = "19:  4 5"
    assert lines_in_file[18] == correct_file_content_18

    correct_file_content_19 = "20:  0 6"
    assert lines_in_file[19] == correct_file_content_19

    correct_file_content_20 = "21:  1 0"
    assert lines_in_file[20] == correct_file_content_20

    correct_file_content_21 = "22:  2 1"
    assert lines_in_file[21] == correct_file_content_21

    correct_file_content_22 = "23:  3 2 <"
    assert lines_in_file[22] == correct_file_content_22

    correct_file_content_23 = "24:  4 3"
    assert lines_in_file[23] == correct_file_content_23
    
    correct_file_content_24 = "25:  0 4 <"
    assert lines_in_file[24] == correct_file_content_24

    correct_file_content_25 = "26:  1 5"
    assert lines_in_file[25] == correct_file_content_25

    correct_file_content_26 = "27:  2 6"
    assert lines_in_file[26] == correct_file_content_26

    correct_file_content_27 = "28:  3 0 <"
    assert lines_in_file[27] == correct_file_content_27

    correct_file_content_28 = "29:  4 1"
    assert lines_in_file[28] == correct_file_content_28

    correct_file_content_29 = "30:  0 2 <"
    assert lines_in_file[29] == correct_file_content_29

    correct_file_content_30 = "31:  1 3"
    assert lines_in_file[30] == correct_file_content_30

    correct_file_content_31 = "32:  2 4 <"
    assert lines_in_file[31] == correct_file_content_31

    correct_file_content_32 = "33:  3 5 <"
    assert lines_in_file[32] == correct_file_content_32

    correct_file_content_33 = "34:  4 6"
    assert lines_in_file[33] == correct_file_content_33

    correct_file_content_34 = "35:  0 0 <"
    assert lines_in_file[34] == correct_file_content_34

    correct_file_content_35 = "Max chain length: 4"
    assert lines_in_file[35] == correct_file_content_35

    correct_file_content_36 = "Average gap between valid combos: 1.3333333333333333"
    assert lines_in_file[36] == correct_file_content_36

    correct_file_content_37 = "Max chain start: 13"
    assert lines_in_file[37] == correct_file_content_37

test_GenerateCombos()
