"""This is an analytical tool for gathering data about a particular set of integers, dubbed "hexadjacents", or "hexas"
Contributors: Robbie Jordan, Freya Gray, Lucas Nieddu, Cory Gamble"""

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

def ViewChains(hexasNum, length, start):
    """INPUT:hexasNum: The number of hexas checked (must be less than the number of hexas generated)
    length: The number of index combinations to be displayed
    start: The starting index of the chain to be displayed
    OUTPUT: Displays the combos for the indices starting at start and ending at start + length; also marks valid combos 
    NOTES: Want to implement a check to make sure hexasNum < generated hexas; may also want to change name for clarity
    """
    if hexasNum >= len(hexasList):
        hexasNum = len(hexasList) - 1
        combo = ""
        valid = false
    print("Hexas checked: " + str(hexasNum) + '\n')

    # Display the combos ranging from start to start + length
    for i in range(start, start + legnth + 1):
        valid = true # Checks if the index is valid
        combo = i + ": "
    for j in hexasNum:
        if(i % hexasList[j] == sexandsList[j] or i % hexas[j] == hexasList[j] - sextandsList[j]):
            valid = false
            combo += i % hexas[j] + " " # Update the string containing the combo for this index
    if valid:
        combo += " <" # Displays a marker for valid combos
    print(combo)

def ViewCritArea(hexasNum):
    """INPUT: hexasNum: The number of hexas being analyzed.
    OUTPUT: Displays all combinations in the critical area for the given set of hexas, and displays their validity"""
    if hexasNum >= len(hexasList):
        hexasNum = len(hexasList) - 1
        viewChains(hexasNum, squareSextandsList[hexasNum - 1], 0)


def ViewCombos(hexasNum, length, start, hexasChecked):
    """INPUT:hexasNum: The number of hexas checked (must be less than the number of hexas generated)
    length: The number of index combinations to be displayed
    start: The starting index of the chain to be displayed
    hexasChecked: The number of hexas to be checked 
    OUTPUT: Displays the combos for the indices starting at start and ending at start + length; also marks valid combos 
    NOTES: Want to implement a check to make sure hexasNum < generated hexas; may also want to change name for clarity
   
    NOTES: Same input/output as viewChains, except the latter allows custom hexa inputs
    ~ May want to deprecate this """
    combo = ""
    valid = True
    end = start + length
    print("Hexas checked: " + str(hexasChecked) + "\n")
    for i in range(start,end):
        combo = str(i) + ": "
        valid = True
        for j in range(0, hexasNum):
            combo += str(i % hexasList[j]) + " "
            #check for invalid moduli
            if i % hexasList[j] == 1 or i % hexasList[j] == hexasList[j] - 1:
                valid = False 
    if(valid):
        combo += "< "
    print(combo)

def ViewCritCombos(hexasChecked):
    """INPUT: hexasChecked: The number of hexas to be checked 
    OUTPUTS: displays the combos in the critical area
    NOTES: Can use viewCombos() or viewChains() """
    ViewCombos(hexasChecked, (squareSextandsList[hexasChecked-1]- squareSextandsList[hexasChecked- 2] + 1), squareSextandsList[hexasChecked - 2], hexasChecked)

def FindAverageGap(hexasChecked):
    """INPUTS: hexasChecked: The number of hexas to be checked 
    OUTPUTS: Displays the expected average gap between valid combos (hexorial / Lexorial)
    NOTES: May want to take an input and find the average gap in that range (e.g. if n = 2, find the average gap in [0, (5*7)) range
    """
    gap, num, denom = 1,1,1
    for i in range(0,hexasChecked):
        num *= hexasList[i]
        denom *= hexasList[i]-2
        gap *= hexasList[i]/(hexasList[i]-2)
    print(str(num) + " / " + str(denom) + "\n" + str(gap))
	
def ValidCoordinates(hexasNum):
    """INPUTS:
    hexasNum: The number of hexas being examined
    OUTPUT: .txt document given the coordinates where x is the number of hexas checked and y is the number of valid combos in critical area
    """
    combo = ""
    validNum = 0
    print("Hexas checked: " + str(hexasNum) + "\n")
    file_name = "valid_coordinates.txt"
    
    if os.path.exists(file_name):
        print("File exists, removing file and creating a new: ", file_name)
        os.remove(file_name)

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
    adv = True
    valid = True
    combo = [hexasNum]
    index = 1
    invalidChainLength, maxChainLength, invalidStart = 0, 0, 0
    chainLengthSum, chainsNum = 0, 0

    while(adv):
        adv = False
        valid = True

        print(format.__format__(str(index)) + ":")
        for i in range(len(combo)):
            combo[i] = index % hexasList[i]

            if(combo[i] != 0):
                adv = True

            # need to be adjusted for the fact that indices start at 0
            # search for invalid remainders
            
            if(i % 2 == 0):
                if(combo[i] == ((i + 2) / 2) or combo[i] == hexasList[i] - ((i + 2) / 2)):
                    valid = False

            elif(i % 2 == 1):
                if(combo[i] == ((i + 1) / 2) or combo[i] == hexasList[i] - ((i + 1) / 2)):
                    valid = False

            print(format.__format__(combo[i]))
        if(valid):
            print("<")
            chainLengthSum += invalidChainLength
            chainsNum+=1

            invalidChainLength = 0
        else: # update chain length info
            invalidChainLength+=1

            if(invalidChainLength > maxChainLength):
                maxChainLength = invalidChainLength
                invalidStart = index - maxChainLength + 1
        
        print('\n')
        index += 1

        print("Max chain length: " + str(maxChainLength) + '\n'
						  + "Average gap between valid combos: " + str((chainLengthSum / chainsNum)) + '\n'
						  + "Max chain start: " + str(invalidStart))

def ValidNumApproximation():
    """INPUTS: none
    ~ Uses the CHECK_LIMIT number defined in main(), i.e. the default number of hexas
    OUTPUTS: Calculates an approximated for the expected number of valid combos within the domain (i.e. [1, A] where A is the upper bound of
   the critical area), counts the true number of valid combos within the domain, and displays the error between them
    """

    # Working to find true value; need even inputs for simplified estimate
    endPoint = squareSextandsList[(len(hexasList) - 1) - 1] # Subtract one for array index
    prodTrue = 0.0
    prodApprox = 1.0 # marks which section of approximation being checked
    marker = 1
    validCombo = False

    """
         - prodApprox is the approximated number of valid combos by taking quotient of the lesser hexorial and the true hexorial,
		    then multiplying that by the index, which in this case is the square-sextand of the greatest hexa being examined, i.e.
		    the upper boundary of the critical area

		 - prodTrue is the actual number of valid combos counted within the range of [1, A], where A is the upper boundary of the
		    critical area
    """
    i = 1
    for i in endPoint:
        validCombo = True
        if (i > squareSextandsList[marker]):
            marker += 2
        for j in marker:
            if(i % hexasList[j] == sextandsList[j] or i % hexasList[j] == (hexasList[j] - sextandsList[j])):
                validCombo = False
                break

        if(validCombo == True):
            prodTrue += 1
        # print("Valid at " + i)

        # print((hexas[j] - 2) / hexas[j])
        # print(prodTrue)
    for j in range(len(hexasList) - 1):
        prodApprox *= ((hexasList[j] - 2) / hexasList[j])
        #print(hexas[j] - 2) / hexas[j]


    prodApprox *= endPoint
    print("Checking to s = " + str(endPoint))
    print("Aproximate combos: " + str(prodApprox))
    print("Number of valid combos: " + str(prodTrue))
    print("Error: " + str(((prodTrue - prodApprox) / prodTrue) * 100 + "%"))
