#!/usr/bin/env python3
import timeit
import itertools as it

def loadSteps():
    with open("testInput1.txt", 'r') as inputFile:
        steps = []
        for line in inputFile.readlines():
            step = {}
            data = line.rstrip().split()
            step['action'] = True if data[0] == "on" else False # define the action for the step
            allCoor = []
            for coor in data[1].split(','):
                start, end = coor[2:].split("..")
                allCoor.append((int(start), int(end)+1))
            step['cubesCoor'] = allCoor
            steps.append(step)
    print("Finished Loading")
    return steps

def genCubes(cubesCoor):
    start = timeit.default_timer()
    allRange = []
    for cubeCoor in cubesCoor:
        coorRange = [i for i in range(cubeCoor[0], cubeCoor[1])]
        allRange.append(coorRange)
    print("    gen in : ", timeit.default_timer() - start)
    return set(it.product(*allRange)) # Generate all combinaisons possible

def findAllOn(steps):
    allOn = set()
    for index, step in enumerate(steps):
        print(f"Step {index+1}/{len(steps)} :")
        cubes = genCubes(step['cubesCoor'])
        if step['action']:
            allOn.update(cubes)
        else:
            allOn = set(filter(lambda x: x not in cubes, allOn))
    return len(allOn)


def main():
    steps = loadSteps()
    allOn = findAllOn(steps)
    print("All on : ", allOn)

if __name__ == '__main__':
    start = timeit.default_timer()
    main()
    print("Time : ", timeit.default_timer() - start)
