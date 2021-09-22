"""This is an analytical tool for gathering data about a particular set of integers, dubbed "hexadjacents", or "hexas"
Contributors: Robbie Jordan, Freya Gray, Lucas Nieddu"""


##### DEFINITIONS AND PROPERTIES #####
#$$$ Hexadjacent (hexa): Integers of the form 6x - 1 and 6x + 1 for positive integers x
#  - Equivalently, a hexa is any number that has neither 2 nor 3 in its prime factorization
# a) The product of two hexas is also a hexa (since the two hexas do not have 2 or 3 as factors, neither can their product)
# b) A composite hexa has only other hexas as factors (if it had a factor that was not a hexa, then it must have 2 or 3 as a factor, which
#    is imposssible by definition of a hexa)
# c) 1 can technically be considered a hexa, but is disregarded due to unusual properties that make it less useful
#  - It is only useful for us to consider hexas where x > 0, but it could technically be generalized to be any integer
#$$$ Sextand: For a given hexa 6x - 1 or 6x + 1, x is the sextand (e.g. 11 = (6 * 2) - 1, thus the sextand of 11 is 2)
#$$$ Limiting Hexa*: The greatest hexa being considered in a given observation
#$$$ Subtending Hexa*: the second-greatest hexa being considered in a given observation
#$$$ Critical area: The indices between those of the square of the subtending and limiting hexas
#   e.g. if we are considering the first 4 hexas [5, 7, 11, 13], 13 is the limiting hexa, 11 is the subtending hexa, and the critical area
#   lies between 11^2 = 121 and 13^2 = 169. Since these must also be hexas (see Hexas note a), this can also refer to the area
#   between the sextands of these numbers, i.e. instead of 121 - 169, it is 20 - 28
#   a) If g is the sextand of the limiting and subtending hexas, then the critical area in the second form is [6g^2 - 2g, 6g^2 + 2g]
#$$$ Hexorial: n^ is the product of the first n hexas (notation can be debated; it is meant to be the Japanese character "he", for "hexorial"
#$$$ Lesser Hexorial (Lexorial*): n^- is the product of the first n hexas less 2 (i.e. (5 - 2) * (7 - 2) * (11 - 2) * (13 - 2) * ...)
#$$$ Sextand-modulo reduction*: Checking indices rather than multiples of 6
#   ~ Looking at indices modulo hexas and looking for hexas +- sextands, rather than multiples of 6 modulo hexas and looking for (hexa - 1)s and (hexa + 1)s
#   ~ This may be a good topic for discussion if this definition is unclear
#$$$ Index: When denoting multiples of 6, the index is the number multiplied by 6 (e.g. the index of 12 is 2)
# a) For some hexa h, an index i is "valid with respect to h" if neither 6i - 1 nor 6i + 1 are divisible by h; otherwise, i is "invalid with respect to h"
# b) i is valid with respect to h if and only if i === s or -s modulo h, where === denotes modulo congruence and s is the sextand of h
#$$$ Combintation/combo*: The set of remainders of an index i modulo h{}, where h{} denotes a set of hexas 
#   - e.g. if h{} = {5, 7}, then the combination at i = 8 is {3, 1}, since 8 === 3 mod 5 and 8 === 1 mod 7
# a) A combination is "valid" if the index is valid with respect to all hexas in h{}; otherwise it is invalid.
hexasList = []
sextandsList = []
squareSextandsList = []

def GenerateHexas(n):
    """INPUT: n: the number of hexas to be examined during the run of the program
    OUTPUT: An int array containing the first n positive hexas, as well as an array of the first n sextands
    NOTES: May be better implemented as a simple startup procedure within main()"""
    for i in n
        sextandsList[i] = i + 1
        hexasList[i] = 6 * (sextandsList[i]) - 1
        squareSextandsList[i] = 6 * (sextandsList[i] * sextandsList[i]) - (2 * sextandsList[i])
        if i + 1 <= n
            sextandsList[i + 1] = i + 1
            hexasList[i + 1] = 6 * (sextands[i]) + 1
            squareSextandsList[i + 1] = 6 * (sextandsList[i + 1] * sextandsList[i + 1]) + (2 * sextandsList[i + 1])
        i++ # Need to skip every other index
        
def FindInvalidChains(n):
    """INPUT: n: the number of hexas to be examined during the run of the program
    OUTPUT: Determines the longest chain of consecutive invalid indices. Prints out the starting index of this chain and its length"""
    if n > len(hexasList)
        n = len(hexasList)
   
    hexorial = 1
    invalidStart = 0
    invalidLength = 0
    maxInvalid = 0
	valid = true;
	for i in n
		hexorial *= hexas[i];
		
    for i in (hexorial - 1) / 2) # Only need half the hexorial because validity is mirrored
			valid = true;
			
			# check  if the index is valid With Respect To (WRT) each hexa checked
			# NOTE: Take advantage of sextand-modulo reduction (only need to check sextand modulo h)
			for j in n
				if(i % hexasList[j] == sextandsList[i] or i % hexas[j] == hexas[j] - sextandsList[j])
					valid = false;
			
			# Update the length of the chain of consecutive invalid indices
			if not(valid) {
				invalidLength++
				
				if maxInvalid < invalidLength
					maxInvalid = invalidLength
					invalidStart = i + 1 - maxInvalid

			else
				invalidLength = 0;

		// Visual output
		print("Start of max chain: " + invalidStart + '\n'
			+ "Max length chain: " + maxInvalid + '\n'
			+ "Critical Zone size: " + (SqSextands[n - 1] - SqSextands[n - 2]));

def ViewChains(hexasNum, length, start):
    """INPUT:hexasNum: The number of hexas checked (must be less than the number of hexas generated)
   length: The number of index combinations to be displayed
   start: The starting index of the chain to be displayed
   OUTPUT: Displays the combos for the indices starting at start and ending at start + length; also marks valid combos 
   NOTES: Want to implement a check to make sure hexasNum < generated hexas; may also want to change name for clarity
   """
    print(hexasNum)

def ViewCritArea(n):
    """INPUT: n: The index of the highest hexa in the array of generated hexas.
    OUTPUT: Displays the start and end indices of the critical area being examined
    Notes: Want to implement a check to ensure n < generated hexas """
    print()


def ViewCombos(hexasNum, lenght, start):
    """INPUT:hexasNum: The number of hexas checked (must be less than the number of hexas generated)
    length: The number of index combinations to be displayed
    start: The starting index of the chain to be displayed
    OUTPUT: Displays the combos for the indices starting at start and ending at start + length; also marks valid combos 
    NOTES: Want to implement a check to make sure hexasNum < generated hexas; may also want to change name for clarity
   
    NOTES: Same input/output as viewChains, except the latter allows custom hexa inputs, but this one uses the CHECK_LIMIT defined in main()
    ~ May want to deprecate this """
    print()

def ViewCritCombos():
    """INPUTS: none
    OUTPUTS: displays the combos in the critical area
    NOTES: Can use viewCombos() or viewChains() """
    print()

def FindAverageGap():
    """INPUTS: none
    OUTPUTS: Displays the expected average gap between valid combos (hexorial / Lexorial)
    NOTES: May want to take an input and find the average gap in that range (e.g. if n = 2, find the average gap in [0, (5*7)) range
    """
    print()

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
