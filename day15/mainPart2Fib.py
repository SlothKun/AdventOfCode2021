#!/usr/bin/env python3
import sys
import timeit
import fibheap as fheap


class Cave:
    def __init__(self):
        self.unvisitedNodes = fheap.makefheap()
        self.nodeData = {}
        self.maxCoord = ''
        self.lastVisited = ''
        self.caveMap = []

    def loadMap(self):
        with open("input.txt", 'r') as inputFile:
            self.caveMap = [[int(value) for value in line.strip()] for line in inputFile]
            print(len(self.caveMap))

    def generateFullMap(self):
        self.caveMap = [
            [x+j+i if x+j+i <= 9 else (x+j+i) - 9 for j in range(5) for x in y]
            for i in range(5) for y in self.caveMap
        ]
        print(len(self.caveMap))

    def loadNodes(self):
        for lineIndex, line in enumerate(self.caveMap):
            for nodeIndex, node in enumerate(line):
                self.nodeData[(lineIndex, nodeIndex)] = ({
                    'weight': int(node),
                    'shortestDist': sys.maxsize,
                    'prevNode': ''
                })
        self.nodeData[(0,0)]["shortestDist"] = 0
        fheap.fheappush(self.unvisitedNodes, (0, (0, 0)))
        self.maxCoord = (len(self.caveMap)-1, len(self.caveMap)-1)

    def findNeighbours(self, nodeCoord):
        neighbours = []
        neighbours.append((nodeCoord[0], nodeCoord[1]-1))
        neighbours.append((nodeCoord[0], nodeCoord[1]+1))
        neighbours.append((nodeCoord[0]-1, nodeCoord[1]))
        neighbours.append((nodeCoord[0]+1, nodeCoord[1]))
        neighbours = [neighbour for neighbour in neighbours if neighbour[0] >= 0 and neighbour[0] < self.maxCoord[0] and
                                                                neighbour[1] >= 0 and neighbour[1] < self.maxCoord[1]]
        return neighbours

    def findShortestPath(self):
        currentNode = ""
        while self.unvisitedNodes.num_nodes != 0:
            currentNode = fheap.fheappop(self.unvisitedNodes)
            for neighbour in self.findNeighbours(currentNode[1]):
                distance = self.nodeData[currentNode[1]]['shortestDist'] + self.nodeData[neighbour]['weight']
                if distance < self.nodeData[neighbour]['shortestDist']:
                    self.nodeData[neighbour]['shortestDist'] = distance
                    self.nodeData[neighbour]['prevNode'] = currentNode[1]
                    fheap.fheappush(self.unvisitedNodes, (distance, neighbour))
        self.lastVisited = currentNode[1]

    def getLowRiskScore(self):
        node = self.lastVisited
        score = 0
        while not self.nodeData[node]['prevNode'] == '':
            score += self.nodeData[node]['weight']
            node = self.nodeData[node]['prevNode']
        print(f"{score=}")

    def main(self):
        self.loadMap()
        self.generateFullMap()
        self.loadNodes()
        self.findShortestPath()
        self.getLowRiskScore()


if __name__ == '__main__':
    cave = Cave()
    start = timeit.default_timer()
    cave.main()
    end = timeit.default_timer()
    print(f"Time : {end - start}")
