#!/usr/bin/env python3
import sys
import timeit
import numpy as np
import pprint

pp = pprint.PrettyPrinter(indent=1)

class Cave:
    def __init__(self):
        self.visitedNodes = []
        self.unvisitedNodes = []
        self.nodeData = {}
        self.maxCoord = ''
        self.lastVisited = ''
        self.caveMap = []

    def loadMap(self):
        with open("testInput.txt", 'r') as inputFile:
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
                self.unvisitedNodes.append((lineIndex, nodeIndex))
                self.nodeData[(lineIndex, nodeIndex)] = ({
                    'weight': int(node),
                    'shortestDist': sys.maxsize,
                    'prevNode': ''
                })
        self.nodeData[(0,0)]["shortestDist"] = 0
        self.maxCoord = (self.unvisitedNodes[-1][0], self.unvisitedNodes[-1][1])

    def findNeighbours(self, nodeCoord):
        neighbours = []
        neighbours.append((nodeCoord[0], nodeCoord[1]-1))
        neighbours.append((nodeCoord[0], nodeCoord[1]+1))
        neighbours.append((nodeCoord[0]-1, nodeCoord[1]))
        neighbours.append((nodeCoord[0]+1, nodeCoord[1]))
        neighbours = [neighbour for neighbour in neighbours if neighbour in self.unvisitedNodes and neighbour[0] >= 0 and neighbour[0] <= self.maxCoord[0] and
                                                                neighbour[1] >= 0 and neighbour[1] <= self.maxCoord[1]]
        return neighbours

    def findShortestPath(self):
        nodeLeft = len(self.unvisitedNodes)
        start = timeit.default_timer()
        while len(self.unvisitedNodes) != 0:
            currentNode = self.unvisitedNodes[0]
            del self.unvisitedNodes[0]
            if len(self.unvisitedNodes) == nodeLeft - 1000:
                end = timeit.default_timer()
                print(f"Node left : {len(self.unvisitedNodes)} - Time spent : {end - start}")
                nodeLeft = len(self.unvisitedNodes)
            self.lastVisited = currentNode

            neighbours = self.findNeighbours(currentNode)
            for neighbour in neighbours:
                distance = self.nodeData[currentNode]['shortestDist'] + self.nodeData[neighbour]['weight']
                if distance < self.nodeData[neighbour]['shortestDist']:
                    self.nodeData[neighbour]['shortestDist'] = distance
                    self.nodeData[neighbour]['prevNode'] = currentNode

    def getLowRiskScore(self):
        node = self.lastVisited
        score = 0
        while not self.nodeData[node]['prevNode'] == '':
            score += self.nodeData[node]['weight']
            self.caveMap[node[0]][node[1]] = 'X'
            node = self.nodeData[node]['prevNode']
        print(f"{score=}")
        pp.pprint(self.caveMap)


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
