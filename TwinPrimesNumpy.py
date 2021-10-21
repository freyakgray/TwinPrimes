import os
import numpy as np
from numpy.lib.function_base import append
from datetime import datetime
import sys
from pympler.asizeof import asizeof


class NumpyTPC:
    def __init__(self, size, hexas_num):
        self.size = size
        self.hexas_num = hexas_num
        
        # initialize empty numpy arrays 
        self.hexas_array = np.empty(self.size)
        self.sextands_array = np.empty(self.size)
        self.square_sextands_array = np.empty(self.size)

        # initialize lists
        self.hexas_list = []
        self.sextands_list = []
        self.square_sextands_list = []

        # file names
        self.ARRAY_FILE_NAME = "valid_coordinates_array.txt"
        self.LIST_FILE_NAME = "valid_coordinates_list.txt"

    def populate_arrays(self):
        print("Populating arrays at size = ", self.size, " ....")
        # Populate hexas array and square_sextands_array
        sxtnd = 0
        for i in range(self.size):
            if((i + 1) % 2 == 1):
                self.hexas_array[i] =  ((3 * (i + 2)) - 1)
                sxtnd += 1
               
            else:
                self.hexas_array[i] = ((3 * (i + 1)) + 1)

            self.square_sextands_array[i] =  (((self.hexas_array[i] * self.hexas_array[i]) - 1) / 6)
            self.sextands_array[i] =  sxtnd

    def populate_lists(self):
        print("Populating lists at size = ", self.size, "....")
        # Populate hexasList and squareSextandsList
        sxtnd = 0
        for i in range(self.size):
            if((i + 1) % 2 == 1):
                self.hexas_list.append((3 * (i + 2)) - 1)
                sxtnd += 1
               
            else:
                self.hexas_list.append((3 * (i + 1)) + 1)

            self.square_sextands_list.append(((self.hexas_list[i] * self.hexas_list[i]) - 1) / 6)
            self.sextands_list.append(sxtnd)
    
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
    
    def ValidCoordinatesArray(self):
        """INPUTS:
        hexasNum: The number of hexas being examined
        OUTPUT: .txt document given the coordinates where x is the number of hexas checked and y is the number of valid combos in critical area
        """
        combo = ""
        validNum = 0
        hexas_checked = "Hexas checked: " + str(self.hexas_num) + "\n"
    
        if os.path.exists(self.ARRAY_FILE_NAME):
            os.remove(self.ARRAY_FILE_NAME)
    
        with open(self.ARRAY_FILE_NAME, "w") as file:
            file.write(hexas_checked)

        start_time = datetime.now()
        for i in range(2, self.hexas_num + 1): # Cycle through all hexa pairs
            combo = "(" + str(i) + ","
            # print(combo)
            validNum = 0

            for j in range(int(self.square_sextands_array[i-2]), int(self.square_sextands_array[i-1] + 1)):
                valid = True
                for k in range(i):
                    result1 = ((6 * j) % self.hexas_array[k] == 1)
                    result2 = (6 * j) % self.hexas_array[k] == self.hexas_array[k] - 1
                    if(result1 or result2):
                        valid = False

                if(valid):
                    validNum += 1
            combo += str(validNum) + ")"
            with open(self.ARRAY_FILE_NAME, "a") as file:
                file.write(combo + '\n')
        end_time = datetime.now()
        print('Time for numpy arrays to populate ---- > Duration: {}'.format(end_time - start_time))
        print("%d bytes" % (self.hexas_array.size * self.hexas_array.itemsize))

    def ValidCoordinatesList(self):
        """INPUTS:
        hexasNum: The number of hexas being examined
        OUTPUT: .txt document given the coordinates where x is the number of hexas checked and y is the number of valid combos in critical area
        """

        combo = ""
        validNum = 0
        hexas_checked = "Hexas checked: " + str(self.hexas_num) + "\n"
    
        if os.path.exists(self.LIST_FILE_NAME):
            os.remove(self.LIST_FILE_NAME)
    
        with open(self.LIST_FILE_NAME, "w") as file:
            file.write(hexas_checked)

        start_time = datetime.now()
        for i in range(2, self.hexas_num + 1): # Cycle through all hexa pairs
            combo = "(" + str(i) + ","
            # print(combo)
            validNum = 0

            for j in range(int(self.square_sextands_list[i-2]), int(self.square_sextands_list[i-1] + 1)):
                valid = True
                for k in range(i):
                    result1 = ((6 * j) % self.hexas_list[k] == 1)
                    result2 = (6 * j) % self.hexas_list[k] == self.hexas_list[k] - 1
                    if(result1 or result2):
                        valid = False

                if(valid):
                    validNum += 1
            combo += str(validNum) + ")"
            with open(self.LIST_FILE_NAME, "a") as file:
                file.write(combo + '\n')
        end_time = datetime.now()
        print('Time for python lists to populate ---- > Duration: {}'.format(end_time - start_time))
        print(sys.getsizeof(self.hexas_list), "bytes")
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

size = 1000
hexas_num = 30
tp = NumpyTPC(size, hexas_num)
tp.populate_arrays()
tp.populate_lists()
tp.ValidCoordinatesArray()
tp.ValidCoordinatesList()



        

        
    

        
