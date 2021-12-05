import pprint

pp = pprint.PrettyPrinter(indent=2)
MAX_X = 1000
MAX_Y = 1000
overlapNb = 0

def createMap():
    ventMap = []
    for x in range(MAX_X):
        ventMap.append([0 for y in range(MAX_Y)])
    return ventMap


inputFile = open("input.txt", 'r')

ventMap = createMap() # Create an empty 2D list of dim MAX_X x MAX_Y

for inputLine in inputFile:
    inputLine = inputLine.rstrip().replace(" -> ", ',')
    coordinates = [int(x) for x in inputLine.split(',')] # Get coordinates (converted to int)

    print("coor : ", coordinates)
    # Put together X coor and Y coor
    # Also sort them asc, will be useful later on
    xPair = sorted([coordinates[0], coordinates[2]])
    yPair = sorted([coordinates[1], coordinates[3]])

    # If XPair are equals, add 1 to every pos x,y (from y1 to y2)
    # Same goes for YPair but from x1 to x2
    # If there's an overlapping (pos = 2), increment the count
    if xPair[0] == xPair[1]:
        line = ventMap[xPair[0]]
        for y in range(yPair[0], yPair[1]+1):
            ventMap[xPair[0]][y] += 1
            if ventMap[xPair[0]][y] == 2:
                overlapNb += 1
    elif yPair[0] == yPair[1]:
        for x in range(xPair[0], xPair[1]+1):
            ventMap[x][yPair[0]] += 1
            if ventMap[x][yPair[0]] == 2:
                overlapNb += 1


#pp.pprint(ventMap)
print("Result : ", overlapNb)
