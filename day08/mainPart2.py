#!/usr/bin/env python3
import itertools

"""
Each number correspond to a place in the segment display :

     0
    ---
 1 |   | 2
    -3-
 4 |   | 5
    ---
     6

In a way that the following string : "abcdefg" will represent these pos :

     a
    ---
 b |   | c
    -d-
 e |   | f
    ---
     g

Because 'a' is in pos 0 in the string, 'b' pos 1 etc...
"""

# Register digit that can be formed with a given length
lenToDigitDict = {
    2:[1],
    3:[7],
    4:[4],
    5:[2, 5, 3],
    6:[6, 0, 9],
    7:[8]
}

# Register position where there can be segment to form digit
digitConfigDict = {
    0: [0,1,2,4,5,6],
    1: [2,5],
    2: [0,2,3,4,6],
    3: [0,2,3,5,6],
    4: [1,2,3,5],
    5: [0,1,3,5,6],
    6: [0,1,3,4,5,6],
    7: [0,2,5],
    8: [0,1,2,3,4,5,6],
    9: [0,1,2,3,5,6]
}


def permuteString(pattern):
    # Create every combinaison of the string (without duplicating letters)
    return [''.join(comb) for comb in itertools.permutations(pattern)]


def applyFilter(permutations, digit, segmentFilter):
    digitConfig = digitConfigDict[digit]
    filteredPermutations = []
    for permutation in permutations:
        validPermutation = True
        for segmentIndex, segment in enumerate(permutation):
            pos = digitConfig[segmentIndex]
            if segment not in segmentFilter[pos] and len(segmentFilter[pos]) != 0:
                validPermutation = False
        if validPermutation and permutation not in filteredPermutations:
            filteredPermutations.append(permutation)
    return filteredPermutations


def updateFilter(permutations, digitConfig, segmentFilter):
    for permutation in permutations:
        for segmentIndex, segment in enumerate(permutation):
            pos = digitConfig[segmentIndex]
            if segment not in segmentFilter[pos]:
                segmentFilter[pos].append(segment)
    return segmentFilter


def getDigitWithoutPos(pos):
    digitWithoutPos = []
    for digit, config in digitConfigDict.items():
        if pos not in config:
            digitWithoutPos.append(digit)
    return digitWithoutPos


def cleanFilter(permutations, segmentFilter):
    newFilter = {}
    for pos, filterContent in segmentFilter.items():
        if len(filterContent) == 1:
            newFilter[pos] = filterContent[0]
        else:
            digitWithoutPos = getDigitWithoutPos(pos)
            for filterSegment in filterContent:
                impostor = False
                for digit in digitWithoutPos:
                    apparitionCount = 0
                    for permut in permutations[digit]:
                        if filterSegment in permut:
                            apparitionCount += 1
                    if apparitionCount == len(permutations[digit]):
                        impostor = True
                if impostor == False and filterSegment not in newFilter.values():
                    newFilter[pos] = filterSegment
    print("new filter : ", newFilter)
    return newFilter


def getOutputValue(digitOutput, uniquePatterns):
    outputValue = ""
    for digit in digitOutput:
        # Permut the digitOutput
        permutedDigit = permuteString(digit)
        # Seach for correspondance in uniquePattern, if found, concat the corresponding digit to outputValue
        outputValue += [str(uniquePatterns[i]) for i in permutedDigit if i in uniquePatterns][0]
    return int(outputValue) # Return the int version


def parseLine(line):
    lineData = line.rstrip().split('|')
    signalPattern = sorted(lineData[0].split(), key=len) # sort by length
    signalPattern.append('') # Useful for condition in PhaseOne
    digitOutput = lineData[1].split()
    return signalPattern, digitOutput

def getUniquePatterns(filteredPermutedPattern, segmentFilter):
    uniquePatterns = {}
    for digit, permut in filteredPermutedPattern.items():
        # Apply final filter to the filteredPermutedPattern to get uniquePattern
        pattern = applyFilter(permut, digit, segmentFilter)
        # Link uniquePattern to the corresponding digit in a Dict
        uniquePatterns[pattern[0]] = digit
    return uniquePatterns


def applyPhaseOne(signalPattern):
    currentLen = 2 # We will start with the len 2
    permutations = {} # Permuted patterns
    filteredPermutations = {} # Permuted patterns on which the filter applied
    segmentFilter = {0:[],1:[],2:[],3:[],4:[],5:[],6:[]} # Filter

    for pattern in signalPattern:
        # Only if every pattern of the given length have been permuted & filtered
        # Save filtered pattern for later use
        # Update filter with the new elements
        # The filter won't be perfect but will be cleaned later on
        if len(pattern) != currentLen:
            for digit, permut in permutations.items():
                filteredPermutations[digit] = permut
                digitConfig = digitConfigDict[digit]
                segmentFilter = updateFilter(permut, digitConfig, segmentFilter)
            permutations = {}
            currentLen = len(pattern)

        # (Ignore if this is the end)
        # Permute the given pattern and apply a filter on the permuted list
        # This greatly reduce the nb of data that will need to be process later on
        if len(pattern) != 0:
            digits = lenToDigitDict[len(pattern)]
            for digit in digits:
                tmpPermutations = permuteString(pattern)
                if digit not in permutations.keys():
                    permutations[digit] = []
                if len(pattern) != 2: # Filter is empty in the first cycle
                    tmpPermutations = applyFilter(tmpPermutations, digit, segmentFilter)
                permutations[digit] += tmpPermutations
    return filteredPermutations, segmentFilter


def main():
    with open("testInput.txt", 'r') as fileInput:
        endResult = 0 # Will sum outputValues
        for line in fileInput:
            # Phase 1
            signalPattern, digitOutput = parseLine(line)
            filteredPermutedPattern, segmentFilter = applyPhaseOne(signalPattern)
            # Phase 2
            segmentFilter = cleanFilter(filteredPermutedPattern, segmentFilter)
            uniquePatterns = getUniquePatterns(filteredPermutedPattern, segmentFilter)
            # Phase 3
            endResult += getOutputValue(digitOutput, uniquePatterns)
        print("finalSum : ", endResult)


if __name__ == '__main__':
    main()
