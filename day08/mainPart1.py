#!/usr/bin/env python3



def main():
    segmentNb = [ 2, 4, 3, 7 ]
    result = 0
    with open("input.txt", 'r') as fileInput:
        for line in fileInput:
            digitsOutput = line.rstrip().split('|')[1]
            for digit in digitsOutput.split():
                if len(digit) in segmentNb:
                    result += 1
    print("result : ", result)




if __name__ == '__main__':
    main()
