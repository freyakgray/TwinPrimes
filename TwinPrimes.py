"""This is an analytical tool for gathering data about a particular set of integers, dubbed "hexadjacents", or "hexas"
Contributors: Robbie Jordan, Freya Gray, Lucas Nieddu"""

hexasList = []
sextandsList = []
squareSextandsList = []

def GenerateHexas(n):
    """INPUT: n: the number of hexas to be examined during the run of the program
    OUTPUT: An int array containing the first n positive hexas, as well as an array of the first n sextands
    NOTES: May be better implemented as a simple startup procedure within main()"""
    for i in n:
        sextandsList[i] = i + 1
        hexasList[i] = 6 * (sextandsList[i]) - 1
        squareSextandsList[i] = 6 * (sextandsList[i] * sextandsList[i]) - (2 * sextandsList[i])
        if i + 1 <= n:
            sextandsList[i + 1] = i + 1
            hexasList[i + 1] = 6 * (sextandsList[i]) + 1
            squareSextandsList[i + 1] = 6 * (sextandsList[i + 1] * sextandsList[i + 1]) + (2 * sextandsList[i + 1])
        i+=1 # Need to skip every other index
        
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
    
    for i in n:
        hexorial *= hexasList[i]	
    for i in ((hexorial - 1) / 2):# Only need half the hexorial because validity is mirrored
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
    if hexasNum >= len(hexasList)
	hexasNum = len(hexasList) - 1
    combo = ""
    valid = false
    print("Hexas checked: " + str(hexasNum) + '\n')

    # Display the combos ranging from start to start + length
    for i in range(start, start + legnth + 1):
        valid = true // Checks if the index is valid
	combo = i + ": ";
	for j in hexasNum:
	    if(i % hexasList[j] == sexandsList[j] or i % hexas[j] == hexasList[j] - sextandsList[j])
	        valid = false
	    combo += i % hexas[j] + " " # Update the string containing the combo for this index
	
	if valid
	    combo += " <" # Displays a marker for valid combos

	print(combo)

def ViewCritArea(hexasNum):
    """INPUT: hexasNum: The number of hexas being analyzed.
    OUTPUT: Displays all combinations in the critical area for the given set of hexas, and displays their validity"""
    if hexasNum >= len(hexasList)
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
    print()

def GenerateCombos(hexasNum):
    """INPUTS:
    hexasNum: The number of hexas being examined (e.g. if hexasnum = 3, then 5,7, and 11 are being examined)
    OUTPUTS: Combines functionality of findInvalidChains() and viewChains()
    """
    print()

def ValidNumApproximation():
    """INPUTS: none
    ~ Uses the CHECK_LIMIT number defined in main(), i.e. the default number of hexas
    OUTPUTS: Calculates an approximated for the expected number of valid combos within the domain (i.e. [1, A] where A is the upper bound of
   the critical area), counts the true number of valid combos within the domain, and displays the error between them
    """
    print()
