#!/usr/bin/env python3
import math

POINTS = {
    '(': 1,
    '[': 2,
    '{': 3,
    '<': 4
}

CHAR_PAIR = {
    ')': '(',
    ']': '[',
    '}': '{',
    '>': '<',
}


def checkCorruption(line, endingChar):
    lineScore = 0
    charSequence = []
    for char in line:
        if char in endingChar:
            if CHAR_PAIR[char] != charSequence[-1]:
                return []
            else:
                charSequence.pop()
        else:
            charSequence.append(char)
    return charSequence

def getCompleteSequenceScore(sequence):
    sequenceScore = 0
    for char in sequence[::-1]:
        sequenceScore *= 5
        sequenceScore += POINTS[char]
    return sequenceScore


def main():
    with open("input.txt", 'r') as inputFile:
        endingChar = list(CHAR_PAIR.keys())
        scores = []
        for line in inputFile:
            remainingSequence = checkCorruption(line.rstrip(), endingChar)
            if len(remainingSequence) != 0: # not corrupted
                scores.append(getCompleteSequenceScore(remainingSequence))
        scoreIndex = math.ceil(len(scores) / 2) - 1 # Check middle index
        scores = sorted(scores) # Sort by asc
        print("Score : ", scores[scoreIndex]) # Get middle score


if __name__ == '__main__':
    main()
