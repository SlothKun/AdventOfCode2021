
nbOfIncrease = 0
stop = False

def addMeasurements(index, lines):
    """
    Add the measure and its 2 following ones
    """
    totalSum = 0
    for i in range(index, index+3):
        totalSum += int(lines[i])
    return totalSum

def checkValidity(index, lines):
    """
    Return True if we need to stop
    """
    return True if (index+2) >= len(lines) else False

with open("input.txt", "r") as file:
    lines = file.readlines()
    index = 0
    value = addMeasurements(index, lines);
    while not stop:
        tempValue = addMeasurements(index, lines)
        if tempValue > value:
            nbOfIncrease += 1
        index += 1
        value = tempValue
        stop = checkValidity(index, lines)

print("Increase : ", nbOfIncrease)
