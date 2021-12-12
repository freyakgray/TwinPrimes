"""This is an analytical tool for gathering data about a particular set of integers, dubbed "hexadjacents", or "hexas"
Contributors: Robbie Jordan, Freya Gray, Lucas Nieddu, Cory Gamble"""

#imports
import os

hexasList = []
sextandsList = []
squareSextandsList = []

def GenerateHexas(n):
    """INPUT: 
    n: the number of hexas to be examined during the run of the program
    OUTPUT: 
    hexasList: the list of hexas
    sextandsList: the list of related sextands
    squareSextandsList: the list of related square sextands
    """
    assert n >= 1
    for i in range(n):
        currentHexa = int(3*(i + 1) + (3/2) - ((-1)**(i + 1) * (1/2)))
        hexasList.insert(i, currentHexa)
        currentSextand = int(((1/2) * (i+1)) + (1/4) + ((1/4) * (-1)**((i+1) - 1)))
        sextandsList.insert(i, currentSextand)
        #if the hexa = 6s - 1 for some s, then its square-sextand is 6(s^2) - 2s, and if the hexa is 6s + 1 then its square-sextand is 6(s^2) + 2s
        if i % 2 == 0:
            squareSextand = 6*(currentSextand**2) - 2*currentSextand
            squareSextandsList.insert(i, int(squareSextand))
        else:
            squareSextand = 6*(currentSextand**2) + 2*currentSextand
            squareSextandsList.insert(i, int(squareSextand))
    
def FindInvalidChains(n):
    """INPUT: n: the number of hexas to be examined during the run of the program
    OUTPUT: Determines the longest chain of consecutive invalid indices. Prints out the starting index of this chain and its length"""
    if n > len(hexasList):
        n = len(hexasList)
    hexorial = 1
    invalidStart = 0
    invalidLength = 0
    maxInvalid = 0
    valid = True
    
    for i in range(n):
        hexorial *= hexasList[i]	
    for i in range((hexorial - 1) / 2):# Only need half the hexorial because validity is mirrored
        valid = True
		# check  if the index is valid With Respect To (WRT) each hexa checked
		# NOTE: Take advantage of sextand-modulo reduction (only need to check sextand modulo h)
        for j in n:
            if(i % hexasList[j] == sextandsList[i] or i % hexasList[j] == hexasList[j] - sextandsList[j]):
                valid = False
			
			# Update the length of the chain of consecutive invalid indices
            if not(valid):
                invalidLength+=1
                if maxInvalid < invalidLength:
                    maxInvalid = invalidLength
                    invalidStart = i + 1 - maxInvalid
            else:
                invalidLength = 0
	#Visual output
    print("Start of max chain: " + str(invalidStart) + '\n'+ 
    "Max length chain: " + str(maxInvalid) + '\n' + 
    "Critical Zone size: " + str((squareSextandsList[n - 1] - squareSextandsList[n - 2])))

def GenerateCombo(hexasChecked, index):
    """
    INPUT: 
    hexasChecked: The number of hexas checked (must be less than the number of hexas generated)
    index: index to check combo
    RETURNS:
    combo: a string with the combos for a certain index, < denotes the combo is valid
    """
    assert hexasChecked < len(hexasList)
    assert hexasChecked >= 1
    assert index >= 0
    valid = True
    combo = ""
    for i in range(hexasChecked):
        combo += str(index % hexasList[i]) + " "
        if (index % hexasList[i] == 1) or (index % hexasList[i] == hexasList[i] - 1):
            valid = False
    if(valid):
        combo += "< "
    return combo
        
def ViewCombo(hexasChecked, start, length):
    """INPUT:
    hexasChecked: The number of hexas checked (must be less than the number of hexas generated)
    start: The starting index of the chain to be displayed
    length: The number of index combinations to be displayed
    OUTPUT: 
    Displays the combos for the indices starting at start and ending at start + length; also marks valid combos 
    Returns: 
    combosList: list of combos
    """
    assert hexasChecked < len(hexasList)
    assert start >= 0
    assert hexasChecked,length >= 1
    combosList = []
    end = start + length
    print("Hexas checked: " + str(hexasChecked) + "\n")
    for i in range(start,end):
        combo = str(i) + ": "
        combo += GenerateCombo(hexasChecked, i)
        combosList.insert(i, combo)
        print(combo + "\n")
    return combosList

def ViewCritCombos(hexasChecked):
    """INPUT: 
    hexasChecked: The number of hexas to be checked 
    OUTPUTS: 
    displays the combos in the critical area
    RETURNS:
    combosList: list of combos
    """
    assert hexasChecked < len(hexasList)
    combosList = ViewCombo(hexasChecked, 0, squareSextandsList[hexasChecked - 1] + 1)
    return combosList

def FindAverageGap(hexasChecked):
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
    gap, num, denom = 1,1,1
    for i in range(0,hexasChecked):
        num *= hexasList[i]
        denom *= hexasList[i]-2
    gap = num/denom
    print(str(num) + " / " + str(denom) + "\n" + str(gap))
    return num, denom, gap
	
def ValidCoordinates(hexasNum):
    """INPUTS:
    hexasNum: The number of hexas being examined
    OUTPUT: .txt document given the coordinates where x is the number of hexas checked and y is the number of valid combos in critical area
    """
    combo = ""
    validNum = 0
    hexas_checked = "Hexas checked: " + str(hexasNum) + "\n"
    file_name = "valid_coordinates.txt"
    
    if os.path.exists(file_name):
        os.remove(file_name)
    
    with open(file_name, "w") as file:
        file.write(hexas_checked)

    for i in range(2, hexasNum + 1): # Cycle through all hexa pairs
        combo = "(" + str(i) + ","
        # print(combo)
        validNum = 0

        for j in range(int(squareSextandsList[i-2]), int(squareSextandsList[i-1] + 1)):
            valid = True
            for k in range(i):
                result1 = ((6 * j) % hexasList[k] == 1)
                result2 = (6 * j) % hexasList[k] == hexasList[k] - 1
                if(result1 or result2):
                    valid = False

            if(valid):
                validNum += 1

        combo += str(validNum) + ")"
        with open("valid_coordinates.txt", "a") as file:
            file.write(combo + '\n')

def GenerateCombos(hexasNum):
    """INPUTS:
    hexasNum: The number of hexas being examined (e.g. if hexasnum = 3, then 5,7, and 11 are being examined)
    OUTPUTS: Combines functionality of findInvalidChains() and viewChains()
    """
    # boolean variables
    adv = True 
    valid = True

    # combo list initialized with size of hexasNum
    combo = [[]] * hexasNum

    # integer varaibles
    index = 1
    invalidChainLength = 0
    maxChainLength = 0
    invalidStart = 0

    # float variables 
    chainLengthSum = 0.0
    chainsNum = 0.0

    # file name
    file_name = "generate_combos.txt"
    
    if os.path.exists(file_name):
        os.remove(file_name)

    while (adv):
        adv = False
        valid = True

        print_statement = str(str(index) + ": ")
        print(str(index), ":", end = " ")
        for i in range(0 , len(combo)):
            combo[i] = (index % hexasList[i])
        
            if(combo[i] != 0):
                adv = True
            
            if(i % 2 == 0):
                result1 = combo[i] == ((i + 2) / 2) 
                result2 = combo[i] == hexasList[i] - ((i + 2) / 2)
                if (result1) or (result2):
                    valid = False

                
                
            elif(i % 2 == 1):
                result3 = combo[i] == ((i + 1) / 2)
                result4 = combo[i] == hexasList[i] - ((i + 1) / 2)
                if (result3) or (result4):
                    valid = False
            
            print_statement += " "
            print_statement += str(combo[i])
            print(str(combo[i]), end = " ")

        if(valid):
            print_statement += " <"
            print(" <", end = " ")

            chainLengthSum += invalidChainLength
            chainsNum+=1
            invalidChainLength = 0
        else:
            invalidChainLength +=1 

            if(invalidChainLength > maxChainLength):
                maxChainLength = invalidChainLength
                invalidStart = index - maxChainLength + 1

        with open("generate_combos.txt", "a" ) as file:
            file.write(print_statement)
            file.write("\n")

        print("\n")
        index+=1

    # End while
    ratio = (chainLengthSum / float(chainsNum))
    with open(file_name, "a") as file:
        file.write("Max chain length: ")
        file.write(str(maxChainLength))
        file.write("\n")
        file.write("Average gap between valid combos: ")
        file.write(str(ratio))
        file.write("\n")
        file.write("Max chain start: ")
        file.write(str(invalidStart))


def ValidNumApproximation(hexasNum):
    """INPUTS: hexasNum
    OUTPUTS: Calculates an approximated for the expected number of valid combos within the domain (i.e. [1, A] where A is the upper bound of
   the critical area), counts the true number of valid combos within the domain, and displays the error between them. Outputs to a txt file named
   valid_num_approx.txt as well as the console. 
    """

    '''
        prodApprox is the approximated number of valid combos by taking quotient of the lesser hexorial and the true hexorial,
		then multiplying that by the index, which in this case is the square-sextand of the greatest hexa being examined, i.e.
		the upper boundary of the critical area
        prodTrue is the actual number of valid combos counted within the range of [1, A], where A is the upper boundary of the
		critical area
    '''    

    # integers
    endPoint = int(squareSextandsList[hexasNum - 1])
    marker = 1

    # floats
    prodTrue = 0.0
    prodApprox = 1.0

    # boolean values
    validCombo = False

    # file name
    file_name = "valid_num_approx.txt"
    
    if os.path.exists(file_name):
        os.remove(file_name)

    for i in range(1, endPoint):
        validCombo = True
        if(i > squareSextandsList[marker]):
            marker += 2

        for j in range(0, marker):
            result1 = i % hexasList[j] == sextandsList[j]
            result2 = i % hexasList[j] == (hexasList[j] - sextandsList[j])
            if (result1) or (result2):
                validCombo = False
                break
        
        if(validCombo == True):
            prodTrue+=1
            print_statement = "Valid at " + str(i)
            print(print_statement)
            with open(file_name, "a") as file:
                file.write(print_statement)
                file.write("\n")
                
    for j in range(0, hexasNum):
        prodApprox *= ((float(hexasList[j] - 2)) / (float(hexasList[j])))
    
    prodApprox *= endPoint
    error = (prodTrue - prodApprox) / float(prodTrue)
    error_percentage = error * 100

    with open(file_name, "a") as file:
        file.write("Checking to s = ")
        file.write(str(endPoint))
        file.write("\n")
        file.write("Approximate combos: ")
        file.write(str(prodApprox))
        file.write("\n")
        file.write("Number of valid combos: ")
        file.write(str(prodTrue))
        file.write("\n")
        file.write("Error: ")
        file.write(str(error_percentage))
        file.write("%")
    print("Checking to s = ", str(endPoint))
    print("Approximate combos: ", str(prodApprox))
    print("Number of valid combos: ", str(prodTrue))
    print("Error: ", str(error_percentage))

def ViewCritArea():
    """
    OUTPUT: 
    Displays the start and end indices of the critical area being examined
    """
    length = len(hexasList) - 1
    limit = hexasList[length]
    subtend = hexasList[length - 1]
    start = (subtend ** 2 - 1) / 6
    end = (limit ** 2 - 1) / 6
    print("*** critical area ***")
    print("start:", int(start))
    print("end:", int(end))