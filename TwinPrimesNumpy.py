import os
import numpy as np
from numpy.lib.function_base import append
from datetime import datetime
import sys
from pympler.asizeof import asizeof


class NumpyTPC:
    def __init__(self, array_size, hexas_num):
        self.array_size = array_size
        self.hexas_num = hexas_num
        
        # initialize empty numpy arrays 
        self.hexas_array = np.empty(self.array_size)
        self.sextands_array = np.empty(self.array_size)
        self.square_sextands_array = np.empty(self.array_size)

    def populate_arrays(self):
        # Populate hexas array and square_sextands_array
        start_time = datetime.now()
        sxtnd = 0
        for i in range(self.array_size):
            if((i + 1) % 2 == 1):
                self.hexas_array[i] =  ((3 * (i + 2)) - 1)
                sxtnd += 1
               
            else:
                self.hexas_array[i] = ((3 * (i + 1)) + 1)

            self.square_sextands_array[i] =  (((self.hexas_array[i] * self.hexas_array[i]) - 1) / 6)
            self.sextands_array[i] =  sxtnd
        end_time = datetime.now()
        print('Time for numpy arrays to populate ---- > Duration: {}'.format(end_time - start_time))
        print("%d bytes" % (self.hexas_array.size * self.hexas_array.itemsize))

    def populate_lists(self):
        # Populate hexasList and squareSextandsList
        hexasList = [] 
        squareSextandsList = [] 
        sextandsList = [] 
        start_time = datetime.now()
        sxtnd = 0
        for i in range(self.array_size):
            if((i + 1) % 2 == 1):
                hexasList.append((3 * (i + 2)) - 1)
                sxtnd += 1
               
            else:
                hexasList.append((3 * (i + 1)) + 1)

            squareSextandsList.append(((hexasList[i] * hexasList[i]) - 1) / 6)
            sextandsList.append(sxtnd)
        end_time = datetime.now()
        print('Time for lists to populate ---- > Duration: {}'.format(end_time - start_time))
        print(sys.getsizeof(hexasList), "bytes")
    
    # TODO
    def GenerateHexas(self, n):
        """INPUT: 
        n: the number of hexas to be examined during the run of the program
        OUTPUT: 
        hexasList: the list of hexas
        sextandsList: the list of related sextands
        squareSextandsList: the list of related square sextands
        """

    # TODO
    def FindInvalidChains(self, n):
        """INPUT: n: the number of hexas to be examined during the run of the program
        OUTPUT: Determines the longest chain of consecutive invalid indices. Prints out the 
        starting index of this chain and its length"""

    # TODO
    def GenerateCombo(self, hexas_checked, index):
        """
        INPUT: 
        hexasChecked: The number of hexas checked (must be less than the number of hexas generated)
        index: index to check combo
        RETURNS:
        combo: a string with the combos for a certain index, < denotes the combo is valid
        """

    # TODO
    def ViewCombo(self, hexas_checked, start, length):
        """INPUT:
        hexasChecked: The number of hexas checked (must be less than the number of hexas generated)
        start: The starting index of the chain to be displayed
        length: The number of index combinations to be displayed
        OUTPUT: 
        Displays the combos for the indices starting at start and ending at start + length; also marks valid combos 
        Returns: 
        combosList: list of combos
        """

    # TODO
    def ViewCritCombos(self, hexas_checked):
        """INPUT: 
        hexasChecked: The number of hexas to be checked 
        OUTPUTS: 
        displays the combos in the critical area
        RETURNS:
        combosList: list of combos
        """

    # TODO
    def FindAverageGap(self, hexas_checked):
        """INPUTS: 
        hexasChecked: The number of hexas to be checked 
        OUTPUTS: 
        Displays the expected average gap between valid combos (hexorial / Lexorial)
        Returns:
        num: Hexorial of n hexas
        denom: Lexorial of n hexas
        gap: average of hexorial/lexorial
        NOTES: May want to take an input and find the average gap in that range (e.g. if n = 2, find the average gap in [0, (5*7)) range
        """
    
    def ValidCoordiniates(self):
        """INPUTS:
    hexasNum: The number of hexas being examined
    OUTPUT: .txt document given the coordinates where x is the number of hexas checked and y is the number of valid combos in critical area
    """
        combo = ""
        valid_num = 0
        hexas_checked = "Hexas checked: " + str(self.hexas_num) + "\n"
        file_name = "valid_coordinates.txt"

        # TODO: file handling 

        for i in range(2, self.hexas_num):
            combo = "(" + str(i) + ","
            valid_num = 0

            for j in range(int(self.square_sextands_array[i - 2]), int(self.square_sextands_array[i - 1])):
                valid = True
                for k in range(i):
                    result1 = ((6 * j) % self.hexas_array[k] == 1)
                    result2 = (6 * j) % self.hexas_array[k] == self.hexas_array[k] - 1
                    if(result1 or result2):
                        valid = False
                    if valid:
                        valid_num += 1
                combo += str(valid_num) + ")"
                print(combo)

    # TODO
    def GenerateCombos(self, hexas_num):
        """INPUTS:
        hexasNum: The number of hexas being examined (e.g. if hexasnum = 3, then 5,7, and 11 are being examined)
        OUTPUTS: Combines functionality of findInvalidChains() and viewChains()
        """

    # TODO
    def ValidNumApproximation(self, hexas_num):
        """INPUTS: hexasNum
        OUTPUTS: Calculates an approximated for the expected number of valid combos within the domain (i.e. [1, A] where A is the upper bound of
        the critical area), counts the true number of valid combos within the domain, and displays the error between them. Outputs to a txt file named
        valid_num_approx.txt as well as the console. 
        """
        
    # TODO
    def ViewCritArea(self):
        """
        OUTPUT: 
        Displays the start and end indices of the critical area being examined
        """

array_size = 10000000
hexas_num = 5
tp = NumpyTPC(array_size, hexas_num)
print("At array/list size = ", array_size)
print("Nummpy array time")
tp.populate_arrays()
print()
print("Python list time ")
tp.populate_lists()



        

        
    

        
