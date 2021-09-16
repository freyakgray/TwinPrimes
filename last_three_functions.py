CHECK_LIMIT = 8
SqSextands = []
hexas = []
hexasSextands = []

def validCoordinates(hexasNum):
    """INPUTS:
    hexasNum: The number of hexas being examined
    OUTPUT: .txt document given the coordinates where x is the number of hexas checked and y is the number of valid combos in critical area
    """
    combo = ""
    valid = False 
    validNumber = 0

    print("Hexas checked: " + hexasNum + '\n')
    i = 2
    j = SqSextands[i-2]
    k = 0
    for i in hexasNum: # cycle through all hexa pairs
        combo = "(" + i + ", "
        validNum = 0
        for j in SqSextands[i-1]: # cycle through critical area
            valid = True
            for k in i: # check modulos of all hexas for a given sextand
                if ((6 * j) % hexas[k] == 1 or (6 * j) % hexas[k] == hexas[k] - 1 ):
                    valid = False 
                
            if(valid):
                validNum+=1
    combo += validNum + ")"
    print(combo)

def generateCombos(hexasNum):
    """INPUTS:
    hexasNum: The number of hexas being examined (e.g. if hexasnum = 3, then 5,7, and 11 are being examined)
    OUTPUTS: Combines functionality of findInvalidChains() and viewChains()
    """
    adv = True
    valid = True
    combo = [hexasNum]
    sxtnd = 1
    invalidChainLength, maxChainLength, invalidStart = 0, 0, 0
    chainLengthSum, chainsNum = 0, 0

    while(adv):
        adv = False
        valid = True

        print(format.__format__(sxtnd) + ":")
        for i in range(len(combo)):
            combo[i] = sxtnd % hexas[i]

            if(combo[i] != 0):
                adv = True

            # need to be adjusted for the fact that incices start at 0
            if(i % 2 == 0):
                if(combo[i] == ((i + 2) / 2) or combo[i] == hexas[i] - ((i + 2) / 2)):
                    valid = False

            elif(i % 2 == 1):
                if(combo[i] == ((i + 1) / 2) or combo[i] == hexas[i] - hexas[i] - ((i + 1) / 2)):
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
                invalidStart = sxtnd - maxChainLength + 1
        
        print('\n')
        sxtnd += 1

        print("Max chain length: " + maxChainLength + '\n'
						  + "Average gap between valid combos: " + (chainLengthSum / chainsNum) + '\n'
						  + "Max chain start: " + invalidStart)

def validNumApproximation():
    """INPUTS: none
    ~ Uses the CHECK_LIMIT number defined in main(), i.e. the default number of hexas
    OUTPUTS: Calculates an approximated for the expected number of valid combos within the domain (i.e. [1, A] where A is the upper bound of
   the critical area), counts the true number of valid combos within the domain, and displays the error between them
    """

    # Working to find true value; need even inputs for simplified estimate
    endPoint = SqSextands[CHECK_LIMIT - 1] # Subtract one for array index
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
        if (i > SqSextands[marker]):
            marker += 2
        for j in marker:
            if(i % hexas[j] == hexasSextands[j] or i % hexas[j] == (hexas[j] - hexasSextands[j])):
                validCombo = False
                break

        if(validCombo == True):
            prodTrue += 1
        # print("Valid at " + i)

        # print((hexas[j] - 2) / hexas[j])
        # print(prodTrue)
    for j in range(CHECK_LIMIT):
        prodApprox *= ((hexas[j] - 2) / hexas[j])
        #print(hexas[j] - 2) / hexas[j]


    prodApprox *= endPoint
    print("Checking to s = " + endPoint)
    print("Aproximate combos: " + prodApprox)
    print("Number of valid combos: " + prodTrue)
    print("Error: " + ((prodTrue - prodApprox) / prodTrue) * 100 + "%")


            
    


