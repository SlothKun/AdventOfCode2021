ratingList = []
oxygenRate = ""
co2Rate = ""

def convertToInt(binary):
    return int(binary, 2)

def findRateNb(ratingList, criteria, blacklist):
    bitPos = 0 # Set the bit pos to verify
    # Continue until there's only one number left
    while len(ratingList) != 1:
        # Clean the dict at the beginning of each cycle
        bitCount = {'1': [], '0': []}
        # Sort each rateNb base on the bit on their bitPos
        for rate in ratingList:
            bitCount[rate[bitPos]].append(rate)

        # Apply criteria
        # Get rid of common element between 2 list : the ratingOne and the one to eliminate
        if len(bitCount['1']) > len(bitCount['0']):
            ratingList = list(set(ratingList).difference(bitCount[blacklist]))
        elif len(bitCount['1']) == len(bitCount['0']):
            ratingList = list(set(ratingList).difference(bitCount[blacklist]))
        else:
            ratingList = list(set(ratingList).difference(bitCount[criteria]))

        bitPos += 1 # increment bit pos
    return ratingList[0]


with open("input.txt", "r") as file:
    # Setup the arrays
    for line in file:
        ratingList.append(line.rstrip())

    # Find the rate nb for each rating and convert them to int
    oxygenRate = convertToInt(findRateNb(ratingList, '1', '0'))
    co2Rate = convertToInt(findRateNb(ratingList, '0', '1'))

    print("oxyRate: ", oxygenRate)
    print("co2Rate: ", co2Rate)
    # multiply values and print the result
    print("final value: ", oxygenRate * co2Rate)
