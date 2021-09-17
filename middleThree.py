import numpy as np

CHECK_LIMIT = 8 #number of hexas checked (min 2, max ARR) 
#maybe rename CHECK_LIMIT
hexas = np.array() #use numpy array
#hexas = [] 
sqSextands = np.array()
#sqSextands = []

def viewCombos(hexasNum, length, start):
    """INPUT:hexasNum: The number of hexas checked (must be less than the number of hexas generated)
    length: The number of index combinations to be displayed
    start: The starting index of the chain to be displayed
    OUTPUT: Displays the combos for the indices starting at start and ending at start + length; also marks valid combos 
    NOTES: Want to implement a check to make sure hexasNum < generated hexas; may also want to change name for clarity
   
    NOTES: Same input/output as viewChains, except the latter allows custom hexa inputs, but this one uses the CHECK_LIMIT defined in main()
    ~ May want to deprecate this """
    combo = ""
    valid = True
    end = start + length
    print("Hexas checked: " + CHECK_LIMIT + "\n")
    for i in range(start,end):
        combo = i + ": "
        valid = True
        for j in range(0, hexasNum):
            combo += i % hexas[j] + " "
            if i % hexas[j] == 1 or i % hexas[j] == hexas[j] - 1:
                valid = False 
    if(valid):
        combo += "< "
    print(combo)

def viewCritCombos():
    """INPUTS: none
    OUTPUTS: displays the combos in the critical area
    NOTES: Can use viewCombos() or viewChains() """
    viewCombos(CHECK_LIMIT, (sqSextands[CHECK_LIMIT-1]- sqSextands[CHECK_LIMIT- 2] + 1), sqSextands[CHECK_LIMIT - 2])

def findAverageGap():
    """INPUTS: none
    OUTPUTS: Displays the expected average gap between valid combos (hexorial / Lexorial)
    NOTES: May want to take an input and find the average gap in that range (e.g. if n = 2, find the average gap in [0, (5*7)) range
    """
    gap, num, denom = 1
    for i in range(0,CHECK_LIMIT):
        num *= hexas[i]
        denom *= hexas[i]-2
        gap *= hexas[i]/(hexas[i]-2)
    print(num + " / " + denom + "\n" + gap)