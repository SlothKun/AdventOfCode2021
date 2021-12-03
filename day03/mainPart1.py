columns = {}
gammaRate = ""
epsilonRate = ""

def convertToInt(binary):
    return int(binary, 2)

with open("input.txt", "r") as file:
    # Setup the dict
    for i in range(0, len(file.readline().rstrip())):
        columns[i] = ""

    # Add each number to its corresponding column
    for line in file:
        for i in range(0, len(line.rstrip())):
            columns[i] += line[i]

    # for each column, get the most & least common bit and assign it to gamma or epsi
    for key, value in columns.items():
        if value.count('1') > value.count('0'):
            gammaRate += '1'
            epsilonRate += '0'
        else:
            gammaRate += '0'
            epsilonRate += '1'

    # Convert values from bin to int, multiply them and print the result
    print("final value: ", convertToInt(gammaRate) * convertToInt(epsilonRate))
