# This is an analytical tool for gathering data about a particular set of integers, dubbed "hexadjacents", or "hexas"
# Contributors: Robbie Jordan, Freya Grey, Lucas Nieddu


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


##### FUNCTIONS #####
# int[] generateHexas(int n)

# void findInvalidChains()

# void viewChains(int hexasNum, int length, int start)

# void viewCritArea(int n)

# void viewCombos(int hexasNum, int length, int start)

# void viewCritCombos()

# void findAverageGap()

# public static void validCoordinates(int hexasNum)

# void generateCombos(int hexasNum)

# void validNumApproximation()
