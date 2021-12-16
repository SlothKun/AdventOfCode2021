#!/usr/bin/env python3
import sys
import timeit

class Cave:
    def __init__(self):
        self.visitedNodes = []
        self.unvisitedNodes = []
        self.nodeData = {}
        self.maxCoord = ''

    def loadNodes(self):
        with open("InputPart1.txt", 'r') as inputFile:
            for lineIndex, line in enumerate(inputFile):
                for nodeIndex, node in enumerate(line.rstrip()):
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
        while len(self.unvisitedNodes) != 0:
            currentNode = self.unvisitedNodes[0]

            self.visitedNodes.append(currentNode)
            del self.unvisitedNodes[0]

            neighbours = self.findNeighbours(currentNode)
            for neighbour in neighbours:
                distance = self.nodeData[currentNode]['shortestDist'] + self.nodeData[neighbour]['weight']
                if distance < self.nodeData[neighbour]['shortestDist']:
                    self.nodeData[neighbour]['shortestDist'] = distance
                    self.nodeData[neighbour]['prevNode'] = currentNode

    def getLowRiskScore(self):
        node = self.visitedNodes[-1]
        score = 0
        while not self.nodeData[node]['prevNode'] == '':
            score += self.nodeData[node]['weight']
            node = self.nodeData[node]['prevNode']
        print(f"{score=}")


    def main(self):
        self.loadNodes()
        self.findShortestPath()
        self.getLowRiskScore()


if __name__ == '__main__':
    cave = Cave()
    start = timeit.default_timer()
    cave.main()
    end = timeit.default_timer()
    print(f"Time : {end - start}")
