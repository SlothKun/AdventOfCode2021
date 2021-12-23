#!/usr/bin/env python3
import timeit
import itertools as it

cubesOnRange = {}
# cubesOnRange[z] = {
#                       y1 : [ [x1Start, x1End], [...] ],
#                       y2 : [ [x2Start, x2End], [...] ]
#                   }

def loadSteps():
    with open("testInput.txt", 'r') as inputFile:
        steps = []
        for line in inputFile.readlines():
            step = {}
            data = line.rstrip().split()
            step['action'] = True if data[0] == "on" else False # define the action for the step
            allCoor = []
            for coor in data[1].split(','):
                extremities = [int(c) if i == 0 else int(c) for i, c in enumerate(coor[2:].split('..'))]
                allCoor.append(extremities)
            step['coors'] = allCoor
            steps.append(step)
    print(f"{len(steps)} Loaded")
    print(f"{steps[0]=}")
    return steps

def checkOverlap(xCoor, y, dim):
    if dim not in cubesOnRange.keys(): # Dim don't exist
        cubesOnRange[dim] = {} # Create it empty
        cubesOnRange[dim][y] = []
    elif y not in cubesOnRange[dim].keys(): # y don't exist in Dim
        cubesOnRange[dim][y] = []
    else:
        for xRange in cubesOnRange[dim][y]:
            # Range will return a len of 0 if no overlap
            print(range(max(xCoor[0], xRange[0]), min(xCoor[-1], xRange[-1])))
            if len(range(max(xCoor[0], xRange[0]), min(xCoor[-1], xRange[-1])+1)) != 0:
                return True
    return False # No overlaps dim

def subdiviseOverlap(xCoor, y, dim, action):
    # () -> red -> XRange
    # [] -> green -> XCoor
    print("h ; ", cubesOnRange[dim][y])
    allRangeInDimY = cubesOnRange[dim][y].copy()
    print(allRangeInDimY, " - ", xCoor)

    newRange = []
    for xIndex, xRange in enumerate(allRangeInDimY):
        if len(range(max(xCoor[0], xRange[0]), min(xCoor[-1], xRange[-1])+1)) != 0:
            if (xCoor[0] <= xRange[0] <= xRange[1] <= xCoor[1]): # Case when |-[-(-)-]-|
                if action:
                    #print("Xcoor save")
                    newRange.append(xCoor)
                else:
                    #print("Nothing Left")
                    #remove range completely
                    pass
            elif (xRange[0] <= xCoor[0] <= xCoor[1] <= xRange[1]): # Case when |--(--[--]--)--|
                if action:
                    #print("Xrange saved")
                    newRange.append(xRange)
                else:
                    #print("Split")
                    newRange.append([xRange[0], xCoor[0]])
                    newRange.append([xCoor[1], xRange[1]])
            else: # Case when |--(---[-)--]--| or |--[--(---]-)--|
                if action:
                    newRange.append([min(xCoor[0], xRange[0]), max(xCoor[1], xRange[1])])
                    #print("ON :", [min(xCoor[0], xRange[0]), max(xCoor[1], xRange[1])])
                else:
                    tmpRange = [max(xCoor[1], xRange[0]), max(xCoor[0], xRange[1])]
                    if tmpRange[0] > tmpRange[1]:
                        tmpRange = [min(xCoor[0], xRange[0]), min(xCoor[0], xRange[1])]
                    newRange.append(tmpRange)
                    #print("OFF :", newRange)
        else:
            newRange.append(xRange)
    cubesOnRange[dim][y] = newRange
    print("h1 : ", cubesOnRange[dim][y])

def sortY(dim, y):
    # TODO: sort array with itself
    # NOT FINISHED
    sorted = True
    while sorted:
        sorted = False
        newX = []
        #for
        #for fIndex, fElement in cubesOnRange[dim][y]:
        for sIndex, sElement in cubesOnRange[dim][y]:
            if sElement != fElement:
                if len(range(max(fElement[0], sElement[0]), min(fElement[-1], sElement[-1])+1)) != 0:
                    if (fElement[0] <= sElement[0] <= sElement[1] <= fElement[1]): # Case when |-[-(-)-]-|
                        newRange.append(fElement)
                    elif (sElement[0] <= fElement[0] <= fElement[1] <= sElement[1]): # Case when |--(--[--]--)--|
                        newRange.append(sElement)
                    else: # Case when |--(---[-)--]--| or |--[--(---]-)--|
                        newRange.append([min(fElement[0], sElement[0]), max(fElement[1], sElement[1])])



def applySteps(steps):
    for stepIndex, step in enumerate(steps):
        print(f"\nStep {stepIndex+1}/{len(steps)} :")
        dimMinMax = step['coors'][2]
        for dim in range(dimMinMax[0], dimMinMax[1]+1): # iterate through 'z' axis
            yMinMax = step['coors'][1]
            for y in range(yMinMax[0], yMinMax[1]+1):
                isOverlap = checkOverlap(step['coors'][0], y, dim)
                if isOverlap:
                    # TODO: subdivise until no overlaps
                    subdiviseOverlap(step['coors'][0], y, dim, step['action'])
                elif step['action']: # don't overlap and action is 'On'
                    # Append coordinates range to the dim
                    cubesOnRange[dim][y].append(step['coors'][0])
                    #print("On no overlap : ", cubesOnRange[dim][y])

def countOn():
    count = 0
    for dim, allY in cubesOnRange.items():
        for y, allX in allY.items():
            for x in allX:
                count += (x[1] - x[0])+1
    print(count)



def main():
    steps = loadSteps()
    applySteps(steps)
    print(cubesOnRange)
    # TODO: Count for each entry in the dict the nb of cube (for 2d we can do range of x * range of y to get it)
    countOn()
    #print("All on : ", allOn)

if __name__ == '__main__':
    start = timeit.default_timer()
    main()
    print("Time : ", timeit.default_timer() - start)
