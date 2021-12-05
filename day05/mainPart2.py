MAX_X = 1000
MAX_Y = 1000
overlapNb = 0

def createMap():
    ventMap = []
    for x in range(MAX_X):
        ventMap.append([0 for y in range(MAX_Y)])
    return ventMap

def createListCoor(pair):
    step = 1 if pair[0] < pair[1] else -1
    coorList = list(range(pair[0], pair[1]+step, step))
    return coorList

def evenListLen(targetList, maxLen):
    while len(targetList) != maxLen:
        targetList.append(targetList[-1])
    return targetList

#inputFile = open("testInput.txt", 'r')
inputFile = open("input.txt", 'r')

ventMap = createMap() # Create an empty 2D list of dim MAX_X x MAX_Y

for inputLine in inputFile:
    inputLine = inputLine.rstrip().replace(" -> ", ',')
    coordinates = [int(x) for x in inputLine.split(',')] # Get coordinates (converted to int)

    # Put together X coor and Y coor
    xPair = [coordinates[1], coordinates[3]]
    yPair = [coordinates[0], coordinates[2]]

    # Get the list of all coordinates in X and Y
    xCoorList = createListCoor(xPair)
    yCoorList = createListCoor(yPair)

    # Even the list (repeat the last coordinates until same len)
    if len(xCoorList) < len(yCoorList):
        xCoorList = evenListLen(xCoorList, len(yCoorList))
    elif len(xCoorList) > len(yCoorList):
        yCoorList = evenListLen(yCoorList, len(xCoorList))

    # Mark coordinate on the map
    # Increment score when coor's marked 2 times exactly
    for i in range(0, len(yCoorList)):
        x = xCoorList[i]
        y = yCoorList[i]
        ventMap[x][y] += 1
        overlapNb += 1 if ventMap[x][y] == 2 else 0


print("Result : ", overlapNb)
