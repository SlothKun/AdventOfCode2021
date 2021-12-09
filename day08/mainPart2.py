#!/usr/bin/env python3
import itertools
import pprint

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

pp = pprint.PrettyPrinter(indent=4)

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


def permutePattern(pattern):
    return [''.join(comb) for comb in itertools.permutations(pattern)]

def applyFilter(permutations, digitConfig, segmentFilter):
    filteredPermutations = []
    # Go through list of permutations
    for permutation in permutations:
        validPermutation = True # Default value
        for segmentIndex, segment in enumerate(permutation):
            pos = digitConfig[segmentIndex]
            if segment not in segmentFilter[pos] and len(segmentFilter[pos]) != 0:
                validPermutation = False
        if validPermutation and permutation not in filteredPermutations:
            filteredPermutations.append(permutation)
    return filteredPermutations


def registerPotentialSegment(permutations, digitConfig, segmentFilter):
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


def main():
    endResult = 0
    with open("input.txt", 'r') as fileInput:
        for line in fileInput:
            signalPattern, *digitOutput = line.rstrip().split('|')
            # Generate all combinaison for all signalPattern
            signalPattern = sorted(signalPattern.split(), key=len)
            signalPattern.append('') # For the last one to be saved
            currentLen = 2
            permutations = {}
            permutAfterFirstFilter = {}
            segmentFilter = {0:[],1:[],2:[],3:[],4:[],5:[],6:[]}
            for pattern in signalPattern:
                # Save permutations
                if len(pattern) != currentLen:
                    for digit, permut in permutations.items():
                        print(f"Permutations cleared for len {currentLen} digit n°{digit} : {permut} ")
                        permutAfterFirstFilter[digit] = permut
                        digitConfig = digitConfigDict[digit]
                        segmentFilter = registerPotentialSegment(permut, digitConfig, segmentFilter)
                    permutations = {}
                    currentLen = len(pattern)

                if len(pattern) != 0:
                    digits = lenToDigitDict[len(pattern)]
                    for digit in digits:
                        tmpPermutations = permutePattern(pattern)
                        if digit not in permutations.keys():
                            permutations[digit] = []
                        if len(pattern) != 2:
                            digitConfig = digitConfigDict[digit]
                            tmpPermutations = applyFilter(tmpPermutations, digitConfig, segmentFilter)
                        permutations[digit] += tmpPermutations

            segmentFilter = cleanFilter(permutAfterFirstFilter, segmentFilter)
            uniquePatterns = {}
            for digit, permut in permutAfterFirstFilter.items():
                digitConfig = digitConfigDict[digit]
                pattern = applyFilter(permut, digitConfig, segmentFilter)
                uniquePatterns[pattern[0]] = digit

            digitOutput = digitOutput[0].split()
            resultDigit = ""
            for digit in digitOutput:
                permutedDigit = permutePattern(digit)
                resultDigit += [str(uniquePatterns[i]) for i in permutedDigit if i in uniquePatterns][0]
            endResult += int(resultDigit)
            print("result : ", endResult)



if __name__ == '__main__':
    main()
