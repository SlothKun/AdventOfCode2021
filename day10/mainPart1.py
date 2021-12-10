#!/usr/bin/env python3

POINTS = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}

CHAR_PAIR = {
    ')': '(',
    ']': '[',
    '}': '{',
    '>': '<',
}


def checkScore(line, endingChar):
    lineScore = 0
    charSequence = []
    for char in line:
        if char in endingChar:
            if CHAR_PAIR[char] != charSequence[-1]:
                return POINTS[char]
            else:
                charSequence.pop()
        else:
            charSequence.append(char)
    return 0

def main():
    with open("input.txt", 'r') as inputFile:
        endingChar = list(CHAR_PAIR.keys())
        score = 0
        for line in inputFile:
            score += checkScore(line.rstrip(), endingChar)
        print("Score : ", score)


if __name__ == '__main__':
    main()
